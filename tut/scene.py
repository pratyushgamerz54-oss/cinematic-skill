"""तूतनख़ामुन: a history documentary and explainer, about 5:27, Hindi narration (the user's Viraj read).

A YouTube intro (welcome, topic, "चलिए शुरू करते हैं") on its own HyperFrames graphic, a cold open on
26 November 1922, then one evidence wall, left to right in time, with a timeline along its top. Under
each section hangs a "screen": a bare Clip the camera flies into for a full-frame cutaway (3D globes,
the KV62 door and cutaway, the coffins, the valley, the scan, HyperFrames hero graphics).
Times come from the voiceover (doc.L / doc.E / doc.W), so a new read re-times everything.
Lines 11, 30 and 52 are left out of the read (film_cut in script.json): guard with has(i).
"""
import math

from engine import (HILITE, BigText, Card, Clip, Counter, Film, GeoMap, MapPin, PaperDoc, PenMark, Print, Route, Stamp,
                    StringLine, Timeline, XMarker)

SY = 7200                  # the row of screens under the wall
RED = (200, 40, 30)
CREAM = (244, 240, 232)
DARK = (26, 22, 20)
INK = (34, 32, 30)
GOLD = (226, 176, 72)
PAPER = (236, 230, 220)
BLUE = (60, 90, 140)

# section centres along the wall
X0, X1, X2, X3, X4, X5, X6, X7, X8 = 0, 17000, 32000, 58000, 77000, 84000, 120000, 131000, 160000


