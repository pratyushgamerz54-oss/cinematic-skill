#!/usr/bin/env python3
"""Build and record a 3D globe shot (three.js) for the film: countries filling in, routes drawing on
along great circles, markers with labels, and a camera that flies between keys.

  python3 make_globe.py --project my-film                  # every globe in globe.json, full recording
  python3 make_globe.py --project my-film --name empire --draft   # 8 fps timing pass, much faster
  python3 make_globe.py --project my-film --still 4.5      # one PNG at 4.5 s, to check a moment

Reads globe.json in the project:
  {"globes": [{
     "name": "empire", "seconds": 9, "fps": 30, "size": "1920x1080",
     "source": "assets/data/countries-50m.json", "object": "countries",     # same boundaries as map.json
     "look": "night",                                   # night (space) or board (dark cork brown)
     "places": {"Pella": [40.76, 22.52], "Babylon": [32.54, 44.42]},      # [lat, lon]
     "fills":   [{"names": ["Greece", "Macedonia"], "rgb": [214, 160, 40], "t_in": 0.8}],
     "routes":  [{"from": "Pella", "to": "Babylon", "t_in": 2.0, "dur": 2.0}],
     "markers": [{"place": "Babylon", "label": "बेबीलोन", "t_in": 3.8, "side": "right"}],
     "camera":  [{"t": 0, "lat": 20, "lon": 10, "dist": 4.2},
                 {"t": 4, "lat": 36, "lon": 40, "dist": 2.2, "tilt": 12}]
  }]}

Camera keys: lat/lon is the point the camera looks down on, dist is its distance from the centre in
earth radii (4.5 shows the whole globe, 1.6 a region), tilt (degrees) swings it south of that point
and aims at the surface for a horizon view, roll leans the frame. Keys ease in and out.

Labels use the project's fonts/label.ttf (Devanagari works when the font has it).
Needs the frame-capture skill (Open 3D Skills) for recording: it is found in .claude/skills,
~/.claude/skills, ~/.agents/skills or $FRAME_CAPTURE. Set CHROME_PATH if Playwright's own Chromium
is not installed. Writes assets/globe/<name>/ (the page) and assets/clips/<name>.mp4, and adds the
clip to clips.json so prep_clips.py picks it up.
"""
import argparse
import json
import os
import pathlib
import shutil
import socket
import subprocess
import sys
import time

from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "globe"
sys.path.insert(0, str(HERE))
from make_map import features, load  # noqa: E402

LOOKS = {
    "night": dict(background=[6, 8, 13], ocean=[18, 52, 70], land=[205, 199, 186], border=[120, 112, 100],
                  atmosphere=[120, 180, 255], stars=True, exposure=1.05),
    "board": dict(background=[34, 27, 22], ocean=[96, 176, 186], land=[226, 221, 211], border=[150, 142, 130],
                  atmosphere=[255, 226, 180], stars=False, exposure=1.0),
}
TEX_W = 8192


def unwrap(ring):
    """Ring longitudes made continuous (no 360-degree jumps), so a polygon across the antimeridian draws whole."""
    out, off, prev = [], 0.0, None
    for lon, lat in ring:
        if prev is not None:
            d = lon - prev
            if d > 180:
                off -= 360
            elif d < -180:
                off += 360
        out.append((lon + off, lat)); prev = lon
    return out


def px(lon, lat, W, H):
    return (lon + 180) / 360 * W, (90 - lat) / 180 * H


def draw_rings(d, rings, W, H, fill=None, outline=None, width=1):
    for rg in rings:
        u = unwrap(rg)
        for shift in (-360, 0, 360):
            pts = [px(lon + shift, lat, W, H) for lon, lat in u]
            if len(pts) > 2:
                d.polygon(pts, fill=fill, outline=None)
                if outline:
                    d.line(pts + [pts[0]], fill=outline, width=width, joint="curve")


def textures(g, feats, out):
    look = LOOKS[g.get("look", "night")]
    W, H = TEX_W, TEX_W // 2
    land, ocean, border = (tuple(g.get(k, look[k])) for k in ("land", "ocean", "border"))
    base = Image.new("RGB", (W, H), ocean); d = ImageDraw.Draw(base)
    for _, rings in feats:
        draw_rings(d, rings, W, H, fill=land)
    for _, rings in feats:
        draw_rings(d, rings, W, H, outline=border, width=3)
    base.save(out / "base.png", optimize=True)
    names = {n for n, _ in feats}
    for i, f in enumerate(g.get("fills", [])):
        missing = [n for n in f["names"] if n not in names]
        if missing:
            print(f"  warning: fill {i}: not in the boundaries: {missing}")
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        for n, rings in feats:
            if n in f["names"]:
                draw_rings(d, rings, W, H, fill=tuple(f["rgb"]) + (255,))
        for n, rings in feats:
            if n in f["names"]:
                draw_rings(d, rings, W, H, outline=tuple(int(c * 0.7) for c in f["rgb"]) + (255,), width=3)
        im.save(out / f"fill_{i}.png", optimize=True)


