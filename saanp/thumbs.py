"""Thumbnails for पिछवाड़े के साँप: YouTube (1280x720) and the reel cover (1080x1920).

  python3 saanp/thumbs.py        -> saanp/out/thumbnail_youtube.jpg, saanp/out/thumbnail_reel.jpg

Drawn with the film's engine (Devanagari shaped, the film's fonts), over the CIA aerial photo of the
Abbottabad compound (public domain) and a frame of the 3D globe.
"""
import pathlib
import sys

import numpy as np
import skia
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "skills" / "cinematic-film" / "scripts"))
from engine import Res, draw_text, paint, text_width  # noqa: E402

RED, CREAM, YEL, INK = (214, 40, 30), (246, 241, 232), (246, 205, 60), (22, 18, 16)


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


def youtube(res, out):
    W, H = 1280, 720
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.Color(8, 7, 7))
    globe = HERE / "assets" / "prep" / "clips" / "g_verdict" / "00240.jpg"
    if globe.exists():
        c.drawImage(load(globe, (W, H), dark=0.55, bw=False), 0, 0)
    # the photo, tilted, on the right
    c.save(); c.translate(905, 360); c.rotate(4)
    c.drawRect(skia.Rect.MakeXYWH(-330, -235, 660, 470), paint((0, 0, 0), 0.6, blur=30))
    c.drawRect(skia.Rect.MakeXYWH(-322, -228, 644, 456), paint((236, 232, 224)))
    c.drawImageRect(load(HERE / "assets" / "photos" / "P01_cia_aerial.jpg", (620, 432), crop=(0.48, 0.36, 0.94, 0.98), dark=0.05),
                    skia.Rect.MakeXYWH(-310, -216, 620, 432))
    c.drawOval(skia.Rect.MakeXYWH(-125, -120, 250, 140), paint(RED, 1.0, stroke=9))
    c.restore()
    vignette(c, W, H, 0.55)
    # words on the left
    text_block(c, res, "पिछवाड़े", 46, 230, 168, "cond", CREAM)
    text_block(c, res, "के साँप", 46, 395, 168, "cond", RED)
    snake(c, 52, 440, 520, 22, 12)
    text_block(c, res, "पाकिस्तान और आतंक: सबूत क्या कहते हैं?", 56, 545, 40, "label", INK, bg=YEL)
    text_block(c, res, "एबटाबाद से पहलगाम तक", 56, 618, 34, "labelm", CREAM)
    s.makeImageSnapshot().save(str(out), skia.kJPEG, 92)


def reel(res, out):
    W, H = 1080, 1920
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.Color(8, 7, 7))
    globe = HERE / "assets" / "prep" / "clips" / "g_abbottabad" / "00120.jpg"
    if globe.exists():
        c.drawImageRect(load(globe, (1920, 1080), dark=0.72, bw=False), skia.Rect.MakeXYWH(-420, 1380, 1920, 1080))
    c.save(); c.translate(540, 980); c.rotate(-3)
    c.drawRect(skia.Rect.MakeXYWH(-470, -330, 940, 660), paint((0, 0, 0), 0.6, blur=36))
    c.drawRect(skia.Rect.MakeXYWH(-460, -320, 920, 640), paint((236, 232, 224)))
    c.drawImageRect(load(HERE / "assets" / "photos" / "P01_cia_aerial.jpg", (890, 610), crop=(0.48, 0.36, 0.94, 0.98), dark=0.05),
                    skia.Rect.MakeXYWH(-445, -305, 890, 610))
    c.drawOval(skia.Rect.MakeXYWH(-170, -165, 340, 195), paint(RED, 1.0, stroke=12))
    c.restore()
    vignette(c, W, H, 0.5)
    text_block(c, res, "पिछवाड़े", W / 2, 330, 230, "cond", CREAM, align="center")
    text_block(c, res, "के साँप", W / 2, 560, 230, "cond", RED, align="center")
    snake(c, 260, 620, 820, 26, 14)
    text_block(c, res, "पाकिस्तान और आतंक", W / 2, 1500, 76, "label", INK, bg=YEL, align="center")
    text_block(c, res, "सबूत क्या कहते हैं?", W / 2, 1640, 70, "label", CREAM, align="center")
    s.makeImageSnapshot().save(str(out), skia.kJPEG, 92)


if __name__ == "__main__":
    res = Res(1.0, HERE / "assets" / "prep", HERE / "fonts")
    (HERE / "out").mkdir(exist_ok=True)
    youtube(res, HERE / "out" / "thumbnail_youtube.jpg")
    reel(res, HERE / "out" / "thumbnail_reel.jpg")
    print("saanp/out/thumbnail_youtube.jpg, saanp/out/thumbnail_reel.jpg")
