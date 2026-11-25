#!/usr/bin/env python3
"""Fetch AWS Terrain Tiles (terrarium) around Groom Lake and write a heightmap + a coloured relief texture.

Output: assets/terrain/height.png (16-bit grey, metres = min + v/65535*(max-min)), meta.json, color.jpg.
Data: AWS Terrain Tiles (Mapzen), USGS 3DEP/NED and SRTM: public domain / open data.
"""
import io, json, math, time, urllib.request
from pathlib import Path
import numpy as np
from PIL import Image

Z = 11
W, E, S, N = -116.40, -115.20, 36.80, 37.70
out = Path(__file__).resolve().parent.parent / "assets" / "terrain"; out.mkdir(parents=True, exist_ok=True)
cache = out / "tiles"; cache.mkdir(exist_ok=True)

def tx(lon): return (lon + 180) / 360 * 2 ** Z
def ty(lat):
    r = math.radians(lat); return (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 2 ** Z

x0, x1, y0, y1 = int(tx(W)), int(tx(E)), int(ty(N)), int(ty(S))
mos = np.zeros(((y1 - y0 + 1) * 256, (x1 - x0 + 1) * 256), np.float32)
for x in range(x0, x1 + 1):
    for y in range(y0, y1 + 1):
        f = cache / f"{Z}_{x}_{y}.png"
        if not f.exists():
            url = f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{Z}/{x}/{y}.png"
            f.write_bytes(urllib.request.urlopen(url, timeout=60).read()); time.sleep(0.2)
        a = np.asarray(Image.open(f).convert("RGB")).astype(np.float32)
        h = a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
        mos[(y - y0) * 256:(y - y0 + 1) * 256, (x - x0) * 256:(x - x0 + 1) * 256] = h
# crop to the exact box
px = lambda lon: int((tx(lon) - x0) * 256); py = lambda lat: int((ty(lat) - y0) * 256)
hm = mos[py(N):py(S), px(W):px(E)]
lo, hi = float(hm.min()), float(hm.max())
Image.fromarray(((hm - lo) / (hi - lo) * 65535).astype(np.uint16)).save(out / "height.png")
# metres per pixel (ground)
lat_c = (N + S) / 2
mpp = 40075016.7 * math.cos(math.radians(lat_c)) / (2 ** Z * 256)
meta = dict(W=W, E=E, S=S, N=N, z=Z, min=lo, max=hi, w=hm.shape[1], h=hm.shape[0], mpp=mpp,
            note="Web-Mercator crop; lat->row is Mercator, lon->col linear")
(out / "meta.json").write_text(json.dumps(meta, indent=1))

# coloured relief: desert ramp by height + hillshade + pale playas (flat and low)
gy, gx = np.gradient(hm, mpp)
slope = np.hypot(gx, gy)
az, alt = math.radians(315), math.radians(38)
asp = np.arctan2(-gx, gy)
shade = np.sin(alt) * np.cos(np.arctan(slope)) + np.cos(alt) * np.sin(np.arctan(slope)) * np.cos(az - asp)
shade = np.clip(shade, 0, 1)
k = (hm - lo) / (hi - lo)
stops = [(0.00, (196, 150, 98)), (0.25, (176, 124, 78)), (0.45, (142, 100, 66)), (0.65, (110, 84, 62)),
         (0.82, (92, 88, 78)), (1.00, (214, 208, 196))]
col = np.zeros(hm.shape + (3,), np.float32)
for (a0, c0), (a1, c1) in zip(stops, stops[1:]):
    m = (k >= a0) & (k <= a1); f = ((k - a0) / (a1 - a0))[m][:, None]
    col[m] = np.array(c0) * (1 - f) + np.array(c1) * f
# playa: very flat and in a basin floor -> pale salt white
from PIL import ImageFilter
from scipy.ndimage import maximum_filter, minimum_filter, binary_opening, binary_closing, gaussian_filter
rng = maximum_filter(hm, 9) - minimum_filter(hm, 9)
playa = (rng < 6) & (hm < minimum_filter(hm, 161) + 10)
playa = binary_closing(binary_opening(playa, iterations=2), iterations=4)
pl = gaussian_filter(playa.astype(np.float32), 2.5)[..., None]
col = col * (1 - pl) + np.array([236, 230, 214]) * pl
rgb = col * (0.42 + 0.78 * shade[..., None])
rgb = np.clip(rgb, 0, 255).astype(np.uint8)
Image.fromarray(rgb).save(out / "color.jpg", quality=92)
print(json.dumps(meta))

# half-resolution float32 heights for the three.js page (row-major, north row first)
half = np.asarray(Image.fromarray(hm).resize((hm.shape[1] // 2, hm.shape[0] // 2), Image.BILINEAR), np.float32)
half.astype("<f4").tofile(out / "height.bin")
meta.update(bw=half.shape[1], bh=half.shape[0]); (out / "meta.json").write_text(json.dumps(meta, indent=1))
