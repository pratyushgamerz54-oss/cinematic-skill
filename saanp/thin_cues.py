"""Thin the auto sound cues for a documentary pace: fewer whooshes and pops, softer.

  python3 saanp/thin_cues.py saanp/sfx_cues.json   (run after render.py --cues, before build_sfx.py)
"""
import json, sys

p = sys.argv[1]
d = json.load(open(p))
cues = d["cues"] if isinstance(d, dict) else d
keep, last = [], {}
GAP = {"whoosh": 5.0, "pop": 2.0}
for c in sorted(cues, key=lambda c: c["t"]):
    k = c["type"]
    if k in GAP:
        if c["t"] - last.get(k, -99) < GAP[k]:
            continue
        c["gain"] = round(c["gain"] * (0.6 if k == "whoosh" else 0.7), 2)
    last[k] = c["t"]; keep.append(c)
if isinstance(d, dict): d["cues"] = keep
else: d = keep
json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
print(f"{p}: {len(cues)} -> {len(keep)} cues")
