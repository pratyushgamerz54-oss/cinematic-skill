"""पिछवाड़े के साँप: an investigative documentary, about 5:18, Hindi narration.

One evidence wall, left to right in time, with a timeline running along its top. Under each section
hangs a "screen": a bare Clip the camera flies into for a full-frame cutaway (3D globe shots recorded
with make_globe.py, the 3D compound model, and HyperFrames motion graphics). Times come from the
voiceover (doc.L / doc.E / doc.W), so a new read re-times everything.
"""
from engine import (HILITE, WHITE, BigText, Card, Clip, Counter, Film, PaperDoc, PenMark, Print, Stamp,
                    StringLine, Timeline)

SY = 7200                  # the row of screens under the wall
RED = (200, 40, 30)
CREAM = (244, 240, 232)
DARK = (26, 22, 20)
INK = (34, 32, 30)

# section centres along the wall
X0, X1, X2, X3, X4, X5, X6, X7 = 0, 12000, 24000, 40000, 58000, 72000, 86000, 104000


def build_film(doc):
    L, E, W = doc.L, doc.E, doc.W
    res = doc.res()

    def photo(key, x, y, w, rot=0.0, t_in=0.0, label=None, label_t=None, **kw):
        """A Print, or a named card in its place when the photo could not be fetched."""
        if key in doc.meta:
            return film.add(Print(key, x, y, w, rot=rot, t_in=t_in, label=label, label_t=label_t, **kw))
        return film.add(Card(x, y, w, w * 0.72, t_in, title=label or "", lines=["(तस्वीर उपलब्ध नहीं)"], rgb=(40, 38, 38),
                             text_rgb=(244, 240, 232), accent=(200, 40, 30), title_size=w * 0.075, body_size=w * 0.05))
    film = Film(doc.duration, fps=30, look="wall")
    shot, cue = film.shot, film.cue

    def screen(cid, x, t0, t1, start=0.0, rate=1.0):
        return film.add(Clip(doc.clip(cid), x, SY, 3840, t_in=t0, t_out=t1, start=start, rate=rate, frame=False, z=40))

    def into(x, t0, t1, z0=1.0, z1=1.035):
        """Camera fills the frame with the screen at x from t0 to t1, with a slow push."""
        shot(t0, x, SY, z0, 0.0, radius=9000, strength=0.0)
        shot(t1, x, SY, z1, 0.0, radius=9000, strength=0.0)

    hf = {s: s for s in ("hf_qopen", "hf_title", "hf_proxy", "hf_mullen", "hf_clinton", "hf_fatf", "hf_mask", "hf_asif", "hf_qend")}

    # ---------------------------------------------------------------- the timeline along the top
    years = [("1980 का दशक", "अफ़ग़ान जिहाद", X1, L(7) + 0.3), ("1989", "कश्मीर", X2 - 2000, L(13) + 0.2),
             ("1999", "IC-814", X2 + 4000, L(16) + 0.3), ("2008", "26/11", X3, L(19) + 0.2),
             ("2011", "एबटाबाद", X4, L(27) + 0.2), ("2014", "पेशावर", X5, L(34) + 0.2),
             ("2018", "FATF", X6, L(43) + 0.1), ("2019", "पुलवामा", X7 - 3000, L(49) + 0.2), ("2025", "पहलगाम", X7 + 5000, L(53) + 0.2)]
    TX0, TX1 = -6000, X7 + 12000
    film.add(Timeline((TX0 + TX1) / 2, -6200, TX1 - TX0, [(d, c, t) for d, c, _, t in years], t_in=L(7) - 0.2,
                      pos=[(x - TX0) / (TX1 - TX0) for *_, x, _ in years], size=300, dur=1.2, rgb=CREAM, accent=RED))

    # ============================================================ COLD OPEN (1-6)
    screen("g_abbottabad", X0, 0.0, L(2) + 0.1)
    screen("compound", X0, L(2), L(3) + 0.4)
    film.add(BigText("2 मई 2011", X0, SY - 1500, 260, L(1) + 0.2, t_out=L(2) + 0.2, bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False, z=60))
    into(X0, 0.0, L(2) - 0.05)
    into(X0, L(2), E(2) + 0.3, 1.0, 1.06)
    # line 3: pull back out of the screen onto the wall: the real compound, from the air
    aerial = photo("P01", X0 + 300, -600, 3600, rot=-1.4, t_in=L(3) - 0.3, label="ओसामा बिन लादेन का ठिकाना", label_t=W(3, "ओसामा"))
    photo("P02", X0 + 4300, 900, 2300, rot=2.2, t_in=L(3) + 0.6, label="एबटाबाद · 4 मई 2011", label_t=L(3) + 1.2)
    shot(L(3) - 0.1, X0 + 1200, 2600, 0.42, 0.4)
    shot(L(3) + 1.0, X0 + 1500, -200, 0.62, -0.4, strength=0.5)
    shot(E(3), X0 + 1300, 0, 0.66, -0.6, strength=0.5)
    screen("compound", X0, L(4) - 0.2, L(5) + 0.2, start=3.4)
    into(X0, L(4) + 0.1, E(4) + 0.2, 1.0, 1.04)
    shot(L(4) - 0.25, X0 + 600, SY - 1800, 0.55, 0.0, strength=0.2)
    screen(hf["hf_qopen"], X0, L(5) - 0.1, L(6) + 0.1)
    into(X0, L(5), E(5) + 0.4, 1.0, 1.05)
    cue("heartbeat", W(5, "इत्तेफ़ाक़"), 0.7); cue("heartbeat", W(5, "पैटर्न"), 0.7)
    screen(hf["hf_title"], X0, L(6) + 0.4, L(7) + 0.6)
    into(X0, L(6) + 0.4, L(7) - 0.2, 1.0, 1.05)
    cue("boom", E(6) + 0.2, 0.6)

    # ============================================================ ROOTS (7-12)
    photo("P03", X1 - 3600, -700, 2600, rot=-2.0, t_in=L(7) + 0.3, label="अफ़ग़ान मुजाहिदीन · 1985", label_t=W(7, "अफ़ग़ानिस्तान"))
    shot(L(7) - 0.2, X1 - 2500, -4200, 0.33, 0.0, strength=0.3)       # the timeline draws on
    shot(L(7) + 1.4, X1 - 3400, -1500, 0.55, -0.5)
    screen("g_roots", X1, L(8) - 0.2, L(10) + 0.2)
    shot(L(8) - 0.3, X1 - 1600, 3200, 0.45, 0.0, strength=0.2)
    into(X1, L(8) + 0.4, E(9) + 0.2, 1.0, 1.06)
    film.add(Stamp("ISI", X1 + 900, SY + 300, size=520, rot=-8, t_in=W(9, "आई") - 0.05, z=60))
    screen(hf["hf_proxy"], X1, L(10) - 0.1, L(11) + 0.4)
    into(X1, L(10), E(10) + 0.1, 1.0, 1.04)
    film.add(BigText("प्रॉक्सी वॉर", X1 + 3000, 600, 900, W(11, "प्रॉक्सी") - 0.05, rgb=CREAM))
    shot(L(11) + 0.1, X1 + 3000, 300, 0.72, 0.6)
    shot(E(11) + 0.3, X1 + 3000, 300, 0.78, 0.8)
    cue("riser", L(12) - 0.2, 0.5, dur=1.6)
    shot(L(12) + 0.4, X1 + 7000, -1500, 0.36, 0.0, strength=0.35)
    shot(E(12) + 0.6, X2 - 3000, -900, 0.4, 0.0, strength=0.4)

    # ============================================================ KASHMIR (13-18)
    film.add(BigText("1989 · कश्मीर", X2 - 2000, -2400, 520, L(13) + 0.1, bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False))
    let = film.add(Card(X2 - 3600, 600, 3000, 1800, W(14, "लश्कर") - 0.1, title="लश्कर-ए-तैयबा", lines=["स्थापना: लगभग 1990", "मुख्यालय: मुरीदके, पाकिस्तान"],
                        rgb=(236, 230, 220), text_rgb=INK, accent=RED, title_size=230, body_size=140))
    film.add(Card(X2 + 200, 300, 2300, 1200, W(15, "आरोप") - 0.1, title="भारत: आरोप", lines=["फ़ौज और ISI का साथ"], rgb=(236, 230, 220), text_rgb=INK, accent=RED, title_size=200, body_size=130))
    film.add(Card(X2 + 200, 1800, 2300, 1200, W(15, "इनकार") - 0.1, title="पाकिस्तान: इनकार", lines=["सरकारी भूमिका से इनकार"], rgb=(205, 212, 220), text_rgb=INK, accent=(60, 90, 140), title_size=200, body_size=130))
    shot(L(13) + 0.3, X2 - 2000, -1600, 0.6, 0.0)
    shot(L(14) + 0.3, X2 - 3600, 600, 0.62, -0.5)
    shot(L(15) + 0.4, X2 + 200, 1050, 0.6, 0.4)
    shot(E(15), X2 + 300, 1050, 0.62, 0.6)
    screen("g_ic814", X2 + 4000, L(16) - 0.2, L(17) + 0.2)
    shot(L(16) - 0.35, X2 + 3000, 4200, 0.45, 0.0, strength=0.2)
    into(X2 + 4000, L(16) + 0.3, E(16) + 0.1, 1.0, 1.05)
    un = film.add(PaperDoc(X2 + 9000, 600, 3000, 3800, rot=1.2, t_in=L(17) - 0.1, rows=14, sentence_row=6, sentence_size=120,
                           header=(("UNITED NATIONS SECURITY COUNCIL", 130, "serif"), ("SANCTIONS LIST · QDi.422", 96, "mono"),
                                   ("MOHAMMED MASOOD AZHAR ALVI", 120, "cond")),
                           sentence="Founded Jaish-i-Mohammed (JEM) upon his release from prison in India in 1999."))
    spans = un.phrase_spans(res, "upon his release from prison in India in 1999.")
    for k, ((hx, hy), hw) in enumerate(spans):
        film.add(PenMark("highlight", hx, hy - 40, hw + 60, 0, t_in=W(17, "संयुक्त") - 0.2 + 0.25 * k, dur=0.35, width=150, rot=1.2, seed=7 + k))
    film.add(StringLine((X2 - 3600, -300), (X2 + 9000, -1300), t_in=W(17, "जैश") - 0.1, dur=0.8, sag=0.04, width=24))
    shot(L(17) + 0.3, X2 + 9000, 600, 0.55, 0.6)
    hx0, hy0 = spans[0][0]
    shot(W(17, "संयुक्त"), hx0 + 900, hy0 + 100, 0.85, 1.0)
    shot(L(18) + 0.2, X2 + 6000, 0, 0.3, 0.0, radius=900, strength=0.88)   # the wall goes dark
    shot(E(18) + 0.7, X2 + 9000, -500, 0.3, 0.0, radius=900, strength=0.9)
    cue("heartbeat", L(18) + 0.4, 0.8); cue("heartbeat", E(18) + 0.1, 0.8)

    # ============================================================ MUMBAI (19-26)
    screen("g_mumbai", X3, L(19) - 0.1, L(20) + 0.3)
    into(X3, L(19) + 0.1, E(19) + 0.1, 1.0, 1.06)
    film.add(BigText("26/11 · 2008", X3, SY - 1500, 260, L(19) + 0.2, t_out=L(20), bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False, z=60))
    photo("P04", X3 + 4500, -900, 3000, rot=1.6, t_in=L(20) - 0.2, label="ताज होटल, मुंबई · दिसंबर 2008", label_t=L(20) + 0.4)
    film.add(Counter(X3 + 4500, 2300, 900, 166, W(20, "छियासठ") - 0.6, dur=1.0, caption="लोग मारे गए"))
    shot(L(20) + 0.2, X3 + 4500, 300, 0.42, 0.4)
    shot(E(20), X3 + 4500, 700, 0.46, 0.2)
    film.add(Card(X3 + 8800, -900, 2200, 2400, L(21) - 0.1, title="अजमल कसाब", lines=["ज़िंदा पकड़ा गया", "पाकिस्तानी नागरिक", "(तस्वीर नहीं दिखाई गई)"],
                  rgb=(40, 38, 38), text_rgb=CREAM, accent=RED, title_size=230, body_size=135))
    shot(L(21) + 0.3, X3 + 8800, -900, 0.62, -0.4)
    film.add(Card(X3 + 12600, -900, 2600, 1700, L(22) - 0.1, title="अदालत · शिकागो 2011", lines=["गवाह: डेविड हेडली"], rgb=(236, 230, 220), text_rgb=INK, accent=RED, title_size=200, body_size=150))
    iq = film.add(Card(X3 + 12600, 1700, 2600, 2200, L(23) - 0.1, title="मेजर इक़बाल", lines=["ISI अफ़सर (हेडली के मुताबिक़)", "चेहरा: अज्ञात", "हैंडलर"], rgb=(236, 230, 220), text_rgb=INK, accent=RED, title_size=230, body_size=140))
    film.add(StringLine((X3 + 12600, -50), (X3 + 12600, 600), t_in=L(23) + 0.2, dur=0.5, sag=0.02, width=20))
    film.add(Stamp("आरोपी", X3 + 13300, 2300, size=380, rot=-10, t_in=W(24, "आरोप") - 0.05))
    film.add(PenMark("underline", X3 + 12600, 50, 2200, 30, t_in=W(25, "शीर्ष") - 0.2, dur=0.5, width=30, seed=11, rgb=(60, 90, 140)))
    film.add(BigText("पर शीर्ष नेतृत्व शामिल नहीं: हेडली", X3 + 12600, -2350, 240, W(25, "शीर्ष") - 0.1, font="label", rgb=CREAM, hit=None, shadow=False))
    shot(L(22) + 0.3, X3 + 12600, -900, 0.6, 0.4)
    shot(L(23) + 0.4, X3 + 12600, 1300, 0.55, 0.0)
    shot(L(24) + 0.6, X3 + 12900, 2000, 0.62, -0.4)
    shot(L(25) + 0.3, X3 + 12600, -1200, 0.5, 0.0)
    shot(E(25), X3 + 12600, -1300, 0.52, 0.2)
    cue("riser", L(26) + 0.5, 0.6, dur=2.0)
    shot(L(26) + 0.8, (X3 + X4) / 2 + 2000, -1000, 0.2, 0.0, strength=0.4)      # the camera races back toward Abbottabad
    shot(E(26) + 0.5, X4 - 1000, -700, 0.36, 0.0, strength=0.45)

    # ============================================================ ABBOTTABAD (27-33)
    photo("P01", X4, -700, 3600, rot=1.0, t_in=L(26) + 2.0, label="एबटाबाद", label_t=L(27) + 0.3)
    film.add(BigText("2 मई 2011", X4, -3500, 520, L(27) + 0.1, bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False))
    film.add(Stamp("पता नहीं?", X4 + 500, -300, size=440, rot=-9, t_in=W(28, "पता") - 0.05))
    shot(L(27) + 0.3, X4, -1600, 0.55, 0.0)
    shot(L(28) + 0.5, X4 + 300, -600, 0.62, -0.5)
    photo("P05", X4 + 5200, -900, 2300, rot=-1.6, t_in=W(29, "एडमिरल") - 0.2, label="एडमिरल माइक मलन", label_t=W(29, "एडमिरल") + 0.1)
    shot(L(29) + 0.4, X4 + 5200, -700, 0.6, 0.4)
    screen(hf["hf_mullen"], X4 + 5200, L(30) - 0.2, L(31) + 0.2)
    shot(L(30) - 0.35, X4 + 5200, 3800, 0.45, 0.0, strength=0.2)
    into(X4 + 5200, L(30) + 0.15, E(30) + 0.2, 1.0, 1.04)
    photo("P06", X4 + 9600, -900, 2300, rot=1.8, t_in=W(31, "हिलेरी") - 0.2, label="हिलेरी क्लिंटन", label_t=W(31, "हिलेरी") + 0.1)
    shot(L(31) + 0.4, X4 + 9600, -700, 0.6, -0.4)
    screen(hf["hf_clinton"], X4 + 9600, L(32) - 0.2, L(33) + 0.2)
    shot(L(32) - 0.35, X4 + 9600, 3800, 0.45, 0.0, strength=0.2)
    into(X4 + 9600, L(32) + 0.15, E(32) + 0.3, 1.0, 1.04)
    shot(L(33) + 0.3, (X4 + X5) / 2 + 2000, -500, 0.28, 0.0, radius=1200, strength=0.8)
    cue("heartbeat", L(33) + 0.3, 0.7)

    # ============================================================ PESHAWAR (34-38)
    film.add(BigText("16 दिसंबर 2014 · पेशावर", X5, -2600, 440, L(34) + 0.1, bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False))
    film.add(Counter(X5, -200, 1300, 132, W(35, "बत्तीस") - 1.2, dur=1.8, caption="बच्चे"))
    for k in range(5):                                         # candles: small warm lights, no images of victims
        film.add(PenMark("highlight", X5 - 2400 + k * 1200, 1900, 120, 0, t_in=L(35) + 0.8 + 0.15 * k, dur=0.3, width=120, rgb=(255, 190, 90), seed=k))
    shot(L(34) + 0.3, X5, -1700, 0.5, 0.0)
    shot(L(35) + 0.3, X5, 0, 0.55, 0.0)
    shot(E(35), X5, 200, 0.58, 0.2)
    film.add(StringLine((X4 + 9600, -2100), (X5 - 900, -1800), t_in=L(36) + 0.2, dur=1.4, sag=0.12, width=34))   # the snake turns back
    shot(L(36) + 0.4, (X4 + X5) / 2 + 3000, -1400, 0.3, 0.0, strength=0.3)
    shot(E(36), X5 - 800, -800, 0.42, 0.0)
    film.add(Card(X5 + 5200, -800, 2800, 1500, L(37) - 0.1, title="नेशनल एक्शन प्लान", lines=["दिसंबर 2014", "अपने यहाँ के गुटों पर अभियान"], rgb=(236, 230, 220), text_rgb=INK, accent=(60, 90, 140), title_size=200, body_size=140))
    film.add(Card(X5 + 4100, 1500, 2000, 1300, W(38, "भारत") - 0.2, title="'अच्छे'", lines=["भारत, अफ़ग़ानिस्तान पर"], rgb=(236, 230, 220), text_rgb=INK, accent=RED, title_size=220, body_size=130))
    film.add(Card(X5 + 6300, 1500, 2000, 1300, W(38, "भारत") + 0.1, title="'बुरे'", lines=["पाकिस्तान पर हमला करने वाले"], rgb=(205, 212, 220), text_rgb=INK, accent=(60, 90, 140), title_size=220, body_size=130))
    film.add(BigText("आलोचकों का आरोप", X5 + 5200, 2700, 200, W(38, "आलोचकों"), font="label", rgb=CREAM, hit=None, shadow=False))
    shot(L(37) + 0.3, X5 + 5200, -800, 0.6, 0.4)
    shot(L(38) + 0.4, X5 + 5200, 1600, 0.52, -0.3)
    shot(E(38) + 0.2, X5 + 5200, 1700, 0.54, -0.4)

    # ============================================================ MONEY (39-48)
    cue("riser", L(39) + 0.4, 0.5, dur=1.6)
    dawn = film.add(PaperDoc(X6 - 4600, -300, 3200, 4000, rot=-1.3, t_in=W(39, "पाकिस्तान") - 0.4, rows=15, sentence_row=6, sentence_size=120,
                             header=(("DAWN", 260, "serif"), ("ISLAMABAD · 3 AUGUST 2015", 96, "mono"), ("TARIQ KHOSA, FORMER FIA DIRECTOR GENERAL", 92, "cond")),
                             sentence="Pakistan has to deal with the Mumbai mayhem, planned and launched from its soil."))
    dsp = dawn.phrase_spans(res, "planned and launched from its soil.")
    for k, ((hx, hy), hw) in enumerate(dsp):
        film.add(PenMark("highlight", hx, hy - 40, hw + 60, 0, t_in=W(41, "प्लान") - 0.3 + 0.3 * k, dur=0.4, width=150, rot=-1.3, seed=21 + k))
    film.add(StringLine((X6 - 4600, -2300), (X3 + 4500, -2400), t_in=W(41, "मुंबई"), dur=1.0, sag=0.05, width=24, persist=True))
    shot(L(39) + 0.5, X6 - 4600, -600, 0.45, 0.0)
    shot(L(40) + 0.4, X6 - 4600, -1200, 0.62, -0.6)
    dx0, dy0 = dsp[0][0]
    shot(L(41) + 0.1, dx0 + 1000, dy0 + 100, 0.82, -1.0)
    shot(E(41) + 0.2, dx0 + 1100, dy0 + 150, 0.86, -1.1)
    film.add(BigText("पैसों का पीछा", X6, -2700, 520, W(42, "पैसों") - 0.1, rgb=CREAM))
    shot(L(42) + 0.2, X6, -2300, 0.5, 0.0)
    film.add(BigText("जून 2018", X6, -1500, 400, L(43) - 0.05, bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False))
    fatf = film.add(Card(X6, 700, 3200, 1900, L(44) - 0.1, title="FATF", lines=["आतंकी फ़ंडिंग पर निगरानी", "पाकिस्तान: जून 2018 से"], rgb=(236, 230, 220), text_rgb=INK, accent=RED, title_size=320, body_size=150))
    grey = film.add(Stamp("ग्रे लिस्ट", X6 + 300, 900, size=520, rot=-8, t_in=W(44, "ग्रे") - 0.05, t_out=W(47, "बाहर")))
    shot(L(43) + 0.1, X6, -900, 0.55, 0.0)
    shot(W(44, "ग्रे") + 0.2, X6, 700, 0.6, 0.3)
    screen(hf["hf_fatf"], X6, L(45) - 0.2, L(46) + 0.2)
    shot(L(45) - 0.3, X6, 3900, 0.45, 0.0, strength=0.2)
    into(X6, L(45) + 0.1, E(45) + 0.2, 1.0, 1.04)
    film.add(Card(X6 + 4600, -500, 2800, 1700, L(46) - 0.1, title="हाफ़िज़ सईद", lines=["लश्कर का संस्थापक", "टेरर-फ़ंडिंग: 31 साल (2022)"], rgb=(236, 230, 220), text_rgb=INK, accent=RED, title_size=230, body_size=140))
    shot(L(46) + 0.3, X6 + 4600, -500, 0.62, -0.4)
    film.add(Stamp("बाहर · अक्टूबर 2022", X6 + 200, 1700, size=300, rot=6, rgb=(60, 90, 140), t_in=W(47, "बाहर") - 0.05))
    shot(L(47) + 0.3, X6 + 100, 1100, 0.55, 0.2)
    shot(L(48) + 0.3, X6 + 5000, 0, 0.3, 0.0, radius=900, strength=0.9)       # hard dark: "...नहीं।"
    cue("heartbeat", W(48, "नहीं"), 0.9)

    # ============================================================ NOW (49-60)
    film.add(BigText("पुलवामा · 14 फ़रवरी 2019", X7 - 4500, -2600, 420, L(49) + 0.1, bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False))
    film.add(Counter(X7 - 4500, -400, 1100, 40, W(49, "चालीस") - 0.2, dur=0.8, caption="CRPF जवान"))
    film.add(StringLine((X7 - 4500, 300), (X2 + 9000, -1300), t_in=W(49, "जैश") - 0.2, dur=1.4, sag=0.05, width=24))
    shot(L(49) + 0.3, X7 - 4500, -1700, 0.55, 0.0)
    shot(W(49, "चालीस"), X7 - 4500, -700, 0.6, 0.3)
    shot(W(49, "जैश"), X7 - 10000, -1200, 0.2, 0.0, strength=0.3)
    film.add(Card(X7 - 4500, 2400, 2600, 1300, L(50) - 0.1, title="मसूद अज़हर", lines=["UN 1267 सूची"], rgb=(236, 230, 220), text_rgb=INK, accent=RED, title_size=220, body_size=150))
    film.add(Stamp("1 मई 2019", X7 - 4300, 2600, size=330, rot=-7, t_in=W(50, "सूची") - 0.05))
    shot(L(50) + 0.6, X7 - 4500, 2300, 0.6, -0.3)
    photo("P07", X7, -900, 2200, rot=-1.5, t_in=L(51) - 0.1, label="इमरान ख़ान · जुलाई 2019", label_t=W(51, "इमरान"))
    film.add(BigText("30,000–40,000", X7, 1900, 700, W(52, "तीस") - 0.1, rgb=CREAM, type_on=0.5))
    film.add(BigText("हथियारबंद लोग, अब भी पाकिस्तान में", X7, 2500, 190, W(52, "हथियारबंद"), font="label", rgb=CREAM, hit=None, shadow=False))
    shot(L(51) + 0.3, X7, -800, 0.6, 0.3)
    shot(L(52) + 0.4, X7, 1700, 0.62, 0.0)
    shot(E(52), X7, 1900, 0.64, 0.0)
    screen("g_pahalgam", X7 + 5000, L(53) - 0.2, L(54) + 0.3)
    film.add(Counter(X7 + 5000, SY + 1300, 600, 26, W(53, "छब्बीस") - 0.1, dur=0.7, caption="आम लोग"))
    shot(L(53) - 0.35, X7 + 5000, 3800, 0.45, 0.0, strength=0.2)
    into(X7 + 5000, L(53) + 0.1, E(53) + 0.2, 1.0, 1.05)
    film.add(Card(X7 + 9400, -800, 2800, 1700, L(54) - 0.1, title="UN रिपोर्ट · 2025", lines=["ज़िम्मेदारी: TRF (दो बार)", "फिर दावा वापस"], rgb=(236, 230, 220), text_rgb=INK, accent=RED, title_size=210, body_size=140))
    shot(L(54) + 0.4, X7 + 9400, -800, 0.62, 0.3)
    screen(hf["hf_mask"], X7 + 9400, L(55) - 0.2, L(56) + 0.2)
    shot(L(55) - 0.3, X7 + 9400, 3800, 0.45, 0.0, strength=0.2)
    into(X7 + 9400, L(55) + 0.1, E(55) + 0.2, 1.0, 1.04)
    asif = photo("P08", X7 + 13600, -900, 2200, rot=1.4, t_in=W(56, "ख़्वाजा") - 0.2, label="ख़्वाजा आसिफ़ · रक्षा मंत्री", label_t=W(56, "ख़्वाजा") + 0.1)
    shot(L(56) + 0.4, X7 + 13600, -800, 0.6, -0.4)
    screen(hf["hf_asif"], X7 + 13600, L(57) - 0.25, L(59) + 0.2)
    shot(L(57) - 0.4, X7 + 13600, 3800, 0.45, 0.0, strength=0.2)
    into(X7 + 13600, L(57) + 0.1, E(58) + 0.2, 1.0, 1.05)
    film.add(Stamp("इनकार", X7 + 14100, -600, size=460, rot=-8, t_in=W(59, "इनकार") - 0.05))
    shot(L(59) + 0.2, X7 + 13600, -700, 0.62, 0.3)
    screen("g_pahalgam", X7 + 5000, L(60) - 0.3, L(61) + 0.3, start=5.0)
    film.add(BigText("ऑपरेशन सिंदूर · 7 मई 2025", X7 + 5000, SY - 1600, 230, L(60) + 0.2, bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False, z=60))
    shot(L(60) - 0.45, X7 + 7500, 3600, 0.42, 0.0, strength=0.2)
    into(X7 + 5000, L(60) + 0.2, E(60) + 0.3, 1.0, 1.04)

    # ============================================================ VERDICT (61-66)
    WALLX = (TX0 + TX1) / 2
    shot(L(61) + 0.3, WALLX, -1500, 0.06, 0.0, radius=60000, strength=0.05)     # the whole case
    shot(E(61) + 0.3, WALLX, -1500, 0.058, 0.0, radius=60000, strength=0.05)
    exhibits = [(X3 + 12600, 1700), (X4 + 5200, -900), (X2 + 9000, 600), (X7 + 13600, -900)]   # court, general, UN list, leaders
    for k, (ex, ey) in enumerate(exhibits):
        film.add(PenMark("ellipse", ex, ey, 3600, 3600, t_in=L(62) + 0.4 + 1.35 * k, dur=0.5, width=60, seed=40 + k))
    for k, (ex, ey) in enumerate(exhibits + [(X0 + 300, -600), (X1 + 900, SY - 2000)]):
        film.add(StringLine((ex, ey), (X5 + 600, -4300), t_in=L(63) + 0.2 + 0.15 * k, dur=0.9, sag=0.05, width=60, persist=True))
    film.add(BigText("प्रॉक्सी का लंबा खेल", X5 + 600, -4700, 1500, W(63, "प्रॉक्सी") - 0.1, rgb=CREAM, z=70))
    shot(L(62) + 0.4, WALLX, -1000, 0.062, 0.0, radius=60000, strength=0.05)
    shot(L(63) + 0.3, X5 + 600, -3000, 0.12, 0.0, radius=20000, strength=0.2)
    shot(L(64) + 0.2, X5, -200, 0.4, 0.0)                                           # Peshawar, lit once more
    shot(E(64), X5, 0, 0.42, 0.0)
    screen("g_verdict", X0, L(65) - 0.3, L(66) + 0.4)
    shot(L(65) - 0.4, X0 + 2000, 3800, 0.2, 0.0, strength=0.2)
    into(X0, L(65) + 0.2, E(65) + 0.3, 1.0, 1.03)
    screen(hf["hf_qend"], X0, L(66) - 0.1, doc.duration + 1)
    into(X0, L(66) + 0.1, doc.duration, 1.0, 1.05)
    cue("boom", L(66) + 0.1, 0.5)
    cue("heartbeat", W(66, "कब") , 0.7)

    film.fade_in, film.fade_out = 0.6, 1.5
    return film