def find_frame_capture():
    cands = [os.environ.get("FRAME_CAPTURE")]
    for root in [pathlib.Path.cwd(), *pathlib.Path.cwd().parents, HERE, *HERE.parents]:
        cands.append(root / ".claude" / "skills" / "frame-capture")
    cands += [pathlib.Path.home() / p / "frame-capture" for p in (".claude/skills", ".agents/skills", ".codex/skills", ".cursor/skills")]
    for c in cands:
        if c and (pathlib.Path(c) / "scripts" / "record.py").exists():
            return pathlib.Path(c)
    sys.exit("frame-capture skill not found: install Open 3D Skills (https://github.com/Moh4696/open-3d-skills) "
             "or set FRAME_CAPTURE to its folder")


def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p


def chrome_env():
    env = dict(os.environ)
    if "CHROME_PATH" not in env:
        for p in ("/opt/pw-browsers/chromium",):
            if os.path.exists(p):
                env["CHROME_PATH"] = p
    return env


def record(page_dir, out_mp4, g, draft, still):
    fc = find_frame_capture()
    port = free_port()
    srv = subprocess.Popen([sys.executable, str(fc / "scripts" / "serve.py"), str(page_dir), "--port", str(port)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(50):
            try:
                socket.create_connection(("127.0.0.1", port), timeout=0.2).close(); break
            except OSError:
                time.sleep(0.1)
        url = f"http://127.0.0.1:{port}/index.html?record=1"
        if still is not None:
            return shoot_still(url, g, still, out_mp4.with_suffix(f".{still:.2f}.png"))
        fps = 8 if draft else g.get("fps", 30)
        cmd = [sys.executable, str(fc / "scripts" / "record.py"), url, str(out_mp4), "--seconds", str(g["seconds"]),
               "--fps", str(fps), "--size", g.get("size", "1920x1080"), "--ready", "window.__ready === true"]
        subprocess.run(cmd, check=True, env=chrome_env())
        return out_mp4
    finally:
        srv.terminate()


def shoot_still(url, g, t, out_png):
    from playwright.sync_api import sync_playwright
    w, h = map(int, g.get("size", "1920x1080").split("x"))
    with sync_playwright() as p:
        exe = chrome_env().get("CHROME_PATH")
        b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(url); pg.wait_for_function("window.__ready === true", timeout=120000)
        pg.evaluate(f"window.__recordFrame({t})"); pg.wait_for_timeout(400)
        pg.screenshot(path=str(out_png)); b.close()
    print(f"still: {out_png}")
    return out_png


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project", required=True)
    ap.add_argument("--name", help="only this globe")
    ap.add_argument("--draft", action="store_true", help="8 fps timing pass")
    ap.add_argument("--still", type=float, help="one PNG at this time instead of a recording")
    a = ap.parse_args()
    proj = pathlib.Path(a.project).resolve()
    spec = json.loads((proj / "globe.json").read_text())
    for g in spec["globes"]:
        if a.name and g["name"] != a.name:
            continue
        page = proj / "assets" / "globe" / g["name"]
        if page.exists():
            shutil.rmtree(page)
        shutil.copytree(TEMPLATE, page)
        (page / "textures").mkdir(); (page / "fonts").mkdir()
        for role in ("label", "labelm", "cond"):
            f = proj / "fonts" / f"{role}.ttf"
            if f.exists():
                shutil.copy(f, page / "fonts" / "label.ttf"); break
        src = g.get("source", "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-50m.json")
        data = json.loads((proj / src).read_text()) if (proj / src).is_file() else load(src, proj / "assets" / "data")
        feats = features(data, g.get("object", "countries"))
        print(f"{g['name']}: drawing textures ({len(feats)} regions)")
        textures(g, feats, page / "textures")
        look = LOOKS[g.get("look", "night")]
        cfg = {"seconds": g["seconds"], "background": g.get("background", look["background"]),
               "atmosphere": g.get("atmosphere", look["atmosphere"]), "stars": g.get("stars", look["stars"]),
               "exposure": g.get("exposure", look["exposure"]), "fov": g.get("fov", 32),
               "route_rgb": g.get("route_rgb", [255, 250, 240]), "places": g.get("places", {}),
               "fills": [{k: v for k, v in f.items() if k != "names"} for f in g.get("fills", [])],
               "routes": g.get("routes", []), "markers": g.get("markers", []), "camera": g["camera"]}
        for r in cfg["routes"]:
            for k in ("from", "to"):
                if isinstance(r[k], str) and r[k] not in cfg["places"]:
                    sys.exit(f"route place {r[k]!r} is not in places")
        (page / "config.json").write_text(json.dumps(cfg, ensure_ascii=False))
        clips = proj / "assets" / "clips"; clips.mkdir(parents=True, exist_ok=True)
        out = clips / (f"{g['name']}_draft.mp4" if a.draft else f"{g['name']}.mp4")
        res = record(page, out, g, a.draft, a.still)
        if a.still is None and not a.draft:
            cp = proj / "clips.json"
            cj = json.loads(cp.read_text()) if cp.exists() else {"fps": 30, "clips": []}
            if not any(c["id"] == g["name"] for c in cj["clips"]):
                cj["clips"].append({"id": g["name"], "file": f"assets/clips/{g['name']}.mp4",
                                    "what": g.get("what", "3D globe shot"), "credit": "Made in code (three.js); boundaries: Natural Earth",
                                    "license": "Own work"})
                cp.write_text(json.dumps(cj, indent=1, ensure_ascii=False) + "\n")
            print(f"{g['name']}: {res}  (in clips.json; run prep_clips.py next)")


if __name__ == "__main__":
    main()
