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
  var IC = { globe: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18', card: 'M2 7a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2zM2 10h20', pen: 'M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z', msg: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z', home: 'M3 11l9-8 9 8v9a2 2 0 0 1-2 2h-4v-7H9v7H5a2 2 0 0 1-2-2z', help: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3M12 17h.01', user: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8', out: 'M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9', ext: 'M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3', cal: 'M3 5h18v16H3zM3 10h18M8 3v4M16 3v4' };
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
  function head(t, sub, extra) { return h('div', { class: 'top' }, h('div', { class: 'hello' }, h('h1', { text: t }), sub ? h('p', { text: sub }) : null), h('div', { class: 'tools' }, extra || [])); }
  var D = function () { return E.demandes[0] || null; };
  var nonLues = function () { return E.notifications.filter(function (n) { return !n.lu; }).length; };
  var enLigne = function () { var d = D(); return !!d && (d.statut === 'en_ligne' || d.statut === 'apercu') && !d.suspendu; };
  var addMonths = function (iso, n) { var d = new Date(iso + 'T12:00:00Z'); d.setUTCMonth(d.getUTCMonth() + n); return d.toISOString().slice(0, 10); };
  function hero(c, icon, v, l, sub, go) { var n = h('div', { class: 'card hero click', role: 'button', tabindex: '0' }, h('div', { class: 'ic ' + c }, ico(icon)), h('div', null, h('b', { text: v }), h('span', { text: l }), sub ? h('em', { text: sub }) : null)); n.classList.add('click'); n.addEventListener('click', go); n.addEventListener('keydown', function (e) { if (e.key === 'Enter') go(); }); return n; }

  /* ===== vues ===== */
  function vAccueil() {
    var d = D(), prenom = (E.compte.nom || '').split(/\s+/)[0], out = h('div'), idx = { nouvelle: 0, en_creation: 1, apercu: 2, en_ligne: 3 }[d && d.statut];
    main.appendChild(head('Bonjour ' + prenom, d ? d.commerce + ' · ' + new Date().toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' }) : 'Bienvenue sur votre espace', d && d.site_url && enLigne() ? [h('a', { class: 'btn', href: d.site_url, target: '_blank', rel: 'noopener' }, 'Voir mon site ', ico('ext', 16))] : []));
    if (d && d.suspendu) out.appendChild(h('div', { class: 'warnbox', role: 'alert' }, h('div', null, h('b', { text: 'Votre site est temporairement suspendu.' }), h('div', { text: 'Les modifications sont désactivées. Écrivez-nous depuis l’onglet Aide pour qu’on regarde ensemble.' }))));
    if (!d) {
      out.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Votre site vitrine' }), h('p', { class: 'sub', text: 'Vous n’avez pas encore fait de demande. Cela prend 3 minutes, sans engagement et sans paiement.' }), h('a', { class: 'btn', href: '/commander', text: 'Faire ma demande' })));
      main.appendChild(out); return;
    }
    var q = E.quota, u = E.utilisees, ab = E.abonnement;
    out.appendChild(h('div', { class: 'grid g4' },
      hero('c1', 'globe', lab(d.statut), 'Mon site', d.domaine || d.ville, function () { go('site'); }),
      hero('c2', 'card', lab(E.formule), 'Ma formule', eur(PRIX[E.formule] + MAILP * (ab ? ab.mails_sup : 0)) + ' / mois', function () { go('abo'); }),
      hero('c3', 'pen', Math.max(q - u, 0) + ' / ' + q, 'Modification(s) ce mois-ci', u ? u + ' utilisée(s)' : 'Aucune utilisée', function () { go('modifs'); }),
      hero('c4', 'msg', String(nonLues()), 'Message(s) non lu(s)', null, function () { go('messages'); })));
    if (idx != null) out.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h2', { text: 'Avancement de votre site' }), h('p', { class: 'sub', text: d.statut === 'en_ligne' ? 'Votre site est en ligne.' : 'Nous vous prévenons ici à chaque étape.' }),
      h('ol', { class: 'steps2' }, ['Demande reçue', 'En création', 'Aperçu à valider', 'En ligne'].map(function (t, i) { return h('li', { class: i < idx || idx === 3 ? 'done' : i === idx ? 'now' : '', text: t }); }))));
    var grid = h('div', { class: 'grid g2', style: 'margin-top:16px' });
    grid.appendChild(h('div', { class: 'card' }, h('h3', { text: 'Dernières nouvelles' }), E.notifications.length ? E.notifications.slice(0, 3).map(msgNode) : h('p', { class: 'empty', text: 'Aucun message pour le moment.' }), E.notifications.length ? h('button', { type: 'button', class: 'btn ghost sm', text: 'Tout voir', onclick: function () { go('messages'); } }) : null));
    if (E.formule === 'pro') grid.appendChild(h('div', { class: 'card' }, h('h3', { text: 'Réservations en ligne' }), h('p', { class: 'sub', text: 'Outil de réservation et agenda inclus dans votre formule Pro.' }), h('p', { class: 'empty', text: 'Aucune réservation pour le moment. Elles apparaîtront ici dès que vos clients réserveront.' })));
    else grid.appendChild(h('div', { class: 'card' }, h('h3', { text: 'Passer à la formule Pro' }), h('p', { class: 'sub', text: '100 € HT par mois' }), h('ul', { class: 'list' }, ['Outil de réservation en ligne et agenda', '3 modifications par mois', '1 adresse mail pro incluse'].map(function (t) { return h('li', { text: '✓ ' + t }); })), h('button', { type: 'button', class: 'btn ghost sm', text: 'En parler avec nous', onclick: function () { go('aide'); } })));
    out.appendChild(grid); main.appendChild(out);
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
    var inc = ['Site vitrine sur mesure', 'Nom de domaine et hébergement', 'Espace client', E.formule === 'pro' ? '3 modifications par mois' : '1 modification par mois', 'Guide pub'].concat(a.formule === 'pro' ? ['Outil de réservation en ligne', 'Agenda', '1 adresse mail pro incluse'] : []);
    main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h3', { text: 'Ce qui est inclus' }), h('ul', { class: 'list' }, inc.map(function (t) { return h('li', { text: '✓ ' + t }); })), h('p', { class: 'sub', style: 'margin-top:12px', text: 'Pour changer de formule ou ajouter une adresse mail, écrivez-nous depuis l’onglet Aide.' })));
  }
  function vMessages() {
    main.appendChild(head('Messages', 'Les nouvelles concernant votre site', nonLues() && !E.lecture ? [h('button', { type: 'button', class: 'btn ghost', text: 'Tout marquer comme lu', onclick: function () { api('/api/espace/lu', 'POST', {}).then(function () { reload('messages'); }); } })] : []));
    main.appendChild(h('div', { class: 'card' }, E.notifications.length ? E.notifications.map(msgNode) : h('p', { class: 'empty', text: 'Aucun message pour le moment.' })));
  }
  function vAide() {
    main.appendChild(head('Aide', 'Une question, un souci ? Écrivez-nous'));
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

  /* ===== navigation ===== */
  var VIEWS = { accueil: vAccueil, site: vSite, modifs: vModifs, abo: vAbo, messages: vMessages, aide: vAide, compte: vCompte };
  var NAV = [['accueil', 'Accueil', 'home'], ['site', 'Mon site', 'globe'], ['modifs', 'Modifications', 'pen'], ['abo', 'Abonnement', 'card'], ['messages', 'Messages', 'msg'], ['aide', 'Aide', 'help'], ['compte', 'Mon compte', 'user']];
  function drawNav() {
    var nav = $('#nav'); nav.textContent = '';
    NAV.forEach(function (x) { var b = h('button', { type: 'button', 'aria-current': cur === x[0] ? 'page' : null, onclick: function () { go(x[0]); } }, ico(x[2], 20), x[1]); if (x[0] === 'messages' && nonLues()) b.appendChild(h('span', { class: 'bdg2', text: String(nonLues()) })); nav.appendChild(b); });
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
