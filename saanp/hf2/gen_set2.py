"""Second set of HyperFrames motion graphics for saanp: writes compositions/*.html and index_set2.html.

  python3 gen_set2.py   then render index_set2.html (see the film's README notes in CLAUDE.md)
"""
import json
import pathlib

C = pathlib.Path("compositions")
FONTS = '''@font-face{font-family:"Teko HF";src:url("assets/fonts/cond.ttf");}
@font-face{font-family:"Hind HF";src:url("assets/fonts/label.ttf");}
@font-face{font-family:"Hind HF Light";src:url("assets/fonts/labelm.ttf");}
@font-face{font-family:"Tiro HF";src:url("assets/fonts/serif.ttf");}'''
BASE = '''#root{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,#1d1716 0%,#0b0909 62%,#050404 100%);overflow:hidden;color:#f3ede4;}
.k{position:absolute;left:0;right:0;text-align:center;}
.red{color:#d8322a;}
.src{position:absolute;left:0;right:0;bottom:120px;text-align:center;font-family:"Hind HF Light";font-size:34px;color:#b9b0a4;}'''


def comp(cid, body, js):
    return f'''<template>
  <style>
{FONTS}
{BASE}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
'''


S = {}

# 1. the target moves from Afghanistan to Kashmir
S["target"] = (5, '''    <div id="target-a" class="clip" data-start="0" data-duration="5" style="position:absolute;left:300px;top:470px;font-family:'Teko HF';font-size:120px;color:#8d857a">अफ़ग़ानिस्तान</div>
    <div id="target-b" class="clip" data-start="0" data-duration="5" style="position:absolute;left:1260px;top:470px;font-family:'Teko HF';font-size:120px;color:#8d857a">कश्मीर</div>
    <svg id="target-x" class="clip" data-start="0" data-duration="5" style="position:absolute;left:0;top:0" width="1920" height="1080"><g id="target-g"><circle cx="0" cy="0" r="120" fill="none" stroke="#d8322a" stroke-width="8"/><circle cx="0" cy="0" r="60" fill="none" stroke="#d8322a" stroke-width="5"/><line x1="-170" y1="0" x2="-70" y2="0" stroke="#d8322a" stroke-width="7"/><line x1="70" y1="0" x2="170" y2="0" stroke="#d8322a" stroke-width="7"/><line x1="0" y1="-170" x2="0" y2="-70" stroke="#d8322a" stroke-width="7"/><line x1="0" y1="70" x2="0" y2="170" stroke="#d8322a" stroke-width="7"/></g></svg>
    <div id="target-c" class="clip k" data-start="2.8" data-duration="2.2" style="top:760px;font-family:'Hind HF';font-size:58px">नया निशाना</div>''',
'''    tl.fromTo("#target-g",{x:560,y:520,scale:1.6,opacity:0},{x:560,y:520,scale:1,opacity:1,duration:0.4,ease:"power3.out"},0.1);
    tl.fromTo("#target-g",{x:560},{x:1440,duration:1.4,ease:"power2.inOut",immediateRender:false},1.1);
    tl.fromTo("#target-g",{rotation:0},{rotation:90,duration:1.4,ease:"power2.inOut",immediateRender:false},1.1);
    tl.fromTo("#target-a",{opacity:1},{opacity:0.25,duration:0.6},1.2);
    tl.fromTo("#target-b",{color:"#8d857a",scale:1},{color:"#f3ede4",scale:1.12,duration:0.3,ease:"power3.out"},2.5);
    tl.fromTo("#target-c",{opacity:0,y:20},{opacity:1,y:0,duration:0.4},2.8);''')

# 2. the Lashkar network
nodes = [("letn1", "मुख्यालय: मुरीदके", 420, 250), ("letn2", "फ्रंट: जमात-उद-दावा", 1500, 250),
         ("letn3", "संस्थापक: हाफ़िज़ सईद", 420, 830), ("letn4", "UN: प्रतिबंधित संगठन", 1500, 830)]
