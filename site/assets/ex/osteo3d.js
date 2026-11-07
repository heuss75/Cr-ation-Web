// Squelette 3D interactif (three.js). Tout est construit en code : aucune image, aucun modèle externe.
import * as T from '/assets/ex/three.module.min.js';

const V = (x, y, z) => new T.Vector3(x, y, z);
const IDS = ['tete', 'nuque', 'epaule', 'dos', 'lombes', 'poignet', 'hanche', 'genou'];
// position du point cliquable, côté visible (normale), hauteur de la caméra et angle quand la zone est choisie
const ZP = {
  tete:    { p: V(0, 166, 10.5), n: V(0, 0, 1),   y: 160, yaw: 0.35 },
  nuque:   { p: V(0, 148, -4.5), n: V(0, 0, -1),  y: 148, yaw: Math.PI - 0.45 },
  epaule:  { p: V(20.5, 143, 3), n: V(1, 0, .35), y: 138, yaw: 0.8 },
  dos:     { p: V(0, 122, -8),   n: V(0, 0, -1),  y: 122, yaw: Math.PI },
  lombes:  { p: V(0, 95, -7.5),  n: V(0, 0, -1),  y: 95,  yaw: Math.PI },
  poignet: { p: V(24.5, 99, 3),  n: V(1, 0, .4),  y: 98,  yaw: 0.9 },
  hanche:  { p: V(13.5, 84, 5),  n: V(1, 0, .5),  y: 84,  yaw: 0.55 },
  genou:   { p: V(10.2, 47, 7.5), n: V(0, 0, 1),  y: 50,  yaw: 0.35 },
};

function longBone(a, b, r, mat) {
  const L = a.distanceTo(b);
  const prof = [[0, 0], [.7, .01], [1.45, .05], [1.1, .14], [.78, .35], [.74, .55], [.85, .8], [1.15, .9], [1.6, .955], [.8, .995], [0, 1]]
    .map(p => new T.Vector2(p[0] * r, p[1] * L));
  const m = new T.Mesh(new T.LatheGeometry(prof, 14), mat);
  m.position.copy(a);
  m.quaternion.setFromUnitVectors(V(0, 1, 0), b.clone().sub(a).normalize());
  return m;
}

