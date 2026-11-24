"""सिकंदर का साम्राज्य (Alexander's empire), about 85 s, narrated in Hindi.

One camera over one wall: a map of the lands from Greece to the Indus in the middle, the cold open
(Alexander's portrait and two numbers) hung on the cork below Babylon, the young king's bust above
Macedonia, Darius over the Mediterranean, and the Porus coin out east past the Punjab.

Country fills use modern borders as an approximation of ancient lands (said on the map's note).
Every time comes from the voiceover: doc.L(i) line start, doc.W(i, "word") a spoken word, so a
new voice re-times the film by itself.
"""
from engine import (HILITE, MUSTARD, RUST, WHITE, BigText, Counter, Film, GeoMap, PenMark, Print,
                    RegionFill, Route, Stamp, StringLine, XMarker)

K = 28000
LBL = dict(size=2.6, label_size=150, label_rgb=(34, 30, 26), shadow=False)
DARK = (30, 26, 22)
CREAMY = (244, 240, 232)

GREECE = ["Greece", "Macedonia", "Bulgaria", "Albania"]
PERSIA_W = ["Turkey", "Syria", "Lebanon", "Israel", "Palestine", "Jordan", "Cyprus", "N. Cyprus"]
EGYPT = ["Egypt"]
PERSIA_E = ["Iraq", "Iran", "Kuwait", "Afghanistan", "Turkmenistan", "Uzbekistan", "Tajikistan", "Armenia", "Azerbaijan"]
INDUS = ["Pakistan"]
EMPIRE = GREECE + PERSIA_W + EGYPT + PERSIA_E + INDUS

# who ended up with what, roughly, once the generals had fought it out (by 301 BCE)
SPLIT = [(["Egypt", "Israel", "Palestine", "Jordan", "Lebanon", "Cyprus", "N. Cyprus"], (46, 122, 128)),     # Ptolemy
         (["Syria", "Iraq", "Iran", "Kuwait", "Afghanistan", "Turkmenistan", "Uzbekistan", "Tajikistan",
           "Armenia", "Azerbaijan", "Pakistan"], (168, 52, 40)),                                                # Seleucus
         (["Turkey"], (112, 84, 150)),                                                                          # Lysimachus
         (GREECE, (196, 150, 48))]                                                                              # Cassander

CX, CY = -1000, 10300          # the cold-open cluster, on the cork below the map


