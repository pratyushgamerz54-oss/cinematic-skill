"""Thumbnails for एरिया 51: YouTube (1280x720) and the reel cover (1080x1920).

  python3 area51/thumbs.py   -> area51/out/thumbnail_youtube.jpg, area51/out/thumbnail_reel.jpg

Photos: Groom Lake from the air (Ken Lund, CC BY-SA 2.0) and the boundary sign (X51, CC BY-SA 3.0), both Wikimedia Commons.
Palette: night blue, radar teal, desert amber (the user asked for less red).
"""
import pathlib, sys
import numpy as np
import skia
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "skills" / "cinematic-film" / "scripts"))
from engine import Res, draw_text, paint, text_width  # noqa: E402

TEAL, AMBER, CREAM, INK, NIGHT, RED = (63, 224, 204), (255, 179, 71), (240, 244, 242), (12, 16, 20), (5, 9, 14), (224, 72, 58)
AIR = HERE / "assets/photos/P01_Groom_Lake_Area_51_North_of_Las_Vegas_Nevada_175.jpg"
SIGN = HERE / "assets/photos/P05_Wfm_x51_area51_warningsign.jpg"

def load(path, size, crop=None, sat=1.15, dark=0.0):
    im = Image.open(path).convert("RGB")
    if crop:
        w, h = im.size; im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    im = im.resize(size, Image.LANCZOS)
    a = np.asarray(im, np.float32); g = a.mean(2, keepdims=True); a = np.clip(g + (a - g) * sat, 0, 255) * (1 - dark)
    return skia.Image.fromarray(np.ascontiguousarray(np.dstack([a.astype(np.uint8), np.full(a.shape[:2], 255, np.uint8)])),
                                colorType=skia.ColorType.kRGBA_8888_ColorType)

def grad(c, x0, y0, x1, y1, a0, a1, rect):
    g = skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], [skia.Color(*NIGHT, a0), skia.Color(*NIGHT, a1)])
    p = skia.Paint(); p.setShader(g); c.drawRect(rect, p)

def vignette(c, W, H, s=0.7):
    g = skia.GradientShader.MakeRadial(skia.Point(W * 0.5, H * 0.5), max(W, H) * 0.75, [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, int(255 * s))])
    p = skia.Paint(); p.setShader(g); c.drawRect(skia.Rect.MakeWH(W, H), p)

def text(c, res, t, x, y, size, font, fg, bg=None, pad=0.18, align="left"):
    w = text_width(res, t, size, font); x0 = x - w / 2 if align == "center" else x
    if bg: c.drawRect(skia.Rect.MakeLTRB(x0 - size * pad, y - size * 0.92, x0 + w + size * pad, y + size * 0.3), paint(bg))
    draw_text(c, res, t, x0, y, size, font, fg, 1.0, 0.0); return w

def glow_ring(c, rect, rgb, w):
    for k, a in [(3.2, 0.12), (2.0, 0.25), (1.0, 1.0)]:
        c.drawOval(rect, paint(rgb, a, stroke=w * k))

def youtube(res, out):
    W, H = 1280, 720
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.Color(*NIGHT))
    c.drawImageRect(load(AIR, (1280, 960), sat=1.3), skia.Rect.MakeXYWH(180, -170, 1280, 960))
    c.drawRect(skia.Rect.MakeXYWH(0, 0, 260, H), paint(NIGHT)); grad(c, 260, 0, 700, 0, 245, 0, skia.Rect.MakeXYWH(260, 0, 460, H))
    vignette(c, W, H, 0.55)
    glow_ring(c, skia.Rect.MakeXYWH(680, 232, 460, 120), TEAL, 6)
    text(c, res, "एरिया 51", 44, 200, 168, "cond", AMBER)
    text(c, res, "अमेरिका का", 50, 330, 84, "cond", CREAM)
    text(c, res, "सबसे बड़ा राज़", 50, 450, 112, "cond", TEAL)
    text(c, res, "पूरा कच्चा चिट्ठा", 58, 600, 44, "label", INK, bg=AMBER)
    text(c, res, "1955 से आज तक · एक जाँच", 58, 676, 32, "labelm", CREAM)
    s.makeImageSnapshot().save(str(out), skia.kJPEG, 92)

def reel(res, out):
    W, H = 1080, 1920
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.Color(*NIGHT))
    c.drawImageRect(load(SIGN, (1300, 1460), crop=(0.0, 0.12, 0.56, 0.95), sat=1.2), skia.Rect.MakeXYWH(-160, 300, 1300, 1460))
    grad(c, 0, 380, 0, 720, 255, 0, skia.Rect.MakeLTRB(0, 380, W, 720)); grad(c, 0, 1300, 0, 1560, 0, 255, skia.Rect.MakeLTRB(0, 1300, W, 1560))
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, 400), paint(NIGHT)); c.drawRect(skia.Rect.MakeLTRB(0, 1560, W, H), paint(NIGHT))
    vignette(c, W, H, 0.4)
    text(c, res, "एरिया 51", W / 2, 270, 230, "cond", AMBER, align="center")
    text(c, res, "नाम लेना तक मना था", W / 2, 390, 76, "label", CREAM, align="center")
    text(c, res, "वहाँ छुपा क्या है?", W / 2, 1680, 124, "cond", TEAL, align="center")
    text(c, res, "एरिया 51 · एक जाँच", W / 2, 1810, 60, "label", INK, bg=AMBER, align="center")
    s.makeImageSnapshot().save(str(out), skia.kJPEG, 92)

if __name__ == "__main__":
    res = Res(1.0, HERE / "assets" / "prep", HERE / "fonts")
    (HERE / "out").mkdir(exist_ok=True)
    youtube(res, HERE / "out" / "thumbnail_youtube.jpg"); reel(res, HERE / "out" / "thumbnail_reel.jpg")
    print("area51/out/thumbnail_youtube.jpg, area51/out/thumbnail_reel.jpg")