function circleTex(label, sel) {
  const c = document.createElement('canvas'); c.width = c.height = 128;
  const g = c.getContext('2d');
  g.beginPath(); g.arc(64, 64, 46, 0, 6.2832);
  g.fillStyle = sel ? '#ffffff' : '#b99c64'; g.fill();
  g.lineWidth = 7; g.strokeStyle = sel ? '#b99c64' : '#ffffff'; g.stroke();
  g.fillStyle = sel ? '#b99c64' : '#ffffff'; g.font = '700 46px system-ui,sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle';
  g.fillText(label, 64, 68);
  const t = new T.CanvasTexture(c); t.colorSpace = T.SRGBColorSpace; return t;
}
function ringTex() {
  const c = document.createElement('canvas'); c.width = c.height = 128;
  const g = c.getContext('2d');
  g.beginPath(); g.arc(64, 64, 52, 0, 6.2832); g.lineWidth = 6; g.strokeStyle = '#ff8a5c'; g.stroke();
  const t = new T.CanvasTexture(c); t.colorSpace = T.SRGBColorSpace; return t;
}
function glowTex() {
  const c = document.createElement('canvas'); c.width = c.height = 256;
  const g = c.getContext('2d'), gr = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  gr.addColorStop(0, 'rgba(185,156,100,.55)'); gr.addColorStop(.5, 'rgba(185,156,100,.12)'); gr.addColorStop(1, 'rgba(185,156,100,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 256, 256);
  const t = new T.CanvasTexture(c); t.colorSpace = T.SRGBColorSpace; return t;
}

export function init({ el, onSelect }) {
  let renderer;
  try { renderer = new T.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' }); } catch (e) { return null; }
  if (!renderer.getContext()) return null;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.toneMapping = T.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.15;
  const cv = renderer.domElement; cv.style.cssText = 'width:100%;height:100%;display:block;touch-action:pan-y;cursor:grab;outline:0';
  cv.setAttribute('role', 'img'); cv.setAttribute('aria-label', 'Squelette humain en 3D : touchez un point pour choisir la zone qui vous fait mal');
  el.appendChild(cv);

  const scene = new T.Scene();
  const camera = new T.PerspectiveCamera(32, 1, 5, 1200);

  // lumières
  scene.add(new T.AmbientLight(0xfff4e6, .5));
  scene.add(new T.HemisphereLight(0xffffff, 0x1b1e23, .75));
  const key = new T.DirectionalLight(0xfff0dc, 2.2); key.position.set(90, 210, 170); scene.add(key);
  const rim = new T.DirectionalLight(0xffd9a0, 2.8); rim.position.set(-130, 130, -170); scene.add(rim);
  const fill = new T.DirectionalLight(0x9fb4c8, .7); fill.position.set(-110, 60, 130); scene.add(fill);

  // matières : une par zone, pour pouvoir éclairer la zone choisie
  const base = new T.MeshStandardMaterial({ color: 0xe8dfcb, roughness: .52, metalness: .04 });
  const M = {}; IDS.forEach(id => { M[id] = base.clone(); });
  const cart = new T.MeshStandardMaterial({ color: 0xcfc4ad, roughness: .6 });
  const dark = new T.MeshStandardMaterial({ color: 0x15171b, roughness: .9 });

  const sk = new T.Group(); scene.add(sk);
  const add = (m) => { sk.add(m); return m; };

  // ---- crâne
  const cran = add(new T.Mesh(new T.SphereGeometry(1, 32, 24), M.tete)); cran.scale.set(7.7, 8.6, 9.4); cran.position.set(0, 165, .3);
  const face = add(new T.Mesh(new T.SphereGeometry(1, 24, 18), M.tete)); face.scale.set(5.6, 5.4, 5.2); face.position.set(0, 158.2, 5.8);
  const zyg = [-1, 1].map(s => { const m = add(new T.Mesh(new T.SphereGeometry(1.5, 12, 10), M.tete)); m.position.set(s * 5.2, 160.6, 6.6); return m; });
  [-1, 1].forEach(s => { const e = add(new T.Mesh(new T.SphereGeometry(1.9, 14, 12), dark)); e.position.set(s * 3.3, 162.4, 8.3); e.scale.set(1, 1.05, .8); });
  const nose = add(new T.Mesh(new T.ConeGeometry(.9, 2.6, 8), dark)); nose.position.set(0, 159.6, 10.4); nose.rotation.x = Math.PI * .5 + .1;
  const jaw = add(new T.Mesh(new T.TorusGeometry(4.6, .95, 10, 22, Math.PI), M.tete));
  jaw.rotation.set(Math.PI / 2, 0, Math.PI); jaw.position.set(0, 153.6, 3.2); jaw.scale.set(1, 1.1, 1);
  [-1, 1].forEach(s => { const r = add(longBone(V(s * 4.6, 154.2, 2.2), V(s * 4.9, 160, -.2), .9, M.tete)); });
  const teeth = add(new T.Mesh(new T.TorusGeometry(3.3, .55, 6, 20, Math.PI), cart)); teeth.rotation.set(Math.PI / 2, 0, Math.PI); teeth.position.set(0, 155.7, 4.2);

  // ---- colonne vertébrale (C1-C7, T1-T12, L1-L5)
  const vert = [];
  for (let i = 0; i < 7; i++) vert.push({ y: 155.2 - 2.3 * i, z: 0.2 + Math.sin(i / 6 * Math.PI) * .9 - 1.2, r: 1.5 + i * .13, h: 1.9, m: M.nuque, sp: .5 });
  for (let i = 0; i < 12; i++) vert.push({ y: 139 - 3.15 * i, z: -1.4 - Math.sin(Math.PI * (i + .6) / 12.4) * 3.0, r: 2.5 + i * .06, h: 2.7, m: M.dos, sp: .55 + i * .02 });
  for (let i = 0; i < 5; i++) vert.push({ y: 101 - 3.45 * i, z: -3.9 + Math.sin(Math.PI * (i + .2) / 4.4) * 2.6, r: 3.5 + i * .1, h: 3.1, m: M.lombes, sp: .1 });
  vert.forEach((v, i) => {
    const body = add(new T.Mesh(new T.CylinderGeometry(v.r, v.r * .94, v.h, 16), v.m)); body.position.set(0, v.y, v.z);
    const sp = add(new T.Mesh(new T.BoxGeometry(.9, v.h * .95, 3.2), v.m)); sp.position.set(0, v.y - .3, v.z - v.r - 1.3); sp.rotation.x = v.sp;
    const tp = add(new T.Mesh(new T.CylinderGeometry(.5, .5, v.r * 2 + 4.4 + (i > 18 ? 3 : 0), 6), v.m)); tp.rotation.z = Math.PI / 2; tp.position.set(0, v.y, v.z - v.r * .55);
    const disc = add(new T.Mesh(new T.CylinderGeometry(v.r * .92, v.r * .92, .65, 14), cart)); disc.position.set(0, v.y - v.h * .5 - .2, v.z);
  });
  const vz = i => vert[7 + i].z, vy = i => vert[7 + i].y;

  // ---- côtes (12 paires) et sternum
  const rx = [6.5, 8.5, 10.5, 12, 13.2, 14, 14.5, 14.2, 13.4, 12.2, 10.5, 9];
  const rz = [5.5, 7, 8.5, 9.5, 10.3, 11, 11.2, 11, 10.4, 9.4, 7, 6];
  const ribFront = [];
  for (let i = 0; i < 12; i++) {
    const y0 = vy(i) - .3, zc = vz(i) + rz[i] * .9 - 1.4, end = i < 10 ? .12 : 1.15, pts = [];
    for (let k = 0; k <= 14; k++) {
      const t = k / 14, a = (Math.PI - .42) + (end - (Math.PI - .42)) * t;
      pts.push([Math.sin(a) * rx[i], y0 - (i < 10 ? 5.4 : 2.4) * t - Math.sin(t * Math.PI) * -.8, zc + Math.cos(a) * rz[i]]);
    }
    ribFront.push({ y: pts[14][1], z: pts[14][2] });
    [-1, 1].forEach(s => {
      const cv2 = new T.CatmullRomCurve3(pts.map(p => V(s * p[0], p[1], p[2])));
      add(new T.Mesh(new T.TubeGeometry(cv2, 28, i < 2 ? .72 : .56, 6, false), M.dos));
    });
  }
  const sz = (ribFront[3].z + ribFront[5].z) / 2 + .6;
  const man = add(new T.Mesh(new T.BoxGeometry(5.2, 4.6, 1.1), cart)); man.position.set(0, ribFront[1].y + 1.2, ribFront[1].z + .4);
  const stb = add(new T.Mesh(new T.BoxGeometry(3.4, 11.5, .95), cart)); stb.position.set(0, ribFront[4].y + 2.6, sz + .6);
  const xip = add(new T.Mesh(new T.ConeGeometry(1, 3.4, 6), cart)); xip.position.set(0, ribFront[6].y + 1.5, sz + .9); xip.rotation.z = Math.PI;

  // ---- épaules : clavicules, omoplates, humérus
  [-1, 1].forEach(s => {
    add(longBone(V(s * 1.8, ribFront[0].y + 3.4, ribFront[0].z + 1), V(s * 11, 143.8, 3.4), .85, M.epaule));
    add(longBone(V(s * 11, 143.8, 3.4), V(s * 19.6, 142.2, -.6), .8, M.epaule));
    const sh = new T.Shape(); sh.moveTo(0, 0); sh.lineTo(11.5, 2.5); sh.lineTo(10, -1); sh.lineTo(4, -14); sh.lineTo(-.5, -12); sh.lineTo(0, 0);
    const sc = add(new T.Mesh(new T.ExtrudeGeometry(sh, { depth: .7, bevelEnabled: true, bevelThickness: .25, bevelSize: .3, bevelSegments: 2 }), M.epaule));
    sc.position.set(s * 6, 138.5, -8.8); sc.rotation.y = s * .32; sc.scale.x = s;
    const hh = add(new T.Mesh(new T.SphereGeometry(3.1, 18, 14), M.epaule)); hh.position.set(s * 20.4, 140.6, 0);
    add(longBone(V(s * 20.4, 140.2, 0), V(s * 23.2, 111, .6), 1.45, M.epaule));
    // coude, avant-bras, main
    const el = add(new T.Mesh(new T.SphereGeometry(2.1, 14, 12), M.poignet)); el.position.set(s * 23.4, 110.6, .6);
    add(longBone(V(s * 23.8, 110, 1.4), V(s * 25.4, 86.5, 2.6), .95, M.poignet));
    add(longBone(V(s * 22.6, 110, -.4), V(s * 23.6, 86.5, .6), .85, M.poignet));
    const wr = add(new T.Mesh(new T.BoxGeometry(4.2, 2.2, 2.6), M.poignet)); wr.position.set(s * 24.5, 84.8, 1.8);
    const pm = add(new T.Mesh(new T.BoxGeometry(5.2, 7, 1.6), M.poignet)); pm.position.set(s * 24.7, 79.5, 2);
    [[-2.2, 8.5], [-.7, 9.6], [.8, 10], [2.2, 9], [3.8, 6.4]].forEach((f, k) => {
      const x = s * (24.7 + f[0]), thumb = k === 4;
      add(longBone(V(x, 76.2 - (thumb ? 1 : 0), 2 + (thumb ? 1.6 : 0)), V(x + s * (thumb ? 2.4 : .3 * k), 76.2 - f[1] - (thumb ? 0 : 0), 2.8 + (thumb ? 2.2 : .3)), .55, M.poignet));
    });
  });

  // ---- bassin
  const sac = add(new T.Mesh(new T.CylinderGeometry(4.4, 1.2, 18, 12), M.lombes)); sac.position.set(0, 77, -5.8); sac.rotation.x = -.42; sac.scale.z = .55;
  [-1, 1].forEach(s => {
    const il = add(new T.Mesh(new T.SphereGeometry(1, 22, 16), M.hanche)); il.scale.set(9.4, 9.2, 2.4); il.position.set(s * 11, 92.4, -1.8); il.rotation.set(.1, s * -.62, s * .3);
    const ac = add(new T.Mesh(new T.SphereGeometry(4.4, 16, 12), M.hanche)); ac.position.set(s * 9.6, 83.4, 1.6);
    add(longBone(V(s * 9.8, 80, 3), V(s * 1.2, 76, 9), 1.2, M.hanche));
    add(longBone(V(s * 9.4, 80.8, 0), V(s * 7.2, 69, -2), 1.3, M.hanche));
  });
  // ---- jambes
  [-1, 1].forEach(s => {
    const fh = add(new T.Mesh(new T.SphereGeometry(3.2, 18, 14), M.hanche)); fh.position.set(s * 9.4, 83.6, 1.6);
    add(longBone(V(s * 9.6, 83.4, 1.6), V(s * 14.2, 79, .4), 1.3, M.hanche));
    add(longBone(V(s * 13.2, 80.4, .6), V(s * 10.2, 49, 1.4), 1.95, M.genou));
    [-1.6, 1.6].forEach(o => { const cd = add(new T.Mesh(new T.SphereGeometry(2.6, 14, 12), M.genou)); cd.position.set(s * (10.2 + o), 47.6, .8); });
    const pa = add(new T.Mesh(new T.SphereGeometry(2.3, 14, 12), M.genou)); pa.scale.set(1, 1.1, .55); pa.position.set(s * 10.4, 47.8, 4.7);
    add(longBone(V(s * 10, 45, 1.2), V(s * 9.2, 8.6, .8), 1.65, M.genou));
    add(longBone(V(s * 13.1, 44, .2), V(s * 11.7, 9.4, .2), .75, M.genou));
    const calc = add(new T.Mesh(new T.SphereGeometry(1, 14, 10), base)); calc.scale.set(2.8, 2.6, 3.6); calc.position.set(s * 9.8, 4.4, -3);
    const tar = add(new T.Mesh(new T.BoxGeometry(6, 2.4, 6), base)); tar.position.set(s * 9.8, 5, 1.2);
    for (let k = 0; k < 5; k++) add(longBone(V(s * (7.6 + k * 1.5), 3.6, 4), V(s * (7.2 + k * 1.7), 1.6, 12.6 - k * .7), .55, base));
  });

  // ---- sol lumineux + anneau
  const glow = new T.Mesh(new T.PlaneGeometry(120, 120), new T.MeshBasicMaterial({ map: glowTex(), transparent: true, depthWrite: false }));
  glow.rotation.x = -Math.PI / 2; glow.position.y = .05; scene.add(glow);
  const ring = new T.Mesh(new T.RingGeometry(31, 31.5, 72), new T.MeshBasicMaterial({ color: 0xb99c64, transparent: true, opacity: .55, side: T.DoubleSide }));
  ring.rotation.x = -Math.PI / 2; ring.position.y = .1; scene.add(ring);

  // ---- points cliquables
  const texN = IDS.map((id, i) => circleTex(String(i + 1), false)), texS = IDS.map((id, i) => circleTex(String(i + 1), true)), texR = ringTex();
  const hot = IDS.map((id, i) => {
    const sp = new T.Sprite(new T.SpriteMaterial({ map: texN[i], transparent: true, depthTest: false, depthWrite: false })); sp.renderOrder = 20; sp.position.copy(ZP[id].p); sk.add(sp);
    const rg = new T.Sprite(new T.SpriteMaterial({ map: texR, transparent: true, depthTest: false, depthWrite: false })); rg.renderOrder = 19; rg.position.copy(ZP[id].p); sk.add(rg);
    return { id, sp, rg };
  });

  // ---- état et animation
  let W = 1, Hh = 1, yaw = .35, yawV = 0, tYaw = null, camY = 92, camD = 360, tY = 92, tD = 360, drag = null, idle = 0, sel = null, last = performance.now(), run = true, vis = true, raf = 0;
  const FULL_D = () => (camera.aspect < .8 ? 400 : 322);
  function resize() {
    W = el.clientWidth || 300; Hh = el.clientHeight || 400;
    renderer.setSize(W, Hh, false); camera.aspect = W / Hh; camera.updateProjectionMatrix();
    if (!sel) { tD = camD = FULL_D(); }
  }
  new ResizeObserver(resize).observe(el); resize();

  function select(id, silent) {
    sel = id;
    if (id) { tYaw = ZP[id].yaw; tY = ZP[id].y; tD = camera.aspect < .8 ? 230 : 190; }
    else { tYaw = null; tY = 92; tD = FULL_D(); }
    IDS.forEach((k, i) => { hot[i].sp.material.map = (k === id) ? texS[i] : texN[i]; hot[i].sp.material.needsUpdate = true; });
    if (!silent && onSelect) onSelect(id);
    wake();
  }
  function pick(cx, cy) {
    const r = cv.getBoundingClientRect(); let best = null, bd = 1e9;
    hot.forEach((h, i) => {
      const w = ZP[h.id].p.clone().applyMatrix4(sk.matrixWorld).project(camera);
      const sx = (w.x * .5 + .5) * r.width + r.left, sy = (-w.y * .5 + .5) * r.height + r.top, d = Math.hypot(sx - cx, sy - cy);
      if (d < bd) { bd = d; best = h; }
    });
    if (best && bd < 34 && best.sp.material.opacity > .5) select(best.id === sel ? null : best.id);
  }
  cv.addEventListener('pointerdown', e => {
    if (e.button > 0) return;
    drag = { x: e.clientX, y: e.clientY, moved: 0, t: performance.now() }; yawV = 0; tYaw = null; idle = 0; cv.style.cursor = 'grabbing';
    try { cv.setPointerCapture(e.pointerId); } catch (_) {}
  });
  cv.addEventListener('pointermove', e => {
    if (!drag) return;
    const dx = e.clientX - drag.x, now = performance.now(), dt = Math.max(4, now - drag.t);
    drag.moved += Math.abs(dx) + Math.abs(e.clientY - drag.y); drag.x = e.clientX; drag.y = e.clientY; drag.t = now;
    const d = dx * .0105; yaw += d; yawV = yawV * .5 + (d / (dt / 1000)) * .5; idle = 0; wake();
  });
  const end = e => {
    if (!drag) return; const m = drag.moved; drag = null; cv.style.cursor = 'grab';
    if (m < 6) { pick(e.clientX, e.clientY); yawV = 0; } else if (performance.now() - last > 120) yawV *= .3;
    wake();
  };
  cv.addEventListener('pointerup', end); cv.addEventListener('pointercancel', () => { drag = null; cv.style.cursor = 'grab'; });
  cv.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') { yawV -= 2; wake(); } if (e.key === 'ArrowRight') { yawV += 2; wake(); } });
  cv.tabIndex = 0;

  function frame(now) {
    raf = 0; const dt = Math.min(.05, (now - last) / 1000); last = now; idle += dt;
    if (!drag) {
      if (tYaw !== null) { let d = tYaw - yaw; d = Math.atan2(Math.sin(d), Math.cos(d)); yaw += d * (1 - Math.exp(-dt * 4.2)); if (Math.abs(d) < .003) { yaw = tYaw; tYaw = null; } }
      else { yaw += yawV * dt; yawV *= Math.exp(-dt * 2.1); if (!sel && idle > 2.5 && Math.abs(yawV) < .3) yaw += .26 * dt; }
    }
    const k = 1 - Math.exp(-dt * 4); camY += (tY - camY) * k; camD += (tD - camD) * k;
    sk.rotation.y = yaw;
    camera.position.set(0, camY + 10 + camD * .02, camD); camera.lookAt(0, camY, 0);
    sk.updateMatrixWorld(true);
    const pulse = (now / 1000) % 1.6 / 1.6;
    hot.forEach(h => {
      const wp = ZP[h.id].p.clone().applyMatrix4(sk.matrixWorld);
      const n = ZP[h.id].n.clone().transformDirection(sk.matrixWorld), v = camera.position.clone().sub(wp).normalize();
      const f = n.dot(v), op = f > .12 ? 1 : f > -.15 ? (f + .15) / .27 : 0, s = (camera.aspect < .8 ? 15 : 11.5) * (camD / 360 < .7 ? .75 : 1), on = h.id === sel;
      h.sp.material.opacity = Math.max(0, Math.min(1, op)) * (on ? 1 : .96); h.sp.scale.setScalar(on ? s * 1.15 : s);
      h.rg.material.opacity = on ? 0 : (1 - pulse) * .7 * Math.max(0, Math.min(1, op)); h.rg.scale.setScalar(s * (1 + pulse * 1.1));
    });
    IDS.forEach(id => { const on = id === sel; M[id].emissive.setHex(on ? 0xb99c64 : 0x000000); M[id].emissiveIntensity = on ? .45 + Math.sin(now / 280) * .18 : 0; });
    ring.material.opacity = .4 + Math.sin(now / 900) * .12;
    renderer.render(scene, camera);
    if (run && vis) raf = requestAnimationFrame(frame);
  }
  function wake() { if (!raf && vis) { last = performance.now(); raf = requestAnimationFrame(frame); } }
  new IntersectionObserver(es => { vis = es[0].isIntersecting; if (vis) wake(); }, { threshold: .05 }).observe(el);
  document.addEventListener('visibilitychange', () => { run = !document.hidden; if (run) wake(); });
  wake();
  return { select, reset: () => select(null) };
}
