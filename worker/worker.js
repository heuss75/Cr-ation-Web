// Worker Cloudflare : sert le site depuis GitHub (dossier /site) et reçoit les demandes du formulaire (base D1).
const REPO = 'https://raw.githubusercontent.com/heuss75/Cr-ation-Web/main/site';
const ROUTES = {
  '/': 'index.html', '/offre': 'offre.html', '/faq': 'faq.html', '/commander': 'commander.html', '/connexion': 'connexion.html',
  '/mentions-legales': 'mentions-legales.html', '/cgv': 'cgv.html', '/confidentialite': 'confidentialite.html', '/cookies': 'cookies.html',
  '/reservation-demo': 'reservation-demo.html', '/inscription': 'inscription.html', '/admin': 'admin.html', '/espace': 'espace.html', '/mot-de-passe-oublie': 'mot-de-passe-oublie.html', '/reinitialiser': 'reinitialiser.html', '/exemples/bistro': 'exemples/bistro.html', '/exemples/salon': 'exemples/salon.html', '/exemples/artisan': 'exemples/artisan.html',
};
const TYPES = {
  html: 'text/html; charset=utf-8', css: 'text/css; charset=utf-8', js: 'text/javascript; charset=utf-8', json: 'application/json; charset=utf-8',
  txt: 'text/plain; charset=utf-8', xml: 'application/xml; charset=utf-8', svg: 'image/svg+xml', woff2: 'font/woff2', png: 'image/png',
  jpg: 'image/jpeg', webp: 'image/webp', ico: 'image/x-icon',
};
const SEC = {
  'x-content-type-options': 'nosniff', 'referrer-policy': 'strict-origin-when-cross-origin', 'x-frame-options': 'SAMEORIGIN',
  'permissions-policy': 'camera=(), microphone=(), geolocation=()', 'strict-transport-security': 'max-age=31536000',
};
const FORMULES = ['essentiel', 'pro'];
// Démo de réservation : mardi au samedi, 9h-12h et 14h-18h, créneaux de 30 min (mêmes règles que tools/src/booking.js)
const UNITS = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30'];
const SERVICES = { 'coupe-femme': 2, 'coupe-homme': 1, 'couleur': 3, 'brushing': 1 };
const ACTIVITES = ['coiffeur', 'restaurant', 'artisan', 'therapeute', 'coach', 'boutique', 'autre'];

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...SEC } });
}

async function fromGithub(file, status = 200) {
  const r = await fetch(REPO + '/' + file, { cf: { cacheTtl: 30, cacheEverything: true } });
  if (!r.ok) return null;
  const ext = file.split('.').pop();
  const h = new Headers({ 'content-type': TYPES[ext] || 'application/octet-stream', ...SEC });
  if (ext === 'html') h.set('cache-control', 'public, max-age=60');
  else if (ext === 'woff2') h.set('cache-control', 'public, max-age=31536000, immutable');
  else h.set('cache-control', 'public, max-age=86400');
  return new Response(r.body, { status, headers: h });
}

function validate(b) {
  const e = {};
  const s = (k) => (typeof b[k] === 'string' ? b[k].trim() : '');
  if (s('nom').length < 2 || s('nom').length > 80) e.nom = 'Nom requis (2 à 80 caractères).';
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(s('email')) || s('email').length > 120) e.email = 'Adresse e-mail invalide.';
  if (s('tel') && !/^[0-9+().\s-]{8,20}$/.test(s('tel'))) e.tel = 'Numéro invalide.';
  if (s('commerce').length < 2 || s('commerce').length > 80) e.commerce = 'Nom du commerce requis (2 à 80 caractères).';
  if (!ACTIVITES.includes(s('activite'))) e.activite = 'Choisissez une activité.';
  if (s('ville').length < 2 || s('ville').length > 60) e.ville = 'Ville requise.';
  if (s('domaine') && !/^[a-z0-9][a-z0-9-]{0,61}(\.[a-z]{2,10})?$/i.test(s('domaine'))) e.domaine = 'Nom de domaine invalide.';
  if (!FORMULES.includes(s('formule'))) e.formule = 'Choisissez une formule.';
  const m = parseInt(b.mails, 10);
  if (!(m >= 0 && m <= 10)) e.mails = 'Nombre invalide.';
  if (s('message').length > 1000) e.message = '1000 caractères au maximum.';
  if (b.cgv !== true) e.cgv = 'Acceptation requise.';
  return e;
}

async function demande(req, env, url) {
  if (req.method !== 'POST') return json({ ok: false }, 405);
  const origin = req.headers.get('origin');
  if (origin && origin !== url.origin) return json({ ok: false }, 403);
  const raw = await req.text();
  if (raw.length > 8000) return json({ ok: false }, 413);
  let b;
  try { b = JSON.parse(raw); } catch (_) { return json({ ok: false }, 400); }
  if (!b || typeof b !== 'object') return json({ ok: false }, 400);
  const alphabet = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
  const rnd = crypto.getRandomValues(new Uint8Array(6));
  const ref = 'SVE-' + Array.from(rnd, (x) => alphabet[x % alphabet.length]).join('');
  if (b.site_web_url) return json({ ok: true, ref }); // piège anti-robots : on fait semblant
  let user = null;
  try { user = await currentUser(req, env); } catch (_) {}
  if (!user) return json({ ok: false, error: 'compte' }, 401);
  if (user.par_admin) return json({ ok: false, error: 'lecture-seule' }, 403);
  const errors = validate(b);
  if (Object.keys(errors).length) return json({ ok: false, errors }, 422);
  const ip = req.headers.get('cf-connecting-ip') || 'inconnue';
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(ip + '|sve'));
  const iph = Array.from(new Uint8Array(buf).slice(0, 8), (x) => x.toString(16).padStart(2, '0')).join('');
  try {
    const c = await env.DB.prepare("SELECT COUNT(*) AS n FROM demandes WHERE ip_hash = ? AND created_at > datetime('now','-1 hour')").bind(iph).first();
    if (c && c.n >= 5) return json({ ok: false }, 429);
    let utm = '';
    if (b.utm && typeof b.utm === 'object') {
      const o = {};
      for (const k of ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'ref', 'landing']) if (typeof b.utm[k] === 'string') o[k] = b.utm[k].slice(0, 100);
      utm = JSON.stringify(o).slice(0, 600);
    }
    const t = (k, n) => (typeof b[k] === 'string' ? b[k].trim().slice(0, n) : '');
    await env.DB.prepare('INSERT INTO demandes (ref, nom, email, tel, commerce, activite, ville, domaine, mails, message, utm, page, ip_hash, ua, formule, compte_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
      .bind(ref, t('nom', 80), t('email', 120), t('tel', 20), t('commerce', 80), t('activite', 20), t('ville', 60), t('domaine', 70), parseInt(b.mails, 10) || 0, t('message', 1000), utm, t('page', 60), iph, (req.headers.get('user-agent') || '').slice(0, 200), t('formule', 12), user.id).run();
  } catch (_) {
    return json({ ok: false }, 500);
  }
  return json({ ok: true, ref });
}


