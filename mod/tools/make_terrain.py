#!/usr/bin/env python3
"""AWS Terrain Tiles (terrarium, open data: USGS 3DEP, SRTM, GMTED, ETOPO1 bathymetry) -> heightmap + coloured relief.

  python3 tools/make_terrain.py <name> W E S N Z <palette>      palette: city | sea | plain

Writes assets/3d/<name>/height.bin (float32, half resolution, north row first), meta.json, color.jpg.
"""
import json, math, sys, time, urllib.request
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

name, W, E, S, N, Z, pal = sys.argv[1], *map(float, sys.argv[2:6]), int(sys.argv[6]), sys.argv[7]
out = Path(__file__).resolve().parent.parent / "assets" / "3d" / name; out.mkdir(parents=True, exist_ok=True)
cache = Path(__file__).resolve().parent.parent / "assets" / "tiles"; cache.mkdir(parents=True, exist_ok=True)
tx = lambda lon: (lon + 180) / 360 * 2 ** Z
def ty(lat):
    r = math.radians(lat); return (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 2 ** Z
x0, x1, y0, y1 = int(tx(W)), int(tx(E)), int(ty(N)), int(ty(S))
mos = np.zeros(((y1 - y0 + 1) * 256, (x1 - x0 + 1) * 256), np.float32)
for x in range(x0, x1 + 1):
    for y in range(y0, y1 + 1):
        f = cache / f"{Z}_{x}_{y}.png"
        if not f.exists():
            f.write_bytes(urllib.request.urlopen(f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{Z}/{x}/{y}.png", timeout=60).read()); time.sleep(0.2)
        a = np.asarray(Image.open(f).convert("RGB")).astype(np.float32)
        mos[(y - y0) * 256:(y - y0 + 1) * 256, (x - x0) * 256:(x - x0 + 1) * 256] = a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
px = lambda lon: int((tx(lon) - x0) * 256); py = lambda lat: int((ty(lat) - y0) * 256)
hm = mos[py(N):py(S), px(W):px(E)]
if pal == "city": hm = gaussian_filter(hm, 1.2)
lo, hi = float(hm.min()), float(hm.max())
mpp = 40075016.7 * math.cos(math.radians((N + S) / 2)) / (2 ** Z * 256)
gy, gx = np.gradient(hm, mpp); sl = np.arctan(np.hypot(gx, gy) * (3 if pal != "sea" else 8))
az, alt = math.radians(315), math.radians(40); asp = np.arctan2(-gx, gy)
shade = np.clip(np.sin(alt) * np.cos(sl) + np.cos(alt) * np.sin(sl) * np.cos(az - asp), 0, 1)

def ramp(k, stops):
    c = np.zeros(k.shape + (3,), np.float32)
    for (a0, c0), (a1, c1) in zip(stops, stops[1:]):
        m = (k >= a0) & (k <= a1); f = ((k - a0) / max(a1 - a0, 1e-6))[m][:, None]
        c[m] = np.array(c0) * (1 - f) + np.array(c1) * f
    return c
if pal == "sea":       # bathymetry blues below 0, greens/ochres above
    sea = hm < 0
    kd = np.clip(-hm / 6000, 0, 1); kl = np.clip(hm / 1500, 0, 1)
    col = np.where(sea[..., None], ramp(kd, [(0, (96, 196, 214)), (0.05, (52, 140, 186)), (0.4, (22, 70, 128)), (1, (8, 24, 60))]),
                   ramp(kl, [(0, (98, 150, 84)), (0.3, (128, 140, 82)), (0.7, (150, 126, 90)), (1, (220, 214, 200))]))
    rgb = col * np.where(sea[..., None], 0.75 + 0.35 * shade[..., None], 0.45 + 0.75 * shade[..., None])
else:
    k = (hm - lo) / max(hi - lo, 1e-6)
    stops = [(0, (92, 108, 84)), (0.25, (104, 124, 82)), (0.55, (118, 130, 88)), (0.8, (140, 128, 98)), (1, (196, 188, 170))] if pal == "city" else \
            [(0, (70, 82, 74)), (0.5, (86, 98, 82)), (1, (128, 132, 112))]
    rgb = ramp(k, stops) * (0.45 + 0.75 * shade[..., None])
Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).save(out / "color.jpg", quality=92)
half = np.asarray(Image.fromarray(hm).resize((hm.shape[1] // 2, hm.shape[0] // 2), Image.BILINEAR), np.float32)
half.astype("<f4").tofile(out / "height.bin")
meta = dict(W=W, E=E, S=S, N=N, z=Z, min=lo, max=hi, w=hm.shape[1], h=hm.shape[0], mpp=mpp, bw=half.shape[1], bh=half.shape[0],
            source="AWS Terrain Tiles (terrarium): USGS 3DEP, SRTM, GMTED2010, ETOPO1 — open data")
(out / "meta.json").write_text(json.dumps(meta, indent=1)); print(name, json.dumps(meta))
