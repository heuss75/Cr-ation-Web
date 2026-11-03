// Banc d'essai : exécute le vrai worker.js sur une base SQLite en mémoire, sert /site en local, capture les e-mails.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { DatabaseSync } from 'node:sqlite';

const REPO_DIR = process.env.REPO_DIR;
const PORT = parseInt(process.env.PORT || '8787', 10);
const GH = 'https://raw.githubusercontent.com/heuss75/Cr-ation-Web/main/site';

const SCHEMA = `
CREATE TABLE comptes (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL UNIQUE, nom TEXT, salt TEXT, hash TEXT, iter INTEGER, ip_hash TEXT, role TEXT NOT NULL DEFAULT 'client', demo INTEGER NOT NULL DEFAULT 0, opt_out INTEGER NOT NULL DEFAULT 0, derniere_connexion TEXT, created_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE sessions (token_hash TEXT PRIMARY KEY, compte_id INTEGER NOT NULL, expires_at TEXT NOT NULL, par_admin INTEGER);
CREATE TABLE essais (id INTEGER PRIMARY KEY AUTOINCREMENT, ip_hash TEXT, at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE journal (id INTEGER PRIMARY KEY AUTOINCREMENT, compte_id INTEGER, admin_id INTEGER, type TEXT, detail TEXT, created_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE reset_tokens (token_hash TEXT PRIMARY KEY, compte_id INTEGER NOT NULL, expires_at TEXT NOT NULL, used INTEGER NOT NULL DEFAULT 0);
CREATE TABLE demandes (id INTEGER PRIMARY KEY AUTOINCREMENT, ref TEXT, nom TEXT, email TEXT, tel TEXT, commerce TEXT, activite TEXT, ville TEXT, domaine TEXT, mails INTEGER, message TEXT, utm TEXT, page TEXT, ip_hash TEXT, ua TEXT, formule TEXT, compte_id INTEGER, statut TEXT NOT NULL DEFAULT 'nouvelle', suspendu INTEGER NOT NULL DEFAULT 0, site_url TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE abonnements (compte_id INTEGER PRIMARY KEY, formule TEXT, statut TEXT, mails_sup INTEGER DEFAULT 0, debut TEXT, fin TEXT, motif TEXT, created_at TEXT NOT NULL DEFAULT (datetime('now')), updated_at TEXT);
CREATE TABLE modifs (id INTEGER PRIMARY KEY AUTOINCREMENT, compte_id INTEGER, type TEXT, description TEXT, statut TEXT NOT NULL DEFAULT 'demandee', created_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE plaintes (id INTEGER PRIMARY KEY AUTOINCREMENT, compte_id INTEGER, sujet TEXT, message TEXT, statut TEXT NOT NULL DEFAULT 'ouverte', created_at TEXT NOT NULL DEFAULT (datetime('now')), resolved_at TEXT);
CREATE TABLE notifications (id INTEGER PRIMARY KEY AUTOINCREMENT, compte_id INTEGER, titre TEXT, message TEXT, lu INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE communications (id INTEGER PRIMARY KEY AUTOINCREMENT, sujet TEXT, corps TEXT, nb INTEGER, nb_mail INTEGER, notif INTEGER, statut TEXT, filtre TEXT, created_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE reservations (id INTEGER PRIMARY KEY AUTOINCREMENT, ref TEXT, site TEXT, jour TEXT, heure TEXT, service TEXT, nom TEXT, tel TEXT, ip_hash TEXT, created_at TEXT NOT NULL DEFAULT (datetime('now')), UNIQUE(site, jour, heure));
CREATE TABLE contenus (compte_id INTEGER, cle TEXT, valeur TEXT, updated_at TEXT, PRIMARY KEY (compte_id, cle));
CREATE TABLE medias (id INTEGER PRIMARY KEY AUTOINCREMENT, compte_id INTEGER, mime TEXT, data TEXT);
`;

let db;
function fresh() { db = new DatabaseSync(':memory:'); db.exec(SCHEMA); }
fresh();

class Stmt {
  constructor(sql) { this.sql = sql; this.args = []; }
  bind(...a) { const n = new Stmt(this.sql); n.args = a; return n; }
  async first() { const r = db.prepare(this.sql).get(...this.args); return r ? { ...r } : null; }
  async all() { return { results: db.prepare(this.sql).all(...this.args).map((r) => ({ ...r })) }; }
  async run() { const i = db.prepare(this.sql).run(...this.args); return { success: true, meta: { last_row_id: Number(i.lastInsertRowid), changes: Number(i.changes) } }; }
}
const DB = {
  prepare: (sql) => new Stmt(sql),
  async batch(stmts) {
    db.exec('BEGIN');
    try { const out = []; for (const s of stmts) out.push(await s.run()); db.exec('COMMIT'); return out; } catch (e) { db.exec('ROLLBACK'); throw e; }
  },
};

const env = { DB };
const mails = [];
const resendCalls = [];