def build_film(doc):
    L, E, W = doc.L, doc.E, doc.W
    res = doc.res()

    def has(i):
        return i in doc.seg

    def nxt(i):
        later = [j for j in doc.seg if j > i]
        return L(min(later)) if later else doc.duration

    film = Film(doc.duration, fps=30, look="wall")
    shot, cue = film.shot, film.cue

    def photo(key, x, y, w, rot=0.0, t_in=0.0, label=None, label_t=None, **kw):
        if key in doc.meta:
            return film.add(Print(key, x, y, w, rot=rot, t_in=t_in, label=label, label_t=label_t, **kw))
        return None

    def card(x, y, w, h, t, title, lines=(), dark=False, accent=RED, ts=230, bs=165, **kw):
        return film.add(Card(x, y, w, h, t, title=title, lines=list(lines), rgb=(40, 38, 38) if dark else PAPER,
                             text_rgb=CREAM if dark else INK, accent=accent, title_size=ts, body_size=bs, **kw))

    def bar(text, x, y, size, t, t_out=None, z=60):
        return film.add(BigText(text, x, y, size, t, t_out=t_out, bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False, z=z))

    def screen(cid, x, t0, t1, start=0.0, rate=1.0):
        return film.add(Clip(doc.clip(cid), x, SY, 3840, t_in=t0, t_out=t1, start=start, rate=rate, frame=False, z=40))

    def into(x, t0, t1, z0=1.0, z1=1.035):
        shot(t0, x, SY, z0, 0.0, radius=9000, strength=0.0)
        shot(t1, x, SY, z1, 0.0, radius=9000, strength=0.0)

    def look(t, x, y, z, rot=0.0, **kw):
        shot(t, x, y, z, rot, **kw)

    # ---------------------------------------------------------------- the timeline along the top
    years = [("≈ 1350 ई.पू.", "अख़ेनातेन", X1, L(12) + 0.4), ("≈ 1332 ई.पू.", "राजा बना", X2, L(17) + 0.2),
             ("≈ 1323 ई.पू.", "मौत", X3, L(22) + 0.2), ("≈ 1140 ई.पू.", "कब्र दबी", X4, L(29) + 0.3),
             ("1922", "खोज", X5, L(33) + 0.2), ("1923", "श्राप?", X6, L(40) + 0.2),
             ("1968–2010", "जाँच", X7, L(44) + 0.2), ("आज", "गीज़ा", X8, L(51) + 0.2)]
    TX0, TX1 = -6000, X8 + 10000
    film.add(Timeline((TX0 + TX1) / 2, -6200, TX1 - TX0, [(d, c, t) for d, c, _, t in years], t_in=L(12) - 0.2,
                      pos=[(x - TX0) / (TX1 - TX0) for *_, x, _ in years], size=300, dur=1.2, rgb=CREAM, accent=RED))

    # ============================================================ YOUTUBE INTRO (1-4): its own motion graphic
    screen("hf_welcome", X0, 0.0, L(2) + 0.1)
    into(X0, 0.0, L(2) - 0.05, 1.0, 1.03)
    screen("hf_topic", X0, L(2) - 0.05, L(3) - 0.1)                    # "आज की कहानी" + chips on the words
    into(X0, L(2), L(3) - 0.2, 1.0, 1.03)
    screen("hf_topic", X0, L(3) - 0.15, L(4) - 0.1, start=4.75)       # the mask rises in the cartouche: the title, once
    into(X0, L(3) - 0.1, L(4) - 0.2, 1.0, 1.04)
    screen("hf_go", X0, L(4) - 0.1, L(4) + 3.4)                       # "चलिए शुरू करते हैं", the year spins back to 1922
    into(X0, L(4), L(4) + 3.3, 1.0, 1.05)
    cue("whoosh", L(4) + 0.8, 0.5)

    # ============================================================ COLD OPEN (5-10)
    screen("g_luxor", X0, L(4) + 3.3, L(6) + 0.2, start=max(0.0, 8.5 - (L(6) - L(4) - 3.3)))
    into(X0, L(4) + 3.35, L(6) - 0.1, 1.0, 1.05)
    bar("26 नवंबर 1922", X0, SY - 760, 230, L(5) + 0.2, t_out=L(6))
    carter = photo("P01", X0 + 4200, -600, 2600, rot=-1.6, t_in=L(6) - 0.2, label="हावर्ड कार्टर", label_t=W(6, "हावर्ड"))
    photo("P20", X0 + 7200, 1300, 2000, rot=2.0, t_in=W(6, "हावर्ड") + 0.4, label="1924", label_t=W(6, "हावर्ड") + 0.8)
    look(L(6) + 0.1, X0 + 5000, 0, 0.42, 0.3)
    look(W(6, "हावर्ड"), X0 + 4300, -500, 0.62, -0.4)
    look(E(6), X0 + 5600, 300, 0.5, 0.0)
    screen("door", X0 + 2000, L(7) - 0.2, L(8) + 0.6, start=0.3)        # 3D: the sealed doorway, the candle at the hole
    shot(L(7) - 0.3, X0 + 2600, 3800, 0.42, 0.0, strength=0.2)
    into(X0 + 2000, L(7), L(8) + 0.5, 1.0, 1.06)
    screen("hf_wonder", X0 + 2000, L(8) + 0.6, L(9) + 0.2, start=max(0.0, 2.3 - (W(8, "कार्टर") - L(8) - 0.6)))
    into(X0 + 2000, L(8) + 0.6, E(8) + 0.2, 1.0, 1.03)
    mask = photo("P03", X0 + 9600, -500, 2700, rot=1.2, t_in=L(9) - 0.3, label="तूतनख़ामुन का सोने का मुखौटा", label_t=W(9, "ख़ज़ाना"))
    look(L(9) + 0.1, X0 + 9600, -300, 0.5, 0.4)
    look(W(9, "तूतनख़ामुन"), X0 + 9600, -700, 0.66, 0.6)
    screen("hf_qopen", X0 + 9600, L(10) - 0.1, nxt(10) + 0.1, start=max(0.0, 0.9 - (W(10, "क्यों") - L(10))))
    shot(L(10) - 0.2, X0 + 9600, 3600, 0.45, 0.0, strength=0.2)
    into(X0 + 9600, L(10) + 0.1, E(10) + 0.2, 1.0, 1.05)
    cue("heartbeat", W(10, "क्यों"), 0.7); cue("heartbeat", W(10, "किसने"), 0.8)
    cue("boom", E(10) + 0.1, 0.6)

    # ============================================================ AMARNA (12-16): the rebel pharaoh
    md = doc.map("egypt"); K = 26000
    fx0, fy0, fx1, fy1 = md["frame"]
    MX, MY = X1 - 3000, 300
    eg = film.add(GeoMap(md, K, origin=(MX - (fx0 + fx1) / 2 * K, MY - (fy0 + fy1) / 2 * K), look="intel"))
    tx, ty = eg.place("Thebes"); ax, ay = eg.place("Amarna"); gx, gy = eg.place("Giza")
    film.add(MapPin(tx, ty, None, t_in=W(12, "मिस्र") - 0.3, size=4.0))
    film.add(XMarker(tx, ty, "थीब्स (लक्सर)", t_in=W(12, "मिस्र") - 0.1, size=3.0, label_size=200, side="right"))
    film.add(XMarker(gx, gy, "मेम्फ़िस / गीज़ा", t_in=W(12, "मिस्र") + 0.4, size=2.0, label_size=170, side="right"))
    film.add(BigText("मिस्र · लगभग 3,300 साल पहले", MX, MY - (fy1 - fy0) / 2 * K - 220, 200, L(12) + 0.6,
                     font="label", rgb=CREAM, bar=RED, bar_h=0.92, shadow=False, grunge=False, z=36))
    look(L(12) - 0.2, X1 - 2500, -4200, 0.33, 0.0, strength=0.3)       # the timeline draws on
    look(L(12) + 1.2, MX, MY, 0.42, 0.0, radius=6000, strength=0.3)
    akh = photo("P04", X1 + 4200, -900, 2400, rot=-1.8, t_in=W(12, "अख़ेनातेन") - 0.4, label="फ़राओ अख़ेनातेन", label_t=W(12, "अख़ेनातेन"))
    look(W(12, "अख़ेनातेन") - 0.1, X1 + 4200, -700, 0.6, -0.4)
    aten = photo("P05", X1 + 4400, 2900, 3000, rot=1.5, t_in=L(13) - 0.2, label="अख़ेनातेन का परिवार, ऊपर सूर्य-गोला आतेन", label_t=W(13, "आतेन"))
    look(L(13) + 0.2, X1 + 4400, 2700, 0.55, 0.3)
    film.add(PenMark("ellipse", X1 + 4400, 2900 - 650, 900, 600, t_in=W(13, "सूर्य") - 0.1, dur=0.5, width=40, seed=13))
    look(W(13, "सूर्य"), X1 + 4400, 2500, 0.7, 0.4)
    film.add(Route((tx, ty), (ax, ay), t_in=W(14, "राजधानी") - 0.4, dur=1.0, bend=0.2, width=80, rgb=(255, 200, 90)))
    film.add(MapPin(ax, ay, None, t_in=W(14, "अमरना") - 0.2, size=4.0))
    film.add(XMarker(ax, ay, "अमरना · नई राजधानी", t_in=W(14, "अमरना") - 0.05, size=3.0, label_size=200, side="left"))
    film.add(Stamp("मंदिर बंद", (tx + ax) / 2 + 1900, (ty + ay) / 2 - 900, size=520, rot=-8, t_in=W(14, "मंदिर") + 0.1))
    look(L(14) - 0.1, (tx + ax) / 2 + 900, (ty + ay) / 2, 0.42, 0.0, radius=6000, strength=0.3)
    look(E(14), (tx + ax) / 2 + 1000, (ty + ay) / 2, 0.45, 0.0, radius=6000, strength=0.3)
    cart = card(X1 + 8600, -400, 3000, 1300, L(15) - 0.1, "तूतनख़ातेन", ["'आतेन की जीती-जागती छवि'"], ts=300, bs=140, accent=GOLD)
    film.add(PenMark("ellipse", X1 + 8600, -400, 3500, 1700, t_in=W(15, "तूतनख़ातेन") - 0.1, dur=0.6, width=46, seed=15, rgb=GOLD))
    look(L(15) + 0.1, X1 + 8600, -300, 0.62, 0.3)
    film.add(BigText("आग पर रखा तख़्त", X1 + 8600, 1900, 560, W(16, "तख़्त") - 0.1, t_out=E(16) + 0.8, rgb=(214, 40, 30), z=70))
    look(L(16) + 0.2, X1 + 8600, 900, 0.4, 0.0, radius=3000, strength=0.75)
    look(E(16) + 0.2, X1 + 8600, 1100, 0.44, 0.0, radius=3000, strength=0.8)
    cue("riser", L(16) + 0.4, 0.5, dur=1.8); cue("heartbeat", W(16, "आग"), 0.7)

    # ============================================================ BOY KING (17-21)
    film.add(Counter(X2 - 3000, -300, 1300, 9, W(17, "नौ") - 0.6, dur=0.9, caption="साल का फ़राओ", rgb=GOLD))
    film.add(BigText("≈ 1332 ई.पू.", X2 - 3000, -1900, 300, L(17) + 0.2, bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False))
    look(L(17) + 0.1, X2 - 3000, -700, 0.6, 0.0)
    boy = card(X2 + 1200, 800, 2600, 1200, L(18) - 0.2, "बच्चा राजा", ["तूतनख़ातेन"], dark=True, accent=GOLD, ts=280, bs=170)
    if "P08" in doc.meta:
        ay_p = photo("P08", X2 - 1400, 2300, 2000, rot=-2.0, t_in=W(18, "आय") - 0.4, label="वज़ीर आय", label_t=W(18, "आय"))
    else:
        card(X2 - 1400, 2300, 2400, 1500, W(18, "आय") - 0.4, "आय", ["बूढ़ा वज़ीर"], ts=300, bs=170)
    photo("P09", X2 + 3800, 2400, 1700, rot=1.8, t_in=W(18, "होरेमहेब") - 0.4, label="सेनापति होरेमहेब", label_t=W(18, "होरेमहेब"))
    film.add(StringLine((X2 - 1400, 1600), (X2 + 1200, 1300), t_in=W(18, "आय") + 0.1, dur=0.6, sag=0.04, width=24))
    film.add(StringLine((X2 + 3800, 1500), (X2 + 1200, 1300), t_in=W(18, "होरेमहेब") + 0.1, dur=0.6, sag=0.04, width=24))
    look(L(18) + 0.1, X2 + 1200, 1600, 0.5, 0.0)
    look(E(18), X2 + 1200, 1700, 0.53, 0.2)
    photo("P06", X2 + 9000, -500, 2200, rot=-1.4, t_in=L(19) - 0.3, label="बहाली का शिलालेख", label_t=L(19) + 0.6)
    film.add(Stamp("बहाली", X2 + 9300, -200, size=420, rot=-9, t_in=W(19, "खुले") - 0.05))
    film.add(BigText("आतेन नहीं, आमुन", X2 + 9000, 1900, 420, W(19, "नाम") - 0.3, rgb=GOLD, z=60))
    film.add(BigText("तूतनख़ामुन", X2 + 9000, 2650, 300, W(19, "तूतनख़ामुन") - 0.1, font="label", rgb=CREAM, shadow=False, grunge=False))
    look(L(19) + 0.2, X2 + 9000, -300, 0.55, -0.3)
    look(W(19, "नाम") - 0.5, X2 + 9000, 900, 0.45, 0.0)
    photo("P07", X2 + 13400, 300, 2600, rot=1.6, t_in=L(20) - 0.3, label="राजा और रानी अंखेसेनामुन · सोने का सिंहासन", label_t=W(20, "अंखेसेनामुन"))
    look(L(20) + 0.1, X2 + 13400, 300, 0.55, 0.3)
    look(W(20, "सौतेली"), X2 + 13600, 300, 0.66, 0.5)
    film.add(BigText("सुनहरी?", X2 + 17600, -300, 800, L(21) + 0.6, t_out=E(21) + 0.8, rgb=CREAM, z=70))
    film.add(BigText("नहीं।", X2 + 17600, 1000, 1100, W(21, "नहीं") - 0.05, t_out=E(21) + 0.8, rgb=(214, 40, 30), z=70))
    look(L(21) + 0.3, X2 + 17600, 300, 0.32, 0.0, radius=2600, strength=0.8)
    look(E(21) + 0.2, X2 + 17600, 300, 0.36, 0.0, radius=2600, strength=0.8)
    cue("heartbeat", W(21, "नहीं"), 0.9)

    # ============================================================ DEATH AND ERASURE (22-27)
    film.add(Counter(X3 - 3800, -400, 1300, 19, W(22, "उन्नीस") - 0.5, dur=0.9, caption="साल की उम्र में मौत", rgb=CREAM, start=9))
    for k in range(3):                                              # candles: small warm lights for a death
        film.add(PenMark("highlight", X3 - 5000 + k * 1200, 1500, 120, 0, t_in=W(22, "मौत") + 0.1 + 0.15 * k, dur=0.3, width=120, rgb=(255, 190, 90), seed=k))
    look(L(22) + 0.1, X3 - 3800, -200, 0.55, 0.0)
    screen("tomb", X3, L(23) - 0.2, nxt(23) + 0.1, start=0.0)        # 3D: the small tomb KV62, its four rooms
    shot(L(23) - 0.3, X3 - 1000, 3800, 0.45, 0.0, strength=0.2)
    into(X3, L(23) + 0.1, E(23) + 0.2, 1.0, 1.04)
    wall = photo("P17", X3 + 4400, -600, 3000, rot=-1.4, t_in=L(24) - 0.3, label="दफ़न कक्ष की दीवार, KV62", label_t=W(24, "दीवार"))
    film.add(PenMark("ellipse", X3 + 4900, -650, 1100, 1700, t_in=W(24, "आय") - 0.2, dur=0.5, width=44, seed=24))
    film.add(BigText("नया राजा: आय", X3 + 4400, 1300, 280, W(24, "आय") - 0.05, font="label", rgb=CREAM, bar=RED, bar_h=0.92, shadow=False, grunge=False))
    look(L(24) + 0.2, X3 + 4400, -500, 0.55, -0.3)
    look(W(24, "आय") - 0.3, X3 + 4800, -200, 0.66, -0.5)
    names = ["अख़ेनातेन", "तूतनख़ामुन", "आय"]
    for k, nm in enumerate(names):
        card(X3 + 9400, -1500 + k * 1300, 2600, 1000, W(25, "अमरना") - 0.3 + 0.25 * k, nm, ts=200, accent=GOLD)
        film.add(PenMark("underline", X3 + 9400, -1500 + k * 1300, 2300, 0, t_in=W(25, "मिटाए") - 0.1 + 0.3 * k, dur=0.35, width=60, seed=30 + k, rgb=RED))
    film.add(Stamp("मिटाया", X3 + 9700, -300, size=480, rot=-10, t_in=W(25, "मिटाए") + 0.8))
    if "P09" in doc.meta:
        film.add(StringLine((X2 + 4800, 1300), (X3 + 9400, -2200), t_in=W(25, "होरेमहेब") - 0.1, dur=0.8, sag=0.06, width=24))
    look(L(25) + 0.1, X3 + 9400, -300, 0.5, 0.3)
    look(E(25), X3 + 9500, -200, 0.54, 0.4)
    if "P11" in doc.meta:
        photo("P11", X3 + 14000, -300, 2800, rot=1.2, t_in=L(26) - 0.3, label="अबीडोस की राजाओं की सूची", label_t=L(26) + 0.4)
    else:
        card(X3 + 14000, -300, 3000, 2300, L(26) - 0.3, "अबीडोस की सूची", ["अमेनहोतेप III", "  ·  ·  ·  ", "होरेमहेब"], ts=210, bs=160)
    film.add(PenMark("strike", X3 + 14000, 250, 1800, 0, t_in=W(26, "नाम") - 0.1, dur=0.5, width=40, seed=26))
    film.add(BigText("तूतनख़ामुन? ग़ायब", X3 + 14000, 1650, 240, W(26, "नाम"), font="label", rgb=CREAM, bar=RED, bar_h=0.92, shadow=False, grunge=False))
    look(L(26) + 0.1, X3 + 14000, 0, 0.55, -0.3)
    screen("valley", X3 + 9400, L(27) + 0.3, L(28) + 0.2, start=0.0)
    shot(L(27) + 0.2, X3 + 9400, 3800, 0.4, 0.0, radius=3000, strength=0.7)
    into(X3 + 9400, W(27, "लेकिन") - 0.3, E(27) + 0.2, 1.0, 1.04)
    cue("riser", W(27, "लेकिन") - 0.4, 0.5, dur=1.6)

    # ============================================================ THE LOST TOMB (28-29)
    photo("P12", X4, -1200, 5200, rot=-0.8, t_in=L(28) - 0.2, label="राजाओं की घाटी, लक्सर", label_t=L(28) + 0.5)
    film.add(Stamp("लूट 1", X4 - 1200, 600, size=360, rot=-9, t_in=W(28, "दो") - 0.05))
    film.add(Stamp("लूट 2", X4 + 1000, 700, size=360, rot=7, t_in=W(28, "चोर") - 0.05))
    film.add(BigText("फिर से सील", X4, 1800, 260, E(28) - 0.6, font="label", rgb=CREAM, bar=BLUE, bar_h=0.92, shadow=False, grunge=False))
    look(L(28) + 0.2, X4, -1000, 0.42, 0.0)
    look(W(28, "तूतनख़ामुन"), X4, 300, 0.55, 0.0)
    screen("valley", X4 + 5000, L(29) - 0.2, nxt(29) + 0.2, start=2.0)
    shot(L(29) - 0.3, X4 + 4000, 3800, 0.45, 0.0, strength=0.2)
    into(X4 + 5000, L(29) + 0.1, E(29) + 0.3, 1.0, 1.05)
    bar("≈ 3000 साल · मलबे के नीचे", X4 + 5000, SY - 760, 200, W(29, "मलबा") + 0.3, t_out=E(29) + 0.5)

    # ============================================================ DISCOVERY (31-39)
    screen("g_carnarvon", X5, L(31) - 0.2, L(32) + 0.2)
    into(X5, L(31) + 0.1, E(31) + 0.1, 1.0, 1.05)
    bar("1917", X5, SY - 760, 260, L(31) + 0.1, t_out=E(31))
    photo("P02", X5 + 4600, -700, 3000, rot=1.5, t_in=L(32) - 0.3, label="लॉर्ड कार्नारवन", label_t=L(32) + 0.4)
    film.add(Counter(X5 + 4600, 2300, 900, 5, W(32, "पाँच") - 0.6, dur=0.8, caption="साल · लगभग कुछ नहीं", rgb=CREAM, start=1))
    film.add(Stamp("आख़िरी मौक़ा", X5 + 5000, -200, size=360, rot=-8, t_in=W(32, "आख़िरी") - 0.05))
    look(L(32) + 0.1, X5 + 4600, 500, 0.45, 0.2)
    look(W(32, "कार्नारवन"), X5 + 4800, -400, 0.6, 0.3)
    screen("tomb", X5 + 9000, L(33) - 0.2, L(34) + 0.1, start=0.3)     # down the stairs to the sealed door
    bar("4 नवंबर 1922", X5 + 9000, SY - 760, 230, L(33) + 0.2, t_out=W(33, "सीढ़ी") + 0.4)
    shot(L(33) - 0.3, X5 + 8000, 3800, 0.45, 0.0, strength=0.2)
    into(X5 + 9000, L(33) + 0.1, E(33) + 0.2, 1.0, 1.05)
    ante = photo("P13", X5 + 9000, -700, 3600, rot=-1.0, t_in=L(34) - 0.3, label="आगे का कक्ष, जैसा मिला · 1922 (हैरी बर्टन)", label_t=L(34) + 0.4)
    film.add(Counter(X5 + 9000, 2100, 900, 5398, W(34, "पाँच") - 0.4, dur=1.4, caption="वस्तुएँ", rgb=GOLD))
    look(L(34) + 0.1, X5 + 9000, 300, 0.42, 0.0)
    look(W(34, "रथ"), X5 + 9000, -500, 0.55, -0.2)
    photo("P14", X5 + 13600, -300, 2600, rot=1.5, t_in=L(35) - 0.3, label="कार्टर, सुनहरे कवच के सामने (बर्टन)", label_t=W(35, "दफ़न"))
    film.add(BigText("फ़रवरी 1923", X5 + 13600, -2150, 260, L(35) + 0.1, bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False))
    look(L(35) + 0.1, X5 + 13600, -700, 0.55, 0.3)
    screen("coffins", X5 + 13600, L(36) - 0.2, L(37) + 0.1, start=0.8)
    shot(L(36) - 0.3, X5 + 13600, 3800, 0.45, 0.0, strength=0.2)
    into(X5 + 13600, L(36) + 0.1, W(36, "सबसे") - 0.2, 1.0, 1.04)
    photo("P15", X5 + 17800, -400, 2400, rot=-1.4, t_in=W(36, "सबसे") - 0.6, label="सबसे अंदर का ताबूत, ठोस सोना", label_t=W(36, "सबसे") - 0.2)
    film.add(Counter(X5 + 17800, 2400, 800, 110, W(36, "एक") - 0.3, dur=1.0, suffix=" किलो", caption="ठोस सोना", rgb=GOLD))
    look(W(36, "सबसे") - 0.1, X5 + 17800, 600, 0.45, -0.2)
    look(E(36), X5 + 17800, 700, 0.48, -0.3)
    photo("P18", X5 + 21800, -300, 2500, rot=1.2, t_in=L(37) - 0.3, label="सोने का मुखौटा", label_t=L(37) + 0.4)
    film.add(Counter(X5 + 21800, 2500, 800, 10, W(37, "दस") - 0.4, dur=0.7, suffix="+ किलो", caption="सोना", rgb=GOLD))
    look(L(37) + 0.1, X5 + 21800, 600, 0.45, 0.3)
    photo("P16", X5 + 21800, 4800, 3600, rot=-0.8, t_in=L(38) - 0.3, label="लोहे का ख़ंजर, मिस्री म्यूज़ियम", label_t=W(38, "ख़ंजर"))
    film.add(BigText("लोहा: उल्कापिंड से", X5 + 21800, 3900, 260, W(38, "उल्कापिंड") - 0.1, font="label", rgb=CREAM, bar=RED, bar_h=0.92, shadow=False, grunge=False))
    film.add(StringLine((X5 + 23800, 2900), (X5 + 22300, 4700), t_in=W(38, "आसमान") - 0.1, dur=0.5, sag=0.0, width=30))
    look(L(38) + 0.1, X5 + 21800, 4500, 0.55, 0.0)
    film.add(BigText("क़ीमत?", X5 + 26000, 300, 1000, W(39, "क़ीमत") - 0.1, t_out=E(39) + 0.8, rgb=(214, 40, 30), z=70))
    look(L(39) + 0.3, X5 + 26000, 300, 0.34, 0.0, radius=2600, strength=0.8)
    look(E(39) + 0.2, X5 + 26000, 300, 0.38, 0.0, radius=2600, strength=0.8)
    cue("heartbeat", W(39, "क़ीमत"), 0.8)

    # ============================================================ THE CURSE (40-43)
    bar("5 अप्रैल 1923 · काहिरा", X6 - 3600, -2400, 300, L(40) + 0.1)
    photo("P02", X6 - 3600, -300, 2400, rot=-1.2, t_in=L(40) - 0.2, label="लॉर्ड कार्नारवन, मौत: 5 अप्रैल 1923", label_t=W(40, "कार्नारवन"))
    look(L(40) + 0.2, X6 - 3600, -700, 0.5, -0.3)
    paper = film.add(PaperDoc(X6 + 900, -300, 3000, 3800, rot=1.4, t_in=L(41) - 0.2, rows=12, sentence_row=5, sentence_size=125,
                              header=(("THE DAILY RECORD", 200, "serif"), ("APRIL 1923 · RECREATION", 90, "mono"), ("CURSE OF THE PHARAOH", 160, "cond")),
                              sentence="Lord Carnarvon dies in Cairo; the press blames the Pharaoh's curse."))
    film.add(Stamp("श्राप?", X6 + 1300, 300, size=460, rot=-9, t_in=W(41, "श्राप") - 0.05))
    look(L(41) + 0.05, X6 + 900, -500, 0.5, 0.4)
    steps = [("मच्छर का काटा", -1500), ("दाढ़ी बनाते कट", 0), ("ख़ून में संक्रमण", 1500)]
    words = ["मच्छर", "दाढ़ी", "संक्रमण"]
    for k, (txt, dy) in enumerate(steps):
        card(X6 + 5600, dy, 2700, 1100, W(42, words[k]) - 0.3, txt, ts=180, dark=k == 2)
        if k:
            film.add(StringLine((X6 + 5600, dy - 1500 + 550), (X6 + 5600, dy - 550), t_in=W(42, words[k]) - 0.2, dur=0.4, sag=0.0, width=22))
    look(L(42) + 0.1, X6 + 5600, 0, 0.42, 0.0)
    film.add(Stamp("कहानी", X6 + 1100, 1500, size=520, rot=7, rgb=BLUE, t_in=W(43, "कहानी") - 0.05))
    look(L(43) + 0.1, X6 + 1000, 600, 0.5, 0.3)
    look(W(43, "लेकिन"), X6 + 3000, 300, 0.32, 0.0, radius=3000, strength=0.7)
    cue("riser", W(43, "लेकिन") - 0.3, 0.5, dur=1.8)

    # ============================================================ INVESTIGATION (44-50)
    screen("ctscan", X7, L(44) - 0.2, L(45) + 0.2, start=1.2)
    bar("1968 · एक्स-रे", X7, SY - 760, 230, L(44) + 0.1, t_out=E(44))
    into(X7, L(44) + 0.1, E(44) + 0.2, 1.0, 1.05)
    film.add(Card(X7 + 4400, -700, 2400, 1300, L(45) - 0.2, title="हत्या?", lines=["अख़बारों का शक"], rgb=(40, 38, 38), text_rgb=CREAM, accent=RED, title_size=300, body_size=130))
    if "P08" in doc.meta:
        photo("P08", X7 + 8400, -500, 1900, rot=1.4, t_in=W(45, "आय") - 0.4, label="वज़ीर आय", label_t=W(45, "आय"))
    else:
        card(X7 + 8400, -500, 2200, 1500, W(45, "आय") - 0.4, "आय", ["शक की सुई"], ts=260, bs=130)
    film.add(StringLine((X7 + 4400, -700), (X7 + 8400, -700), t_in=W(45, "सुई") - 0.1, dur=0.6, sag=0.05, width=26))
    film.add(BigText("आरोप, सबूत नहीं", X7 + 6400, 1400, 220, E(45) - 1.2, font="label", rgb=CREAM, bar=BLUE, bar_h=0.92, shadow=False, grunge=False))
    look(L(45) + 0.1, X7 + 4400, -500, 0.6, 0.0)
    look(W(45, "सुई") - 0.2, X7 + 6400, -200, 0.42, 0.0)
    screen("ctscan", X7, L(46) - 0.2, nxt(46) + 0.2, start=3.2)
    bar("2005 · सीटी स्कैन", X7, SY - 760, 230, L(46) + 0.1, t_out=E(46))
    shot(L(46) - 0.3, X7 + 1000, 3800, 0.45, 0.0, strength=0.2)
    into(X7, L(46) + 0.1, E(46) + 0.2, 1.0, 1.04)
    bar("2010 · डीएनए", X7 + 12200, -2600, 300, L(47) + 0.1)
    dad = card(X7 + 10600, -900, 2600, 1300, W(47, "माता") - 0.4, "पिता", ["KV55 · शायद अख़ेनातेन"], ts=260, bs=170)
    mom = card(X7 + 13800, -900, 2600, 1300, W(47, "माता") - 0.2, "माता", ["'यंगर लेडी' · KV35"], ts=260, bs=170)
    film.add(StringLine((X7 + 11900, -900), (X7 + 12500, -900), t_in=W(47, "भाई") - 0.2, dur=0.4, sag=0.0, width=30))
    film.add(Stamp("भाई-बहन", X7 + 12200, -200, size=380, rot=-8, t_in=W(47, "भाई") - 0.05))
    son = card(X7 + 12200, 1300, 2600, 1100, W(47, "माता") + 0.3, "तूतनख़ामुन", ts=220, dark=True, accent=GOLD)
    film.add(StringLine((X7 + 12200, -250), (X7 + 12200, 750), t_in=W(47, "माता") + 0.4, dur=0.4, sag=0.0, width=22))
    look(L(47) + 0.2, X7 + 12200, 0, 0.5, 0.0)
    screen("ctscan", X7 + 12200, L(48) - 0.2, L(49) + 0.1, start=5.0)
    shot(L(48) - 0.3, X7 + 12200, 3800, 0.45, 0.0, strength=0.2)
    into(X7 + 12200, L(48) + 0.1, E(48) + 0.2, 1.0, 1.05)
    film.add(Counter(X7 + 17000, -400, 1300, 130, W(49, "तीस") - 0.7, dur=1.0, caption="छड़ियाँ कब्र में", rgb=CREAM))
    for k in range(13):                                             # a row of sticks, one per ten
        film.add(PenMark("underline", X7 + 15200 + k * 280, 1700, 0, 900, t_in=W(49, "छड़ियाँ") + 0.05 * k, dur=0.2, width=40, seed=60 + k, rgb=GOLD))
    look(L(49) + 0.1, X7 + 17000, 400, 0.5, 0.0)
    for k, (nm, dy) in enumerate([("बीमारी?", -1300), ("हादसा?", 0), ("साज़िश?", 1300)]):
        card(X7 + 21400, dy, 2800, 1000, W(50, nm.rstrip("?")) - 0.2, nm, ts=260, dark=k == 2)
    film.add(BigText("विशेषज्ञ: एकमत नहीं", X7 + 21400, 2500, 230, W(50, "विशेषज्ञ"), font="label", rgb=CREAM, bar=BLUE, bar_h=0.92, shadow=False, grunge=False))
    look(L(50) + 0.1, X7 + 21400, 400, 0.45, 0.0)
    look(E(50), X7 + 21400, 500, 0.47, 0.2)

    # ============================================================ VERDICT (51-54)
    photo("P03", X8, -600, 2800, rot=-1.0, t_in=L(51) - 0.3, label="आज: दुनिया का सबसे मशहूर फ़राओ", label_t=W(51, "मशहूर"))
    film.add(Stamp("मिटाया?", X8 + 600, 1200, size=360, rot=-8, t_in=W(51, "मिटाने") - 0.05))
    look(L(51) + 0.2, X8, -300, 0.52, -0.3)
    look(W(51, "मशहूर"), X8, -600, 0.6, -0.4)
    screen("g_verdict", X8, L(53) - 0.2, L(54) + 0.1)
    film.add(BigText("विडंबना", X8, SY - 760, 300, W(53, "विडंबना") - 0.1, bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False, z=60, t_out=E(53) + 0.2))
    shot(L(53) - 0.3, X8 + 1000, 3800, 0.45, 0.0, strength=0.2)
    into(X8, L(53) + 0.1, E(53) + 0.2, 1.0, 1.04)
    screen("hf_qend", X8, L(54) - 0.1, doc.duration + 1, start=max(0.0, 0.0))
    into(X8, L(54) + 0.1, doc.duration, 1.0, 1.05)
    cue("heartbeat", W(54, "बीमारी"), 0.7); cue("heartbeat", W(54, "साज़िश"), 0.8)
    cue("boom", W(54, "आप") - 0.1, 0.5)

    # ------------------------------------------------ moods: background and finish follow the scene's emotion
    def mood(i, name, d=0.0, fade=1.2):
        if has(i):
            film.mood(L(i) + d, name, fade)
    film.mood(0.0, "verdict", 0.1)
    for args in [(5, "archive", -0.3), (10, "tension", 0.0, 0.6), (12, "intel", -0.4), (13, "archive", -0.2),
                 (16, "tension", 0.0, 0.6), (17, "archive", -0.3), (18, "intel", -0.2), (19, "archive", -0.2),
                 (21, "tension", 0.0, 0.6), (22, "grief", -0.3), (24, "evidence", -0.2), (25, "intel", -0.2),
                 (27, "tension"), (28, "archive", -0.3), (31, "intel", -0.2), (32, "archive", -0.3),
                 (34, "archive"), (39, "tension", 0.0, 0.6), (40, "grief", -0.3), (41, "evidence", -0.2),
                 (43, "tension"), (44, "intel", -0.3), (45, "evidence", -0.2), (46, "intel", -0.2),
                 (47, "evidence", -0.2), (48, "intel", -0.2), (50, "evidence", -0.2), (51, "verdict", -0.3)]:
        mood(*args)

    tidy_keys(film.cam_keys)
    tidy_keys(film.focus_keys)

    # ------------------------------------------------ word chips: a new explaining label on a key word,
    # placed in a corner of wherever the camera is holding (explainer style; the camera stays calm)
    SLOT = {"tl": (-0.25, -0.31), "tr": (0.25, -0.31), "ml": (-0.32, 0.04), "mr": (0.32, 0.04)}

    def chip(i, word, text, slot, red=False):
        if not has(i):
            return
        try:
            t = W(i, word) - 0.1
        except Exception:
            print("chip: word not found", i, word); return
        x, y, z, _ = film.camera(t + 0.5)
        fx, fy = SLOT[slot]
        film.add(BigText(text, x + fx * 3840 / z, y + fy * 2160 / z, 150 / z, t, t_out=min(E(i) + 0.5, nxt(i) + 0.2),
                         font="label", rgb=CREAM if red else DARK, bar=RED if red else HILITE, bar_h=0.92,
                         shadow=False, grunge=False, z=78, sfx=False))

    for args in [
        (6, "पुरातत्वविद्", "मिस्र में 30 साल", "tl"),
        (7, "मोमबत्ती", "26 नवंबर 1922 · दोपहर", "tl"),
        (9, "ख़ज़ाना", "लगभग 3,300 साल पुराना", "tl", True),
        (12, "अख़ेनातेन", "18वाँ राजवंश", "tl"),
        (13, "पुराने", "आमुन और बाक़ी", "tl"), (13, "आतेन", "सिर्फ़ एक देवता: आतेन", "tr", True),
        (14, "पुजारियों", "पुजारियों की ताक़त छिनी", "tl"),
        (15, "बच्चा", "शायद अख़ेनातेन का बेटा", "tl"),
        (17, "फ़राओ", "बच्चा राजा", "tr"),
        (18, "वज़ीर", "असली ताक़त किसके पास?", "tl", True),
        (20, "सौतेली", "शायद सौतेली बहन", "tl"),
        (22, "अचानक", "अचानक मौत", "tr", True),
        (23, "छोटी", "राजा के लिए बहुत छोटी", "tl"), (23, "किसी", "शायद किसी और की", "tr"),
        (24, "रस्म", "'मुँह खोलने' की रस्म", "tl"),
        (25, "स्मारकों", "छेनी से काटे नाम", "tl", True),
        (28, "घाटी", "60 से ज़्यादा कब्रें", "tl"), (28, "चोर", "दो बार चोरी", "tr", True),
        (29, "रामसेस", "रामसेस VI · KV9", "tl"),
        (31, "कार्नारवन", "पैसा: लॉर्ड कार्नारवन", "tl"),
        (33, "मुहर", "राजा की मुहर", "tl", True),
        (35, "दफ़न", "दफ़न कक्ष · सुनहरा कवच", "tl"),
        (36, "ताबूत", "तीन ताबूत, एक के अंदर एक", "tl"),
        (38, "उल्कापिंड", "2016 की जाँच", "tl"),
        (40, "मौत", "संक्रमण और निमोनिया", "tl"),
        (42, "मच्छर", "असल वजह", "tl", True),
        (43, "कहानी", "कार्टर 1939 तक जिए", "tr"),
        (44, "टुकड़ा", "हड्डी का टुकड़ा", "tl", True),
        (46, "टूटा", "शायद ममी बनाते वक़्त", "tl"), (46, "फ़्रैक्चर", "बायाँ पैर: फ़्रैक्चर", "tr", True),
        (48, "मलेरिया", "मलेरिया के निशान", "tl", True),
        (49, "सहारे", "चलने में दिक़्क़त?", "tl"),
        (51, "मशहूर", "आज सबसे मशहूर", "tl", True),
        (53, "भुलाया", "भूली कब्र = बची कब्र", "tl"),
    ]:
        chip(*args)
    film.fade_in, film.fade_out = 0.4, 1.5
    return film