def build_film(doc):
    L, E, W = doc.L, doc.E, doc.W
    film = Film(doc.duration, fps=30, look="wall")
    cam, foc, cue = film.cam, film.focus, film.cue

    em = film.add(GeoMap(doc.map("empire"), K, look="explainer"))
    P = em.place
    pella, hell, issus, alex = P("Pella"), P("Hellespont"), P("Issus"), P("Alexandria")
    gaug, bab, hk, jh, beas = P("Gaugamela"), P("Babylon"), P("Hindu Kush"), P("Jhelum"), P("Beas")

    # ============================================================ COLD OPEN (1-4)
    film.add(BigText("323 ई.पू.", bab[0], bab[1] - 1500, 640, L(1) - 0.1, t_out=L(5), type_on=0.5, bar=HILITE, bar_h=0.92,
                     rgb=DARK, shadow=False))
    film.add(XMarker(*bab, "बेबीलोन", t_in=W(1, "बेबीलोन") + 0.05, side="right", **LBL))
    alexp = film.add(Print("P01", CX, 11000, 2300, rot=-1.4, t_in=L(2) - 0.15, label="सिकंदर", label_t=W(2, "उम्र")))
    film.add(StringLine(bab, (CX, 11000 - 1050), t_in=L(2), dur=0.8, sag=0.03, width=16, t_out=W(3, "ज़मीन") - 0.4))
    film.add(Counter(CX - 3100, 10500, 900, 32, W(2, "बत्तीस") - 0.1, dur=0.7, caption="साल की उम्र"))
    film.add(Counter(CX + 3500, 10500, 900, 50, W(3, "पचास") - 0.1, dur=0.9, suffix=" लाख", caption="वर्ग किलोमीटर"))
    film.add(RegionFill(em, EMPIRE, MUSTARD, W(3, "ज़मीन") - 0.6, t_out=L(5) + 0.3, alpha=0.9))
    note = dict(font="labelm", rgb=CREAMY, hit=None, shadow=False)
    film.add(BigText("नक़्शा: आज की सरहदें, साम्राज्य का फैलाव अनुमानित", 200, 7350, 190, W(3, "ज़मीन"), t_out=L(6), **note))

    title_t = E(4) + 0.4
    film.add(BigText("सिकंदर का साम्राज्य", 2200, -6500, 1500, title_t, rgb=DARK, hit=None, shadow=False, bar=HILITE, bar_h=0.92))
    film.add(PenMark("underline", 2200, -5900, 9000, 0, t_in=title_t + 0.35, dur=0.6, width=30, seed=4, rgb=(200, 40, 30)))
    cue("boom", title_t, 0.55)

    cam(0.0, bab[0], bab[1] - 1400, 0.95, -1.0)                     # the date over Babylon
    cam(W(1, "बेबीलोन") + 0.3, bab[0] + 300, bab[1] - 800, 0.62, -0.4)
    cam(E(1) - 0.2, bab[0] + 400, bab[1] - 700, 0.58, 0.0)
    cam(L(2) + 0.5, CX, 10900, 0.62, -0.6)                          # the portrait lands; the counter beside it
    cam(E(2) + 0.1, CX - 1300, 10800, 0.55, -0.3)
    cam(W(3, "पचास") + 0.1, CX + 2400, 10600, 0.52, 0.0)
    cam(W(3, "ज़मीन") + 0.3, 1200, -800, 0.14, 0.0)                    # pull back: the whole empire filled
    cam(W(4, "हिंदुस्तान"), 1500, -1200, 0.13, 0.0)
    cam(title_t + 0.5, 1600, -2800, 0.13, 0.0)                      # title over the whole map
    cam(title_t + 1.3, 1700, -3000, 0.13, 0.0)
    foc(0.0, bab[0], bab[1] - 1400, 1900, 0.5)
    foc(W(1, "बेबीलोन") + 0.2, bab[0] + 300, bab[1] - 800, 4000, 0.35)
    foc(E(1) - 0.2, bab[0] + 400, bab[1] - 700, 4000, 0.35)
    foc(L(2) + 0.4, CX, 10900, 2200, 0.6)
    foc(E(2), CX - 1800, 10700, 3000, 0.5)
    foc(W(3, "पचास"), CX + 2200, 10600, 3000, 0.5)
    foc(W(3, "ज़मीन") - 0.1, 500, 0, 16000, 0.15)
    foc(title_t + 0.2, 1200, -2500, 18000, 0.12)

    # ============================================================ MACEDON (5-7)
    film.add(RegionFill(em, GREECE, RUST, W(5, "मकदूनिया") - 0.3, to_rgb=MUSTARD, t_change=L(6) + 0.3, t_out=W(16, "सेनापति")))
    film.add(XMarker(*pella, "मकदूनिया", t_in=W(5, "मकदूनिया"), side="left", **LBL))
    BX, BY = -9600, -11300
    film.add(Print("P03", BX, BY, 1700, rot=1.8, t_in=W(5, "बीस") - 0.2, label="सिकंदर, 20 साल", label_t=W(5, "राजा")))
    film.add(StringLine(pella, (BX, BY + 1550), t_in=W(5, "मकदूनिया") + 0.1, dur=0.6, sag=0.02, width=16))
    film.add(BigText("336 ई.पू.", BX, BY - 2250, 520, W(5, "तेरह"), t_out=L(7), bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False))
    film.add(Counter(BX + 4300, BY + 300, 800, 37000, W(6, "सैंतीस") - 0.1, dur=1.0, caption="सैनिक", t_out=L(9)))
    film.add(Route(pella, hell, t_in=W(6, "एशिया") - 0.5, dur=0.8, bend=-0.25, width=60))
    film.add(XMarker(*hell, "एशिया की ओर", t_in=W(6, "उतरा") - 0.2, side="right", **LBL))
    film.add(RegionFill(em, PERSIA_W, RUST, W(7, "फ़ारस") - 0.1, to_rgb=MUSTARD, t_change=W(8, "भागा") + 0.2, t_out=W(16, "सेनापति")))
    film.add(RegionFill(em, EGYPT, RUST, W(7, "फ़ारस") + 0.1, to_rgb=MUSTARD, t_change=W(9, "खोल") - 0.1, t_out=W(16, "सेनापति")))
    film.add(RegionFill(em, PERSIA_E, RUST, W(7, "फ़ारस") + 0.3, to_rgb=MUSTARD, t_change=W(10, "सिकंदर") - 0.1, t_out=W(16, "सेनापति")))
    film.add(BigText("फ़ारस", 2600, -500, 1300, W(7, "फ़ारस"), t_out=L(8) + 0.4, rgb=CREAMY))

    cam(L(5) + 0.7, -5200, -3000, 0.24, 0.0)                         # wide: back across to Macedonia
    cam(W(5, "बीस") + 0.2, BX, BY - 700, 0.46, 0.6)
    cam(E(5), BX + 200, BY - 800, 0.5, 0.8)
    cam(W(6, "सैंतीस") + 0.2, BX + 2400, BY + 300, 0.45, 0.2)
    cam(W(6, "एशिया"), -8200, -4600, 0.55, 0.0)
    cam(E(6) + 0.2, -8000, -4500, 0.58, -0.2)
    cam(W(7, "फ़ारस") + 0.3, -600, -1200, 0.2, 0.0)                    # Persia, all of it
    cam(E(7) + 0.4, 0, -1000, 0.19, 0.0)
    foc(L(5) + 0.6, -5200, -3000, 9000, 0.25)
    foc(W(5, "बीस") + 0.1, BX, BY, 2400, 0.55)
    foc(W(6, "सैंतीस"), BX + 2200, BY + 300, 4000, 0.45)
    foc(W(6, "एशिया") - 0.1, -8200, -5000, 3200, 0.45)
    foc(W(7, "फ़ारस") + 0.2, -600, -1000, 15000, 0.15)

    # ============================================================ PERSIA (8-10)
    DX, DY = -10400, -1100
    film.add(XMarker(*issus, "इस्सुस · 333 ई.पू.", t_in=W(8, "इस्सुस"), side="right", **LBL))
    dar = film.add(Print("P02", DX, DY, 2500, rot=-1.6, t_in=W(8, "इस्सुस") + 0.1, label="दारा, फ़ारस का बादशाह", label_t=W(8, "बादशाह") - 0.1))
    film.add(StringLine(issus, (DX + 900, DY - 1250), t_in=W(8, "लड़ाई"), dur=0.7, sag=0.04, width=16))
    film.add(Stamp("भागा", DX + 300, DY + 500, size=420, rot=-9, t_in=W(8, "भागा") - 0.05))
    film.add(Route(issus, alex, t_in=L(9) + 0.1, dur=1.2, bend=0.2, width=60))
    film.add(XMarker(*alex, "अलेक्ज़ेंड्रिया", t_in=W(9, "अलेक्ज़ेंड्रिया") - 0.05, side="left", **LBL))
    film.add(Route(alex, gaug, t_in=L(10) + 0.05, dur=1.3, bend=-0.22, width=60))
    film.add(XMarker(*gaug, "गौगामेला · 331 ई.पू.", t_in=W(10, "गौगामेला") + 0.3, side="right", **LBL))

    cam(L(8) + 0.4, -6500, -1600, 0.4, 0.4)
    cam(W(8, "बादशाह"), DX + 200, DY, 0.72, 0.8)
    cam(W(8, "भागा") + 0.3, DX + 200, DY + 300, 0.8, 1.0)
    cam(L(9) + 0.6, -5600, -700, 0.36, 0.0)                          # down the coast to Egypt
    cam(W(9, "अलेक्ज़ेंड्रिया") + 0.2, alex[0], alex[1] - 300, 0.48, -0.4)
    cam(L(10) + 0.7, -3700, -800, 0.32, 0.0)                          # across to Gaugamela
    cam(W(10, "हारा") + 0.2, gaug[0], gaug[1], 0.42, 0.2)
    cam(E(10) + 0.2, 200, -600, 0.19, 0.0)                            # Persia changes hands
    foc(L(8) + 0.3, -7000, -1500, 5000, 0.35)
    foc(W(8, "बादशाह") - 0.1, DX + 200, DY, 2300, 0.6)
    foc(L(9) + 0.5, -5600, -700, 5000, 0.3)
    foc(W(9, "अलेक्ज़ेंड्रिया"), alex[0], alex[1], 3000, 0.45)
    foc(L(10) + 0.6, -3500, -800, 5500, 0.3)
    foc(E(10), 200, -600, 15000, 0.12)

    # ============================================================ INDIA (11-14)
    CO = (16000, -3900)
    film.add(Route(gaug, hk, t_in=L(11) + 0.1, dur=1.8, bend=-0.12, width=60))
    film.add(XMarker(*hk, "हिंदू कुश", t_in=W(11, "हिंदू") - 0.1, side="left", **LBL))
    film.add(RegionFill(em, INDUS, RUST, W(12, "झेलम"), to_rgb=MUSTARD, t_change=W(13, "जीता"), t_out=W(16, "सेनापति")))
    film.add(Route(hk, jh, t_in=W(11, "हिंदुस्तान") - 0.3, dur=0.8, bend=0.2, width=60))
    film.add(XMarker(*jh, "झेलम · 326 ई.पू.", t_in=W(12, "झेलम") + 0.05, side="left", **LBL))
    coin = film.add(Print("P04", *CO, 2300, rot=2.0, t_in=W(12, "राजा") - 0.1, label="राजा पोरस का हाथी (सिक्का)", label_t=W(12, "हाथियों")))
    film.add(StringLine(jh, (CO[0] - 1100, CO[1] - 1100), t_in=W(12, "राजा"), dur=0.6, sag=0.03, width=16))
    film.add(PenMark("ellipse", CO[0], CO[1] - 100, 3200, 3000, t_in=W(13, "लौटा") - 0.3, dur=0.6, width=26, seed=9, rot=-3))
    film.add(Route(jh, beas, t_in=L(14) + 0.1, dur=0.6, bend=0.25, width=60))
    film.add(XMarker(*beas, "ब्यास नदी", t_in=W(14, "ब्यास") + 0.1, side="right", **LBL))
    film.add(Stamp("यहीं तक", beas[0] + 1400, beas[1] + 1300, size=380, rot=-7, t_in=W(14, "मना") - 0.05))

    cam(L(11) + 0.4, 3500, -1700, 0.18, 0.0)                          # wide: the long march east
    cam(W(11, "हिंदुस्तान"), hk[0] + 500, hk[1] + 300, 0.36, 0.2)
    cam(W(12, "झेलम") + 0.2, jh[0] + 1200, jh[1] - 1200, 0.4, 0.0)
    cam(W(12, "पोरस"), CO[0] - 600, CO[1] + 300, 0.55, 0.6)
    cam(W(12, "हाथियों") + 0.2, CO[0], CO[1] + 200, 0.75, 1.0)
    cam(E(13), CO[0] - 200, CO[1] + 100, 0.6, 0.6)
    cam(W(14, "ब्यास") + 0.2, beas[0] + 600, beas[1] + 600, 0.45, 0.0)
    cam(W(14, "मना") + 0.2, beas[0] + 1300, beas[1] + 1100, 0.55, -0.4)
    cam(E(14) + 0.4, beas[0] + 1200, beas[1] + 1000, 0.5, -0.5)
    foc(L(11) + 0.3, 4000, -1500, 14000, 0.15)
    foc(W(11, "हिंदुस्तान") - 0.1, hk[0], hk[1], 3500, 0.35)
    foc(W(12, "पोरस") + 0.3, CO[0], CO[1], 2600, 0.6)
    foc(W(14, "ब्यास"), beas[0] + 800, beas[1] + 800, 3000, 0.45)

    # ============================================================ CLOSE (15-17)
    film.add(Route(beas, bab, t_in=L(15) + 0.2, dur=1.6, bend=0.18, width=60))
    film.add(XMarker(*bab, None, t_in=W(15, "बेबीलोन"), size=3.6))
    film.add(BigText("323 ई.पू.", bab[0], bab[1] + 1400, 560, W(15, "बेबीलोन"), t_out=L(17), bar=HILITE, bar_h=0.92,
                     rgb=DARK, shadow=False))
    film.add(PenMark("strike", CX, 11000, 2100, 0, t_in=W(15, "मौत") - 0.1, dur=0.4, width=34, seed=15, rgb=(200, 40, 30)))
    for k, (names, rgb) in enumerate(SPLIT):
        film.add(RegionFill(em, names, rgb, W(16, "सेनापति") - 0.2 + 0.35 * k, alpha=0.9))
    for k in range(3):
        cue("heartbeat", W(16, "लड़") + k * 0.9, 0.5)

    cam(L(15) + 0.5, 5000, -1000, 0.14, 0.0)                           # back west along the route
    cam(W(15, "बेबीलोन") + 0.3, bab[0], bab[1] + 800, 0.42, 0.0)
    cam(W(16, "सेनापति"), 600, -600, 0.2, 0.0)                         # the map splits
    cam(E(16) + 0.2, 600, -400, 0.19, 0.0)
    cam(W(17, "ग्यारह"), 500, 0, 0.15, 0.0)
    cam(film.duration, 1200, 500, 0.118, 0.0)                         # the whole board
    foc(L(15) + 0.4, 5000, -800, 12000, 0.2)
    foc(W(15, "बेबीलोन"), bab[0], bab[1] + 800, 3500, 0.4)
    foc(W(16, "सेनापति") - 0.1, 600, -600, 16000, 0.12)
    foc(W(17, "ग्यारह"), 800, 500, 30000, 0.05)

    film.fade_in, film.fade_out = 0.8, 2.0
    return film
