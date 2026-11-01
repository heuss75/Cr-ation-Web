/* Espace admin indépendant : tableau de bord, clients, abonnements, plaintes, connexion « en tant que ». Le texte venant de la base passe toujours par textContent. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var NS = 'http://www.w3.org/2000/svg';
  function h(tag, attrs) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'class') e.className = attrs[k]; else if (k === 'text') e.textContent = attrs[k];
      else if (k.slice(0, 2) === 'on') e.addEventListener(k.slice(2), attrs[k]); else if (attrs[k] !== null && attrs[k] !== undefined) e.setAttribute(k, attrs[k]);
    });
    (function add(list) { for (var i = 0; i < list.length; i++) { var c = list[i]; if (c === null || c === undefined || c === false) continue; if (Array.isArray(c)) add(c); else e.appendChild(typeof c === 'string' || typeof c === 'number' ? document.createTextNode(String(c)) : c); } })(Array.prototype.slice.call(arguments, 2));
    return e;
  }
  function s(tag, attrs) { var e = document.createElementNS(NS, tag); Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); }); for (var i = 2; i < arguments.length; i++) if (arguments[i]) e.appendChild(arguments[i]); return e; }
  function api(path, method, body) {
    return fetch(path, { method: method || 'GET', credentials: 'same-origin', headers: body ? { 'content-type': 'application/json' } : {}, body: body ? JSON.stringify(body) : undefined })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { s: r.status, j: j }; }); });
  }
  var IC = {
    users: 'M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8',
    file: 'M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8zM14 3v5h5M9 13h6M9 17h6',
    euro: 'M18 6.5A7 7 0 1 0 18 17.5M4 10h9M4 14h9',
    repeat: 'M17 2l4 4-4 4M3 11V9a3 3 0 0 1 3-3h15M7 22l-4-4 4-4M21 13v2a3 3 0 0 1-3 3H3',
    globe: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18',
    alert: 'M12 9v4M12 17h.01M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0',
    check: 'M20 6L9 17l-5-5',
    trend: 'M3 17l6-6 4 4 8-8M15 7h6v6',
    home: 'M3 11l9-8 9 8v9a2 2 0 0 1-2 2h-4v-7H9v7H5a2 2 0 0 1-2-2z',
    key: 'M21 2l-2 2m-7.6 7.6a5.5 5.5 0 1 1-7.8 7.8 5.5 5.5 0 0 1 7.8-7.8zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4',
    out: 'M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9',
    ext: 'M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3',
    card: 'M2 7a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2zM2 10h20',
    msg: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'
  };
  function ico(n, size, color) { return s('svg', { width: size || 20, height: size || 20, viewBox: '0 0 24 24', fill: 'none', stroke: color || 'currentColor', 'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'aria-hidden': 'true' }, s('path', { d: IC[n] })); }
  var LBL = { nouvelle: 'À traiter', en_creation: 'En création', apercu: 'Aperçu envoyé', en_ligne: 'En ligne', abandonnee: 'Abandonnée', actif: 'Actif', impaye: 'Impayé', suspendu: 'Suspendu', resilie: 'Résilié', ouverte: 'Ouverte', en_cours: 'En cours', resolue: 'Résolue', essentiel: 'Essentiel', pro: 'Pro' };
  var lab = function (k) { return LBL[k] || k || '—'; };
  var COL = { pri: '#4f46e5', sky: '#0ea5e9', ok: '#10b981', warn: '#f59e0b', bad: '#ef4444', gray: '#94a3b8', pur: '#7c3aed' };
  var eur = function (n) { return (Math.round((n || 0) * 10) / 10).toLocaleString('fr-FR') + ' €'; };
  var num = function (n) { return (n || 0).toLocaleString('fr-FR'); };
  function dt(x) { if (!x) return '—'; var d = new Date(x.replace(' ', 'T') + 'Z'); return isNaN(d) ? x : d.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' }) + ' ' + d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }); }
  function dOnly(x) { if (!x) return '—'; var d = new Date(x + 'T12:00:00Z'); return isNaN(d) ? x : d.toLocaleDateString('fr-FR'); }
  function pillFor(k) { var c = { en_ligne: 'ok', actif: 'ok', resolue: 'ok', apercu: 'pri', en_creation: 'pri', en_cours: 'warn', nouvelle: 'warn', ouverte: 'bad', impaye: 'bad', abandonnee: '', resilie: 'bad', suspendu: 'warn' }[k]; return h('span', { class: 'pill ' + (c || ''), text: lab(k) }); }
  var main = $('#main'), toast = $('#toast');
  function flash(t, bad) { toast.textContent = t; toast.className = 'toast on' + (bad ? ' bad' : ''); clearTimeout(flash.t); flash.t = setTimeout(function () { toast.className = 'toast'; }, 3800); }

  /* ----- briques graphiques ----- */
  function hero(color, icon, value, label, badge, down) { return h('div', { class: 'card hero' }, h('div', { class: 'ic ' + color }, ico(icon, 22)), h('div', null, h('b', { text: value }), h('span', { text: label }), badge ? h('em', { class: down ? 'dn' : '', text: badge }) : null)); }
  function mini(items) { return h('div', { class: 'mini' }, items.map(function (i) { return h('div', null, h('b', { text: i[1] }), h('span', { text: i[0] })); })); }
  function area(jours) {
    var map = {}; jours.forEach(function (j) { map[j.d] = j.n; });
    var days = [], now = new Date(), i;
    for (i = 29; i >= 0; i--) days.push(new Date(now.getTime() - i * 864e5).toISOString().slice(0, 10));
    var vals = days.map(function (d) { return map[d] || 0; }), max = Math.max.apply(null, vals.concat([3]));
    var W = 640, H = 190, L = 28, B = 24, T = 10, iw = W - L - 6, ih = H - B - T;
    var X = function (k) { return L + (iw * k) / 29; }, Y = function (v) { return T + ih - (ih * v) / max; };
    var svg = s('svg', { class: 'chart', viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Inscriptions des 30 derniers jours' });
    var defs = s('defs', null, (function () { var g = s('linearGradient', { id: 'ga', x1: 0, y1: 0, x2: 0, y2: 1 }); g.appendChild(s('stop', { offset: '0%', 'stop-color': COL.pri, 'stop-opacity': '.35' })); g.appendChild(s('stop', { offset: '100%', 'stop-color': COL.pri, 'stop-opacity': '0' })); return g; })());
    svg.appendChild(defs);
    [0, 1, 2, 3].forEach(function (k) { var y = T + (ih * k) / 3; svg.appendChild(s('line', { x1: L, x2: W - 6, y1: y, y2: y, class: 'gl', 'stroke-dasharray': '3 4' })); var t = s('text', { x: 0, y: y + 3 }); t.textContent = Math.round(max - (max * k) / 3); svg.appendChild(t); });
    var pts = vals.map(function (v, k) { return [X(k), Y(v)]; }), d = 'M' + pts[0][0] + ' ' + pts[0][1];
    for (i = 1; i < pts.length; i++) { var cx = (pts[i - 1][0] + pts[i][0]) / 2; d += ' C' + cx + ' ' + pts[i - 1][1] + ' ' + cx + ' ' + pts[i][1] + ' ' + pts[i][0] + ' ' + pts[i][1]; }
    svg.appendChild(s('path', { d: d + ' L' + X(29) + ' ' + (T + ih) + ' L' + X(0) + ' ' + (T + ih) + ' Z', fill: 'url(#ga)' }));
    svg.appendChild(s('path', { d: d, fill: 'none', stroke: COL.pri, 'stroke-width': 3, 'stroke-linecap': 'round' }));
    pts.forEach(function (p, k) { if (vals[k] > 0) { var c = s('circle', { cx: p[0], cy: p[1], r: 4, fill: '#fff', stroke: COL.pri, 'stroke-width': 2.5 }); var tt = s('title'); tt.textContent = days[k].split('-').reverse().join('/') + ' : ' + vals[k] + ' inscrit(s)'; c.appendChild(tt); svg.appendChild(c); } });
    [0, 7, 14, 21, 29].forEach(function (k) { var t = s('text', { x: X(k), y: H - 6, 'text-anchor': k === 0 ? 'start' : k === 29 ? 'end' : 'middle' }); t.textContent = days[k].slice(5).split('-').reverse().join('/'); svg.appendChild(t); });
    return svg;
  }
  function donut(parts, centerTop, centerSub) {
    var tot = parts.reduce(function (a, p) { return a + p.n; }, 0), R = 52, C = 2 * Math.PI * R, off = 0;
    var svg = s('svg', { viewBox: '0 0 140 140', role: 'img', 'aria-label': centerSub });
    svg.appendChild(s('circle', { cx: 70, cy: 70, r: R, fill: 'none', stroke: 'var(--soft)', 'stroke-width': 18 }));
    if (tot) parts.forEach(function (p) { if (!p.n) return; var len = (p.n / tot) * C; svg.appendChild(s('circle', { cx: 70, cy: 70, r: R, fill: 'none', stroke: p.c, 'stroke-width': 18, 'stroke-dasharray': len + ' ' + (C - len), 'stroke-dashoffset': -off, transform: 'rotate(-90 70 70)' })); off += len; });
    var t1 = s('text', { x: 70, y: 70, 'text-anchor': 'middle', style: 'font:800 24px Plus Jakarta Sans,system-ui,sans-serif;fill:var(--ink)' }); t1.textContent = centerTop; svg.appendChild(t1);
    var t2 = s('text', { x: 70, y: 87, 'text-anchor': 'middle', style: 'font:600 10px Plus Jakarta Sans,system-ui,sans-serif;fill:var(--mut)' }); t2.textContent = centerSub; svg.appendChild(t2);
    return h('div', { class: 'donutwrap' }, svg, h('ul', { class: 'legend' }, parts.map(function (p) { return h('li', null, h('i', { style: 'background:' + p.c }), p.l, h('b', { text: p.n })); })));
  }
  function bars(rows, empty) {
    var mx = Math.max.apply(null, rows.map(function (r) { return r.n; }).concat([1]));
    if (!rows.length) return h('p', { class: 'empty', text: empty || 'Pas encore de données.' });
    return h('ul', { class: 'bars' }, rows.map(function (r) { return h('li', null, h('span', { text: r.l }), h('b', { text: r.n }), h('div', { class: 't' }, h('u', { style: 'width:' + Math.max(4, Math.round((r.n / mx) * 100)) + '%' }))); }));
  }
  function funnel(steps) {
    var mx = Math.max.apply(null, steps.map(function (x) { return x.n; }).concat([1]));
    return h('div', { class: 'funnel' }, steps.map(function (x) { return h('div', null, h('span', { text: x.l }), h('div', { class: 'bar' }, h('u', { style: 'width:' + Math.max(8, Math.round((x.n / mx) * 100)) + '%;background:' + x.c, text: num(x.n) })), h('b', { text: x.p == null ? '' : x.p + ' %' })); }));
  }
  function card(title, sub, body) { return h('div', { class: 'card' }, h('h3', { text: title }), sub ? h('p', { class: 'sub', text: sub }) : null, body); }

  /* ----- tableau de bord ----- */
  function dashboard(S) {
    var c = S.comptes, d = S.demandes, a = S.abonnements, p = S.plaintes, cv = S.conversion;
    var st = {}; d.statut.forEach(function (x) { st[x.statut] = x.n; });
    var out = h('div');
    out.appendChild(h('div', { class: 'grid g4' },
      hero('c3', 'euro', eur(a.mrr), 'Revenu mensuel (HT)', a.nouveaux30 ? '+' + a.nouveaux30 + ' ce mois' : null),
      hero('c1', 'users', num(c.total), 'Inscrits', c.j7 ? '+' + c.j7 + ' / 7 j' : null),
      hero('c2', 'file', num(d.total), 'Demandes de site', d.j7 ? '+' + d.j7 + ' / 7 j' : null),
      hero('c4', 'repeat', num(a.actifs), 'Abonnements actifs', a.resilies30 ? '-' + a.resilies30 + ' résilié(s)' : null, true)));
    out.appendChild(h('div', { class: 'sec', text: 'Croissance' }));
    out.appendChild(h('div', { class: 'grid g2' },
      card('Inscriptions', '30 derniers jours · ' + c.j30 + ' nouveau(x)', area(c.jours)),
      card('Tunnel de conversion', 'De l’inscription à l’abonnement', funnel([{ l: 'Inscrits', n: c.total, c: COL.pri, p: 100 }, { l: 'Ont fait une demande', n: Math.round(c.total * cv.inscritDemande / 100), c: COL.sky, p: cv.inscritDemande }, { l: 'Abonnés', n: a.actifs + a.resiliesTotal, c: COL.ok, p: cv.demandeAbonne }]))));
    out.appendChild(h('div', { class: 'sec', text: 'Revenus et abonnements' }));
    out.appendChild(h('div', { class: 'grid g3' },
      card('Chiffre d’affaires', 'Hors taxes', mini([['Revenu annuel prévu', eur(a.arr)], ['Panier moyen', eur(a.panier)], ['Taux de résiliation', a.churn + ' %'], ['Mails pro en plus', num(a.mailsSup)]])),
      card('Formules', 'Abonnements actifs', donut([{ l: 'Essentiel', n: a.parFormule.essentiel || 0, c: COL.pri }, { l: 'Pro', n: a.parFormule.pro || 0, c: COL.sky }], String(a.actifs), 'abonnés')),
      card('Mouvements', '30 derniers jours', mini([['Nouveaux', a.nouveaux30], ['Récurrents (+30 j)', a.recurrents], ['Résiliés (30 j)', a.resilies30], ['Résiliés au total', a.resiliesTotal], ['Impayés', a.impayes], ['Suspendus', a.suspendus]]))));
    out.appendChild(h('div', { class: 'sec', text: 'Sites en cours' }));
    out.appendChild(h('div', { class: 'grid g3' },
      card('Avancement des sites', d.total + ' demande(s)', donut([{ l: 'À traiter', n: st.nouvelle || 0, c: COL.warn }, { l: 'En création', n: st.en_creation || 0, c: COL.pri }, { l: 'Aperçu envoyé', n: st.apercu || 0, c: COL.sky }, { l: 'En ligne', n: st.en_ligne || 0, c: COL.ok }, { l: 'Abandonnées', n: st.abandonnee || 0, c: COL.gray }], String(d.total), 'demandes')),
      card('Activité des demandeurs', 'Par type de commerce', bars(d.activite.map(function (x) { return { l: x.activite || '—', n: x.n }; }))),
      card('Villes', 'D’où viennent les demandes', bars(d.ville.map(function (x) { return { l: x.ville, n: x.n }; })))));
    out.appendChild(h('div', { class: 'sec', text: 'Clients et service' }));
    out.appendChild(h('div', { class: 'grid g3' },
      card('Plaintes', p.total + ' au total · délai moyen ' + (p.delai_h == null ? '—' : p.delai_h + ' h'), donut([{ l: 'Ouvertes', n: p.ouvertes, c: COL.bad }, { l: 'En cours', n: p.en_cours, c: COL.warn }, { l: 'Résolues', n: p.resolues, c: COL.ok }], String(p.total), 'plaintes')),
      card('Motifs de résiliation', null, bars(a.motifs.map(function (x) { return { l: x.motif, n: x.n }; }), 'Aucune résiliation.')),
      card('Provenance des demandes', null, bars(d.sources.map(function (x) { return { l: x.s, n: x.n }; })))));
    out.appendChild(h('div', { class: 'grid g2', style: 'margin-top:16px' },
      card('Activité des visiteurs', 'Inscrits', mini([['Dernières 24 h', c.j1], ['7 jours', c.j7], ['30 jours', c.j30], ['Connectés (7 j)', c.actifs7], ['Session ouverte', c.connectes], ['Sans demande', c.sansDemande]])),
      card('Événements (30 jours)', 'Journal du site', bars(S.divers.evenements30.map(function (x) { return { l: x.type.replace(/_/g, ' '), n: x.n }; }), 'Aucun événement.'))));
    return out;
  }

  /* ----- clients ----- */
  function initials(n) { return (n || '?').trim().split(/\s+/).slice(0, 2).map(function (x) { return x[0]; }).join('').toUpperCase(); }
  function sel(opts, val) { var e = h('select'); opts.forEach(function (o) { var op = h('option', { value: o, text: lab(o) }); if (o === val) op.selected = true; e.appendChild(op); }); return e; }
  function clients() {
    main.textContent = '';
    main.appendChild(head('Clients', 'Tous les comptes inscrits'));
    var box = h('input', { class: 'find', type: 'search', placeholder: 'Rechercher un nom ou un e-mail…', 'aria-label': 'Rechercher' }), body = h('div', { class: 'tablewrap' });
    main.appendChild(h('div', { class: 'card' }, box, body));
    function load() {
      api('/api/admin/comptes?q=' + encodeURIComponent(box.value)).then(function (r) {
        body.textContent = '';
        if (!r.j.ok) { body.appendChild(h('p', { class: 'empty', text: 'Erreur de chargement.' })); return; }
        if (!r.j.comptes.length) { body.appendChild(h('p', { class: 'empty', text: 'Aucun client pour le moment.' })); return; }
        var tb = h('tbody');
        r.j.comptes.forEach(function (c) {
          tb.appendChild(h('tr', null,
            h('td', null, h('div', { class: 'who' }, h('div', { class: 'av', text: initials(c.nom) }), h('div', null, h('b', { text: c.nom }), h('small', { text: c.email })))),
            h('td', { text: dt(c.created_at) }), h('td', { text: dt(c.derniere_connexion) }),
            h('td', null, c.demandes ? pillFor(c.statut_site) : h('span', { class: 'pill', text: 'Aucune demande' })),
            h('td', null, c.formule ? h('span', null, h('span', { class: 'pill pri', text: lab(c.formule) }), ' ', pillFor(c.abo)) : h('span', { class: 'pill', text: 'Aucun' })),
            h('td', null, c.plaintes_ouvertes ? h('span', { class: 'pill bad', text: c.plaintes_ouvertes + ' ouverte(s)' }) : '—'),
            h('td', { class: 'acts' }, h('button', { type: 'button', class: 'btn ghost sm', text: 'Ouvrir', onclick: function () { detail(c.id); } }), h('button', { type: 'button', class: 'btn sm', text: 'Voir en tant que', onclick: function () { impersonate(c.id); } }))));
        });
        body.appendChild(h('table', null, h('thead', null, h('tr', null, ['Client', 'Inscrit', 'Dernière connexion', 'Site', 'Abonnement', 'Plaintes', ''].map(function (x) { return h('th', { text: x }); }))), tb));
      });
    }
    var tm; box.addEventListener('input', function () { clearTimeout(tm); tm = setTimeout(load, 250); }); load();
  }
  function impersonate(id) {
    api('/api/admin/impersonate', 'POST', { compte_id: id }).then(function (r) {
      if (r.s === 200 && r.j.ok) { try { document.cookie = 'sv_imp=1; Path=/; Max-Age=7200; Secure; SameSite=Lax'; } catch (_) {} location.href = '/commander'; }
      else flash('Connexion au compte impossible.', true);
    });
  }
  function detail(id) {
    api('/api/admin/compte?id=' + id).then(function (r) {
      if (!r.j.ok) { flash('Compte introuvable.', true); return; }
      var c = r.j.compte, ab = r.j.abonnement;
      main.textContent = '';
      main.appendChild(head(c.nom, c.email + ' · inscrit le ' + dt(c.created_at), [h('button', { type: 'button', class: 'btn ghost', text: '← Clients', onclick: clients }), h('button', { type: 'button', class: 'btn', text: 'Voir en tant que ce client', onclick: function () { impersonate(c.id); } })]));
      var g = h('div', { class: 'grid g2' });
      var dc = h('div', { class: 'card' }, h('h2', { text: 'Demandes de site (' + r.j.demandes.length + ')' }));
      if (!r.j.demandes.length) dc.appendChild(h('p', { class: 'empty', text: 'Aucune demande.' }));
      r.j.demandes.forEach(function (d) {
        var sl = sel(['nouvelle', 'en_creation', 'apercu', 'en_ligne', 'abandonnee'], d.statut);
        sl.addEventListener('change', function () { api('/api/admin/demande', 'POST', { id: d.id, statut: sl.value }).then(function (x) { flash(x.j.ok ? 'Statut du site mis à jour.' : 'Échec de la mise à jour.', !x.j.ok); }); });
        dc.appendChild(h('div', { class: 'row' }, h('div', null, h('b', { text: d.commerce }), h('div', { class: 'sub', text: [d.ref, lab(d.formule), d.activite, d.ville, d.domaine && ('domaine : ' + d.domaine), d.mails ? d.mails + ' mail(s) pro' : '', d.tel, dt(d.created_at)].filter(Boolean).join(' · ') }), d.message ? h('div', { class: 'sub', text: d.message }) : null), sl));
      });
      g.appendChild(dc);
      var fo = sel(['essentiel', 'pro'], ab ? ab.formule : 'essentiel'), stt = sel(['actif', 'impaye', 'suspendu', 'resilie'], ab ? ab.statut : 'actif');
      var ml = h('input', { type: 'number', min: '0', max: '50', value: ab ? ab.mails_sup : 0 }), mo = h('input', { type: 'text', maxlength: '200', placeholder: 'Motif (si résiliation)', value: ab ? ab.motif || '' : '' });
      g.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Abonnement' }), h('p', { class: 'sub', text: ab ? 'Début : ' + dOnly(ab.debut) + (ab.fin ? ' · fin : ' + dOnly(ab.fin) : '') : 'Aucun abonnement. Créez-le quand le client a accepté et payé.' }),
        h('div', { class: 'form' }, h('label', null, 'Formule', fo), h('label', null, 'Statut', stt), h('label', null, 'Mails pro en plus', ml), h('label', { class: 'wide' }, 'Motif', mo)),
        h('button', { type: 'button', class: 'btn', text: ab ? 'Enregistrer' : 'Créer l’abonnement', onclick: function () { api('/api/admin/abonnement', 'POST', { compte_id: c.id, formule: fo.value, statut: stt.value, mails_sup: ml.value, motif: mo.value }).then(function (x) { flash(x.j.ok ? 'Abonnement enregistré.' : 'Échec de l’enregistrement.', !x.j.ok); if (x.j.ok) detail(c.id); }); } })));
      main.appendChild(g);
      var g2 = h('div', { class: 'grid g2', style: 'margin-top:16px' });
      var pc = h('div', { class: 'card' }, h('h2', { text: 'Plaintes (' + r.j.plaintes.length + ')' }));
      r.j.plaintes.forEach(function (p) {
        var sl = sel(['ouverte', 'en_cours', 'resolue'], p.statut);
        sl.addEventListener('change', function () { api('/api/admin/plainte-statut', 'POST', { id: p.id, statut: sl.value }).then(function (x) { flash(x.j.ok ? 'Plainte mise à jour.' : 'Échec.', !x.j.ok); }); });
        pc.appendChild(h('div', { class: 'row' }, h('div', null, h('b', { text: p.sujet }), h('div', { class: 'sub', text: dt(p.created_at) + (p.resolved_at ? ' · résolue le ' + dt(p.resolved_at) : '') }), p.message ? h('div', { class: 'sub', text: p.message }) : null), sl));
      });
      var sj = h('input', { type: 'text', maxlength: '120', placeholder: 'Sujet' }), ms = h('textarea', { rows: '2', maxlength: '1500', placeholder: 'Détails (facultatif)' });
      pc.appendChild(h('div', { class: 'form' }, h('label', { class: 'wide' }, 'Nouvelle plainte', sj), h('label', { class: 'wide' }, 'Détails', ms)));
      pc.appendChild(h('button', { type: 'button', class: 'btn ghost', text: 'Ajouter la plainte', onclick: function () { if (!sj.value.trim()) { flash('Indiquez un sujet.', true); return; } api('/api/admin/plainte', 'POST', { compte_id: c.id, sujet: sj.value, message: ms.value }).then(function (x) { flash(x.j.ok ? 'Plainte ajoutée.' : 'Échec.', !x.j.ok); if (x.j.ok) detail(c.id); }); } }));
      g2.appendChild(pc);
      g2.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Journal' }), r.j.journal.length ? h('ul', { class: 'log' }, r.j.journal.map(function (j) { return h('li', null, h('time', { text: dt(j.created_at) }), h('b', { text: j.type.replace(/_/g, ' ') }), h('span', { text: j.detail || '' }), j.admin_id ? h('span', { class: 'pill', text: 'admin' }) : null); })) : h('p', { class: 'empty', text: 'Rien pour le moment.' })));
      main.appendChild(g2);
    });
  }
  function motDePasse() {
    main.textContent = '';
    main.appendChild(head('Mot de passe', 'Changez votre mot de passe administrateur'));
    var a = h('input', { type: 'password', autocomplete: 'current-password' }), n = h('input', { type: 'password', autocomplete: 'new-password' }), n2 = h('input', { type: 'password', autocomplete: 'new-password' });
    main.appendChild(h('div', { class: 'card', style: 'max-width:520px' }, h('div', { class: 'form' }, h('label', { class: 'wide' }, 'Mot de passe actuel', a), h('label', { class: 'wide' }, 'Nouveau mot de passe (8 caractères minimum)', n), h('label', { class: 'wide' }, 'Confirmez le nouveau mot de passe', n2)),
      h('button', { type: 'button', class: 'btn', text: 'Changer le mot de passe', onclick: function () {
        if (n.value.length < 8) { flash('Au moins 8 caractères.', true); return; }
        if (n.value !== n2.value) { flash('Les deux mots de passe ne sont pas identiques.', true); return; }
        api('/api/mot-de-passe', 'POST', { actuel: a.value, nouveau: n.value }).then(function (r) { if (r.j.ok) { flash('Mot de passe changé.'); a.value = n.value = n2.value = ''; } else flash(r.s === 401 ? 'Le mot de passe actuel est incorrect.' : 'Impossible de changer le mot de passe.', true); });
      } })));
  }
  function head(title, sub, extra) { return h('div', { class: 'top' }, h('div', { class: 'hello' }, h('h1', { text: title }), sub ? h('p', { text: sub }) : null), h('div', { class: 'tools' }, extra || [])); }

  var nav = { stats: $('#n-stats'), clients: $('#n-clients'), mdp: $('#n-mdp') };
  function cur(k) { Object.keys(nav).forEach(function (x) { if (x === k) nav[x].setAttribute('aria-current', 'page'); else nav[x].removeAttribute('aria-current'); }); }
  function showStats() {
    cur('stats'); main.textContent = '';
    var hr = new Date().getHours(), greet = hr < 18 ? 'Bonjour' : 'Bonsoir';
    main.appendChild(head(greet + ', Admin', new Date().toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }) + ' · voici votre espace et toutes vos statistiques.', [h('button', { type: 'button', class: 'btn ghost', text: 'Actualiser', onclick: showStats })]));
    var box = h('div', null, h('p', { class: 'empty', text: 'Chargement des statistiques…' })); main.appendChild(box);
    api('/api/admin/stats').then(function (r) { box.textContent = ''; if (r.j.ok) box.appendChild(dashboard(r.j)); else box.appendChild(h('p', { class: 'empty', text: 'Impossible de charger les statistiques.' })); });
  }
  nav.stats.addEventListener('click', showStats);
  nav.clients.addEventListener('click', function () { cur('clients'); clients(); });
  nav.mdp.addEventListener('click', function () { cur('mdp'); motDePasse(); });
  $('#n-out').addEventListener('click', function () { api('/api/deconnexion', 'POST').then(function () { location.href = '/connexion'; }); });

  api('/api/moi').then(function (r) {
    var gate = $('#gate');
    if (r.s === 401) { gate.textContent = ''; gate.appendChild(h('h1', { text: 'Espace administrateur' })); gate.appendChild(h('p', { text: 'Connectez-vous avec votre compte administrateur.' })); gate.appendChild(h('a', { class: 'btn', href: '/connexion', text: 'Se connecter' })); return; }
    if (!r.j.admin) { gate.textContent = ''; gate.appendChild(h('h1', { text: 'Accès refusé' })); gate.appendChild(h('p', { text: 'Cet espace est réservé à l’administrateur.' })); gate.appendChild(h('a', { class: 'btn', href: '/', text: 'Retour au site' })); return; }
    gate.hidden = true; $('#app').hidden = false; showStats();
  }).catch(function () { $('#gate').textContent = 'Connexion impossible pour le moment.'; });
})();