def tidy_keys(keys, min_gap=0.6, hold_after=1.8, move=1.0):
    """Separate keys that land on the same moment, and hold each key until shortly before the next
    one so the camera rests on its hero instead of drifting through the whole line."""
    keys.sort(key=lambda k: k[0])
    for i in range(len(keys) - 2, -1, -1):
        if keys[i + 1][0] - keys[i][0] < min_gap:
            keys[i] = (keys[i + 1][0] - min_gap,) + tuple(keys[i][1:])
    keys.sort(key=lambda k: k[0])
    i = 1
    while i < len(keys) - 1:
        p, a, b = keys[i - 1], keys[i], keys[i + 1]
        if b[0] - a[0] < 1.0 and math.hypot(b[1] - p[1], b[2] - p[2]) < 400 and math.hypot(a[1] - p[1], a[2] - p[2]) > 1500:
            del keys[i + 1]
            continue
        i += 1
    extra = []
    for a, b in zip(keys, keys[1:]):
        if b[0] - a[0] > hold_after:
            k = list(a); k[0] = b[0] - move
            if len(k) == 5 and k[3] < 0.95:
                k[3] *= 1.035; k[1] += 60 / k[3]; k[2] -= 25 / k[3]; k[4] += 0.15
            extra.append(tuple(k))
    keys.extend(extra); keys.sort(key=lambda k: k[0])