// ---------- Comptes (inscription, connexion, session par cookie) ----------
const enc = new TextEncoder();
const hex = (u8) => Array.from(u8, (x) => x.toString(16).padStart(2, '0')).join('');
const unhex = (h) => new Uint8Array((h.match(/../g) || []).map((x) => parseInt(x, 16)));
const ITER = 100000;
async function pbkdf2(pw, salt, iter = ITER) {
  const key = await crypto.subtle.importKey('raw', enc.encode(pw), 'PBKDF2', false, ['deriveBits']);
  return new Uint8Array(await crypto.subtle.deriveBits({ name: 'PBKDF2', hash: 'SHA-256', salt, iterations: iter }, key, 256));
}
function same(a, b) { if (a.length !== b.length) return false; let d = 0; for (let i = 0; i < a.length; i++) d |= a[i] ^ b[i]; return d === 0; }
async function sha(txt) { return hex(new Uint8Array(await crypto.subtle.digest('SHA-256', enc.encode(txt)))); }
async function ipHash(req, tag) { return (await sha((req.headers.get('cf-connecting-ip') || 'inconnue') + '|' + tag)).slice(0, 16); }
function cookieOf(req, name) {
  const m = (req.headers.get('cookie') || '').split(/;\s*/).find((c) => c.startsWith(name + '='));
  return m ? m.slice(name.length + 1) : '';
}
function sessionCookie(token, maxAge) {
  return 'sv_session=' + token + '; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=' + maxAge;
}
async function currentUser(req, env) {
  const t = cookieOf(req, 'sv_session');
  if (!/^[0-9a-f]{64}$/.test(t)) return null;
  const r = await env.DB.prepare("SELECT c.id, c.nom, c.email, c.role, s.par_admin FROM sessions s JOIN comptes c ON c.id = s.compte_id WHERE s.token_hash = ? AND s.expires_at > datetime('now')").bind(await sha(t)).first();
  return r || null;
}
async function log(env, compteId, adminId, type, detail) {
  try { await env.DB.prepare('INSERT INTO journal (compte_id, admin_id, type, detail) VALUES (?,?,?,?)').bind(compteId || null, adminId || null, type, (detail || '').slice(0, 300)).run(); } catch (_) {}
}
async function newSession(env, compteId, parAdmin) {
  const token = hex(crypto.getRandomValues(new Uint8Array(32)));
  await env.DB.prepare("INSERT INTO sessions (token_hash, compte_id, expires_at, par_admin) VALUES (?, ?, datetime('now', ?), ?)").bind(await sha(token), compteId, parAdmin ? '+2 hours' : '+30 days', parAdmin || null).run();
  return token;
}
async function readJson(req, url, max = 2000) {
  const origin = req.headers.get('origin');
  if (origin && origin !== url.origin) return { err: json({ ok: false }, 403) };
  const raw = await req.text();
  if (raw.length > max) return { err: json({ ok: false }, 413) };
  try { const b = JSON.parse(raw); if (b && typeof b === 'object') return { b }; } catch (_) {}
  return { err: json({ ok: false }, 400) };
}
const MAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
async function inscription(req, env, url) {
  if (req.method !== 'POST') return json({ ok: false }, 405);
  const { b, err } = await readJson(req, url); if (err) return err;
  if (b.site_web_url) return json({ ok: true });
  const nom = typeof b.nom === 'string' ? b.nom.trim() : '';
  const email = typeof b.email === 'string' ? b.email.trim().toLowerCase() : '';
  const pw = typeof b.password === 'string' ? b.password : '';
  const errors = {};
  if (nom.length < 2 || nom.length > 80) errors.nom = 'Nom requis (2 à 80 caractères).';
  if (!MAIL_RE.test(email) || email.length > 120) errors.email = 'Adresse e-mail invalide.';
  if (pw.length < 8 || pw.length > 100) errors.password = 'Le mot de passe contient entre 8 et 100 caractères.';
  if (b.cgv !== true) errors.cgv = 'Acceptation requise.';
  if (Object.keys(errors).length) return json({ ok: false, errors }, 422);
  const iph = await ipHash(req, 'ins');
  try {
    const c = await env.DB.prepare("SELECT COUNT(*) AS n FROM comptes WHERE ip_hash = ? AND created_at > datetime('now','-1 hour')").bind(iph).first();
    if (c && c.n >= 5) return json({ ok: false }, 429);
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const h = await pbkdf2(pw, salt);
    let id;
    try {
      const r = await env.DB.prepare('INSERT INTO comptes (email, nom, salt, hash, iter, ip_hash) VALUES (?,?,?,?,?,?)').bind(email, nom, hex(salt), hex(h), ITER, iph).run();
      id = r.meta.last_row_id;
    } catch (e) {
      if (String(e && e.message).includes('UNIQUE')) return json({ ok: false, errors: { email: 'Un compte existe déjà avec cette adresse : connectez-vous.' } }, 409);
      throw e;
    }
    await log(env, id, null, 'inscription', '');
    const token = await newSession(env, id);
    const res = json({ ok: true, nom });
    res.headers.append('set-cookie', sessionCookie(token, 2592000));
    return res;
  } catch (_) { return json({ ok: false }, 500); }
}
async function connexion(req, env, url) {
  if (req.method !== 'POST') return json({ ok: false }, 405);
  const { b, err } = await readJson(req, url); if (err) return err;
  const email = typeof b.email === 'string' ? b.email.trim().toLowerCase() : '';
  const pw = typeof b.password === 'string' ? b.password : '';
  if (!MAIL_RE.test(email) || pw.length < 1 || pw.length > 100) return json({ ok: false, error: 'identifiants' }, 401);
  const iph = await ipHash(req, 'log');
  try {
    await env.DB.prepare("DELETE FROM essais WHERE at < datetime('now','-1 day')").run();
    const c = await env.DB.prepare("SELECT COUNT(*) AS n FROM essais WHERE ip_hash = ? AND at > datetime('now','-15 minutes')").bind(iph).first();
    if (c && c.n >= 10) return json({ ok: false }, 429);
    const u = await env.DB.prepare('SELECT id, nom, salt, hash, iter FROM comptes WHERE email = ?').bind(email).first();
    const h = await pbkdf2(pw, u ? unhex(u.salt) : new Uint8Array(16), u ? u.iter : ITER);
    if (!u || !same(h, unhex(u.hash))) {
      await env.DB.prepare('INSERT INTO essais (ip_hash) VALUES (?)').bind(iph).run();
      return json({ ok: false, error: 'identifiants' }, 401);
    }
    await env.DB.prepare("UPDATE comptes SET derniere_connexion = datetime('now') WHERE id = ?").bind(u.id).run();
    await log(env, u.id, null, 'connexion', '');
    const token = await newSession(env, u.id);
    const res = json({ ok: true, nom: u.nom });
    res.headers.append('set-cookie', sessionCookie(token, 2592000));
    return res;
  } catch (_) { return json({ ok: false }, 500); }
}
async function deconnexion(req, env, url) {
  if (req.method !== 'POST') return json({ ok: false }, 405);
  const t = cookieOf(req, 'sv_session');
  try { if (/^[0-9a-f]{64}$/.test(t)) await env.DB.prepare('DELETE FROM sessions WHERE token_hash = ?').bind(await sha(t)).run(); } catch (_) {}
  const res = json({ ok: true });
  res.headers.append('set-cookie', sessionCookie('', 0));
  return res;
}
async function moi(req, env) {
  try {
    const u = await currentUser(req, env);
    if (!u) return json({ ok: false }, 401);
    const o = { ok: true, nom: u.nom, email: u.email, admin: u.role === 'admin' && !u.par_admin };
    if (u.par_admin) { const ad = await env.DB.prepare('SELECT nom FROM comptes WHERE id = ?').bind(u.par_admin).first(); o.impersonation = true; o.admin_nom = ad ? ad.nom : 'Admin'; }
    return json(o);
  } catch (_) { return json({ ok: false }, 500); }
}
async function quitterImpersonation(req, env, url) {
  if (req.method !== 'POST') return json({ ok: false }, 405);
  const t = cookieOf(req, 'sv_session');
  try {
    const u = await currentUser(req, env);
    if (!u || !u.par_admin) return json({ ok: false }, 400);
    await env.DB.prepare('DELETE FROM sessions WHERE token_hash = ?').bind(await sha(t)).run();
    await log(env, u.id, u.par_admin, 'admin_fin_impersonation', '');
    const token = await newSession(env, u.par_admin);
    const res = json({ ok: true });
    res.headers.append('set-cookie', sessionCookie(token, 2592000));
    return res;
  } catch (_) { return json({ ok: false }, 500); }
}
async function motDePasse(req, env, url) {
  if (req.method !== 'POST') return json({ ok: false }, 405);
  const { b, err } = await readJson(req, url); if (err) return err;
  try {
    const u = await currentUser(req, env);
    if (!u) return json({ ok: false }, 401);
    if (u.par_admin) return json({ ok: false, error: 'lecture-seule' }, 403);
    const ancien = typeof b.actuel === 'string' ? b.actuel : '', nouveau = typeof b.nouveau === 'string' ? b.nouveau : '';
    if (nouveau.length < 8 || nouveau.length > 100) return json({ ok: false, error: 'longueur' }, 422);
    const iph = await ipHash(req, 'log');
    const c = await env.DB.prepare("SELECT COUNT(*) AS n FROM essais WHERE ip_hash = ? AND at > datetime('now','-15 minutes')").bind(iph).first();
    if (c && c.n >= 10) return json({ ok: false }, 429);
    const row = await env.DB.prepare('SELECT salt, hash, iter FROM comptes WHERE id = ?').bind(u.id).first();
    const h = await pbkdf2(ancien, unhex(row.salt), row.iter);
    if (!same(h, unhex(row.hash))) { await env.DB.prepare('INSERT INTO essais (ip_hash) VALUES (?)').bind(iph).run(); return json({ ok: false, error: 'actuel' }, 401); }
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const nh = await pbkdf2(nouveau, salt);
    await env.DB.prepare('UPDATE comptes SET salt = ?, hash = ?, iter = ? WHERE id = ?').bind(hex(salt), hex(nh), ITER, u.id).run();
    await env.DB.prepare('DELETE FROM sessions WHERE compte_id = ? AND token_hash != ?').bind(u.id, await sha(cookieOf(req, 'sv_session'))).run();
    await log(env, u.id, null, 'mot_de_passe', '');
    return json({ ok: true });
  } catch (_) { return json({ ok: false }, 500); }
}

