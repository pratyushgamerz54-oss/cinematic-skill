#!/usr/bin/env python3
"""Writes mod/script.json, mod/reel/script.json and both voiceover scripts from the lists below.

  python3 mod/tools/gen_script.py

Each line: (spoken, hero, typed, mood, v3 tag, hook). The display text is the spoken text with the
dramatic pauses ("...") turned into commas.
"""
import json
import pathlib
import re

P = pathlib.Path(__file__).resolve().parent.parent

S, M, I, W, O, T = ("[low, suspenseful]", "[storytelling, measured]", "[intrigued, mysterious]",
                    "[warm, inviting]", "[ominous, slow]", "[tense, urgent]")
V = "[reflective, slow]"

FILM = [
    ("T00_intro", "स्वागत (YouTube इंट्रो)", [
        ("नमस्कार दोस्तों... आपका स्वागत है।",
         "HyperFrames intro part 1 (hf_welcome): a slow brass clock dial turns in dark gold dust; 'नमस्कार' · 'स्वागत है'",
         "नमस्कार · स्वागत है", "archive", W, None),
        ("क्या एक ग़लत मोड़, विश्व युद्ध शुरू कर सकता है? क्या एक गंदी प्लेट... करोड़ों जानें बचा सकती है?",
         "hf_topic: teaser chips land on the words, each with an icon: 'ग़लत मोड़?' (a car arrow bending) · 'गंदी प्लेट?' (a petri dish)",
         "ग़लत मोड़? · गंदी प्लेट?", "archive", I, "question"),
        ("और क्या, एक आदमी की एक 'ना'... दुनिया को, परमाणु युद्ध से बचा सकती है?",
         "hf_topic continued: a third chip 'एक ना?' with a launch key that is never turned; heartbeat",
         "एक 'ना'?", "archive", I, "question"),
        ("आज कहानी है, उन पाँच पलों की, जिन्होंने दुनिया बदल दी... और हर पल के पीछे है, एक छोटी सी चूक।",
         "hf_topic finale: five dates light up on the dial (1914 · 1928 · 1962 · 1983 · 1989), the title 'पाँच पल' stamps in (the film's one title card)",
         "title पाँच पल", "archive", S, None),
        ("तो चलिए... शुरू करते हैं।",
         "HyperFrames intro part 3 (hf_go): the dial spins and lands on 26.09.1983, a radar scan line wipes into the cold open",
         "▶", "radar", W, None),
    ]),
    ("T01_cold_open", "आधी रात का अलार्म", [
        ("छब्बीस सितंबर, उन्नीस सौ तिरासी... मॉस्को के पास, एक गुप्त बंकर। आधी रात।",
         "3D globe (look dark, borders false, radar palette): night descent to Moscow, label 'सेरपुख़ोव-15 (गुप्त बंकर)'; date bar",
         "26.09.1983 · आधी रात", "radar", S, "open"),
        ("अचानक, स्क्रीन पर चमकता है... स्टार्ट। यानी, अमेरिका ने, परमाणु मिसाइल दाग दी है।",
         "3D bunker console (प्रतीकात्मक 3D मॉडल): dark room, world wall map; the word СТАРТ flashes red; a dotted arc rises from the US toward the USSR; siren cue",
         "СТАРТ", "tension", T, None),
        ("ड्यूटी पर बैठे अफ़सर के पास, फ़ैसले के लिए थे... बस कुछ मिनट।",
         "engine motion graphic: a countdown clock ticks on the console; heartbeat",
         "कुछ मिनट", "tension", S, None),
        ("उसने क्या किया, ये आगे बताएँगे... पर दुनिया, पहले भी, ऐसे मोड़ पर आ चुकी थी।",
         "the dial spins back 1983 → 1914, the archive mood fades in; riser",
         "1983 → 1914", "archive", I, "hook"),
    ]),
    ("T02_sarajevo", "एक ग़लत मोड़", [
        ("अट्ठाईस जून, उन्नीस सौ चौदह, साराजेवो। खुली कार में, ऑस्ट्रिया के राजकुमार, फ़्रांज़ फ़र्डिनेंड।",
         "real archive film: Franz Ferdinand and Sophie in Sarajevo, 28 June 1914 (Commons, public domain), graded sepia; date bar; name bar",
         "28.06.1914 · साराजेवो", "archive", M, None),
        ("सुबह, उनकी कार पर बम फेंका गया... पर वो बच गए। साज़िश, नाकाम लगी।",
         "3D map of 1914 Sarajevo (tilted relief, river Miljacka, Appel Quay): the motorcade moves along the quay; a bomb marker bounces off the car and bursts behind it; stamp 'नाकाम'",
         "पहला हमला: नाकाम", "tension", T, None),
        ("फिर रास्ता बदला गया... पर ड्राइवर को, किसी ने बताया ही नहीं।",
         "3D map: the new route draws along the quay in green, the old turn into Franz Josef Street in amber; tag 'ड्राइवर को ख़बर नहीं'",
         "नया रास्ता", "evidence", I, None),
        ("कार ग़लत गली में मुड़ी, और रुक गई... ठीक उन्नीस साल के, गैवरिलो प्रिंसिप के सामने।",
         "3D map: the car turns into Franz Josef Street and stops at the Latin Bridge corner; XMarker 'लैटिन ब्रिज'; archive photo of Princip (Commons) in a cartouche",
         "गैवरिलो प्रिंसिप · 19", "tension", S, None),
        ("दो गोलियाँ... राजकुमार और उनकी पत्नी सोफ़ी, दोनों की मौत।",
         "two shot marks stamp on the board (no bodies); archive photo of the car in the Heeresgeschichtliches Museum, Vienna (Commons)",
         "28.06.1914", "grief", O, None),
        ("ठीक एक महीने बाद, पहला विश्व युद्ध शुरू हुआ... जिसमें, लगभग दो करोड़ लोग मारे गए।",
         "2.5D Europe map (look intel, borderless): war fronts draw on; dot-grid Counter to ≈ 2 करोड़ (estimates vary)",
         "≈ 2 करोड़ मौतें", "grief", O, None),
        ("एक ग़लत मोड़... और दुनिया बदल गई। लेकिन अगला मोड़, छुपा था... एक प्लेट में।",
         "the board slides; a glass petri dish rises out of the dark (3D, symbolic); heartbeat",
         "अगला मोड़?", "archive", I, "hook"),
    ]),
    ("T03_penicillin", "एक गंदी प्लेट", [
        ("सितंबर, उन्नीस सौ अट्ठाईस। लंदन। वैज्ञानिक अलेक्ज़ेंडर फ़्लेमिंग, छुट्टियों से लौटे।",
         "3D globe: flight Sarajevo → London; archive photo of Alexander Fleming in his laboratory (Commons, public domain); date bar; name bar",
         "1928 · अलेक्ज़ेंडर फ़्लेमिंग", "archive", M, None),
        ("लैब में, बैक्टीरिया की एक प्लेट, खुली छूट गई थी... और उस पर, फफूँद उग आई थी।",
         "3D petri dish (प्रतीकात्मक 3D मॉडल): yellow bacteria colonies; a blue-green mould spot grows on the plate",
         "खुली प्लेट", "evidence", M, None),
        ("और फफूँद के चारों तरफ़... बैक्टीरिया, ग़ायब। फ़्लेमिंग ने इसे नाम दिया, पेनिसिलिन।",
         "same 3D dish: a clear ring opens around the mould; then the real culture plate photo (Commons) with a pen circle; Card 'PENICILLIN'",
         "बैक्टीरिया ग़ायब", "evidence", I, None),
        ("उस ज़माने में, एक खरोंच भी, जान ले सकती थी। अनुमान है, इस दवा ने... करोड़ों जानें बचाईं।",
         "real archive footage/photos: 1940s penicillin production (US government, public domain); Counter 'करोड़ों जानें (अनुमान)'",
         "करोड़ों जानें (अनुमान)", "verdict", M, None),
        ("पर अब, दुनिया के सामने था, एक नया ख़तरा... परमाणु बम।",
         "the board darkens; a slow 3D globe turn to the Caribbean; riser",
         "नया ख़तरा", "tension", O, "hook"),
    ]),
    ("T04_arkhipov", "तीसरी चाबी", [
        ("अक्टूबर, उन्नीस सौ बासठ। क्यूबा में, सोवियत परमाणु मिसाइलें... और अमेरिका ने, क्यूबा को समुद्र में घेर लिया।",
         "real archive: US reconnaissance photo of a Cuban missile site, October 1962 (public domain); then the 3D tilted Caribbean map (NASA Blue Marble relief): the quarantine line draws around Cuba, ship icons",
         "अक्टूबर 1962 · क्यूबा", "intel", M, None),
        ("सत्ताईस अक्टूबर। पानी के नीचे, सोवियत पनडुब्बी, बी-उनसठ। मॉस्को से, कोई संपर्क नहीं।",
         "3D underwater scene (प्रतीकात्मक 3D मॉडल): the Foxtrot-class submarine B-59 glides in dark blue water; tag 'मॉस्को से संपर्क नहीं'",
         "B-59 · 27.10.1962", "tension", S, None),
        ("ऊपर से, अमेरिकी जहाज़, सिग्नल वाले छोटे बम गिरा रहे थे। अंदर लगा... जंग शुरू हो गई है।",
         "same 3D scene: destroyer hulls overhead, small practice depth charges sink and flash; the hull shakes",
         "सिग्नल बम", "tension", T, None),
        ("और पनडुब्बी में था, परमाणु टॉरपीडो। गवाहों के मुताबिक़, कप्तान ने उसे तैयार करवाया।",
         "3D cutaway: the hull turns translucent, the torpedo bay lights up amber, label 'परमाणु टॉरपीडो'; testimony card 'वादिम ओर्लोव, B-59 (बाद का बयान)'",
         "परमाणु टॉरपीडो", "tension", O, None),
        ("पर दाग़ने के लिए, तीन अफ़सरों की हाँ चाहिए थी। दो ने कहा, हाँ... तीसरे ने कहा, ना।",
         "engine motion graphic: three lamps for three officers; two turn green 'हाँ', the third stays dark and stamps 'ना'",
         "हाँ · हाँ · ना", "tension", S, None),
        ("वो थे, वसीली आर्खिपोव। पनडुब्बी सतह पर आई, और लौट गई।",
         "real archive photo: B-59 surfaced beside a US destroyer, October 1962 (US Navy, public domain); photo of Arkhipov (Commons) in a cartouche",
         "वसीली आर्खिपोव", "verdict", M, None),
        ("लेकिन इक्कीस साल बाद, फ़ैसला फिर... एक अकेले आदमी के हाथ में था।",
         "the dial spins 1962 → 1983, back to the bunker console; heartbeat",
         "1962 → 1983", "radar", I, "hook"),
    ]),
    ("T05_petrov", "सूरज की चमक", [
        ("वापस उसी बंकर में। एक मिसाइल, फिर दूसरी... कुल पाँच। ड्यूटी पर थे, स्तानिस्लाव पेत्रोव।",
         "3D bunker console: five missile tracks appear one by one, counter 1 → 5; photo of Stanislav Petrov (Commons, free licence) in a cartouche; name bar",
         "मिसाइल: 5 · पेत्रोव", "radar", T, None),
        ("पेत्रोव ने सोचा, हमला सिर्फ़ पाँच मिसाइलों से क्यों? असली हमला... सैकड़ों से होता।",
         "engine motion graphic: 5 dots beside a field of hundreds; a question mark lands on '5?'",
         "5 या सैकड़ों?", "evidence", I, None),
        ("उन्होंने ऊपर ख़बर दी, ये सिस्टम की ग़लती है... और कोई मिसाइल नहीं आई।",
         "3D console: the phone; stamp 'झूठा अलार्म'; a clock runs on and nothing arrives",
         "झूठा अलार्म", "tension", S, None),
        ("सैटेलाइट ने, बादलों पर पड़ी धूप को, मिसाइल समझ लिया था। पर आख़िरी मोड़... सबसे अजीब था।",
         "3D globe: the Oko satellite in its high orbit, sunlight glints off clouds over the US, label 'बादलों पर धूप'; then a folded paper note slides in; riser",
         "बादलों पर धूप", "verdict", I, "hook"),
    ]),
    ("T06_berlin", "एक पर्ची", [
        ("नौ नवंबर, उन्नीस सौ नवासी। अट्ठाईस साल से, एक दीवार, बर्लिन को बाँटे खड़ी थी।",
         "3D map of Berlin (tilted, satellite colours): the wall line glows across the city; date bar; archive photo of the wall (Commons)",
         "09.11.1989 · बर्लिन", "intel", M, None),
        ("प्रेस कॉन्फ़्रेंस में, नेता गुंटर शाबोव्स्की को, नए यात्रा नियमों की, एक पर्ची थमाई गई।",
         "archive photo: Schabowski at the press conference, 9 Nov 1989 (Bundesarchiv, CC BY-SA); name bar; the note slides in",
         "गुंटर शाबोव्स्की", "evidence", M, None),
        ("पूछा गया, कब से लागू? उन्होंने काग़ज़ पलटे... और कहा, तुरंत। जबकि नियम, अगले दिन से थे।",
         "HyperFrames quote card: 'sofort, unverzüglich' with the Hindi below (transcript, Wilson Center); then a pen strike and tag 'असल योजना: अगला दिन'",
         "SOFORT · UNVERZÜGLICH", "evidence", S, None),
        ("हज़ारों लोग, दीवार की तरफ़ दौड़ पड़े। उसी रात, फाटक खुल गए... और एक साल में, जर्मनी एक हो गया।",
         "real archive footage: crowds at the Berlin Wall, November 1989 (Commons, free licence); 3D map pin 'बोर्नहोल्मर स्ट्रासे'; Timeline 1989 → 1990",
         "1990 · जर्मनी एक", "verdict", T, None),
    ]),
    ("T07_verdict", "आपका सवाल", [
        ("एक मोड़, एक प्लेट, एक 'ना', एक भरोसा, एक पर्ची... कभी कभी, एक छोटा सा पल, इतिहास पलट देता है।",
         "five evidence cards line up on the board, one per word, each with its photo and year; a slow 3D globe at night links the five places",
         "1914 · 1928 · 1962 · 1983 · 1989", "verdict", V, None),
        ("तो क्या आज भी, कहीं कोई ऐसा पल... चुपचाप, हमारा इंतज़ार कर रहा है? आप क्या सोचते हैं?",
         "HyperFrames closing question (qend), word by word, ends on the viewer question; heartbeat",
         "qend", "tension", I, "question"),
    ]),
]

