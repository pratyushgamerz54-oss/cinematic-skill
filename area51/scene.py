"""एरिया 51: पूरा कच्चा चिट्ठा. A mystery/investigative documentary, about 8:39, Hindi narration (the user's Viraj read).

A YouTube intro on its own HyperFrames graphic (welcome, three curiosity questions, title, go), a cold open on
Storm Area 51 (2019), the opening question, then one wall left to right in time with a timeline along its top.
Under each section hangs a "screen" row: Clips the camera flies into for full-frame cutaways (3D globes, the
Groom Lake 3D terrain map, the aircraft and S-4 models, NASA footage, HyperFrames hero graphics).
Palette (user: less red): night blue, radar teal, desert amber; moods radar/desert replace red tension.
A moving background (Atmos: dust, stars, light sweep, radar rings) keeps held frames alive.
Times come from the voiceover (doc.L / doc.E / doc.W), so a new read re-times everything.
"""
import math

from engine import (HILITE, Atmos, BarChart, BigText, Card, Clip, Counter, DotField, Film, PaperDoc, PenMark, Print,
                    Stamp, StringLine, Timeline)

SY = 7200                  # the row of screens under the wall
TEAL = (63, 224, 204)
AMBER = (255, 179, 71)
CREAM = (240, 244, 242)
DARK = (14, 18, 22)
INK = (30, 32, 34)
PAPER = (232, 232, 226)
NAVY = (36, 70, 110)
RED = (214, 64, 48)        # used sparingly: only for the gun, death and "STATE SECRETS"

# section centres along the wall
XS = [0, 16000, 50000, 88000, 126000, 162000, 196000, 237000, 263000, 302000, 336000, 376000]


