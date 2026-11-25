"""Thumbnails for तूतनख़ामुन: YouTube (1280x720) and the reel cover (1080x1920).

  python3 tut/thumbs.py        -> tut/out/thumbnail_youtube.jpg, tut/out/thumbnail_reel.jpg

Drawn with the film's engine over the gold mask (Roland Unger, public domain) and the scan diagram.
"""
import pathlib
import sys

import numpy as np
import skia
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "skills" / "cinematic-film" / "scripts"))
from engine import Res, draw_text, paint, text_width  # noqa: E402

RED, CREAM, YEL, INK, GOLD = (214, 40, 30), (246, 241, 232), (246, 205, 60), (22, 18, 16), (232, 178, 70)


def load(path, size, crop=None, dark=0.0, bw=True):
    im = Image.open(path).convert("RGB")
    if crop:
        w, h = im.size; im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    if bw:
        im = im.convert("L").convert("RGB")
    im = im.resize(size, Image.LANCZOS)
    a = np.asarray(im, np.float32) * (1 - dark)
    return skia.Image.fromarray(np.ascontiguousarray(np.dstack([a.astype(np.uint8), np.full(a.shape[:2], 255, np.uint8)])),
                                colorType=skia.ColorType.kRGBA_8888_ColorType)


def vignette(c, W, H, strength=0.8):
    g = skia.GradientShader.MakeRadial(skia.Point(W * 0.5, H * 0.5), max(W, H) * 0.75,
                                       [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, int(255 * strength))])
    p = skia.Paint(); p.setShader(g); c.drawRect(skia.Rect.MakeWH(W, H), p)


def text_block(c, res, txt, x, y, size, font, fg, bg=None, pad=0.18, align="left"):
    w = text_width(res, txt, size, font)
    x0 = x - w / 2 if align == "center" else x
    if bg:
        c.drawRect(skia.Rect.MakeLTRB(x0 - size * pad, y - size * 0.92, x0 + w + size * pad, y + size * 0.3), paint(bg))
    draw_text(c, res, txt, x0, y, size, font, fg, 1.0, 0.0)
    return w


def snake(c, x0, y0, x1, amp, width, rgb=RED):
    p = skia.Path(); p.moveTo(x0, y0); n = 4; seg = (x1 - x0) / n
    for i in range(n):
        p.cubicTo(x0 + seg * (i + 0.33), y0 - amp, x0 + seg * (i + 0.66), y0 + amp, x0 + seg * (i + 1), y0)
    c.drawPath(p, paint(rgb, 1.0, stroke=width))


MASK = HERE / "assets" / "photos" / "P03_CairoEgMuseumTaaMaskMostlyPhotographed.jpg"


def youtube(res, out):
    W, H = 1280, 720
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.Color(8, 6, 4))
    # the mask fills the right side, in colour (gold is the story)
    c.drawImageRect(load(MASK, (600, 750), crop=(0.08, 0.06, 0.92, 0.98), dark=0.0, bw=False), skia.Rect.MakeXYWH(650, -10, 600, 750))
    g = skia.GradientShader.MakeLinear([skia.Point(640, 0), skia.Point(860, 0)], [skia.Color(8, 6, 4, 255), skia.Color(8, 6, 4, 0)])
    p = skia.Paint(); p.setShader(g); c.drawRect(skia.Rect.MakeXYWH(640, 0, 230, H), p)
    vignette(c, W, H, 0.5)
    c.drawOval(skia.Rect.MakeXYWH(860, 150, 270, 330), paint(RED, 1.0, stroke=9))
    text_block(c, res, "तूतनख़ामुन", 46, 200, 150, "cond", GOLD)
    text_block(c, res, "हत्या", 50, 380, 170, "cond", RED)
    text_block(c, res, "या बीमारी?", 50, 530, 120, "cond", CREAM)
    text_block(c, res, "मिटाया गया राजा: एक जाँच", 56, 625, 40, "label", INK, bg=YEL)
    text_block(c, res, "3,300 साल पुराना रहस्य", 56, 690, 32, "labelm", CREAM)
    s.makeImageSnapshot().save(str(out), skia.kJPEG, 92)


def reel(res, out):
    W, H = 1080, 1920
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.Color(8, 6, 4))
    c.drawImageRect(load(MASK, (1080, 1350), crop=(0.0, 0.03, 1.0, 1.0), bw=False), skia.Rect.MakeXYWH(0, 420, 1080, 1350))
    for y0, y1, a0, a1 in [(380, 700, 255, 0), (1450, 1920, 0, 255)]:
        g = skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)], [skia.Color(8, 6, 4, a0), skia.Color(8, 6, 4, a1)])
        p = skia.Paint(); p.setShader(g); c.drawRect(skia.Rect.MakeLTRB(0, y0, W, y1), p)
    vignette(c, W, H, 0.45)
    c.drawOval(skia.Rect.MakeXYWH(330, 700, 420, 520), paint(RED, 1.0, stroke=12))
    text_block(c, res, "तूतनख़ामुन", W / 2, 260, 210, "cond", GOLD, align="center")
    text_block(c, res, "19 साल का राजा", W / 2, 390, 84, "label", CREAM, align="center")
    c.drawRect(skia.Rect.MakeLTRB(0, 1470, W, 1800), paint((8, 6, 4), 0.82))
    text_block(c, res, "हत्या या बीमारी?", W / 2, 1600, 120, "cond", RED, align="center")
    text_block(c, res, "मिटाया गया राजा: एक जाँच", W / 2, 1740, 64, "label", INK, bg=YEL, align="center")
    s.makeImageSnapshot().save(str(out), skia.kJPEG, 92)


if __name__ == "__main__":
    res = Res(1.0, HERE / "assets" / "prep", HERE / "fonts")
    (HERE / "out").mkdir(exist_ok=True)
    youtube(res, HERE / "out" / "thumbnail_youtube.jpg")
    reel(res, HERE / "out" / "thumbnail_reel.jpg")
    print("tut/out/thumbnail_youtube.jpg, tut/out/thumbnail_reel.jpg")