body = '    <svg id="let-lines" class="clip" data-start="0" data-duration="6" style="position:absolute;inset:0" width="1920" height="1080">'
body += "".join(f'<line id="{n}-l" x1="960" y1="540" x2="{x}" y2="{y}" stroke="#d8322a" stroke-width="5"/>' for n, _, x, y in nodes) + "</svg>\n"
body += '''    <div id="let-c" class="clip" data-start="0" data-duration="6" style="position:absolute;left:640px;top:450px;width:640px;height:180px;background:#2a1b19;border:4px solid #d8322a;display:flex;align-items:center;justify-content:center;font-family:'Teko HF';font-size:92px">लश्कर-ए-तैयबा</div>\n'''
js = '    tl.fromTo("#let-c",{opacity:0,scale:1.3},{opacity:1,scale:1,duration:0.35,ease:"power4.out"},0.1);\n'
for k, (n, t, x, y) in enumerate(nodes):
    body += f'''    <div id="{n}" class="clip" data-start="0" data-duration="6" style="position:absolute;left:{x - 270}px;top:{y - 50}px;width:540px;height:100px;background:#e8e1d6;color:#151111;display:flex;align-items:center;justify-content:center;font-family:'Hind HF';font-size:44px;border-radius:8px">{t}</div>\n'''
    js += f'    tl.fromTo("#{n}-l",{{strokeDasharray:800,strokeDashoffset:800}},{{strokeDashoffset:0,duration:0.5,ease:"power2.out"}},{0.7 + k * 0.7});\n'
    js += f'    tl.fromTo("#{n}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{1.0 + k * 0.7});\n'
S["letnet"] = (6, body, js)

# 3. sixty hours
S["hours"] = (5, '''    <div id="hours-n" class="clip k" data-start="0" data-duration="5" style="top:300px;font-family:'Teko HF';font-size:330px;line-height:1">≈ 60</div>
    <div id="hours-u" class="clip k" data-start="0" data-duration="5" style="top:640px;font-family:'Hind HF';font-size:64px">घंटे · मुंबई बंधक</div>
    <div id="hours-bar" class="clip" data-start="0" data-duration="5" style="position:absolute;left:460px;top:780px;width:1000px;height:14px;background:#3a302c"><div id="hours-fill" style="width:100%;height:100%;background:#d8322a;transform-origin:0 50%;transform:scaleX(0)"></div></div>
    <div id="hours-s" class="clip src" data-start="0.5" data-duration="4.5">26 से 29 नवंबर 2008</div>''',
'''    tl.fromTo("#hours-n",{opacity:0,scale:1.3},{opacity:1,scale:1,duration:0.4,ease:"power4.out"},0.1);
    tl.fromTo("#hours-fill",{scaleX:0},{scaleX:1,duration:3.2,ease:"power2.out"},0.2);
    tl.fromTo("#hours-u",{opacity:0},{opacity:1,duration:0.4},0.3);''')

# 4. Headley's testimony, typed out
txt = 'गवाह ने कहा: ISI का एक अफ़सर, "मेजर इक़बाल", उसका हैंडलर था।'
S["headley"] = (6, f'''    <div id="headley-p" class="clip" data-start="0" data-duration="6" style="position:absolute;left:220px;top:240px;width:1480px;height:600px;background:#ece5d8;border-radius:6px"></div>
    <div id="headley-h" class="clip" data-start="0" data-duration="6" style="position:absolute;left:300px;top:290px;font-family:'Tiro HF';font-size:42px;color:#5a514a">अमेरिकी अदालत · शिकागो · 2011 · गवाही का सार</div>
    <div id="headley-t" class="clip" data-start="0" data-duration="6" style="position:absolute;left:300px;top:400px;width:1320px;font-family:'Hind HF';font-size:68px;line-height:1.5;color:#1b1614;clip-path:inset(0 100% 0 0)">{txt}</div>
    <div id="headley-m" class="clip" data-start="0" data-duration="6" style="position:absolute;left:300px;top:690px;font-family:'Hind HF Light';font-size:40px;color:#5a514a">— डेविड हेडली (उसके अपने बयान के मुताबिक़)</div>''',
'''    tl.fromTo("#headley-p",{opacity:0,y:30},{opacity:1,y:0,duration:0.4,ease:"power3.out"},0);
    tl.fromTo("#headley-h",{opacity:0},{opacity:1,duration:0.4},0.1);
    tl.fromTo("#headley-t",{clipPath:"inset(0 100% 0 0)"},{clipPath:"inset(0 0% 0 0)",duration:2.6,ease:"steps(40)"},0.5);
    tl.fromTo("#headley-m",{opacity:0},{opacity:1,duration:0.5},3.2);''')