def build_film(doc):
    L, E, W0 = doc.L, doc.E, doc.W
    res = doc.res()

    def has(i):
        return i in doc.seg

    def W(i, word, nth=0, frac=0.5):
        try:
            return W0(i, word, nth)
        except Exception:
            print("word not found:", i, word)
            return L(i) + (E(i) - L(i)) * frac

    def nxt(i):
        later = [j for j in doc.seg if j > i]
        return L(min(later)) if later else doc.duration

    film = Film(doc.duration, fps=30, look="wall")
    shot, cue = film.shot, film.cue
    film.add(Atmos(film))

    def photo(key, x, y, w, rot=0.0, t_in=0.0, label=None, label_t=None, **kw):
        if key in doc.meta:
            return film.add(Print(key, x, y, w, rot=rot, t_in=t_in, label=label, label_t=label_t, label_rgb=(20, 90, 96), **kw))
        print("photo missing:", key)
        return None

    def card(x, y, w, h, t, title, lines=(), dark=True, accent=TEAL, ts=230, bs=150, **kw):
        return film.add(Card(x, y, w, h, t, title=title, lines=list(lines), rgb=(22, 28, 34) if dark else PAPER,
                             text_rgb=CREAM if dark else INK, accent=accent, title_size=ts, body_size=bs, **kw))

    def bar(text, x, y, size, t, t_out=None, z=60):
        return film.add(BigText(text, x, y, size, t, t_out=t_out, bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False, z=z))

    def tag(text, x, y, size, t, t_out=None, rgb=TEAL, z=62):
        return film.add(BigText(text, x, y, size, t, t_out=t_out, font="label", rgb=DARK, bar=rgb, bar_h=0.92,
                                shadow=False, grunge=False, z=z))

    def screen(cid, x, t0, t1, start=0.0, rate=1.0):
        return film.add(Clip(doc.clip(cid), x, SY, 3840, t_in=t0, t_out=t1, start=start, rate=rate, frame=False, z=40))

    def into(x, t0, t1, z0=1.0, z1=1.035):
        shot(t0, x, SY, z0, 0.0, radius=9000, strength=0.0)
        shot(t1, x, SY, z1, 0.0, radius=9000, strength=0.0)

    def cut(cid, x, i0, i1=None, start=0.0, z1=1.04, label=None, until=None):
        """A full-frame cutaway on screen x from line i0 to the end of line i1 (or the next line).
        until: the camera leaves the screen at this time (when the line goes on to another visual)."""
        i1 = i1 or i0
        t0, t1 = L(i0) - 0.15, nxt(i1) + 0.05
        screen(cid, x, t0, (until + 0.6) if until else t1, start=start)
        into(x, t0 + 0.1, (until - 0.1) if until else t1 - 0.5, 1.0, z1)
        if label:
            tag(label, x - 1920 + 120 + len(label) * 38, SY + 1080 - 170, 120, t0 + 0.3, t_out=t1, rgb=AMBER)

    def look(t, x, y, z, rot=0.0, **kw):
        shot(t, x, y, z, rot, **kw)

    X = XS

    # ---------------------------------------------------------------- the timeline along the top
    years = [("1955", "ग्रूम लेक", X[2], L(14) + 0.3), ("1960", "U-2 गिरा", X[4], L(26) + 0.3),
             ("1962", "A-12", X[4] + 9000, L(27) + 0.3), ("1968", "MiG", X[5], L(32) + 0.3),
             ("1977", "स्टेल्थ", X[5] + 8000, L(33) + 0.3), ("1989", "लज़ार", X[6], L(37) + 0.3),
             ("1994", "अदालत", X[9], L(54) + 0.3), ("2013", "CIA ने माना", X[10], L(60) + 0.3),
             ("2024", "AARO", X[10] + 12000, L(64) + 0.3)]
    TX0, TX1 = X[2] - 9000, X[11] + 6000
    film.add(Timeline((TX0 + TX1) / 2, -6200, TX1 - TX0, [(d, c, t) for d, c, _, t in years], t_in=L(14) - 0.2,
                      pos=[(x - TX0) / (TX1 - TX0) for *_, x, _ in years], size=300, dur=1.2, rgb=CREAM, accent=TEAL))

    # ============================================================ YOUTUBE INTRO (1-6): its own motion graphic
    x = X[0]
    screen("hf_welcome", x, 0.0, L(2) + 0.1)
    into(x, 0.0, L(2) - 0.05, 1.0, 1.03)
    for i, st in [(2, 0.0), (3, 7.0), (4, 15.0), (5, 20.0)]:
        screen("hf_topic", x, L(i) - 0.1, nxt(i) + 0.05, start=st)
        into(x, L(i) - 0.05, nxt(i) - 0.5, 1.0, 1.03)
    cue("heartbeat", W(3, "गोली"), 0.6); cue("heartbeat", W(4, "दूसरी"), 0.7); cue("boom", W(5, "एरिया") - 0.1, 0.6)
    screen("hf_go", x, L(6) - 0.1, E(6) + 2.2)
    into(x, L(6), E(6) + 2.1, 1.0, 1.05)
    cue("whoosh", E(6) + 0.9, 0.5)

    # ============================================================ COLD OPEN: STORM AREA 51 (7-13)
    x = X[1]
    screen("g_nevada", x, E(6) + 2.1, nxt(7) + 0.1, start=max(0.0, 8.0 - (nxt(7) - E(6) - 2.1)))
    into(x, E(6) + 2.15, nxt(7) - 0.05, 1.0, 1.05)
    bar("सितंबर 2019 · नेवाडा", x, SY - 760, 230, L(7) + 0.2, t_out=nxt(7))
    ev = card(x - 4200, -400, 4600, 2400, L(8) - 0.2, "STORM AREA 51", ["\"They can't stop all of us\"", "फ़ेसबुक इवेंट · जून 2019 · मज़ाक़ में"],
              ts=340, bs=150, accent=AMBER)
    film.add(Stamp("मज़ाक़?", x - 2600, 900, size=380, rot=-8, t_in=W(8, "मज़ाक़") + 0.1, rgb=AMBER))
    look(L(8) + 0.05, x - 4200, -300, 0.5, -0.2)
    film.add(Counter(x + 3600, -900, 1100, 2000000, W(9, "बीस") - 0.5, dur=1.4, suffix="+", caption="लोगों ने लिखा: हम आ रहे हैं", rgb=TEAL))
    pts = [(x + 1400 + (k % 30) * 150, 600 + (k // 30) * 150) for k in range(300)]
    film.add(DotField(pts, W(9, "देखते"), W(9, "लिखा") + 0.4, rgb=TEAL, r=28))
    look(L(9) + 0.05, x + 3600, 100, 0.42, 0.0)
    photo("P06", x + 8600, -500, 3000, rot=-1.5, t_in=L(10) - 0.3, label="बैक गेट · 20 सितंबर 2019", label_t=W(10, "गेट"))
    photo("P07", x + 12500, -300, 2700, rot=1.8, t_in=W(10, "मेलों") - 0.5, label="'एलियनस्टॉक' मेला, रेचल", label_t=W(10, "मेलों"))
    film.add(Counter(x + 10600, 2300, 800, 1500, W(10, "हज़ार") - 0.6, dur=0.9, prefix="≈ ", caption="मेलों में", rgb=AMBER))
    look(L(10) + 0.05, x + 8600, -400, 0.55, -0.3)
    look(W(10, "मेलों") - 0.2, x + 10600, 600, 0.4, 0.2)
    photo("P04", x + 18600, -400, 2900, rot=1.2, t_in=L(11) - 0.3, label="मुख्य गेट के बोर्ड", label_t=L(11) + 0.4)
    film.add(BigText("USE OF DEADLY FORCE AUTHORIZED", x + 18600, 2200, 260, W(11, "जानलेवा") - 0.1, font="cond", rgb=CREAM,
                     bar=(120, 30, 24), bar_h=0.92, shadow=False, z=64))
    film.add(PenMark("underline", x + 18600, 2380, 3900, 0, t_in=W(11, "इजाज़त") - 0.1, dur=0.5, width=34, seed=11, rgb=AMBER))
    look(L(11) + 0.05, x + 18600, 700, 0.44, 0.2)
    screen("hf_qopen", x + 18600, L(12) - 0.1, nxt(12) + 0.05, start=max(0.0, 1.6 - (W(12, "आख़िर") - L(12))))
    shot(L(12) - 0.25, x + 18600, 3800, 0.45, 0.0, strength=0.2)
    into(x + 18600, L(12) + 0.05, nxt(12) - 0.5, 1.0, 1.05)
    cue("heartbeat", W(12, "आख़िर"), 0.7); cue("heartbeat", W(12, "गोली"), 0.8); cue("boom", E(12) + 0.1, 0.5)
    film.add(Counter(X[2] - 7000, 0, 1500, 1955, L(13) + 0.2, dur=1.8, caption="लगभग 70 साल पीछे", rgb=AMBER, start=2019))
    look(L(13) + 0.05, X[2] - 7000, -300, 0.45, 0.0)
    cue("riser", L(13) + 0.3, 0.5, dur=1.8)

    # ============================================================ 1955: A DRY LAKE (14-19)
    x = X[2]
    card(x - 1200, -700, 4400, 1900, L(14) - 0.1, "शीत युद्ध · 1955", ["सोवियत परमाणु बम: कितने? कहाँ?"], ts=300, bs=170, accent=AMBER)
    film.add(Stamp("?", x + 1900, 900, size=700, rot=8, t_in=W(14, "कहाँ") - 0.05, rgb=AMBER))
    look(L(14) + 0.1, x - 1000, -300, 0.5, 0.0)
    photo("P12", x + 5400, -600, 2800, rot=-1.4, t_in=L(15) - 0.3, label="केली जॉनसन और U-2 · स्कंक वर्क्स", label_t=W(15, "लॉकहीड"))
    look(L(15) + 0.05, x + 5400, -500, 0.58, -0.3)
    screen("air_A", x + 5400, W(15, "यू-टू") - 0.3, nxt(15) + 0.05, start=1.0)
    shot(W(15, "यू-टू") - 0.4, x + 5400, 3800, 0.45, 0.0, strength=0.2)
    into(x + 5400, W(15, "यू-टू"), nxt(15) - 0.5, 1.0, 1.04)
    photo("P13", x + 10400, -900, 1900, rot=1.5, t_in=L(16) - 0.3, label="रिचर्ड बिसेल · CIA", label_t=W(16, "सीआईए"))
    look(L(16) + 0.05, x + 10400, -800, 0.6, 0.3)
    screen("ter_A", x + 10400, W(16, "नेवाडा") - 0.6, nxt(16) + 0.05, start=max(0.0, 8.0 - (nxt(16) - W(16, "नेवाडा") + 0.6)))
    into(x + 10400, W(16, "नेवाडा") - 0.3, nxt(16) - 0.5, 1.0, 1.04)
    cut("ter_H", x + 14300, 17)
    tag("परमाणु परीक्षण क्षेत्र · बगल में", x + 14300, SY - 800, 170, W(17, "परमाणु"), t_out=nxt(17), rgb=AMBER)
    MX, MY = x + 21400, 200
    nums = [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55]          # symbolic grid of numbered map areas
    for k, n in enumerate(nums):
        cx_, cy_ = MX - 3300 + (k % 4) * 2200, MY - 1700 + (k // 4) * 1700
        hot = n == 51
        card(cx_, cy_, 2000, 1500, L(18) - 0.1 + 0.06 * k if not hot else W(18, "इक्यावन") - 0.3, str(n),
             ["AREA"] if hot else [], ts=420 if hot else 300, bs=150, accent=AMBER if hot else (60, 90, 100), dark=True)
    gx, gy = MX - 3300 + 3 * 2200, MY - 1700 + 1700
    film.add(PenMark("ellipse", gx, gy, 2700, 2100, t_in=W(18, "इक्यावन") - 0.05, dur=0.5, width=44, seed=18, rgb=AMBER))
    film.add(Stamp("AREA 51", gx, gy + 1500, size=360, rot=-8, t_in=W(18, "जन्म") - 0.2, rgb=TEAL))
    tag("नक़्शे के खाने (प्रतीकात्मक)", MX, MY - 3100, 150, L(18) + 0.2, rgb=TEAL)
    photo("P03", MX + 7800, -400, 2600, rot=1.6, t_in=W(18, "जन्म") - 0.4, label="CORONA उपग्रह · 1968", label_t=W(18, "जन्म"))
    look(L(18) - 0.1, MX, MY, 0.38, 0.0, radius=6000, strength=0.3)
    look(W(18, "इक्यावन") - 0.2, gx - 400, gy, 0.5, 0.0, radius=3000, strength=0.5)
    look(W(18, "जन्म") - 0.1, MX + 6400, -300, 0.4, 0.2)
    photo("P01", x + 31000, -300, 3600, rot=-1.0, t_in=L(19) - 0.3, label="ग्रूम लेक · आज", label_t=L(19) + 0.5)
    look(L(19) + 0.05, x + 31000, -200, 0.44, -0.2)
    look(E(19) - 0.6, x + 31000, -300, 0.5, -0.3)
    cue("riser", W(19, "उड़ने"), 0.5, dur=1.8); cue("heartbeat", W(19, "चौंका"), 0.6)

    # ============================================================ THE U-2 AND THE "SAUCERS" (20-25)
    x = X[3]
    cut("ft_er2", x, 20, start=12.0, label="NASA ER-2 · U-2 का नागरिक रूप (फ़ुटेज)")
    bar("अगस्त 1955", x, SY - 760, 230, L(20) + 0.2, t_out=nxt(20))
    film.add(BarChart(x + 4600, 400, 3600, 2600, [("यात्री विमान", 20000), ("U-2", 60000)], W(21, "यात्री") - 0.3,
                      stagger=0.9, suffix=" फ़ीट", rgb=CREAM, accent=TEAL, size=300))
    photo("P14", x + 9800, -800, 2600, rot=1.4, t_in=W(21, "यू-टू") - 0.3, label="U-2 · 1960", label_t=W(21, "साठ"))
    look(L(21) + 0.05, x + 4600, 300, 0.45, 0.0)
    look(W(21, "यू-टू"), x + 7000, 0, 0.38, 0.0)
    cut("air_B", x + 14000, 22, start=0.5)
    film.add(BigText("उड़न तश्तरी?", x + 14000, SY - 650, 380, W(22, "उड़न") - 0.1, t_out=nxt(22), rgb=TEAL, z=70))
    photo("P26", x + 19400, -300, 2200, rot=-1.6, t_in=L(23) - 0.3, label="प्रोजेक्ट ब्लू बुक · USAF", label_t=W(23, "टीमों"))
    for k, (nm, yy) in enumerate([("मौसम?", -1200), ("तारे?", 200), ("असली वजह?", 1600)]):
        card(x + 23200, yy, 2600, 1000, W(23, nm.rstrip("?").split()[-1] if k < 2 else "असली") - 0.2, nm, ts=230, accent=AMBER if k == 2 else TEAL)
    film.add(Stamp("छुपाई गई", x + 23300, 1800, size=380, rot=-7, t_in=W(23, "छुपा") - 0.05, rgb=AMBER))
    look(L(23) + 0.05, x + 20400, 0, 0.45, -0.2)
    look(W(23, "असली") - 0.2, x + 22400, 600, 0.45, 0.0)
    screen("hf_haines", x + 27400, L(24) - 0.1, nxt(24) + 0.05, start=max(0.0, 0.9 - (W(24, "आधी") - L(24))))
    shot(L(24) - 0.3, x + 27400, 3800, 0.45, 0.0, strength=0.2)
    into(x + 27400, L(24) + 0.05, nxt(24) - 0.5, 1.0, 1.04)
    film.add(BigText("परदा", x + 31600, -300, 1500, W(25, "परदा") - 0.2, rgb=TEAL, z=60))
    film.add(BigText("असली खेल... अभी बाक़ी", x + 31600, 1300, 300, W(25, "असली") - 0.1, font="label", rgb=CREAM, shadow=False, grunge=False))
    look(L(25) + 0.05, x + 31600, 300, 0.45, 0.0, radius=3000, strength=0.75)
    cue("riser", W(25, "लेकिन"), 0.5, dur=1.8); cue("heartbeat", W(25, "शुरू"), 0.7)

    # ============================================================ OXCART (26-29)
    x = X[4]
    cut("g_powers", x, 26, start=0.0, until=W(26, "पायलट") - 0.4)
    photo("P15", x + 4600, -700, 2000, rot=-1.8, t_in=W(26, "पायलट") - 0.4, label="फ़्रांसिस गैरी पावर्स · 1962", label_t=W(26, "पावर्स"))
    look(W(26, "पायलट") - 0.3, x + 4600, -600, 0.6, -0.4)
    photo("P16", x + 9000, -800, 3400, rot=1.2, t_in=L(27) - 0.3, label="A-12 · OXCART", label_t=W(27, "ऑक्सकार्ट"))
    film.add(Counter(x + 9000, 1800, 900, 3, W(27, "तीन") - 0.6, dur=0.6, prefix="MACH ", suffix="+", caption="आवाज़ से तीन गुना", rgb=TEAL))
    look(L(27) + 0.05, x + 9000, -400, 0.48, 0.2)
    look(W(27, "रफ़्तार") - 0.2, x + 9000, 700, 0.45, 0.2)
    cut("ft_sr71", x + 13800, 28, start=2.0, label="SR-71 · A-12 परिवार (NASA फ़ुटेज)")
    tag("Ti · टाइटेनियम", x + 13800, SY - 800, 220, W(28, "टाइटेनियम") - 0.1, t_out=nxt(28), rgb=TEAL)
    a = card(x + 17400, -900, 3000, 1300, L(29) + 0.1, "सोवियत संघ", ["टाइटेनियम"], ts=320, bs=200, accent=AMBER)
    b = card(x + 21000, 900, 3400, 1300, W(29, "नक़ली") - 0.2, "नक़ली कंपनियाँ", ["बीच के रास्ते"], ts=320, bs=200, accent=TEAL)
    c3 = card(x + 24600, -900, 3000, 1300, W(29, "आया") - 0.1, "CIA · A-12", ["अमेरिका"], ts=320, bs=200, accent=TEAL)
    film.add(StringLine((x + 18600, -600), (x + 19700, 800), t_in=W(29, "नक़ली") + 0.1, dur=0.6, sag=0.05, width=24))
    film.add(StringLine((x + 22300, 800), (x + 23400, -600), t_in=W(29, "आया") + 0.1, dur=0.6, sag=0.05, width=24))
    film.add(Stamp("दुश्मन की धातु", x + 21000, -2200, size=360, rot=-6, t_in=W(29, "दुश्मन") - 0.05, rgb=AMBER))
    tag("बताया जाता है", x + 17400, -2200, 140, L(29) + 0.2, rgb=AMBER)
    look(L(29) + 0.05, x + 21000, -200, 0.42, 0.0)

    # ============================================================ MiGs AND STEALTH (30-36)
    x = X[5]
    photo("P17", x - 2200, -500, 3400, rot=-1.0, t_in=L(30) - 0.3, label="USAF के पास सोवियत MiG-21", label_t=W(30, "अमेरिकी"))
    film.add(Stamp("दुश्मन का विमान", x - 2000, 1400, size=320, rot=-7, t_in=W(30, "नहीं") - 0.1, rgb=AMBER))
    look(L(30) + 0.05, x - 2200, -200, 0.5, -0.2)
    screen("g_mig", x + 3000, L(31) - 0.15, nxt(32) + 0.05, start=0.0)
    into(x + 3000, L(31) - 0.1, nxt(32) - 0.5, 1.0, 1.05)
    tag("HAVE DOUGHNUT · 1968", x + 3000, SY - 800, 220, W(32, "हैव") - 0.1, t_out=nxt(32), rgb=TEAL)
    photo("P18", x + 8000, -600, 3200, rot=1.3, t_in=L(33) - 0.3, label="HAVE BLUE · 1977", label_t=W(33, "हैव"))
    look(L(33) + 0.05, x + 8000, -500, 0.5, 0.2)
    screen("air_D", x + 8000, L(34) - 0.15, nxt(34) + 0.05, start=0.3)
    shot(L(34) - 0.3, x + 8000, 3800, 0.45, 0.0, strength=0.2)
    into(x + 8000, L(34) + 0.05, W(34, "स्टेल्थ") - 0.2, 1.0, 1.04)
    photo("P19", x + 12600, -700, 3000, rot=-1.4, t_in=W(34, "स्टेल्थ") - 0.4, label="F-117 नाइटहॉक", label_t=W(34, "एफ़"))
    look(W(34, "स्टेल्थ") - 0.3, x + 12600, -600, 0.5, -0.2)
    wx = x + 18400
    ufo = card(wx + 2400, 0, 2400, 1200, L(35) - 0.1, "UFO?", ["आसमान की रोशनियाँ"], ts=320, accent=AMBER)
    for k, (nm, yy) in enumerate([("U-2", -1800), ("A-12", 0), ("HAVE BLUE", 1800)]):
        card(wx - 2600, yy, 2600, 1000, L(35) + 0.2 + 0.35 * k, nm, ts=230)
        film.add(StringLine((wx - 1300, yy), (wx + 1200, 0), t_in=W(35, "असल") + 0.15 * k, dur=0.5, sag=0.04, width=22))
    film.add(Stamp("गुप्त विमान", wx + 2400, 1300, size=340, rot=-8, t_in=W(35, "गुप्त") - 0.05, rgb=TEAL))
    look(L(35) + 0.05, wx, 0, 0.36, 0.0)
    film.add(BigText("तो क्या कहानी ख़त्म?", wx + 7400, -1300, 300, L(36) + 0.1, font="label", rgb=CREAM, shadow=False, grunge=False))
    film.add(BigText("नहीं।", wx + 7400, 400, 1100, W(36, "नहीं") - 0.05, rgb=AMBER, z=60))
    look(L(36) + 0.05, wx + 7400, 0, 0.42, 0.0, radius=2600, strength=0.8)
    cue("heartbeat", W(36, "नहीं"), 0.9); cue("boom", W(36, "नहीं") + 0.1, 0.5)

    # ============================================================ LAZAR (37-44)
    x = X[6]
    card(x - 1200, -400, 4400, 2200, L(37) - 0.1, "KLAS-TV · लास वेगास", ["मई 1989 · चेहरा छुपाए एक आदमी", "(पुनर्निर्माण)"], ts=300, bs=150, accent=TEAL)
    film.add(BigText("बॉब लज़ार", x - 1200, 1500, 380, W(37, "बॉब") - 0.1, rgb=AMBER, z=60))
    look(L(37) + 0.05, x - 1200, 300, 0.5, 0.0)
    cut("s4", x + 4800, 38, start=0.0)
    film.add(Counter(x + 9800, -600, 1400, 115, W(39, "एक") - 0.5, dur=0.9, prefix="", caption="'एलिमेंट 115' (दावा)", rgb=TEAL))
    look(L(39) + 0.05, x + 9800, -300, 0.5, 0.0)
    photo("P10", x + 14600, -700, 3200, rot=-1.2, t_in=L(40) - 0.3, label="रेचल, नेवाडा · एलियन टूरिज़्म", label_t=W(40, "हंगामा"))
    tag("एक्स्ट्राटेरेस्ट्रियल हाईवे · 1996", x + 14600, 1700, 170, W(40, "अड्डा") - 0.3, rgb=AMBER)
    look(L(40) + 0.05, x + 14600, -300, 0.5, -0.2)
    cl = card(x + 20000, -300, 3600, 1800, L(41) - 0.1, "लज़ार के दावे", ["S-4 · 9 तश्तरियाँ · एलिमेंट 115"], ts=260, bs=150, accent=TEAL)
    film.add(PenMark("ellipse", x + 20000, -300, 4200, 2400, t_in=W(41, "छेद") - 0.2, dur=0.6, width=40, seed=41, rgb=AMBER))
    look(L(41) + 0.05, x + 20000, -200, 0.5, 0.0)
    for k, nm in enumerate(["MIT", "Caltech"]):
        card(x + 24600 + k * 3200, -400, 2800, 1300, W(42, ["एमआईटी", "कैलटेक"][k]) - 0.2, nm, ["छात्र रिकॉर्ड"], ts=300, accent=TEAL, dark=False)
    film.add(Stamp("रिकॉर्ड नहीं", x + 26200, 900, size=380, rot=-7, t_in=W(42, "रिकॉर्ड") - 0.05, rgb=AMBER))
    look(L(42) + 0.05, x + 26200, 0, 0.45, 0.0)
    card(x + 31000, -800, 3200, 1200, W(43, "समर्थक") - 0.2, "समर्थक", ["'रिकॉर्ड मिटाए गए'"], ts=240, accent=TEAL)
    card(x + 31000, 900, 3200, 1200, W(43, "आलोचक") - 0.2, "आलोचक", ["'कहानी गढ़ी गई'"], ts=240, accent=AMBER)
    look(L(43) + 0.05, x + 31000, 0, 0.45, 0.0)
    film.add(Counter(x + 35400, -700, 1100, 115, L(44) + 0.2, dur=0.6, caption="मॉस्कोवियम · 2003", rgb=CREAM))
    film.add(BigText("< 1 सेकंड", x + 35400, 1300, 420, W(44, "सेकंड") - 0.2, rgb=AMBER, z=60))
    look(L(44) + 0.05, x + 35400, 0, 0.45, 0.0)

    # ============================================================ ROSWELL (45-47)
    x = X[7]
    screen("g_roswell", x, L(45) - 0.15, W(45, "सैंतालीस") + 0.2, start=0.0)
    into(x, L(45) - 0.1, W(45, "सैंतालीस"), 1.0, 1.04)
    photo("P20", x + 4400, -600, 3600, rot=-1.0, t_in=W(45, "सैंतालीस") - 0.2, label="रोसवेल डेली रिकॉर्ड · 8 जुलाई 1947", label_t=W(45, "तश्तरी"))
    look(W(45, "सैंतालीस"), x + 4400, -500, 0.48, -0.2)
    photo("P21", x + 9400, -500, 2400, rot=1.6, t_in=L(46) - 0.3, label="'मौसम का गुब्बारा' · 1947", label_t=W(46, "गुब्बारा"))
    photo("P22", x + 13200, -300, 2200, rot=-1.4, t_in=W(46, "वायुसेना") - 0.3, label="प्रोजेक्ट मोगुल · USAF 1995", label_t=W(46, "मोगुल"))
    look(L(46) + 0.05, x + 9400, -400, 0.52, 0.2)
    look(W(46, "वायुसेना") - 0.2, x + 13200, -200, 0.52, -0.2)
    film.add(BigText("1947", x + 17000, -800, 800, L(47) + 0.1, rgb=CREAM, z=60))
    film.add(BigText("1955", x + 21600, -800, 800, W(47, "जबकि") - 0.1, rgb=TEAL, z=60))
    film.add(PenMark("arrow", x + 19300, -800, 2000, 0, t_in=W(47, "जबकि"), dur=0.5, width=34, seed=47, rgb=AMBER))
    film.add(Stamp("तब बना ही नहीं था", x + 19300, 800, size=330, rot=-6, t_in=W(47, "बना") - 0.1, rgb=AMBER))
    look(L(47) + 0.05, x + 19300, 0, 0.5, 0.0)

    # ============================================================ THE REAL GUARD (48-53)
    x = X[8]
    cut("ter_C", x, 48, start=0.0)
    film.add(BigText("इतना पहरा क्यों?", x, SY - 650, 320, W(48, "पहरा") - 0.1, t_out=nxt(48), rgb=TEAL, z=70))
    photo("P11", x + 4600, -700, 3000, rot=-1.3, t_in=L(49) - 0.3, label="JANET 737 · लास वेगास", label_t=W(49, "सफ़ेद"))
    look(L(49) + 0.05, x + 4600, -600, 0.55, -0.2)
    screen("ter_E", x + 4600, W(49, "कोडनेम") - 0.3, nxt(49) + 0.05, start=1.5)
    shot(W(49, "कोडनेम") - 0.4, x + 4600, 3800, 0.45, 0.0, strength=0.2)
    into(x + 4600, W(49, "कोडनेम"), nxt(49) - 0.5, 1.0, 1.04)
    photo("P05", x + 9600, -600, 3000, rot=1.2, t_in=L(50) - 0.3, label="सीमा का बोर्ड और नारंगी खंभे", label_t=W(50, "नारंगी"))
    film.add(PenMark("ellipse", x + 10400, -300, 900, 1400, t_in=W(50, "खंभे") - 0.1, dur=0.5, width=34, seed=50, rgb=AMBER))
    photo("P08", x + 13800, 1200, 2200, rot=-1.6, t_in=W(50, "सेंसर") - 0.4, label="ग्रूम लेक रोड पर कैमरा", label_t=W(50, "सेंसर"))
    look(L(50) + 0.05, x + 9600, -400, 0.52, 0.2)
    look(W(50, "सेंसर") - 0.3, x + 12000, 500, 0.42, 0.0)
    card(x + 18000, -400, 3800, 1600, L(51) - 0.1, "कैमो ड्यूड्स", ["सफ़ेद पिकअप · बिना वर्दी", "पहाड़ियों पर पहरा"], ts=300, bs=150, accent=AMBER)
    look(L(51) + 0.05, x + 18000, -300, 0.52, 0.0)
    cut("ter_D", x + 23000, 52, start=0.4, until=W(52, "बंद") - 0.7)
    photo("P09", x + 28200, -500, 3400, rot=1.0, t_in=W(52, "बंद") - 0.6, label="टिकाबू पीक से, लगभग 40 किमी दूर", label_t=W(52, "बंद"))
    look(W(52, "बंद") - 0.5, x + 28200, -400, 0.5, 0.2)
    cut("ter_G", x + 33200, 53, start=0.0)
    cue("riser", W(53, "राज़"), 0.5, dur=1.6); cue("heartbeat", W(53, "बीमार"), 0.8)

    # ============================================================ THE SMOKE (54-59)
    x = X[9]
    pd = film.add(PaperDoc(x, 200, 3200, 4000, rot=-1.2, t_in=L(54) - 0.2, rows=13, sentence_row=6, sentence_size=120,
                           header=(("UNITED STATES DISTRICT COURT", 120, "serif"), ("DISTRICT OF NEVADA · 1994", 96, "mono"),
                                   ("FROST v. PERRY", 150, "cond")),
                           sentence="Former workers allege open-pit burning of hazardous waste."))
    tag("मुक़दमा · 1994 (पुनर्निर्माण)", x, -2000, 150, L(54) + 0.3, rgb=TEAL)
    look(L(54) + 0.05, x, 0, 0.45, -0.2)
    cut("ter_G", x + 5200, 55, start=1.0)
    card(x + 10200, -300, 3400, 1500, W(56, "कर्मचारी") - 0.3, "रॉबर्ट फ़्रॉस्ट", ["पूर्व कर्मचारी", "उनके परिवार के मुताबिक़"], ts=280, bs=140, accent=(150, 160, 175))
    look(L(56) + 0.05, x + 10200, -300, 0.55, 0.0)
    film.add(BigText("राष्ट्रीय सुरक्षा", x + 15400, -400, 520, W(57, "राष्ट्रीय") - 0.2, rgb=CREAM, z=60))
    film.add(PaperDoc(x + 15400, 1400, 3000, 1800, rot=0.8, t_in=L(57) + 0.1, rows=5, sentence_row=2, sentence_size=110,
                      header=(("RESPONSE OF THE UNITED STATES", 100, "serif"),), sentence="██████ ███ ████████ ██████████ ████"))
    film.add(Stamp("CLASSIFIED", x + 15400, 1600, size=300, rot=-6, t_in=W(57, "मामला") - 0.1, rgb=TEAL))
    look(L(57) + 0.05, x + 15400, 500, 0.42, 0.0)
    photo("P23", x + 20200, -700, 2200, rot=-1.4, t_in=L(58) - 0.3, label="राष्ट्रपति बिल क्लिंटन", label_t=W(58, "क्लिंटन"))
    film.add(Stamp("छूट · 1995", x + 23400, 300, size=380, rot=-7, t_in=W(58, "छूट") - 0.05, rgb=AMBER))
    look(L(58) + 0.05, x + 21400, -200, 0.45, -0.1)
    film.add(Stamp("STATE SECRETS", x + 28400, -500, size=420, rot=-6, t_in=W(59, "स्टेट") - 0.05, rgb=RED))
    film.add(BigText("केस ख़ारिज", x + 28400, 900, 420, W(59, "ख़ारिज") - 0.1, rgb=CREAM, z=60))
    film.add(BigText("धुआँ किस चीज़ का था?", x + 28400, 2000, 240, W(59, "धुआँ") - 0.1, font="label", rgb=TEAL, shadow=False, grunge=False))
    look(L(59) + 0.05, x + 28400, 300, 0.42, 0.0)

    # ============================================================ THE ADMISSION (60-65)
    x = X[10]
    doc_ = film.add(PaperDoc(x, 200, 3200, 4000, rot=1.3, t_in=L(60) - 0.2, rows=12, sentence_row=5, sentence_size=120,
                             header=(("CENTRAL INTELLIGENCE AGENCY", 120, "serif"), ("THE U-2 AND OXCART PROGRAMS, 1954-1974", 84, "mono"),
                                     ("RELEASED AUGUST 2013", 130, "cond")),
                             sentence="...a remote site near Groom Lake, Nevada, known as Area 51."))
    bar("अगस्त 2013", x, -2400, 230, L(60) + 0.2)
    look(L(60) + 0.05, x, 0, 0.45, 0.2)
    photo("P02", x + 5600, -400, 3000, rot=-1.2, t_in=L(61) - 0.3, label="ग्रूम लेक · उपग्रह चित्र (NASA)", label_t=W(61, "एरिया"))
    film.add(PenMark("ellipse", x + 5600, -600, 1400, 900, t_in=W(61, "एरिया") - 0.1, dur=0.5, width=34, seed=61, rgb=TEAL))
    film.add(Counter(x + 9800, 300, 1000, 58, W(61, "अट्ठावन") - 0.6, dur=0.9, suffix=" साल", caption="1955 → 2013", rgb=AMBER))
    look(L(61) + 0.05, x + 5600, -400, 0.5, -0.2)
    look(W(61, "अट्ठावन") - 0.3, x + 8000, 0, 0.42, 0.0)
    card(x + 14200, -200, 3800, 1700, L(62) - 0.1, "खोज: 'alien'", ["नतीजा: 0"], ts=300, bs=260, accent=TEAL)
    look(L(62) + 0.05, x + 14200, -200, 0.55, 0.0)
    photo("P24", x + 19600, -500, 3400, rot=1.0, t_in=L(63) - 0.3, label="डेविड ग्रश · संसद, 26 जुलाई 2023", label_t=W(63, "डेविड"))
    tag("दावा", x + 21000, 1400, 220, W(63, "दावा") - 0.1, rgb=AMBER)
    look(L(63) + 0.05, x + 19600, -300, 0.5, 0.2)
    screen("hf_aaro", x + 24600, L(64) - 0.1, nxt(64) + 0.05, start=max(0.0, 0.9 - (W(64, "एलियन") - L(64))))
    shot(L(64) - 0.3, x + 24600, 3800, 0.45, 0.0, strength=0.2)
    into(x + 24600, L(64) + 0.05, nxt(64) - 0.5, 1.0, 1.04)
    card(x + 29000, -300, 2600, 1500, W(65, "दावे") - 0.2, "दावे", ["लज़ार · ग्रश"], ts=300, accent=AMBER)
    card(x + 35000, -300, 2600, 1500, W(65, "इनकार") - 0.2, "इनकार", ["CIA · पेंटागन"], ts=300, accent=TEAL)
    photo("P05", x + 32000, 0, 2400, rot=0.6, t_in=L(65) - 0.2, label="वही बंद दरवाज़ा", label_t=W(65, "दरवाज़ा"))
    look(L(65) + 0.05, x + 32000, 0, 0.38, 0.0)

    # ============================================================ VERDICT (66-69)
    x = X[11]
    cut("ter_B", x, 66, start=0.0)
    tag("गुप्त विमानों की प्रयोगशाला", x, SY - 800, 200, W(66, "प्रयोगशाला") - 0.2, t_out=nxt(66), rgb=TEAL)
    cut("air_E", x + 3900, 67, start=0.0)
    screen("g_verdict", x + 7800, L(68) - 0.15, nxt(68) + 0.05)
    into(x + 7800, L(68) - 0.05, nxt(68) - 0.5, 1.0, 1.04)
    film.add(BigText("सबसे अच्छा परदा?", x + 7800, SY - 650, 320, W(68, "परदा") - 0.2, t_out=nxt(68), rgb=AMBER, z=70))
    screen("hf_qend", x + 11700, L(69) - 0.1, doc.duration + 1, start=0.0)
    into(x + 11700, L(69) + 0.05, doc.duration, 1.0, 1.05)
    cue("heartbeat", W(69, "इंसानों"), 0.7); cue("heartbeat", W(69, "और"), 0.8); cue("boom", W(69, "आप") - 0.1, 0.5)

    # ------------------------------------------------ moods: background and finish follow the scene and emotion
    def mood(i, name, d=0.0, fade=1.2):
        if has(i):
            film.mood(L(i) + d, name, fade)
    film.mood(0.0, "radar", 0.1)
    for args in [(7, "intel", -0.3), (8, "evidence", -0.2), (12, "radar", 0.0, 0.6), (13, "archive", 0.0),
                 (15, "archive", -0.2), (16, "desert", -0.3), (18, "intel", -0.3), (19, "desert", -0.3),
                 (20, "archive", -0.3), (21, "intel", -0.2), (22, "radar", -0.2), (23, "evidence", -0.2),
                 (25, "radar", 0.0, 0.6), (26, "intel", -0.3), (27, "archive", -0.2), (29, "intel", -0.2),
                 (30, "archive", -0.2), (31, "intel", -0.2), (33, "archive", -0.2), (35, "evidence", -0.2),
                 (36, "radar", 0.0, 0.5), (37, "evidence", -0.2), (38, "radar", -0.2), (40, "evidence", -0.2),
                 (44, "intel", -0.2), (45, "archive", -0.3), (47, "evidence", -0.2), (48, "desert", -0.3),
                 (50, "evidence", -0.2), (52, "desert", -0.2), (53, "grief", -0.2), (57, "evidence", -0.2),
                 (59, "grief", -0.2), (60, "evidence", -0.3), (61, "intel", -0.2), (63, "evidence", -0.2),
                 (66, "desert", -0.3), (68, "verdict", -0.3), (69, "radar", -0.2)]:
        mood(*args)

    tidy_keys(film.cam_keys)
    tidy_keys(film.focus_keys)

    # ------------------------------------------------ word chips: an explaining label on a key word, in a corner
    SLOT = {"tl": (-0.25, -0.31), "tr": (0.25, -0.31), "ml": (-0.32, 0.04), "mr": (0.32, 0.04)}

    def chip(i, word, text, slot, hot=False):
        if not has(i):
            return
        t = W(i, word) - 0.1
        x_, y_, z, _ = film.camera(t + 0.5)
        fx, fy = SLOT[slot]
        film.add(BigText(text, x_ + fx * 3840 / z, y_ + fy * 2160 / z, 150 / z, t, t_out=min(E(i) + 0.5, nxt(i) + 0.2),
                         font="label", rgb=DARK, bar=AMBER if hot else HILITE, bar_h=0.92,
                         shadow=False, grunge=False, z=78, sfx=False))

    for args in [
        (7, "नेवाडा", "लास वेगास से लगभग 130 किमी उत्तर", "tl"),
                (14, "शीत", "अमेरिका बनाम सोवियत संघ", "tl"),
        (15, "जासूसी", "70,000 फ़ीट तक उड़ने वाला", "tl"),
        (16, "सीआईए", "12 अप्रैल 1955", "tl"),
                (18, "नक़्शे", "AEC के नक़्शे का खाना", "tl"),
        (20, "पहली", "पहली उड़ान: 4 अगस्त 1955", "tl"),
        (22, "चमकती", "शाम की धूप चाँदी जैसे पंखों पर", "tl"),
        (24, "अध्ययन", "CIA इतिहासकार, 1997", "tl"),
        (26, "मई", "सोवियत संघ के ऊपर", "tl", True),
        (27, "मिसाइल", "90,000 फ़ीट · Mach 3+", "tl"),
        (31, "इराक़ी", "पायलट मुनीर रेदफ़ा", "tl"),
        (33, "नुकीला", "रडार से बचने वाले कोण", "tl"),
        (37, "टीवी", "KLAS-TV · जॉर्ज नैप", "tr"),
        (38, "दावा", "सिर्फ़ दावा, सबूत नहीं", "tr", True),
        (40, "हंगामा", "एलियन पर्यटन शुरू", "tl"),
        (45, "रोसवेल", "न्यू मेक्सिको · 1947", "tl"),
        (46, "मोगुल", "सोवियत परमाणु परीक्षण सुनने के लिए", "tl"),
        (49, "विमान", "बिना नाम के बोइंग 737", "tl"),
        (52, "चौरासी", "1984 · 1995", "tl"),
        (54, "विधवाएँ", "वकील: जोनाथन टर्ली", "tl"),
        (56, "मुताबिक़", "बीमारी की वजह कभी तय नहीं हुई", "tl"),
        (58, "छूट", "हर साल आगे बढ़ी", "tl", True),
        (59, "स्टेट", "सुप्रीम कोर्ट: 1998", "tl"),
        (60, "इतिहास", "नेशनल सिक्योरिटी आर्काइव", "tl"),
        (63, "दावा", "शपथ लेकर दावा", "tl"),
        (64, "रिपोर्ट", "AARO · मार्च 2024", "tl"),
        (67, "दशकों", "U-2 · A-12 · F-117", "tl"),
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
