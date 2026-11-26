#!/usr/bin/env python3
"""Writes the Turning Points HyperFrames hero graphics (palette: archive gold, radar teal; red only on the one "ना")."""
import json, random
random.seed(1914)
CSS = """.gold{color:#e8c27a;} .dust{position:absolute;border-radius:50%;background:#f0d8a0;}
@font-face{font-family:"Teko HF";src:url("assets/fonts/cond.ttf");}
@font-face{font-family:"Hind HF";src:url("assets/fonts/label.ttf");}
@font-face{font-family:"Hind HF Light";src:url("assets/fonts/labelm.ttf");}
@font-face{font-family:"Tiro HF";src:url("assets/fonts/serif.ttf");}
#root{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 55%,#2a2016 0%,#100c08 60%,#050403 100%);overflow:hidden;color:#eef2f0;}
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

CSS2 = ".gold{color:#e8c27a;} .dust{position:absolute;border-radius:50%;background:#f0d8a0;}"
def dust(cid, n, dur):
    b, j = [], []
    for i in range(n):
        x, y, s = random.randint(0, 1920), random.randint(0, 1080), random.uniform(2, 5)
        b.append(f'    <div id="{cid}-d{i}" class="clip dust" data-start="0" data-duration="{dur}" style="left:{x}px;top:{y}px;width:{s:.1f}px;height:{s:.1f}px;opacity:0"></div>')
        j.append(f'    tl.fromTo("#{cid}-d{i}",{{opacity:0,y:0}},{{opacity:{random.uniform(.25,.7):.2f},y:{-random.randint(40,160)},duration:{dur},ease:"none"}},0);')
    return b, j
def dial(cid, dur, cx=960, cy=540, R=360, t0=0.0, spin=60, labels=None, tlab=None):
    """a brass clock dial: two rings, 60 ticks, a rotating hand; optional year labels at given angles."""
    b, j = [], []
    for k, (r, w, op) in enumerate([(R, 4, .8), (R - 40, 2, .45)]):
        b.append(f'    <div id="{cid}-ring{k}" class="clip" data-start="0" data-duration="{dur}" style="position:absolute;left:{cx-r}px;top:{cy-r}px;width:{2*r}px;height:{2*r}px;border-radius:50%;border:{w}px solid rgba(232,194,122,{op})"></div>')
        j.append(f'    tl.fromTo("#{cid}-ring{k}",{{opacity:0,scale:0.85}},{{opacity:1,scale:1,duration:0.9,ease:"power2.out"}},{t0 + k*0.15:.2f});')
    b.append(f'    <div id="{cid}-ticks" class="clip" data-start="0" data-duration="{dur}" style="position:absolute;left:{cx-R}px;top:{cy-R}px;width:{2*R}px;height:{2*R}px;border-radius:50%;background:repeating-conic-gradient(from 0deg,rgba(232,194,122,.75) 0deg 0.8deg,rgba(0,0,0,0) 0.8deg 6deg);-webkit-mask:radial-gradient(circle,transparent {R-22}px,#000 {R-21}px,#000 {R-6}px,transparent {R-5}px);mask:radial-gradient(circle,transparent {R-22}px,#000 {R-21}px,#000 {R-6}px,transparent {R-5}px)"></div>')
    j.append(f'    tl.fromTo("#{cid}-ticks",{{opacity:0,rotation:-20}},{{opacity:1,rotation:0,duration:1.2,ease:"power2.out"}},{t0+0.2:.2f});')
    b.append(f'    <div id="{cid}-hand" class="clip" data-start="0" data-duration="{dur}" style="position:absolute;left:{cx-3}px;top:{cy-R+60}px;width:6px;height:{R-60}px;background:linear-gradient(180deg,#f6dca0,rgba(232,194,122,.2));transform-origin:50% 100%"></div>')
    j.append(f'    tl.fromTo("#{cid}-hand",{{rotation:0,opacity:0}},{{rotation:{spin},opacity:1,duration:{dur - t0},ease:"none"}},{t0});')
    return b, j
C = {}
# welcome 0-5
b, j = dust("wel", 40, 5); db, dj = dial("wel", 5, spin=50); b += db; j += dj
b += ['    <div id="wel-a" class="clip k gold" data-start="0" data-duration="5" style="top:350px;font-family:\'Teko HF\';font-size:230px;line-height:1">नमस्कार</div>',
      '    <div id="wel-b" class="clip k" data-start="0.8" data-duration="4.2" style="top:620px;font-family:\'Hind HF\';font-size:72px">आपका स्वागत है</div>']
j += ['    tl.fromTo("#wel-a",{opacity:0,y:40,scaleX:1.25},{opacity:1,y:0,scaleX:1,duration:1.0,ease:"power3.out"},0.15);',
      '    tl.fromTo("#wel-b",{opacity:0,y:20},{opacity:1,y:0,duration:0.6,ease:"power2.out"},0.8);',
      '    tl.fromTo("#wel-a",{scale:1},{scale:1.04,duration:3.8,ease:"none",immediateRender:false},1.1);']
C["welcome"] = (5, b, j)
# topic 0-24: (2) two question chips 0-9; (3) the "ना" key 9-15; (4) five dates + title 15-24
b, j = dust("top", 50, 24); db, dj = dial("top", 24, R=420, spin=200); b += db; j += dj
yrs = [("1914", -72), ("1928", -36), ("1962", 0), ("1983", 36), ("1989", 72)]
b += ['    <div id="top-car" class="clip" data-start="0.6" data-duration="8.4" style="position:absolute;left:330px;top:300px;width:300px;height:300px"><svg viewBox="0 0 300 300" width="300" height="300"><path id="top-carp" d="M30 250 L30 120 Q30 70 80 70 L250 70" fill="none" stroke="#e8c27a" stroke-width="14" stroke-linecap="round" stroke-dasharray="420" stroke-dashoffset="420"/><path d="M230 40 L270 70 L230 100" fill="none" stroke="#e8c27a" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></svg></div>',
      '    <div id="top-c1" class="clip chip" data-start="0.8" data-duration="8.2" style="left:260px;top:640px;border-left-color:#e8c27a">ग़लत मोड़?</div>',
      '    <div id="top-dish" class="clip" data-start="4.0" data-duration="5" style="position:absolute;left:1270px;top:290px;width:320px;height:320px;border-radius:50%;border:8px solid rgba(232,240,240,.7);background:radial-gradient(circle at 40% 42%,#3c7a6c 0 16%,#f2e6bc 17% 34%,#c9a85a 36% 100%)"></div>',
      '    <div id="top-c2" class="clip chip" data-start="4.2" data-duration="4.8" style="left:1180px;top:640px;border-left-color:#3fe0cc">गंदी प्लेट?</div>',
      '    <div id="top-key" class="clip" data-start="9.2" data-duration="5.8" style="position:absolute;left:810px;top:330px;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,#3a0a06 0 52%,#e0483a 53% 58%,#1a0806 59% 100%);box-shadow:0 0 60px rgba(224,72,58,.35)"></div>',
      '    <div id="top-keyb" class="clip" data-start="9.2" data-duration="5.8" style="position:absolute;left:945px;top:360px;width:30px;height:240px;border-radius:12px;background:#d8d0c4"></div>',
      '    <div id="top-c3" class="clip chip" data-start="9.6" data-duration="5.4" style="left:770px;top:700px;border-left-color:#e0483a">एक <span class="red">‘ना’</span>?</div>']
for k, (y, a) in enumerate(yrs):
    import math
    x = 960 + math.sin(math.radians(a)) * 520 - 120; yy = 560 - math.cos(math.radians(a)) * 380 - 40
    b.append(f'    <div id="top-y{k}" class="clip" data-start="15" data-duration="9" style="position:absolute;left:{x:.0f}px;top:{yy:.0f}px;width:240px;text-align:center;font-family:\'Teko HF\';font-size:96px;line-height:1;color:#e8c27a">{y}</div>')
    j.append(f'    tl.fromTo("#top-y{k}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4,ease:"power2.out"}},{15.2 + k*0.35:.2f});')
b += ['    <div id="top-t" class="clip k gold" data-start="18" data-duration="6" style="top:420px;font-family:\'Teko HF\';font-size:300px;line-height:1;letter-spacing:.03em">पाँच पल</div>',
      '    <div id="top-st" class="clip k" data-start="18.8" data-duration="5.2" style="top:740px;font-family:\'Hind HF\';font-size:70px">जिन्होंने दुनिया बदल दी</div>',
      '    <div id="top-ln" class="clip" data-start="18.4" data-duration="5.6" style="position:absolute;left:560px;top:716px;width:800px;height:6px;background:#3fe0cc;transform-origin:50% 50%"></div>']
j += ['    tl.to("#top-carp",{strokeDashoffset:0,duration:1.2,ease:"power2.inOut"},0.7);',
      '    tl.fromTo("#top-car",{opacity:0},{opacity:1,duration:0.3},0.6);',
      '    tl.fromTo("#top-c1",{opacity:0,x:-40},{opacity:1,x:0,duration:0.4,ease:"power2.out"},0.9);',
      '    tl.fromTo("#top-dish",{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.6,ease:"back.out(1.6)"},4.0);',
      '    tl.fromTo("#top-c2",{opacity:0,x:40},{opacity:1,x:0,duration:0.4,ease:"power2.out"},4.3);',
      '    tl.to(["#top-car","#top-c1","#top-dish","#top-c2"],{opacity:0,duration:0.5},8.6);',
      '    tl.fromTo(["#top-key","#top-keyb"],{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.5,ease:"back.out(1.8)"},9.2);',
      '    tl.fromTo("#top-keyb",{rotation:0},{rotation:-18,duration:0.5,yoyo:true,repeat:3,ease:"sine.inOut",immediateRender:false},10.6);',
      '    tl.fromTo("#top-c3",{opacity:0,y:30},{opacity:1,y:0,duration:0.4,ease:"power2.out"},9.7);',
      '    tl.to(["#top-key","#top-keyb","#top-c3"],{opacity:0,duration:0.5},14.6);',
      '    tl.to(["#top-y0","#top-y1","#top-y2","#top-y3","#top-y4"],{opacity:0.35,duration:0.5},17.8);',
      '    tl.fromTo("#top-t",{opacity:0,scale:1.4,filter:"blur(16px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:0.5,ease:"power4.out"},18.05);',
      '    tl.fromTo("#top-ln",{scaleX:0},{scaleX:1,duration:0.6,ease:"power3.out"},18.4);',
      '    tl.fromTo("#top-st",{opacity:0,y:20},{opacity:1,y:0,duration:0.5},18.8);',
      '    tl.fromTo("#top-t",{scale:1},{scale:1.05,duration:5.4,ease:"none",immediateRender:false},18.6);']
C["topic"] = (24, b, j)
# go 0-4: the dial spins and lands on the cold-open date
b, j = dial("go", 4, spin=720)
b += ['    <div id="go-a" class="clip k" data-start="0" data-duration="2.2" style="top:440px;font-family:\'Hind HF\';font-size:110px">तो चलिए...</div>',
      '    <div id="go-scan" class="clip" data-start="0" data-duration="4" style="position:absolute;left:0;top:0;width:1920px;height:14px;background:linear-gradient(180deg,rgba(63,224,204,0),#3fe0cc,rgba(63,224,204,0));box-shadow:0 0 40px #3fe0cc"></div>',
      '    <div id="go-d" class="clip k" data-start="2.0" data-duration="2" style="top:400px;font-family:\'Teko HF\';font-size:250px;line-height:1;color:#3fe0cc">26.09.1983</div>']
j += ['    tl.fromTo("#go-a",{opacity:0,y:20},{opacity:1,y:0,duration:0.5},0.1);',
      '    tl.to("#go-a",{opacity:0,duration:0.3},1.9);',
      '    tl.fromTo("#go-scan",{y:-20},{y:1100,duration:1.4,ease:"power2.inOut"},1.4);',
      '    tl.fromTo("#go-d",{opacity:0,scale:1.3},{opacity:1,scale:1,duration:0.35,ease:"power3.out"},2.1);']
C["go"] = (4, b, j)
C["sofort"] = (9,) + quote("sofort", 9, "गुंटर शाबोव्स्की · प्रेस कॉन्फ़्रेंस, 9 नवंबर 1989", "„...sofort, unverzüglich.“", "तुरंत... बिना देरी के", "प्रेस कॉन्फ़्रेंस की ट्रांसक्रिप्ट · Wilson Center Digital Archive")
# qend 0-10
b, j = dust("qe", 50, 10); db, dj = dial("qe", 10, R=430, spin=40, t0=0.2); b += db; j += dj
b += ['    <div id="qe-a" class="clip k" data-start="0" data-duration="10" style="top:230px;font-family:\'Hind HF\';font-size:80px">क्या आज भी, कहीं...</div>',
      '    <div id="qe-b" class="clip k gold" data-start="1.8" data-duration="8.2" style="top:360px;font-family:\'Teko HF\';font-size:190px;line-height:1">कोई ऐसा पल</div>',
      '    <div id="qe-b2" class="clip k" data-start="3.2" data-duration="6.8" style="top:560px;font-family:\'Hind HF\';font-size:70px;color:#c8bca8">चुपचाप इंतज़ार कर रहा है?</div>',
      '    <div id="qe-c" class="clip k teal" data-start="5.4" data-duration="4.6" style="top:680px;font-family:\'Teko HF\';font-size:170px;line-height:1">आप क्या सोचते हैं?</div>',
      '    <div id="qe-d" class="clip k" data-start="6.8" data-duration="3.2" style="top:880px;font-family:\'Hind HF Light\';font-size:46px;color:#c8bca8">कमेंट में बताइए ↓</div>']
j += ['    tl.fromTo("#qe-a",{opacity:0,y:20},{opacity:1,y:0,duration:0.6},0.1);',
      '    tl.fromTo("#qe-b",{opacity:0,scale:1.3,filter:"blur(12px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:0.4,ease:"power4.out"},1.85);',
      '    tl.fromTo("#qe-b2",{opacity:0,y:20},{opacity:1,y:0,duration:0.5},3.2);',
      '    tl.fromTo("#qe-c",{opacity:0,y:40},{opacity:1,y:0,duration:0.4,ease:"power3.out"},5.45);',
      '    tl.fromTo("#qe-d",{opacity:0},{opacity:1,duration:0.5},6.8);',
      '    tl.fromTo("#qe-c",{scale:1},{scale:1.05,duration:4.5,ease:"none",immediateRender:false},5.9);']
C["qend"] = (10, b, j)
# rq 0-7 (reel opening question)
b, j = dust("rq", 40, 7); db, dj = dial("rq", 7, R=400, spin=90); b += db; j += dj
b += ['    <div id="rq-a" class="clip k" data-start="0" data-duration="7" style="top:250px;font-family:\'Hind HF\';font-size:84px">एक छोटी सी ग़लती...</div>',
      '    <div id="rq-b" class="clip k gold" data-start="1.6" data-duration="5.4" style="top:400px;font-family:\'Teko HF\';font-size:200px;line-height:1">दुनिया बदल सकती है?</div>',
      '    <div id="rq-c" class="clip k teal" data-start="3.8" data-duration="3.2" style="top:690px;font-family:\'Teko HF\';font-size:130px;line-height:1">हाँ · पाँच बार</div>']
j += ['    tl.fromTo("#rq-a",{opacity:0,y:20},{opacity:1,y:0,duration:0.5},0.1);',
      '    tl.fromTo("#rq-b",{opacity:0,scale:1.3,filter:"blur(12px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:0.4,ease:"power4.out"},1.65);',
      '    tl.fromTo("#rq-c",{opacity:0,y:30},{opacity:1,y:0,duration:0.4},3.8);']
C["rq"] = (7, b, j)

order = ["welcome", "topic", "go", "sofort", "qend", "rq"]
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
json.dump({"id": "mod-hf", "name": "mod-hf", "createdAt": "2026-11-25T00:00:00Z"}, open("meta.json", "w"))
print(t, "s total")
