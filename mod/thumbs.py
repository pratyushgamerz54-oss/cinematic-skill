"""Thumbnails for पाँच पल, जिन्होंने दुनिया बदल दी: YouTube (1280x720) and the reel cover (1080x1920).

  python3 mod/thumbs.py   -> mod/out/thumbnail_youtube.jpg, mod/out/thumbnail_reel.jpg

Five photo strips, one per turning point (Wikimedia Commons, credits in credits.md), with the year on each.
Palette: archive gold, radar teal; red only for the one "ना".
"""
import glob, pathlib, sys
import numpy as np
import skia
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "skills" / "cinematic-film" / "scripts"))
from engine import Res, draw_text, paint, text_width  # noqa: E402

GOLD, TEAL, CREAM, INK, NIGHT, RED = (232, 194, 122), (63, 224, 204), (244, 238, 228), (14, 12, 10), (8, 7, 6), (224, 72, 58)
# (photo id, crop l,t,r,b as fractions, year, sepia?)
STRIPS = [("P01", (0.30, 0.05, 0.72, 0.95), "1914", True), ("P07", (0.15, 0.0, 0.85, 0.9), "1928", True),
          ("P13", (0.25, 0.1, 0.75, 0.95), "1962", True), ("P15", (0.15, 0.0, 0.85, 0.9), "1983", False),
          ("P18", (0.1, 0.05, 0.9, 0.95), "1989", False)]

def photo(pid):
    f = sorted(glob.glob(str(HERE / "assets/photos" / f"{pid}_*")))
    return f[0] if f else None

def load(path, size, crop, sepia):
    im = Image.open(path).convert("RGB"); w, h = im.size
    im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    tw, th = size; s = max(tw / im.width, th / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    l, t = (im.width - tw) // 2, (im.height - th) // 2; im = im.crop((l, t, l + tw, t + th))
    a = np.asarray(im, np.float32); g = a.mean(2, keepdims=True)
    a = np.clip(g * np.array([1.08, 0.94, 0.74]), 0, 255) if sepia else np.clip(g + (a - g) * 1.1, 0, 255)
    return skia.Image.fromarray(np.ascontiguousarray(np.dstack([a.astype(np.uint8), np.full(a.shape[:2], 255, np.uint8)])),
                                colorType=skia.ColorType.kRGBA_8888_ColorType)

def grad(c, x0, y0, x1, y1, a0, a1, rect):
    g = skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], [skia.Color(*NIGHT, a0), skia.Color(*NIGHT, a1)])
    p = skia.Paint(); p.setShader(g); c.drawRect(rect, p)

def text(c, res, t, x, y, size, font, fg, bg=None, pad=0.18, align="left"):
    w = text_width(res, t, size, font); x0 = x - w / 2 if align == "center" else x
    if bg: c.drawRect(skia.Rect.MakeLTRB(x0 - size * pad, y - size * 0.92, x0 + w + size * pad, y + size * 0.3), paint(bg))
    draw_text(c, res, t, x0, y, size, font, fg, 1.0, 0.0); return w

def strips(c, res, x, y, w, h, gap, vertical, ysize):
    n = len(STRIPS)
    for i, (pid, crop, yr, sep) in enumerate(STRIPS):
        if vertical: sw, sh = (w - gap * (n - 1)) / n, h; rx, ry = x + i * (sw + gap), y
        else: sw, sh = w, (h - gap * (n - 1)) / n; rx, ry = x, y + i * (sh + gap)
        r = skia.Rect.MakeXYWH(rx, ry, sw, sh); f = photo(pid)
        if f: c.drawImageRect(load(f, (int(sw), int(sh)), crop, sep), r)
        else: c.drawRect(r, paint((40, 34, 28)))
        grad(c, 0, ry + sh * 0.55, 0, ry + sh, 0, 230, skia.Rect.MakeXYWH(rx, ry + sh * 0.55, sw, sh * 0.45))
        c.drawRect(r, paint(GOLD, 0.9, stroke=3))
        text(c, res, yr, rx + sw / 2, ry + sh - ysize * 0.35, ysize, "cond", GOLD if i != 2 else TEAL, align="center")

def youtube(res, out):
    W, H = 1280, 720
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.Color(*NIGHT))
    strips(c, res, 24, 250, W - 48, 446, 10, True, 64)
    text(c, res, "पाँच पल", 40, 178, 176, "cond", GOLD)
    text(c, res, "जिन्होंने", 560, 110, 70, "cond", CREAM)
    text(c, res, "दुनिया बदल दी", 560, 196, 92, "cond", TEAL)
    text(c, res, "हर पल के पीछे: एक छोटी सी ग़लती", 1016, 232, 26, "label", INK, bg=GOLD, align="center")
    s.makeImageSnapshot().save(str(out), skia.kJPEG, 92)

def reel(res, out):
    W, H = 1080, 1920
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.Color(*NIGHT))
    strips(c, res, 60, 470, W - 120, 1150, 14, False, 96)
    text(c, res, "पाँच पल", W / 2, 260, 240, "cond", GOLD, align="center")
    text(c, res, "जिन्होंने दुनिया बदल दी", W / 2, 390, 84, "label", CREAM, align="center")
    text(c, res, "एक ग़लती, दुनिया बदली?", W / 2, 1760, 104, "cond", TEAL, align="center")
    text(c, res, "पाँच पल · एक जाँच", W / 2, 1870, 54, "label", INK, bg=GOLD, align="center")
    s.makeImageSnapshot().save(str(out), skia.kJPEG, 92)

if __name__ == "__main__":
    res = Res(1.0, HERE / "assets" / "prep", HERE / "fonts")
    (HERE / "out").mkdir(exist_ok=True)
    youtube(res, HERE / "out" / "thumbnail_youtube.jpg"); reel(res, HERE / "out" / "thumbnail_reel.jpg")
    print("mod/out/thumbnail_youtube.jpg, mod/out/thumbnail_reel.jpg")
