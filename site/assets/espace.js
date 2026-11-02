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
  var LBL = { nouvelle: 'Demande reçue', en_creation: 'En création', apercu: 'Aperçu à valider', en_ligne: 'En ligne', abandonnee: 'Abandonnée', actif: 'Actif', impaye: 'Impayé', suspendu: 'Suspendu', resilie: 'Résilié', ouverte: 'Reçue', en_cours: 'En cours', resolue: 'Traitée', essentiel: 'Essentiel', pro: 'Pro', demandee: 'Demandée', faite: 'Faite' };
  var PRIX = { essentiel: 60, pro: 100 }, MAILP = 4;
  var lab = function (k) { return LBL[k] || k || '—'; };
  var eur = function (n) { return (Math.round((n || 0) * 100) / 100).toLocaleString('fr-FR') + ' € HT'; };
  function dt(x) { if (!x) return '—'; var d = new Date(String(x).replace(' ', 'T') + 'Z'); return isNaN(d) ? x : d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }); }
  function dOnly(x) { if (!x) return '—'; var d = new Date(x + 'T12:00:00Z'); return isNaN(d) ? x : d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }); }
  function pill(k, c) { var m = { en_ligne: 'ok', actif: 'ok', faite: 'ok', resolue: 'ok', apercu: 'warn', en_creation: 'pri', nouvelle: 'pri', demandee: 'warn', ouverte: 'warn', en_cours: 'pri', impaye: 'bad', resilie: 'bad', suspendu: 'bad', abandonnee: '' }; return h('span', { class: 'pill ' + (c || m[k] || ''), text: lab(k) }); }
  var main = $('#main'), toast = $('#toast'), E = null, cur = 'accueil';
  function flash(t, bad) { toast.textContent = t; toast.className = 'toast on' + (bad ? ' bad' : ''); clearTimeout(flash.t); flash.t = setTimeout(function () { toast.className = 'toast'; }, 3800); }
  function initials(n) { return (n || '?').split(/\s+/).slice(0, 2).map(function (x) { return x.charAt(0).toUpperCase(); }).join(''); }
  function who() {
    var nl = nonLues(), bell = h('button', { type: 'button', class: 'bellb', 'aria-label': 'Messages', title: 'Messages', onclick: function () { go('messages'); } }, ico('bell', 22), nl ? h('i', { text: String(nl) }) : null);
    var av = h('button', { type: 'button', class: 'avb', title: 'Mon compte', onclick: function () { go('compte'); } }, h('span', { text: initials(E.compte.nom) }), ico('down', 16));
    return h('div', { class: 'who2' }, bell, av);
  }
  function head(t, sub, extra) { return h('div', { class: 'top' }, h('div', { class: 'hello' }, h('h1', { text: t }), sub ? h('p', { text: sub }) : null), h('div', { class: 'tools' }, (extra || []).concat([who()]))); }
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
  function vAccueil() {
    var d = D(), prenom = (E.compte.nom || '').split(/\s+/)[0], out = h('div'), idx = { nouvelle: 0, en_creation: 1, apercu: 2, en_ligne: 3 }[d && d.statut];
    main.appendChild(head('Bonjour ' + prenom + ' 👋', 'Bienvenue dans votre espace Devanture Web.', []));
    if (d && d.suspendu) out.appendChild(h('div', { class: 'warnbox', role: 'alert' }, h('div', null, h('b', { text: 'Votre site est temporairement suspendu.' }), h('div', { text: 'Les modifications sont désactivées. Écrivez-nous depuis l’onglet Aide pour qu’on regarde ensemble.' }))));
    if (!d) {
      out.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Votre site vitrine' }), h('p', { class: 'sub', text: 'Vous n’avez pas encore fait de demande. Cela prend 3 minutes, sans engagement et sans paiement.' }), h('a', { class: 'btn', href: '/commander', text: 'Faire ma demande' })));
      main.appendChild(out); return;
    }
    var q = E.quota, u = E.utilisees, ab = E.abonnement, pro = E.formule === 'pro', live = enLigne();
    out.appendChild(h('div', { class: 'kpis' },
      kp('layers', 'Mon site', lab(d.statut), d.domaine || d.ville, d.statut === 'en_ligne', function () { go('site'); }, d.statut === 'en_ligne'),
      kp('layers', 'Mon offre', lab(E.formule), (PRIX[E.formule] + MAILP * (ab ? ab.mails_sup : 0)) + ' € HT / mois', false, function () { go('abo'); }),
      kp('pen', 'Modifications', Math.max(q - u, 0) + ' / ' + q, 'restantes ce mois-ci', false, function () { go('modifs'); }),
      kp('mail', 'Messages', String(nonLues()), nonLues() > 1 ? 'nouveaux messages' : 'nouveau message', false, function () { go('messages'); })));
    var dEnLigne = (E.notifications.filter(function (n) { return /en ligne/i.test(n.titre); })[0] || {}).created_at;
    var site = h('div', { class: 'card sitec' }, preview(d), h('div', { class: 'sinfo' },
      h('div', { class: 'stop' }, h('h2', { text: d.commerce }), h('span', { class: 'dots', 'aria-hidden': 'true', text: '···' })),
      d.domaine ? h('a', { class: 'dom', href: d.site_url || '#', target: '_blank', rel: 'noopener' }, d.domaine, ico('ext', 14)) : h('span', { class: 'dom', text: d.ville }),
      h('div', { class: 'stat ' + (d.statut === 'en_ligne' ? 'ok' : '') }, ico('check', 16), lab(d.suspendu ? 'suspendu' : d.statut)),
      dEnLigne && d.statut === 'en_ligne' ? h('p', { class: 'mise', }, ico('cal', 18), 'Mis en ligne le ' + new Date(dEnLigne.replace(' ', 'T') + 'Z').toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' })) : null,
      h('div', { class: 'sbtn' }, d.site_url && live ? h('a', { class: 'btn', href: d.site_url, target: '_blank', rel: 'noopener' }, 'Voir mon site ', ico('ext', 16)) : null, h('button', { type: 'button', class: 'btn ghost', onclick: function () { go(pro ? 'editeur' : 'modifs'); } }, ico('edit', 16), ' Modifier mon site'))));
    var steps = ['Demande reçue', 'En création', 'Aperçu validé', 'En ligne'];
    var avanc = h('div', { class: 'card' }, h('h3', { class: 'ctit' }, ico('layers', 22), 'Avancement de mes demandes'), idx != null ? h('ol', { class: 'steps2' }, steps.map(function (t, i) { var done = i < idx || idx === 3; return h('li', { class: done ? 'done' : i === idx ? 'now' : '' }, h('b', { text: t }), h('small', { text: i === 0 ? dt(d.created_at).split(' ').slice(0, 3).join(' ') : done ? 'Terminé' : i === idx ? 'En cours' : 'À venir' })); })) : null);
    var tiles = h('div', { class: 'card' }, h('h3', { class: 'ctit' }, ico('bolt', 22), 'Accès rapides'), h('div', { class: 'tiles' }, [['pen', 'Demander une modification', 'modifs'], ['cal', 'Gérer mes réservations', 'resa'], ['mail', 'Envoyer un message', 'aide'], ['book', 'Consulter les guides', 'aide']].map(function (t) { return h('button', { type: 'button', class: 'tile', onclick: function () { go(t[2]); } }, ico(t[0], 24), h('span', { text: t[1] })); })));
    var stats = h('div', { class: 'card' }, h('h3', { class: 'ctit' }, ico('chart', 22), 'Statistiques de mon site'), h('div', { class: 'sts' }, [['eye', 'Visites'], ['right', 'Demandes de contact'], ['cal', 'Réservations']].map(function (t) { return h('div', null, ico(t[0], 20), h('b', { text: '—' }), h('small', { text: t[1] })); })), h('p', { class: 'sub', style: 'margin:10px 0 0', text: 'Les statistiques de fréquentation arrivent bientôt.' }));
    var inc = ['Site vitrine complet', 'Modifications (' + q + ' / mois)'].concat(pro ? ['Outil de réservation', 'Éditeur en libre-service'] : []).concat(aMail() ? ['Adresse e-mail pro'] : []).concat(pro ? ['Support prioritaire'] : []);
    var abo = h('div', { class: 'card' }, h('h3', { class: 'ctit' }, ico('card', 22), 'Mon abonnement'), h('div', { class: 'aboh' }, h('div', null, h('b', { class: 'plan', text: lab(E.formule) }), h('small', { text: (PRIX[E.formule] + MAILP * (ab ? ab.mails_sup : 0)) + ' € HT / mois' })), ab ? pill(ab.statut) : pill('nouvelle')), checks(inc), h('button', { type: 'button', class: 'btn ghost wide', onclick: function () { go('abo'); } }, 'Gérer mon abonnement ', ico('right', 16)));
    var acts = [].concat(E.notifications.slice(0, 3).map(function (n) { return [n.titre, n.message, n.created_at]; }));
    if (acts.length < 3) acts.push(['Nouvelle demande', 'Création de votre site.', d.created_at]);
    var act = h('div', { class: 'card' }, h('h3', { class: 'ctit' }, ico('clock', 22), 'Dernières activités'), h('ul', { class: 'tl' }, acts.slice(0, 3).map(function (a, i) { return h('li', { class: i === 0 ? 'first' : '' }, h('div', { class: 'tr' }, h('b', { text: a[0] }), h('small', { text: dt(a[2]).split(' ').slice(0, 3).join(' ') })), h('p', { text: a[1] })); })), h('button', { type: 'button', class: 'btn ghost wide', onclick: function () { go('messages'); } }, 'Voir toutes les activités ', ico('right', 16)));
    out.appendChild(h('div', { class: 'dgrid' }, h('div', { class: 'dleft' }, site, avanc, h('div', { class: 'two' }, tiles, stats)), h('div', { class: 'dright' }, abo, act)));
    main.appendChild(out);
  }
  function vFactures() {
    main.appendChild(head('Factures', 'Vos factures d’abonnement'));
    var ab = E.abonnement;
    main.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Vos factures' }), ab ? h('p', { class: 'sub', text: 'Abonnement ' + lab(ab.formule) + ' depuis le ' + dOnly(ab.debut) + '. Vos factures sont envoyées par e-mail et apparaîtront ici.' }) : h('p', { class: 'sub', text: 'Votre abonnement démarre à la mise en ligne de votre site. Vos factures apparaîtront ici dès ce moment.' }), h('p', { class: 'empty', text: 'Aucune facture pour le moment.' })));
  }
  function vResa() {
    main.appendChild(head('Réservations', 'Les réservations de vos clients'));
    if (E.formule === 'pro') main.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Outil de réservation en ligne' }), h('p', { class: 'sub', text: 'Inclus dans votre formule Pro : vos clients réservent seuls, jour et nuit, sans double réservation.' }), h('p', { class: 'empty', text: 'Aucune réservation pour le moment. Elles apparaîtront ici dès que vos clients réserveront.' })));
    else main.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Passer à la formule Pro' }), h('p', { class: 'sub', text: '100 € HT par mois' }), checks(['Outil de réservation en ligne et agenda', '3 modifications par mois', '1 adresse mail pro incluse']), h('button', { type: 'button', class: 'btn', text: 'En parler avec nous', onclick: function () { go('aide'); } })));
  }
  function msgNode(n) { return h('div', { class: 'msg' + (n.lu ? '' : ' nl') }, h('b', { text: n.titre }), h('p', { text: n.message }), h('small', { text: dt(n.created_at) })); }
  function vSite() {
    var d = D(); main.appendChild(head('Mon site', 'Les informations de votre site vitrine'));
    if (!d) { main.appendChild(h('div', { class: 'card' }, h('p', { class: 'empty', text: 'Aucun site pour le moment.' }), h('a', { class: 'btn', href: '/commander', text: 'Faire ma demande' }))); return; }
    var dl = h('dl', { class: 'dl' }, [['Commerce', d.commerce], ['Statut', lab(d.statut)], ['Activité', d.activite], ['Ville', d.ville], ['Nom de domaine', d.domaine || 'À définir'], ['Référence', d.ref], ['Demande du', dt(d.created_at)], ['Adresses mail pro', String(d.mails || 0)]].map(function (x) { return h('div', null, h('dt', { text: x[0] }), h('dd', { text: x[1] || '—' })); }));
    main.appendChild(h('div', { class: 'card' }, h('div', { class: 'tbar' }, h('h2', { text: d.commerce }), pill(d.suspendu ? 'suspendu' : d.statut)), dl));
    if (d.site_url && enLigne()) {
      var rel = d.site_url.charAt(0) === '/';
      main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('div', { class: 'tbar' }, h('h2', { text: 'Aperçu' }), h('a', { class: 'btn', href: d.site_url, target: '_blank', rel: 'noopener' }, 'Ouvrir mon site ', ico('ext', 16))),
        rel ? h('div', { class: 'browser' }, h('div', { class: 'bar' }, h('i'), h('i'), h('i'), h('span', { text: d.domaine || d.site_url })), h('iframe', { src: d.site_url, title: 'Aperçu de mon site', loading: 'lazy' })) : h('p', { class: 'sub', text: 'Cliquez sur « Ouvrir mon site » pour le voir en grand.' })));
    } else main.appendChild(h('div', { class: 'infobox', style: 'margin-top:16px', text: d.suspendu ? 'Votre site est suspendu pour le moment.' : 'Votre site apparaîtra ici dès que l’aperçu sera prêt. Nous vous prévenons dans l’onglet Messages.' }));
  }
  function vModifs() {
    var q = E.quota, u = E.utilisees, left = Math.max(q - u, 0), d = D(), can = !E.lecture && enLigne() && left > 0;
    main.appendChild(head('Mes modifications', q + ' modification' + (q > 1 ? 's' : '') + ' par mois avec la formule ' + lab(E.formule), []));
    var ty = h('select', null, [['texte', 'Remplacer un texte'], ['photo', 'Remplacer une photo'], ['bloc', 'Ajouter ou supprimer un bloc'], ['autre', 'Autre']].map(function (o) { return h('option', { value: o[0], text: o[1] }); })), ds = h('textarea', { maxlength: '1200', placeholder: 'Décrivez précisément ce que vous voulez changer et où.' });
    var why = E.lecture ? 'Lecture seule : vous consultez ce compte en tant qu’administrateur.' : !d ? 'Faites d’abord votre demande de site.' : d.suspendu ? 'Votre site est suspendu.' : !enLigne() ? 'Disponible dès que votre aperçu est prêt.' : left < 1 ? 'Vous avez utilisé votre modification de ce mois-ci. Elle revient le 1er du mois prochain.' : '';
    main.appendChild(h('div', { class: 'card' }, h('h2', { text: left + ' restante' + (left > 1 ? 's' : '') + ' ce mois-ci' }), h('div', { class: 'quota' }, h('u', { style: 'width:' + Math.min(100, Math.round((u / q) * 100)) + '%' })), h('p', { class: 'sub', text: u + ' utilisée' + (u > 1 ? 's' : '') + ' sur ' + q + ' · une modification non utilisée ne se cumule pas.' }),
      why ? h('div', { class: 'infobox', text: why }) : null,
      h('div', { class: 'form' }, h('label', null, 'Type de modification', ty), h('label', { class: 'wide' }, 'Votre demande', ds)),
      h('button', { type: 'button', class: 'btn', text: 'Envoyer ma modification', disabled: can ? null : 'disabled', onclick: function () {
        api('/api/espace/modif', 'POST', { type: ty.value, description: ds.value }).then(function (r) { if (r.j.ok) { flash('Modification envoyée.'); reload('modifs'); } else flash(r.j.error === 'vide' ? 'Décrivez votre demande (5 caractères minimum).' : r.j.error === 'quota' ? 'Quota du mois atteint.' : 'Envoi impossible pour le moment.', true); });
      } })));
    main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h3', { text: 'Historique' }), E.modifs.length ? h('ul', { class: 'list' }, E.modifs.map(function (m) { return h('li', null, h('div', { class: 'tbar', style: 'margin:0' }, h('b', { text: lab(m.type) === m.type ? ({ texte: 'Texte', photo: 'Photo', bloc: 'Bloc', autre: 'Autre' }[m.type] || m.type) : m.type }), pill(m.statut)), h('div', { class: 'sub', style: 'margin:4px 0 0', text: m.description }), h('small', { text: dt(m.created_at) })); })) : h('p', { class: 'empty', text: 'Aucune modification pour le moment.' })));
  }
  function vAbo() {
    var a = E.abonnement; main.appendChild(head('Mon abonnement', 'Formule, prix et engagement'));
    if (!a) { main.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Formule ' + lab(E.formule) }), h('p', { class: 'sub', text: 'Votre abonnement démarre à la mise en ligne de votre site. Aucun paiement n’a été demandé à ce stade.' }), h('p', { text: eur(PRIX[E.formule]) + ' par mois, engagement de 12 mois.' }))); return; }
    var tot = PRIX[a.formule] + MAILP * (a.mails_sup || 0), fin = a.debut ? addMonths(a.debut, 12) : null;
    main.appendChild(h('div', { class: 'card' }, h('div', { class: 'tbar' }, h('h2', { text: 'Formule ' + lab(a.formule) }), pill(a.statut)),
      h('dl', { class: 'dl' }, [['Total par mois', eur(tot)], ['Formule', eur(PRIX[a.formule])], ['Mails pro en plus', (a.mails_sup || 0) + ' × ' + eur(MAILP).replace(' HT', '') + ' HT'], ['Début', dOnly(a.debut)], ['Fin de l’engagement de 12 mois', fin ? dOnly(fin) : '—']].map(function (x) { return h('div', null, h('dt', { text: x[0] }), h('dd', { text: x[1] })); }))));
    var inc = ['Site vitrine sur mesure', 'Nom de domaine et hébergement', 'Espace client', E.formule === 'pro' ? '3 modifications par mois réalisées par nous' : '1 modification par mois réalisée par nous', 'Guide pub'].concat(aMail() ? ['Guide d’installation de la messagerie'] : []).concat(a.formule === 'pro' ? ['Éditeur en libre-service : textes, prix, horaires, photos', 'Outil de réservation en ligne', 'Agenda', '1 adresse mail pro incluse'] : []);
    main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h3', { text: 'Ce qui est inclus' }), h('ul', { class: 'list' }, inc.map(function (t) { return h('li', { text: '✓ ' + t }); })), h('p', { class: 'sub', style: 'margin-top:12px', text: 'Pour changer de formule ou ajouter une adresse mail, écrivez-nous depuis l’onglet Aide.' })));
  }
  function vMessages() {
    if (nonLues() && !E.lecture) { api('/api/espace/lu', 'POST', {}).then(function () { E.notifications.forEach(function (n) { n.lu = 1; }); drawNav(); document.querySelectorAll('.bellb i').forEach(function (e) { e.remove(); }); }); }
    main.appendChild(head('Messages', 'Les nouvelles concernant votre site', nonLues() && !E.lecture ? [h('button', { type: 'button', class: 'btn ghost', text: 'Tout marquer comme lu', onclick: function () { api('/api/espace/lu', 'POST', {}).then(function () { reload('messages'); }); } })] : []));
    main.appendChild(h('div', { class: 'card' }, E.notifications.length ? E.notifications.map(msgNode) : h('p', { class: 'empty', text: 'Aucun message pour le moment.' })));
  }
  function vAide() {
    main.appendChild(head('Aide', 'Une question, un souci ? Écrivez-nous'));
    if (aMail()) main.appendChild(mailCard());
    var sj = h('input', { type: 'text', maxlength: '120', placeholder: 'Ex. : changer de formule, un souci sur mon site…' }), ms = h('textarea', { maxlength: '1500', placeholder: 'Expliquez-nous en quelques lignes.' });
    main.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Nous écrire' }), h('div', { class: 'form' }, h('label', { class: 'wide' }, 'Sujet', sj), h('label', { class: 'wide' }, 'Message', ms)),
      h('button', { type: 'button', class: 'btn', text: 'Envoyer', disabled: E.lecture ? 'disabled' : null, onclick: function () { if (!sj.value.trim()) { flash('Indiquez un sujet.', true); return; } api('/api/espace/plainte', 'POST', { sujet: sj.value, message: ms.value }).then(function (r) { if (r.j.ok) { flash('Message envoyé. Nous revenons vers vous rapidement.'); reload('aide'); } else flash('Envoi impossible.', true); }); } }),
      h('p', { class: 'sub', style: 'margin-top:10px' }, 'Pensez aussi à la ', h('a', { href: '/faq', target: '_blank', rel: 'noopener', text: 'FAQ' }), '.')));
    main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h3', { text: 'Mes messages envoyés' }), E.plaintes.length ? h('ul', { class: 'list' }, E.plaintes.map(function (p) { return h('li', null, h('div', { class: 'tbar', style: 'margin:0' }, h('b', { text: p.sujet }), pill(p.statut)), h('small', { text: dt(p.created_at) })); })) : h('p', { class: 'empty', text: 'Rien pour le moment.' })));
  }
  function vCompte() {
    main.appendChild(head('Mon compte', E.compte.email));
    main.appendChild(h('div', { class: 'card', style: 'margin-bottom:16px' }, h('dl', { class: 'dl' }, [['Nom', E.compte.nom], ['E-mail', E.compte.email], ['Compte créé le', dt(E.compte.created_at)]].map(function (x) { return h('div', null, h('dt', { text: x[0] }), h('dd', { text: x[1] })); }))));
    var a = h('input', { type: 'password', autocomplete: 'current-password' }), n = h('input', { type: 'password', autocomplete: 'new-password' }), n2 = h('input', { type: 'password', autocomplete: 'new-password' });
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
      var C = r.j.champs, off = r.j.lecture || !!r.j.suspendu, frame = h('iframe', { src: r.j.site_url, title: 'Aperçu de mon site', loading: 'lazy' }), cnt = h('span', { class: 'pill', text: '' }), refT;
      var maj = function () { cnt.textContent = C.filter(function (c) { return c.val !== null; }).length + ' modifié(s)'; };
      var refresh = function () { clearTimeout(refT); refT = setTimeout(function () { frame.src = r.j.site_url + '?v=' + Date.now(); }, 350); };
      function save(c, valeur, st, rst, node) {
        var p = valeur === null ? api('/api/espace/contenu', 'POST', { k: c.k, reset: true }) : api('/api/espace/contenu', 'POST', { k: c.k, valeur: valeur });
        st.textContent = 'Enregistrement…';
        return p.then(function (x) {
          if (!x.j.ok) { st.textContent = ''; flash(x.j.error === 'texte' ? 'Le texte doit faire entre 1 et 600 caractères.' : x.j.error === 'suspendu' ? 'Votre site est suspendu.' : x.j.error === 'lecture-seule' ? 'Lecture seule.' : 'Enregistrement impossible.', true); return false; }
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
      if (r.j.suspendu) box.appendChild(h('div', { class: 'warnbox' }, 'Votre site est suspendu : les modifications sont désactivées.'));
      if (r.j.lecture) box.appendChild(h('div', { class: 'infobox', text: 'Lecture seule : vous consultez cet éditeur en tant qu’administrateur.' }));
      box.appendChild(h('div', { class: 'editor' },
        h('div', { class: 'edcol card' }, h('div', { class: 'tbar' }, h('h2', { text: 'Contenu du site' }), cnt), q, list),
        h('div', { class: 'edprev card' }, h('div', { class: 'tbar' }, h('h3', { text: 'Votre site' }), h('a', { class: 'btn ghost sm', href: r.j.site_url, target: '_blank', rel: 'noopener', text: 'Ouvrir' })), h('div', { class: 'browser' }, h('div', { class: 'bar' }, h('i'), h('i'), h('i'), h('span', { text: 'Aperçu en direct' })), frame))));
    }).catch(function () { box.textContent = ''; box.appendChild(h('div', { class: 'card' }, h('p', { class: 'empty', text: 'Chargement impossible.' }))); });
  }

  /* ===== navigation ===== */
  var VIEWS = { accueil: vAccueil, editeur: vEditeur, site: vSite, modifs: vModifs, abo: vAbo, messages: vMessages, factures: vFactures, resa: vResa, aide: vAide, compte: vCompte };
  var NAV = [['accueil', 'Tableau de bord', 'home'], ['site', 'Mon site', 'globe'], ['editeur', 'Modifications', 'edit', 'pro'], ['modifs', 'Demandes à l’équipe', 'headset'], ['abo', 'Abonnement', 'card'], ['messages', 'Messages', 'msg'], ['factures', 'Factures', 'file'], ['resa', 'Réservations', 'cal'], ['aide', 'Aide & Guides', 'help']];
  function drawNav() {
    var nav = $('#nav'); nav.textContent = '';
    NAV.forEach(function (x) { if (x[3] === 'pro' && E.formule !== 'pro') return; var b = h('button', { type: 'button', 'aria-current': cur === x[0] ? 'page' : null, onclick: function () { go(x[0]); } }, ico(x[2], 20), x[1]); if (x[0] === 'messages' && nonLues()) b.appendChild(h('span', { class: 'bdg2', text: String(nonLues()) })); if (x[0] === 'editeur' && E.quota) b.appendChild(h('span', { class: 'bdg2', text: String(Math.max(E.quota - E.utilisees, 0)) })); nav.appendChild(b); });
    var sf = $('#sidefoot'); if (sf) { sf.textContent = ''; sf.appendChild(h('div', { class: 'helpc' }, h('div', { class: 'hh' }, ico('headset', 22), h('div', null, h('b', { text: 'Besoin d’aide ?' }), h('small', { text: 'Notre équipe vous répond sous 24 h.' }))), h('button', { type: 'button', class: 'btn', onclick: function () { go('aide'); } }, 'Contacter le support ', ico('right', 16)))); sf.appendChild(h('button', { type: 'button', class: 'userc', onclick: function () { go('compte'); } }, h('span', { class: 'av2', text: initials(E.compte.nom) }), h('div', null, h('b', { text: E.compte.nom }), h('small', { text: (D() && D().commerce) || E.compte.email })), ico('right', 16))); }
  }
  function go(k) { cur = k; location.hash = k === 'accueil' ? '' : k; draw(); window.scrollTo(0, 0); }
  function draw() { main.textContent = ''; drawNav(); (VIEWS[cur] || vAccueil)(); }
  function reload(k) { return api('/api/espace').then(function (r) { if (r.s === 401) { location.href = '/connexion'; return; } E = r.j; if (k) cur = k; draw(); }); }
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
      E = r.j; var k = location.hash.slice(1); cur = VIEWS[k] ? k : 'accueil';
      $('#gate').hidden = true; $('#app').hidden = false; draw();
    });
  }).catch(function () { $('#gate').textContent = 'Connexion impossible pour le moment.'; });
})();
