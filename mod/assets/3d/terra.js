// Terrain helpers for the mod 3D maps: AWS Terrain Tiles heights + coloured relief, draped lines, pins, fills.
import * as THREE from 'three';
import { clamp, ease, ramp } from './common.js';
export async function terrain(S, dir, center, { exg = 2.0, seg = [400, 300], km = 1, tint = null } = {}) {
  const meta = await (await fetch(dir + '/meta.json')).json();
  const H = new Float32Array(await (await fetch(dir + '/height.bin')).arrayBuffer());
  const tex = await new THREE.TextureLoader().loadAsync(dir + '/color.jpg'); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const KM = meta.mpp * 2 / 1000 / km;                // world units per height.bin pixel (km / km)
  const WX = meta.bw * KM, WZ = meta.bh * KM;
  const mx = lon => (lon + 180) / 360, my = lat => { const r = lat * Math.PI / 180; return (1 - Math.log(Math.tan(r) + 1 / Math.cos(r)) / Math.PI) / 2; };
  const u = lon => (mx(lon) - mx(meta.W)) / (mx(meta.E) - mx(meta.W)), v = lat => (my(lat) - my(meta.N)) / (my(meta.S) - my(meta.N));
  const ox = u(center[1]) * WX, oz = v(center[0]) * WZ;
  const hAt = (x, z) => {
    const fx = clamp((x + ox) / KM, 0, meta.bw - 1.001), fz = clamp((z + oz) / KM, 0, meta.bh - 1.001);
    const i = Math.floor(fx), j = Math.floor(fz), a = fx - i, b = fz - j, w = meta.bw;
    const h = H[j * w + i] * (1 - a) * (1 - b) + H[j * w + i + 1] * a * (1 - b) + H[(j + 1) * w + i] * (1 - a) * b + H[(j + 1) * w + i + 1] * a * b;
    return (Math.max(h, meta.seaClamp ?? -1e9) - meta.min) / 1000 / km * exg;
  };
  const P = (lat, lon, up = 0) => { const x = u(lon) * WX - ox, z = v(lat) * WZ - oz; return new THREE.Vector3(x, hAt(x, z) + up, z); };
  const geo = new THREE.PlaneGeometry(WX, WZ, seg[0], seg[1]); geo.rotateX(-Math.PI / 2); geo.translate(WX / 2 - ox, 0, WZ / 2 - oz);
  const pos = geo.attributes.position; for (let i = 0; i < pos.count; i++) pos.setY(i, hAt(pos.getX(i), pos.getZ(i)));
  geo.computeVertexNormals();
  const mat = new THREE.MeshStandardMaterial({ map: tex, roughness: 0.95, metalness: 0 }); if (tint) mat.color.setHex(tint);
  const land = new THREE.Mesh(geo, mat); land.receiveShadow = true; S.add(land);
  function drapedPath(pts, up = 0.06, close = false, n = 400) {
    const vs = pts.map(p => P(p[0], p[1])); if (close) vs.push(vs[0].clone());
    const c = new THREE.CatmullRomCurve3(vs, false, 'catmullrom', 0.0), out = [];
    for (let i = 0; i <= n; i++) { const q = c.getPoint(i / n); q.y = hAt(q.x, q.z) + up; out.push(q); }
    return out;
  }
  function tube(points, r, m) {
    const c = new THREE.CatmullRomCurve3(points), g = new THREE.TubeGeometry(c, points.length, r, 6, false);
    const t = new THREE.Mesh(g, m.clone()); t.userData.n = g.index.count; t.userData.curve = c; g.setDrawRange(0, 0); S.add(t); return t;
  }
  function fillPoly(pts, color, op, up = 0.05) {
    const vs = pts.map(p => P(p[0], p[1]));
    const xs = vs.map(q => q.x), zs = vs.map(q => q.z), x0 = Math.min(...xs) - 0.5, x1 = Math.max(...xs) + 0.5, z0 = Math.min(...zs) - 0.5, z1 = Math.max(...zs) + 0.5;
    const c = document.createElement('canvas'); c.width = c.height = 1024; const g = c.getContext('2d');
    g.fillStyle = '#fff'; g.beginPath(); vs.forEach((q, i) => { const X = (q.x - x0) / (x1 - x0) * 1024, Y = (q.z - z0) / (z1 - z0) * 1024; i ? g.lineTo(X, Y) : g.moveTo(X, Y); }); g.closePath(); g.fill();
    const t = new THREE.CanvasTexture(c);
    const gg = new THREE.PlaneGeometry(x1 - x0, z1 - z0, 96, 96); gg.rotateX(-Math.PI / 2); gg.translate((x0 + x1) / 2, 0, (z0 + z1) / 2);
    const p = gg.attributes.position; for (let i = 0; i < p.count; i++) p.setY(i, hAt(p.getX(i), p.getZ(i)) + up);
    const m = new THREE.Mesh(gg, new THREE.MeshBasicMaterial({ color, alphaMap: t, transparent: true, opacity: 0, depthWrite: false, fog: false }));
    m.userData.op = op; S.add(m); return m;
  }
  function pin(lat, lon, m, s = 1) {
    const g = new THREE.Group(), base = P(lat, lon);
    const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.05 * s, 0.05 * s, 2.2 * s, 8), m.clone()); stem.position.y = 1.1 * s;
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.28 * s, 16, 12), m.clone()); head.position.y = 2.3 * s;
    const ring = new THREE.Mesh(new THREE.RingGeometry(0.4 * s, 0.6 * s, 32), m.clone()); ring.rotation.x = -Math.PI / 2; ring.position.y = 0.05;
    g.add(stem, head, ring); g.position.copy(base); g.scale.setScalar(0.001); S.add(g); g.userData.top = base.clone().add(new THREE.Vector3(0, 2.9 * s, 0)); return g;
  }
  return { meta, land, mat, hAt, P, drapedPath, tube, fillPoly, pin, WX, WZ };
}
export const drawTube = (t, k) => { t.visible = k > 0.001; t.geometry.setDrawRange(0, Math.floor(t.userData.n * clamp(k))); };
export const showPin = (g, t, tin, tout = 1e9) => { const k = ease(ramp(t, tin, 0.5)) * (1 - ramp(t, tout, 0.3)); g.scale.setScalar(Math.max(0.001, k)); g.visible = k > 0.002; };
export function sky(S, top, mid, low) {
  const m = new THREE.Mesh(new THREE.SphereGeometry(900, 32, 16), new THREE.ShaderMaterial({ side: THREE.BackSide, depthWrite: false, fog: false,
    uniforms: { top: { value: new THREE.Color(top) }, mid: { value: new THREE.Color(mid) }, low: { value: new THREE.Color(low) }, k: { value: 1 } },
    vertexShader: 'varying vec3 p; void main(){ p = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }',
    fragmentShader: 'uniform vec3 top,mid,low; uniform float k; varying vec3 p; void main(){ float y=p.y; vec3 c = y>0.12 ? mix(mid,top,clamp((y-.12)/.5,0.,1.)) : mix(low,mid,clamp(y/.12,0.,1.)); gl_FragColor=vec4(c*k,1.); }' }));
  S.add(m); return m;
}
// camera along shots: [[t0, [pos,target], [pos,target]], ..., [tEnd]]
export function shotCam(cam, SHOTS, t) {
  let i = 0; while (i < SHOTS.length - 2 && t >= SHOTS[i + 1][0]) i++;
  const [t0, a, b] = SHOTS[i], t1 = SHOTS[i + 1][0], k = ease(clamp((t - t0) / (t1 - t0)));
  cam.position.lerpVectors(a[0], b[0], k); cam.lookAt(a[1].clone().lerp(b[1], k)); return i;
}