// ---------- Espace client et communication ----------
const MOIS_QUOTA = { essentiel: 1, pro: 3 };
const premierDuMois = () => new Date().toISOString().slice(0, 7) + '-01';
async function espace(req, env, url, p) {
  let u;
  try { u = await currentUser(req, env); } catch (_) { return json({ ok: false }, 500); }
  if (!u) return json({ ok: false }, 401);
  const one = (sql, ...a) => env.DB.prepare(sql).bind(...a).first();
  const all = async (sql, ...a) => (await env.DB.prepare(sql).bind(...a).all()).results || [];
  const lecture = !!u.par_admin;
  try {
    if (p === '/api/espace' && req.method === 'GET') {
      const compte = await one('SELECT nom, email, created_at FROM comptes WHERE id = ?', u.id);
      const demandes = await all('SELECT id, ref, created_at, commerce, activite, ville, domaine, mails, tel, formule, statut, suspendu, site_url FROM demandes WHERE compte_id = ? ORDER BY id DESC', u.id);
      const abo = await one('SELECT formule, statut, mails_sup, debut, fin FROM abonnements WHERE compte_id = ?', u.id);
      const formule = abo ? abo.formule : (demandes[0] ? demandes[0].formule : 'essentiel');
      const used = await one('SELECT COUNT(*) n FROM modifs WHERE compte_id = ? AND created_at >= ?', u.id, premierDuMois());
      return json({ ok: true, lecture, compte, demandes, abonnement: abo, formule, quota: MOIS_QUOTA[formule] || 1, utilisees: used ? used.n : 0,
        notifications: await all('SELECT id, titre, message, lu, created_at FROM notifications WHERE compte_id = ? ORDER BY id DESC LIMIT 40', u.id),
        modifs: await all('SELECT id, type, description, statut, created_at FROM modifs WHERE compte_id = ? ORDER BY id DESC LIMIT 30', u.id),
        plaintes: await all('SELECT id, sujet, statut, created_at FROM plaintes WHERE compte_id = ? ORDER BY id DESC LIMIT 20', u.id) });
    }
    if (req.method !== 'POST') return json({ ok: false }, 405);
    if (lecture) return json({ ok: false, error: 'lecture-seule' }, 403);
    const { b, err } = await readJson(req, url, 4000); if (err) return err;
    const txt = (v, n) => (typeof v === 'string' ? v.trim().slice(0, n) : '');
    if (p === '/api/espace/lu') {
      await env.DB.prepare('UPDATE notifications SET lu = 1 WHERE compte_id = ?').bind(u.id).run();
      return json({ ok: true });
    }
    if (p === '/api/espace/modif') {
      const d = await one("SELECT id, statut, suspendu, formule FROM demandes WHERE compte_id = ? ORDER BY id DESC LIMIT 1", u.id);
      if (!d || d.suspendu) return json({ ok: false, error: 'suspendu' }, 403);
      if (!['apercu', 'en_ligne'].includes(d.statut)) return json({ ok: false, error: 'pas-en-ligne' }, 409);
      const abo = await one('SELECT formule FROM abonnements WHERE compte_id = ?', u.id);
      const quota = MOIS_QUOTA[abo ? abo.formule : d.formule] || 1;
      const used = await one('SELECT COUNT(*) n FROM modifs WHERE compte_id = ? AND created_at >= ?', u.id, premierDuMois());
      if (used.n >= quota) return json({ ok: false, error: 'quota' }, 409);
      const type = ['texte', 'photo', 'bloc', 'autre'].includes(b.type) ? b.type : 'autre', desc = txt(b.description, 1200);
      if (desc.length < 5) return json({ ok: false, error: 'vide' }, 422);
      await env.DB.prepare('INSERT INTO modifs (compte_id, type, description) VALUES (?,?,?)').bind(u.id, type, desc).run();
      await log(env, u.id, null, 'modification', type);
      return json({ ok: true });
    }
    if (p === '/api/espace/plainte') {
      const sujet = txt(b.sujet, 120);
      if (!sujet) return json({ ok: false }, 422);
      await env.DB.prepare('INSERT INTO plaintes (compte_id, sujet, message) VALUES (?,?,?)').bind(u.id, sujet, txt(b.message, 1500)).run();
      await log(env, u.id, null, 'plainte', sujet);
      return json({ ok: true });
    }
    return json({ ok: false }, 404);
  } catch (_) { return json({ ok: false }, 500); }
}
const escH = (s) => String(s || '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const mailOk = (env) => !!(env.RESEND_API_KEY && env.MAIL_FROM);
async function envoyerMail(env, to, subject, text, html) {
  if (!mailOk(env)) return false;
  try {
    const r = await fetch('https://api.resend.com/emails', { method: 'POST', headers: { authorization: 'Bearer ' + env.RESEND_API_KEY, 'content-type': 'application/json' }, body: JSON.stringify({ from: env.MAIL_FROM, to: [to], subject, text, html }) });
    return r.ok;
  } catch (_) { return false; }
}
async function oubli(req, env, url) {
  if (req.method !== 'POST') return json({ ok: false }, 405);
  const { b, err } = await readJson(req, url); if (err) return err;
  if (b.site_web_url) return json({ ok: true });
  const email = typeof b.email === 'string' ? b.email.trim().toLowerCase() : '';
  if (!MAIL_RE.test(email) || email.length > 120) return json({ ok: true });
  try {
    const iph = await ipHash(req, 'oubli');
    await env.DB.prepare("DELETE FROM essais WHERE at < datetime('now','-1 day')").run();
    const c = await env.DB.prepare("SELECT COUNT(*) AS n FROM essais WHERE ip_hash = ? AND at > datetime('now','-1 hour')").bind(iph).first();
    if (c && c.n >= 5) return json({ ok: false }, 429);
    await env.DB.prepare('INSERT INTO essais (ip_hash) VALUES (?)').bind(iph).run();
    const u = await env.DB.prepare('SELECT id, nom, demo FROM comptes WHERE email = ?').bind(email).first();
    if (u && !u.demo) {
      const token = hex(crypto.getRandomValues(new Uint8Array(32)));
      await env.DB.prepare("INSERT INTO reset_tokens (token_hash, compte_id, expires_at) VALUES (?,?,datetime('now','+1 hour'))").bind(await sha(token), u.id).run();
      const lien = url.origin + '/reinitialiser?t=' + token, prenom = (u.nom || '').split(/\s+/)[0];
      const texte = 'Bonjour ' + prenom + ',\n\nVous avez demandé à changer votre mot de passe SiteVitrine Express. Ouvrez ce lien (valable 1 heure) :\n' + lien + '\n\nSi vous n’êtes pas à l’origine de cette demande, ignorez ce message : votre mot de passe ne change pas.';
      const ok = await envoyerMail(env, email, 'Votre nouveau mot de passe SiteVitrine Express', texte,
        '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.55;color:#111"><p>Bonjour ' + escH(prenom) + ',</p><p>Vous avez demandé à changer votre mot de passe SiteVitrine Express.</p><p><a href="' + lien + '" style="display:inline-block;background:#0b0b0c;color:#fff;padding:12px 20px;border-radius:10px;text-decoration:none;font-weight:bold">Choisir un nouveau mot de passe</a></p><p style="font-size:13px;color:#555">Le lien est valable 1 heure. Si vous n’êtes pas à l’origine de cette demande, ignorez ce message : votre mot de passe ne change pas.</p></div>');
      await log(env, u.id, null, ok ? 'oubli_mdp_mail' : 'oubli_mdp_sans_mail', '');
    }
    return json({ ok: true });
  } catch (_) { return json({ ok: false }, 500); }
}
async function reinitialiser(req, env, url) {
  if (req.method !== 'POST') return json({ ok: false }, 405);
  const { b, err } = await readJson(req, url); if (err) return err;
  const t = typeof b.token === 'string' ? b.token : '', pw = typeof b.password === 'string' ? b.password : '';
  if (!/^[0-9a-f]{64}$/.test(t) || pw.length < 8 || pw.length > 100) return json({ ok: false }, 422);
  try {
    const th = await sha(t);
    const r = await env.DB.prepare("SELECT compte_id FROM reset_tokens WHERE token_hash = ? AND used = 0 AND expires_at > datetime('now')").bind(th).first();
    if (!r) return json({ ok: false }, 410);
    const salt = crypto.getRandomValues(new Uint8Array(16)), h = await pbkdf2(pw, salt);
    await env.DB.prepare('UPDATE comptes SET salt = ?, hash = ?, iter = ? WHERE id = ?').bind(hex(salt), hex(h), ITER, r.compte_id).run();
    await env.DB.prepare('UPDATE reset_tokens SET used = 1 WHERE compte_id = ?').bind(r.compte_id).run();
    await env.DB.prepare('DELETE FROM sessions WHERE compte_id = ?').bind(r.compte_id).run();
    await log(env, r.compte_id, null, 'mot_de_passe_reinit_mail', '');
    return json({ ok: true });
  } catch (_) { return json({ ok: false }, 500); }
}
async function adminExtra(req, env, url, p, me, one, all) {
  const num = (v) => { const n = parseInt(v, 10); return Number.isFinite(n) ? n : 0; };
  const txt = (v, n) => (typeof v === 'string' ? v.trim().slice(0, n) : '');
  if (p === '/api/admin/compte-plus' && req.method === 'GET') {
    const id = num(url.searchParams.get('id'));
    return json({ ok: true, modifs: await all('SELECT id, type, description, statut, created_at FROM modifs WHERE compte_id = ? ORDER BY id DESC LIMIT 30', id),
      notifications: await all('SELECT titre, message, lu, created_at FROM notifications WHERE compte_id = ? ORDER BY id DESC LIMIT 20', id),
      opt_out: ((await one('SELECT opt_out FROM comptes WHERE id = ?', id)) || {}).opt_out || 0 });
  }
  if (p === '/api/admin/communications' && req.method === 'GET') {
    return json({ ok: true, mail_ok: mailOk(env), liste: await all('SELECT id, sujet, nb, nb_mail, notif, statut, created_at FROM communications ORDER BY id DESC LIMIT 30') });
  }
  if (req.method !== 'POST' || !['/api/admin/site', '/api/admin/notifier', '/api/admin/reset-mdp', '/api/admin/modif-statut', '/api/admin/opt-out', '/api/admin/communication'].includes(p)) return null;
  const { b, err } = await readJson(req, url, 40000); if (err) return err;
  if (p === '/api/admin/site') {
    const d = await one('SELECT id, compte_id FROM demandes WHERE id = ?', num(b.id)); if (!d) return json({ ok: false }, 404);
    if (typeof b.suspendu === 'boolean') {
      await env.DB.prepare('UPDATE demandes SET suspendu = ? WHERE id = ?').bind(b.suspendu ? 1 : 0, d.id).run();
      await log(env, d.compte_id, me.id, b.suspendu ? 'site_suspendu' : 'site_reactive', '');
    }
    if (typeof b.site_url === 'string') {
      const su = b.site_url.trim().slice(0, 200);
      if (su && !/^(\/|https:\/\/)[^\s<>"]*$/.test(su)) return json({ ok: false, error: 'url' }, 422);
      await env.DB.prepare('UPDATE demandes SET site_url = ? WHERE id = ?').bind(su, d.id).run();
      await log(env, d.compte_id, me.id, 'site_url', su);
    }
    return json({ ok: true });
  }
  if (p === '/api/admin/notifier') {
    const titre = txt(b.titre, 120), message = txt(b.message, 1000), ids = (Array.isArray(b.ids) ? b.ids : []).map(num).filter(Boolean).slice(0, 500);
    if (!titre || !message || !ids.length) return json({ ok: false }, 422);
    const ok = new Set((await all("SELECT id FROM comptes WHERE role != 'admin'")).map((r) => r.id));
    const cibles = ids.filter((i) => ok.has(i));
    await env.DB.batch(cibles.map((i) => env.DB.prepare('INSERT INTO notifications (compte_id, titre, message) VALUES (?,?,?)').bind(i, titre, message)));
    for (const i of cibles.slice(0, 20)) await log(env, i, me.id, 'notification', titre);
    return json({ ok: true, nb: cibles.length });
  }
  if (p === '/api/admin/reset-mdp') {
    const id = num(b.compte_id), c = await one("SELECT id FROM comptes WHERE id = ? AND role != 'admin'", id); if (!c) return json({ ok: false }, 404);
    const al = 'abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789', r = crypto.getRandomValues(new Uint8Array(12));
    const mdp = Array.from(r, (x) => al[x % al.length]).join('');
    const salt = crypto.getRandomValues(new Uint8Array(16)), h = await pbkdf2(mdp, salt);
    await env.DB.prepare('UPDATE comptes SET salt = ?, hash = ?, iter = ? WHERE id = ?').bind(hex(salt), hex(h), ITER, id).run();
    await env.DB.prepare('DELETE FROM sessions WHERE compte_id = ?').bind(id).run();
    await log(env, id, me.id, 'mot_de_passe_reinit', '');
    return json({ ok: true, mdp });
  }
  if (p === '/api/admin/modif-statut') {
    if (!['demandee', 'faite'].includes(b.statut)) return json({ ok: false }, 422);
    await env.DB.prepare('UPDATE modifs SET statut = ? WHERE id = ?').bind(b.statut, num(b.id)).run();
    return json({ ok: true });
  }
  if (p === '/api/admin/opt-out') {
    await env.DB.prepare("UPDATE comptes SET opt_out = ? WHERE id = ? AND role != 'admin'").bind(b.opt_out ? 1 : 0, num(b.compte_id)).run();
    return json({ ok: true });
  }
  if (p === '/api/admin/communication') {
    const sujet = txt(b.sujet, 150), corps = txt(b.corps, 8000), ids = new Set((Array.isArray(b.ids) ? b.ids : []).map(num).filter(Boolean).slice(0, 1000));
    if (!sujet || corps.length < 5 || !ids.size) return json({ ok: false, error: 'incomplet' }, 422);
    const cibles = (await all("SELECT id, nom, email, opt_out, demo FROM comptes WHERE role != 'admin'")).filter((c) => ids.has(c.id));
    const mail = !!b.mail, notif = !!b.notif;
    if (!mail && !notif) return json({ ok: false, error: 'canal' }, 422);
    const perso = (s, c) => s.replace(/\{prenom\}/gi, (c.nom || '').split(/\s+/)[0] || '').replace(/\{nom\}/gi, c.nom || '');
    let nbNotif = 0, nbMail = 0, statut = 'notif_seule';
    if (notif) {
      await env.DB.batch(cibles.map((c) => env.DB.prepare('INSERT INTO notifications (compte_id, titre, message) VALUES (?,?,?)').bind(c.id, perso(sujet, c), perso(corps, c).slice(0, 1000))));
      nbNotif = cibles.length;
    }
    if (mail) {
      const dest = cibles.filter((c) => !c.opt_out && !c.demo && !/\.invalid$/i.test(c.email));
      if (!mailOk(env)) statut = notif ? 'notif_seule' : 'mail_non_configure';
      else {
        statut = 'envoye';
        for (let i = 0; i < dest.length; i += 100) {
          const lot = dest.slice(i, i + 100).map((c) => {
            const t = perso(corps, c);
            return { from: env.MAIL_FROM, to: [c.email], subject: perso(sujet, c), text: t + '\n\n—\nPour ne plus recevoir ces messages, répondez STOP.',
              html: '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.55;color:#111">' + escH(t).replace(/\n/g, '<br>') + '<hr style="border:0;border-top:1px solid #ddd;margin:24px 0"><p style="font-size:12px;color:#666">Pour ne plus recevoir ces messages, répondez STOP.</p></div>' };
          });
          try {
            const r = await fetch('https://api.resend.com/emails/batch', { method: 'POST', headers: { authorization: 'Bearer ' + env.RESEND_API_KEY, 'content-type': 'application/json' }, body: JSON.stringify(lot) });
            if (r.ok) nbMail += lot.length; else statut = 'partiel';
          } catch (_) { statut = 'partiel'; }
        }
        if (!nbMail && dest.length) statut = 'echec';
      }
    }
    await env.DB.prepare('INSERT INTO communications (sujet, corps, nb, nb_mail, notif, statut, filtre) VALUES (?,?,?,?,?,?,?)').bind(sujet, corps, cibles.length, nbMail, nbNotif ? 1 : 0, statut, txt(b.filtre, 500)).run();
    await log(env, null, me.id, 'communication', sujet + ' (' + cibles.length + ')');
    return json({ ok: true, statut, nb: cibles.length, nb_mail: nbMail, nb_notif: nbNotif, mail_ok: mailOk(env) });
  }
  return null;
}

// ---------- Administration (réservée au rôle admin, jamais pendant une impersonation) ----------
const STATUTS_DEMANDE = ['nouvelle', 'en_creation', 'apercu', 'en_ligne', 'abandonnee'];
const STATUTS_ABO = ['actif', 'impaye', 'suspendu', 'resilie'];
const STATUTS_PLAINTE = ['ouverte', 'en_cours', 'resolue'];
const PRIX = { essentiel: 60, pro: 100 };
const PRIX_MAIL = 4;
async function adminApi(req, env, url, p) {
  let me;
  try { me = await currentUser(req, env); } catch (_) { return json({ ok: false }, 500); }
  if (!me || me.role !== 'admin' || me.par_admin) return json({ ok: false }, 403);
  const one = async (sql, ...a) => env.DB.prepare(sql).bind(...a).first();
  const all = async (sql, ...a) => (await env.DB.prepare(sql).bind(...a).all()).results || [];
  const NOADM = "role != 'admin'";
  try {
    { const x = await adminExtra(req, env, url, p, me, one, all); if (x) return x; }
    if (p === '/api/admin/stats' && req.method === 'GET') {
      const c = await one(`SELECT COUNT(*) total,
        SUM(created_at >= datetime('now','-1 day')) j1, SUM(created_at >= datetime('now','-7 days')) j7, SUM(created_at >= datetime('now','-30 days')) j30,
        SUM(derniere_connexion >= datetime('now','-7 days')) actifs7 FROM comptes WHERE ${NOADM}`);
      const jours = await all(`SELECT date(created_at) d, COUNT(*) n FROM comptes WHERE ${NOADM} AND created_at >= datetime('now','-30 days') GROUP BY d ORDER BY d`);
      const sessions = await one(`SELECT COUNT(DISTINCT s.compte_id) n FROM sessions s JOIN comptes c ON c.id = s.compte_id WHERE c.${NOADM} AND s.expires_at > datetime('now')`);
      const sansDemande = await one(`SELECT COUNT(*) n FROM comptes c WHERE c.${NOADM} AND NOT EXISTS (SELECT 1 FROM demandes d WHERE d.compte_id = c.id)`);
      const dem = await one(`SELECT COUNT(*) total, SUM(created_at >= datetime('now','-7 days')) j7, SUM(created_at >= datetime('now','-30 days')) j30 FROM demandes`);
      const dStatut = await all('SELECT statut, COUNT(*) n FROM demandes GROUP BY statut');
      const dFormule = await all('SELECT formule, COUNT(*) n FROM demandes GROUP BY formule');
      const dAct = await all("SELECT activite, COUNT(*) n FROM demandes GROUP BY activite ORDER BY n DESC LIMIT 8");
      const dVille = await all("SELECT ville, COUNT(*) n FROM demandes WHERE ville != '' GROUP BY lower(ville) ORDER BY n DESC LIMIT 8");
      const dMail = await one('SELECT COALESCE(SUM(mails),0) n FROM demandes');
      const src = await all("SELECT COALESCE(NULLIF(json_extract(utm,'$.utm_source'),''), NULLIF(json_extract(utm,'$.ref'),''), 'direct') s, COUNT(*) n FROM demandes WHERE json_valid(utm) GROUP BY s ORDER BY n DESC LIMIT 8").catch(() => []);
      const ab = await all("SELECT formule, statut, COUNT(*) n, COALESCE(SUM(mails_sup),0) m FROM abonnements GROUP BY formule, statut");
      const abNew = await one("SELECT COUNT(*) n FROM abonnements WHERE debut >= date('now','-30 days')");
      const abRec = await one("SELECT COUNT(*) n FROM abonnements WHERE statut = 'actif' AND debut < date('now','-30 days')");
      const abRes30 = await one("SELECT COUNT(*) n FROM abonnements WHERE statut = 'resilie' AND fin >= date('now','-30 days')");
      const abResTot = await one("SELECT COUNT(*) n FROM abonnements WHERE statut = 'resilie'");
      const motifs = await all("SELECT COALESCE(NULLIF(motif,''),'non précisé') motif, COUNT(*) n FROM abonnements WHERE statut = 'resilie' GROUP BY 1 ORDER BY n DESC LIMIT 6");
      const pl = await one("SELECT COUNT(*) total, SUM(statut='ouverte') ouvertes, SUM(statut='en_cours') en_cours, SUM(statut='resolue') resolues, SUM(created_at >= datetime('now','-30 days')) j30, AVG(CASE WHEN resolved_at IS NOT NULL THEN (julianday(resolved_at) - julianday(created_at)) * 24 END) delai_h FROM plaintes");
      const resa = await one('SELECT COUNT(*) n FROM reservations');
      const j = await all("SELECT type, COUNT(*) n FROM journal WHERE created_at >= datetime('now','-30 days') GROUP BY type");
      let actifs = 0, mrr = 0, mailsSup = 0; const parFormule = { essentiel: 0, pro: 0 };
      for (const r of ab) if (r.statut === 'actif' || r.statut === 'impaye') { actifs += r.n; mailsSup += r.m; mrr += (PRIX[r.formule] || 0) * r.n + PRIX_MAIL * r.m; parFormule[r.formule] = (parFormule[r.formule] || 0) + r.n; }
      const base = actifs + abRes30.n;
      return json({ ok: true,
        comptes: { total: c.total || 0, j1: c.j1 || 0, j7: c.j7 || 0, j30: c.j30 || 0, actifs7: c.actifs7 || 0, connectes: sessions.n, sansDemande: sansDemande.n, jours },
        demandes: { total: dem.total || 0, j7: dem.j7 || 0, j30: dem.j30 || 0, statut: dStatut, formule: dFormule, activite: dAct, ville: dVille, mailsDemandes: dMail.n, sources: src },
        abonnements: { actifs, parFormule, nouveaux30: abNew.n, recurrents: abRec.n, resilies30: abRes30.n, resiliesTotal: abResTot.n, impayes: ab.filter((r) => r.statut === 'impaye').reduce((x, r) => x + r.n, 0), suspendus: ab.filter((r) => r.statut === 'suspendu').reduce((x, r) => x + r.n, 0), mailsSup, mrr, arr: mrr * 12, panier: actifs ? Math.round((mrr / actifs) * 10) / 10 : 0, churn: base ? Math.round((abRes30.n / base) * 1000) / 10 : 0, motifs, detail: ab },
        plaintes: { total: pl.total || 0, ouvertes: pl.ouvertes || 0, en_cours: pl.en_cours || 0, resolues: pl.resolues || 0, j30: pl.j30 || 0, delai_h: pl.delai_h == null ? null : Math.round(pl.delai_h * 10) / 10 },
        conversion: { inscritDemande: c.total ? Math.round(((c.total - sansDemande.n) / c.total) * 1000) / 10 : 0, demandeAbonne: dem.total ? Math.round(((actifs + abResTot.n) / dem.total) * 1000) / 10 : 0 },
        divers: { reservationsDemo: resa.n, evenements30: j } });
    }
    if (p === '/api/admin/donnees' && req.method === 'GET') {
      return json({ ok: true,
        comptes: await all(`SELECT id, nom, email, created_at, derniere_connexion, opt_out, demo FROM comptes WHERE ${NOADM} ORDER BY id DESC LIMIT 2000`),
        abonnements: await all('SELECT compte_id, formule, statut, mails_sup, debut, fin, motif, created_at FROM abonnements LIMIT 5000'),
        demandes: await all('SELECT compte_id, ref, commerce, activite, ville, domaine, mails, tel, formule, statut, suspendu, site_url, utm, message, created_at FROM demandes ORDER BY id DESC LIMIT 3000'),
        plaintes: await all('SELECT compte_id, sujet, message, statut, created_at, resolved_at FROM plaintes ORDER BY id DESC LIMIT 3000'),
        journal: await all('SELECT compte_id, type, detail, created_at FROM journal ORDER BY id DESC LIMIT 500') });
    }
    if (p === '/api/admin/comptes' && req.method === 'GET') {
      const q = (url.searchParams.get('q') || '').trim().slice(0, 60).replace(/[%_\\]/g, '');
      const like = '%' + q + '%';
      const rows = await all(`SELECT c.id, c.nom, c.email, c.created_at, c.derniere_connexion,
        (SELECT COUNT(*) FROM demandes d WHERE d.compte_id = c.id) demandes,
        (SELECT statut FROM demandes d WHERE d.compte_id = c.id ORDER BY d.id DESC LIMIT 1) statut_site,
        a.formule, a.statut abo, (SELECT COUNT(*) FROM plaintes x WHERE x.compte_id = c.id AND x.statut != 'resolue') plaintes_ouvertes
        FROM comptes c LEFT JOIN abonnements a ON a.compte_id = c.id WHERE c.${NOADM} AND (c.nom LIKE ?1 OR c.email LIKE ?1) ORDER BY c.id DESC LIMIT 200`, like);
      return json({ ok: true, comptes: rows });
    }
    if (p === '/api/admin/compte' && req.method === 'GET') {
      const id = parseInt(url.searchParams.get('id'), 10);
      const cpt = await one('SELECT id, nom, email, created_at, derniere_connexion, role FROM comptes WHERE id = ?', id);
      if (!cpt) return json({ ok: false }, 404);
      return json({ ok: true, compte: cpt,
        demandes: await all('SELECT id, ref, created_at, commerce, activite, ville, domaine, mails, tel, message, formule, statut, suspendu, site_url FROM demandes WHERE compte_id = ? ORDER BY id DESC', id),
        abonnement: await one('SELECT * FROM abonnements WHERE compte_id = ?', id),
        plaintes: await all('SELECT * FROM plaintes WHERE compte_id = ? ORDER BY id DESC', id),
        journal: await all('SELECT type, detail, created_at, admin_id FROM journal WHERE compte_id = ? ORDER BY id DESC LIMIT 30', id) });
    }
    if (req.method !== 'POST') return json({ ok: false }, 405);
    const { b, err } = await readJson(req, url, 4000); if (err) return err;
    const num = (v) => { const n = parseInt(v, 10); return Number.isFinite(n) ? n : 0; };
    const txt = (v, n) => (typeof v === 'string' ? v.trim().slice(0, n) : '');
    if (p === '/api/admin/demande') {
      if (!STATUTS_DEMANDE.includes(b.statut)) return json({ ok: false }, 422);
      const d = await one('SELECT compte_id FROM demandes WHERE id = ?', num(b.id)); if (!d) return json({ ok: false }, 404);
      await env.DB.prepare('UPDATE demandes SET statut = ? WHERE id = ?').bind(b.statut, num(b.id)).run();
      await log(env, d.compte_id, me.id, 'site_statut', b.statut);
      return json({ ok: true });
    }
    if (p === '/api/admin/abonnement') {
      const cid = num(b.compte_id); if (!(await one("SELECT id FROM comptes WHERE id = ? AND role != 'admin'", cid))) return json({ ok: false }, 404);
      if (!FORMULES.includes(b.formule) || !STATUTS_ABO.includes(b.statut)) return json({ ok: false }, 422);
      const mails = Math.min(Math.max(num(b.mails_sup), 0), 50), motif = txt(b.motif, 200);
      const ex = await one('SELECT * FROM abonnements WHERE compte_id = ?', cid);
      if (!ex) {
        await env.DB.prepare("INSERT INTO abonnements (compte_id, formule, statut, mails_sup, debut, fin, motif) VALUES (?,?,?,?,date('now'),?,?)").bind(cid, b.formule, b.statut, mails, b.statut === 'resilie' ? new Date().toISOString().slice(0, 10) : null, motif).run();
        await log(env, cid, me.id, 'abonnement_cree', b.formule + ' / ' + b.statut);
      } else {
        const fin = b.statut === 'resilie' ? (ex.fin || new Date().toISOString().slice(0, 10)) : null;
        const debut = ex.statut === 'resilie' && b.statut !== 'resilie' ? new Date().toISOString().slice(0, 10) : ex.debut;
        await env.DB.prepare("UPDATE abonnements SET formule = ?, statut = ?, mails_sup = ?, debut = ?, fin = ?, motif = ?, updated_at = datetime('now') WHERE compte_id = ?").bind(b.formule, b.statut, mails, debut, fin, b.statut === 'resilie' ? motif : '', cid).run();
        if (ex.statut !== b.statut) await log(env, cid, me.id, b.statut === 'resilie' ? 'resiliation' : 'abonnement_statut', b.statut + (motif ? ' : ' + motif : ''));
        if (ex.formule !== b.formule) await log(env, cid, me.id, 'changement_formule', ex.formule + ' → ' + b.formule);
      }
      return json({ ok: true });
    }
    if (p === '/api/admin/plainte') {
      const cid = num(b.compte_id), sujet = txt(b.sujet, 120);
      if (!sujet || !(await one('SELECT id FROM comptes WHERE id = ?', cid))) return json({ ok: false }, 422);
      await env.DB.prepare('INSERT INTO plaintes (compte_id, sujet, message) VALUES (?,?,?)').bind(cid, sujet, txt(b.message, 1500)).run();
      await log(env, cid, me.id, 'plainte', sujet);
      return json({ ok: true });
    }
    if (p === '/api/admin/plainte-statut') {
      if (!STATUTS_PLAINTE.includes(b.statut)) return json({ ok: false }, 422);
      const x = await one('SELECT compte_id FROM plaintes WHERE id = ?', num(b.id)); if (!x) return json({ ok: false }, 404);
      await env.DB.prepare("UPDATE plaintes SET statut = ?, resolved_at = CASE WHEN ? = 'resolue' THEN datetime('now') ELSE NULL END WHERE id = ?").bind(b.statut, b.statut, num(b.id)).run();
      await log(env, x.compte_id, me.id, 'plainte_statut', b.statut);
      return json({ ok: true });
    }
    if (p === '/api/admin/impersonate') {
      const t = await one("SELECT id, nom FROM comptes WHERE id = ? AND role != 'admin'", num(b.compte_id));
      if (!t) return json({ ok: false }, 404);
      await log(env, t.id, me.id, 'admin_impersonation', 'début');
      const token = await newSession(env, t.id, me.id);
      const res = json({ ok: true, nom: t.nom });
      res.headers.append('set-cookie', sessionCookie(token, 7200));
      return res;
    }
    return json({ ok: false }, 404);
  } catch (e) { return json({ ok: false, error: 'serveur' }, 500); }
}
function parisToday() {
  return new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Paris' }).format(new Date());
}
function addDays(iso, n) { const d = new Date(iso + 'T12:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); }
function validDay(iso) {
  if (typeof iso !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(iso)) return false;
  const w = new Date(iso + 'T12:00:00Z').getUTCDay();
  if (w < 2 || w > 6) return false;
  const t = parisToday();
  return iso >= addDays(t, 1) && iso <= addDays(t, 45);
}
function plusMin(h, min) { const [a, b] = h.split(':').map(Number); const t = a * 60 + b + min; return String(Math.floor(t / 60)).padStart(2, '0') + ':' + String(t % 60).padStart(2, '0'); }

async function creneaux(req, env, url) {
  const date = url.searchParams.get('date');
  if (!validDay(date)) return json({ ok: false }, 422);
  try {
    await env.DB.prepare("DELETE FROM reservations WHERE created_at < datetime('now','-1 day')").run();
    const r = await env.DB.prepare("SELECT heure FROM reservations WHERE site = 'demo' AND jour = ?").bind(date).all();
    return json({ ok: true, taken: (r.results || []).map((x) => x.heure) });
  } catch (_) { return json({ ok: false }, 500); }
}

async function reservation(req, env, url) {
  if (req.method !== 'POST') return json({ ok: false }, 405);
  const origin = req.headers.get('origin');
  if (origin && origin !== url.origin) return json({ ok: false }, 403);
  const raw = await req.text();
  if (raw.length > 2000) return json({ ok: false }, 413);
  let b;
  try { b = JSON.parse(raw); } catch (_) { return json({ ok: false }, 400); }
  if (!b || typeof b !== 'object') return json({ ok: false }, 400);
  const alphabet = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
  const rnd = crypto.getRandomValues(new Uint8Array(6));
  const ref = 'RDV-' + Array.from(rnd, (x) => alphabet[x % alphabet.length]).join('');
  if (b.site_web_url) return json({ ok: true, ref });
  const nom = typeof b.nom === 'string' ? b.nom.trim() : '';
  const tel = typeof b.tel === 'string' ? b.tel.trim() : '';
  const n = SERVICES[b.service];
  if (nom.length < 2 || nom.length > 40) return json({ ok: false, error: 'Prénom invalide.' }, 422);
  if (tel && !/^[0-9+().\s-]{8,20}$/.test(tel)) return json({ ok: false, error: 'Numéro invalide.' }, 422);
  if (!n || !validDay(b.date) || !UNITS.includes(b.heure)) return json({ ok: false, error: 'Créneau invalide.' }, 422);
  const used = [];
  for (let i = 0; i < n; i++) { const u = plusMin(b.heure, 30 * i); if (!UNITS.includes(u)) return json({ ok: false, error: 'Créneau trop court pour cette prestation.' }, 422); used.push(u); }
  const ip = req.headers.get('cf-connecting-ip') || 'inconnue';
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(ip + '|rdv'));
  const iph = Array.from(new Uint8Array(buf).slice(0, 8), (x) => x.toString(16).padStart(2, '0')).join('');
  try {
    await env.DB.prepare("DELETE FROM reservations WHERE created_at < datetime('now','-1 day')").run();
    const c = await env.DB.prepare("SELECT COUNT(DISTINCT ref) AS n FROM reservations WHERE ip_hash = ? AND created_at > datetime('now','-1 hour')").bind(iph).first();
    if (c && c.n >= 6) return json({ ok: false }, 429);
    const st = env.DB.prepare("INSERT INTO reservations (ref, site, jour, heure, service, nom, tel, ip_hash) VALUES (?,?,?,?,?,?,?,?)");
    await env.DB.batch(used.map((h) => st.bind(ref, 'demo', b.date, h, b.service, nom, tel.slice(0, 20), iph)));
  } catch (e) {
    if (String(e && e.message).includes('UNIQUE')) return json({ ok: false }, 409);
    return json({ ok: false }, 500);
  }
  return json({ ok: true, ref });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    let p = url.pathname;
    if (p.length > 1 && p.endsWith('/')) p = p.slice(0, -1);
    if (p.startsWith('/api/espace')) return espace(req, env, url, p);
    if (p === '/api/mot-de-passe-oublie') return oubli(req, env, url);
    if (p === '/api/reinitialiser') return reinitialiser(req, env, url);
    if (p === '/api/demande') return demande(req, env, url);
    if (p === '/api/reservation') return reservation(req, env, url);
    if (p === '/api/inscription') return inscription(req, env, url);
    if (p === '/api/connexion') return connexion(req, env, url);
    if (p === '/api/deconnexion') return deconnexion(req, env, url);
    if (p === '/api/moi' && req.method === 'GET') return moi(req, env);
    if (p === '/api/quitter-impersonation') return quitterImpersonation(req, env, url);
    if (p === '/api/mot-de-passe') return motDePasse(req, env, url);
    if (p.startsWith('/api/admin/')) return adminApi(req, env, url, p);
    if (p === '/api/creneaux' && req.method === 'GET') return creneaux(req, env, url);
    if (req.method !== 'GET' && req.method !== 'HEAD') return new Response('Méthode non autorisée', { status: 405 });
    if (p === '/index.html' || (p.endsWith('.html') && p !== '/404.html')) {
      const clean = p === '/index.html' ? '/' : p.slice(0, -5);
      return Response.redirect(url.origin + clean + url.search, 301);
    }
    let file = ROUTES[p];
    if (!file && (/^\/assets\/[a-z0-9._\/-]+$/i.test(p) && !p.includes('..'))) file = p.slice(1);
    if (!file && (p === '/robots.txt' || p === '/sitemap.xml')) file = p.slice(1);
    if (file) {
      const r = await fromGithub(file);
      if (r) return r;
    }
    const nf = await fromGithub('404.html', 404);
    return nf || new Response('Page introuvable', { status: file ? 502 : 404 });
  },
};
