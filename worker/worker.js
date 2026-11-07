// Worker Cloudflare : sert le site depuis GitHub (dossier /site) et reçoit les demandes du formulaire (base D1).
const REPO = 'https://raw.githubusercontent.com/heuss75/Cr-ation-Web/main/site';
const ROUTES = {
  '/': 'index.html', '/offre': 'offre.html', '/faq': 'faq.html', '/contact': 'contact.html', '/commander': 'commander.html', '/connexion': 'connexion.html',
  '/mentions-legales': 'mentions-legales.html', '/cgv': 'cgv.html', '/confidentialite': 'confidentialite.html', '/cookies': 'cookies.html', '/guide-messagerie': 'guide-messagerie.html',
  '/reservation-demo': 'reservation-demo.html', '/inscription': 'inscription.html', '/admin': 'admin.html', '/espace': 'espace.html', '/mot-de-passe-oublie': 'mot-de-passe-oublie.html', '/reinitialiser': 'reinitialiser.html', '/exemples/bistro': 'exemples/bistro.html', '/exemples/salon': 'exemples/salon.html', '/exemples/artisan': 'exemples/artisan.html', '/exemples/bistro-reservation-client': 'exemples/bistro-reservation-client.html', '/exemples/bistro-reservation-interne': 'exemples/bistro-reservation-interne.html', '/exemples/osteo-reservation-interne': 'exemples/osteo-reservation-interne.html', '/exemples/salon-reservation-interne': 'exemples/salon-reservation-interne.html',
};
const TYPES = {
  html: 'text/html; charset=utf-8', css: 'text/css; charset=utf-8', js: 'text/javascript; charset=utf-8', json: 'application/json; charset=utf-8',
  txt: 'text/plain; charset=utf-8', xml: 'application/xml; charset=utf-8', svg: 'image/svg+xml', woff2: 'font/woff2', png: 'image/png',
  jpg: 'image/jpeg', webp: 'image/webp', ico: 'image/x-icon',
};
const SEC = {
  'x-content-type-options': 'nosniff', 'referrer-policy': 'strict-origin-when-cross-origin', 'x-frame-options': 'SAMEORIGIN',
  'permissions-policy': 'camera=(), microphone=(), geolocation=()', 'strict-transport-security': 'max-age=31536000',
  'content-security-policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: blob:; connect-src 'self'; frame-ancestors 'self'; base-uri 'self'; form-action 'self'; object-src 'none'",
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
  if (s('metier')) { if (s('metier').length < 2 || s('metier').length > 60) e.activite = 'Indiquez votre activité (2 à 60 caractères).'; }
  else if (!ACTIVITES.includes(s('activite'))) e.activite = 'Indiquez votre activité.';
  if (s('activite') && !ACTIVITES.includes(s('activite'))) e.activite = 'Activité invalide.';
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
    const deja = await env.DB.prepare("SELECT ref FROM demandes WHERE compte_id = ? AND statut != 'abandonnee' ORDER BY id DESC LIMIT 1").bind(user.id).first();
    if (deja) return json({ ok: false, error: 'deja', ref: deja.ref }, 409);
    let utm = '';
    if (b.utm && typeof b.utm === 'object') {
      const o = {};
      for (const k of ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'ref', 'landing']) if (typeof b.utm[k] === 'string') o[k] = b.utm[k].slice(0, 100);
      utm = JSON.stringify(o).slice(0, 600);
    }
    const t = (k, n) => (typeof b[k] === 'string' ? b[k].trim().slice(0, n) : '');
    await ensureSchema(env);
    await env.DB.prepare('INSERT INTO demandes (ref, nom, email, tel, commerce, activite, metier, ville, domaine, mails, message, utm, page, ip_hash, ua, formule, compte_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
      .bind(ref, t('nom', 80), t('email', 120), t('tel', 20), t('commerce', 80), ACTIVITES.includes(t('activite', 20)) ? t('activite', 20) : 'autre', (t('metier', 60) || null), t('ville', 60), t('domaine', 70), parseInt(b.mails, 10) || 0, t('message', 1000), utm, t('page', 60), iph, (req.headers.get('user-agent') || '').slice(0, 200), t('formule', 12), user.id).run();
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
const mailOk0 = (env) => !!(env.RESEND_API_KEY && env.MAIL_FROM);
async function ensureCodes(env) {
  await env.DB.prepare("CREATE TABLE IF NOT EXISTS codes_mail (email TEXT PRIMARY KEY, code_hash TEXT NOT NULL, essais INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL DEFAULT (datetime('now')), expires_at TEXT NOT NULL)").run();
}
async function inscriptionConfig(env) { return json({ ok: true, verif: mailOk0(env) }); }
async function inscriptionCode(req, env, url) {
  if (req.method !== 'POST') return json({ ok: false }, 405);
  const { b, err } = await readJson(req, url); if (err) return err;
  if (b.site_web_url) return json({ ok: true });
  if (!mailOk0(env)) return json({ ok: false, error: 'indisponible' }, 503);
  const email = typeof b.email === 'string' ? b.email.trim().toLowerCase() : '';
  if (!MAIL_RE.test(email) || email.length > 120) return json({ ok: false, errors: { email: 'Adresse e-mail invalide.' } }, 422);
  try {
    await ensureCodes(env);
    const iph = await ipHash(req, 'code');
    await env.DB.prepare("DELETE FROM essais WHERE at < datetime('now','-1 day')").run();
    const c = await env.DB.prepare("SELECT COUNT(*) AS n FROM essais WHERE ip_hash = ? AND at > datetime('now','-1 hour')").bind(iph).first();
    if (c && c.n >= 8) return json({ ok: false }, 429);
    if (await env.DB.prepare('SELECT id FROM comptes WHERE email = ?').bind(email).first()) {
      // Même réponse qu'un envoi réussi (pas de fuite sur les adresses inscrites) ; la personne est prévenue par e-mail.
      await env.DB.prepare('INSERT INTO essais (ip_hash) VALUES (?)').bind(iph).run();
      await envoyerMail(env, email, 'Vous avez déjà un compte Devanture Web',
        'Bonjour,\n\nUne inscription vient d’être demandée avec cette adresse, mais vous avez déjà un compte Devanture Web. Connectez-vous : ' + url.origin + '/connexion\n(mot de passe oublié : ' + url.origin + '/mot-de-passe-oublie)\n\nSi vous n’êtes pas à l’origine de cette demande, ignorez ce message.\n\nDevanture Web',
        '<div style="font-family:system-ui,sans-serif;max-width:480px;margin:auto;padding:24px"><p>Une inscription vient d’être demandée avec cette adresse, mais vous avez déjà un compte Devanture Web.</p><p><a href="' + url.origin + '/connexion">Me connecter</a> · <a href="' + url.origin + '/mot-de-passe-oublie">Mot de passe oublié</a></p><p style="color:#666;font-size:13px">Si vous n’êtes pas à l’origine de cette demande, ignorez ce message.</p></div>');
      return json({ ok: true });
    }
    const ex = await env.DB.prepare("SELECT 1 AS x FROM codes_mail WHERE email = ? AND created_at > datetime('now','-30 seconds')").bind(email).first();
    if (ex) return json({ ok: false, error: 'attente' }, 429);
    await env.DB.prepare('INSERT INTO essais (ip_hash) VALUES (?)').bind(iph).run();
    const code = String(crypto.getRandomValues(new Uint32Array(1))[0] % 1000000).padStart(6, '0');
    await env.DB.prepare("INSERT OR REPLACE INTO codes_mail (email, code_hash, essais, created_at, expires_at) VALUES (?,?,0,datetime('now'),datetime('now','+10 minutes'))").bind(email, await sha(code + '|' + email)).run();
    const ok = await envoyerMail(env, email, 'Votre code de vérification : ' + code,
      'Bonjour,\n\nVotre code de vérification Devanture Web est : ' + code + '\n\nIl est valable 10 minutes. Si vous n’êtes pas à l’origine de cette demande, ignorez ce message.\n\nDevanture Web',
      '<div style="font-family:system-ui,sans-serif;max-width:480px;margin:auto;padding:24px"><h2 style="margin:0 0 12px">Votre code de vérification</h2><p>Saisissez ce code pour créer votre compte Devanture Web :</p><p style="font-size:34px;letter-spacing:8px;font-weight:800;margin:20px 0">' + code + '</p><p style="color:#666">Il est valable 10 minutes. Si vous n’êtes pas à l’origine de cette demande, ignorez ce message.</p></div>');
    if (!ok) return json({ ok: false, error: 'envoi' }, 502);
    return json({ ok: true });
  } catch (_) { return json({ ok: false }, 500); }
}
async function codeValide(env, email, code) {
  await ensureCodes(env);
  const r = await env.DB.prepare("SELECT code_hash, essais FROM codes_mail WHERE email = ? AND expires_at > datetime('now')").bind(email).first();
  if (!r) return 'expire';
  if (r.essais >= 5) { await env.DB.prepare('DELETE FROM codes_mail WHERE email = ?').bind(email).run(); return 'trop'; }
  if (!/^[0-9]{6}$/.test(code) || !same(unhex(r.code_hash), unhex(await sha(code + '|' + email)))) {
    await env.DB.prepare('UPDATE codes_mail SET essais = essais + 1 WHERE email = ?').bind(email).run(); return 'faux';
  }
  await env.DB.prepare('DELETE FROM codes_mail WHERE email = ?').bind(email).run();
  return 'ok';
}
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
  if (mailOk0(env)) {
    const v = await codeValide(env, email, typeof b.code === 'string' ? b.code.trim() : '').catch(() => 'erreur');
    if (v !== 'ok') return json({ ok: false, errors: { code: v === 'faux' ? 'Code incorrect.' : v === 'trop' ? 'Trop d’essais : demandez un nouveau code.' : 'Code expiré ou absent : demandez un nouveau code.' } }, 422);
  }
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
    let parrain = null;
    if (typeof b.parrain === 'string' && b.parrain.trim()) { try { await ensureSchema(env); const r = await appliquerParrain(env, id, b.parrain); parrain = r.ok ? 'ok' : r.error; } catch (_) { parrain = 'erreur'; } }
    const token = await newSession(env, id);
    const res = json({ ok: true, nom, parrain });
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
const ABO_BLOQUE = ['impaye', 'suspendu', 'resilie']; // pas de nouvelle modification tant que l'abonnement n'est pas régularisé
const premierDuMois = () => new Date().toISOString().slice(0, 7) + '-01';
async function espace(req, env, url, p) {
  let u;
  try { u = await currentUser(req, env); } catch (_) { return json({ ok: false }, 500); }
  if (!u) return json({ ok: false }, 401);
  const one = (sql, ...a) => env.DB.prepare(sql).bind(...a).first();
  const all = async (sql, ...a) => (await env.DB.prepare(sql).bind(...a).all()).results || [];
  const lecture = !!u.par_admin;
  try {
    if (V2_ESPACE.has(p)) return await espaceV2(req, env, url, p, u, lecture);
    if (p === '/api/espace/editeur' || p === '/api/espace/contenu' || p === '/api/espace/media') return await espaceEdit(req, env, url, p, u, lecture);
    if (p === '/api/espace' && req.method === 'GET') {
      const compte = await one('SELECT nom, email, created_at, opt_out FROM comptes WHERE id = ?', u.id);
      const demandes = await all('SELECT id, ref, created_at, commerce, COALESCE(metier, activite) AS activite, ville, domaine, mails, tel, formule, statut, suspendu, site_url FROM demandes WHERE compte_id = ? ORDER BY id DESC', u.id);
      await appliquerChangements(env);
      const abo = await one('SELECT formule, statut, mails_sup, debut, fin FROM abonnements WHERE compte_id = ?', u.id);
      const formule = abo ? abo.formule : (demandes[0] ? demandes[0].formule : 'essentiel');
      const used = await one('SELECT COUNT(*) n FROM modifs WHERE compte_id = ? AND created_at >= ?', u.id, premierDuMois());
      return json({ ok: true, lecture, compte, demandes, abonnement: abo, formule, quota: MOIS_QUOTA[formule] || 1, utilisees: used ? used.n : 0, prix: PRIX, prix_mail: PRIX_MAIL,
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
      if (!d) return json({ ok: false, error: 'aucune-demande' }, 404);
      if (d.suspendu) return json({ ok: false, error: 'suspendu' }, 403);
      if (!['apercu', 'en_ligne'].includes(d.statut)) return json({ ok: false, error: 'pas-en-ligne' }, 409);
      const abo = await one('SELECT formule, statut FROM abonnements WHERE compte_id = ?', u.id);
      if (abo && ABO_BLOQUE.includes(abo.statut)) return json({ ok: false, error: 'abonnement' }, 403);
      const quota = MOIS_QUOTA[abo ? abo.formule : d.formule] || 1;
      const used = await one('SELECT COUNT(*) n FROM modifs WHERE compte_id = ? AND created_at >= ?', u.id, premierDuMois());
      if (used.n >= quota) return json({ ok: false, error: 'quota' }, 409);
      const type = ['texte', 'photo', 'bloc', 'autre'].includes(b.type) ? b.type : 'autre', desc = txt(b.description, 1200);
      if (desc.length < 5) return json({ ok: false, error: 'vide' }, 422);
      await env.DB.prepare('INSERT INTO modifs (compte_id, type, description) VALUES (?,?,?)').bind(u.id, type, desc).run();
      await log(env, u.id, null, 'modification', type);
      return json({ ok: true });
    }
    if (p === '/api/espace/opt-out') {
      await env.DB.prepare('UPDATE comptes SET opt_out = ? WHERE id = ?').bind(b.opt_out ? 1 : 0, u.id).run();
      await log(env, u.id, null, 'opt-out', b.opt_out ? 'oui' : 'non');
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
async function unsubTok(env, id) { return (await sha((env.UNSUB_SECRET || env.RESEND_API_KEY || 'dev') + '|unsub|' + id)).slice(0, 32); }
async function desinscription(req, env, url) {
  const t = url.searchParams.get('t') || '', m = t.match(/^(\d{1,9})\.([0-9a-f]{32})$/);
  const page = (titre, corps) => new Response('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Désinscription | Devanture Web</title></head><body style="font-family:system-ui,sans-serif;max-width:480px;margin:12vh auto;padding:0 20px;line-height:1.5"><h1 style="font-size:22px">' + titre + '</h1>' + corps + '</body></html>', { headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store', ...SEC } });
  if (!m || !same(unhex(await unsubTok(env, m[1])), unhex(m[2]))) return page('Lien invalide', '<p>Ce lien de désinscription n’est pas valide.</p>');
  if (req.method === 'POST') {
    await env.DB.prepare("UPDATE comptes SET opt_out = 1 WHERE id = ? AND role != 'admin'").bind(parseInt(m[1], 10)).run();
    await log(env, parseInt(m[1], 10), null, 'opt-out', 'lien e-mail');
    return page('C’est noté', '<p>Vous ne recevrez plus nos e-mails de communication. Les messages liés à votre compte (code, mot de passe) continuent d’être envoyés.</p>');
  }
  if (req.method !== 'GET') return new Response('Méthode non autorisée', { status: 405 });
  return page('Ne plus recevoir nos e-mails ?', '<p>Confirmez pour ne plus recevoir les e-mails de communication de Devanture Web.</p><form method="post"><button style="font:inherit;padding:10px 18px;border-radius:8px;border:0;background:#111;color:#fff;cursor:pointer">Me désinscrire</button></form>');
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
      const texte = 'Bonjour ' + prenom + ',\n\nVous avez demandé à changer votre mot de passe Devanture Web. Ouvrez ce lien (valable 1 heure) :\n' + lien + '\n\nSi vous n’êtes pas à l’origine de cette demande, ignorez ce message : votre mot de passe ne change pas.';
      const ok = await envoyerMail(env, email, 'Votre nouveau mot de passe Devanture Web', texte,
        '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.55;color:#111"><p>Bonjour ' + escH(prenom) + ',</p><p>Vous avez demandé à changer votre mot de passe Devanture Web.</p><p><a href="' + lien + '" style="display:inline-block;background:#0b0b0c;color:#fff;padding:12px 20px;border-radius:10px;text-decoration:none;font-weight:bold">Choisir un nouveau mot de passe</a></p><p style="font-size:13px;color:#555">Le lien est valable 1 heure. Si vous n’êtes pas à l’origine de cette demande, ignorez ce message : votre mot de passe ne change pas.</p></div>');
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
const SITE_RE = /^\/exemples\/(bistro|salon|artisan|fleuriste|garage|osteo)$/;
const PAGE_SUSPENDU = '<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Site momentanément indisponible</title><body style="font-family:system-ui,sans-serif;display:grid;place-items:center;min-height:100vh;margin:0;background:#f5f6f6;color:#0b0b0c;text-align:center;padding:24px"><div><h1 style="margin:0 0 8px">Site momentanément indisponible</h1><p style="color:#5e5e64">Ce site est en cours de maintenance. Merci de revenir un peu plus tard.</p></div></body></html>';
async function champsDe(sitePath) {
  const r = await fromGithub(sitePath.slice(1) + '.edit.json');
  if (!r) return null;
  try { return (await r.json()).champs || null; } catch (_) { return null; }
}
async function exemple(req, env, p) {
  const r = await fromGithub(p.slice(1) + '.html');
  if (!r) return null;
  let d = null;
  try { d = await env.DB.prepare("SELECT d.compte_id, d.suspendu, c.demo, COALESCE(a.formule, d.formule) formule FROM demandes d JOIN comptes c ON c.id = d.compte_id LEFT JOIN abonnements a ON a.compte_id = d.compte_id WHERE d.site_url = ? ORDER BY d.id DESC LIMIT 1").bind(p).first(); } catch (_) {}
  if (!d) return r;
  if (d.suspendu && !d.demo) return new Response(PAGE_SUSPENDU, { status: 503, headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' } });
  if (d.formule !== 'pro') return r;
  const rows = (await env.DB.prepare('SELECT cle, valeur FROM contenus WHERE compte_id = ?').bind(d.compte_id).all()).results || [];
  if (!rows.length) return r;
  const ov = {}; rows.forEach((x) => { ov[x.cle] = x.valeur; });
  const out = new HTMLRewriter().on('[data-k]', { element(el) {
    const v = ov[el.getAttribute('data-k')];
    if (v === undefined) return;
    if (el.tagName === 'img') { if (/^\/media\/\d+$/.test(v)) { el.setAttribute('src', v); el.removeAttribute('srcset'); } } else el.setInnerContent(String(v));
  } }).transform(r);
  const h = new Headers(out.headers); h.set('cache-control', 'no-store');
  return new Response(out.body, { status: out.status, headers: h });
}
async function media(env, id) {
  const m = await env.DB.prepare('SELECT mime, data FROM medias WHERE id = ?').bind(id).first();
  if (!m) return null;
  const bin = atob(m.data), a = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) a[i] = bin.charCodeAt(i);
  return new Response(a, { headers: { 'content-type': m.mime, 'cache-control': 'public, max-age=31536000, immutable', 'x-content-type-options': 'nosniff' } });
}
async function espaceEdit(req, env, url, p, u, lecture) {
  const d = await env.DB.prepare("SELECT d.id, d.site_url, d.suspendu, COALESCE(a.formule, d.formule) formule FROM demandes d LEFT JOIN abonnements a ON a.compte_id = d.compte_id WHERE d.compte_id = ? ORDER BY d.id DESC LIMIT 1").bind(u.id).first();
  if (!d || d.formule !== 'pro') return json({ ok: false, error: 'pro' }, 403);
  const aboE = await env.DB.prepare('SELECT statut FROM abonnements WHERE compte_id = ?').bind(u.id).first();
  const bloque = !!(aboE && ABO_BLOQUE.includes(aboE.statut));
  if (!d.site_url || !SITE_RE.test(d.site_url)) return json({ ok: false, error: 'pas-pret' }, 409);
  const champs = await champsDe(d.site_url);
  if (!champs) return json({ ok: false, error: 'pas-pret' }, 409);
  if (p === '/api/espace/editeur' && req.method === 'GET') {
    const rows = (await env.DB.prepare('SELECT cle, valeur FROM contenus WHERE compte_id = ?').bind(u.id).all()).results || [];
    const ov = {}; rows.forEach((x) => { ov[x.cle] = x.valeur; });
    return json({ ok: true, lecture, site_url: d.site_url, suspendu: d.suspendu, abo_bloque: bloque ? aboE.statut : null, champs: champs.map((c) => ({ k: c.k, type: c.type, sec: c.sec, v: c.v, val: ov[c.k] === undefined ? null : ov[c.k] })) });
  }
  if (req.method !== 'POST') return json({ ok: false }, 405);
  if (lecture) return json({ ok: false, error: 'lecture-seule' }, 403);
  if (bloque) return json({ ok: false, error: 'abonnement' }, 403);
  if (d.suspendu) return json({ ok: false, error: 'suspendu' }, 403);
  if (p === '/api/espace/media') {
    const { b, err } = await readJson(req, url, 1600000); if (err) return err;
    const mime = ['image/jpeg', 'image/png', 'image/webp'].includes(b.mime) ? b.mime : '';
    if (!mime || typeof b.data !== 'string' || !/^[A-Za-z0-9+/=]+$/.test(b.data)) return json({ ok: false, error: 'format' }, 422);
    let bin; try { bin = atob(b.data); } catch (_) { return json({ ok: false, error: 'format' }, 422); }
    if (bin.length > 1200000 || bin.length < 100) return json({ ok: false, error: 'taille' }, 413);
    const sig = bin.slice(0, 12), okSig = (mime === 'image/jpeg' && sig.startsWith('\xff\xd8\xff')) || (mime === 'image/png' && sig.startsWith('\x89PNG')) || (mime === 'image/webp' && sig.startsWith('RIFF') && sig.slice(8, 12) === 'WEBP');
    if (!okSig) return json({ ok: false, error: 'format' }, 422);
    const n = await env.DB.prepare('SELECT COUNT(*) n FROM medias WHERE compte_id = ?').bind(u.id).first();
    if (n.n >= 60) return json({ ok: false, error: 'limite' }, 409);
    const r = await env.DB.prepare('INSERT INTO medias (compte_id, mime, data) VALUES (?,?,?)').bind(u.id, mime, b.data).run();
    return json({ ok: true, url: '/media/' + r.meta.last_row_id });
  }
  if (p === '/api/espace/contenu') {
    const { b, err } = await readJson(req, url, 6000); if (err) return err;
    const c = champs.find((x) => x.k === b.k);
    if (!c) return json({ ok: false, error: 'cle' }, 422);
    if (b.reset === true) {
      await env.DB.prepare('DELETE FROM contenus WHERE compte_id = ? AND cle = ?').bind(u.id, c.k).run();
      return json({ ok: true });
    }
    let v = typeof b.valeur === 'string' ? b.valeur.replace(/[\u0000-\u0008\u000b-\u001f]/g, '').trim() : '';
    if (c.type === 'img') {
      const m = v.match(/^\/media\/(\d+)$/);
      if (!m || !(await env.DB.prepare('SELECT id FROM medias WHERE id = ? AND compte_id = ?').bind(parseInt(m[1], 10), u.id).first())) return json({ ok: false, error: 'media' }, 422);
    } else if (v.length < 1 || v.length > 600) return json({ ok: false, error: 'texte' }, 422);
    await env.DB.prepare("INSERT INTO contenus (compte_id, cle, valeur) VALUES (?,?,?) ON CONFLICT(compte_id, cle) DO UPDATE SET valeur = excluded.valeur, updated_at = datetime('now')").bind(u.id, c.k, v).run();
    await log(env, u.id, null, 'edition_site', c.k);
    return json({ ok: true });
  }
  return json({ ok: false }, 404);
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
        const origin = new URL(req.url).origin;
        for (const c of dest) c.tok = await unsubTok(env, c.id);
        for (let i = 0; i < dest.length; i += 100) {
          const lot = dest.slice(i, i + 100).map((c) => {
            const t = perso(corps, c), lien = origin + '/desinscription?t=' + c.id + '.' + c.tok;
            return { from: env.MAIL_FROM, to: [c.email], subject: perso(sujet, c), headers: { 'List-Unsubscribe': '<' + lien + '>', 'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click' }, text: t + '\n\n—\nPour ne plus recevoir ces messages : ' + lien,
              html: '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.55;color:#111">' + escH(t).replace(/\n/g, '<br>') + '<hr style="border:0;border-top:1px solid #ddd;margin:24px 0"><p style="font-size:12px;color:#666"><a href="' + lien + '">Ne plus recevoir ces messages</a></p></div>' };
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
const STATUTS_DEMANDE = ['nouvelle', 'en_creation', 'apercu', 'en_ligne', 'abandonnee', 'hesite', 'a_rappeler', 'plus_tard', 'refusee', 'sans_reponse', 'trop_cher', 'concurrent'];
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
    await ensureSchema(env);
    if (V2_ADMIN.has(p)) { const x = await adminV2(req, env, url, p, me, one, all); if (x) return x; }
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
        demandes: await all('SELECT compte_id, ref, commerce, COALESCE(metier, activite) AS activite, ville, domaine, mails, tel, formule, statut, suspendu, site_url, utm, message, created_at FROM demandes ORDER BY id DESC LIMIT 3000'),
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
      await appliquerChangements(env);
      const id = parseInt(url.searchParams.get('id'), 10);
      const cpt = await one('SELECT id, nom, email, created_at, derniere_connexion, role FROM comptes WHERE id = ?', id);
      if (!cpt) return json({ ok: false }, 404);
      return json({ ok: true, compte: cpt,
        demandes: await all('SELECT id, ref, created_at, commerce, COALESCE(metier, activite) AS activite, ville, domaine, mails, tel, message, formule, statut, suspendu, site_url FROM demandes WHERE compte_id = ? ORDER BY id DESC', id),
        abonnement: await one('SELECT * FROM abonnements WHERE compte_id = ?', id), changements: await changementsDe(env, id),
        stats_site: await (async () => { const dd = await one('SELECT ref, statut FROM demandes WHERE compte_id = ? ORDER BY id DESC LIMIT 1', id); return dd ? { ref: dd.ref, statut: dd.statut, ...(await statsSite(env, dd.ref)) } : null; })(),
        plaintes: await all('SELECT * FROM plaintes WHERE compte_id = ? ORDER BY id DESC', id),
        journal: await all('SELECT type, detail, created_at, admin_id FROM journal WHERE compte_id = ? ORDER BY id DESC LIMIT 30', id) });
    }
    if (req.method !== 'POST') return json({ ok: false }, 405);
    const { b, err } = await readJson(req, url, 4000); if (err) return err;
    const num = (v) => { const n = parseInt(v, 10); return Number.isFinite(n) ? n : 0; };
    const txt = (v, n) => (typeof v === 'string' ? v.trim().slice(0, n) : '');
    if (p === '/api/admin/demande') {
      if (!STATUTS_DEMANDE.includes(b.statut)) return json({ ok: false }, 422);
      const d = await one('SELECT compte_id, statut FROM demandes WHERE id = ?', num(b.id)); if (!d) return json({ ok: false }, 404);
      await env.DB.prepare('UPDATE demandes SET statut = ? WHERE id = ?').bind(b.statut, num(b.id)).run();
      await log(env, d.compte_id, me.id, 'site_statut', b.statut);
      if (d.statut !== b.statut) {
        const MSG = { en_creation: ['Création en cours', 'Nous avons commencé la création de votre site.'], apercu: ['Votre aperçu est prêt', 'Découvrez votre aperçu dans votre espace, puis validez-le ou demandez des ajustements.'], en_ligne: ['Votre site est en ligne !', 'Félicitations, votre site est en ligne. Votre avis nous aide beaucoup : vous pouvez le donner dans votre espace.'] };
        if (MSG[b.statut]) await notifier(env, d.compte_id, MSG[b.statut][0], MSG[b.statut][1]);
        if (b.statut === 'en_ligne') await env.DB.prepare("UPDATE retours_apercu SET statut = 'traite', traite_at = datetime('now') WHERE compte_id = ? AND statut = 'a_traiter'").bind(d.compte_id).run();
      }
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
        if (b.statut === 'actif') await validerParrainage(env, cid);
      } else {
        const fin = b.statut === 'resilie' ? (ex.fin || new Date().toISOString().slice(0, 10)) : null;
        const debut = ex.statut === 'resilie' && b.statut !== 'resilie' ? new Date().toISOString().slice(0, 10) : ex.debut;
        await env.DB.prepare("UPDATE abonnements SET formule = ?, statut = ?, mails_sup = ?, debut = ?, fin = ?, motif = ?, updated_at = datetime('now') WHERE compte_id = ?").bind(b.formule, b.statut, mails, debut, fin, b.statut === 'resilie' ? motif : '', cid).run();
        if (ex.statut !== b.statut) await log(env, cid, me.id, b.statut === 'resilie' ? 'resiliation' : 'abonnement_statut', b.statut + (motif ? ' : ' + motif : ''));
        if (b.statut === 'actif' && ex.statut !== 'actif') await validerParrainage(env, cid);
        if (b.statut === 'resilie') await env.DB.prepare("UPDATE resiliations SET statut = 'traitee', traite_at = datetime('now') WHERE compte_id = ? AND statut = 'demandee'").bind(cid).run();
        if (ex.formule !== b.formule) await log(env, cid, me.id, 'changement_formule', ex.formule + ' → ' + b.formule);
      }
      if (b.statut === 'impaye') await ouvrirLitige(env, cid, 'impaye', { montant: Math.round((PRIX[b.formule] + PRIX_MAIL * mails) * 1.2 * 100) / 100, periode: parisToday().slice(0, 7), note: 'Abonnement passé en impayé.', source: 'auto' });
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

// ---------- Parcours client, suivi, parrainage, avis, visites ----------
let SCHEMA_OK = false;
async function ensureSchema(env) {
  if (SCHEMA_OK) return;
  const S = [
    "CREATE TABLE IF NOT EXISTS retours_apercu (id INTEGER PRIMARY KEY AUTOINCREMENT, compte_id INTEGER NOT NULL, demande_id INTEGER, type TEXT NOT NULL, message TEXT, statut TEXT NOT NULL DEFAULT 'a_traiter', created_at TEXT NOT NULL DEFAULT (datetime('now')), traite_at TEXT)",
    "CREATE TABLE IF NOT EXISTS dossier (compte_id INTEGER NOT NULL, cle TEXT NOT NULL, valeur TEXT, updated_at TEXT, PRIMARY KEY (compte_id, cle))",
    "CREATE TABLE IF NOT EXISTS dossier_fichiers (id INTEGER PRIMARY KEY AUTOINCREMENT, compte_id INTEGER NOT NULL, categorie TEXT, nom TEXT, mime TEXT, taille INTEGER, data TEXT, created_at TEXT NOT NULL DEFAULT (datetime('now')))",
    "CREATE TABLE IF NOT EXISTS resiliations (id INTEGER PRIMARY KEY AUTOINCREMENT, compte_id INTEGER NOT NULL, motif TEXT, message TEXT, effet TEXT, decale INTEGER NOT NULL DEFAULT 0, statut TEXT NOT NULL DEFAULT 'demandee', created_at TEXT NOT NULL DEFAULT (datetime('now')), traite_at TEXT)",
    "CREATE TABLE IF NOT EXISTS taches (id INTEGER PRIMARY KEY AUTOINCREMENT, compte_id INTEGER, titre TEXT NOT NULL, detail TEXT, echeance TEXT, fait INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL DEFAULT (datetime('now')), fait_at TEXT)",
    "CREATE TABLE IF NOT EXISTS suivi (compte_id INTEGER PRIMARY KEY, rappel_le TEXT, motif TEXT, updated_at TEXT)",
    "CREATE TABLE IF NOT EXISTS parrains (compte_id INTEGER PRIMARY KEY, code TEXT NOT NULL UNIQUE, created_at TEXT NOT NULL DEFAULT (datetime('now')))",
    "CREATE TABLE IF NOT EXISTS parrainages (id INTEGER PRIMARY KEY AUTOINCREMENT, parrain_id INTEGER NOT NULL, filleul_id INTEGER NOT NULL UNIQUE, code TEXT, statut TEXT NOT NULL DEFAULT 'en_attente', created_at TEXT NOT NULL DEFAULT (datetime('now')), valide_at TEXT)",
    "CREATE TABLE IF NOT EXISTS credits (id INTEGER PRIMARY KEY AUTOINCREMENT, compte_id INTEGER NOT NULL, mois INTEGER NOT NULL DEFAULT 1, origine TEXT, parrainage_id INTEGER, utilise_at TEXT, expire_at TEXT, created_at TEXT NOT NULL DEFAULT (datetime('now')), mois_offert TEXT)",
    "CREATE TABLE IF NOT EXISTS avis (id INTEGER PRIMARY KEY AUTOINCREMENT, compte_id INTEGER NOT NULL UNIQUE, demande_id INTEGER, note INTEGER NOT NULL, commentaire TEXT, nom TEXT, commerce TEXT, statut TEXT NOT NULL DEFAULT 'en_attente', created_at TEXT NOT NULL DEFAULT (datetime('now')), publie_at TEXT)",
    "CREATE TABLE IF NOT EXISTS changements_formule (id INTEGER PRIMARY KEY AUTOINCREMENT, compte_id INTEGER NOT NULL, de TEXT NOT NULL, vers TEXT NOT NULL, effet TEXT NOT NULL, statut TEXT NOT NULL DEFAULT 'demande', mails_avant INTEGER, mails_apres INTEGER, created_at TEXT NOT NULL DEFAULT (datetime('now')), applique_at TEXT)",
    "CREATE TABLE IF NOT EXISTS litiges (id INTEGER PRIMARY KEY AUTOINCREMENT, compte_id INTEGER NOT NULL, type TEXT NOT NULL, montant_ttc REAL, periode TEXT, note TEXT, source TEXT NOT NULL DEFAULT 'manuel', statut TEXT NOT NULL DEFAULT 'ouvert', created_at TEXT NOT NULL DEFAULT (datetime('now')), clos_at TEXT)",
    "CREATE TABLE IF NOT EXISTS vues_site (site TEXT NOT NULL, jour TEXT NOT NULL, n INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (site, jour))",
    "CREATE TABLE IF NOT EXISTS vues_site_uniq (site TEXT NOT NULL, jour TEXT NOT NULL, h TEXT NOT NULL, n INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (site, jour, h))",
    "CREATE TABLE IF NOT EXISTS vues (jour TEXT NOT NULL, page TEXT NOT NULL, n INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (jour, page))",
  ];
  await env.DB.batch(S.map((q) => env.DB.prepare(q)));
  try { await env.DB.prepare('ALTER TABLE credits ADD COLUMN mois_offert TEXT').run(); } catch (_) { /* colonne déjà présente */ }
  try { await env.DB.prepare('ALTER TABLE demandes ADD COLUMN metier TEXT').run(); } catch (_) { /* colonne déjà présente */ }
  SCHEMA_OK = true;
}

const DOSSIER_CLES = { description: 700, horaires: 500, adresse_pub: 200, tel_pub: 30, email_pub: 120, services: 900, reseaux: 300, couleurs: 120, slogan: 120, domaine_choisi: 70, remarques: 900 };
const DOSSIER_REQUIS = ['description', 'horaires', 'adresse_pub', 'tel_pub', 'services'];
const DOSSIER_LIBELLES = { description: 'La présentation de votre commerce', horaires: 'Les horaires', adresse_pub: 'L’adresse', tel_pub: 'Le téléphone', services: 'Les prestations ou la carte avec les tarifs' };
const FICHIER_MAX = 1200000; // octets : une ligne D1 est limitée à environ 2 Mo une fois en base64
const FICHIERS_MAX = 15;
const CAT_FICHIER = ['logo', 'photo', 'document', 'autre'];
const MOTIFS_RESIL = ['prix', 'plus_besoin', 'insatisfait', 'fermeture', 'autre'];
const DELAI_JOURS_OUVRES = 5; // CGV article 6 : 5 jours ouvrés après un dossier complet
const PARRAIN_VALIDITE_JOURS = 90; // un parrainage non transformé en abonnement actif expire au bout de 90 jours
const CREDIT_VALIDITE_MOIS = 12;
const STATUTS_PAUSE = ['hesite', 'a_rappeler', 'plus_tard', 'refusee', 'sans_reponse', 'trop_cher', 'concurrent', 'abandonnee'];

const MOIS_FR = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
function moisFr(ym) { return MOIS_FR[+ym.slice(5, 7) - 1] + ' ' + ym.slice(0, 4); }
function plusMois(iso, n) {
  const d = new Date(iso.slice(0, 10) + 'T12:00:00Z'), j = d.getUTCDate();
  d.setUTCDate(1); d.setUTCMonth(d.getUTCMonth() + n);
  const dim = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, 0)).getUTCDate();
  d.setUTCDate(Math.min(j, dim));
  return d.toISOString().slice(0, 10);
}
function joursOuvres(iso, n) {
  const d = new Date(iso.slice(0, 10) + 'T12:00:00Z'); let k = 0;
  while (k < n) { d.setUTCDate(d.getUTCDate() + 1); const w = d.getUTCDay(); if (w !== 0 && w !== 6) k++; }
  return d.toISOString().slice(0, 10);
}
function ecartJours(a, b) { return Math.round((new Date(b.slice(0, 10) + 'T12:00:00Z') - new Date(a.slice(0, 10) + 'T12:00:00Z')) / 86400000); }
// CGV art. 17 : résiliation à l'échéance de la période de 12 mois, avec 30 jours de préavis
function effetResiliation(debut, today) {
  if (!debut) return { effet: today, decale: false, echeance: null };
  let e = plusMois(debut, 12); while (e <= today) e = plusMois(e, 12);
  const echeance = e; let decale = false;
  if (ecartJours(today, e) < 30) { e = plusMois(e, 12); decale = true; }
  return { effet: e, decale, echeance };
}
function prenomDe(nom) { return ((nom || '').trim().split(/\s+/)[0]) || ''; }
function nomAvis(nom) { const p = (nom || '').trim().split(/\s+/); return p.length > 1 ? p[0] + ' ' + p[p.length - 1][0].toUpperCase() + '.' : (p[0] || 'Client'); }
const CODE_AL = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
async function codeDe(env, compteId) {
  let r = await env.DB.prepare('SELECT code FROM parrains WHERE compte_id = ?').bind(compteId).first();
  if (r) return r.code;
  for (let i = 0; i < 8; i++) {
    const code = 'DW-' + Array.from(crypto.getRandomValues(new Uint8Array(5)), (x) => CODE_AL[x % CODE_AL.length]).join('');
    try { await env.DB.prepare('INSERT INTO parrains (compte_id, code) VALUES (?,?)').bind(compteId, code).run(); return code; }
    catch (_) { r = await env.DB.prepare('SELECT code FROM parrains WHERE compte_id = ?').bind(compteId).first(); if (r) return r.code; }
  }
  return null;
}
async function notifier(env, compteId, titre, message) {
  try { await env.DB.prepare('INSERT INTO notifications (compte_id, titre, message) VALUES (?,?,?)').bind(compteId, titre.slice(0, 120), message.slice(0, 1000)).run(); } catch (_) {}
}
// Mois offert : le mois en cours reste facturé, le premier mois libre suivant est offert.
async function moisLibres(env, compteId, n) {
  const today = parisToday();
  const pris = new Set(((await env.DB.prepare('SELECT mois_offert FROM credits WHERE compte_id = ? AND mois_offert IS NOT NULL').bind(compteId).all()).results || []).map((r) => r.mois_offert));
  const out = []; let k = 1;
  while (out.length < n && k < 400) { const m = plusMois(today.slice(0, 8) + '01', k).slice(0, 7); if (!pris.has(m)) out.push(m); k++; }
  return out;
}
function etatCredit(c, today) {
  if (c.utilise_at) return 'utilise';
  if (c.mois_offert) return c.mois_offert < today.slice(0, 7) ? 'utilise' : (c.mois_offert === today.slice(0, 7) ? 'en_cours' : 'planifie');
  return c.expire_at && c.expire_at < today + ' 23:59:59' ? 'expire' : 'disponible';
}
async function expirerParrainages(env) {
  await env.DB.prepare("UPDATE parrainages SET statut = 'expire' WHERE statut = 'en_attente' AND created_at < datetime('now', ?)").bind('-' + PARRAIN_VALIDITE_JOURS + ' days').run();
}
// Applique un code de parrainage à un nouveau client. Renvoie { ok:true } ou { ok:false, error }.
async function appliquerParrain(env, filleulId, brut) {
  const code = typeof brut === 'string' ? brut.trim().toUpperCase() : '';
  if (!/^DW-[A-Z0-9]{5}$/.test(code)) return { ok: false, error: 'inconnu' };
  const one = (sql, ...a) => env.DB.prepare(sql).bind(...a).first();
  const par = await one('SELECT compte_id FROM parrains WHERE code = ?', code);
  if (!par) return { ok: false, error: 'inconnu' };
  if (par.compte_id === filleulId) return { ok: false, error: 'soi' };
  if (await one('SELECT id FROM parrainages WHERE filleul_id = ?', filleulId)) return { ok: false, error: 'deja' };
  if (await one('SELECT compte_id FROM abonnements WHERE compte_id = ?', filleulId)) return { ok: false, error: 'client' };
  const a = await one('SELECT statut FROM abonnements WHERE compte_id = ?', par.compte_id);
  if (!a || a.statut !== 'actif') return { ok: false, error: 'inactif' };
  try { await env.DB.prepare('INSERT INTO parrainages (parrain_id, filleul_id, code) VALUES (?,?,?)').bind(par.compte_id, filleulId, code).run(); }
  catch (_) { return { ok: false, error: 'deja' }; }
  await log(env, filleulId, null, 'parrainage', 'code ' + code);
  return { ok: true };
}
// Appelée quand l'abonnement d'un filleul devient actif : un mois offert pour les deux.
async function validerParrainage(env, filleulId) {
  await expirerParrainages(env);
  const pa = await env.DB.prepare("SELECT id, parrain_id FROM parrainages WHERE filleul_id = ? AND statut = 'en_attente'").bind(filleulId).first();
  if (!pa) return false;
  const exp = "datetime('now','+" + CREDIT_VALIDITE_MOIS + " months')";
  const mP = (await moisLibres(env, pa.parrain_id, 1))[0], mF = (await moisLibres(env, filleulId, 1))[0];
  await env.DB.batch([
    env.DB.prepare("UPDATE parrainages SET statut = 'valide', valide_at = datetime('now') WHERE id = ?").bind(pa.id),
    env.DB.prepare('INSERT INTO credits (compte_id, mois, origine, parrainage_id, expire_at, mois_offert) VALUES (?,1,?,?,' + exp + ',?)').bind(pa.parrain_id, 'parrain', pa.id, mP),
    env.DB.prepare('INSERT INTO credits (compte_id, mois, origine, parrainage_id, expire_at, mois_offert) VALUES (?,1,?,?,' + exp + ',?)').bind(filleulId, 'filleul', pa.id, mF),
  ]);
  await notifier(env, pa.parrain_id, 'Parrainage validé : un mois offert', 'Merci ! Votre filleul est devenu client. Un mois offert est ajouté à votre compte, le mois de ' + moisFr(mP) + ' ne vous sera pas facturé.');
  await notifier(env, filleulId, 'Bienvenue : un mois offert', 'Grâce à votre parrain, un mois offert est ajouté à votre compte : le mois de ' + moisFr(mF) + ' ne vous sera pas facturé.');
  await log(env, filleulId, null, 'parrainage_valide', 'filleul');
  await log(env, pa.parrain_id, null, 'parrainage_valide', 'parrain');
  return true;
}

async function dossierDe(env, compteId) {
  const rows = (await env.DB.prepare('SELECT cle, valeur FROM dossier WHERE compte_id = ?').bind(compteId).all()).results || [];
  const o = {}; for (const r of rows) o[r.cle] = r.valeur; return o;
}
function manquants(dos) { return DOSSIER_REQUIS.filter((k) => !(dos[k] || '').trim()); }

function octetsOk(b64, mime) {
  let h; try { h = atob(b64.slice(0, 16)); } catch (_) { return false; }
  const s = (i, n) => h.slice(i, i + n);
  if (mime === 'image/png') return s(0, 4) === '\x89PNG';
  if (mime === 'image/jpeg') return s(0, 3) === '\xFF\xD8\xFF';
  if (mime === 'image/webp') return s(0, 4) === 'RIFF' && s(8, 4) === 'WEBP';
  if (mime === 'application/pdf') return s(0, 4) === '%PDF';
  return false;
}
async function envoiFichier(env, id, compteId) {
  const f = compteId == null
    ? await env.DB.prepare('SELECT nom, mime, data FROM dossier_fichiers WHERE id = ?').bind(id).first()
    : await env.DB.prepare('SELECT nom, mime, data FROM dossier_fichiers WHERE id = ? AND compte_id = ?').bind(id, compteId).first();
  if (!f) return json({ ok: false }, 404);
  const bin = atob(f.data), a = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) a[i] = bin.charCodeAt(i);
  const nom = (f.nom || 'fichier').replace(/[^\w.\- ]/g, '_').slice(0, 80);
  return new Response(a, { headers: { 'content-type': f.mime, 'content-disposition': (f.mime === 'application/pdf' ? 'attachment' : 'inline') + '; filename="' + nom + '"', 'x-content-type-options': 'nosniff', 'cache-control': 'private, no-store', 'content-security-policy': "default-src 'none'; sandbox" } });
}

function frise(d, dos, journal, retours) {
  const date = (st) => { const e = journal.filter((j) => j.detail === st).pop(); return e ? e.created_at.slice(0, 10) : null; };
  const ordre = { nouvelle: 0, en_creation: 1, apercu: 2, en_ligne: 3 };
  const idx = ordre[d.statut] == null ? 0 : ordre[d.statut];
  const termine = (dos._termine || '').slice(0, 10) || null;
  const valide = retours.find((r) => r.type === 'valide');
  const prevue = termine ? joursOuvres(termine, DELAI_JOURS_OUVRES) : null;
  const pause = STATUTS_PAUSE.includes(d.statut);
  const etapes = [
    { cle: 'recue', titre: 'Demande reçue', detail: 'Nous avons bien reçu votre demande.', etat: 'fait', date: d.created_at.slice(0, 10) },
    { cle: 'dossier', titre: 'Votre dossier', detail: termine ? 'Votre dossier est complet.' : 'À compléter : présentation, horaires, adresse, téléphone, prestations, logo et photos.', etat: termine || idx >= 1 ? 'fait' : 'cours', date: termine },
    { cle: 'creation', titre: 'Création de votre site', detail: 'Nous créons votre site à partir de votre dossier.', etat: idx >= 2 ? 'fait' : (idx === 1 || (termine && idx === 0) ? 'cours' : 'avenir'), date: date('en_creation'), prevue: idx < 2 ? prevue : null },
    { cle: 'apercu', titre: 'Votre validation', detail: valide ? 'Vous avez validé l’aperçu.' : 'Vous découvrez l’aperçu, puis vous le validez ou demandez des ajustements.', etat: valide || idx >= 3 ? 'fait' : (idx === 2 ? 'cours' : 'avenir'), date: valide ? valide.created_at.slice(0, 10) : date('apercu') },
    { cle: 'en_ligne', titre: 'Mise en ligne', detail: idx >= 3 ? 'Votre site est en ligne.' : 'Nous mettons votre site en ligne après votre validation.', etat: idx >= 3 ? 'fait' : 'avenir', date: date('en_ligne') },
  ];
  return { etapes, pause, prevue };
}


// ---- changement de formule : effet au 1er du mois suivant ----
function premierMoisSuivant(iso) { return plusMois(iso.slice(0, 7) + '-01', 1); }
// Pro -> Essentiel : l'adresse mail incluse devient payante (4 € HT) ; Essentiel -> Pro : une adresse payante devient incluse
function mailsApresChangement(de, vers, avant) { return de === 'pro' && vers === 'essentiel' ? avant + 1 : de === 'essentiel' && vers === 'pro' ? Math.max(0, avant - 1) : avant; }
async function appliquerChangements(env) {
  await ensureSchema(env);
  const today = parisToday();
  const dus = (await env.DB.prepare("SELECT id, compte_id, de, vers, effet FROM changements_formule WHERE statut = 'demande' AND effet <= ? ORDER BY effet, id").bind(today).all()).results || [];
  for (const c of dus) {
    const abo = await env.DB.prepare('SELECT formule, statut, mails_sup FROM abonnements WHERE compte_id = ?').bind(c.compte_id).first();
    if (!abo || abo.statut === 'resilie' || abo.formule === c.vers) { await env.DB.prepare("UPDATE changements_formule SET statut = 'annule', applique_at = datetime('now') WHERE id = ?").bind(c.id).run(); continue; }
    const avant = abo.mails_sup || 0, apres = mailsApresChangement(abo.formule, c.vers, avant);
    const r = await env.DB.prepare("UPDATE changements_formule SET statut = 'applique', de = ?, mails_avant = ?, mails_apres = ?, applique_at = datetime('now') WHERE id = ? AND statut = 'demande'").bind(abo.formule, avant, apres, c.id).run();
    if (!(r.meta && r.meta.changes)) continue;
    await env.DB.prepare("UPDATE abonnements SET formule = ?, mails_sup = ?, updated_at = datetime('now') WHERE compte_id = ?").bind(c.vers, apres, c.compte_id).run();
    await log(env, c.compte_id, null, 'changement_formule', abo.formule + ' → ' + c.vers + ' (effet ' + c.effet + ')');
    const txtMail = abo.formule === 'pro' && c.vers === 'essentiel' ? ' Votre adresse mail pro, auparavant incluse, est désormais facturée 4 € HT (4,80 € TTC) par mois.' : '';
    await notifier(env, c.compte_id, 'Votre formule a changé', 'Votre abonnement est passé à la formule ' + (c.vers === 'pro' ? 'Pro' : 'Essentiel') + ' à compter du ' + c.effet.split('-').reverse().join('/') + '.' + txtMail);
  }
}
async function changementsDe(env, cid) {
  return (await env.DB.prepare("SELECT id, de, vers, effet, statut, mails_avant, mails_apres, created_at FROM changements_formule WHERE compte_id = ? AND statut IN ('demande','applique') ORDER BY effet, id").bind(cid).all()).results || [];
}
// ---- litiges (impayés, prélèvements rejetés, contestations) ----
const TYPES_LITIGE = ['impaye', 'prelevement_rejete', 'contestation', 'autre'];
async function ouvrirLitige(env, cid, type, o) {
  o = o || {};
  const ex = o.source === 'auto' && o.periode
    ? await env.DB.prepare("SELECT id FROM litiges WHERE compte_id = ? AND type = ? AND source = 'auto' AND (statut = 'ouvert' OR periode = ?)").bind(cid, type, o.periode).first()
    : await env.DB.prepare("SELECT id FROM litiges WHERE compte_id = ? AND type = ? AND statut = 'ouvert'").bind(cid, type).first();
  if (ex) return ex.id;
  const r = await env.DB.prepare('INSERT INTO litiges (compte_id, type, montant_ttc, periode, note, source) VALUES (?,?,?,?,?,?)').bind(cid, type, o.montant == null ? null : o.montant, o.periode || '', o.note || '', o.source || 'auto').run();
  return r.meta.last_row_id;
}
async function synchroLitigesImpayes(env) {
  await ensureSchema(env);
  const imp = (await env.DB.prepare("SELECT compte_id, formule, mails_sup FROM abonnements WHERE statut = 'impaye'").all()).results || [];
  for (const a of imp) await ouvrirLitige(env, a.compte_id, 'impaye', { montant: Math.round((PRIX[a.formule] + PRIX_MAIL * (a.mails_sup || 0)) * 1.2 * 100) / 100, periode: parisToday().slice(0, 7), note: 'Abonnement en statut impayé.', source: 'auto' });
  await env.DB.prepare("UPDATE litiges SET statut = 'regle', clos_at = datetime('now') WHERE statut = 'ouvert' AND type = 'impaye' AND source = 'auto' AND compte_id NOT IN (SELECT compte_id FROM abonnements WHERE statut = 'impaye')").run();
}

const V2_ESPACE = new Set(['/api/espace/parcours', '/api/espace/apercu', '/api/espace/dossier', '/api/espace/dossier-termine', '/api/espace/fichier', '/api/espace/fichier-suppr', '/api/espace/resiliation', '/api/espace/resiliation-annuler', '/api/espace/avis', '/api/espace/parrain-appliquer', '/api/espace/formule-changer', '/api/espace/formule-annuler', '/api/espace/stats']);
async function espaceV2(req, env, url, p, u, lecture) {
  await ensureSchema(env);
  const one = (sql, ...a) => env.DB.prepare(sql).bind(...a).first();
  const all = async (sql, ...a) => (await env.DB.prepare(sql).bind(...a).all()).results || [];
  const txt = (v, n) => (typeof v === 'string' ? v.trim().slice(0, n) : '');
  const dem = () => one('SELECT id, ref, created_at, statut, suspendu, site_url, formule, commerce, domaine FROM demandes WHERE compte_id = ? ORDER BY id DESC LIMIT 1', u.id);
  const today = parisToday();
  if (p === '/api/espace/parcours' && req.method === 'GET') {
    await expirerParrainages(env); await appliquerChangements(env);
    const d = await dem();
    const abo = await one('SELECT formule, statut, mails_sup, debut, fin FROM abonnements WHERE compte_id = ?', u.id);
    const dos = await dossierDe(env, u.id);
    const retours = await all('SELECT id, type, message, statut, created_at FROM retours_apercu WHERE compte_id = ? ORDER BY id DESC LIMIT 10', u.id);
    const journal = await all("SELECT detail, created_at FROM journal WHERE compte_id = ? AND type = 'site_statut' ORDER BY id", u.id);
    const fr = d ? frise(d, dos, journal, retours) : null;
    const resil = await one("SELECT id, motif, message, effet, decale, created_at FROM resiliations WHERE compte_id = ? AND statut = 'demandee' ORDER BY id DESC LIMIT 1", u.id);
    const code = await codeDe(env, u.id);
    const filleuls = await all('SELECT p.statut, p.created_at, c.nom FROM parrainages p JOIN comptes c ON c.id = p.filleul_id WHERE p.parrain_id = ? ORDER BY p.id DESC LIMIT 50', u.id);
    const credits = await all('SELECT id, mois, origine, utilise_at, expire_at, created_at, mois_offert FROM credits WHERE compte_id = ? ORDER BY id DESC', u.id);
    const moi = await one('SELECT p.code, p.statut, p.created_at FROM parrainages p WHERE p.filleul_id = ?', u.id);
    const avis = await one('SELECT note, commentaire, statut FROM avis WHERE compte_id = ?', u.id);
    return json({ ok: true, lecture, aujourdhui: today, demande: d, abonnement: abo, dossier: dos, requis: DOSSIER_REQUIS.map((k) => ({ cle: k, libelle: DOSSIER_LIBELLES[k], ok: !!(dos[k] || '').trim() })),
      fichiers: await all('SELECT id, categorie, nom, mime, taille, created_at FROM dossier_fichiers WHERE compte_id = ? ORDER BY id', u.id), fichiers_max: FICHIERS_MAX, fichier_max: FICHIER_MAX,
      retours, frise: fr, delai: DELAI_JOURS_OUVRES, resiliation: resil, changements: await changementsDe(env, u.id), effet: effetResiliation(abo && abo.debut, today),
      parrainage: { code, lien: url.origin + '/inscription?parrain=' + code, filleuls: filleuls.map((f) => ({ prenom: prenomDe(f.nom), statut: f.statut, date: f.created_at.slice(0, 10) })), credits: credits.map((c) => ({ id: c.id, mois: c.mois, origine: c.origine, mois_offert: c.mois_offert || null, etat: etatCredit(c, today), expire_at: c.expire_at ? c.expire_at.slice(0, 10) : null, utilise_le: c.utilise_at ? String(c.utilise_at).slice(0, 10) : null })), moi: moi ? { code: moi.code, statut: moi.statut } : null, validite: PARRAIN_VALIDITE_JOURS },
      avis: avis || null, avis_invite: !!(d && d.statut === 'en_ligne' && !avis) });
  }
  if (p === '/api/espace/stats' && req.method === 'GET') {
    const d = await dem();
    if (!d) return json({ ok: true, actif: false, raison: 'aucun-site' });
    if (d.statut !== 'en_ligne') return json({ ok: true, actif: false, raison: 'pas-en-ligne' });
    return json({ ok: true, actif: true, ...(await statsSite(env, d.ref)) });
  }
  if (p === '/api/espace/fichier' && req.method === 'GET') {
    const id = parseInt(url.searchParams.get('id'), 10);
    return Number.isFinite(id) ? envoiFichier(env, id, u.id) : json({ ok: false }, 400);
  }
  if (req.method !== 'POST') return json({ ok: false }, 405);
  if (lecture) return json({ ok: false, error: 'lecture-seule' }, 403);
  const gros = p === '/api/espace/fichier';
  const { b, err } = await readJson(req, url, gros ? 1700000 : 4000); if (err) return err;
  const d = await dem();
  if (p === '/api/espace/apercu') {
    if (!d) return json({ ok: false, error: 'aucune-demande' }, 404);
    if (d.suspendu) return json({ ok: false, error: 'suspendu' }, 403);
    if (d.statut !== 'apercu') return json({ ok: false, error: 'pas-apercu' }, 409);
    if (await one("SELECT id FROM retours_apercu WHERE demande_id = ? AND type = 'valide'", d.id)) return json({ ok: false, error: 'deja' }, 409);
    if (b.action === 'valide') {
      await env.DB.prepare("INSERT INTO retours_apercu (compte_id, demande_id, type) VALUES (?,?, 'valide')").bind(u.id, d.id).run();
      await env.DB.prepare("UPDATE retours_apercu SET statut = 'traite', traite_at = datetime('now') WHERE demande_id = ? AND type = 'changements' AND statut = 'a_traiter'").bind(d.id).run();
      await log(env, u.id, null, 'apercu_valide', d.ref);
      await notifier(env, u.id, 'Aperçu validé', 'Merci ! Vous avez validé l’aperçu. Nous préparons la mise en ligne de votre site.');
      return json({ ok: true });
    }
    if (b.action === 'changements') {
      const m = txt(b.message, 1500);
      if (m.length < 10) return json({ ok: false, error: 'vide' }, 422);
      if (await one("SELECT id FROM retours_apercu WHERE demande_id = ? AND type = 'changements' AND statut = 'a_traiter'", d.id)) return json({ ok: false, error: 'en-cours' }, 409);
      await env.DB.prepare("INSERT INTO retours_apercu (compte_id, demande_id, type, message) VALUES (?,?, 'changements', ?)").bind(u.id, d.id, m).run();
      await log(env, u.id, null, 'apercu_changements', d.ref);
      return json({ ok: true });
    }
    return json({ ok: false }, 422);
  }
  if (p === '/api/espace/dossier') {
    if (!d) return json({ ok: false, error: 'aucune-demande' }, 404);
    const ch = b.champs && typeof b.champs === 'object' ? b.champs : {};
    const ops = [];
    for (const k of Object.keys(DOSSIER_CLES)) if (typeof ch[k] === 'string') ops.push(env.DB.prepare("INSERT INTO dossier (compte_id, cle, valeur, updated_at) VALUES (?,?,?,datetime('now')) ON CONFLICT(compte_id, cle) DO UPDATE SET valeur = excluded.valeur, updated_at = excluded.updated_at").bind(u.id, k, txt(ch[k], DOSSIER_CLES[k])));
    if (!ops.length) return json({ ok: false, error: 'vide' }, 422);
    await env.DB.batch(ops);
    return json({ ok: true });
  }
  if (p === '/api/espace/dossier-termine') {
    if (!d) return json({ ok: false, error: 'aucune-demande' }, 404);
    const dos = await dossierDe(env, u.id), m = manquants(dos);
    if (m.length) return json({ ok: false, error: 'incomplet', manquants: m.map((k) => DOSSIER_LIBELLES[k]) }, 422);
    if (dos._termine) return json({ ok: true, deja: true });
    await env.DB.prepare("INSERT INTO dossier (compte_id, cle, valeur, updated_at) VALUES (?, '_termine', ?, datetime('now'))").bind(u.id, today).run();
    await log(env, u.id, null, 'dossier_complet', d.ref);
    await notifier(env, u.id, 'Dossier reçu', 'Votre dossier est complet. Votre aperçu est prévu au plus tard le ' + joursOuvres(today, DELAI_JOURS_OUVRES).split('-').reverse().join('/') + '.');
    return json({ ok: true, prevue: joursOuvres(today, DELAI_JOURS_OUVRES) });
  }
  if (p === '/api/espace/fichier') {
    if (!d) return json({ ok: false, error: 'aucune-demande' }, 404);
    const mime = typeof b.mime === 'string' ? b.mime : '', data = typeof b.data === 'string' ? b.data : '';
    const cat = CAT_FICHIER.includes(b.categorie) ? b.categorie : 'autre';
    if (!/^[A-Za-z0-9+/]+={0,2}$/.test(data) || data.length < 8) return json({ ok: false, error: 'fichier' }, 422);
    if (!['image/png', 'image/jpeg', 'image/webp', 'application/pdf'].includes(mime)) return json({ ok: false, error: 'type' }, 415);
    if (Math.floor(data.length * 3 / 4) > FICHIER_MAX) return json({ ok: false, error: 'taille' }, 413);
    if (!octetsOk(data, mime)) return json({ ok: false, error: 'type' }, 415);
    const n = await one('SELECT COUNT(*) n FROM dossier_fichiers WHERE compte_id = ?', u.id);
    if (n.n >= FICHIERS_MAX) return json({ ok: false, error: 'trop' }, 409);
    const r = await env.DB.prepare('INSERT INTO dossier_fichiers (compte_id, categorie, nom, mime, taille, data) VALUES (?,?,?,?,?,?)').bind(u.id, cat, txt(b.nom, 80) || 'fichier', mime, Math.floor(data.length * 3 / 4), data).run();
    await log(env, u.id, null, 'fichier', cat);
    return json({ ok: true, id: r.meta.last_row_id });
  }
  if (p === '/api/espace/fichier-suppr') {
    await env.DB.prepare('DELETE FROM dossier_fichiers WHERE id = ? AND compte_id = ?').bind(parseInt(b.id, 10) || 0, u.id).run();
    return json({ ok: true });
  }
  if (p === '/api/espace/formule-changer') {
    const abo = await one('SELECT formule, statut, mails_sup FROM abonnements WHERE compte_id = ?', u.id);
    if (!abo || abo.statut !== 'actif') return json({ ok: false, error: 'pas-actif' }, 409);
    if (!FORMULES.includes(b.vers) || b.vers === abo.formule) return json({ ok: false, error: 'formule' }, 422);
    if (b.confirme !== true) return json({ ok: false, error: 'confirmation' }, 422);
    if (await one("SELECT id FROM resiliations WHERE compte_id = ? AND statut = 'demandee'", u.id)) return json({ ok: false, error: 'resiliation' }, 409);
    if (await one("SELECT id FROM changements_formule WHERE compte_id = ? AND statut = 'demande'", u.id)) return json({ ok: false, error: 'deja' }, 409);
    const effet = premierMoisSuivant(today);
    await env.DB.prepare('INSERT INTO changements_formule (compte_id, de, vers, effet) VALUES (?,?,?,?)').bind(u.id, abo.formule, b.vers, effet).run();
    await log(env, u.id, null, 'changement_formule_demande', abo.formule + ' → ' + b.vers + ' / effet ' + effet);
    await notifier(env, u.id, 'Changement de formule enregistré', 'Votre passage à la formule ' + (b.vers === 'pro' ? 'Pro' : 'Essentiel') + ' prendra effet le ' + effet.split('-').reverse().join('/') + '. Le mois en cours reste facturé à la formule actuelle. Vous pouvez annuler jusqu’à cette date.');
    return json({ ok: true, effet, mails_apres: mailsApresChangement(abo.formule, b.vers, abo.mails_sup || 0) });
  }
  if (p === '/api/espace/formule-annuler') {
    const r = await env.DB.prepare("UPDATE changements_formule SET statut = 'annule', applique_at = datetime('now') WHERE compte_id = ? AND statut = 'demande'").bind(u.id).run();
    if (!(r.meta && r.meta.changes)) return json({ ok: false, error: 'aucun' }, 404);
    await log(env, u.id, null, 'changement_formule_annule', '');
    return json({ ok: true });
  }
  if (p === '/api/espace/resiliation') {
    if (!d) return json({ ok: false, error: 'aucune-demande' }, 404);
    if (b.confirme !== true) return json({ ok: false, error: 'confirmation' }, 422);
    if (await one("SELECT id FROM resiliations WHERE compte_id = ? AND statut = 'demandee'", u.id)) return json({ ok: false, error: 'deja' }, 409);
    const abo = await one('SELECT statut, debut FROM abonnements WHERE compte_id = ?', u.id);
    if (abo && abo.statut === 'resilie') return json({ ok: false, error: 'resilie' }, 409);
    const motif = MOTIFS_RESIL.includes(b.motif) ? b.motif : 'autre', eff = effetResiliation(abo && abo.debut, today);
    await env.DB.prepare('INSERT INTO resiliations (compte_id, motif, message, effet, decale) VALUES (?,?,?,?,?)').bind(u.id, motif, txt(b.message, 800), eff.effet, eff.decale ? 1 : 0).run();
    await log(env, u.id, null, 'resiliation_demandee', motif + ' / effet ' + eff.effet);
    await notifier(env, u.id, 'Demande de résiliation reçue', 'Nous avons bien reçu votre demande. Elle prendra effet le ' + eff.effet.split('-').reverse().join('/') + '. Vous pouvez l’annuler tant qu’elle n’est pas traitée.');
    return json({ ok: true, effet: eff.effet, decale: eff.decale });
  }
  if (p === '/api/espace/resiliation-annuler') {
    const r = await env.DB.prepare("UPDATE resiliations SET statut = 'annulee', traite_at = datetime('now') WHERE compte_id = ? AND statut = 'demandee'").bind(u.id).run();
    if (!(r.meta && r.meta.changes)) return json({ ok: false, error: 'aucune' }, 404);
    await log(env, u.id, null, 'resiliation_annulee', '');
    return json({ ok: true });
  }
  if (p === '/api/espace/avis') {
    if (!d || d.statut !== 'en_ligne') return json({ ok: false, error: 'pas-en-ligne' }, 409);
    const note = parseInt(b.note, 10), com = txt(b.commentaire, 600);
    if (!(note >= 1 && note <= 5)) return json({ ok: false, error: 'note' }, 422);
    if (b.publication !== true) return json({ ok: false, error: 'consentement' }, 422);
    const ex = await one('SELECT statut FROM avis WHERE compte_id = ?', u.id);
    if (ex && ex.statut === 'publie') return json({ ok: false, error: 'publie' }, 409);
    const c = await one('SELECT nom FROM comptes WHERE id = ?', u.id);
    await env.DB.prepare("INSERT INTO avis (compte_id, demande_id, note, commentaire, nom, commerce) VALUES (?,?,?,?,?,?) ON CONFLICT(compte_id) DO UPDATE SET note = excluded.note, commentaire = excluded.commentaire, statut = 'en_attente'").bind(u.id, d.id, note, com, nomAvis(c && c.nom), (d.commerce || '').slice(0, 80)).run();
    await log(env, u.id, null, 'avis', note + '/5');
    return json({ ok: true });
  }
  if (p === '/api/espace/parrain-appliquer') {
    const r = await appliquerParrain(env, u.id, b.code);
    return json(r, r.ok ? 200 : 422);
  }
  return json({ ok: false }, 404);
}

// ---------- Public : avis publiés et mesure de visites sans cookie ----------
async function avisPublics(req, env) {
  await ensureSchema(env);
  const rows = (await env.DB.prepare("SELECT note, commentaire, nom, commerce, publie_at FROM avis WHERE statut = 'publie' ORDER BY publie_at DESC, id DESC LIMIT 12").all()).results || [];
  const s = await env.DB.prepare("SELECT COUNT(*) n, AVG(note) m FROM avis WHERE statut = 'publie'").first();
  const res = json({ ok: true, nb: s.n || 0, moyenne: s.n ? Math.round(s.m * 10) / 10 : null, avis: rows.map((r) => ({ note: r.note, commentaire: r.commentaire, nom: r.nom, commerce: r.commerce, date: (r.publie_at || '').slice(0, 10) })) });
  res.headers.set('cache-control', 'public, max-age=300');
  return res;
}
const VUE_OK = /^\/(?:[a-z0-9-]+(?:\/[a-z0-9-]+)?)?$/;
const VUE_EXCLUES = new Set(['/admin', '/espace', '/connexion', '/inscription', '/reinitialiser', '/mot-de-passe-oublie', '/desinscription']);
async function vue(req, env, url) {
  if (req.method !== 'POST') return json({ ok: false }, 405);
  if (req.headers.get('dnt') === '1' || req.headers.get('sec-gpc') === '1') return json({ ok: true, ignore: true });
  if (/bot|crawl|spider|headless|preview|monitor/i.test(req.headers.get('user-agent') || '')) return json({ ok: true, ignore: true });
  const { b, err } = await readJson(req, url, 300); if (err) return err;
  const page = typeof b.p === 'string' ? b.p.split('?')[0].replace(/\/+$/, '') || '/' : '';
  if (!VUE_OK.test(page) || VUE_EXCLUES.has(page)) return json({ ok: true, ignore: true });
  try {
    await ensureSchema(env);
    await env.DB.prepare('INSERT INTO vues (jour, page, n) VALUES (?,?,1) ON CONFLICT(jour, page) DO UPDATE SET n = n + 1').bind(parisToday(), page).run();
  } catch (_) { return json({ ok: false }, 500); }
  return json({ ok: true });
}


// ---------- Statistiques de fréquentation des sites clients (sans cookie, sans IP conservée) ----------
const CORS_VUE = { 'access-control-allow-origin': '*', 'access-control-allow-methods': 'POST, OPTIONS', 'access-control-allow-headers': 'content-type', 'access-control-max-age': '86400' };
async function vueSite(req, env, url) {
  const rep = (o, st = 200) => { const r = json(o, st); for (const k in CORS_VUE) r.headers.set(k, CORS_VUE[k]); return r; };
  if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS_VUE });
  if (req.method !== 'POST') return rep({ ok: false }, 405);
  if (req.headers.get('dnt') === '1' || req.headers.get('sec-gpc') === '1') return rep({ ok: true, ignore: true });
  if (/bot|crawl|spider|headless|preview|monitor|curl|wget/i.test(req.headers.get('user-agent') || '')) return rep({ ok: true, ignore: true });
  let b = null; try { const raw = await req.text(); if (raw.length <= 300) b = JSON.parse(raw); } catch (_) {}
  if (!b || typeof b !== 'object' || typeof b.s !== 'string' || !/^[A-Za-z0-9-]{4,30}$/.test(b.s)) return rep({ ok: false }, 400);
  try {
    await ensureSchema(env);
    const d = await env.DB.prepare("SELECT d.ref FROM demandes d WHERE d.ref = ? AND d.statut = 'en_ligne' AND d.suspendu = 0").bind(b.s).first();
    if (!d) return rep({ ok: true, ignore: true });
    const jour = parisToday(), h = await ipHash(req, b.s + '|' + jour + '|' + (req.headers.get('user-agent') || ''));
    const r = await env.DB.prepare('INSERT INTO vues_site_uniq (site, jour, h, n) VALUES (?,?,?,1) ON CONFLICT(site, jour, h) DO UPDATE SET n = n + 1 WHERE n < 300').bind(b.s, jour, h).run();
    if (r.meta && r.meta.changes) await env.DB.prepare('INSERT INTO vues_site (site, jour, n) VALUES (?,?,1) ON CONFLICT(site, jour) DO UPDATE SET n = n + 1').bind(b.s, jour).run();
    if (Math.random() < 0.02) await env.DB.prepare("DELETE FROM vues_site_uniq WHERE jour < date('now','-40 days')").run();
  } catch (_) { return rep({ ok: false }, 500); }
  return rep({ ok: true });
}
async function statsSite(env, ref) {
  await ensureSchema(env);
  const q = async (sql, ...a) => (await env.DB.prepare(sql).bind(...a).all()).results || [];
  const t = parisToday();
  const jours = await q("SELECT jour, n FROM vues_site WHERE site = ? AND jour >= date(?, '-29 days') ORDER BY jour", ref, t);
  const som = (n) => jours.filter((x) => x.jour >= plusJours(t, -(n - 1))).reduce((a, x) => a + x.n, 0);
  const uniq = async (n) => ((await q("SELECT COUNT(DISTINCT h) c FROM vues_site_uniq WHERE site = ? AND jour >= date(?, ?)", ref, t, '-' + (n - 1) + ' days'))[0] || {}).c || 0;
  const tot = ((await q('SELECT COALESCE(SUM(n),0) n FROM vues_site WHERE site = ?', ref))[0] || {}).n || 0;
  return { visites_7: som(7), visites_30: som(30), visiteurs_7: await uniq(7), visiteurs_30: await uniq(30), moyenne_jour: Math.round(som(30) / 30 * 10) / 10, total: tot, jours };
}
function plusJours(iso, n) { const d = new Date(iso.slice(0, 10) + 'T12:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); }

// ---------- Administration : à traiter, tâches, suivi, parcours, avis, visites, sauvegarde ----------
const TABLES_SAUVEGARDE = ['comptes', 'demandes', 'abonnements', 'modifs', 'plaintes', 'notifications', 'communications', 'journal', 'reservations', 'contenus', 'retours_apercu', 'dossier', 'taches', 'suivi', 'resiliations', 'parrains', 'parrainages', 'credits', 'avis', 'vues'];
const TABLES_LOURDES = ['medias', 'dossier_fichiers'];
const V2_ADMIN = new Set(['/api/admin/atraiter', '/api/admin/taches', '/api/admin/parcours', '/api/admin/fichier', '/api/admin/avis', '/api/admin/visites', '/api/admin/sauvegarde', '/api/admin/tache', '/api/admin/tache-fait', '/api/admin/tache-suppr', '/api/admin/suivi', '/api/admin/retour-traite', '/api/admin/resiliation-statut', '/api/admin/avis-statut', '/api/admin/credit-utilise', '/api/admin/parrain-appliquer', '/api/admin/parrainages', '/api/admin/mois-offert', '/api/admin/credit-suppr', '/api/admin/litiges', '/api/admin/litige-ajout', '/api/admin/litige-statut', '/api/admin/changement-annuler', '/api/admin/changement-programmer']);
async function adminV2(req, env, url, p, me, one, all) {
  await ensureSchema(env);
  const num = (v) => { const n = parseInt(v, 10); return Number.isFinite(n) ? n : 0; };
  const txt = (v, n) => (typeof v === 'string' ? v.trim().slice(0, n) : '');
  const today = parisToday();
  const client = async (id) => one("SELECT id, nom FROM comptes WHERE id = ? AND role != 'admin'", id);
  if (req.method === 'GET') {
    if (p === '/api/admin/atraiter') {
      await expirerParrainages(env);
      const items = [];
      const add = (niveau, cle, titre, detail, c, date) => items.push({ niveau, cle, titre, detail, compte_id: c ? c.compte_id : null, nom: c ? c.nom : '', date: date || '' });
      const dems = await all("SELECT d.id, d.compte_id, d.commerce, d.statut, d.created_at, c.nom, (SELECT valeur FROM dossier x WHERE x.compte_id = d.compte_id AND x.cle = '_termine') termine, (SELECT MAX(created_at) FROM journal j WHERE j.compte_id = d.compte_id AND j.type = 'site_statut' AND j.detail = 'apercu') apercu_le, (SELECT type FROM retours_apercu r WHERE r.demande_id = d.id AND r.type = 'valide' LIMIT 1) valide FROM demandes d JOIN comptes c ON c.id = d.compte_id WHERE d.id IN (SELECT MAX(id) FROM demandes GROUP BY compte_id) AND d.statut IN ('nouvelle','en_creation','apercu')");
      for (const d of dems) {
        const c = { compte_id: d.compte_id, nom: d.nom }, nomC = d.commerce || d.nom;
        if (d.statut === 'nouvelle') {
          if (d.termine) { const pv = joursOuvres(d.termine, DELAI_JOURS_OUVRES); add(pv < today ? 'urgent' : 'normal', 'dossier_complet', 'Dossier complet : créer le site de ' + nomC, (pv < today ? 'En retard : l’aperçu était promis pour le ' : 'Aperçu à livrer avant le ') + pv.split('-').reverse().join('/'), c, d.termine); }
          else add('normal', 'nouvelle', 'Nouvelle demande : ' + nomC, 'Dossier du client pas encore complet. Contactez-le si besoin.', c, d.created_at);
        } else if (d.statut === 'en_creation') {
          if (d.termine) { const pv = joursOuvres(d.termine, DELAI_JOURS_OUVRES); add(pv < today ? 'urgent' : 'normal', 'creation', 'Site en création : ' + nomC, (pv < today ? 'En retard : aperçu promis le ' : 'Aperçu à livrer avant le ') + pv.split('-').reverse().join('/'), c, d.termine); }
        } else if (d.statut === 'apercu') {
          if (d.valide) add('urgent', 'mettre_en_ligne', 'Aperçu validé : mettre en ligne ' + nomC, 'Le client a validé son aperçu.', c, d.apercu_le);
          else if (d.apercu_le) {
            const j = ecartJours(d.apercu_le, today);
            if (j >= 15) add('urgent', 'relance15', 'Aperçu sans réponse depuis ' + j + ' jours : ' + nomC, 'Délai de 15 jours dépassé (CGV article 6) : voir la clause après relance.', c, d.apercu_le);
            else if (j >= 5) add('normal', 'relance', 'Relancer le client : ' + nomC, 'Aperçu envoyé il y a ' + j + ' jours, sans réponse.', c, d.apercu_le);
          }
        }
      }
      for (const r of await all("SELECT r.id, r.compte_id, r.message, r.created_at, c.nom, d.commerce FROM retours_apercu r JOIN comptes c ON c.id = r.compte_id LEFT JOIN demandes d ON d.id = r.demande_id WHERE r.type = 'changements' AND r.statut = 'a_traiter'")) add('urgent', 'ajustements', 'Ajustements demandés : ' + (r.commerce || r.nom), r.message, { compte_id: r.compte_id, nom: r.nom }, r.created_at);
      for (const m of await all("SELECT m.id, m.compte_id, m.type, m.description, m.created_at, c.nom FROM modifs m JOIN comptes c ON c.id = m.compte_id WHERE m.statut = 'demandee' ORDER BY m.id")) add('normal', 'modif', 'Modification demandée (' + m.type + ')', m.description, { compte_id: m.compte_id, nom: m.nom }, m.created_at);
      for (const r of await all("SELECT r.compte_id, r.motif, r.effet, r.created_at, c.nom FROM resiliations r JOIN comptes c ON c.id = r.compte_id WHERE r.statut = 'demandee'")) add('urgent', 'resiliation', 'Résiliation demandée', 'Motif : ' + (r.motif || 'non précisé') + '. Prend effet le ' + r.effet.split('-').reverse().join('/') + '.', { compte_id: r.compte_id, nom: r.nom }, r.created_at);
      for (const x of await all("SELECT p.compte_id, p.sujet, p.created_at, c.nom FROM plaintes p JOIN comptes c ON c.id = p.compte_id WHERE p.statut != 'resolue'")) add('urgent', 'plainte', 'Réclamation ouverte', x.sujet, { compte_id: x.compte_id, nom: x.nom }, x.created_at);
      await appliquerChangements(env); await synchroLitigesImpayes(env);
      for (const l of await all("SELECT l.compte_id, l.type, l.note, l.created_at, c.nom FROM litiges l JOIN comptes c ON c.id = l.compte_id WHERE l.statut = 'ouvert' AND l.type != 'impaye'")) add('urgent', 'litige', 'Litige : ' + ({ prelevement_rejete: 'prélèvement rejeté', contestation: 'contestation', autre: 'litige' }[l.type] || 'litige'), l.note || 'Voir l’onglet Litiges.', { compte_id: l.compte_id, nom: l.nom }, l.created_at);
      for (const a of await all("SELECT a.compte_id, c.nom FROM abonnements a JOIN comptes c ON c.id = a.compte_id WHERE a.statut = 'impaye'")) add('urgent', 'impaye', 'Impayé', 'L’abonnement est en impayé : relancer le client.', { compte_id: a.compte_id, nom: a.nom }, '');
      for (const s of await all("SELECT s.compte_id, s.rappel_le, s.motif, c.nom FROM suivi s JOIN comptes c ON c.id = s.compte_id WHERE s.rappel_le IS NOT NULL AND s.rappel_le != '' AND s.rappel_le <= ?", today)) add(s.rappel_le < today ? 'urgent' : 'normal', 'rappel', 'À rappeler', s.motif || 'Rappel prévu le ' + s.rappel_le.split('-').reverse().join('/'), { compte_id: s.compte_id, nom: s.nom }, s.rappel_le);
      for (const t of await all("SELECT t.id, t.compte_id, t.titre, t.detail, t.echeance, c.nom FROM taches t LEFT JOIN comptes c ON c.id = t.compte_id WHERE t.fait = 0 AND (t.echeance IS NULL OR t.echeance = '' OR t.echeance <= ?) ORDER BY t.id", today)) { add(t.echeance && t.echeance < today ? 'urgent' : 'normal', 'tache', t.titre, t.detail || '', t.compte_id ? { compte_id: t.compte_id, nom: t.nom } : null, t.echeance || ''); }
      for (const a of await all("SELECT a.compte_id, a.note, a.commerce, c.nom, a.created_at FROM avis a JOIN comptes c ON c.id = a.compte_id WHERE a.statut = 'en_attente'")) add('normal', 'avis', 'Avis à modérer (' + a.note + '/5)', a.commerce || '', { compte_id: a.compte_id, nom: a.nom }, a.created_at);
      const ord = { urgent: 0, normal: 1 };
      items.sort((x, y) => ord[x.niveau] - ord[y.niveau]);
      return json({ ok: true, aujourdhui: today, urgents: items.filter((i) => i.niveau === 'urgent').length, items });
    }
    if (p === '/api/admin/taches') {
      const cid = num(url.searchParams.get('compte_id'));
      const rows = cid ? await all('SELECT id, compte_id, titre, detail, echeance, fait, created_at, fait_at FROM taches WHERE compte_id = ? ORDER BY fait, id DESC LIMIT 200', cid)
        : await all('SELECT t.id, t.compte_id, t.titre, t.detail, t.echeance, t.fait, t.created_at, t.fait_at, c.nom FROM taches t LEFT JOIN comptes c ON c.id = t.compte_id ORDER BY t.fait, t.id DESC LIMIT 300');
      return json({ ok: true, taches: rows });
    }
    if (p === '/api/admin/parcours') {
      const id = num(url.searchParams.get('compte_id'));
      if (!(await client(id))) return json({ ok: false }, 404);
      const d = await one('SELECT id, statut FROM demandes WHERE compte_id = ? ORDER BY id DESC LIMIT 1', id);
      const dos = await dossierDe(env, id), code = await codeDe(env, id);
      return json({ ok: true, dossier: dos, manquants: manquants(dos).map((k) => DOSSIER_LIBELLES[k]), fichiers: await all('SELECT id, categorie, nom, mime, taille, created_at FROM dossier_fichiers WHERE compte_id = ? ORDER BY id', id),
        retours: await all('SELECT id, type, message, statut, created_at FROM retours_apercu WHERE compte_id = ? ORDER BY id DESC LIMIT 20', id),
        resiliations: await all('SELECT id, motif, message, effet, decale, statut, created_at FROM resiliations WHERE compte_id = ? ORDER BY id DESC LIMIT 10', id),
        changements: await changementsDe(env, id), litiges: await all('SELECT id, type, montant_ttc, periode, note, statut, created_at FROM litiges WHERE compte_id = ? ORDER BY id DESC LIMIT 20', id),
        suivi: (await one('SELECT rappel_le, motif FROM suivi WHERE compte_id = ?', id)) || { rappel_le: '', motif: '' },
        parrainage: { code, filleuls: await all('SELECT p.statut, p.created_at, c.nom, c.id compte_id FROM parrainages p JOIN comptes c ON c.id = p.filleul_id WHERE p.parrain_id = ? ORDER BY p.id DESC', id), parrain: await one('SELECT p.code, p.statut, p.parrain_id, c.nom FROM parrainages p JOIN comptes c ON c.id = p.parrain_id WHERE p.filleul_id = ?', id), credits: (await all('SELECT id, mois, origine, utilise_at, expire_at, created_at, mois_offert FROM credits WHERE compte_id = ? ORDER BY id DESC', id)).map((c) => ({ ...c, etat: etatCredit(c, today) })) },
        avis: await one('SELECT id, note, commentaire, statut FROM avis WHERE compte_id = ?', id), demande: d });
    }
    if (p === '/api/admin/litiges') {
      await synchroLitigesImpayes(env);
      const lignes = await all("SELECT l.id, l.compte_id, l.type, l.montant_ttc, l.periode, l.note, l.source, l.statut, l.created_at, l.clos_at, c.nom, c.email, (SELECT commerce FROM demandes d WHERE d.compte_id = l.compte_id ORDER BY d.id DESC LIMIT 1) commerce, (SELECT tel FROM demandes d WHERE d.compte_id = l.compte_id ORDER BY d.id DESC LIMIT 1) tel FROM litiges l JOIN comptes c ON c.id = l.compte_id ORDER BY CASE l.statut WHEN 'ouvert' THEN 0 ELSE 1 END, l.id DESC LIMIT 300");
      const ouv = lignes.filter((l) => l.statut === 'ouvert');
      return json({ ok: true, ouverts: ouv.length, montant_ouvert: Math.round(ouv.reduce((t, l) => t + (l.montant_ttc || 0), 0) * 100) / 100, lignes });
    }
    if (p === '/api/admin/fichier') { const id = num(url.searchParams.get('id')); return id ? envoiFichier(env, id, null) : json({ ok: false }, 400); }
    if (p === '/api/admin/avis') return json({ ok: true, avis: await all('SELECT id, compte_id, note, commentaire, nom, commerce, statut, created_at, publie_at FROM avis ORDER BY id DESC LIMIT 200') });
    if (p === '/api/admin/parrainages') {
      await expirerParrainages(env);
      const lignes = await all("SELECT p.id, p.statut, p.code, p.created_at, p.valide_at, pa.id parrain_id, pa.nom parrain, fi.id filleul_id, fi.nom filleul, (SELECT commerce FROM demandes d WHERE d.compte_id = pa.id ORDER BY d.id DESC LIMIT 1) parrain_commerce, (SELECT commerce FROM demandes d WHERE d.compte_id = fi.id ORDER BY d.id DESC LIMIT 1) filleul_commerce FROM parrainages p JOIN comptes pa ON pa.id = p.parrain_id JOIN comptes fi ON fi.id = p.filleul_id ORDER BY p.id DESC LIMIT 500");
      const top = await all("SELECT pa.id compte_id, pa.nom, COUNT(*) n, SUM(CASE WHEN p.statut = 'valide' THEN 1 ELSE 0 END) valides FROM parrainages p JOIN comptes pa ON pa.id = p.parrain_id GROUP BY pa.id ORDER BY valides DESC, n DESC LIMIT 10");
      const offerts = await all("SELECT c.id, c.compte_id, c.origine, c.mois_offert, c.utilise_at, c.created_at, co.nom FROM credits c JOIN comptes co ON co.id = c.compte_id ORDER BY c.id DESC LIMIT 300");
      const cnt = (s) => lignes.filter((l) => l.statut === s).length;
      return json({ ok: true, total: lignes.length, valides: cnt('valide'), en_attente: cnt('en_attente'), expires: cnt('expire'), mois_parrainage: offerts.filter((o) => o.origine !== 'admin').length, mois_admin: offerts.filter((o) => o.origine === 'admin').length, lignes, top, offerts: offerts.map((o) => ({ ...o, etat: etatCredit(o, today) })) });
    }
    if (p === '/api/admin/visites') {
      return json({ ok: true, jours: await all("SELECT jour, SUM(n) n FROM vues WHERE jour >= date('now','-30 days') GROUP BY jour ORDER BY jour"), pages: await all("SELECT page, SUM(n) n FROM vues WHERE jour >= date('now','-30 days') GROUP BY page ORDER BY n DESC LIMIT 15"),
        total30: ((await one("SELECT COALESCE(SUM(n),0) n FROM vues WHERE jour >= date('now','-30 days')")) || {}).n || 0, total7: ((await one("SELECT COALESCE(SUM(n),0) n FROM vues WHERE jour >= date('now','-7 days')")) || {}).n || 0 });
    }
    if (p === '/api/admin/sauvegarde') {
      const lourd = url.searchParams.get('medias') === '1', tables = {};
      for (const t of TABLES_SAUVEGARDE.concat(lourd ? TABLES_LOURDES : [])) {
        try { tables[t] = await all('SELECT * FROM ' + t + ' LIMIT 100000'); } catch (_) { tables[t] = null; }
      }
      await log(env, null, me.id, 'sauvegarde', lourd ? 'avec fichiers' : 'données');
      const res = new Response(JSON.stringify({ ok: true, version: 2, genere_le: new Date().toISOString(), contient_fichiers: lourd, tables }), { headers: { 'content-type': 'application/json; charset=utf-8', 'content-disposition': 'attachment; filename="sauvegarde-devanture-web-' + today + '.json"', 'cache-control': 'no-store', ...SEC } });
      return res;
    }
    return null;
  }
  if (req.method !== 'POST') return null;
  const { b, err } = await readJson(req, url, 4000); if (err) return err;
  if (p === '/api/admin/tache') {
    const titre = txt(b.titre, 140), cid = num(b.compte_id) || null;
    if (!titre) return json({ ok: false, error: 'titre' }, 422);
    if (cid && !(await client(cid))) return json({ ok: false }, 404);
    const ech = typeof b.echeance === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(b.echeance) ? b.echeance : null;
    const r = await env.DB.prepare('INSERT INTO taches (compte_id, titre, detail, echeance) VALUES (?,?,?,?)').bind(cid, titre, txt(b.detail, 800), ech).run();
    return json({ ok: true, id: r.meta.last_row_id });
  }
  if (p === '/api/admin/tache-fait') {
    await env.DB.prepare("UPDATE taches SET fait = ?, fait_at = CASE WHEN ? = 1 THEN datetime('now') ELSE NULL END WHERE id = ?").bind(b.fait ? 1 : 0, b.fait ? 1 : 0, num(b.id)).run();
    return json({ ok: true });
  }
  if (p === '/api/admin/tache-suppr') { await env.DB.prepare('DELETE FROM taches WHERE id = ?').bind(num(b.id)).run(); return json({ ok: true }); }
  if (p === '/api/admin/suivi') {
    const cid = num(b.compte_id); if (!(await client(cid))) return json({ ok: false }, 404);
    const r = typeof b.rappel_le === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(b.rappel_le) ? b.rappel_le : '';
    await env.DB.prepare("INSERT INTO suivi (compte_id, rappel_le, motif, updated_at) VALUES (?,?,?,datetime('now')) ON CONFLICT(compte_id) DO UPDATE SET rappel_le = excluded.rappel_le, motif = excluded.motif, updated_at = excluded.updated_at").bind(cid, r, txt(b.motif, 200)).run();
    return json({ ok: true });
  }
  if (p === '/api/admin/retour-traite') {
    const r = await one('SELECT id, compte_id, type, statut FROM retours_apercu WHERE id = ?', num(b.id)); if (!r) return json({ ok: false }, 404);
    await env.DB.prepare("UPDATE retours_apercu SET statut = 'traite', traite_at = datetime('now') WHERE id = ?").bind(r.id).run();
    if (r.type === 'changements' && r.statut === 'a_traiter') await notifier(env, r.compte_id, 'Ajustements effectués', 'Vos ajustements ont été appliqués. Regardez à nouveau l’aperçu, puis validez-le ou demandez d’autres changements.');
    await log(env, r.compte_id, me.id, 'retour_traite', r.type);
    return json({ ok: true });
  }
  if (p === '/api/admin/changement-programmer') {
    const cid = num(b.compte_id); if (!(await client(cid))) return json({ ok: false }, 404);
    const abo = await one('SELECT formule, statut, mails_sup FROM abonnements WHERE compte_id = ?', cid);
    if (!abo || abo.statut !== 'actif') return json({ ok: false, error: 'pas-actif' }, 409);
    if (!FORMULES.includes(b.vers) || b.vers === abo.formule) return json({ ok: false, error: 'formule' }, 422);
    if (await one("SELECT id FROM changements_formule WHERE compte_id = ? AND statut = 'demande'", cid)) return json({ ok: false, error: 'deja' }, 409);
    const effet = premierMoisSuivant(parisToday());
    await env.DB.prepare('INSERT INTO changements_formule (compte_id, de, vers, effet) VALUES (?,?,?,?)').bind(cid, abo.formule, b.vers, effet).run();
    await log(env, cid, me.id, 'changement_formule_demande', abo.formule + ' → ' + b.vers + ' / effet ' + effet);
    await notifier(env, cid, 'Changement de formule enregistré', 'Votre passage à la formule ' + (b.vers === 'pro' ? 'Pro' : 'Essentiel') + ' prendra effet le ' + effet.split('-').reverse().join('/') + '. Le mois en cours reste facturé à la formule actuelle.');
    return json({ ok: true, effet });
  }
  if (p === '/api/admin/changement-annuler') {
    const r = await env.DB.prepare("UPDATE changements_formule SET statut = 'annule', applique_at = datetime('now') WHERE id = ? AND statut = 'demande'").bind(num(b.id)).run();
    if (!(r.meta && r.meta.changes)) return json({ ok: false }, 404);
    return json({ ok: true });
  }
  if (p === '/api/admin/litige-ajout') {
    const cid = num(b.compte_id), type = TYPES_LITIGE.includes(b.type) ? b.type : 'autre';
    if (!(await client(cid))) return json({ ok: false }, 404);
    const m = Number(b.montant), id = await ouvrirLitige(env, cid, type, { montant: Number.isFinite(m) && m >= 0 ? Math.round(m * 100) / 100 : null, periode: txt(b.periode, 20), note: txt(b.note, 500), source: 'manuel' });
    await log(env, cid, me.id, 'litige_ouvert', type);
    return json({ ok: true, id });
  }
  if (p === '/api/admin/litige-statut') {
    const l = await one('SELECT id, compte_id FROM litiges WHERE id = ?', num(b.id)); if (!l || !['ouvert', 'regle', 'abandonne'].includes(b.statut)) return json({ ok: false }, 404);
    const nt = txt(b.note, 500);
    await env.DB.prepare("UPDATE litiges SET statut = ?, clos_at = CASE WHEN ? = 'ouvert' THEN NULL ELSE datetime('now') END, note = CASE WHEN ? != '' THEN ? ELSE note END WHERE id = ?").bind(b.statut, b.statut, nt, nt, l.id).run();
    await log(env, l.compte_id, me.id, 'litige_' + b.statut, '');
    return json({ ok: true });
  }
  if (p === '/api/admin/resiliation-statut') {
    if (!['traitee', 'refusee', 'demandee'].includes(b.statut)) return json({ ok: false }, 422);
    const r = await one('SELECT id, compte_id FROM resiliations WHERE id = ?', num(b.id)); if (!r) return json({ ok: false }, 404);
    await env.DB.prepare("UPDATE resiliations SET statut = ?, traite_at = CASE WHEN ? = 'demandee' THEN NULL ELSE datetime('now') END WHERE id = ?").bind(b.statut, b.statut, r.id).run();
    await log(env, r.compte_id, me.id, 'resiliation_' + b.statut, '');
    return json({ ok: true });
  }
  if (p === '/api/admin/avis-statut') {
    if (!['publie', 'refuse', 'en_attente'].includes(b.statut)) return json({ ok: false }, 422);
    await env.DB.prepare("UPDATE avis SET statut = ?, publie_at = CASE WHEN ? = 'publie' THEN datetime('now') ELSE NULL END WHERE id = ?").bind(b.statut, b.statut, num(b.id)).run();
    return json({ ok: true });
  }
  if (p === '/api/admin/credit-utilise') {
    await env.DB.prepare("UPDATE credits SET utilise_at = CASE WHEN ? = 1 THEN datetime('now') ELSE NULL END WHERE id = ?").bind(b.utilise ? 1 : 0, num(b.id)).run();
    return json({ ok: true });
  }
  if (p === '/api/admin/mois-offert') {
    const cid = num(b.compte_id); if (!(await client(cid))) return json({ ok: false }, 404);
    const n = num(b.mois); if (n < 1 || n > 12) return json({ ok: false, error: 'mois' }, 422);
    const ab = await one('SELECT statut FROM abonnements WHERE compte_id = ?', cid);
    if (!ab || ab.statut === 'resilie') return json({ ok: false, error: 'pas-abonne' }, 422);
    const ms = await moisLibres(env, cid, n), motif = txt(b.motif, 120) || 'geste commercial';
    await env.DB.batch(ms.map((m) => env.DB.prepare("INSERT INTO credits (compte_id, mois, origine, mois_offert, expire_at) VALUES (?,1,'admin',?, NULL)").bind(cid, m)));
    await log(env, cid, me.id, 'mois_offert', n + ' mois : ' + ms.join(', ') + ' (' + motif + ')');
    await notifier(env, cid, n > 1 ? n + ' mois offerts' : 'Un mois offert', (n > 1 ? 'Les mois de ' + ms.map(moisFr).join(', ') + ' ne vous seront pas facturés.' : 'Le mois de ' + moisFr(ms[0]) + ' ne vous sera pas facturé.') + ' Merci pour votre confiance.');
    return json({ ok: true, mois: ms });
  }
  if (p === '/api/admin/credit-suppr') {
    const c = await one('SELECT id, compte_id, mois_offert FROM credits WHERE id = ?', num(b.id)); if (!c) return json({ ok: false }, 404);
    if (!c.mois_offert || c.mois_offert <= today.slice(0, 7)) return json({ ok: false, error: 'deja-applique' }, 409);
    await env.DB.prepare('DELETE FROM credits WHERE id = ?').bind(c.id).run();
    await log(env, c.compte_id, me.id, 'mois_offert_annule', c.mois_offert);
    return json({ ok: true });
  }
  if (p === '/api/admin/parrain-appliquer') {
    const cid = num(b.compte_id); if (!(await client(cid))) return json({ ok: false }, 404);
    const r = await appliquerParrain(env, cid, b.code);
    return json(r, r.ok ? 200 : 422);
  }
  return null;
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    let p = url.pathname;
    if (p.length > 1 && p.endsWith('/')) p = p.slice(0, -1);
    if (p.startsWith('/api/espace')) return espace(req, env, url, p);
    if (p === '/desinscription') return desinscription(req, env, url);
    if (p === '/api/mot-de-passe-oublie') return oubli(req, env, url);
    if (p === '/api/reinitialiser') return reinitialiser(req, env, url);
    if (p === '/api/demande') return demande(req, env, url);
    if (p === '/api/avis' && req.method === 'GET') return avisPublics(req, env);
    if (p === '/api/vue') return vue(req, env, url);
    if (p === '/api/vue-site') return vueSite(req, env, url);
    if (p === '/api/reservation') return reservation(req, env, url);
    if (p === '/api/inscription/config') return inscriptionConfig(env);
    if (p === '/api/inscription/code') return inscriptionCode(req, env, url);
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
    const mm = p.match(/^\/media\/(\d+)$/);
    if (mm) { const rm = await media(env, parseInt(mm[1], 10)); if (rm) return rm; }
    if (SITE_RE.test(p)) { const re = await exemple(req, env, p); if (re) return re; }
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
