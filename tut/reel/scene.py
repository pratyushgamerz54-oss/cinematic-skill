"""तूतनख़ामुन: the ~63-second vertical reel (1080x1920), in the fixed reel format.

THE REEL FORMAT (the same on every beat, so the reel reads as one consistent piece):
  top     a story-style progress bar (one segment per beat) and the series tag
  head    one hook headline per beat, same place and size: yellow bar; red only for the opening
          and closing questions to the viewer
  window  one 16:9 media window with the same frame on every beat (clip, photo, map or document),
          an exhibit tag on its top-left corner ("प्रमाण 01", "प्रतीकात्मक 3D मॉडल") and a
          source line under it
  bottom  the burned-in captions (bottom quarter, highlighter style)
The overlay is drawn with engine.Hud, so it never moves; only the media changes. Backgrounds follow the
beat's emotion with film.mood. The reel has its own script and its own recording (reel/script.json, REEL);
line 9 is left out of the read (reel_cut). Render: render.py --project tut/reel --size 1080x1920
"""
from engine import (HILITE, BigText, Card, Clip, Counter, Film, Hud, Item, PenMark, Print, Stamp, draw_text,
                    ease_out_cubic, paint, ramp)
import skia

CREAM = (244, 240, 232)
DARK = (26, 22, 20)
RED = (200, 40, 30)
GREY = (170, 164, 156)

# screen layout in 4K px from the frame centre (frame is 3840 x 6827 at 1080x1920)
WIN_W, WIN_CY = 3600, -300
WIN_H = WIN_W * 9 / 16
CAM_Y = -250                       # camera centre in world y; the window centre sits at CAM_Y + WIN_CY


class ProgressBar(Item):
    """Story-style segmented progress bar: past beats full, the current one filling, future ones faint."""
    z = 96

    def __init__(self, spans, y=-3230, w=3400, h=22, gap=36):
        super().__init__(-1)
        self.spans, self.y, self.w, self.h, self.gap = spans, y, w, h, gap

    def draw(self, c, res, t):
        n = len(self.spans); sw = (self.w - self.gap * (n - 1)) / n
        for k, (a, b) in enumerate(self.spans):
            x = -self.w / 2 + k * (sw + self.gap)
            c.drawRoundRect(skia.Rect.MakeXYWH(x, self.y, sw, self.h), 11, 11, paint(CREAM, 0.25))
            u = min(max((t - a) / max(b - a, 0.1), 0.0), 1.0)
            if u > 0:
                c.drawRoundRect(skia.Rect.MakeXYWH(x, self.y, sw * u, self.h), 11, 11, paint(RED if k < n - 1 else CREAM, 0.95))


class SeriesTag(Item):
    """Fixed series tag under the progress bar."""
    z = 96

    def __init__(self, text, y=-2960):
        super().__init__(-1)
        self.text, self.y = text, y

    def draw(self, c, res, t):
        c.drawRect(skia.Rect.MakeXYWH(-1700, self.y - 100, 34, 120), paint(RED))
        draw_text(c, res, self.text, -1630, self.y, 118, "label", CREAM, 0.92, 0.04, "left")


class Window(Item):
    """The media window frame: thin cream border with corner ticks, a soft shadow outside it."""
    z = 94

    def draw(self, c, res, t):
        r = skia.Rect.MakeXYWH(-WIN_W / 2, WIN_CY - WIN_H / 2, WIN_W, WIN_H)
        c.drawRect(r.makeOutset(26, 26), paint((0, 0, 0), 0.0, stroke=40))
        c.drawRect(r, paint(CREAM, 0.85, stroke=10))
        k = 150
        for (x, y, sx, sy) in [(r.left(), r.top(), 1, 1), (r.right(), r.top(), -1, 1), (r.left(), r.bottom(), 1, -1), (r.right(), r.bottom(), -1, -1)]:
            c.drawLine(x - sx * 30, y + sy * k, x - sx * 30, y - sy * 30, paint(RED, 0.95, stroke=16))
            c.drawLine(x - sx * 30, y - sy * 30, x + sx * k, y - sy * 30, paint(RED, 0.95, stroke=16))