# 5. the snake turns back on its own house (no title card)
S["turn"] = (6, '''    <div id="turn-a" class="clip" data-start="0" data-duration="6" style="position:absolute;left:1350px;top:300px;font-family:'Teko HF';font-size:110px;color:#8d857a">पड़ोसी</div>
    <div id="turn-b" class="clip" data-start="0" data-duration="6" style="position:absolute;left:300px;top:300px;font-family:'Teko HF';font-size:110px;color:#8d857a">घर</div>
    <svg id="turn-s" class="clip" data-start="0" data-duration="6" style="position:absolute;inset:0" width="1920" height="1080"><path id="turn-p" d="M420 560 C 700 420, 900 700, 1180 560 S 1500 460, 1460 620 S 1100 820, 820 760 S 520 640, 460 470" fill="none" stroke="#d8322a" stroke-width="14" stroke-linecap="round"/></svg>
    <div id="turn-c" class="clip k" data-start="3.2" data-duration="2.8" style="top:860px;font-family:'Hind HF';font-size:62px">साँप पलटकर घर को डसने लगे</div>''',
'''    tl.fromTo("#turn-p",{strokeDasharray:2600,strokeDashoffset:2600},{strokeDashoffset:0,duration:3.0,ease:"power1.inOut"},0.2);
    tl.fromTo("#turn-a",{color:"#8d857a"},{color:"#f3ede4",duration:0.3},1.0);
    tl.fromTo("#turn-b",{color:"#8d857a",scale:1},{color:"#d8322a",scale:1.2,duration:0.3,ease:"power3.out"},3.1);
    tl.fromTo("#turn-c",{opacity:0,y:20},{opacity:1,y:0,duration:0.4},3.2);''')

# 6. the money trail
acc = [(300, 300), (300, 780), (960, 540), (1620, 300), (1620, 780)]
links = [(0, 2), (1, 2), (2, 3), (2, 4)]
body = '    <svg id="money-l" class="clip" data-start="0" data-duration="6" style="position:absolute;inset:0" width="1920" height="1080">'
for k, (a, b) in enumerate(links):
    (x0, y0), (x1, y1) = acc[a], acc[b]
    body += f'<line id="money-ln{k}" x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#8d857a" stroke-width="4" stroke-dasharray="14 10"/>'
body += "</svg>\n"
for k, (x, y) in enumerate(acc):
    lab, w = ("ट्रस्ट / चैरिटी", 380) if k == 2 else ("?", 200)
    body += f'''    <div id="money-a{k}" class="clip" data-start="0" data-duration="6" style="position:absolute;left:{x - w // 2}px;top:{y - 55}px;width:{w}px;height:110px;background:#e8e1d6;color:#151111;display:flex;align-items:center;justify-content:center;font-family:'Hind HF';font-size:44px;border-radius:10px">{lab}</div>\n'''
for k in range(8):
    body += f'    <div id="money-d{k}" class="clip" data-start="0" data-duration="6" style="position:absolute;left:0;top:0;width:26px;height:26px;border-radius:50%;background:#d8a62a"></div>\n'
body += '''    <div id="money-t" class="clip k" data-start="2.6" data-duration="3.4" style="top:960px;font-family:'Hind HF';font-size:52px">दुनिया ने पैसों का पीछा किया</div>\n'''
js = '''    for (let k=0;k<5;k++) tl.fromTo("#money-a"+k,{opacity:0,scale:0.8},{opacity:1,scale:1,duration:0.3},0.1+k*0.12);
    for (let k=0;k<4;k++) tl.fromTo("#money-ln"+k,{opacity:0},{opacity:1,duration:0.3},0.6+k*0.1);
'''
for k in range(8):
    a, b = links[k % 4]; (x0, y0), (x1, y1) = acc[a], acc[b]
    js += f'    tl.fromTo("#money-d{k}",{{x:{x0 - 13},y:{y0 - 13},opacity:0}},{{x:{x1 - 13},y:{y1 - 13},opacity:1,duration:1.1,ease:"none"}},{0.9 + k * 0.35});\n'
js += '    tl.fromTo("#money-t",{opacity:0},{opacity:1,duration:0.4},2.6);'
S["money"] = (6, body, js)