REEL = [
    ("क्या एक छोटी सी ग़लती, दुनिया बदल सकती है? इतिहास कहता है... हाँ, पाँच बार।",
     "HyperFrames reel question (rq)", "एक ग़लती, दुनिया बदली?", "सवाल", "—", "archive", "red", I),
    ("उन्नीस सौ चौदह। राजकुमार की कार, ग़लत गली में मुड़ी... और हत्यारे के सामने रुकी। शुरू हुआ, विश्व युद्ध।",
     "1914 Sarajevo archive film; then the 3D map turn at the Latin Bridge", "1914: एक ग़लत मोड़", "प्रमाण 01", "फ़िल्म: Wikimedia Commons (public domain)", "archive", "yellow", M),
    ("उन्नीस सौ अट्ठाईस। फ़्लेमिंग की लैब में, एक प्लेट खुली छूटी... और उस पर उगी फफूँद से, मिली पेनिसिलिन।",
     "Fleming photo; 3D petri dish with the clear ring", "1928: एक खुली प्लेट", "प्रमाण 02", "फ़ोटो: Wikimedia Commons", "evidence", "yellow", M),
    ("उन्नीस सौ बासठ। क्यूबा के पास, एक सोवियत पनडुब्बी में, परमाणु टॉरपीडो तैयार था।",
     "3D submarine B-59 under depth charges", "1962: पानी के नीचे", "प्रतीकात्मक 3D मॉडल", "स्रोत: National Security Archive", "tension", "yellow", S),
    ("तीन हाँ चाहिए थीं। वसीली आर्खिपोव ने कहा... ना।",
     "three lamps: हाँ · हाँ · ना; B-59 surfaced photo (US Navy)", "तीसरे ने कहा: ना", "प्रमाण 03", "फ़ोटो: US Navy (public domain)", "verdict", "yellow", S),
    ("उन्नीस सौ तिरासी। सोवियत स्क्रीन पर, पाँच मिसाइलें। पर स्तानिस्लाव पेत्रोव ने कहा... झूठा अलार्म।",
     "3D bunker console with five tracks; Petrov photo", "1983: पाँच मिसाइलें", "प्रमाण 04", "फ़ोटो: Wikimedia Commons", "radar", "yellow", T),
    ("वो सही थे। सैटेलाइट ने, बादलों पर पड़ी धूप को, मिसाइल समझा था।",
     "3D globe: satellite and sunlight on clouds", "मिसाइल नहीं, धूप", "प्रतीकात्मक 3D मॉडल", "स्रोत: Britannica, RFE/RL", "radar", "yellow", M),
    ("उन्नीस सौ नवासी। एक नेता ने, पर्ची ग़लत पढ़ी, और कहा, सरहद... तुरंत खुलेगी।",
     "Schabowski press conference photo; the note", "1989: एक पर्ची", "प्रमाण 05", "फ़ोटो: Bundesarchiv (CC BY-SA)", "evidence", "yellow", S),
    ("उसी रात, बर्लिन की दीवार खुल गई।",
     "1989 Berlin Wall footage", "उसी रात: दीवार खुली", "प्रमाण 06", "फ़ुटेज: Wikimedia Commons", "verdict", "yellow", M),
    ("अगर अगला ऐसा पल, आज ही हो रहा हो तो? आप क्या सोचते हैं?",
     "closing question card", "आप क्या सोचते हैं?", "सवाल", "—", "tension", "red", I),
]

