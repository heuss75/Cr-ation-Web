/* Espace client : tableau de bord du commerçant. Le texte venant de la base passe toujours par textContent. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var NS = 'http://www.w3.org/2000/svg';
  function h(tag, attrs) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'class') e.className = attrs[k]; else if (k === 'text') e.textContent = attrs[k];
      else if (k.slice(0, 2) === 'on') e.addEventListener(k.slice(2), attrs[k]); else if (attrs[k] !== null && attrs[k] !== undefined && attrs[k] !== false) e.setAttribute(k, attrs[k]);
    });
    (function add(list) { for (var i = 0; i < list.length; i++) { var c = list[i]; if (c === null || c === undefined || c === false) continue; if (Array.isArray(c)) add(c); else e.appendChild(typeof c === 'string' || typeof c === 'number' ? document.createTextNode(String(c)) : c); } })(Array.prototype.slice.call(arguments, 2));
    return e;
  }
  function api(path, method, body) {
    return fetch(path, { method: method || 'GET', credentials: 'same-origin', headers: body ? { 'content-type': 'application/json' } : {}, body: body ? JSON.stringify(body) : undefined })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { s: r.status, j: j }; }); });
  }
  var IC = { globe: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18', card: 'M2 7a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2zM2 10h20', pen: 'M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z', msg: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z', home: 'M3 11l9-8 9 8v9a2 2 0 0 1-2 2h-4v-7H9v7H5a2 2 0 0 1-2-2z', help: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3M12 17h.01', user: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8', out: 'M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9', ext: 'M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3', cal: 'M3 5h18v16H3zM3 10h18M8 3v4M16 3v4', edit: 'M4 20h4L19 9l-4-4L4 16zM13.5 6.5l4 4', bell: 'M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 0 1-3.4 0', file: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M8 13h8M8 17h5', book: 'M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2zM22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z', bolt: 'M13 2L3 14h9l-1 8 10-12h-9z', chart: 'M4 20V10M10 20V4M16 20v-7M22 20H2', layers: 'M12 2l10 5-10 5L2 7zM2 17l10 5 10-5M2 12l10 5 10-5', eye: 'M2 12s4-8 10-8 10 8 10 8-4 8-10 8S2 12 2 12zM12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6', mail: 'M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zM22 6l-10 7L2 6', clock: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18M12 7v5l3 2', headset: 'M3 14v-2a9 9 0 0 1 18 0v2M3 14a2 2 0 0 1 2-2h1v6H5a2 2 0 0 1-2-2zM21 14a2 2 0 0 0-2-2h-1v6h1a2 2 0 0 0 2-2z', check: 'M5 12l5 5L20 7', down: 'M6 9l6 6 6-6', right: 'M5 12h14M13 6l6 6-6 6' };
  function ico(n, size) { var s = document.createElementNS(NS, 'svg'); s.setAttribute('width', size || 22); s.setAttribute('height', size || 22); s.setAttribute('viewBox', '0 0 24 24'); s.setAttribute('fill', 'none'); s.setAttribute('stroke', 'currentColor'); s.setAttribute('stroke-width', 2); s.setAttribute('stroke-linecap', 'round'); s.setAttribute('stroke-linejoin', 'round'); s.setAttribute('aria-hidden', 'true'); var p = document.createElementNS(NS, 'path'); p.setAttribute('d', IC[n]); s.appendChild(p); return s; }
  var LBL = { nouvelle: 'Demande reçue', en_creation: 'En création', apercu: 'Aperçu à valider', en_ligne: 'En ligne', abandonnee: 'Abandonnée', hesite: 'En pause', a_rappeler: 'En pause', plus_tard: 'En pause', sans_reponse: 'En pause', refusee: 'Clôturée', trop_cher: 'Clôturée', concurrent: 'Clôturée', actif: 'Actif', impaye: 'Impayé', suspendu: 'Suspendu', resilie: 'Résilié', ouverte: 'Reçue', en_cours: 'En cours', resolue: 'Traitée', essentiel: 'Essentiel', pro: 'Pro', demandee: 'Demandée', faite: 'Faite' };
  var PRIX = { essentiel: 60, pro: 100 }, MAILP = 4, ACT = { coiffeur: 'Coiffeur', restaurant: 'Restaurant', artisan: 'Artisan du bâtiment', therapeute: 'Thérapeute, bien-être', coach: 'Coach sportif', boutique: 'Boutique de quartier', autre: 'Autre' };
  var lab = function (k) { return LBL[k] || k || '—'; };
  var nf = function (n) { return (Math.round((n || 0) * 100) / 100).toLocaleString('fr-FR'); };
  var eur = function (n) { return nf(n) + ' € HT'; };
  var eurT = function (n) { return nf(n) + ' € HT · ' + nf(n * 1.2) + ' € TTC'; };
  function dt(x) { if (!x) return '—'; var d = new Date(String(x).replace(' ', 'T') + 'Z'); return isNaN(d) ? x : d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }); }
  function dOnly(x) { if (!x) return '—'; var d = new Date(x + 'T12:00:00Z'); return isNaN(d) ? x : d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }); }
  function pill(k, c) { var m = { en_ligne: 'ok', actif: 'ok', faite: 'ok', resolue: 'ok', apercu: 'warn', en_creation: 'pri', nouvelle: 'pri', demandee: 'warn', ouverte: 'warn', en_cours: 'pri', impaye: 'bad', resilie: 'bad', suspendu: 'bad', abandonnee: '' }; return h('span', { class: 'pill ' + (c || m[k] || ''), text: lab(k) }); }
  var main = $('#main'), toast = $('#toast'), E = null, cur = 'accueil';
  function flash(t, bad) { toast.textContent = t; toast.className = 'toast on' + (bad ? ' bad' : ''); clearTimeout(flash.t); flash.t = setTimeout(function () { toast.className = 'toast'; }, 3800); }
  function initials(n) { return (n || '?').split(/\s+/).slice(0, 2).map(function (x) { return x.charAt(0).toUpperCase(); }).join(''); }
  function who() { return null; }
  function head(t, sub, extra) { return h('div', { class: 'top' }, h('div', { class: 'hello' }, h('h1', { text: t }), sub ? h('p', { text: sub }) : null), h('div', { class: 'tools' }, (extra || []))); }
  var D = function () { return E.demandes[0] || null; };
  function aMail() { var ab = E.abonnement; return E.formule === 'pro' || !!(ab && ab.mails_sup > 0) || E.demandes.some(function (d) { return d.mails > 0; }); }
  function mailCard() { return h('div', { class: 'card', style: 'margin-top:16px' }, h('h3', { text: 'Installer ma messagerie' }), h('p', { class: 'sub', text: 'Votre adresse mail pro sur iPhone, Android, Thunderbird ou Outlook, pas à pas. Comptez cinq minutes.' }), h('a', { class: 'btn', href: '/guide-messagerie', target: '_blank', rel: 'noopener', text: 'Ouvrir le guide' })); }
  var nonLues = function () { return E.notifications.filter(function (n) { return !n.lu; }).length; };
  var enLigne = function () { var d = D(); return !!d && (d.statut === 'en_ligne' || d.statut === 'apercu') && !d.suspendu; };
  var addMonths = function (iso, n) { var d = new Date(iso + 'T12:00:00Z'); d.setUTCMonth(d.getUTCMonth() + n); return d.toISOString().slice(0, 10); };
  function hero(c, icon, v, l, sub, go) { var n = h('div', { class: 'card hero click', role: 'button', tabindex: '0' }, h('div', { class: 'ic ' + c }, ico(icon)), h('div', null, h('b', { text: v }), h('span', { text: l }), sub ? h('em', { text: sub }) : null)); n.classList.add('click'); n.addEventListener('click', go); n.addEventListener('keydown', function (e) { if (e.key === 'Enter') go(); }); return n; }

  /* ===== vues ===== */
  function kp(icon, titre, big, sub, tint, go2, ext) { var n = h('div', { class: 'card kp' + (tint ? ' tint' : '') + (go2 ? ' click' : '') }, h('div', { class: 'kic' }, ico(icon, 26)), h('div', null, h('span', { text: titre }), h('b', null, big, ext ? ico('ext', 18) : null), h('small', { text: sub || '' }))); if (go2) { n.setAttribute('role', 'button'); n.setAttribute('tabindex', '0'); n.addEventListener('click', go2); n.addEventListener('keydown', function (e) { if (e.key === 'Enter') go2(); }); } return n; }
  function preview(d) {
    var box = h('div', { class: 'sprev' });
    if (d.site_url && d.site_url.charAt(0) === '/' && enLigne()) {
      var f = h('iframe', { src: d.site_url, title: 'Aperçu de mon site', loading: 'lazy', tabindex: '-1' }); box.appendChild(f);
      var fit = function () { var w = box.clientWidth; if (w) f.style.transform = 'scale(' + (w / 1280) + ')'; };
      setTimeout(fit, 0); window.addEventListener('resize', fit);
    } else box.appendChild(h('div', { class: 'sph' }, ico('globe', 34), h('b', { text: d.commerce }), h('small', { text: enLigne() ? 'Votre site' : 'Aperçu bientôt disponible' })));
    return box;
  }
  function checks(list) { return h('ul', { class: 'checks' }, list.map(function (t) { return h('li', null, ico('check', 16), t); })); }
  /* ===== statistiques de fréquentation du site (visites réelles, comptées sans cookie) ===== */
  function statsCard() {
    var vals = [['eye', 'Visites, 7 derniers jours', 'visites_7'], ['eye', 'Visites, 30 derniers jours', 'visites_30'], ['user', 'Visiteurs différents, 30 jours', 'visiteurs_30']];
    var cells = vals.map(function (t) { var b = h('b', { text: '—' }); return { b: b, k: t[2], el: h('div', null, ico(t[0], 20), b, h('small', { text: t[1] })) }; });
    var note = h('p', { class: 'sub', style: 'margin:10px 0 0', text: 'Chargement…' }), spark = h('div', { class: 'spark', 'aria-hidden': 'true' });
    var card = h('div', { class: 'card', id: 'stats-site' }, h('h3', { class: 'ctit' }, ico('chart', 22), 'Statistiques de mon site'), h('div', { class: 'sts' }, cells.map(function (c) { return c.el; })), spark, note);
    api('/api/espace/stats').then(function (r) {
      var j = r.j || {};
      if (r.s !== 200 || !j.ok) { note.textContent = 'Statistiques indisponibles pour le moment.'; return; }
      if (!j.actif) { note.textContent = j.raison === 'aucun-site' ? 'Les statistiques apparaîtront après la création de votre site.' : 'Les visites sont comptées à partir de la mise en ligne de votre site.'; return; }
      cells.forEach(function (c) { c.b.textContent = String(j[c.k] || 0); });
      var byDay = {}; (j.jours || []).forEach(function (x) { byDay[x.jour] = x.n; });
      var t = (P && P.aujourdhui) || new Date().toISOString().slice(0, 10), days = [], mx = 1, k;
      for (k = 29; k >= 0; k--) { var dd = addDays(t, -k); days.push([dd, byDay[dd] || 0]); mx = Math.max(mx, byDay[dd] || 0); }
      days.forEach(function (d) { spark.appendChild(h('i', { title: fdate(d[0]) + ' : ' + d[1] + ' visite' + (d[1] > 1 ? 's' : ''), style: 'height:' + Math.max(4, Math.round(d[1] / mx * 100)) + '%' })); });
      note.textContent = j.total ? 'Depuis la mise en ligne : ' + j.total + ' visite' + (j.total > 1 ? 's' : '') + ', environ ' + j.moyenne_jour + ' par jour sur le dernier mois. Les visites de robots et de personnes qui refusent le suivi ne sont pas comptées.' : 'Pas encore de visite enregistrée. Les premières apparaîtront ici dès que quelqu’un ouvrira votre site.';
    }).catch(function () { note.textContent = 'Statistiques indisponibles pour le moment.'; });
    return card;
  }

  function vAccueil() {
    var d = D(), prenom = (E.compte.nom || '').split(/\s+/)[0], out = h('div'), idx = { nouvelle: 0, en_creation: 1, apercu: 2, en_ligne: 3 }[d && d.statut];
    main.appendChild(head('Bonjour ' + prenom + ' 👋', 'Bienvenue dans votre espace Devanture Web.', []));
    if (d && d.suspendu) out.appendChild(h('div', { class: 'warnbox', role: 'alert' }, h('div', null, h('b', { text: 'Votre site est temporairement suspendu.' }), h('div', { text: 'Les modifications sont désactivées. Écrivez-nous depuis l’onglet Aide pour qu’on regarde ensemble.' }))));
    var tf = aFaire(); if (tf) out.appendChild(tf);
    if (!d) {
      out.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Votre site vitrine' }), h('p', { class: 'sub', text: 'Vous n’avez pas encore fait de demande. Cela prend 3 minutes, sans engagement et sans paiement.' }), h('a', { class: 'btn', href: '/commander', text: 'Faire ma demande' })));
      main.appendChild(out); return;
    }
    var q = E.quota, u = E.utilisees, ab = E.abonnement, pro = E.formule === 'pro', live = enLigne();
    out.appendChild(h('div', { class: 'kpis' },
      kp('layers', 'Mon site', lab(d.statut), d.domaine || d.ville, d.statut === 'en_ligne', function () { go('site'); }, d.statut === 'en_ligne'),
      kp('layers', 'Mon offre', lab(E.formule), eurT(PRIX[E.formule] + MAILP * (ab ? ab.mails_sup : 0)) + ' / mois', false, function () { go('abo'); }),
      kp('pen', 'Modifications', Math.max(q - u, 0) + ' / ' + q, 'restantes ce mois-ci', false, function () { go('modifs'); }),
      kp('file', 'Mon dossier', P && P.requis ? P.requis.filter(function (r) { return r.ok; }).length + ' / ' + P.requis.length : '—', 'éléments obligatoires remplis', false, function () { go('dossier'); })));
    var dEnLigne = (E.notifications.filter(function (n) { return /en ligne/i.test(n.titre); })[0] || {}).created_at;
    var site = h('div', { class: 'card sitec' }, preview(d), h('div', { class: 'sinfo' },
      h('div', { class: 'stop' }, h('h2', { text: d.commerce }), h('span', { class: 'dots', 'aria-hidden': 'true', text: '···' })),
      d.domaine ? h('a', { class: 'dom', href: d.site_url || '#', target: '_blank', rel: 'noopener' }, d.domaine, ico('ext', 14)) : h('span', { class: 'dom', text: d.ville }),
      h('div', { class: 'stat ' + (d.statut === 'en_ligne' ? 'ok' : '') }, ico('check', 16), lab(d.suspendu ? 'suspendu' : d.statut)),
      dEnLigne && d.statut === 'en_ligne' ? h('p', { class: 'mise', }, ico('cal', 18), 'Mis en ligne le ' + new Date(dEnLigne.replace(' ', 'T') + 'Z').toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' })) : null,
      h('div', { class: 'sbtn' }, d.site_url && live ? h('a', { class: 'btn', href: d.site_url, target: '_blank', rel: 'noopener' }, 'Voir mon site ', ico('ext', 16)) : null, h('button', { type: 'button', class: 'btn ghost', onclick: function () { go(pro ? 'editeur' : 'modifs'); } }, ico('edit', 16), ' Modifier mon site'))));
    var steps = ['Demande reçue', 'En création', 'Aperçu validé', 'En ligne'];
    var avanc = h('div', { class: 'card' }, h('h3', { class: 'ctit' }, ico('layers', 22), 'Avancement de mes demandes'), idx != null ? h('ol', { class: 'steps2' }, steps.map(function (t, i) { var done = i < idx || idx === 3; return h('li', { class: done ? 'done' : i === idx ? 'now' : '' }, h('b', { text: t }), h('small', { text: i === 0 ? dt(d.created_at).split(' ').slice(0, 3).join(' ') : done ? 'Terminé' : i === idx ? 'En cours' : 'À venir' })); })) : null);
    var tiles = h('div', { class: 'card' }, h('h3', { class: 'ctit' }, ico('bolt', 22), 'Accès rapides'), h('div', { class: 'tiles' }, [['pen', 'Demander une modification', 'modifs'], ['mail', 'Envoyer un message', 'support'], ['book', 'Consulter les guides', 'aide']].map(function (t) { return h('button', { type: 'button', class: 'tile', onclick: function () { go(t[2]); } }, ico(t[0], 24), h('span', { text: t[1] })); })));
    var stats = statsCard();
    var inc = ['Site vitrine complet', 'Modifications (' + q + ' / mois)'].concat(pro ? ['Outil de réservation', 'Éditeur en libre-service'] : []).concat(aMail() ? ['Adresse e-mail pro'] : []).concat(pro ? ['Support prioritaire'] : []);
    var abo = h('div', { class: 'card' }, h('h3', { class: 'ctit' }, ico('card', 22), 'Mon abonnement'), h('div', { class: 'aboh' }, h('div', null, h('b', { class: 'plan', text: lab(E.formule) }), h('small', { text: eurT(PRIX[E.formule] + MAILP * (ab ? ab.mails_sup : 0)) + ' / mois' })), ab ? pill(ab.statut) : pill('nouvelle')), checks(inc), h('button', { type: 'button', class: 'btn ghost wide', onclick: function () { go('abo'); } }, 'Gérer mon abonnement ', ico('right', 16)));
    var acts = [].concat(E.notifications.slice(0, 3).map(function (n) { return [n.titre, n.message, n.created_at]; }));
    if (acts.length < 3) acts.push(['Nouvelle demande', 'Création de votre site.', d.created_at]);
    var act = h('div', { class: 'card' }, h('h3', { class: 'ctit' }, ico('clock', 22), 'Dernières activités'), h('ul', { class: 'tl' }, acts.slice(0, 3).map(function (a, i) { return h('li', { class: i === 0 ? 'first' : '' }, h('div', { class: 'tr' }, h('b', { text: a[0] }), h('small', { text: dt(a[2]).split(' ').slice(0, 3).join(' ') })), h('p', { text: a[1] })); })), h('button', { type: 'button', class: 'btn ghost wide', onclick: function () { go('messages'); } }, 'Voir toutes les activités ', ico('right', 16)));
    out.appendChild(h('div', { class: 'dgrid' }, h('div', { class: 'dleft' }, site, avanc, h('div', { class: 'two' }, tiles, stats)), h('div', { class: 'dright' }, abo, act)));
    main.appendChild(out);
  }
  function resaUrls() {
    var d = D(), u = d && d.site_url; if (!u || !enLigne()) return null;
    if (u === '/exemples/bistro') return { client: u + '-reservation-client', interne: u + '-reservation-interne' };
    if (u.indexOf('/exemples/') === 0) return null;
    var base = u.replace(/\/+$/, ''); return { client: base + '/reservation', interne: base + '/reservation/gestion' };
  }
  function vResa() {
    main.appendChild(head('Réservations', 'Sur votre site, pas ici'));
    if (E.formule !== 'pro') { main.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Passer à la formule Pro' }), h('p', { class: 'sub', text: '100 € HT (120 € TTC) par mois' }), checks(['Outil de réservation en ligne et agenda, sur votre site', 'Statistiques de réservations', '3 modifications par mois', '1 adresse mail pro incluse']), h('button', { type: 'button', class: 'btn', text: 'En parler avec nous', onclick: function () { go('aide'); } }))); return; }
    var U = resaUrls();
    main.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Votre outil de réservation est sur votre site' }),
      h('p', { class: 'sub', text: 'Vos clients réservent directement sur votre site. Vous gérez votre planning et vos statistiques (nombre de réservations et de personnes, matin, midi, soir, par jour ou par période) depuis votre site, sur une page protégée. Elles ne sont pas dans cet espace.' }),
      U ? h('div', { class: 'tools', style: 'flex-wrap:wrap;margin-top:12px' }, h('a', { class: 'btn', href: U.interne, target: '_blank', rel: 'noopener' }, 'Ouvrir mon planning et mes statistiques ', ico('ext', 16)), h('a', { class: 'btn ghost', href: U.client, target: '_blank', rel: 'noopener' }, 'Voir la page de réservation de mes clients ', ico('ext', 16)))
        : h('p', { class: 'empty', text: 'Les liens apparaîtront ici dès que votre site sera en ligne.' })));
  }
  function msgNode(n) { return h('div', { class: 'msg' + (n.lu ? '' : ' nl') }, h('b', { text: n.titre }), h('p', { text: n.message }), h('small', { text: dt(n.created_at) })); }
  function vSite() {
    var d = D(); main.appendChild(head('Mon site', 'Les informations de votre site vitrine'));
    if (!d) { main.appendChild(h('div', { class: 'card' }, h('p', { class: 'empty', text: 'Aucun site pour le moment.' }), h('a', { class: 'btn', href: '/commander', text: 'Faire ma demande' }))); return; }
    var dl = h('dl', { class: 'dl' }, [['Commerce', d.commerce], ['Statut', lab(d.statut)], ['Activité', ACT[d.activite] || d.activite], ['Ville', d.ville], ['Nom de domaine', d.domaine || 'À définir'], ['Référence', d.ref], ['Demande du', dt(d.created_at)], ['Adresses mail pro', String(d.mails || 0)]].map(function (x) { return h('div', null, h('dt', { text: x[0] }), h('dd', { text: x[1] || '—' })); }));
    main.appendChild(h('div', { class: 'card' }, h('div', { class: 'tbar' }, h('h2', { text: d.commerce }), pill(d.suspendu ? 'suspendu' : d.statut)), dl));
    if (d.site_url && enLigne()) {
      var rel = d.site_url.charAt(0) === '/';
      main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('div', { class: 'tbar' }, h('h2', { text: 'Aperçu' }), h('a', { class: 'btn', href: d.site_url, target: '_blank', rel: 'noopener' }, 'Ouvrir mon site ', ico('ext', 16))),
        rel ? h('div', { class: 'browser' }, h('div', { class: 'bar' }, h('i'), h('i'), h('i'), h('span', { text: d.domaine || d.site_url })), h('iframe', { src: d.site_url, title: 'Aperçu de mon site', loading: 'lazy' })) : h('p', { class: 'sub', text: 'Cliquez sur « Ouvrir mon site » pour le voir en grand.' })));
    } else main.appendChild(h('div', { class: 'infobox', style: 'margin-top:16px', text: d.suspendu ? 'Votre site est suspendu pour le moment.' : 'Votre site apparaîtra ici dès que l’aperçu sera prêt. Nous vous prévenons dans l’onglet Messages.' }));
  }
  function vModifs() {
    var q = E.quota, u = E.utilisees, left = Math.max(q - u, 0), d = D(), can = !E.lecture && enLigne() && left > 0 && !(E.abonnement && ['impaye', 'suspendu', 'resilie'].indexOf(E.abonnement.statut) >= 0);
    main.appendChild(head('Mes modifications', q + ' modification' + (q > 1 ? 's' : '') + ' par mois avec la formule ' + lab(E.formule), []));
    var ty = h('select', null, [['texte', 'Remplacer un texte'], ['photo', 'Remplacer une photo'], ['bloc', 'Ajouter ou supprimer un bloc'], ['autre', 'Autre']].map(function (o) { return h('option', { value: o[0], text: o[1] }); })), ds = h('textarea', { maxlength: '1200', placeholder: 'Décrivez précisément ce que vous voulez changer et où.' });
    var ab = E.abonnement, aboKo = ab && ['impaye', 'suspendu', 'resilie'].indexOf(ab.statut) >= 0;
    var why = E.lecture ? 'Lecture seule : vous consultez ce compte en tant qu’administrateur.' : aboKo ? 'Votre abonnement est ' + lab(ab.statut).toLowerCase() + ' : les nouvelles modifications sont suspendues. Écrivez-nous depuis « Contacter le support » pour régulariser.' : !d ? 'Faites d’abord votre demande de site.' : d.suspendu ? 'Votre site est suspendu.' : !enLigne() ? 'Disponible dès que votre aperçu est prêt.' : left < 1 ? (q > 1 ? 'Vous avez utilisé vos ' + q + ' modifications de ce mois-ci. Elles reviennent le 1er du mois prochain.' : 'Vous avez utilisé votre modification de ce mois-ci. Elle revient le 1er du mois prochain.') : '';
    main.appendChild(h('div', { class: 'card' }, h('h2', { text: left + ' restante' + (left > 1 ? 's' : '') + ' ce mois-ci' }), h('div', { class: 'quota' }, h('u', { style: 'width:' + Math.min(100, Math.round((u / q) * 100)) + '%' })), h('p', { class: 'sub', text: u + ' utilisée' + (u > 1 ? 's' : '') + ' sur ' + q + ' · une modification non utilisée ne se cumule pas.' }),
      why ? h('div', { class: 'infobox', text: why }) : null,
      h('div', { class: 'form' }, h('label', null, 'Type de modification', ty), h('label', { class: 'wide' }, 'Votre demande', ds)),
      h('button', { type: 'button', class: 'btn', text: 'Envoyer ma modification', disabled: can ? null : 'disabled', onclick: function () {
        api('/api/espace/modif', 'POST', { type: ty.value, description: ds.value }).then(function (r) { if (r.j.ok) { flash('Modification envoyée.'); reload('modifs'); } else flash(r.j.error === 'vide' ? 'Décrivez votre demande (5 caractères minimum).' : r.j.error === 'quota' ? 'Quota du mois atteint.' : r.j.error === 'abonnement' ? 'Votre abonnement doit être régularisé avant de demander une modification.' : r.j.error === 'aucune-demande' ? 'Faites d’abord votre demande de site.' : r.j.error === 'suspendu' ? 'Votre site est suspendu.' : 'Envoi impossible pour le moment.', true); });
      } })));
    main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h3', { text: 'Historique' }), E.modifs.length ? h('ul', { class: 'list' }, E.modifs.map(function (m) { return h('li', null, h('div', { class: 'tbar', style: 'margin:0' }, h('b', { text: lab(m.type) === m.type ? ({ texte: 'Texte', photo: 'Photo', bloc: 'Bloc', autre: 'Autre' }[m.type] || m.type) : m.type }), pill(m.statut)), h('div', { class: 'sub', style: 'margin:4px 0 0', text: m.description }), h('small', { text: dt(m.created_at) })); })) : h('p', { class: 'empty', text: 'Aucune modification pour le moment.' })));
  }
  function vAbo() {
    var a = E.abonnement; main.appendChild(head('Mon abonnement', 'Formule, prix et engagement'));
    if (!a) { main.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Formule ' + lab(E.formule) }), h('p', { class: 'sub', text: 'Votre abonnement démarre à la mise en ligne de votre site. Aucun paiement n’a été demandé à ce stade.' }), h('p', { text: eurT(PRIX[E.formule]) + ' par mois, engagement de 12 mois.' }))); var rc0 = resilCard(); if (rc0) main.appendChild(rc0); return; }
    var tot = PRIX[a.formule] + MAILP * (a.mails_sup || 0), fin = a.debut ? addMonths(a.debut, 12) : null;
    main.appendChild(h('div', { class: 'card' }, h('div', { class: 'tbar' }, h('h2', { text: 'Formule ' + lab(a.formule) }), pill(a.statut)),
      h('dl', { class: 'dl' }, [['Total par mois', eurT(tot)], ['Formule', eurT(PRIX[a.formule])], ['Mails pro en plus', (a.mails_sup || 0) + ' × ' + eurT(MAILP)], ['Début', dOnly(a.debut)], ['Fin de l’engagement de 12 mois', fin ? dOnly(fin) : '—']].map(function (x) { return h('div', null, h('dt', { text: x[0] }), h('dd', { text: x[1] })); }))));
    var inc = ['Site vitrine sur mesure', 'Nom de domaine et hébergement', 'Espace client', E.formule === 'pro' ? '3 modifications par mois réalisées par nous' : '1 modification par mois réalisée par nous', 'Guide pub'].concat(aMail() ? ['Guide d’installation de la messagerie'] : []).concat(a.formule === 'pro' ? ['Éditeur en libre-service : textes, prix, horaires, photos', 'Outil de réservation en ligne', 'Agenda', '1 adresse mail pro incluse'] : []);
    main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h3', { text: 'Ce qui est inclus' }), h('ul', { class: 'list' }, inc.map(function (t) { return h('li', { text: '✓ ' + t }); })), h('p', { class: 'sub', style: 'margin-top:12px', text: 'Pour ajouter une adresse mail, écrivez-nous depuis l’onglet Aide.' })));
    var fc = formuleCard(); if (fc) main.appendChild(fc);
    var rc = resilCard(); if (rc) main.appendChild(rc);
  }
  function vMessages() {
    if (nonLues()) { if (!E.lecture) api('/api/espace/lu', 'POST', {}); setTimeout(function () { E.notifications.forEach(function (n) { n.lu = 1; }); drawNav(); document.querySelectorAll('.bellb i').forEach(function (e) { e.remove(); }); }, 0); }
    main.appendChild(head('Messages', 'Les nouvelles concernant votre site', nonLues() && !E.lecture ? [h('button', { type: 'button', class: 'btn ghost', text: 'Tout marquer comme lu', onclick: function () { api('/api/espace/lu', 'POST', {}).then(function () { reload('messages'); }); } })] : []));
    main.appendChild(h('div', { class: 'card' }, E.notifications.length ? E.notifications.map(msgNode) : h('p', { class: 'empty', text: 'Aucun message pour le moment.' })));
  }
  function vSupport() {
    main.appendChild(head('Contacter le support', 'Une question, un souci ? Écrivez-nous, nous vous répondons rapidement'));
    var sj = h('input', { type: 'text', maxlength: '120', placeholder: 'Ex. : changer de formule, un souci sur mon site…' }), ms = h('textarea', { maxlength: '1500', placeholder: 'Expliquez-nous en quelques lignes.' });
    main.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Nous écrire' }), h('div', { class: 'form' }, h('label', { class: 'wide' }, 'Sujet', sj), h('label', { class: 'wide' }, 'Message', ms)),
      h('button', { type: 'button', class: 'btn', text: 'Envoyer', disabled: E.lecture ? 'disabled' : null, onclick: function () { if (!sj.value.trim()) { flash('Indiquez un sujet.', true); return; } api('/api/espace/plainte', 'POST', { sujet: sj.value, message: ms.value }).then(function (r) { if (r.j.ok) { flash('Message envoyé. Nous revenons vers vous rapidement.'); reload('support'); } else flash('Envoi impossible.', true); }); } }),
      h('p', { class: 'sub', style: 'margin-top:10px' }, 'Pensez aussi à la ', h('a', { href: '/faq', target: '_blank', rel: 'noopener', text: 'FAQ' }), '.')));
    main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h3', { text: 'Mes messages envoyés' }), E.plaintes.length ? h('ul', { class: 'list' }, E.plaintes.map(function (p) { return h('li', null, h('div', { class: 'tbar', style: 'margin:0' }, h('b', { text: p.sujet }), pill(p.statut)), h('small', { text: dt(p.created_at) })); })) : h('p', { class: 'empty', text: 'Rien pour le moment.' })));
  }
  function vCompte() {
    main.appendChild(head('Mon compte', E.compte.email));
    main.appendChild(h('div', { class: 'card', style: 'margin-bottom:16px' }, h('dl', { class: 'dl' }, [['Nom', E.compte.nom], ['E-mail', E.compte.email], ['Compte créé le', dt(E.compte.created_at)]].map(function (x) { return h('div', null, h('dt', { text: x[0] }), h('dd', { text: x[1] })); }))));
    var a = h('input', { type: 'password', autocomplete: 'current-password' }), n = h('input', { type: 'password', autocomplete: 'new-password' }), n2 = h('input', { type: 'password', autocomplete: 'new-password' });
    var oo = h('input', { type: 'checkbox', disabled: E.lecture ? 'disabled' : null }); oo.checked = !!E.compte.opt_out;
    oo.addEventListener('change', function () { api('/api/espace/opt-out', 'POST', { opt_out: oo.checked }).then(function (r) { if (r.j.ok) { E.compte.opt_out = oo.checked ? 1 : 0; flash(oo.checked ? 'Vous ne recevrez plus nos e-mails de communication.' : 'E-mails de communication réactivés.'); } else { oo.checked = !oo.checked; flash('Enregistrement impossible.', true); } }); });
    main.appendChild(h('div', { class: 'card', style: 'max-width:560px;margin-bottom:16px' }, h('h2', { text: 'E-mails' }), h('label', { class: 'chk' }, oo, document.createTextNode(' Ne plus recevoir les e-mails de communication de Devanture Web (nouveautés, conseils). Les messages liés à votre compte restent envoyés.'))));
    main.appendChild(h('div', { class: 'card', style: 'max-width:560px' }, h('h2', { text: 'Changer de mot de passe' }), h('div', { class: 'form' }, h('label', { class: 'wide' }, 'Mot de passe actuel', a), h('label', { class: 'wide' }, 'Nouveau mot de passe (8 caractères minimum)', n), h('label', { class: 'wide' }, 'Confirmez le nouveau mot de passe', n2)),
      h('button', { type: 'button', class: 'btn', text: 'Changer le mot de passe', disabled: E.lecture ? 'disabled' : null, onclick: function () {
        if (n.value.length < 8) { flash('Au moins 8 caractères.', true); return; }
        if (n.value !== n2.value) { flash('Les deux mots de passe ne sont pas identiques.', true); return; }
        api('/api/mot-de-passe', 'POST', { actuel: a.value, nouveau: n.value }).then(function (r) { if (r.j.ok) { flash('Mot de passe changé.'); a.value = n.value = n2.value = ''; } else flash(r.s === 401 ? 'Le mot de passe actuel est incorrect.' : 'Impossible de changer le mot de passe.', true); });
      } })));
  }


  /* ===== éditeur en libre-service (formule Pro) ===== */
  function reduire(file) {
    return new Promise(function (ok, ko) {
      var img = new Image(), u = URL.createObjectURL(file);
      img.onload = function () {
        var m = Math.max(img.width, img.height), tries = [[1600, 0.82], [1400, 0.72], [1100, 0.64], [900, 0.55]], i = 0;
        (function essai() {
          var k = Math.min(1, tries[i][0] / m), c = document.createElement('canvas'); c.width = Math.round(img.width * k); c.height = Math.round(img.height * k);
          var g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height); g.drawImage(img, 0, 0, c.width, c.height);
          var d = c.toDataURL('image/jpeg', tries[i][1]), b = d.split(',')[1];
          if (b.length * 0.75 > 1100000 && ++i < tries.length) return essai();
          URL.revokeObjectURL(u); if (b.length * 0.75 > 1150000) ko(new Error('taille')); else ok(b);
        })();
      };
      img.onerror = function () { URL.revokeObjectURL(u); ko(new Error('format')); };
      img.src = u;
    });
  }
  var TAGS = { h1: 'Titre', h2: 'Titre de section', h3: 'Sous-titre', h4: 'Sous-titre', p: 'Paragraphe', a: 'Bouton ou lien', small: 'Précision', b: 'Prix ou valeur', li: 'Élément de liste' };
  function vEditeur() {
    main.appendChild(head('Modifier mon site', 'Changez vos textes, prix, horaires et photos : le résultat apparaît tout de suite sur votre site.', []));
    var box = h('div'); main.appendChild(box); box.appendChild(h('div', { class: 'card' }, h('p', { class: 'empty', text: 'Chargement de l’éditeur…' })));
    api('/api/espace/editeur').then(function (r) {
      box.textContent = '';
      if (!r.j.ok) { box.appendChild(h('div', { class: 'card' }, h('p', { class: 'empty', text: r.j.error === 'pro' ? 'L’éditeur est réservé à la formule Pro.' : 'L’éditeur sera disponible dès que votre site sera en ligne.' }))); return; }
      var C = r.j.champs, off = r.j.lecture || !!r.j.suspendu || !!r.j.abo_bloque, frame = h('iframe', { src: r.j.site_url, title: 'Aperçu de mon site', loading: 'lazy' }), cnt = h('span', { class: 'pill', text: '' }), refT;
      var maj = function () { cnt.textContent = C.filter(function (c) { return c.val !== null; }).length + ' modifié(s)'; };
      var refresh = function () { clearTimeout(refT); refT = setTimeout(function () { frame.src = r.j.site_url + '?v=' + Date.now(); }, 350); };
      function save(c, valeur, st, rst, node) {
        var p = valeur === null ? api('/api/espace/contenu', 'POST', { k: c.k, reset: true }) : api('/api/espace/contenu', 'POST', { k: c.k, valeur: valeur });
        st.textContent = 'Enregistrement…';
        return p.then(function (x) {
          if (!x.j.ok) { st.textContent = ''; flash(x.j.error === 'texte' ? 'Le texte doit faire entre 1 et 600 caractères.' : x.j.error === 'suspendu' ? 'Votre site est suspendu.' : x.j.error === 'abonnement' ? 'Votre abonnement doit être régularisé.' : x.j.error === 'lecture-seule' ? 'Lecture seule.' : 'Enregistrement impossible.', true); return false; }
          c.val = valeur; st.textContent = 'Enregistré ✓'; setTimeout(function () { st.textContent = ''; }, 2200); rst.hidden = valeur === null; maj(); refresh(); return true;
        });
      }
      function champ(c) {
        var cur = c.val !== null ? c.val : c.v, st = h('small', { class: 'sub' }), rst = h('button', { type: 'button', class: 'lnk', text: 'Rétablir l’original', hidden: c.val === null ? '' : null });
        var w = h('div', { class: 'fld' });
        if (c.type === 'img') {
          var im = h('img', { src: cur, alt: '', onerror: function () { im.style.visibility = 'hidden'; } }), fi = h('input', { type: 'file', accept: 'image/jpeg,image/png,image/webp', hidden: '', 'aria-label': 'Choisir une photo' });
          fi.addEventListener('change', function () {
            var f = fi.files[0]; if (!f) return; st.textContent = 'Envoi de la photo…';
            reduire(f).then(function (b64) { return api('/api/espace/media', 'POST', { mime: 'image/jpeg', data: b64 }); }).then(function (m) {
              if (!m.j.ok) { st.textContent = ''; flash(m.j.error === 'limite' ? 'Limite de photos atteinte.' : 'Photo refusée.', true); return; }
              return save(c, m.j.url, st, rst).then(function (ok) { if (ok) { im.src = m.j.url; im.style.visibility = ''; } });
            }).catch(function () { st.textContent = ''; flash('Cette image ne peut pas être utilisée (JPEG, PNG ou WebP).', true); });
            fi.value = '';
          });
          w.appendChild(h('div', { class: 'imgrow' }, h('div', { class: 'thumb' }, im), h('div', null, h('b', { text: 'Photo' }), h('div', null, h('button', { type: 'button', class: 'btn ghost sm', text: 'Changer la photo', disabled: off ? 'disabled' : null, onclick: function () { fi.click(); } }), fi), st, rst)));
          rst.addEventListener('click', function () { save(c, null, st, rst).then(function (ok) { if (ok) im.src = c.v; }); });
        } else {
          var long = c.v.length > 70, inp = h(long ? 'textarea' : 'input', { maxlength: '600', 'aria-label': TAGS[c.label] || 'Texte', disabled: off ? 'disabled' : null });
          if (long) inp.rows = Math.min(5, Math.ceil(c.v.length / 70)); else inp.type = 'text';
          inp.value = cur;
          inp.addEventListener('change', function () { var v = inp.value.trim(); if (!v) { inp.value = c.val !== null ? c.val : c.v; flash('Le texte ne peut pas être vide.', true); return; } if (v === (c.val !== null ? c.val : c.v)) return; save(c, v === c.v ? null : v, st, rst); });
          rst.addEventListener('click', function () { save(c, null, st, rst).then(function (ok) { if (ok) inp.value = c.v; }); });
          w.appendChild(h('label', null, h('span', { text: TAGS[c.label] || 'Texte' }), inp)); w.appendChild(h('div', { class: 'fst' }, st, rst));
        }
        c.node = w; return w;
      }
      var secs = [], seen = {};
      C.forEach(function (c) { if (!seen[c.sec]) { seen[c.sec] = { n: c.sec, c: [] }; secs.push(seen[c.sec]); } seen[c.sec].c.push(c); });
      var q = h('input', { class: 'find', type: 'search', placeholder: 'Chercher un texte ou une section…', 'aria-label': 'Chercher' }), list = h('div');
      var dets = secs.map(function (s, i) { var d = h('details', { class: 'sec2' }, h('summary', null, s.n, h('span', { class: 'pill', text: String(s.c.length) })), s.c.map(champ)); if (i === 0) d.open = true; s.d = d; return d; });
      dets.forEach(function (d) { list.appendChild(d); });
      q.addEventListener('input', function () { var t = q.value.trim().toLowerCase(); secs.forEach(function (s) { var any = false; s.c.forEach(function (c) { var m = !t || (c.v + ' ' + (c.val || '') + ' ' + s.n).toLowerCase().indexOf(t) >= 0; c.node.hidden = !m; if (m) any = true; }); s.d.hidden = !any; if (t && any) s.d.open = true; }); });
      maj();
      if (r.j.abo_bloque) box.appendChild(h('div', { class: 'warnbox' }, 'Votre abonnement est ' + lab(r.j.abo_bloque).toLowerCase() + ' : l’éditeur est désactivé tant qu’il n’est pas régularisé.'));
      if (r.j.suspendu) box.appendChild(h('div', { class: 'warnbox' }, 'Votre site est suspendu : les modifications sont désactivées.'));
      if (r.j.lecture) box.appendChild(h('div', { class: 'infobox', text: 'Lecture seule : vous consultez cet éditeur en tant qu’administrateur.' }));
      box.appendChild(h('div', { class: 'infobox', text: 'Modifiez votre site autant de fois que vous le souhaitez, sans limite. Vous avez en plus droit à ' + E.quota + ' modifications par mois réalisées par notre équipe, si vous préférez ne pas le faire vous-même (rubrique « Demandes à l’équipe »).' }));
      box.appendChild(h('div', { class: 'editor' },
        h('div', { class: 'edcol card' }, h('div', { class: 'tbar' }, h('h2', { text: 'Contenu du site' }), cnt), q, list),
        h('div', { class: 'edprev card' }, h('div', { class: 'tbar' }, h('h3', { text: 'Votre site' }), h('a', { class: 'btn ghost sm', href: r.j.site_url, target: '_blank', rel: 'noopener', text: 'Ouvrir' })), h('div', { class: 'browser' }, h('div', { class: 'bar' }, h('i'), h('i'), h('i'), h('span', { text: 'Aperçu en direct' })), frame))));
    }).catch(function () { box.textContent = ''; box.appendChild(h('div', { class: 'card' }, h('p', { class: 'empty', text: 'Chargement impossible.' }))); });
  }

  /* ===== aide & guides : guide publicité et visibilité ===== */
  var SV = function (inner, vb, label) { return '<svg viewBox="' + vb + '" role="img" aria-label="' + label + '" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,sans-serif">' + inner + '</svg>'; };
  var GP_SVG = {
    google: SV(
      '<rect x="1" y="1" width="558" height="218" rx="14" fill="var(--card)" stroke="var(--line)"/>' +
      '<rect x="16" y="14" width="528" height="28" rx="14" fill="var(--soft)"/><circle cx="34" cy="28" r="6" fill="none" stroke="var(--mut)" stroke-width="2"/><path d="M39 33l5 5" stroke="var(--mut)" stroke-width="2"/><text x="54" y="33" font-size="13" fill="var(--ink)">coiffeur lyon 3</text>' +
      '<rect x="16" y="54" width="190" height="150" rx="10" fill="var(--soft)"/><path d="M16 120l70-30 60 24 60-28M60 54v150M130 54v150" stroke="var(--line)" stroke-width="6" fill="none"/>' +
      '<g fill="#17C26E" stroke="#fff" stroke-width="2"><circle cx="78" cy="100" r="9"/><circle cx="140" cy="136" r="9"/><circle cx="102" cy="168" r="9"/></g><g font-size="10" font-weight="700" fill="#fff" text-anchor="middle"><text x="78" y="103.5">1</text><text x="140" y="139.5">2</text><text x="102" y="171.5">3</text></g>' +
      '<g><rect x="222" y="54" width="322" height="46" rx="10" fill="var(--card)" stroke="#17C26E" stroke-width="2"/><text x="236" y="73" font-size="13" font-weight="700" fill="var(--ink)">Salon Léa · Coiffeur</text><text x="236" y="91" font-size="11" fill="var(--mut)">4,8 ★★★★★ (86 avis) · Ouvert jusqu’à 19 h</text><rect x="470" y="63" width="62" height="18" rx="9" fill="#17C26E"/><text x="501" y="76" font-size="10" font-weight="700" fill="#fff" text-anchor="middle">VOUS</text></g>' +
      '<g><rect x="222" y="108" width="322" height="46" rx="10" fill="var(--card)" stroke="var(--line)"/><text x="236" y="127" font-size="13" font-weight="700" fill="var(--ink)">Coiffure Martin</text><text x="236" y="145" font-size="11" fill="var(--mut)">4,5 ★★★★☆ (31 avis) · Ouvert</text></g>' +
      '<g><rect x="222" y="162" width="322" height="42" rx="10" fill="var(--card)" stroke="var(--line)"/><text x="236" y="180" font-size="13" font-weight="700" fill="var(--ink)">Atelier Coupe &amp; Couleur</text><text x="236" y="196" font-size="11" fill="var(--mut)">4,2 ★★★★☆ (12 avis)</text></g>',
      '0 0 560 220', 'Résultats Google : la carte avec trois fiches puis la liste, votre commerce en première position'),
    snippet: SV(
      '<rect x="1" y="1" width="558" height="168" rx="14" fill="var(--card)" stroke="var(--line)"/>' +
      '<circle cx="30" cy="32" r="10" fill="var(--soft)"/><text x="48" y="30" font-size="11" fill="var(--ink)">Salon Léa</text><text x="48" y="44" font-size="10" fill="var(--mut)">https://salon-lea.fr</text>' +
      '<text x="20" y="74" font-size="17" font-weight="700" fill="#17C26E">Coiffeur à Lyon 3e · Salon Léa · Réservation en ligne</text>' +
      '<text x="20" y="98" font-size="12.5" fill="var(--mut)">Coupe, couleur, balayage et soins à Lyon 3e. Réservez votre créneau en ligne</text><text x="20" y="116" font-size="12.5" fill="var(--mut)">en 1 minute. Ouvert du mardi au samedi, 12 rue des Fleurs.</text>' +
      '<path d="M20 128h430" stroke="#17C26E" stroke-width="2"/><path d="M20 124v8M450 124v8" stroke="#17C26E" stroke-width="2"/><text x="20" y="148" font-size="11" font-weight="700" fill="var(--ink)">Titre : métier + ville + nom, environ 55 caractères</text>' +
      '<rect x="468" y="60" width="78" height="62" rx="8" fill="none" stroke="var(--line)" stroke-dasharray="4 4"/><text x="507" y="88" font-size="10" fill="var(--mut)" text-anchor="middle">Description</text><text x="507" y="102" font-size="10" fill="var(--mut)" text-anchor="middle">~150 car.</text>',
      '0 0 560 170', 'Aperçu d’un résultat Google : titre, adresse du site et description'),
    avis: SV(
      '<rect x="1" y="1" width="558" height="150" rx="14" fill="var(--card)" stroke="var(--line)"/>' +
      '<text x="28" y="62" font-size="42" font-weight="800" fill="var(--ink)">4,8</text><text x="28" y="86" font-size="14" fill="#17C26E">★★★★★</text><text x="28" y="106" font-size="11" fill="var(--mut)">86 avis</text>' +
      [[5, 232], [4, 40], [3, 10], [2, 4], [1, 4]].map(function (r, i) { var y = 28 + i * 22; return '<text x="150" y="' + (y + 11) + '" font-size="11" fill="var(--mut)">' + r[0] + ' ★</text><rect x="182" y="' + y + '" width="230" height="10" rx="5" fill="var(--soft)"/><rect x="182" y="' + y + '" width="' + Math.max(4, Math.round(r[1] * 230 / 232)) + '" height="10" rx="5" fill="#17C26E"/>'; }).join('') +
      '<rect x="440" y="24" width="100" height="100" rx="10" fill="#fff" stroke="var(--line)"/>' +
      (function () { var s = '', q = [1,1,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,1,1,0,1,0,1,1,0,1,1,0,1,0,1,0,1,0,0,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,0,1,0,1,1,1,0,1,1,0,0,1,0,0,1,1,1,1,0,1,1,1,1,0,1,0,1,0,0,1,1,1,0,1,1,0,1,0,1,1,1,0,1,0,1,1,0,0,1,0]; q.forEach(function (v, i) { if (v) s += '<rect x="' + (448 + (i % 10) * 8.4) + '" y="' + (32 + Math.floor(i / 10) * 8.4) + '" width="7.2" height="7.2" fill="#0B0B0C"/>'; }); return s; })() +
      '<text x="490" y="140" font-size="10" fill="var(--mut)" text-anchor="middle">Laissez-nous un avis</text>',
      '0 0 560 152', 'Note moyenne de 4,8 sur 86 avis, et un QR code pour laisser un avis'),
    semaine: SV(
      '<rect x="1" y="1" width="558" height="120" rx="14" fill="var(--card)" stroke="var(--line)"/>' +
      [['Lun', 'Photo', 1], ['Mar', 'Story', 0], ['Mer', 'Avant / après', 1], ['Jeu', 'Story', 0], ['Ven', 'Vidéo courte', 1], ['Sam', 'Story', 0], ['Dim', 'Repos', 2]].map(function (d, i) { var x = 14 + i * 77; return '<rect x="' + x + '" y="16" width="70" height="88" rx="10" fill="' + (d[2] === 1 ? '#17C26E' : 'var(--soft)') + '"/><text x="' + (x + 35) + '" y="38" font-size="12" font-weight="700" text-anchor="middle" fill="' + (d[2] === 1 ? '#fff' : 'var(--ink)') + '">' + d[0] + '</text><text x="' + (x + 35) + '" y="66" font-size="10.5" text-anchor="middle" fill="' + (d[2] === 1 ? '#fff' : 'var(--mut)') + '">' + d[1] + '</text><text x="' + (x + 35) + '" y="86" font-size="9.5" text-anchor="middle" fill="' + (d[2] === 1 ? '#fff' : 'var(--mut)') + '">' + (d[2] === 1 ? 'publication' : d[2] === 2 ? '' : '24 h') + '</text>'; }).join(''),
      '0 0 560 122', 'Rythme de publication sur une semaine : trois publications et trois stories'),
    suivi: SV(
      '<rect x="1" y="1" width="558" height="150" rx="14" fill="var(--card)" stroke="var(--line)"/>' +
      [['Vus sur Google', 520, 'Recherches et affichages de la fiche'], ['Visites du site', 330, 'Statistiques de mon site'], ['Appels, itinéraires, réservations', 170, 'Fiche Google et site'], ['Nouveaux clients', 90, 'Votre question « comment nous avez-vous connus ? »']].map(function (b, i) { var y = 16 + i * 32; return '<rect x="16" y="' + y + '" width="' + b[1] + '" height="26" rx="8" fill="#17C26E"/><text x="26" y="' + (y + 17) + '" font-size="12" font-weight="700" fill="#fff">' + b[0] + '</text>'; }).join(''),
      '0 0 560 152', 'Entonnoir : des vues sur Google aux nouveaux clients'),
  };
  var GP = [
    { id: 'google', n: 1, t: 'Comment Google classe les commerces', intro: 'Quand quelqu’un tape « coiffeur Lyon 3 », Google affiche d’abord une carte avec trois fiches, puis les sites. Pour être choisi, il faut figurer à ces deux endroits : votre fiche Google et votre site.', fig: 'google',
      pts: ['<b>Pertinence</b> : votre fiche et votre site disent clairement ce que vous faites (métier, prestations, ville).', '<b>Distance</b> : Google privilégie les commerces proches de la personne ou du quartier cherché. Vous ne la contrôlez pas, mais une adresse exacte et une zone bien indiquée aident.', '<b>Notoriété</b> : nombre et qualité des avis, présence sur d’autres sites, mentions locales. C’est la partie que vous pouvez le plus faire progresser.'],
      tip: 'Ces trois critères sont publics, mais personne ne peut garantir une place. Ce guide vous donne les actions qui comptent vraiment, dans l’ordre.' },
    { id: 'fiche', n: 2, t: 'Soignez votre fiche Google (gratuit)', intro: 'C’est l’action n° 1 : elle fait apparaître votre commerce sur Google Maps et dans la carte des résultats. Rendez-vous sur business.google.com, cherchez votre commerce, puis « Revendiquer » ou « Créer ».',
      pts: ['<b>Nom exact</b> du commerce, sans mots ajoutés. « Salon Léa » et non « Salon Léa coiffeur pas cher Lyon » : Google peut suspendre la fiche.', '<b>Catégorie principale la plus précise</b> (« Coiffeur » plutôt que « Beauté »), puis 2 à 4 catégories secondaires.', '<b>Adresse, téléphone et horaires</b> exacts, y compris jours fériés et fermetures exceptionnelles.', '<b>Adresse de votre site</b> et, avec la formule Pro, le <b>lien de réservation</b>.', '<b>Description</b> de 3 à 5 phrases : ce que vous faites, pour qui, dans quel quartier.', '<b>Prestations ou produits</b> avec les prix quand c’est possible.', '<b>Au moins 10 photos réelles</b> : façade, intérieur, équipe, réalisations. Ajoutez-en une nouvelle chaque semaine.', '<b>Validez la fiche</b> (courrier, téléphone ou vidéo selon ce que Google propose) : sans validation, elle apparaît très peu.', '<b>Publications</b> : une offre ou une nouveauté de temps en temps, comme sur un réseau social.'],
      avoid: 'Ne créez pas plusieurs fiches pour le même lieu, et ne mettez pas une adresse qui n’est pas la vôtre : c’est interdit et cela fait disparaître la fiche.' },
    { id: 'avis', n: 3, t: 'Collectez des avis, régulièrement', intro: 'Les avis pèsent beaucoup dans le classement local et dans le choix du client. Un flux régulier de nouveaux avis vaut mieux qu’une grosse vague puis plus rien.', fig: 'avis',
      pts: ['<b>Demandez au bon moment</b> : juste après le service, quand le client est content, en face à face ou par SMS.', '<b>Facilitez</b> : sur votre fiche Google, copiez le lien « Demander des avis » et transformez-le en QR code (gratuit en ligne) posé au comptoir ou sur le ticket.', '<b>Répondez à chaque avis</b> sous deux ou trois jours : remerciez, citez la prestation, restez bref.', '<b>Avis négatif</b> : répondez calmement, sans vous justifier à outrance, et proposez d’en parler par téléphone. Les futurs clients lisent votre réponse.', '<b>Exemple de demande par SMS</b> : « Merci pour votre visite ! Si vous avez 30 secondes, votre avis nous aide beaucoup : [lien] »'],
      avoid: 'N’achetez pas d’avis, n’en écrivez pas vous-même et ne les réservez pas aux clients satisfaits : Google détecte ces pratiques et peut retirer des avis, voire la fiche.' },
    { id: 'seo', n: 4, t: 'Votre site : être trouvé sur Google (SEO)', intro: 'Le référencement naturel (SEO) consiste à aider Google à comprendre votre site. Les bases techniques sont déjà faites : site rapide, adapté au mobile et sécurisé (HTTPS). Ce que vous apportez : les bons mots et de vraies photos.', fig: 'snippet',
      pts: ['<b>Les mots que les clients tapent</b> : « métier + ville » (ou quartier), par exemple « coiffeur Lyon 3e ». Utilisez-les naturellement dans le titre, le premier texte et les titres de section.', '<b>Un titre clair</b> pour votre page d’accueil : métier, ville, nom du commerce. C’est ce qui s’affiche en bleu ou en vert dans Google.', '<b>Une description</b> d’environ 150 caractères, avec une raison de venir (prestation phare, réservation en ligne, horaires).', '<b>Un texte par prestation</b>, avec quelques phrases utiles et le prix : un texte unique et précis vaut mieux qu’un long texte vague.', '<b>De vraies photos</b> de votre lieu et de vos réalisations, plutôt que des images génériques.', '<b>Infos pratiques visibles</b> : adresse, horaires, téléphone, plan d’accès.', '<b>Des liens vers votre site</b> depuis des sites sérieux : annuaires, partenaires, association de commerçants, mairie, presse locale.', '<b>Le même nom, la même adresse et le même téléphone</b> partout où vous apparaissez.'],
      tip: 'Pour modifier les textes de votre site, utilisez l’onglet Mon site. Pour un changement de titre ou de description de page, envoyez-nous une demande de modification depuis votre espace.' },
    { id: 'annuaires', n: 5, t: 'Les annuaires et plateformes utiles', intro: 'Chaque fiche cohérente renforce votre crédibilité auprès de Google et vous apporte des visiteurs en plus. Visez la qualité : quelques inscriptions bien tenues valent mieux que vingt oubliées.',
      pts: ['<b>Toujours</b> : Google Business Profile, Apple Plans (Apple Business Connect), Bing Places, Facebook, PagesJaunes.', '<b>Selon votre activité</b> : Planity ou Treatwell (coiffure, beauté), TheFork ou Tripadvisor (restauration, hôtellerie), Doctolib ou Resalib (santé), annuaires de votre fédération ou de votre métier.', '<b>Local</b> : site de la mairie, office de tourisme, CCI, association de commerçants de votre quartier.', 'Sur chacun : même nom, même adresse, même téléphone, même horaires, et le lien vers votre site.'],
      tip: 'Gardez un petit tableau (plateforme, identifiant, date de dernière mise à jour). Quand vos horaires changent, vous savez où corriger.' },
    { id: 'reseaux', n: 6, t: 'Instagram et Facebook', intro: 'Les réseaux sociaux montrent que vous êtes actif et rassurent avant la première visite. Mieux vaut peu, mais régulièrement.', fig: 'semaine',
      pts: ['<b>Un seul profil par réseau</b>, au nom du commerce, avec le même logo que sur le site.', '<b>Bio</b> : ce que vous faites, la ville, un appel à l’action et le lien vers votre site. Exemple : « Coiffeur à Lyon 3e · Sur rendez-vous · Réservez ↓ ».', '<b>Trois publications par semaine</b> : une réalisation, un avant/après, un coulisse, une nouveauté, une offre, l’avis d’un client (avec son accord).', '<b>Stories</b> : le quotidien, les horaires exceptionnels, les créneaux libres. Rapides à faire et très vues.', '<b>Vidéos courtes</b> (10 à 20 secondes) : elles sont davantage montrées aux personnes qui ne vous suivent pas encore.', '<b>3 à 5 mots-clics locaux</b> (#lyon3, #coiffeurlyon) plutôt qu’une longue liste.', '<b>Répondez</b> aux messages et commentaires dans la journée.'],
      avoid: 'Ne publiez pas de photos de clients sans leur accord, et ne copiez pas des images trouvées en ligne : elles sont protégées.' },
    { id: 'horsligne', n: 7, t: 'Le bouche-à-oreille et le hors ligne', intro: 'Beaucoup de clients vous trouvent encore par un voisin, une affiche ou un ami. Votre site sert de point de rendez-vous : donnez-lui sa place partout.',
      pts: ['<b>QR code du site</b> sur les cartes de visite, flyers, tickets, sacs, devis, factures, véhicule et vitrine.', '<b>Vitrine</b> : une affiche « Réservez en ligne » (formule Pro) ou « Retrouvez-nous sur notre site ».', '<b>Signature de mail</b> avec l’adresse du site et le lien vers votre fiche Google.', '<b>Partenaires du quartier</b> : échangez des cartes avec les commerces voisins, proposez des offres croisées.', '<b>Parrainage</b> : « Amenez un ami, vous avez tous les deux … ». Votre propre code de parrainage est dans l’onglet Parrainage.', '<b>Événements locaux</b> : marchés, journées portes ouvertes, associations de quartier.'] },
    { id: 'pub', n: 8, t: 'La publicité payante (facultatif)', intro: 'Elle ne remplace pas les étapes précédentes, mais peut accélérer. Commencez petit, mesurez, et arrêtez si cela ne rapporte rien.',
      pts: ['<b>Google Ads</b> : vous payez quand une personne clique sur votre annonce après avoir cherché votre métier. Utile pour une période précise (ouverture, soldes, saison).', '<b>Facebook et Instagram</b> : sponsorisez une publication qui marche déjà, en ciblant un rayon de 5 à 10 km autour du commerce.', '<b>Budget test</b> : quelques euros par jour pendant deux semaines, puis comparez le nombre d’appels, de réservations et de visites avec la période d’avant.', '<b>Une seule offre claire</b> par annonce, avec un seul bouton (appeler, réserver).', 'Faites une pause d’abord si vous n’avez pas encore de fiche Google complète ni d’avis : la publicité envoie alors des visiteurs vers une vitrine incomplète.'],
      avoid: 'Méfiez-vous des démarcheurs qui promettent « la première place sur Google, garantie ». Personne ne peut la garantir.' },
    { id: 'suivi', n: 9, t: 'Mesurer ce qui marche', intro: 'Un quart d’heure par semaine suffit pour garder ce qui fonctionne et arrêter le reste.', fig: 'suivi',
      pts: ['<b>Fiche Google</b> : dans l’espace de gestion, regardez les recherches, les appels, les itinéraires et les clics vers le site.', '<b>Votre site</b> : l’onglet Accueil affiche les statistiques de visites de votre site.', '<b>Au comptoir ou au téléphone</b> : demandez « Comment nous avez-vous connus ? » et notez la réponse.', '<b>Chaque mois</b> : comparez avec le mois précédent. Ne tirez pas de conclusion sur une seule semaine.'],
      tip: 'Comptez plusieurs semaines, parfois quelques mois, avant de voir un effet régulier : Google réévalue les fiches et les sites progressivement.' },
  ];
  var GP_PLAN = [
    ['Semaine 1 : la base', ['Créer ou revendiquer la fiche Google, la valider', 'Compléter catégorie, horaires, description, prestations', 'Ajouter 10 photos', 'Vérifier nom, adresse et téléphone sur le site']],
    ['Semaine 2 : les avis', ['Créer le QR code « avis » et l’afficher', 'Envoyer la demande d’avis aux 10 derniers clients satisfaits', 'Répondre à tous les avis existants']],
    ['Semaine 3 : la présence', ['S’inscrire sur Apple Plans, Bing Places, PagesJaunes', 'Mettre à jour Facebook et Instagram (bio, lien, logo)', 'Publier trois fois']],
    ['Semaine 4 : le suivi', ['Ajouter le QR code du site sur vos supports', 'Noter les premiers chiffres (appels, visites, avis)', 'Décider : que garder, que changer, que tester']],
  ];
  var GP_FAQ = [
    ['Combien de temps avant d’apparaître en haut ?', 'Cela dépend de votre métier, de votre ville et de la concurrence. Une fiche complète apparaît souvent en quelques semaines ; monter dans le classement demande des avis et de la régularité, parfois plusieurs mois. Personne ne peut promettre une position.'],
    ['Pourquoi mon concurrent est-il devant moi ?', 'Il a probablement plus d’avis récents, une fiche mieux remplie ou une adresse plus proche de la personne qui cherche. Regardez sa fiche : catégories, photos, avis, réponses. Vous verrez ce qu’il faut rattraper.'],
    ['Dois-je payer pour apparaître sur Google ?', 'Non. La fiche Google et le référencement naturel sont gratuits. La publicité est un coup de pouce facultatif.'],
    ['Mes horaires ont changé, que faire ?', 'Mettez à jour la fiche Google et les annuaires le jour même, puis votre site depuis l’onglet Mon site. Des horaires faux font perdre des clients et des avis.'],
    ['Que faire d’un faux avis ?', 'Sur votre fiche Google, signalez-le (menu de l’avis, « Signaler »). Répondez poliment : votre réponse est lue par les futurs clients.'],
    ['Faut-il écrire des articles de blog ?', 'Pas pour démarrer. Mieux vaut des pages de prestations précises, des avis et une fiche Google complète.'],
  ];
  function gpFig(k) { var d = h('div', { class: 'gp-fig' }); d.innerHTML = GP_SVG[k]; return d; }
  function vGuidePub() {
    main.appendChild(head('Guide publicité et visibilité', 'Être trouvé sur Google et choisi par les clients', [h('button', { type: 'button', class: 'btn ghost', text: '← Aide & Guides', onclick: function () { go('aide'); } })]));
    main.appendChild(h('div', { class: 'card gp-hero' },
      h('div', null, h('h2', { text: 'Les trois leviers qui comptent' }), h('p', { class: 'sub', text: 'Dans l’ordre : une fiche Google complète, des avis réguliers, un site clair qui contient les mots de vos clients. Le reste vient ensuite. Comptez un quart d’heure par semaine.' })),
      h('ol', { class: 'gp-keys' }, [['Fiche Google', 'Elle vous fait apparaître sur la carte.'], ['Avis clients', 'Ils vous font choisir.'], ['Site et mots-clés', 'Ils vous font trouver.']].map(function (k, i) { return h('li', null, h('b', { text: String(i + 1) }), h('span', null, h('strong', { text: k[0] }), h('small', { text: k[1] }))); }))));
    main.appendChild(h('div', { class: 'gp-toc', role: 'navigation', 'aria-label': 'Sommaire du guide' }, GP.map(function (s) { return h('button', { type: 'button', class: 'chip', text: s.n + '. ' + s.t.split(' (')[0].replace('Votre site : ', ''), onclick: function () { var e = document.getElementById('gp-' + s.id); if (e) e.scrollIntoView({ behavior: 'smooth', block: 'start' }); } }); }).concat([h('button', { type: 'button', class: 'chip', text: 'Plan sur 30 jours', onclick: function () { var e = document.getElementById('gp-plan'); if (e) e.scrollIntoView({ behavior: 'smooth', block: 'start' }); } })])));
    GP.forEach(function (s) {
      var body = h('div', { class: 'gp-body' });
      body.appendChild(h('p', { class: 'gp-intro', text: s.intro }));
      if (s.fig) body.appendChild(gpFig(s.fig));
      var ul = h('ul', { class: 'gp-chk' }); s.pts.forEach(function (t) { var li = h('li'); li.innerHTML = t; ul.appendChild(li); }); body.appendChild(ul);
      if (s.tip) body.appendChild(h('p', { class: 'gp-tip' }, h('b', { text: 'À retenir · ' }), s.tip));
      if (s.avoid) body.appendChild(h('p', { class: 'gp-avoid' }, h('b', { text: 'À éviter · ' }), s.avoid));
      main.appendChild(h('section', { class: 'card gp-sec', id: 'gp-' + s.id }, h('div', { class: 'gp-h' }, h('b', { class: 'gp-n', text: String(s.n) }), h('h2', { text: s.t })), body));
    });
    main.appendChild(h('section', { class: 'card gp-sec', id: 'gp-plan' }, h('div', { class: 'gp-h' }, h('b', { class: 'gp-n', text: '✓' }), h('h2', { text: 'Votre plan sur 30 jours' })),
      h('div', { class: 'gp-plan' }, GP_PLAN.map(function (p) { return h('div', { class: 'gp-wk' }, h('h3', { text: p[0] }), h('ul', { class: 'gp-chk' }, p[1].map(function (t) { return h('li', { text: t }); }))); }))));
    main.appendChild(h('section', { class: 'card gp-sec' }, h('div', { class: 'gp-h' }, h('b', { class: 'gp-n', text: '?' }), h('h2', { text: 'Questions fréquentes' })),
      GP_FAQ.map(function (q) { return h('details', { class: 'sec2' }, h('summary', null, h('b', { text: q[0] })), h('p', { class: 'sub', text: q[1] })); })));
    main.appendChild(h('p', { class: 'sub gp-foot', text: 'Ces conseils sont généraux et évoluent avec les règles des plateformes. Aucun résultat n’est garanti. Pour toute question sur votre site, écrivez-nous depuis Aide & Guides.' }));
  }
  function vAide() {
    main.appendChild(head('Aide & Guides', 'Tout pour bien démarrer, pas à pas'));
    var g = function (ic, t, d, btn, fn) { return h('div', { class: 'card gcard' }, h('div', { class: 'kic' }, ico(ic, 28)), h('div', null, h('h3', { text: t }), h('p', { class: 'sub', text: d }), btn ? h('button', { type: 'button', class: 'btn', onclick: fn }, btn, ' ', ico('right', 16)) : null)); };
    main.appendChild(h('div', { class: 'gridg' },
      g('mail', 'Guide messagerie', 'Installer votre adresse mail pro sur iPhone, Android, Thunderbird ou Outlook, avec les réglages à copier.', 'Ouvrir le guide', function () { window.open('/guide-messagerie', '_blank', 'noopener'); }),
      g('book', 'Guide publicité et visibilité', 'Fiche Google, avis, référencement, réseaux, publicité : les actions qui font venir des clients.', 'Ouvrir le guide', function () { go('guidepub'); })));
  }

  /* ===== factures ===== */
  var EMET = { nom: 'Devanture Web', l1: '[Raison sociale à compléter]', adr: '[Adresse à compléter]', siret: '[à compléter]', tva: '[FR… à compléter]', mail: 'contact@devantureweb.fr', ok: false };
  var LOGO = '<svg width="54" height="54" viewBox="0 0 64 64" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M8 20 12 8h40l4 12"/><path d="M8 20a6 6 0 0 0 12 0 6 6 0 0 0 12 0 6 6 0 0 0 12 0 6 6 0 0 0 12 0"/><path d="M12 33v23h40V33"/><path d="M26 56V42h12v14"/><path d="M41 38l11 4.5-4.6 1.8-1.8 4.7z" fill="#17C26E" stroke="#17C26E" stroke-width="1.5"/></svg>';
  var fe = function (n) { return (Math.round(n * 100) / 100).toLocaleString('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' €'; };
  var MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
  function moisLong(ym) { var m = +ym.slice(5, 7); return MOIS[m - 1] + ' ' + ym.slice(0, 4); }
  /* formule et nombre d'adresses payantes en vigueur un mois donné (YYYY-MM), selon l'historique des changements appliqués */
  function etatMois(k) {
    var ab = E.abonnement, ch = (P && P.changements || []).filter(function (c) { return c.statut === 'applique'; });
    if (!ch.length) return { formule: ab.formule, mails: ab.mails_sup || 0 };
    var f = ch[0].de, m = ch[0].mails_avant || 0;
    ch.forEach(function (c) { if (c.effet.slice(0, 7) <= k) { f = c.vers; m = c.mails_apres || 0; } });
    return { formule: f, mails: m };
  }
  function mesFactures() {
    var ab = E.abonnement, d = D(); if (!ab || !ab.debut || !d) return [];
    var nowK = new Date().toISOString().slice(0, 7), fin = ab.statut === 'resilie' && ab.fin ? String(ab.fin).slice(0, 7) : nowK, out = [], y = +ab.debut.slice(0, 4), m = +ab.debut.slice(5, 7), day = ab.debut.slice(8, 10) || '01';
    for (var n = 0; n < 36; n++) {
      var k = y + '-' + (m < 10 ? '0' : '') + m; if (k > fin || k > nowK || k + '-' + day > new Date().toISOString().slice(0, 10)) break;
      var et = etatMois(k), fm = et.formule, lignes = [fm === 'pro' ? ['Abonnement Pro', 'Site web + nom de domaine + adresse mail pro · ' + MOIS[m - 1] + ' ' + y, 1, 100] : ['Abonnement Essentiel', 'Site web + nom de domaine · ' + MOIS[m - 1] + ' ' + y, 1, 60]];
      if (et.mails > 0) lignes.push([fm === 'pro' ? 'Adresses mail pro supplémentaires' : 'Adresses mail pro', fm === 'pro' ? 'Adresses en plus de celle incluse' : 'Adresse mail à 4 € HT par mois', et.mails, 4]);
      var cu = P && P.parrainage ? P.parrainage.credits.filter(function (c) { return (c.mois_offert || (c.utilise_le || '').slice(0, 7)) === k; }).length : 0;
      if (cu) lignes.push(['Mois offert (parrainage)', 'Remise de 100 % sur l’abonnement du mois', cu, -(fm === 'pro' ? 100 : 60)]);
      var ht = lignes.reduce(function (t, l) { return t + l[2] * l[3]; }, 0), tva = Math.round(ht * 20) / 100;
      out.push({ id: k, num: 'F-' + y + (m < 10 ? '0' : '') + m + '-' + String(d.id).padStart(4, '0'), date: day + '/' + (m < 10 ? '0' : '') + m + '/' + y, periode: MOIS[m - 1].charAt(0).toUpperCase() + MOIS[m - 1].slice(1) + ' ' + y, lignes: lignes, ht: ht, tva: tva, ttc: ht + tva, statut: k === nowK && ab.statut === 'impaye' ? 'A régler' : 'Payée' });
      m++; if (m > 12) { m = 1; y++; }
    }
    return out.reverse();
  }
  var FAC = { id: null };
  function vFactures() {
    main.appendChild(head('Factures', 'Vos factures d’abonnement, à télécharger en PDF'));
    var l = mesFactures();
    if (!l.length) { main.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Vos factures' }), h('p', { class: 'sub', text: 'Votre abonnement démarre à la mise en ligne de votre site. Vos factures apparaîtront ici dès ce moment.' }), h('p', { class: 'empty', text: 'Aucune facture pour le moment.' }))); return; }
    var tb = h('tbody'); l.forEach(function (f) { var tr = h('tr', null, h('td', null, h('b', { text: f.num })), h('td', { text: f.periode }), h('td', { text: f.date }), h('td', { class: 'num', text: fe(f.ttc) }), h('td', null, pill(f.statut === 'Payée' ? 'actif' : 'impaye')), h('td', { class: 'num' }, h('button', { type: 'button', class: 'btn sm', onclick: function () { FAC.id = f.id; go('facture'); } }, 'Voir / PDF'))); tb.appendChild(tr); });
    main.appendChild(h('div', { class: 'card' }, h('div', { class: 'tablewrap' }, h('table', { class: 'revt' }, h('thead', null, h('tr', null, ['Facture', 'Période', 'Date', 'Total TTC', 'Statut', ''].map(function (x, i) { return h('th', { text: x, class: i === 3 || i === 5 ? 'num' : '' }); }))), tb))));
  }
  function vFacture() {
    var f = mesFactures().filter(function (x) { return x.id === FAC.id; })[0], d = D();
    if (!f) { main.appendChild(h('div', { class: 'card' }, h('p', { class: 'empty', text: 'Facture introuvable.' }), h('button', { type: 'button', class: 'btn', text: '← Mes factures', onclick: function () { go('factures'); } }))); return; }
    main.appendChild(head('Facture ' + f.num, f.periode, [h('button', { type: 'button', class: 'btn ghost', text: '← Mes factures', onclick: function () { go('factures'); } }), h('button', { type: 'button', class: 'btn', text: '⬇ Télécharger en PDF', onclick: function () { window.print(); } })]));
    var esc = function (t) { return String(t == null ? '' : t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
    var rows = f.lignes.map(function (l) { return '<tr><td><b>' + esc(l[0]) + '</b><small>' + esc(l[1]) + '</small></td><td class="n">' + l[2] + '</td><td class="n">' + fe(l[3]) + '</td><td class="n">20 %</td><td class="n">' + fe(l[2] * l[3]) + '</td></tr>'; }).join('');
    var html = (EMET.ok ? '' : '<div class="inv-ex">EXEMPLE DE FACTURE · informations de l’entreprise à compléter</div>') +
      '<div class="inv-top"><div class="inv-brand">' + LOGO + '<div><b>Devanture <em>Web</em></b><small>Site vitrine pour commerçants</small></div></div><div class="inv-ft"><h1>FACTURE</h1><p>N° ' + esc(f.num) + '</p><p><span class="inv-badge' + (f.statut === 'Payée' ? '' : ' warn') + '">' + (f.statut === 'Payée' ? 'Payée' : 'À régler') + '</span></p></div></div>' +
      '<div class="inv-meta"><div><span>Date d’émission</span><b>' + esc(f.date) + '</b></div><div><span>Échéance</span><b>' + esc(f.date) + '</b></div><div><span>Période</span><b>' + esc(f.periode) + '</b></div><div><span>Mode de paiement</span><b>Prélèvement SEPA</b></div></div>' +
      '<div class="inv-parties"><div><h2>Émetteur</h2><b>' + esc(EMET.nom) + '</b><p>' + esc(EMET.l1) + '</p><p>' + esc(EMET.adr) + '</p><p>SIRET : ' + esc(EMET.siret) + '</p><p>N° TVA : ' + esc(EMET.tva) + '</p><p>' + esc(EMET.mail) + '</p></div>' +
      '<div><h2>Facturé à</h2><b>' + esc(d.commerce) + '</b><p>' + esc(E.compte.nom) + '</p><p>' + esc(d.ville) + '</p><p>' + esc(E.compte.email) + '</p>' + (d.domaine ? '<p>Site : ' + esc(d.domaine) + '</p>' : '') + '</div></div>' +
      '<table class="inv-t"><thead><tr><th>Désignation</th><th class="n">Qté</th><th class="n">Prix unitaire HT</th><th class="n">TVA</th><th class="n">Total HT</th></tr></thead><tbody>' + rows + '</tbody></table>' +
      '<div class="inv-tot"><div><span>Total HT</span><b>' + fe(f.ht) + '</b></div><div><span>TVA 20 %</span><b>' + fe(f.tva) + '</b></div><div class="g"><span>Total TTC</span><span>' + fe(f.ttc) + '</span></div></div>' +
      '<div class="inv-pay"><div><h2>Paiement</h2><p>' + (f.statut === 'Payée' ? 'Réglée le ' + esc(f.date) + ' par prélèvement.' : 'À régler par prélèvement SEPA.') + '</p></div><div><h2>Engagement</h2><p>Abonnement mensuel, engagement de 12 mois. Résiliation selon les conditions générales de vente.</p></div></div>' +
      '<div class="inv-legal"><b>Pénalités de retard :</b> 3 fois le taux d’intérêt légal. <b>Indemnité forfaitaire de recouvrement :</b> 40 €. <b>Escompte :</b> aucun pour paiement anticipé. Facture établie en euros. Prestation : abonnement de création, d’hébergement et d’entretien d’un site vitrine.</div>';
    var box = h('div', { class: 'invoice' }); box.innerHTML = html; main.appendChild(box);
  }

  /* ===== parcours, dossier, résiliation, parrainage, avis ===== */
  var P = null;
  function loadP() { return api('/api/espace/parcours').then(function (r) { P = r.s === 200 && r.j.ok ? r.j : null; }).catch(function () { P = null; }); }
  function reloadP(k) { return loadP().then(function () { if (k) cur = k; draw(); }); }
  var fdate = function (iso) { return iso ? dOnly(iso) : '—'; };
  var ERR = { 'pas-apercu': 'Votre aperçu n’est pas (ou plus) à valider.', deja: 'C’est déjà fait.', 'en-cours': 'Une demande d’ajustements est déjà en cours.', vide: 'Écrivez au moins quelques mots pour que nous comprenions.', suspendu: 'Votre site est suspendu : écrivez-nous depuis Aide & Guides.', 'lecture-seule': 'Lecture seule : vous consultez ce compte en tant qu’administrateur.', incomplet: 'Il manque encore des informations obligatoires.', type: 'Format non accepté : envoyez une image PNG, JPEG ou WebP, ou un PDF.', taille: 'Ce fichier est trop lourd. Réduisez-le ou envoyez-le par e-mail.', trop: 'Vous avez atteint le nombre maximum de fichiers : supprimez-en un d’abord.', fichier: 'Ce fichier n’a pas pu être lu.', consentement: 'Cochez la case pour autoriser la publication.', note: 'Choisissez une note de 1 à 5 étoiles.', confirmation: 'Cochez la case de confirmation.', resilie: 'Votre abonnement est déjà résilié.', inconnu: 'Ce code n’existe pas. Vérifiez-le : il commence par DW-.', soi: 'Vous ne pouvez pas utiliser votre propre code.', client: 'Les codes sont réservés aux nouveaux clients.', inactif: 'Ce code n’est pas utilisable pour le moment (le parrain n’a pas d’abonnement actif).', publie: 'Votre avis est déjà publié.' };
  var errTxt = function (j, s) { return (j && ERR[j.error]) || (s === 429 ? 'Trop de tentatives, réessayez dans un instant.' : 'Une erreur est survenue. Réessayez dans un instant.'); };

  function modal(titre, body, onclose) {
    var prev = document.activeElement, ov = h('div', { class: 'mdl', role: 'presentation' });
    var box = h('div', { class: 'mdl-box', role: 'dialog', 'aria-modal': 'true', 'aria-label': titre, tabindex: '-1' });
    var close = function () { document.removeEventListener('keydown', key); ov.remove(); if (prev && prev.focus) prev.focus(); if (onclose) onclose(); };
    var key = function (e) { if (e.key === 'Escape') close(); };
    box.appendChild(h('button', { type: 'button', class: 'mdl-x', 'aria-label': 'Fermer', text: '×', onclick: close }));
    box.appendChild(body); ov.appendChild(box);
    ov.addEventListener('mousedown', function (e) { if (e.target === ov) close(); });
    document.addEventListener('keydown', key); document.body.appendChild(ov); box.focus();
    return close;
  }
  function stars(init, onchange) {
    var v = init || 0, wrap = h('div', { class: 'stars', role: 'radiogroup', 'aria-label': 'Votre note sur 5' }), bs = [];
    var paint = function () { bs.forEach(function (b, i) { b.className = i < v ? 'on' : ''; b.setAttribute('aria-checked', String(i + 1 === v)); b.tabIndex = (v ? i + 1 === v : i === 0) ? 0 : -1; }); };
    for (var i = 1; i <= 5; i++) (function (n) {
      var b = h('button', { type: 'button', role: 'radio', 'aria-label': n + ' étoile' + (n > 1 ? 's' : ''), text: '★', onclick: function () { v = n; paint(); onchange(n); },
        onkeydown: function (e) { if (e.key === 'ArrowRight' || e.key === 'ArrowUp') { e.preventDefault(); v = Math.min(5, (v || 0) + 1); paint(); onchange(v); bs[v - 1].focus(); } else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') { e.preventDefault(); v = Math.max(1, (v || 2) - 1); paint(); onchange(v); bs[v - 1].focus(); } } });
      bs.push(b); wrap.appendChild(b);
    })(i);
    paint(); return wrap;
  }
  function avisForm(done) {
    var note = (P && P.avis && P.avis.note) || 0, st = stars(note, function (n) { note = n; });
    var com = h('textarea', { maxlength: '600', rows: '4', placeholder: 'Ce que vous avez aimé, ce qui peut être amélioré… (facultatif)', 'aria-label': 'Votre commentaire' }); com.value = (P && P.avis && P.avis.commentaire) || '';
    var ok = h('input', { type: 'checkbox', id: 'av-ok' }), msg = h('p', { class: 'err', role: 'alert', hidden: 'hidden' });
    var btn = h('button', { type: 'button', class: 'btn', text: 'Envoyer mon avis', onclick: function () {
      msg.hidden = true;
      if (!note) { msg.textContent = ERR.note; msg.hidden = false; return; }
      btn.disabled = true;
      api('/api/espace/avis', 'POST', { note: note, commentaire: com.value, publication: ok.checked }).then(function (r) {
        btn.disabled = false;
        if (r.j.ok) { flash('Merci pour votre avis !'); done(true); } else { msg.textContent = errTxt(r.j, r.s); msg.hidden = false; }
      });
    } });
    return h('div', { class: 'avf' }, h('h2', { text: 'Votre site est en ligne. Qu’en pensez-vous ?' }), h('p', { class: 'sub', text: 'Votre avis nous aide à nous améliorer et rassure les autres commerçants. Cela prend une minute.' }), st, h('label', { class: 'wide', style: 'display:block;margin-top:12px' }, 'Votre commentaire', com),
      h('label', { class: 'chk' }, ok, h('span', { text: 'J’autorise la publication de mon avis sur le site, avec mon prénom, l’initiale de mon nom et le nom de mon commerce.' })), msg,
      h('div', { class: 'tools', style: 'margin-top:14px;flex-wrap:wrap' }, btn, h('button', { type: 'button', class: 'btn ghost', text: 'Plus tard', onclick: function () { done(false, true); } })));
  }
  function avisPopup() {
    if (!P || !P.avis_invite || E.lecture) return;
    try { var t = +localStorage.getItem('dw-avis-plus-tard'); if (t && Date.now() - t < 7 * 864e5) return; } catch (_) {}
    var closeFn;
    var f = avisForm(function (sent, later) { if (later) { try { localStorage.setItem('dw-avis-plus-tard', String(Date.now())); } catch (_) {} } closeFn(); if (sent) reloadP(); });
    closeFn = modal('Donner mon avis', f, null);
  }

  function aFaire() {
    if (!P || !P.demande || E.lecture) return null;
    var d = P.demande, items = [], req = P.requis, n = req.filter(function (r) { return r.ok; }).length;
    var termine = !!P.dossier._termine, val = P.retours.some(function (r) { return r.type === 'valide'; }), enCours = P.retours.some(function (r) { return r.type === 'changements' && r.statut === 'a_traiter'; });
    if (d.statut === 'nouvelle' && !termine) items.push(['Complétez votre dossier (' + n + ' sur ' + req.length + ' éléments obligatoires)', 'Sans votre dossier complet, nous ne pouvons pas commencer.', 'Compléter mon dossier', 'dossier']);
    if (d.statut === 'apercu' && !val && !enCours) items.push(['Votre aperçu est prêt', 'Regardez-le, puis validez-le ou demandez des ajustements.', 'Voir mon aperçu', 'dossier']);
    if (d.statut === 'en_ligne' && P.avis_invite) items.push(['Donnez votre avis', 'Votre site est en ligne : dites-nous ce que vous en pensez.', 'Donner mon avis', 'avis']);
    if (P.resiliation) items.push(['Votre demande de résiliation est en cours', 'Elle prendra effet le ' + fdate(P.resiliation.effet) + '. Vous pouvez l’annuler depuis « Abonnement ».', 'Voir', 'abo']);
    if (!items.length) return null;
    return h('div', { class: 'card todo' }, h('h3', { class: 'ctit' }, ico('bolt', 22), 'À faire'), items.map(function (x) { return h('div', { class: 'todo-i' }, h('div', null, h('b', { text: x[0] }), h('p', { class: 'sub', text: x[1] })), h('button', { type: 'button', class: 'btn', text: x[2], onclick: function () { if (x[3] === 'avis') { try { localStorage.removeItem('dw-avis-plus-tard'); } catch (_) {} avisPopup(); } else go(x[3]); } })); }));
  }

  function vParcours(inner) {
    if (!inner) main.appendChild(head('Mon dossier', 'Où en est votre site, et ce qu’il vous reste à faire'));
    if (!P || !P.demande) { main.appendChild(h('div', { class: 'card' }, h('p', { class: 'empty', text: P ? 'Vous n’avez pas encore fait de demande de site.' : 'Impossible de charger votre parcours pour le moment.' }), h('a', { class: 'btn', href: '/commander', text: 'Faire ma demande' }))); return; }
    var d = P.demande, F = P.frise;
    if (F.pause) main.appendChild(h('div', { class: 'infobox', text: 'Votre demande est en pause. Écrivez-nous depuis « Aide & Guides » pour la reprendre.' }));
    var ol = h('ol', { class: 'frise' }, F.etapes.map(function (e) {
      var dd = e.etat === 'fait' && e.date ? fdate(e.date) : '';
      return h('li', { class: e.etat, 'aria-current': e.etat === 'cours' ? 'step' : null }, h('i', { 'aria-hidden': 'true' }, e.etat === 'fait' ? ico('check', 14) : null), h('div', null, h('b', { text: e.titre }), h('span', { class: 'sr', text: e.etat === 'fait' ? ' (terminé)' : e.etat === 'cours' ? ' (en cours)' : ' (à venir)' }), h('p', { text: e.detail }), dd ? h('small', { text: dd }) : null));
    }));
    main.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Les étapes de votre site' }), ol, h('p', { class: 'sub', style: 'margin:12px 0 0', text: 'Dès que votre dossier est complet, nous créons votre site rapidement.' })));
    if (d.statut === 'apercu') main.appendChild(apercuCard());

    if (d.statut === 'en_ligne') {
      var av = P.avis;
      main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h3', { text: 'Votre avis' }),
        av ? h('div', null, h('p', { class: 'stars ro', 'aria-label': 'Votre note : ' + av.note + ' sur 5', text: '★★★★★'.slice(0, av.note) + '☆☆☆☆☆'.slice(0, 5 - av.note) }), av.commentaire ? h('p', { text: '« ' + av.commentaire + ' »' }) : null, h('p', { class: 'sub', text: av.statut === 'publie' ? 'Merci ! Votre avis est publié sur notre site.' : av.statut === 'refuse' ? 'Merci pour votre retour.' : 'Merci ! Votre avis sera publié après relecture.' }), av.statut === 'en_attente' && !E.lecture ? h('button', { type: 'button', class: 'btn ghost', text: 'Modifier mon avis', onclick: function () { var c; c = modal('Modifier mon avis', avisForm(function (sent) { c(); if (sent) reloadP(); }), null); } }) : null)
          : h('div', null, h('p', { class: 'sub', text: 'Votre site est en ligne. Donnez-nous votre avis en une minute.' }), E.lecture ? null : h('button', { type: 'button', class: 'btn', text: 'Donner mon avis', onclick: function () { try { localStorage.removeItem('dw-avis-plus-tard'); } catch (_) {} avisPopup(); } }))));
    }
  }
  function apercuCard() {
    var d = P.demande, val = P.retours.filter(function (r) { return r.type === 'valide'; })[0], enCours = P.retours.filter(function (r) { return r.type === 'changements' && r.statut === 'a_traiter'; })[0];
    var box = h('div', { class: 'card apv', id: 'apercu', style: 'margin-top:16px' }, h('h2', { text: val ? 'Aperçu validé' : 'Votre aperçu est prêt' }));
    if (val) { box.appendChild(h('div', { class: 'infobox', text: 'Vous avez validé votre aperçu le ' + fdate(val.created_at.slice(0, 10)) + '. Nous préparons la mise en ligne de votre site.' })); return box; }
    box.appendChild(h('p', { class: 'sub', text: 'Regardez votre site sur téléphone et sur ordinateur. Vérifiez les textes, les horaires, les prix, l’adresse et les photos. Si tout vous convient, validez-le. Sinon, dites-nous précisément ce qui doit changer.' }));
    if (d.site_url) box.appendChild(h('p', null, h('a', { class: 'btn ghost', href: d.site_url, target: '_blank', rel: 'noopener' }, 'Ouvrir mon aperçu ', ico('ext', 16))));
    else box.appendChild(h('p', { class: 'sub', text: 'Le lien de votre aperçu vous est communiqué dans l’onglet Messages ou par téléphone.' }));
    if (enCours) box.appendChild(h('div', { class: 'infobox' }, h('b', { text: 'Votre demande d’ajustements est en cours de traitement.' }), h('p', { class: 'sub', style: 'margin:6px 0 0', text: '« ' + enCours.message + ' »' })));
    var zone = h('div', { class: 'apv-zone' }), btns = h('div', { class: 'tools', style: 'flex-wrap:wrap;gap:10px' });
    var dis = E.lecture ? 'disabled' : null;
    var bv = h('button', { type: 'button', class: 'btn', text: 'Je valide mon site', disabled: dis || (enCours ? 'disabled' : null), onclick: function () {
      zone.textContent = '';
      var msg = h('p', { class: 'err', role: 'alert', hidden: 'hidden' });
      zone.appendChild(h('div', { class: 'infobox' }, h('b', { text: 'Confirmer la validation ?' }), h('p', { class: 'sub', style: 'margin:6px 0 10px', text: 'Votre site sera mis en ligne et votre abonnement démarrera, avec un engagement de 12 mois. Vous pourrez ensuite demander des modifications dans la limite de votre formule.' }),
        h('div', { class: 'tools', style: 'flex-wrap:wrap;gap:10px' }, h('button', { type: 'button', class: 'btn', text: 'Oui, je valide', onclick: function () { api('/api/espace/apercu', 'POST', { action: 'valide' }).then(function (r) { if (r.j.ok) { flash('Aperçu validé, merci !'); reloadP('dossier'); } else { msg.textContent = errTxt(r.j, r.s); msg.hidden = false; } }); } }), h('button', { type: 'button', class: 'btn ghost', text: 'Pas encore', onclick: function () { zone.textContent = ''; } })), msg));
    } });
    var bc = h('button', { type: 'button', class: 'btn ghost', text: 'Je veux des changements', disabled: dis || (enCours ? 'disabled' : null), onclick: function () {
      zone.textContent = '';
      var ta = h('textarea', { maxlength: '1500', rows: '5', placeholder: 'Exemple : « Sur la page d’accueil, remplacez la photo du haut par celle de ma vitrine, et corrigez le téléphone : 04 12 34 56 78. »' }), msg = h('p', { class: 'err', role: 'alert', hidden: 'hidden' });
      zone.appendChild(h('div', { class: 'form' }, h('label', { class: 'wide' }, 'Que faut-il changer ?', ta), msg,
        h('div', { class: 'tools', style: 'flex-wrap:wrap;gap:10px' }, h('button', { type: 'button', class: 'btn', text: 'Envoyer mes demandes', onclick: function () { msg.hidden = true; api('/api/espace/apercu', 'POST', { action: 'changements', message: ta.value }).then(function (r) { if (r.j.ok) { flash('Vos demandes sont envoyées.'); reloadP('dossier'); } else { msg.textContent = errTxt(r.j, r.s); msg.hidden = false; } }); } }), h('button', { type: 'button', class: 'btn ghost', text: 'Annuler', onclick: function () { zone.textContent = ''; } }))));
      ta.focus();
    } });
    btns.appendChild(bv); btns.appendChild(bc); box.appendChild(btns); box.appendChild(zone);
    if (E.lecture) box.appendChild(h('p', { class: 'sub', text: 'Lecture seule : vous consultez ce compte en tant qu’administrateur.' }));
    var hist = P.retours.filter(function (r) { return r.type === 'changements'; });
    if (hist.length) box.appendChild(h('div', { style: 'margin-top:16px' }, h('h3', { text: 'Vos demandes d’ajustements' }), h('ul', { class: 'list' }, hist.map(function (r) { return h('li', null, h('div', { class: 'tbar', style: 'margin:0' }, h('b', { text: fdate(r.created_at.slice(0, 10)) }), h('span', { class: 'pill ' + (r.statut === 'traite' ? 'ok' : 'warn'), text: r.statut === 'traite' ? 'Faite' : 'En cours' })), h('div', { class: 'sub', text: r.message })); }))));
    return box;
  }

  var CHAMPS = [
    ['description', 'Présentation de votre commerce', 'ta', 'Qui êtes-vous, que proposez-vous, depuis quand, ce qui vous distingue. Quelques phrases suffisent, nous les mettrons en forme.', 'Boulangerie artisanale à Lyon depuis 2012. Pain au levain, viennoiseries maison…', true],
    ['horaires', 'Horaires d’ouverture', 'ta', 'Jour par jour, avec les fermetures (déjeuner, jours fériés).', 'Lundi : fermé\nMardi au samedi : 7h00 – 19h30\nDimanche : 7h00 – 13h00', true],
    ['adresse_pub', 'Adresse', 'in', 'L’adresse affichée sur votre site, comme sur une enseigne.', '12 rue des Fleurs, 69003 Lyon', true],
    ['tel_pub', 'Téléphone', 'in', 'Le numéro que vos clients doivent appeler.', '04 12 34 56 78', true],
    ['email_pub', 'E-mail de contact', 'in', 'Pour recevoir les messages de vos clients (facultatif).', 'contact@moncommerce.fr', false],
    ['services', 'Prestations ou carte, avec les tarifs', 'ta', 'Listez ce que vous vendez, avec les prix et les durées si cela s’applique.', 'Baguette tradition 1,20 €\nCroissant 1,40 €', true],
    ['reseaux', 'Réseaux sociaux', 'in', 'Les liens de vos pages Facebook, Instagram, etc. (facultatif).', 'https://www.instagram.com/moncommerce', false],
    ['couleurs', 'Couleurs et style souhaités', 'in', 'Vos couleurs préférées, ou le style : sobre, chaleureux, moderne… (facultatif).', 'Bleu marine et blanc, style sobre', false],
    ['slogan', 'Slogan', 'in', 'Une phrase d’accroche si vous en avez une (facultatif).', 'Le goût du vrai pain', false],
    ['domaine_choisi', 'Nom de domaine souhaité', 'in', 'L’adresse de votre site, par exemple boulangerie-martin.fr. Nous vérifions qu’elle est disponible.', 'boulangerie-martin.fr', false],
    ['remarques', 'Autre chose à nous dire ?', 'ta', 'Toute information utile (facultatif).', '', false]
  ];
  function lisFichier(f) {
    var max = P.fichier_max, isImg = /^image\/(png|jpeg|webp)$/.test(f.type);
    return new Promise(function (res, rej) {
      var fr = new FileReader();
      var send = function (blob, name, mime) { var r2 = new FileReader(); r2.onload = function () { res({ nom: name, mime: mime, data: String(r2.result).split(',')[1] }); }; r2.onerror = function () { rej(new Error('lecture')); }; r2.readAsDataURL(blob); };
      if (!isImg && f.type !== 'application/pdf') { rej(new Error('type')); return; }
      if (f.size <= max * 0.9 && (!isImg || f.size < 700000)) { send(f, f.name, f.type); return; }
      if (!isImg) { rej(new Error('taille')); return; }
      fr.onload = function () {
        var im = new Image();
        im.onload = function () {
          var s = Math.min(1, 1800 / Math.max(im.width, im.height)), cv = document.createElement('canvas'); cv.width = Math.round(im.width * s); cv.height = Math.round(im.height * s);
          var cx = cv.getContext('2d'); cx.fillStyle = '#fff'; cx.fillRect(0, 0, cv.width, cv.height); cx.drawImage(im, 0, 0, cv.width, cv.height);
          var q = 0.85, tryOnce = function () { cv.toBlob(function (b) { if (!b) { rej(new Error('lecture')); return; } if (b.size > max * 0.9 && q > 0.4) { q -= 0.15; tryOnce(); } else if (b.size > max * 0.9) rej(new Error('taille')); else send(b, f.name.replace(/\.\w+$/, '') + '.jpg', 'image/jpeg'); }, 'image/jpeg', q); };
          tryOnce();
        };
        im.onerror = function () { rej(new Error('lecture')); }; im.src = fr.result;
      };
      fr.onerror = function () { rej(new Error('lecture')); }; fr.readAsDataURL(f);
    });
  }
  var FERR = {};
  function vDossier() {
    main.appendChild(head('Mon dossier', 'Où en est votre site, et les informations dont nous avons besoin pour le créer'));
    if (!P || !P.demande) { main.appendChild(h('div', { class: 'card' }, h('p', { class: 'empty', text: P ? 'Faites d’abord votre demande de site.' : 'Impossible de charger votre dossier pour le moment.' }), h('a', { class: 'btn', href: '/commander', text: 'Faire ma demande' }))); return; }
    vParcours(true);
    main.appendChild(h('h2', { class: 'sech', style: 'margin:26px 0 12px;font-size:20px', text: 'Mes informations et mes fichiers' }));
    var dos = P.dossier, termine = !!dos._termine, ro = E.lecture ? 'disabled' : null, n = P.requis.filter(function (r) { return r.ok; }).length;
    main.appendChild(h('div', { class: 'card' }, h('h2', { text: termine ? 'Votre dossier est complet' : 'Comment ça marche' }),
      termine ? h('p', { class: 'sub', text: 'Reçu le ' + fdate(dos._termine) + '. Vous pouvez encore le compléter ou le corriger : prévenez-nous par un message si vous changez quelque chose d’important.' })
        : h('ol', { class: 'howto' }, h('li', { text: 'Remplissez les champs ci-dessous. Seuls cinq sont obligatoires, les autres nous aident mais sont facultatifs.' }), h('li', { text: 'Ajoutez votre logo (si vous en avez un) et quelques belles photos.' }), h('li', { text: 'Cliquez sur « J’ai terminé mon dossier ». C’est à ce moment que nous commençons la création de votre site.' })),
      h('p', { class: 'sub', style: 'margin:8px 0 0', text: 'Vous pouvez enregistrer et revenir plus tard : rien n’est perdu.' })));
    var prog = h('div', { class: 'card', style: 'margin-top:16px' }, h('div', { class: 'tbar' }, h('h3', { text: 'Éléments obligatoires' }), h('span', { class: 'pill ' + (n === P.requis.length ? 'ok' : 'warn'), text: n + ' sur ' + P.requis.length })),
      h('div', { class: 'quota', 'aria-hidden': 'true' }, h('u', { style: 'width:' + Math.round(n / P.requis.length * 100) + '%' })),
      h('ul', { class: 'reqs' }, P.requis.map(function (r) { return h('li', { class: r.ok ? 'ok' : '' }, h('i', { 'aria-hidden': 'true', text: r.ok ? '✓' : '○' }), r.libelle, h('span', { class: 'sr', text: r.ok ? ' (rempli)' : ' (à remplir)' })); })));
    main.appendChild(prog);
    var inputs = {}, form = h('div', { class: 'form dos' });
    CHAMPS.forEach(function (c) {
      var el = c[2] === 'ta' ? h('textarea', { rows: '4', maxlength: '900', placeholder: c[4], disabled: ro, id: 'dos-' + c[0] }) : h('input', { type: 'text', maxlength: '300', placeholder: c[4], disabled: ro, id: 'dos-' + c[0] });
      el.value = dos[c[0]] != null ? dos[c[0]] : (c[0] === 'domaine_choisi' && P.demande.domaine ? P.demande.domaine : ''); inputs[c[0]] = el;
      form.appendChild(h('label', { class: 'wide', for: 'dos-' + c[0] }, c[1] + (c[5] ? ' *' : ''), h('small', { class: 'hint', text: c[3] }), el));
    });
    var msg = h('p', { class: 'err', role: 'alert', hidden: 'hidden' });
    var save = function (after) {
      var ch = {}; CHAMPS.forEach(function (c) { ch[c[0]] = inputs[c[0]].value; });
      return api('/api/espace/dossier', 'POST', { champs: ch }).then(function (r) { if (r.j.ok) { if (after) after(); else { flash('Dossier enregistré.'); reloadP('dossier'); } } else { msg.textContent = errTxt(r.j, r.s); msg.hidden = false; } });
    };
    main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h3', { text: 'Vos informations' }), form, msg, E.lecture ? null : h('button', { type: 'button', class: 'btn', text: 'Enregistrer', onclick: function () { msg.hidden = true; save(); } })));
    var files = h('div', { class: 'card', style: 'margin-top:16px' }, h('h3', { text: 'Vos fichiers' }), h('p', { class: 'sub', text: 'Formats acceptés : images PNG, JPEG ou WebP, et PDF. Les photos trop lourdes sont réduites automatiquement. Vous pouvez envoyer jusqu’à ' + P.fichiers_max + ' fichiers.' }));
    [['logo', 'Votre logo', 'Si vous n’en avez pas, ce n’est pas grave : nous en créons un simple pour vous (inclus).'], ['photo', 'Vos photos', 'Vitrine, intérieur, produits, réalisations, vous au travail. Des photos nettes, prises en journée.'], ['document', 'Vos documents', 'Carte, tarifs, brochure en PDF.']].forEach(function (cat) {
      var mine = P.fichiers.filter(function (f) { return f.categorie === cat[0] || (cat[0] === 'document' && f.categorie === 'autre'); });
      var fin = h('input', { type: 'file', accept: cat[0] === 'document' ? 'application/pdf,image/png,image/jpeg,image/webp' : 'image/png,image/jpeg,image/webp', multiple: cat[0] !== 'logo' ? 'multiple' : null, disabled: ro, 'aria-label': 'Ajouter : ' + cat[1] });
      var em = h('p', { class: 'err', role: 'alert', hidden: FERR[cat[0]] ? null : 'hidden', text: FERR[cat[0]] || '' }); FERR[cat[0]] = '';
      fin.addEventListener('change', function () {
        var list = Array.prototype.slice.call(fin.files); if (!list.length) return;
        var chain = Promise.resolve(), okn = 0, errs = [];
        list.forEach(function (f) { chain = chain.then(function () { return lisFichier(f).then(function (x) { return api('/api/espace/fichier', 'POST', { categorie: cat[0], nom: x.nom, mime: x.mime, data: x.data }).then(function (r) { if (r.j.ok) okn++; else errs.push(f.name + ' : ' + errTxt(r.j, r.s)); }); }, function (er) { errs.push(f.name + ' : ' + (er.message === 'taille' ? ERR.taille : er.message === 'type' ? ERR.type : ERR.fichier)); }); }); });
        chain.then(function () { if (okn) flash(okn + ' fichier' + (okn > 1 ? 's' : '') + ' ajouté' + (okn > 1 ? 's' : '') + '.'); FERR[cat[0]] = errs.join(' '); return loadP(); }).then(function () { cur = 'dossier'; draw(); });
      });
      files.appendChild(h('div', { class: 'fcat' }, h('h4', { text: cat[1] }), h('p', { class: 'sub', text: cat[2] }),
        mine.length ? h('ul', { class: 'flist' }, mine.map(function (f) { var isI = /^image\//.test(f.mime); return h('li', null, isI ? h('img', { src: '/api/espace/fichier?id=' + f.id, alt: f.nom, width: '48', height: '48', loading: 'lazy' }) : h('span', { class: 'fico', 'aria-hidden': 'true', text: 'PDF' }), h('div', null, h('b', { text: f.nom }), h('small', { text: Math.max(1, Math.round(f.taille / 1024)) + ' Ko · ajouté le ' + fdate(f.created_at.slice(0, 10)) })), E.lecture ? null : h('button', { type: 'button', class: 'btn ghost sm', text: 'Supprimer', 'aria-label': 'Supprimer ' + f.nom, onclick: function () { api('/api/espace/fichier-suppr', 'POST', { id: f.id }).then(function () { flash('Fichier supprimé.'); reloadP('dossier'); }); } })); })) : h('p', { class: 'empty', style: 'margin:6px 0', text: 'Aucun fichier pour le moment.' }),
        E.lecture ? null : h('label', { class: 'upl' }, h('span', { class: 'btn ghost sm', text: cat[0] === 'logo' ? 'Ajouter mon logo' : cat[0] === 'photo' ? 'Ajouter des photos' : 'Ajouter un document' }), fin), em));
    });
    main.appendChild(files);
    if (!termine && !E.lecture) {
      var m2 = h('div', { class: 'err', role: 'alert', hidden: 'hidden' });
      main.appendChild(h('div', { class: 'card fin', style: 'margin-top:16px' }, h('h3', { text: 'Dernière étape' }), h('p', { class: 'sub', text: 'Quand vous avez tout rempli, cliquez ici. Nous recevons votre dossier et commençons la création de votre site.' }),
        h('button', { type: 'button', class: 'btn', text: 'J’ai terminé mon dossier', onclick: function () {
          m2.hidden = true;
          save(function () { api('/api/espace/dossier-termine', 'POST', {}).then(function (r) {
            if (r.j.ok) { flash('Dossier reçu, merci !'); reloadP('dossier'); }
            else if (r.j.error === 'incomplet') { m2.textContent = 'Il manque encore : ' + r.j.manquants.join(', ') + '.'; m2.hidden = false; loadP(); }
            else { m2.textContent = errTxt(r.j, r.s); m2.hidden = false; } }); });
        } }), m2));
    }
  }

  /* ===== changer de formule (effet au 1er du mois suivant) ===== */
  function nextFirst() { var t = (P && P.aujourdhui) || new Date().toISOString().slice(0, 10), y = +t.slice(0, 4), m = +t.slice(5, 7) + 1; if (m > 12) { m = 1; y++; } return y + '-' + (m < 10 ? '0' : '') + m + '-01'; }
  function addDays(iso, n) { var d = new Date(iso + 'T12:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); }
  function formuleCard() {
    var a = E.abonnement; if (!a || a.statut !== 'actif' || !P) return null;
    var ch = (P.changements || []).filter(function (c) { return c.statut === 'demande'; })[0];
    var box = h('div', { class: 'card', id: 'formule-card', style: 'margin-top:16px' }, h('h3', { text: 'Changer de formule' }));
    var mails = a.mails_sup || 0;
    if (ch) {
      var pro = ch.vers === 'pro', nm = pro ? Math.max(0, mails - 1) : mails + 1;
      box.appendChild(h('div', { class: 'infobox' }, h('b', { text: 'Votre passage à la formule ' + lab(ch.vers) + ' est programmé pour le ' + fdate(ch.effet) + '.' }),
        h('p', { class: 'sub', style: 'margin:6px 0 0', text: 'Jusqu’au ' + fdate(addDays(ch.effet, -1)) + ' inclus, vous gardez la formule ' + lab(ch.de) + ' et le mois en cours est facturé comme d’habitude. À partir du ' + fdate(ch.effet) + ' : ' + eurT(PRIX[ch.vers] + MAILP * nm) + ' par mois' + (!pro ? ' (dont votre adresse mail pro, désormais payante)' : '') + '.' })));
      if (!E.lecture) box.appendChild(h('button', { type: 'button', class: 'btn ghost', text: 'Annuler ce changement', onclick: function () { api('/api/espace/formule-annuler', 'POST', {}).then(function (x) { if (x.j.ok) { flash('Changement annulé : vous gardez votre formule.'); reloadP('abo'); } else flash(errTxt(x.j, x.s), true); }); } }));
      return box;
    }
    if (P.resiliation) { box.appendChild(h('p', { class: 'sub', text: 'Une demande de résiliation est en cours : le changement de formule n’est pas possible tant qu’elle n’est pas annulée ou traitée.' })); return box; }
    var vers = a.formule === 'pro' ? 'essentiel' : 'pro', eff = nextFirst(), up = vers === 'pro', nm2 = up ? Math.max(0, mails - 1) : mails + 1;
    box.appendChild(h('p', { class: 'sub', text: 'Vous pouvez passer à la formule ' + (up ? 'supérieure' : 'inférieure') + ' (' + lab(vers) + '). Le changement prend effet à la fin du mois en cours, sans prorata : le mois en cours reste facturé comme aujourd’hui, la nouvelle formule s’applique à partir du ' + fdate(eff) + '.' }));
    var zone = h('div'), b1 = h('button', { type: 'button', class: 'btn ghost', disabled: E.lecture ? 'disabled' : null, text: up ? 'Passer à la formule Pro' : 'Passer à la formule Essentiel', onclick: function () {
      b1.hidden = true;
      var ck = h('input', { type: 'checkbox', id: 'fc-ck' }), er = h('p', { class: 'err', role: 'alert', hidden: 'hidden' });
      var li = up ? [
        'Prix : ' + eurT(PRIX.essentiel) + ' → ' + eurT(PRIX.pro) + ' par mois (hors adresses mail en plus).',
        'Une adresse mail pro est incluse' + (mails > 0 ? ' : l’une de vos adresses payantes devient gratuite, il vous en reste ' + nm2 + ' à ' + eurT(MAILP) + '.' : '.'),
        '3 modifications par mois réalisées par nous (au lieu d’1), l’éditeur en libre-service, l’outil de réservation en ligne et l’agenda.'
      ] : [
        'Prix : ' + eurT(PRIX.pro) + ' → ' + eurT(PRIX.essentiel) + ' par mois.',
        'Votre adresse mail pro, jusqu’ici incluse dans la formule Pro, devient payante : ' + eurT(MAILP) + ' par mois et par adresse, soit ' + eurT(PRIX.essentiel + MAILP * nm2) + ' par mois au total avec ' + nm2 + ' adresse' + (nm2 > 1 ? 's' : '') + ' mail. Elle continue de fonctionner sans interruption.',
        '1 modification par mois réalisée par nous (au lieu de 3).',
        'Vous perdez l’éditeur en libre-service, l’outil de réservation en ligne et l’agenda à partir du ' + fdate(eff) + ' : pensez à récupérer vos données avant cette date.'
      ];
      zone.appendChild(h('div', { class: 'form' }, h('div', { class: 'warnbox', style: 'margin:0' }, h('div', null, h('b', { text: 'Ce qui change le ' + fdate(eff) + ' :' }), h('ul', { class: 'list', style: 'margin:8px 0 0' }, li.map(function (t) { return h('li', { text: t }); })), h('p', { class: 'sub', style: 'margin:10px 0 0', text: 'Votre engagement de 12 mois ne change pas. Vous pouvez annuler ce changement à tout moment jusqu’au ' + fdate(addDays(eff, -1)) + '.' }))),
        h('label', { class: 'chk' }, ck, h('span', { text: 'J’ai compris ce qui change et à quelle date.' })), er,
        h('div', { class: 'tools', style: 'flex-wrap:wrap;gap:10px' }, h('button', { type: 'button', class: 'btn', text: 'Confirmer le changement', onclick: function () { er.hidden = true; api('/api/espace/formule-changer', 'POST', { vers: vers, confirme: ck.checked }).then(function (x) { if (x.j.ok) { flash('Changement enregistré pour le ' + fdate(x.j.effet) + '.'); reloadP('abo'); } else { er.textContent = x.j.error === 'confirmation' ? 'Cochez la case pour confirmer.' : errTxt(x.j, x.s); er.hidden = false; } }); } }), h('button', { type: 'button', class: 'btn ghost', text: 'Je garde ma formule', onclick: function () { zone.textContent = ''; b1.hidden = false; } }))));
    } });
    box.appendChild(b1); box.appendChild(zone); return box;
  }

  function resilCard() {
    var r = P && P.resiliation, a = E.abonnement, eff = P && P.effet, box = h('div', { class: 'card resil', style: 'margin-top:16px' }, h('h3', { text: 'Résilier mon abonnement' }));
    if (!P || !P.demande) return null;
    if (a && a.statut === 'resilie') { box.appendChild(h('p', { class: 'sub', text: 'Votre abonnement est résilié' + (a.fin ? ' depuis le ' + dOnly(a.fin) : '') + '.' })); return box; }
    if (r) {
      box.appendChild(h('div', { class: 'infobox' }, h('b', { text: 'Votre demande de résiliation est enregistrée.' }), h('p', { class: 'sub', style: 'margin:6px 0 0', text: 'Elle prendra effet le ' + fdate(r.effet) + '. Jusque-là, votre site reste en ligne. Vous pouvez changer d’avis tant que nous ne l’avons pas traitée.' })));
      if (!E.lecture) box.appendChild(h('button', { type: 'button', class: 'btn ghost', text: 'Annuler ma demande de résiliation', onclick: function () { api('/api/espace/resiliation-annuler', 'POST', {}).then(function (x) { if (x.j.ok) { flash('Votre demande est annulée.'); reloadP('abo'); } else flash(errTxt(x.j, x.s), true); }); } }));
      return box;
    }
    box.appendChild(h('p', { class: 'sub', text: a && a.debut ? 'Votre engagement de 12 mois court jusqu’au ' + fdate(eff.echeance) + '. La résiliation prend effet à cette échéance, avec un préavis d’au moins 30 jours. Les mensualités de la période en cours restent dues.' : 'Votre abonnement n’a pas encore démarré : vous pouvez nous demander d’arrêter dès maintenant, sans engagement en cours.' }));
    var zone = h('div'), b1 = h('button', { type: 'button', class: 'btn ghost', text: 'Demander la résiliation', disabled: E.lecture ? 'disabled' : null, onclick: function () {
      b1.hidden = true;
      var mo = h('select', { 'aria-label': 'Motif' }, [['', 'Choisir un motif (facultatif)'], ['prix', 'Le prix'], ['plus_besoin', 'Je n’en ai plus besoin'], ['insatisfait', 'Je ne suis pas satisfait'], ['fermeture', 'Je ferme mon commerce'], ['autre', 'Autre raison']].map(function (o) { return h('option', { value: o[0], text: o[1] }); }));
      var ms = h('textarea', { rows: '3', maxlength: '800', placeholder: 'Dites-nous ce que nous aurions pu mieux faire (facultatif).' }), ck = h('input', { type: 'checkbox', id: 'rs-ck' }), er = h('p', { class: 'err', role: 'alert', hidden: 'hidden' });
      var quand = a && a.debut ? (eff.decale ? 'Le préavis de 30 jours avant votre échéance du ' + fdate(eff.echeance) + ' est dépassé : votre résiliation prendrait effet le ' + fdate(eff.effet) + '.' : 'Votre résiliation prendrait effet le ' + fdate(eff.effet) + '.') : 'Votre résiliation prendrait effet immédiatement.';
      zone.appendChild(h('div', { class: 'form' }, h('div', { class: 'warnbox', style: 'margin:0' }, h('div', null, h('b', { text: quand }), h('div', { text: 'Votre site sera ensuite mis hors ligne. Vous pourrez nous demander de récupérer vos textes et photos, et le transfert de votre nom de domaine.' }))), h('label', { class: 'wide' }, 'Motif', mo), h('label', { class: 'wide' }, 'Message', ms),
        h('label', { class: 'chk' }, ck, h('span', { text: 'Je confirme vouloir résilier mon abonnement et j’ai compris la date d’effet.' })), er,
        h('div', { class: 'tools', style: 'flex-wrap:wrap;gap:10px' }, h('button', { type: 'button', class: 'btn danger', text: 'Confirmer la résiliation', onclick: function () { er.hidden = true; api('/api/espace/resiliation', 'POST', { motif: mo.value, message: ms.value, confirme: ck.checked }).then(function (x) { if (x.j.ok) { flash('Demande de résiliation enregistrée.'); reloadP('abo'); } else { er.textContent = errTxt(x.j, x.s); er.hidden = false; } }); } }), h('button', { type: 'button', class: 'btn ghost', text: 'Je garde mon abonnement', onclick: function () { zone.textContent = ''; b1.hidden = false; } }))));
    } });
    box.appendChild(b1); box.appendChild(zone); return box;
  }

  function vParrainage() {
    main.appendChild(head('Parrainage', 'Un mois offert pour vous et pour le commerçant que vous nous présentez'));
    if (!P) { main.appendChild(h('div', { class: 'card' }, h('p', { class: 'empty', text: 'Impossible de charger le parrainage pour le moment.' }))); return; }
    var pa = P.parrainage, dispo = pa.credits.filter(function (c) { return c.etat === 'planifie' || c.etat === 'en_cours' || c.etat === 'disponible'; }).length;
    var cp = function (txt, ok) { var done = function () { flash(ok); }; if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done, function () { flash('Copiez le texte à la main : ' + txt, true); }); else flash('Copiez le texte à la main : ' + txt, true); };
    main.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Votre code de parrainage' }), h('p', { class: 'code', 'aria-label': 'Votre code : ' + pa.code.split('').join(' '), text: pa.code }),
      h('div', { class: 'tools', style: 'flex-wrap:wrap;gap:10px;margin:8px 0 12px' }, h('button', { type: 'button', class: 'btn', text: 'Copier mon code', onclick: function () { cp(pa.code, 'Code copié.'); } }), h('button', { type: 'button', class: 'btn ghost', text: 'Copier le lien à partager', onclick: function () { cp(pa.lien, 'Lien copié.'); } })),
      h('ol', { class: 'howto' }, h('li', { text: 'Donnez votre code à un commerçant, ou envoyez-lui le lien.' }), h('li', { text: 'Il le saisit en créant son compte, ou dans son espace avant le démarrage de son abonnement.' }), h('li', { text: 'Quand son abonnement démarre, un mois offert est ajouté à votre compte et au sien, déduit d’une prochaine facture.' })),
      h('p', { class: 'sub', style: 'margin:10px 0 0', text: 'Vous pouvez parrainer autant de commerçants que vous voulez : un mois offert pour chacun. Le code n’est valable que pour de nouveaux clients, et un parrainage non transformé en abonnement expire au bout de ' + pa.validite + ' jours. Chaque mois offert est valable 12 mois.' })));
    main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('div', { class: 'tbar' }, h('h3', { text: 'Mes mois offerts' }), h('span', { class: 'pill ' + (dispo ? 'ok' : ''), text: dispo + ' à venir' })),
      pa.credits.length ? h('ul', { class: 'list' }, pa.credits.map(function (c) { var o = c.origine === 'filleul' ? 'bienvenue' : c.origine === 'admin' ? 'geste de notre part' : 'parrainage'; return h('li', null, h('div', { class: 'tbar', style: 'margin:0' }, h('b', { text: c.mois_offert ? 'Mois offert : ' + moisLong(c.mois_offert) : '1 mois offert' }), h('span', { class: 'pill ' + (c.etat === 'utilise' ? 'pri' : c.etat === 'expire' ? 'bad' : 'ok'), text: c.etat === 'utilise' ? 'Appliqué' : c.etat === 'en_cours' ? 'En cours' : c.etat === 'expire' ? 'Expiré' : 'Prévu' })), h('div', { class: 'sub', text: (c.etat === 'utilise' ? 'Ce mois ne vous a pas été facturé' : c.etat === 'en_cours' ? 'Ce mois ne vous est pas facturé' : 'Ce mois ne vous sera pas facturé : le mois en cours est facturé normalement') + ' (' + o + ').' })); })) : h('p', { class: 'empty', text: 'Aucun mois offert pour le moment.' })));
    main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h3', { text: 'Mes filleuls' }), pa.filleuls.length ? h('ul', { class: 'list' }, pa.filleuls.map(function (f) { return h('li', null, h('div', { class: 'tbar', style: 'margin:0' }, h('b', { text: f.prenom || 'Un commerçant' }), h('span', { class: 'pill ' + (f.statut === 'valide' ? 'ok' : f.statut === 'expire' ? 'bad' : 'warn'), text: f.statut === 'valide' ? 'Parrainage validé' : f.statut === 'expire' ? 'Expiré' : 'En attente de son abonnement' })), h('div', { class: 'sub', text: 'Depuis le ' + fdate(f.date) })); })) : h('p', { class: 'empty', text: 'Personne n’a encore utilisé votre code.' })));
    if (pa.moi) main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h3', { text: 'Votre parrain' }), h('p', { class: 'sub', text: 'Vous avez utilisé le code ' + pa.moi.code + '. ' + (pa.moi.statut === 'valide' ? 'Votre mois offert est ajouté à votre compte.' : pa.moi.statut === 'expire' ? 'Ce parrainage a expiré.' : 'Votre mois offert sera ajouté au démarrage de votre abonnement.') })));
    else if (!E.lecture && (!E.abonnement) && P.demande && P.demande.statut !== 'en_ligne') {
      var ci = h('input', { type: 'text', maxlength: '9', placeholder: 'DW-XXXXX', 'aria-label': 'Code de parrainage reçu', autocapitalize: 'characters', autocomplete: 'off' }), er = h('p', { class: 'err', role: 'alert', hidden: 'hidden' });
      main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h3', { text: 'J’ai reçu un code de parrainage' }), h('p', { class: 'sub', text: 'Saisissez-le avant le démarrage de votre abonnement pour recevoir un mois offert.' }), h('div', { class: 'form' }, h('label', null, 'Code', ci), er), h('button', { type: 'button', class: 'btn', text: 'Appliquer le code', onclick: function () { er.hidden = true; api('/api/espace/parrain-appliquer', 'POST', { code: ci.value }).then(function (x) { if (x.j.ok) { flash('Code appliqué : un mois offert vous attend.'); reloadP('parrainage'); } else { er.textContent = errTxt(x.j, x.s); er.hidden = false; } }); } })));
    }
  }

  /* ===== navigation ===== */
  var VIEWS = { accueil: vAccueil, editeur: vEditeur, site: vSite, modifs: vModifs, abo: vAbo, messages: vMessages, factures: vFactures, facture: vFacture, resa: vResa, parcours: vDossier, dossier: vDossier, parrainage: vParrainage, aide: vAide, support: vSupport, guidepub: vGuidePub, compte: vCompte };
  var NAV = [['accueil', 'Tableau de bord', 'home'], ['dossier', 'Mon dossier', 'file'], ['site', 'Mon site', 'globe'], ['editeur', 'Modifications', 'edit', 'pro'], ['modifs', 'Demandes à l’équipe', 'headset'], ['abo', 'Abonnement', 'card'], ['factures', 'Factures', 'file'], ['parrainage', 'Parrainage', 'bolt'], ['aide', 'Aide & Guides', 'help'], ['compte', 'Mon compte', 'user']];
  var NAVALIAS = { facture: 'factures', guidepub: 'aide', support: 'aide', parcours: 'dossier', messages: 'accueil', resa: 'accueil' };
  function drawNav() {
    var nav = $('#nav'); nav.textContent = '';
    NAV.forEach(function (x) { if (x[3] === 'pro' && E.formule !== 'pro') return; var b = h('button', { type: 'button', 'aria-current': (cur === x[0] || NAVALIAS[cur] === x[0]) ? 'page' : null, onclick: function () { go(x[0]); } }, ico(x[2], 20), x[1]); if (x[0] === 'messages' && nonLues()) b.appendChild(h('span', { class: 'bdg2', text: String(nonLues()) })); nav.appendChild(b); });
    var sf = $('#sidefoot'); if (sf) { sf.textContent = ''; sf.appendChild(h('div', { class: 'helpc' }, h('div', { class: 'hh' }, ico('headset', 22), h('div', null, h('b', { text: 'Besoin d’aide ?' }), h('small', { text: 'Notre équipe vous répond rapidement.' }))), h('button', { type: 'button', class: 'btn', onclick: function () { go('support'); } }, 'Contacter le support ', ico('right', 16)))); sf.appendChild(h('a', { class: 'faql', href: '/faq', target: '_blank', rel: 'noopener', text: 'Questions fréquentes' })); }
  }
  function go(k) { cur = k; location.hash = k === 'accueil' ? '' : k; draw(); window.scrollTo(0, 0); }
  function draw() { main.textContent = ''; drawNav(); (VIEWS[cur] || vAccueil)(); }
  function prix() { if (E && E.prix) { PRIX = E.prix; MAILP = E.prix_mail || MAILP; } }
  function reload(k) { return api('/api/espace').then(function (r) { if (r.s === 401) { location.href = '/connexion'; return; } E = r.j; prix(); if (k) cur = k; return loadP().then(draw); }); }
  $('#n-out').addEventListener('click', function () { api('/api/deconnexion', 'POST').then(function () { location.href = '/connexion'; }); });
  window.addEventListener('hashchange', function () { var k = location.hash.slice(1) || 'accueil'; if (VIEWS[k] && k !== cur && E) { cur = k; draw(); } });

  api('/api/moi').then(function (m) {
    if (m.s === 401) { location.replace('/connexion'); return; }
    if (m.j.admin) { location.replace('/admin'); return; }
    if (m.j.impersonation) {
      document.body.classList.add('imp');
      document.body.appendChild(h('div', { class: 'impbar', role: 'status' }, 'Vous voyez l’espace de ' + m.j.nom + ' en lecture seule.', h('button', { type: 'button', text: 'Revenir à l’admin', onclick: function () { api('/api/quitter-impersonation', 'POST').then(function () { try { document.cookie = 'sv_imp=; Path=/; Max-Age=0; Secure; SameSite=Lax'; } catch (_) {} location.href = '/admin'; }); } })));
    }
    return api('/api/espace').then(function (r) {
      if (r.s !== 200 || !r.j.ok) { $('#gate').textContent = 'Impossible de charger votre espace. Réessayez dans un instant.'; return; }
      E = r.j; prix(); var k = location.hash.slice(1); cur = VIEWS[k] ? k : 'accueil';
      return loadP().then(function () { $('#gate').hidden = true; $('#app').hidden = false; draw(); avisPopup(); });
    });
  }).catch(function () { $('#gate').textContent = 'Connexion impossible pour le moment.'; });
})();
