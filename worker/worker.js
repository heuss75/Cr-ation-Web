// Worker Cloudflare : sert le site depuis GitHub (dossier /site) et reçoit les demandes du formulaire (base D1).
const REPO = 'https://raw.githubusercontent.com/heuss75/Cr-ation-Web/main/site';
const ROUTES = {
  '/': 'index.html', '/offre': 'offre.html', '/faq': 'faq.html', '/commander': 'commander.html', '/connexion': 'connexion.html',
  '/mentions-legales': 'mentions-legales.html', '/cgv': 'cgv.html', '/confidentialite': 'confidentialite.html', '/cookies': 'cookies.html',
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
    await env.DB.prepare('INSERT INTO demandes (ref, nom, email, tel, commerce, activite, ville, domaine, mails, message, utm, page, ip_hash, ua) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
      .bind(ref, t('nom', 80), t('email', 120), t('tel', 20), t('commerce', 80), t('activite', 20), t('ville', 60), t('domaine', 70), parseInt(b.mails, 10) || 0, t('message', 1000), utm, t('page', 60), iph, (req.headers.get('user-agent') || '').slice(0, 200)).run();
  } catch (_) {
    return json({ ok: false }, 500);
  }
  return json({ ok: true, ref });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    let p = url.pathname;
    if (p.length > 1 && p.endsWith('/')) p = p.slice(0, -1);
    if (p === '/api/demande') return demande(req, env, url);
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