// --- fetch simulé : GitHub -> fichiers locaux ; Resend -> capture
const realFetch = globalThis.fetch;
globalThis.fetch = async (input, init) => {
  const u = typeof input === 'string' ? input : input.url;
  if (u.startsWith(GH + '/')) {
    const f = path.join(REPO_DIR, 'site', u.slice(GH.length + 1));
    if (!fs.existsSync(f) || !fs.statSync(f).isFile()) return new Response('nf', { status: 404 });
    return new Response(fs.readFileSync(f), { status: 200 });
  }
  if (u === 'https://api.resend.com/emails') {
    if (env.RESEND_FAIL) return new Response('{}', { status: 500 });
    const b = JSON.parse(init.body); mails.push(b); return new Response('{"id":"x"}', { status: 200 });
  }
  if (u === 'https://api.resend.com/emails/batch') {
    if (env.RESEND_FAIL) return new Response('{}', { status: 500 });
    const arr = JSON.parse(init.body); arr.forEach((b) => mails.push(b)); resendCalls.push(arr.length); return new Response('{"data":[]}', { status: 200 });
  }
  return realFetch(input, init);
};

// --- HTMLRewriter minimal (suffisant pour [data-k])
globalThis.HTMLRewriter = class {
  constructor() { this.h = null; }
  on(sel, h) { this.h = h; return this; }
  transform(resp) {
    const h = this.h;
    const body = (async () => {
      let t = await resp.text();
      t = t.replace(/<(\w+)([^>]*?\sdata-k="([^"]*)"[^>]*)>/g, (m, tag, attrs, k) => {
        const el = { tagName: tag.toLowerCase(), _attrs: attrs, _inner: undefined, getAttribute: (n) => (n === 'data-k' ? k : null),
          setAttribute(n, v) { this._attrs = this._attrs.replace(new RegExp('\\s' + n + '="[^"]*"'), '') + ' ' + n + '="' + v + '"'; },
          removeAttribute(n) { this._attrs = this._attrs.replace(new RegExp('\\s' + n + '="[^"]*"'), ''); },
          setInnerContent(s) { this._inner = s; } };
        h.element(el);
        return '<' + tag + el._attrs + '>' + (el._inner !== undefined ? '\u0000INNER:' + Buffer.from(String(el._inner)).toString('base64') + '\u0000' : '');
      });
      // remplace le contenu jusqu'à la balise fermante de même nom
      t = t.replace(/\u0000INNER:([A-Za-z0-9+/=]*)\u0000([\s\S]*?)<\/(\w+)>/g, (m, b64, old, tag) => {
        const s = Buffer.from(b64, 'base64').toString('utf8').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
        return s + '</' + tag + '>';
      });
      return t;
    })();
    return new Response(new ReadableStream({ async start(c) { c.enqueue(new TextEncoder().encode(await body)); c.close(); } }), { status: resp.status, headers: resp.headers });
  }
};

const { default: worker } = await import(process.env.WORKER_PATH);

const server = http.createServer(async (rq, rs) => {
  const chunks = []; for await (const c of rq) chunks.push(c);
  const body = Buffer.concat(chunks);
  const url = new URL(rq.url, 'http://' + (rq.headers.host || ('localhost:' + PORT)));
  if (url.pathname.startsWith('/__test/')) {
    const send = (o, code = 200) => { rs.writeHead(code, { 'content-type': 'application/json' }); rs.end(JSON.stringify(o)); };
    if (url.pathname === '/__test/mails') return send(mails);
    if (url.pathname === '/__test/reset') { fresh(); if (globalThis.__schemaReset) globalThis.__schemaReset(); mails.length = 0; resendCalls.length = 0; env.RESEND_API_KEY = ''; env.MAIL_FROM = ''; env.RESEND_FAIL = false; return send({ ok: true }); }
    if (url.pathname === '/__test/mail') { const j = JSON.parse(body.toString() || '{}'); env.RESEND_API_KEY = j.on ? 'test-key' : ''; env.MAIL_FROM = j.on ? 'Devanture Web <no-reply@test.invalid>' : ''; env.RESEND_FAIL = !!j.fail; return send({ ok: true }); }
    if (url.pathname === '/__test/batches') return send(resendCalls);
    if (url.pathname === '/__test/sql') {
      const j = JSON.parse(body.toString());
      try {
        const st = db.prepare(j.sql);
        if (/^\s*select/i.test(j.sql)) return send({ rows: st.all(...(j.args || [])).map((r) => ({ ...r })) });
        const i = st.run(...(j.args || [])); return send({ changes: Number(i.changes), id: Number(i.lastInsertRowid) });
      } catch (e) { return send({ error: String(e.message) }, 400); }
    }
    return send({}, 404);
  }
  const headers = new Headers();
  for (const [k, v] of Object.entries(rq.headers)) if (v !== undefined) headers.set(k, Array.isArray(v) ? v.join(', ') : v);
  headers.set('cf-connecting-ip', rq.headers['x-test-ip'] || '203.0.113.1');
  const init = { method: rq.method, headers };
  if (!['GET', 'HEAD'].includes(rq.method) && body.length) init.body = body;
  const resp = await worker.fetch(new Request(url, init), env);
  const h = {};
  resp.headers.forEach((v, k) => { if (k !== 'set-cookie') h[k] = v; });
  const sc = resp.headers.getSetCookie ? resp.headers.getSetCookie() : [];
  if (sc.length) h['set-cookie'] = sc;
  rs.writeHead(resp.status, h);
  rs.end(Buffer.from(await resp.arrayBuffer()));
});
server.listen(PORT, '127.0.0.1', () => console.log('bench up on', PORT));