# 7. forty figures
figs = "".join(f'<div id="forty-f{i}" class="clip" data-start="0" data-duration="6" style="position:absolute;left:{360 + (i % 10) * 125}px;top:{230 + (i // 10) * 150}px;width:60px;height:120px"><div style="width:40px;height:40px;border-radius:50%;background:#f3ede4;margin:0 auto"></div><div style="width:60px;height:70px;background:#f3ede4;border-radius:26px 26px 6px 6px;margin-top:6px"></div></div>' for i in range(40))
S["forty"] = (6, f'''    {figs}
    <div id="forty-t" class="clip k" data-start="2.8" data-duration="3.2" style="top:860px;font-family:'Teko HF';font-size:110px;line-height:1">40 जवान · पुलवामा</div>''',
'''    for (let i=0;i<40;i++) tl.fromTo("#forty-f"+i,{opacity:0,y:20},{opacity:0.92,y:0,duration:0.2},0.2+i*0.06);
    tl.fromTo("#forty-t",{opacity:0,scale:1.2},{opacity:1,scale:1,duration:0.35,ease:"power4.out"},2.8);''')

# 8. thousands of armed men: a field of dots
dots = "".join(f'<div id="many-d{i}" class="clip" data-start="0" data-duration="7" style="position:absolute;left:{140 + (i % 40) * 41}px;top:{150 + (i // 40) * 41}px;width:22px;height:22px;border-radius:50%;background:#d8322a"></div>' for i in range(400))
S["many"] = (7, f'''    {dots}
    <div id="many-n" class="clip k" data-start="0" data-duration="7" style="top:620px;font-family:'Teko HF';font-size:200px;line-height:1;text-shadow:0 8px 30px #000">30,000 – 40,000</div>
    <div id="many-t" class="clip k" data-start="0" data-duration="7" style="top:840px;font-family:'Hind HF';font-size:54px">हथियारबंद लोग, अब भी पाकिस्तान में · इमरान ख़ान, 2019</div>
    <div id="many-k" class="clip src" data-start="0" data-duration="7" style="bottom:60px">हर बिंदु ≈ 100 लोग</div>''',
'''    for (let i=0;i<400;i++) tl.fromTo("#many-d"+i,{opacity:0,scale:0},{opacity:0.85,scale:1,duration:0.12},0.1+i*0.0075);
    tl.fromTo("#many-n",{opacity:0,scale:1.2},{opacity:1,scale:1,duration:0.4,ease:"power4.out"},2.6);
    tl.fromTo("#many-t",{opacity:0},{opacity:1,duration:0.4},3.0);
    tl.fromTo("#many-k",{opacity:0},{opacity:1,duration:0.4},1.0);''')

# 9. 132 candles
cand = "".join(f'<div id="cand-c{i}" class="clip" data-start="0" data-duration="7" style="position:absolute;left:{170 + (i % 22) * 72}px;top:{230 + (i // 22) * 90}px;width:16px;height:46px"><div style="width:16px;height:24px;border-radius:50% 50% 45% 45%;background:radial-gradient(#fff3c0,#ffb040 60%,rgba(255,120,30,0))"></div><div style="width:10px;height:22px;margin:0 auto;background:#e8e1d6"></div></div>' for i in range(132))
S["candles"] = (7, f'''    {cand}
    <div id="cand-t" class="clip k" data-start="0" data-duration="7" style="top:860px;font-family:'Teko HF';font-size:110px;line-height:1">132 बच्चे</div>
    <div id="cand-s" class="clip src" data-start="0" data-duration="7" style="bottom:50px">आर्मी पब्लिक स्कूल, पेशावर · 16 दिसंबर 2014</div>''',
'''    for (let i=0;i<132;i++) tl.fromTo("#cand-c"+i,{opacity:0},{opacity:1,duration:0.25},0.2+i*0.025);
    tl.fromTo("#cand-t",{opacity:0},{opacity:1,duration:0.6},3.6);
    tl.fromTo("#cand-s",{opacity:0},{opacity:1,duration:0.6},3.9);''')

ORDER = ["target", "letnet", "hours", "headley", "turn", "money", "forty", "many", "candles"]
t = 0; hosts = []; segs = []
for cid in ORDER:
    dur, body, js = S[cid]
    (C / f"{cid}.html").write_text(comp(cid, body, js))
    hosts.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{t}" data-duration="{dur}" data-track-index="0" data-track-kind="graphics" data-width="1920" data-height="1080"></div>')
    segs.append({"id": cid, "start": t, "end": t + dur}); t += dur
head = open("index.html").read().split('<div id="root"')[0]
html = head + f'''<div id="root" data-composition-id="main" data-start="0" data-duration="{t}" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
'''
open("index_set2.html", "w").write(html)
json.dump(segs, open("segments2.json", "w"), indent=1)
print(t, ORDER)
