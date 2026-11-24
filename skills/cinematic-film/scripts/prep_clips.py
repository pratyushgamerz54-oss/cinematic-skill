#!/usr/bin/env python3
"""Prepare video clips for the film: extract each one as JPEG frames at the film's frame rate.

  python3 prep_clips.py --project my-film

Reads clips.json in the project:
  {"fps": 30,
   "clips": [
     {"id": "globe", "file": "assets/clips/globe.mp4", "what": "3D globe flight, Pella to the Beas",
      "credit": "Made in code (three.js)", "license": "Own work"},
     {"id": "ships", "file": "assets/clips/ships.mp4", "trim": [2.0, 8.5], "width": 1920, "grade": "sepia"}
   ]}

- file: any video ffmpeg reads (a frame-capture recording, an archive film, an AI clip).
- trim: [start, end] seconds of the source to keep. width: frame width to store (default 1920;
  use 3840 for a full-frame cutaway in a 4K render). grade: "natural" (default), "bw" or "sepia",
  matching the photos' look so clips and prints read as one set.

Writes assets/prep/clips/<id>/00001.jpg ... and meta.json {"id", "w", "h", "fps", "n", "seconds"}.
In scene.py:  Clip(doc.clip("globe"), x, y, w, t_in=..., start=0, rate=1, frame=True)
Credits: list clips beside the photos (fetch_commons.py credits only covers photos.json).
"""
import argparse
import json
import pathlib
import shutil
import subprocess
import sys

GRADES = {
    "natural": "eq=contrast=1.04:saturation=0.95",
    "bw": "hue=s=0,eq=contrast=1.12:brightness=-0.01",
    "sepia": "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131,eq=contrast=1.05",
}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project", required=True)
    ap.add_argument("--force", action="store_true", help="extract again even if the frames exist")
    a = ap.parse_args()
    proj = pathlib.Path(a.project)
    spec_p = proj / "clips.json"
    if not spec_p.exists():
        sys.exit(f"{spec_p} not found (see this script's help for the format)")
    spec = json.loads(spec_p.read_text())
    fps = spec.get("fps", 30)
    for c in spec["clips"]:
        src = proj / c["file"]
        if not src.exists():
            sys.exit(f"{c['id']}: {src} not found")
        out = proj / "assets" / "prep" / "clips" / c["id"]
        meta_p = out / "meta.json"
        if meta_p.exists() and not a.force and meta_p.stat().st_mtime > src.stat().st_mtime:
            print(f"{c['id']}: up to date"); continue
        shutil.rmtree(out, ignore_errors=True); out.mkdir(parents=True)
        vf = [f"fps={fps}", f"scale={c.get('width', 1920)}:-2:flags=lanczos", GRADES[c.get("grade", "natural")]]
        cmd = ["ffmpeg", "-v", "error", "-y"]
        if c.get("trim"):
            t0, t1 = c["trim"]; cmd += ["-ss", str(t0), "-t", str(t1 - t0)]
        cmd += ["-i", str(src), "-vf", ",".join(vf), "-q:v", "3", str(out / "%05d.jpg")]
        subprocess.run(cmd, check=True)
        frames = sorted(out.glob("*.jpg"))
        if not frames:
            sys.exit(f"{c['id']}: no frames extracted from {src}")
        from PIL import Image
        w, h = Image.open(frames[0]).size
        meta = {"id": c["id"], "w": w, "h": h, "fps": fps, "n": len(frames), "seconds": round(len(frames) / fps, 3)}
        meta_p.write_text(json.dumps(meta))
        print(f"{c['id']}: {len(frames)} frames {w}x{h} ({meta['seconds']} s)")


if __name__ == "__main__":
    main()