class Source(Item):
    """Source line under the window; types on."""
    z = 96

    def __init__(self, text, t_in, t_out):
        super().__init__(t_in, t_out)
        self.text = text

    def draw(self, c, res, t):
        a = ramp(t, self.t_in, 0.3) * self.fade(t)
        if a <= 0:
            return
        n = len(self.text) * ease_out_cubic(ramp(t, self.t_in, 0.6))
        draw_text(c, res, self.text, -WIN_W / 2, WIN_CY + WIN_H / 2 + 170, 92, "labelm", GREY, a, 0.02, "left", reveal=n + 0.999)


def build_film(doc):
    L, E, W = doc.L, doc.E, doc.W
    film = Film(doc.duration, fps=30, look="wall")
    order = [s["id"] for s in doc.timing["segments"]]
    X = {i: k * 7000 for k, i in enumerate(order)}
    hud = lambda item: film.add(Hud(film, item))

    # ---- the beats: lines, headline, exhibit tag, source line, mood (from reel/script.json)
    beats = [
        dict(lines=[1], head="मिटाया गया राजा, अमर कैसे?", q=True, tag="सवाल", src=None, mood="tension"),
        dict(lines=[2], head="9 में राजा, 19 में मौत", tag="प्रमाण 01", src="सोने का मुखौटा · मिस्री म्यूज़ियम, काहिरा (विकिमीडिया कॉमन्स)", mood="archive"),
        dict(lines=[3], head="नाम मिटा दिया गया", tag="प्रमाण 02", src="अबीडोस की राजाओं की सूची में अमरना के राजा नहीं", mood="evidence"),
        dict(lines=[4], head="3000 साल तक छिपी कब्र", tag="प्रतीकात्मक 3D मॉडल", src="राजाओं की घाटी, लक्सर · KV62 और KV9", mood="archive"),
        dict(lines=[5], head="1922: “wonderful things”", tag="प्रमाण 03", src="हावर्ड कार्टर की किताब (1923) के मुताबिक़", mood="archive"),
        dict(lines=[6], head="5,398 चीज़ें · 110 किलो सोना", tag="प्रतीकात्मक 3D मॉडल", src="ग्रिफ़िथ इंस्टीट्यूट कैटलॉग", mood="evidence"),
        dict(lines=[7], head="हत्या?", tag="प्रतीकात्मक 3D मॉडल", src="एक्स-रे, 1968 (आर. जी. हैरिसन) · असली ममी नहीं", mood="tension"),
        dict(lines=[8], head="डीएनए: मलेरिया + बीमारी", tag="प्रमाण 04", src="हवास और साथी, JAMA, 2010", mood="intel"),
        dict(lines=[10], head="आप क्या सोचते हैं?", q=True, tag="सवाल", src=None, mood="verdict"),
    ]
    beats = [b for b in beats if b["lines"][0] in doc.seg]
    spans = []
    for k, b in enumerate(beats):
        a = 0.0 if k == 0 else L(b["lines"][0]) - 0.3
        z = doc.duration if k == len(beats) - 1 else L(beats[k + 1]["lines"][0]) - 0.3
        b["t0"], b["t1"] = a, z
        spans.append((a, z))

    # ---- the fixed overlay
    hud(ProgressBar(spans))
    hud(SeriesTag("तूतनख़ामुन · एक जाँच"))
    hud(Window(-1))
    for b in beats:
        q = b.get("q")
        hud(BigText(b["head"], 0, -2350, 300 if len(b["head"]) < 22 else 260, b["t0"] + 0.05, t_out=b["t1"] - 0.55,
                    rgb=CREAM if q else DARK, bar=RED if q else HILITE, bar_h=0.92, shadow=False, hit=None, sfx=False))
        hud(BigText(b["tag"], -WIN_W / 2 + 40 + len(b["tag"]) * 22, WIN_CY - WIN_H / 2 - 60, 100, b["t0"] + 0.25, t_out=b["t1"] - 0.55,
                    font="label", rgb=CREAM, bar=RED, bar_h=0.92, shadow=False, grunge=False, hit=None, sfx=False))
        if b["src"]:
            hud(Source(b["src"], b["t0"] + 0.6, b["t1"] - 0.55))
        film.mood(b["t0"], b["mood"], 0.5)
        x = X[b["lines"][0]]
        film.shot(b["t0"] + (0.0 if b is beats[0] else 0.3), x, CAM_Y, 1.0, 0.0, radius=20000, strength=0.0)
        film.shot(b["t1"] - 0.05, x, CAM_Y, 1.0, 0.0, radius=20000, strength=0.0)

    MY = CAM_Y + WIN_CY                     # world y of the window centre
    B = {b["lines"][0]: b for b in beats}

    def clip(cid, i, t0, t1, start=0.0):
        film.add(Clip(doc.clip(cid), X[i], MY, WIN_W, t_in=t0, t_out=t1, start=start, frame=False, z=40))

    def still(key, i, t0):
        film.add(Print(key, X[i], MY, WIN_W, t_in=t0, border=0.0, pin=False, aspect=16 / 9, sfx=False))

    # ---- the media, one beat at a time, always inside the window
    clip("hf_rq", 1, 0.0, B[1]["t1"] + 0.3)
    film.cue("heartbeat", W(1, "मिटा"), 0.8)
    still("P03", 2, B[2]["t0"])
    film.add(Counter(X[2] + 1300, MY + 250, 520, 9, W(2, "नौ") - 0.4, dur=0.6, caption="साल: राजा", rgb=(226, 176, 72)))
    film.add(Counter(X[2] - 1300, MY + 250, 520, 19, W(2, "उन्नीस") - 0.5, dur=0.7, caption="साल: मौत", rgb=CREAM, start=9))
    for k, nm in enumerate(["अख़ेनातेन", "तूतनख़ामुन", "आय"]):
        film.add(Card(X[3], MY - 600 + k * 620, 2400, 520, B[3]["t0"] + 0.3 + 0.3 * k, title=nm, rgb=(236, 230, 220), text_rgb=(34, 32, 30),
                      accent=(226, 176, 72), title_size=230))
        film.add(PenMark("strike", X[3], MY - 600 + k * 620, 2000, 0, t_in=W(3, "मिटा") - 0.2 + 0.2 * k, dur=0.3, width=50, seed=40 + k))
    film.add(Stamp("मिटाया", X[3] + 900, MY + 500, size=380, rot=-9, t_in=W(3, "मिटा") + 0.5))
    clip("valley", 4, B[4]["t0"], B[4]["t1"] + 0.3, start=1.5)
    clip("door", 5, B[5]["t0"], W(5, "कहा") - 0.1, start=0.8)
    clip("hf_wonder", 5, W(5, "कहा") - 0.1, B[5]["t1"] + 0.3, start=2.2)
    clip("coffins", 6, B[6]["t0"], B[6]["t1"] + 0.3, start=2.0)
    film.add(Counter(X[6], MY + 650, 380, 5398, W(6, "पाँच") - 0.3, dur=1.0, caption="चीज़ें", rgb=(226, 176, 72)))
    clip("ctscan", 7, B[7]["t0"], B[7]["t1"] + 0.3, start=0.6)
    film.cue("heartbeat", W(7, "हत्या"), 0.8)
    clip("ctscan", 8, B[8]["t0"], B[8]["t1"] + 0.3, start=4.6)
    clip("hf_qend", 10, B[10]["t0"], doc.duration + 1)
    film.cue("boom", L(10), 0.5)

    film.fade_in, film.fade_out = 0.2, 1.0
    return film
