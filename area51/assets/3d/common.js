// Shared helpers for the area51 3D shots (illustrative models, recorded frame by frame with frame-capture).
import * as THREE from 'three';
export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const ease = x => x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
export const ramp = (t, t0, d) => clamp((t - t0) / d);
export const lerp = (a, b, k) => a + (b - a) * k;
export function setup(bg = 0x07080a) {
  const canvas = document.getElementById('c');
  const R = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  R.setPixelRatio(1); R.outputColorSpace = THREE.SRGBColorSpace;
  R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.05;
  R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap;
  const S = new THREE.Scene(); S.background = new THREE.Color(bg);
  const cam = new THREE.PerspectiveCamera(34, 16 / 9, 0.05, 4000);
  function resize() { const w = innerWidth, h = innerHeight; R.setSize(w, h, false); cam.aspect = w / h; cam.updateProjectionMatrix(); }
  addEventListener('resize', resize); resize();
  return { R, S, cam };
}
// a warm studio environment map so gold reads as gold
export function goldEnv(R) {
  const es = new THREE.Scene(); es.background = new THREE.Color(0x0a0806);
  const m = c => new THREE.MeshBasicMaterial({ color: c, side: THREE.BackSide });
  const room = new THREE.Mesh(new THREE.BoxGeometry(20, 10, 20), m(0x1a120a)); es.add(room);
  for (const [x, y, z, c, s] of [[-6, 3, -6, 0xffd9a0, 4], [7, 2, 3, 0xffb060, 3], [0, 4.5, 6, 0xfff0d8, 5], [-8, -2, 4, 0x553a20, 6]]) {
    const p = new THREE.Mesh(new THREE.PlaneGeometry(s, s), new THREE.MeshBasicMaterial({ color: c, side: THREE.DoubleSide }));
    p.position.set(x, y, z); p.lookAt(0, 0, 0); es.add(p);
  }
  const pm = new THREE.PMREMGenerator(R); return pm.fromScene(es, 0.04).texture;
}
export function noiseTex(base, spots, alpha, n = 9000, size = 1024, seed0 = 7) {
  const c = document.createElement('canvas'); c.width = c.height = size; const g = c.getContext('2d');
  g.fillStyle = base; g.fillRect(0, 0, size, size);
  let seed = seed0; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  for (let i = 0; i < n; i++) { g.fillStyle = `rgba(${spots},${rnd() * alpha})`; const s = 2 + rnd() * 10; g.fillRect(rnd() * size, rnd() * size, s, s); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; return t;
}
// label sprite: dark bar, red edge, Hindi text (fonts/label.ttf)
export async function labeller(S) {
  await document.fonts.load('80px L', 'अ');
  return function label(text, sub, red = false) {
    const c = document.createElement('canvas'), x = c.getContext('2d'); c.height = 300;
    x.font = '600 110px L'; const w1 = x.measureText(text).width; x.font = '400 60px L'; const w2 = sub ? x.measureText(sub).width : 0;
    const w = Math.ceil(Math.max(w1, w2) + 90); c.width = w;
    x.fillStyle = red ? 'rgba(150,60,16,0.92)' : 'rgba(8,14,18,0.82)'; x.fillRect(0, 0, w, 300);
    x.fillStyle = red ? '#f6f1e8' : '#3fd0c0'; x.fillRect(0, 0, 12, 300);
    x.fillStyle = '#f6f1e8'; x.font = '600 110px L'; x.textBaseline = 'middle'; x.fillText(text, 45, sub ? 105 : 152);
    if (sub) { x.fillStyle = '#d8cdbd'; x.font = '400 60px L'; x.fillText(sub, 45, 228); }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthTest: false, opacity: 0 }));
    s.userData.a = w / 300; s.renderOrder = 50; s.visible = false; S.add(s); return s;
  };
}
// size a label to a fixed share of the screen and fade it in at tin (out at tout)
export function showLabel(s, cam, t, tin, sc = 0.05, tout = 1e9) {
  const k = ramp(t, tin, 0.4) * (1 - ramp(t, tout, 0.4));
  s.material.opacity = k; s.visible = k > 0.001;
  const d = cam.position.distanceTo(s.position); s.scale.set(d * sc * s.userData.a, d * sc, 1);
}
// the "प्रतीकात्मक 3D मॉडल" tag pinned low-left of the frame
export function pinNote(s, cam, t, tin = 0.3, tout = 1e9) {
  const dir = cam.getWorldDirection(new THREE.Vector3());
  s.position.copy(cam.position).add(dir.multiplyScalar(10))
    .add(new THREE.Vector3(-3.3, -2.25, 0).applyQuaternion(cam.quaternion));
  showLabel(s, cam, t, tin, 0.032, tout);
}
export function run(draw, loopLen = 10) {
  const t0 = performance.now(); let recording = false, T = 0;
  window.__recordFrame = t => { recording = true; T = t; draw(T); };
  function loop() { if (!recording) { T = ((performance.now() - t0) / 1000) % loopLen; draw(T); } requestAnimationFrame(loop); }
  draw(0); window.__ready = true; requestAnimationFrame(loop);
}
