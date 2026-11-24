"""पिछवाड़े के साँप: the 62-second vertical reel (1080x1920).

The same recorded lines as the film, re-cut: opens on the question, ends on the question, with a hook
headline over every beat. Each beat sits at its own spot on the wall; the 16:9 clip or exhibit fills the
frame's width in the middle, the headline sits above it and the burned-in captions below.
Render: render.py --project saanp/reel --size 1080x1920
"""
from engine import Card, HILITE, BigText, Clip, Counter, Film, PaperDoc, PenMark, Print

CREAM = (244, 240, 232)
DARK = (26, 22, 20)
RED = (200, 40, 30)


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
    order = [s["id"] for s in doc.timing["segments"]]
    X = {i: k * 7000 for k, i in enumerate(order)}

    def clip(cid, i, t0, t1, start=0.0):
        film.add(Clip(doc.clip(cid), X[i], 0, 3840, t_in=t0, t_out=t1, start=start, frame=False, z=40))

    def head(text, i, t0, t1, red=False, size=430):
        film.add(BigText(text, X[i], -2350, size, t0, t_out=t1, rgb=DARK if not red else CREAM,
                         bar=HILITE if not red else RED, bar_h=0.92, shadow=False, hit=None, z=80))

    def hold(i, t0, t1, z0=1.0, z1=1.04):
        film.shot(t0, X[i], -250, z0, 0.0, radius=20000, strength=0.0)
        film.shot(t1, X[i], -250, z1, 0.0, radius=20000, strength=0.0)

    # 5: the question first
    clip("hf_qopen", 5, 0.0, E(5) + 0.4)
    head("एक सवाल", 5, 0.0, E(5) + 0.3, red=True)
    hold(5, 0.0, E(5) + 0.1)
    film.cue("heartbeat", W(5, "इत्तेफ़ाक़"), 0.8)
    # 1, 3, 4: Abbottabad
    clip("g_abbottabad", 1, L(1) - 0.3, E(1) + 0.4)
    head("2 मई 2011 · एबटाबाद", 1, L(1) - 0.2, E(4) + 0.3, size=380)
    hold(1, L(1) - 0.2, E(1) + 0.1)
    photo("P02", X[3], -200, 3500, rot=-1.0, t_in=L(3) - 0.3, label="ओसामा बिन लादेन का ठिकाना", label_t=W(3, "ओसामा"))
    head("2 मई 2011 · एबटाबाद", 3, L(3) - 0.3, E(3) + 0.3, size=380)
    hold(3, L(3) - 0.15, E(3) + 0.1)
    clip("compound", 4, L(4) - 0.3, E(4) + 0.4, start=3.4)
    head("फ़ौजी अकादमी से ≈ 1 किमी", 4, L(4) - 0.2, E(4) + 0.3, size=380)
    hold(4, L(4) - 0.15, E(4) + 0.1)
    # 19, 20: Mumbai
    clip("g_mumbai", 19, L(19) - 0.3, E(19) + 0.4)
    head("मुंबई · 26/11", 19, L(19) - 0.2, E(20) + 0.3)
    hold(19, L(19) - 0.15, E(19) + 0.1)
    if "P04" in doc.meta:
        photo("P04", X[20], -750, 3300, rot=1.2, t_in=L(20) - 0.3, label="ताज होटल · दिसंबर 2008", label_t=L(20) + 0.3)
    film.add(Counter(X[20], 2550, 1000, 166, W(20, "छियासठ") - 0.6, dur=0.9, caption="लोग मारे गए"))
    head("मुंबई · 26/11", 20, L(20) - 0.3, E(20) + 0.3)
    hold(20, L(20) - 0.15, E(20) + 0.1)
    # 41: Pakistan's own investigator
    dawn = film.add(PaperDoc(X[41], 0, 3500, 4300, rot=-1.0, t_in=L(41) - 0.4, rows=14, sentence_row=6, sentence_size=135,
                             header=(("DAWN", 280, "serif"), ("3 AUGUST 2015", 110, "mono"), ("TARIQ KHOSA, FORMER FIA CHIEF", 100, "cond")),
                             sentence="Pakistan has to deal with the Mumbai mayhem, planned and launched from its soil."))
    for k, ((hx, hy), hw) in enumerate(dawn.phrase_spans(res, "planned and launched from its soil.")):
        film.add(PenMark("highlight", hx, hy - 45, hw + 60, 0, t_in=W(41, "प्लान") - 0.3 + 0.3 * k, dur=0.4, width=165, rot=-1.0, seed=21 + k))
    head("पाकिस्तान के अंदर से गवाही", 41, L(41) - 0.3, E(41) + 0.3, red=True, size=360)
    film.shot(L(41) - 0.15, X[41], -300, 0.78, 0.0, radius=20000, strength=0.0)
    film.shot(E(41) + 0.1, X[41], 0, 0.84, 0.0, radius=20000, strength=0.0)
    # 32: the warning
    clip("hf_clinton", 32, L(32) - 0.3, E(32) + 0.4)
    head("अमेरिका की चेतावनी · 2011", 32, L(32) - 0.2, E(32) + 0.3, size=380)
    hold(32, L(32) - 0.15, E(32) + 0.1)
    # 35, 36: the snakes turn
    film.add(Counter(X[35], -200, 1700, 132, W(35, "बत्तीस") - 1.0, dur=1.5, caption="बच्चे · पेशावर 2014"))
    for k in range(5):
        film.add(PenMark("highlight", X[35] - 1600 + k * 800, 1500, 110, 0, t_in=L(35) + 0.6 + 0.15 * k, dur=0.3, width=110, rgb=(255, 190, 90), seed=k))
    head("फिर साँप पलटे", 35, L(35) - 0.3, E(36) + 0.3, red=True)
    hold(35, L(35) - 0.15, E(35) + 0.1)
    clip("hf_title", 36, L(36) - 0.3, E(36) + 0.4, start=0.3)
    head("फिर साँप पलटे", 36, L(36) - 0.3, E(36) + 0.3, red=True)
    hold(36, L(36) - 0.15, E(36) + 0.1)
    # 57, 58: the minister
    clip("hf_asif", 57, L(57) - 0.3, E(58) + 0.4)
    head("रक्षा मंत्री ने क्या कहा?", 57, L(57) - 0.2, E(58) + 0.3, size=400)
    hold(57, L(57) - 0.15, E(58) + 0.1)
    # 66: end on the question
    clip("hf_qend", 66, L(66) - 0.3, doc.duration + 1)
    head("आप क्या सोचते हैं?", 66, L(66) - 0.2, doc.duration + 1, red=True)
    hold(66, L(66) - 0.15, doc.duration)
    film.cue("boom", L(66), 0.5)

    film.fade_in, film.fade_out = 0.2, 1.0
    return film
