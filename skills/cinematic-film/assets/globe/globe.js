// A 3D globe shot for cinematic-film, recorded frame by frame with frame-capture.
//
// make_globe.py writes config.json and the textures next to this file, then records
// index.html?record=1. Everything moves on one clock T (seconds): fills fade in, routes draw on
// along great circles, markers pop with their labels, and the camera flies between keys.
// Under the recorder, window.__recordFrame(t) sets T before each frame; in a normal browser
// T follows performance.now(), so the page also plays as a preview.
import * as THREE from 'three';

const cfg = await (await fetch('config.json')).json();
const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = cfg.exposure ?? 1.05;

const scene = new THREE.Scene();
scene.background = new THREE.Color(...cfg.background.map(v => v / 255));
const camera = new THREE.PerspectiveCamera(cfg.fov ?? 32, 16 / 9, 0.01, 200);

// ---------------------------------------------------------------- helpers
const D2R = Math.PI / 180;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const ramp = (t, t0, d) => clamp((t - t0) / Math.max(d, 1e-6));
const easeInOut = x => x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const easeOutBack = (x, s = 1.6) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2);
function ll(lat, lon, r = 1) {             // matches three's SphereGeometry UVs for an equirectangular map
  const phi = (90 - lat) * D2R, th = (lon + 180) * D2R;
  return new THREE.Vector3(-r * Math.sin(phi) * Math.cos(th), r * Math.cos(phi), r * Math.sin(phi) * Math.sin(th));
}
const place = p => (typeof p === 'string' ? cfg.places[p] : p);
const fade = (t, tin, tout, d = 0.4) => ramp(t, tin, d) * (tout == null ? 1 : 1 - ramp(t, tout, d));

// ---------------------------------------------------------------- the globe and its fills
const loader = new THREE.TextureLoader();
const loadTex = url => new Promise((ok, err) => loader.load(url, tx => { tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8; ok(tx); }, undefined, err));
const sphere = new THREE.SphereGeometry(1, 192, 128);
const globe = new THREE.Mesh(sphere, new THREE.MeshStandardMaterial({ map: await loadTex('textures/base.png'), roughness: 0.92, metalness: 0 }));
scene.add(globe);
const fills = [];
for (let i = 0; i < cfg.fills.length; i++) {
  const f = cfg.fills[i];
  const m = new THREE.MeshStandardMaterial({ map: await loadTex(`textures/fill_${i}.png`), transparent: true, depthWrite: false, roughness: 0.9, opacity: 0 });
  const mesh = new THREE.Mesh(sphere, m); mesh.scale.setScalar(1.0008 + i * 0.0002); mesh.renderOrder = 1 + i;
  scene.add(mesh); fills.push({ f, m });
}

// atmosphere: a back-face shell that glows at the limb
const atmo = new THREE.Mesh(new THREE.SphereGeometry(1.0, 96, 64), new THREE.ShaderMaterial({
  side: THREE.BackSide, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  uniforms: { uColor: { value: new THREE.Color(...cfg.atmosphere.map(v => v / 255)) } },
  vertexShader: 'varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix * vec4(position,1.0); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }',
  fragmentShader: 'uniform vec3 uColor; varying vec3 vN; varying vec3 vV; void main(){ float k = pow(clamp(1.0 + dot(vN, vV) * 1.0, 0.0, 1.0), 3.0); gl_FragColor = vec4(uColor * k * 1.4, k); }',
}));
atmo.scale.setScalar(1.12); scene.add(atmo);

// stars
if (cfg.stars) {
  const n = 2600, pos = new Float32Array(n * 3); let s = 7;
  const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  for (let i = 0; i < n; i++) { const v = new THREE.Vector3(rnd() - 0.5, rnd() - 0.5, rnd() - 0.5).normalize().multiplyScalar(60 + rnd() * 30); pos.set([v.x, v.y, v.z], i * 3); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: 0xcfd8e6, size: 0.12, sizeAttenuation: true, transparent: true, opacity: 0.8 })));
}

