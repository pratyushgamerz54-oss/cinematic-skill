#!/usr/bin/env python3
"""Writes the Area 51 HyperFrames hero graphics (palette: night blue, radar teal, desert amber; red only on 'गोली')."""
import json, random
random.seed(51)
CSS = """@font-face{font-family:"Teko HF";src:url("assets/fonts/cond.ttf");}
@font-face{font-family:"Hind HF";src:url("assets/fonts/label.ttf");}
@font-face{font-family:"Hind HF Light";src:url("assets/fonts/labelm.ttf");}
@font-face{font-family:"Tiro HF";src:url("assets/fonts/serif.ttf");}
#root{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 55%,#10202a 0%,#070c12 60%,#030507 100%);overflow:hidden;color:#eef2f0;}
.k{position:absolute;left:0;right:0;text-align:center;}
.teal{color:#3fe0cc;} .amber{color:#ffb347;} .red{color:#e0483a;}
.src{position:absolute;left:0;right:0;bottom:130px;text-align:center;font-family:"Hind HF Light";font-size:34px;color:#9fb3b0;letter-spacing:.02em;}
.chip{position:absolute;font-family:'Hind HF';font-size:60px;padding:10px 34px 4px;background:rgba(6,14,18,.86);border-left:10px solid #3fe0cc;color:#eef2f0;}
.star{position:absolute;border-radius:50%;background:#dfe8f0;}
.ring{position:absolute;border:3px solid rgba(63,224,204,.55);border-radius:50%;}
"""
def comp(cid, dur, body, js):
    return f"""<template>
  <style>
{CSS}</style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""
def stars(cid, n, dur):
    b, j = [], []
    for i in range(n):
        x, y, s = random.randint(0, 1920), random.randint(0, 760), random.uniform(1.5, 4)
        b.append(f'    <div id="{cid}-s{i}" class="clip star" data-start="0" data-duration="{dur}" style="left:{x}px;top:{y}px;width:{s:.1f}px;height:{s:.1f}px"></div>')
        j.append(f'    tl.fromTo("#{cid}-s{i}",{{opacity:0}},{{opacity:{random.uniform(.3,.9):.2f},duration:{random.uniform(.6,2):.1f},yoyo:true,repeat:{int(dur)},ease:"sine.inOut"}},{random.uniform(0,1.5):.2f});')
    return b, j
def radar(cid, dur, cx=960, cy=560, n=4, r0=160, dr=150, t0=0.0):
    b, j = [], []
    for i in range(n):
        r = r0 + i * dr
        b.append(f'    <div id="{cid}-r{i}" class="clip ring" data-start="0" data-duration="{dur}" style="left:{cx-r}px;top:{cy-r}px;width:{2*r}px;height:{2*r}px"></div>')
        j.append(f'    tl.fromTo("#{cid}-r{i}",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.9,ease:"power2.out"}},{t0 + i*0.12:.2f});')
    R = r0 + (n - 1) * dr
    b.append(f'    <div id="{cid}-sw" class="clip" data-start="0" data-duration="{dur}" style="position:absolute;left:{cx-R}px;top:{cy-R}px;width:{2*R}px;height:{2*R}px;border-radius:50%;background:conic-gradient(from 0deg,rgba(63,224,204,.38),rgba(63,224,204,0) 70deg,rgba(0,0,0,0) 360deg)"></div>')
    j.append(f'    tl.fromTo("#{cid}-sw",{{rotation:0,opacity:0}},{{rotation:{360*dur/3.2:.0f},opacity:1,duration:{dur},ease:"none"}},{t0});')
    return b, j
C = {}
# welcome 0-5
b, j = stars("wel", 50, 5); rb, rj = radar("wel", 5)
b += rb; j += rj
b += ['    <div id="wel-a" class="clip k amber" data-start="0" data-duration="5" style="top:330px;font-family:\'Teko HF\';font-size:240px;line-height:1">नमस्कार</div>',
      '    <div id="wel-b" class="clip k" data-start="0.8" data-duration="4.2" style="top:640px;font-family:\'Hind HF\';font-size:76px">आपका स्वागत है</div>']
j += ['    tl.fromTo("#wel-a",{opacity:0,y:40,scaleX:1.25},{opacity:1,y:0,scaleX:1,duration:1.0,ease:"power3.out"},0.15);',
      '    tl.fromTo("#wel-b",{opacity:0,y:20},{opacity:1,y:0,duration:0.6,ease:"power2.out"},0.8);',
      '    tl.fromTo("#wel-a",{scale:1},{scale:1.04,duration:3.8,ease:"none",immediateRender:false},1.1);']
C["welcome"] = (5, b, j)
# topic 0-26: (2) photo + redaction 0-7; (3) chips 7-15; (4) the light 15-20; (5) title 20-26
b, j = stars("top", 40, 26)
b += ['    <img id="top-ph" class="clip" data-start="0" data-duration="26" src="assets/img/groom.jpg" style="position:absolute;left:0;top:-180px;width:1920px;height:1440px;object-fit:cover;filter:saturate(1.15) contrast(1.05)">',
      '    <div id="top-vig" class="clip" data-start="0" data-duration="26" style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(3,5,7,0) 40%,rgba(3,5,7,.8) 100%)"></div>',
      '    <div id="top-bar" class="clip" data-start="0" data-duration="26" style="position:absolute;left:460px;top:470px;width:1000px;height:120px;background:#050708;transform-origin:0 50%"></div>',
      '    <div id="top-bt" class="clip k" data-start="0" data-duration="26" style="top:484px;font-family:\'Teko HF\';font-size:110px;line-height:1;color:#3fe0cc;letter-spacing:.2em">CLASSIFIED</div>',
      '    <div id="top-c1" class="clip chip" data-start="1.4" data-duration="5.6" style="left:220px;top:760px">नाम लेना मना</div>',
      '    <div id="top-c2" class="clip chip" data-start="3.4" data-duration="3.6" style="left:1180px;top:760px;border-left-color:#ffb347">≈ 60 साल</div>',
      '    <div id="top-streak" class="clip" data-start="7" data-duration="8" style="position:absolute;left:-300px;top:260px;width:320px;height:8px;border-radius:4px;background:linear-gradient(90deg,rgba(255,255,255,0),#e8fff9);box-shadow:0 0 24px #8ff;"></div>',
      '    <div id="top-c3" class="clip chip" data-start="7.6" data-duration="7.4" style="left:260px;top:620px">अजीब रोशनियाँ?</div>',
      '    <div id="top-tri" class="clip" data-start="10.8" data-duration="4.2" style="position:absolute;left:1210px;top:420px;width:0;height:0;border-left:110px solid transparent;border-right:110px solid transparent;border-bottom:190px solid #ffb347"></div>',
      '    <div id="top-tri2" class="clip k" data-start="10.8" data-duration="4.2" style="left:1210px;right:auto;width:220px;top:470px;font-family:\'Teko HF\';font-size:150px;line-height:1;color:#101418">!</div>',
      '    <div id="top-c4" class="clip chip" data-start="11.2" data-duration="3.8" style="left:1040px;top:660px;border-left-color:#e0483a"><span class="red">गोली</span> की इजाज़त?</div>',
      '    <div id="top-orb" class="clip" data-start="15" data-duration="5" style="position:absolute;left:930px;top:820px;width:60px;height:60px;border-radius:50%;background:radial-gradient(circle,#fff 0%,#bff 30%,rgba(63,224,204,0) 70%)"></div>',
      '    <div id="top-q" class="clip k" data-start="15.6" data-duration="4.4" style="top:220px;font-family:\'Hind HF\';font-size:80px">दूसरी दुनिया का राज़?</div>',
      '    <div id="top-t" class="clip k amber" data-start="20" data-duration="6" style="top:330px;font-family:\'Teko HF\';font-size:330px;line-height:1;letter-spacing:.04em">एरिया 51</div>',
      '    <div id="top-st" class="clip k" data-start="20.8" data-duration="5.2" style="top:700px;font-family:\'Hind HF\';font-size:72px">पूरा कच्चा चिट्ठा</div>',
      '    <div id="top-ln" class="clip" data-start="20.4" data-duration="5.6" style="position:absolute;left:560px;top:672px;width:800px;height:6px;background:#3fe0cc;transform-origin:50% 50%"></div>']
j += ['    tl.fromTo("#top-ph",{opacity:0,scale:1.15},{opacity:1,scale:1.0,duration:7,ease:"none"},0);',
      '    tl.fromTo("#top-bar",{scaleX:0},{scaleX:1,duration:0.5,ease:"power3.out"},0.4);',
      '    tl.fromTo("#top-bt",{opacity:0},{opacity:1,duration:0.3},0.8);',
      '    tl.fromTo("#top-c1",{opacity:0,x:-40},{opacity:1,x:0,duration:0.4,ease:"power2.out"},1.4);',
      '    tl.fromTo("#top-c2",{opacity:0,x:40},{opacity:1,x:0,duration:0.4,ease:"power2.out"},3.4);',
      '    tl.to(["#top-bar","#top-bt"],{opacity:0,duration:0.5},6.8); tl.to("#top-ph",{opacity:0.22,duration:0.6},6.8);',
      '    tl.fromTo("#top-streak",{x:0,opacity:0},{x:2400,opacity:1,duration:2.2,ease:"power1.in"},7.2);',
      '    tl.fromTo("#top-c3",{opacity:0,y:30},{opacity:1,y:0,duration:0.4,ease:"power2.out"},7.6);',
      '    tl.fromTo("#top-tri",{opacity:0,scale:0.4},{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"},10.8);',
      '    tl.fromTo("#top-tri2",{opacity:0},{opacity:1,duration:0.2},10.95);',
      '    tl.fromTo("#top-c4",{opacity:0,y:30},{opacity:1,y:0,duration:0.4,ease:"power2.out"},11.2);',
      '    tl.to(["#top-c3","#top-c4","#top-tri","#top-tri2"],{opacity:0,duration:0.5},14.6);',
      '    tl.fromTo("#top-orb",{opacity:0,y:0,scale:0.6},{opacity:1,y:-520,scale:1.4,duration:4.4,ease:"power1.inOut"},15.1);',
      '    tl.fromTo("#top-q",{opacity:0},{opacity:1,duration:0.8},15.6);',
      '    tl.to(["#top-orb","#top-q","#top-ph","#top-bar","#top-bt"],{opacity:0,duration:0.5},19.6);',
      '    tl.fromTo("#top-t",{opacity:0,scale:1.4,filter:"blur(16px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:0.5,ease:"power4.out"},20.05);',
      '    tl.fromTo("#top-ln",{scaleX:0},{scaleX:1,duration:0.6,ease:"power3.out"},20.4);',
      '    tl.fromTo("#top-st",{opacity:0,y:20},{opacity:1,y:0,duration:0.5},20.8);',
      '    tl.fromTo("#top-t",{scale:1},{scale:1.05,duration:5.4,ease:"none",immediateRender:false},20.6);']
C["topic"] = (26, b, j)
# go 0-4
b, j = radar("go", 4, n=3)
b += ['    <div id="go-a" class="clip k" data-start="0" data-duration="2.2" style="top:420px;font-family:\'Hind HF\';font-size:110px">तो चलिए...</div>',
      '    <div id="go-scan" class="clip" data-start="0" data-duration="4" style="position:absolute;left:0;top:0;width:1920px;height:14px;background:linear-gradient(180deg,rgba(63,224,204,0),#3fe0cc,rgba(63,224,204,0));box-shadow:0 0 40px #3fe0cc"></div>',
      '    <div id="go-d" class="clip k amber" data-start="2.0" data-duration="2" style="top:380px;font-family:\'Teko HF\';font-size:260px;line-height:1">20.09.2019</div>']
j += ['    tl.fromTo("#go-a",{opacity:0,y:20},{opacity:1,y:0,duration:0.5},0.1);',
      '    tl.to("#go-a",{opacity:0,duration:0.3},1.9);',
      '    tl.fromTo("#go-scan",{y:-20},{y:1100,duration:1.4,ease:"power2.inOut"},1.4);',
      '    tl.fromTo("#go-d",{opacity:0,scale:1.3},{opacity:1,scale:1,duration:0.35,ease:"power3.out"},2.1);']
C["go"] = (4, b, j)
# qopen 0-8
b, j = stars("qo", 30, 8)
b += ['    <div id="qo-a" class="clip k" data-start="0" data-duration="8" style="top:220px;font-family:\'Hind HF\';font-size:76px;color:#c6d4d2">इस बंद दरवाज़े के पीछे...</div>',
      '    <div id="qo-b" class="clip k amber" data-start="1.6" data-duration="6.4" style="top:350px;font-family:\'Teko HF\';font-size:250px;line-height:1">आख़िर क्या है?</div>',
      '    <div id="qo-c" class="clip k" data-start="4.0" data-duration="4" style="top:700px;font-family:\'Hind HF\';font-size:84px">जिसके लिए <span class="red">गोली</span> तक चल सकती है</div>',
      '    <div id="qo-flash" class="clip" data-start="0" data-duration="8" style="position:absolute;inset:0;background:#dff;opacity:0"></div>']
j += ['    tl.fromTo("#qo-a",{opacity:0,y:20},{opacity:1,y:0,duration:0.6,ease:"power2.out"},0.05);',
      '    tl.fromTo("#qo-b",{opacity:0,scale:1.35,filter:"blur(14px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:0.35,ease:"power4.out"},1.65);',
      '    tl.fromTo("#qo-flash",{opacity:0.3},{opacity:0,duration:0.25,immediateRender:false},4.0);',
      '    tl.fromTo("#qo-c",{opacity:0,y:40},{opacity:1,y:0,duration:0.35,ease:"power3.out"},4.02);',
      '    tl.fromTo("#qo-b",{scale:1},{scale:1.05,duration:6,ease:"none",immediateRender:false},2.0);']
C["qopen"] = (8, b, j)
def quote(cid, dur, intro, en, hi, src):
    b = [f'    <div id="{cid}-g" class="clip" data-start="0" data-duration="{dur}" style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 55%,rgba(63,224,204,.22) 0%,rgba(0,0,0,0) 65%);opacity:0"></div>',
         f'    <div id="{cid}-i" class="clip k" data-start="0" data-duration="{dur}" style="top:200px;font-family:\'Hind HF\';font-size:58px;color:#b8c8c6">{intro}</div>',
         f'    <div id="{cid}-e" class="clip k teal" data-start="0.9" data-duration="{dur-0.9}" style="top:330px;left:160px;right:160px;font-family:\'Tiro HF\';font-size:108px;line-height:1.15">{en}</div>',
         f'    <div id="{cid}-h" class="clip k" data-start="2.4" data-duration="{dur-2.4}" style="top:660px;font-family:\'Hind HF\';font-size:72px">{hi}</div>',
         f'    <div id="{cid}-s" class="clip src" data-start="2.8" data-duration="{dur-2.8}">{src}</div>']
    j = [f'    tl.fromTo("#{cid}-i",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.6}},0.1);',
         f'    tl.fromTo("#{cid}-g",{{opacity:0}},{{opacity:1,duration:1.2}},0.6);',
         f'    tl.fromTo("#{cid}-e",{{opacity:0,scale:1.06,filter:"blur(10px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.9,ease:"power3.out"}},0.9);',
         f'    tl.fromTo("#{cid}-h",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.5}},2.4);',
         f'    tl.fromTo("#{cid}-s",{{opacity:0}},{{opacity:1,duration:0.5}},2.8);',
         f'    tl.fromTo("#{cid}-e",{{scale:1}},{{scale:1.03,duration:{dur-2},ease:"none",immediateRender:false}},1.8);']
    return b, j
C["haines"] = (8,) + quote("haines", 8, "सीआईए का अपना अध्ययन (1997)", "“...over half of all UFO reports...”", "आधी से ज़्यादा यूएफ़ओ रिपोर्टें: जासूसी उड़ानें", "Gerald K. Haines, CIA Studies in Intelligence, 1997")
C["aaro"] = (7,) + quote("aaro", 7, "पेंटागन का दफ़्तर AARO (मार्च 2024)", "“...no evidence...”", "एलियन तकनीक का कोई सबूत नहीं", "AARO, Report on the Historical Record, Vol. I, 2024")
# qend 0-9
b, j = stars("qe", 40, 9); rb, rj = radar("qe", 9, n=3, t0=0.2); b += rb; j += rj
b += ['    <div id="qe-a" class="clip k" data-start="0" data-duration="9" style="top:220px;font-family:\'Hind HF\';font-size:84px">सिर्फ़ इंसानों के राज़?</div>',
      '    <div id="qe-b" class="clip k teal" data-start="1.8" data-duration="7.2" style="top:360px;font-family:\'Teko HF\';font-size:200px;line-height:1">या कुछ और?</div>',
      '    <div id="qe-c" class="clip k amber" data-start="4.0" data-duration="5" style="top:640px;font-family:\'Teko HF\';font-size:170px;line-height:1">आप क्या सोचते हैं?</div>',
      '    <div id="qe-d" class="clip k" data-start="5.6" data-duration="3.4" style="top:860px;font-family:\'Hind HF Light\';font-size:46px;color:#b8c8c6">कमेंट में बताइए ↓</div>']
j += ['    tl.fromTo("#qe-a",{opacity:0,y:20},{opacity:1,y:0,duration:0.6},0.1);',
      '    tl.fromTo("#qe-b",{opacity:0,scale:1.3,filter:"blur(12px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:0.4,ease:"power4.out"},1.85);',
      '    tl.fromTo("#qe-c",{opacity:0,y:40},{opacity:1,y:0,duration:0.4,ease:"power3.out"},4.05);',
      '    tl.fromTo("#qe-d",{opacity:0},{opacity:1,duration:0.5},5.6);',
      '    tl.fromTo("#qe-c",{scale:1},{scale:1.05,duration:4.5,ease:"none",immediateRender:false},4.5);']
C["qend"] = (9, b, j)
# rq 0-6 (reel opening question)
b, j = stars("rq", 30, 6)
b += ['    <div id="rq-a" class="clip k" data-start="0" data-duration="6" style="top:240px;font-family:\'Hind HF\';font-size:84px">नाम लेना तक मना था...</div>',
      '    <div id="rq-b" class="clip k amber" data-start="1.8" data-duration="4.2" style="top:400px;font-family:\'Teko HF\';font-size:230px;line-height:1">वहाँ छुपा क्या है?</div>',
      '    <div id="rq-c" class="clip k teal" data-start="3.0" data-duration="3" style="top:720px;font-family:\'Teko HF\';font-size:120px;line-height:1;letter-spacing:.08em">AREA 51</div>']
j += ['    tl.fromTo("#rq-a",{opacity:0,y:20},{opacity:1,y:0,duration:0.5},0.1);',
      '    tl.fromTo("#rq-b",{opacity:0,scale:1.3,filter:"blur(12px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:0.4,ease:"power4.out"},1.85);',
      '    tl.fromTo("#rq-c",{opacity:0,y:30},{opacity:1,y:0,duration:0.4},3.0);']
C["rq"] = (6, b, j)

order = ["welcome", "topic", "go", "qopen", "haines", "aaro", "qend", "rq"]
t = 0; segs = []; divs = []
for cid in order:
    dur, b, j = C[cid]
    open(f"compositions/{cid}.html", "w").write(comp(cid, dur, "\n".join(b), "\n".join(j)))
    segs.append({"id": cid, "start": t, "end": t + dur})
    divs.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{t}" data-duration="{dur}" data-track-index="0" data-track-kind="graphics" data-width="1920" data-height="1080"></div>')
    t += dur
open("index.html", "w").write(f"""<!doctype html>
<html lang="hi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #030507; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{t}" data-width="1920" data-height="1080">
{chr(10).join(divs)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
json.dump(segs, open("segments.json", "w"), indent=1)
json.dump({"id": "area51-hf", "name": "area51-hf", "createdAt": "2026-11-25T00:00:00Z"}, open("meta.json", "w"))
print(t, "s total")
