"""पिछवाड़े के साँप: the ~59-second vertical reel (1080x1920), in the fixed reel format.

THE REEL FORMAT (the same on every beat, so the reel reads as one consistent piece):
  top     a story-style progress bar (one segment per beat) and the series tag
  head    one hook headline per beat, same place and size: yellow bar; red only for the opening
          and closing questions to the viewer
  window  one 16:9 media window with the same frame on every beat (clip, photo, map or document),
          an exhibit tag on its top-left corner ("प्रमाण 01", "प्रतीकात्मक 3D मॉडल") and a
          source line under it
  bottom  the burned-in captions (bottom quarter, highlighter style)
The overlay is drawn with engine.Hud, so it never moves; only the media changes. Backgrounds follow the
beat's emotion with film.mood. Same recorded lines as the film, re-cut.
Render: render.py --project saanp/reel --size 1080x1920
"""
from engine import (HILITE, BigText, Clip, Film, Hud, Item, PaperDoc, PenMark, Print, draw_text, ease_out_cubic,
                    paint, ramp)
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
    res = doc.res()
    film = Film(doc.duration, fps=30, look="wall")
    order = [s["id"] for s in doc.timing["segments"]]
    X = {i: k * 7000 for k, i in enumerate(order)}
    hud = lambda item: film.add(Hud(film, item))

    # ---- the beats: lines, headline, exhibit tag, source line, mood
    beats = [
        dict(lines=[5], head="एक सवाल", q=True, tag="सवाल", src=None, mood="evidence"),
        dict(lines=[3], head="2 मई 2011 · एबटाबाद", tag="प्रमाण 01", src="तस्वीर: एबटाबाद का ठिकाना, 4 मई 2011 (विकिमीडिया कॉमन्स)", mood="evidence"),
        dict(lines=[4], head="फ़ौजी अकादमी से ≈ 1 किमी", tag="प्रतीकात्मक 3D मॉडल", src="दूरी: लगभग 1 किमी, काकुल अकादमी तक", mood="intel"),
        dict(lines=[19], head="मुंबई · 26/11 · 2008", tag="प्रमाण 02", src="समुद्र के रास्ते, कराची से मुंबई (मैप: नैचुरल अर्थ)", mood="tension"),
        dict(lines=[41], head="पाकिस्तान के अंदर से गवाही", tag="प्रमाण 03", src="डॉन अख़बार · 3 अगस्त 2015 · तारिक़ खोसा, पूर्व FIA प्रमुख", mood="evidence"),
        dict(lines=[32], head="अमेरिका की चेतावनी · 2011", tag="प्रमाण 04", src="हिलेरी क्लिंटन · इस्लामाबाद · 21 अक्टूबर 2011", mood="evidence"),
        dict(lines=[35], head="फिर साँप पलटे", tag="पेशावर · 2014", src="आर्मी पब्लिक स्कूल हमला · 16 दिसंबर 2014", mood="grief"),
        dict(lines=[57, 58], head="रक्षा मंत्री ने क्या माना?", tag="प्रमाण 05", src="ख़्वाजा आसिफ़ · स्काई न्यूज़ इंटरव्यू · अप्रैल 2025", mood="evidence"),
        dict(lines=[66], head="आप क्या सोचते हैं?", q=True, tag="सवाल", src=None, mood="verdict"),
    ]
    spans = []
    for k, b in enumerate(beats):
        a = 0.0 if k == 0 else L(b["lines"][0]) - 0.3
        z = doc.duration if k == len(beats) - 1 else L(beats[k + 1]["lines"][0]) - 0.3
        b["t0"], b["t1"] = a, z
        spans.append((a, z))

    # ---- the fixed overlay
    hud(ProgressBar(spans))
    hud(SeriesTag("पिछवाड़े के साँप · एक जाँच"))
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

    def clip(cid, i, t0, t1, start=0.0):
        film.add(Clip(doc.clip(cid), X[i], MY, WIN_W, t_in=t0, t_out=t1, start=start, frame=False, z=40))

    # ---- the media, one beat at a time, always inside the window
    clip("hf_qopen", 5, 0.0, beats[0]["t1"] + 0.3)
    film.cue("heartbeat", W(5, "इत्तेफ़ाक़"), 0.8)
    clip("g_abbottabad", 3, beats[1]["t0"], W(3, "ओसामा") - 0.1, start=3.0)
    film.add(Print("P02", X[3], MY, WIN_W, t_in=W(3, "ओसामा") - 0.3, border=0.0, pin=False, aspect=16 / 9, sfx=False))
    clip("compound", 4, beats[2]["t0"], beats[2]["t1"] + 0.3, start=3.4)
    clip("g_mumbai", 19, beats[3]["t0"], beats[3]["t1"] + 0.3)
    dawn = film.add(PaperDoc(X[41], MY, WIN_W - 60, WIN_H - 60, t_in=beats[4]["t0"], rows=6, sentence_row=3, sentence_size=150, pin=False,
                             header=(("DAWN", 230, "serif"), ("3 AUGUST 2015 · TARIQ KHOSA", 90, "mono")),
                             sentence="Pakistan has to deal with the Mumbai mayhem, planned and launched from its soil."))
    for k, ((hx, hy), hw) in enumerate(dawn.phrase_spans(res, "planned and launched from its soil.")):
        film.add(PenMark("highlight", hx, hy - 50, hw + 60, 0, t_in=W(41, "प्लान") - 0.3 + 0.3 * k, dur=0.4, width=175, seed=21 + k))
    clip("hf_clinton", 32, beats[5]["t0"], beats[5]["t1"] + 0.3)
    clip("hf2_candles", 35, beats[6]["t0"], beats[6]["t1"] + 0.3, start=0.6)
    clip("hf_asif", 57, beats[7]["t0"], beats[7]["t1"] + 0.3)
    clip("hf_qend", 66, beats[8]["t0"], doc.duration + 1)
    film.cue("boom", L(66), 0.5)

    film.fade_in, film.fade_out = 0.2, 1.0
    return film