FACTS = [
    "Sarajevo, 28 June 1914: Čabrinović's bomb bounced off Franz Ferdinand's car and exploded under the following car; after the town-hall reception the route was changed to visit the wounded in hospital, but the driver (Leopold Lojka) was not told, turned into Franz Josef Street, stopped when General Potiorek shouted, and Gavrilo Princip (19) shot Franz Ferdinand and Sophie near the Latin Bridge (History.com 'How a wrong turn started World War I'; Smithsonian 'Gavrilo Princip's sandwich' — the sandwich story is a myth, not used; Mental Floss WWI centennial). Austria-Hungary declared war on Serbia on 28 July 1914.",
    "WWI deaths: estimates of military plus civilian deaths run from about 15 to 22 million; 'लगभग दो करोड़' is said as an approximation (Britannica, 'World War I: Killed, wounded and missing').",
    "Penicillin: Alexander Fleming, St Mary's Hospital, Paddington, returned from holiday in September 1928 (28 Sept is the usual date he noticed it) and found a Staphylococcus plate contaminated by a Penicillium mould with a clear zone around it; he named the substance penicillin (paper 1929). Mass production came in the 1940s (Florey and Chain; US production for D-Day 1944). 'करोड़ों जानें बचाईं' is a widely cited estimate (Science History Institute; World History Encyclopedia; PBS NewsHour 'The real story behind the world's first antibiotic'; Live Science).",
    "B-59, 27 October 1962: hunted by USS Randolph and destroyers, which dropped practice (signalling) depth charges to force it up; batteries low, no contact with Moscow. Per Vadim Orlov (2002) Captain Savitsky ordered the nuclear torpedo readied; launch needed the agreement of Savitsky, political officer Maslennikov and flotilla chief of staff Vasili Arkhipov, who refused; the boat surfaced (National Security Archive, nsarchive.gwu.edu/node/4005 and the 2002 Havana conference briefing book; National Geographic 2016). Accounts of the scene come from crew testimony years later: said 'के मुताबिक़'.",
    "Petrov, 26 September 1983: Lt Col Stanislav Petrov on duty at Serpukhov-15, the Oko early-warning system reported one Minuteman launch then more (up to five); he judged it a false alarm because a real US first strike would use hundreds of missiles and he distrusted the new system; the cause was sunlight reflecting off high clouds seen by the satellite from its Molniya orbit (Britannica 'Stanislav Petrov'; RFE/RL; Wikipedia '1983 Soviet nuclear false alarm incident'). The screen word was 'СТАРТ' (start) per Petrov's interviews.",
    "Berlin, 9 November 1989: at the evening press conference Günter Schabowski read a new travel regulation from a note he had not been briefed on; asked when it took effect he said 'Das tritt nach meiner Kenntnis... ist das sofort, unverzüglich' (transcript, Wilson Center Digital Archive 89307; Bundesregierung archive). The rule was meant to start the next day with visa applications. Crowds gathered; at Bornholmer Straße guards let the first people through around 21:20 and Harald Jäger opened the gate fully about 23:30 (berlin.de 'Opening and fall of the Wall'). The wall stood from August 1961 (28 years). Germany reunified on 3 October 1990; the USSR dissolved in December 1991.",
    "Framing: the five moments are chosen as 'small accidents or single decisions' with large consequences; historians stress deeper causes too (alliances and nationalism in 1914; Florey and Chain's work made penicillin a drug; the end of the Cold War had many causes). The film says this in the verdict line ('हमेशा बड़े फ़ैसलों से नहीं').",
]


