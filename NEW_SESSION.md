# नए session के लिए (copy करके नए session में भेजें)

नीचे वाला पूरा ब्लॉक नए session की पहली message में चिपकाइए, फिर आख़िर में अपना topic लिख दीजिए।

```
इस repo (cinematic-skill) में पहले HANDOFF.md और CLAUDE.md पूरा पढ़ो। उनमें मेरे सारे order लिखे हैं, उन्हीं के हिसाब से काम करो।
saanp/, tut/ (तूतनख़ामुन) और area51/ (एरिया 51, सबसे नया) तैयार reference projects हैं, उनके patterns copy करो।

मैं सिर्फ़ topic दूँगा। उसका मतलब है पूरा package:
1. Research + fact-check (sources fact_notes में), फिर दो अलग स्क्रिप्ट:
   - YouTube फ़िल्म (script.json): पहले YouTube इंट्रो T00_intro ("नमस्कार दोस्तों, आपका स्वागत है" → topic की 1-2 लाइन → "तो चलिए, शुरू करते हैं"), फिर कहानी की 50 लाइनें, 9 टेक, ~3,700-3,900 अक्षर (Viraj की नैचुरल स्पीड पर ~5:18 से 5:30)।
   - रील (reel/script.json): अलग स्क्रिप्ट, अलग रिकॉर्डिंग, 9-11 लाइनें, ~720 अक्षर (~60 सेकंड), सवाल से शुरू, "आप क्या सोचते हैं?" पर ख़त्म।
2. एक ही बार रुको: beats.md भेजो और पूछो कि स्क्रिप्ट मंज़ूर है या नहीं। मैं आवाज़ ख़ुद ElevenLabs पर Viraj से बनाऊँगा।
   इसलिए हर फ़ाइल का एक अलग copy करने लायक ब्लॉक दो (v3 emotion tags के साथ): T00_intro, T01 से T09, और REEL।
3. आवाज़ आने तक बाक़ी सब बना लो: Commons फ़ोटो (15-20), 3D ग्लोब, 2D नक्शा, कम से कम 3-4 3D मॉडल, HyperFrames hero graphics (इंट्रो welcome/topic/go, शुरुआती सवाल, 1-2 quote card, आख़िरी सवाल, रील का सवाल), थंबनेल।
   ज़रूरत हो तो उसी scene का असली वीडियो फ़ुटेज भी (free licence, credit के साथ)।
4. मैं आवाज़ इस तरह भेज सकता हूँ: Greeting (इंट्रो), पूरी कहानी एक ही फ़ाइल में, और Reel। तब पूरी कहानी को एक टेक मानकर split करो (tut/audio/_split जैसे)।
   आवाज़ कभी तेज़ मत करना (1.0x)। फ़िल्म लंबी हो तो पूरी लाइनें हटाओ (film_cut), gap 0.45 से 0.6 सेकंड।
5. Scene (हर लाइन पर उसी को समझाने वाला visual, शांत documentary camera, बोले गए शब्द पर नई चीज़, mood background), हर लाइन का still check करो, 20 सेकंड के test हिस्से render करके देखो, फिर sound, render, captions (फ़िल्म clean, रील highlighter), SRT, share copies, थंबनेल।
6. भेजो: फ़िल्म (captions के साथ), caption-free copy, SRT, रील + SRT, दोनों थंबनेल। फिर commit + push करो (100 MB से बड़ी फ़ाइलें git में नहीं)।
मेरा हर नया order HANDOFF.md और CLAUDE.md में सेव करते जाओ।

Topic: <यहाँ अपना topic लिखें>
```

## सबसे छोटा version (अब यही काफ़ी है)

```
HANDOFF.md और CLAUDE.md पढ़ो। area51/ सबसे नया reference है। पिछला काम अधूरा हो तो पहले उसे पूरा करो (bash area51/tools/finish.sh)।
Topic: <यहाँ अपना topic लिखें>
```

## छोटा version (अगर बस topic भेजना हो)

`CLAUDE.md` हर session में अपने-आप पढ़ी जाती है, इसलिए नए session में सिर्फ़ topic भेजना भी काफ़ी है।
ऊपर वाला ब्लॉक बस पक्का करने के लिए है कि कोई बात छूटे नहीं।
