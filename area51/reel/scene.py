"""एरिया 51: the ~63-second vertical reel (1080x1920), in the fixed reel format.

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
line 3 is left out of the read (reel_cut). Render: render.py --project area51/reel --size 1080x1920
"""
from engine import (HILITE, Atmos, BigText, Card, Clip, Counter, Film, Hud, Item, PenMark, Print, Stamp, draw_text,
                    ease_out_cubic, paint, ramp)
import skia

CREAM = (244, 240, 232)
DARK = (26, 22, 20)
RED = (200, 40, 30)
TEAL = (63, 224, 204)
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
                c.drawRoundRect(skia.Rect.MakeXYWH(x, self.y, sw * u, self.h), 11, 11, paint(TEAL if k < n - 1 else CREAM, 0.95))


class SeriesTag(Item):
    """Fixed series tag under the progress bar."""
    z = 96

    def __init__(self, text, y=-2960):
        super().__init__(-1)
        self.text, self.y = text, y

    def draw(self, c, res, t):
        c.drawRect(skia.Rect.MakeXYWH(-1700, self.y - 100, 34, 120), paint(TEAL))
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
        dict(lines=[1], head="नाम लेना तक मना था, क्यों?", q=True, tag="सवाल", src=None, mood="radar"),
        dict(lines=[2], head="गेट पर: गोली की इजाज़त", tag="प्रमाण 01", src="सीमा का बोर्ड, नेवाडा · विकिमीडिया कॉमन्स (X51, CC BY-SA 3.0)", mood="evidence"),
        dict(lines=[4], head="1955: U-2, 60,000 फ़ीट ऊपर", tag="प्रमाण 02 · NASA फ़ुटेज", src="NASA ER-2, U-2 का नागरिक रूप · NASA SVS (public domain)", mood="archive"),
        dict(lines=[5], head="चमकती चीज़ = उड़न तश्तरी?", tag="प्रतीकात्मक 3D मॉडल", src="शाम की धूप में U-2 के चाँदी जैसे पंख", mood="radar"),
        dict(lines=[6], head="आधे UFO = जासूसी विमान", tag="प्रमाण 03", src="CIA, Studies in Intelligence, 1997 (Gerald K. Haines)", mood="evidence"),
        dict(lines=[7], head="एलियन यान? रिकॉर्ड तक नहीं", tag="दावा · प्रतीकात्मक 3D मॉडल", src="KLAS-TV, 1989 · MIT और Caltech में कोई रिकॉर्ड नहीं", mood="intel"),
        dict(lines=[8], head="ज़हरीला धुआँ, केस बंद", tag="आरोप · प्रतीकात्मक 3D मॉडल", src="Frost v. Perry (1994-98) · राष्ट्रपति की छूट, 1995", mood="grief"),
        dict(lines=[9], head="2013: CIA ने आख़िर माना", tag="प्रमाण 04", src="CIA का U-2 इतिहास · नेशनल सिक्योरिटी आर्काइव, 2013", mood="intel"),
        dict(lines=[10], head="आप क्या सोचते हैं?", q=True, tag="सवाल", src=None, mood="radar"),
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
    hud(SeriesTag("एरिया 51 · एक जाँच"))
    hud(Window(-1))
    film.add(Atmos(film, strength=0.8))
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
    film.cue("heartbeat", W(1, "छुपा"), 0.8)
    still("P05", 2, B[2]["t0"])
    film.add(BigText("USE OF DEADLY FORCE AUTHORIZED", X[2], MY + 700, 150, W(2, "गोली") - 0.2, font="cond", rgb=CREAM,
                     bar=(120, 30, 24), bar_h=0.92, shadow=False, sfx=False))
    clip("ft_er2", 4, B[4]["t0"], B[4]["t1"] + 0.3, start=12.0)
    film.add(Counter(X[4] + 1100, MY - 500, 380, 60000, W(4, "साठ") - 0.5, dur=0.8, suffix=" फ़ीट", rgb=TEAL))
    clip("air_B", 5, B[5]["t0"], B[5]["t1"] + 0.3, start=0.8)
    clip("hf_haines", 6, B[6]["t0"], B[6]["t1"] + 0.3, start=0.6)
    clip("s4", 7, B[7]["t0"], B[7]["t1"] + 0.3, start=1.5)
    film.add(Stamp("रिकॉर्ड नहीं", X[7] + 900, MY + 550, size=300, rot=-8, t_in=W(7, "रिकॉर्ड") - 0.1, rgb=(255, 179, 71)))
    clip("ter_G", 8, B[8]["t0"], B[8]["t1"] + 0.3, start=0.2)
    film.add(Stamp("STATE SECRETS", X[8] + 600, MY + 650, size=260, rot=-7, t_in=W(8, "केस") - 0.1))
    still("P02", 9, B[9]["t0"])
    film.add(PenMark("ellipse", X[9], MY - 100, 1300, 800, t_in=W(9, "माना") - 0.1, dur=0.5, width=34, seed=9, rgb=TEAL))
    clip("hf_qend", 10, B[10]["t0"], doc.duration + 1)
    film.cue("boom", W(10, "आप") - 0.1, 0.5)

    film.fade_in, film.fade_out = 0.2, 1.0
    return film