// light: a soft key from over the camera's shoulder, so the side we look at is always lit
scene.add(new THREE.HemisphereLight(0xffffff, 0x22262e, 1.1));
const key = new THREE.DirectionalLight(0xfff4e6, 2.0); scene.add(key);

// ---------------------------------------------------------------- routes (great-circle arcs that draw on)
const routeCol = new THREE.Color(...(cfg.route_rgb || [255, 250, 240]).map(v => v / 255));
const routes = cfg.routes.map(r => {
  const a = ll(...place(r.from)), b = ll(...place(r.to));
  const ang = a.angleTo(b), h = r.height ?? Math.min(0.25, 0.05 + ang * 0.18);
  const pts = [];
  for (let i = 0; i <= 96; i++) {
    const u = i / 96, q = new THREE.Vector3().copy(a).applyAxisAngle(new THREE.Vector3().crossVectors(a, b).normalize(), ang * u);
    pts.push(q.multiplyScalar(1.002 + h * Math.sin(Math.PI * u)));
  }
  const curve = new THREE.CatmullRomCurve3(pts);
  const geo = new THREE.TubeGeometry(curve, 240, r.width ?? 0.0045, 8, false);
  const mesh = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: routeCol, transparent: true }));
  mesh.renderOrder = 20; scene.add(mesh);
  const head = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex(), color: routeCol, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
  head.scale.setScalar(0.06); head.renderOrder = 21; scene.add(head);
  return { r, mesh, geo, curve, head, total: geo.index.count };
});

function glowTex() {
  if (glowTex.t) return glowTex.t;
  const c = document.createElement('canvas'); c.width = c.height = 128;
  const g = c.getContext('2d'), gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.25, 'rgba(255,255,255,0.7)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
  return (glowTex.t = new THREE.CanvasTexture(c));
}