def disp(s):
    return re.sub(r"\s*\.\.\.\s*", ", ", s).replace(", ,", ",").strip()


def main():
    takes, n = [], 0
    for take, heading, lines in FILM:
        out = []
        for spoken, hero, typed, mood, tag, hook in lines:
            n += 1
            d = {"id": n, "text": disp(spoken), "spoken": spoken, "hero": hero, "typed": typed, "mood": mood, "v3": tag}
            if hook:
                d["hook"] = hook
            out.append(d)
        takes.append({"take": take, "heading": heading, "lines": out})
    script = {
        "title": "पाँच पल, जिन्होंने दुनिया बदल दी",
        "subtitle": "World-Changing Turning Points · एक जाँच",
        "series": "World-Changing Turning Points",
        "language": "hi",
        "format": {"film": "1920x1080, about 4:00 (user, 26 Nov 2026: length follows the recorded voice), with the YouTube intro T00_intro",
                   "reel": "separate script in reel/script.json"},
        "takes": takes, "fact_notes": FACTS, "film_cut": {"dropped_lines": [], "note": "set after the voice arrives"},
    }
    (P / "script.json").write_text(json.dumps(script, ensure_ascii=False, indent=1) + "\n")

    rl = []
    for k, (spoken, hero, headline, tag, source, mood, col, v3) in enumerate(REEL, 1):
        rl.append({"id": k, "text": disp(spoken), "spoken": spoken, "hero": hero, "typed": "", "headline": headline,
                   "tag": tag, "source": source, "mood": mood, "headline_color": col, "v3": v3})
    reel = {"title": script["title"], "series_tag": "पाँच पल · एक जाँच", "language": "hi",
            "format": {"reel": "1080x1920, about 60 s, fixed reel format (saanp/reel/scene.py), its own recording REEL"},
            "note": "Separate reel script (not cut from the film): opens on a question, ends on 'आप क्या सोचते हैं?'. Facts as in ../script.json fact_notes.",
            "takes": [{"take": "REEL", "heading": "रील", "lines": rl}], "reel_cut": {"dropped_lines": []}}
    (P / "reel" / "script.json").write_text(json.dumps(reel, ensure_ascii=False, indent=1) + "\n")

    fc = sum(len(l["spoken"]) for t in takes for l in t["lines"])
    rc = sum(len(l["spoken"]) for l in rl)
    head = ["- **दो अलग रिकॉर्डिंग:** (1) YouTube फ़िल्म: हर टेक एक फ़ाइल (`T00_intro.mp3` से `T07_verdict.mp3`), "
            "या तीन फ़ाइलें: Greeting (= T00_intro), पूरी कहानी एक फ़ाइल में (T01..T07), Reel; (2) रील: अलग फ़ाइल `REEL.mp3`।",
            "- हर लाइन के बाद लगभग **1 सेकंड रुकें**। `...` = छोटा नाटकीय ठहराव। आवाज़ Viraj, नैचुरल स्पीड (1.0x)।"]
    for tags, name, note in ((True, "voiceover_script_emotions.md", "(Eleven v3 इमोशन टैग के साथ)"), (False, "voiceover_script.md", "(सादी)")):
        o = [f"# {script['title']}: वॉयसओवर स्क्रिप्ट {note}", ""] + head
        if tags:
            o.append("- टैग **Eleven v3** के लिए हैं (बोले नहीं जाते)। Multilingual v2 में `voiceover_script.md` की सादी लाइनें लें।")
        o += ["", f"# भाग 1: YouTube फ़िल्म ({n} लाइनें, लगभग 4 मिनट, {fc} अक्षर)", ""]
        for t in takes:
            o += [f"## {t['heading']}  [{t['take']}.mp3]", ""]
            for l in t["lines"]:
                sp = l["spoken"].replace("... ", "... [short pause] ") if tags else l["spoken"]
                o += [f"{l['id']}. {l['v3'] + ' ' if tags else ''}{sp}", ""]
        o += [f"# भाग 2: रील (अलग रिकॉर्डिंग, {len(rl)} लाइनें, {rc} अक्षर)  [REEL.mp3]", ""]
        for l in rl:
            sp = l["spoken"].replace("... ", "... [short pause] ") if tags else l["spoken"]
            o += [f"{l['id']}. {l['v3'] + ' ' if tags else ''}{sp}", ""]
        (P / name).write_text("\n".join(o))
    print(f"film: {n} lines, {fc} chars (~{fc / 11.4 / 60:.1f} min); reel: {len(rl)} lines, {rc} chars (~{rc / 11.4:.0f} s)")
    for t in takes:
        print(f"  {t['take']}: {sum(len(l['spoken']) for l in t['lines'])} chars")


if __name__ == "__main__":
    main()