// ---------------------------------------------------------------- markers with labels
await document.fonts.load('64px GlobeLabel', 'अ A');
function labelSprite(text, side) {
  const fs = 72, pad = 26, c = document.createElement('canvas'), g = c.getContext('2d');
  g.font = `600 ${fs}px GlobeLabel, sans-serif`;
  const w = Math.ceil(g.measureText(text).width) + pad * 2, h = Math.ceil(fs * 1.55);
  c.width = w; c.height = h;
  g.font = `600 ${fs}px GlobeLabel, sans-serif`; g.textBaseline = 'middle';
  g.fillStyle = 'rgba(12,12,14,0.72)'; roundRect(g, 0, 0, w, h, 14); g.fill();
  g.fillStyle = '#fbf8f1'; g.fillText(text, pad, h * 0.54);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tx, transparent: true, depthTest: false }));
  sp.center.set(side === 'left' ? 1.08 : -0.08, 0.5);
  sp.userData.aspect = w / h; sp.renderOrder = 40;
  return sp;
}
function roundRect(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
const markers = cfg.markers.map(m => {
  const p = ll(...place(m.place), 1.003);
  const dot = new THREE.Mesh(new THREE.SphereGeometry(1, 24, 16), new THREE.MeshBasicMaterial({ color: new THREE.Color(...(m.rgb || [210, 34, 28]).map(v => v / 255)) }));
  const ring = new THREE.Mesh(new THREE.RingGeometry(1.25, 1.75, 40), new THREE.MeshBasicMaterial({ color: 0xfbf8f1, side: THREE.DoubleSide, transparent: true }));
  ring.lookAt(p.clone().multiplyScalar(2)); dot.position.copy(p); ring.position.copy(p);
  const lab = m.label ? labelSprite(m.label, m.side) : null;
  if (lab) { lab.position.copy(ll(...place(m.place), 1.004)); scene.add(lab); }
  scene.add(dot, ring);
  return { m, p, dot, ring, lab };
});

// ---------------------------------------------------------------- camera keys
const keys = cfg.camera.map(k => ({ ...k }));
for (let i = 1; i < keys.length; i++) {      // take the short way round in longitude
  while (keys[i].lon - keys[i - 1].lon > 180) keys[i].lon -= 360;
  while (keys[i].lon - keys[i - 1].lon < -180) keys[i].lon += 360;
}
function camAt(t) {
  let i = 0; while (i < keys.length - 2 && t > keys[i + 1].t) i++;
  const a = keys[i], b = keys[Math.min(i + 1, keys.length - 1)];
  const u = b.t > a.t ? easeInOut(clamp((t - a.t) / (b.t - a.t))) : 1;
  const mix = k => (a[k] ?? 0) + ((b[k] ?? 0) - (a[k] ?? 0)) * u;
  return { lat: mix('lat'), lon: mix('lon'), dist: mix('dist'), tilt: mix('tilt'), roll: mix('roll') };
}

// ---------------------------------------------------------------- frame
let T = 0, recording = false;
window.__recordFrame = t => { recording = true; T = t; };
const t0 = performance.now();
const tmp = new THREE.Vector3();

function draw(t) {
  // camera: orbit position above (lat - tilt, lon), looking at the surface point (lat, lon)
  const c = camAt(t);
  const target = ll(c.lat, c.lon, 1).multiplyScalar(c.tilt ? 1 : 0);
  camera.position.copy(ll(c.lat - (c.tilt || 0), c.lon, c.dist));
  camera.up.set(0, 1, 0); camera.lookAt(target);
  if (c.roll) camera.rotateZ(c.roll * D2R);
  key.position.copy(camera.position).add(tmp.set(0.6, 0.8, 0).applyQuaternion(camera.quaternion));

  for (const { f, m } of fills) m.opacity = fade(t, f.t_in, f.t_out, f.dur ?? 0.6) * (f.alpha ?? 0.92);

  for (const R of routes) {
    const tout = R.r.t_out;
    const u = easeInOut(ramp(t, R.r.t_in, R.r.dur ?? 1.2));
    R.geo.setDrawRange(0, Math.floor(R.total * u / 3) * 3);
    const a = tout == null ? 1 : 1 - ramp(t, tout, 0.5);
    R.mesh.material.opacity = a; R.mesh.visible = u > 0;
    R.head.visible = u > 0 && u < 1; R.head.position.copy(R.curve.getPoint(u)); R.head.material.opacity = a;
  }

  const camDir = camera.position.clone().normalize();
  const dist = camera.position.length();
  for (const M of markers) {
    const u = ramp(t, M.m.t_in, 0.35), a = u * (M.m.t_out == null ? 1 : 1 - ramp(t, M.m.t_out, 0.4));
    const facing = clamp((M.p.clone().normalize().dot(camDir) - 0.05) * 6);
    const s = (0.0045 + 0.0035 * dist) * (M.m.size ?? 1) * (u > 0 ? easeOutBack(u) : 0);
    M.dot.scale.setScalar(s * 0.55); M.ring.scale.setScalar(s * 0.55);
    M.dot.visible = M.ring.visible = a > 0 && facing > 0;
    M.ring.material.opacity = a * facing;
    if (M.lab) {
      const la = ramp(t, M.m.t_in + 0.15, 0.3) * a * facing, h = (0.018 + 0.016 * dist) * (M.m.label_size ?? 1);
      M.lab.material.opacity = la; M.lab.visible = la > 0;
      M.lab.scale.set(h * M.lab.userData.aspect, h, 1);
    }
  }
  renderer.render(scene, camera);
}

function resize() {
  const w = window.innerWidth, h = window.innerHeight;
  renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
}
window.addEventListener('resize', resize); resize();

function loop() {
  if (!recording) T = ((performance.now() - t0) / 1000) % (cfg.seconds + 1);
  draw(T);
  requestAnimationFrame(loop);
}
draw(0);
window.__ready = true;
requestAnimationFrame(loop);
