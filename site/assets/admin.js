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
    msg: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z',
    filter: 'M22 3H2l8 9.5V19l4 2v-8.5z'
  };
  function ico(n, size, color) { return s('svg', { width: size || 20, height: size || 20, viewBox: '0 0 24 24', fill: 'none', stroke: color || 'currentColor', 'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'aria-hidden': 'true' }, s('path', { d: IC[n] })); }
  var LBL = { nouvelle: 'À traiter', en_creation: 'En création', apercu: 'Aperçu envoyé', en_ligne: 'En ligne', abandonnee: 'Abandonnée', hesite: 'Hésite', a_rappeler: 'À rappeler', plus_tard: 'Reviendra plus tard', sans_reponse: 'Sans réponse', trop_cher: 'Trouve ça trop cher', concurrent: 'Parti chez un concurrent', refusee: 'A refusé', actif: 'Actif', impaye: 'Impayé', suspendu: 'Suspendu', resilie: 'Résilié', ouverte: 'Ouverte', en_cours: 'En cours', resolue: 'Résolue', essentiel: 'Essentiel', pro: 'Pro' };
  var lab = function (k) { return LBL[k] || k || '—'; };
  var COL = { pri: '#4f46e5', sky: '#0ea5e9', ok: '#10b981', warn: '#f59e0b', bad: '#ef4444', gray: '#94a3b8', pur: '#7c3aed' };
  var eur = function (n) { return (Math.round((n || 0) * 10) / 10).toLocaleString('fr-FR') + ' €'; };
  var num = function (n) { return (n || 0).toLocaleString('fr-FR'); };
  function dt(x) { if (!x) return '—'; var d = new Date(x.replace(' ', 'T') + 'Z'); return isNaN(d) ? x : d.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' }) + ' ' + d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }); }
  function dOnly(x) { if (!x) return '—'; var d = new Date(x + 'T12:00:00Z'); return isNaN(d) ? x : d.toLocaleDateString('fr-FR'); }
  function pillFor(k) { var c = { en_ligne: 'ok', actif: 'ok', resolue: 'ok', apercu: 'pri', en_creation: 'pri', en_cours: 'warn', nouvelle: 'warn', ouverte: 'bad', impaye: 'bad', abandonnee: '', hesite: 'warn', a_rappeler: 'warn', plus_tard: 'warn', sans_reponse: '', trop_cher: '', concurrent: '', refusee: 'bad', resilie: 'bad', suspendu: 'warn' }[k]; return h('span', { class: 'pill ' + (c || ''), text: lab(k) }); }
  var main = $('#main'), toast = $('#toast');
  function flash(t, bad) { toast.textContent = t; toast.className = 'toast on' + (bad ? ' bad' : ''); clearTimeout(flash.t); flash.t = setTimeout(function () { toast.className = 'toast'; }, 3800); }

  function impersonate(id) {
    api('/api/admin/impersonate', 'POST', { compte_id: id }).then(function (r) {
      if (r.s === 200 && r.j.ok) { try { document.cookie = 'sv_imp=1; Path=/; Max-Age=7200; Secure; SameSite=Lax'; } catch (_) {} location.href = '/espace'; }
      else flash('Connexion au compte impossible.', true);
    });
  }
  /* ===== actions sur un client ===== */
  function actionsCard(c, demandes) {
    var d = demandes[0], box = h('div', { class: 'card', style: 'margin-bottom:16px' }), nz = h('div');
    box.appendChild(h('h2', { text: 'Actions' })); box.appendChild(h('p', { class: 'sub', text: 'Tout ce que vous pouvez faire pour ce client.' }));
    var bt = function (t, fn, ghost) { return h('button', { type: 'button', class: 'btn sm' + (ghost === false ? '' : ' ghost'), text: t, onclick: fn }); };
    var row = h('div', { class: 'tools', style: 'flex-wrap:wrap' });
    row.appendChild(bt('Se connecter à sa place', function () { impersonate(c.id); }, false));
    if (d) row.appendChild(bt(d.suspendu ? 'Réactiver le site' : 'Suspendre le site', function () { api('/api/admin/site', 'POST', { id: d.id, suspendu: !d.suspendu }).then(function (x) { flash(x.j.ok ? (d.suspendu ? 'Site réactivé.' : 'Site suspendu.') : 'Échec.', !x.j.ok); if (x.j.ok) loadAll().then(function () { detail(c.id); }); }); }));
    row.appendChild(bt('Envoyer une notification', function () { nz.hidden = !nz.hidden; }));
    row.appendChild(bt('Envoyer un e-mail', function () { COMM.pre = [c.id]; top(commView); mark('com'); }));
    row.appendChild(bt('Réinitialiser le mot de passe', function () { if (!window.confirm('Générer un nouveau mot de passe pour ' + c.nom + ' ? L’ancien ne fonctionnera plus et ses sessions seront fermées.')) return; api('/api/admin/reset-mdp', 'POST', { compte_id: c.id }).then(function (x) { if (!x.j.ok) { flash('Échec.', true); return; } var o = h('div', { class: 'infobox' }, 'Nouveau mot de passe (à transmettre au client, affiché une seule fois) : ', h('b', { text: x.j.mdp })); box.appendChild(o); }); }));
    box.appendChild(row);
    var ti = h('input', { type: 'text', maxlength: '120', placeholder: 'Titre' }), ms = h('textarea', { maxlength: '1000', placeholder: 'Message affiché dans l’espace du client', style: 'min-height:80px' });
    nz.hidden = true; nz.appendChild(h('div', { class: 'form' }, h('label', { class: 'wide' }, 'Titre', ti), h('label', { class: 'wide' }, 'Message', ms)));
    nz.appendChild(h('button', { type: 'button', class: 'btn', text: 'Envoyer la notification', onclick: function () { api('/api/admin/notifier', 'POST', { ids: [c.id], titre: ti.value, message: ms.value }).then(function (x) { flash(x.j.ok ? 'Notification envoyée.' : 'Titre et message requis.', !x.j.ok); if (x.j.ok) { ti.value = ms.value = ''; nz.hidden = true; } }); } }));
    box.appendChild(nz);
    if (d) {
      var u = h('input', { type: 'text', maxlength: '200', value: d.site_url || '', placeholder: 'https://… ou /exemples/…' });
      box.appendChild(h('div', { class: 'form' }, h('label', { class: 'wide' }, 'Adresse du site en ligne (bouton « Voir mon site » du client)', u)));
      box.appendChild(bt('Enregistrer l’adresse', function () { api('/api/admin/site', 'POST', { id: d.id, site_url: u.value }).then(function (x) { flash(x.j.ok ? 'Adresse enregistrée.' : 'Adresse invalide (https:// ou /chemin).', !x.j.ok); if (x.j.ok) loadAll(); }); }));
    }
    var plus = h('div'); box.appendChild(plus);
    api('/api/admin/compte-plus?id=' + c.id).then(function (x) {
      if (!x.j.ok) return;
      var oo = h('label', { class: 'chk', style: 'margin-top:12px' }), cb = h('input', { type: 'checkbox' }); cb.checked = !!x.j.opt_out;
      cb.addEventListener('change', function () { api('/api/admin/opt-out', 'POST', { compte_id: c.id, opt_out: cb.checked }).then(function () { flash(cb.checked ? 'Ce client ne recevra plus vos e-mails de communication.' : 'E-mails de communication réactivés.'); loadAll(); }); });
      oo.appendChild(cb); oo.appendChild(document.createTextNode(' A demandé à ne plus recevoir les e-mails de communication')); plus.appendChild(oo);
      plus.appendChild(h('h3', { style: 'margin-top:16px', text: 'Modifications demandées (' + x.j.modifs.length + ')' }));
      if (!x.j.modifs.length) plus.appendChild(h('p', { class: 'empty', text: 'Aucune.' }));
      x.j.modifs.forEach(function (m) { plus.appendChild(h('div', { class: 'row' }, h('div', null, h('b', { text: m.type }), h('div', { class: 'sub', text: m.description }), h('small', { class: 'sub', text: dt(m.created_at) })), h('button', { type: 'button', class: 'btn sm ghost', text: m.statut === 'faite' ? 'Marquer à faire' : 'Marquer faite', onclick: function () { api('/api/admin/modif-statut', 'POST', { id: m.id, statut: m.statut === 'faite' ? 'demandee' : 'faite' }).then(function () { detail(c.id); }); } }))); });
    });
    main.appendChild(box);
  }
  function detailPieces(id, done) {
    api('/api/admin/compte?id=' + id).then(function (r) {
      if (!r.j.ok) { flash('Compte introuvable.', true); return; }
      var c = r.j.compte, ab = r.j.abonnement, realMain = main, holder = h('div'); main = holder;
      main.textContent = '';
      main.appendChild(head(c.nom, c.email + ' · inscrit le ' + dt(c.created_at), [h('button', { type: 'button', class: 'btn ghost', text: '← Clients', onclick: function () { top(clientsView); } }), h('button', { type: 'button', class: 'btn', text: 'Voir en tant que ce client', onclick: function () { impersonate(c.id); } })]));
      actionsCard(c, r.j.demandes);
      var g = h('div', { class: 'grid g2' });
      var dc = h('div', { class: 'card' }, h('h2', { text: 'Demandes de site (' + r.j.demandes.length + ')' }));
      if (!r.j.demandes.length) dc.appendChild(h('p', { class: 'empty', text: 'Aucune demande.' }));
      r.j.demandes.forEach(function (d) {
        var sl = sel(STATUTS_SITE, d.statut);
        sl.addEventListener('change', function () { api('/api/admin/demande', 'POST', { id: d.id, statut: sl.value }).then(function (x) { flash(x.j.ok ? 'Statut du site mis à jour.' : 'Échec de la mise à jour.', !x.j.ok); if (x.j.ok) loadAll(); }); });
        dc.appendChild(h('div', { class: 'row' }, h('div', null, h('b', { text: d.commerce }), h('div', { class: 'sub', text: [d.ref, lab(d.formule), d.activite, d.ville, d.domaine && ('domaine : ' + d.domaine), d.mails ? d.mails + ' mail(s) pro' : '', d.tel, dt(d.created_at)].filter(Boolean).join(' · ') }), d.message ? h('div', { class: 'sub', text: d.message }) : null), sl));
      });
      g.appendChild(dc);
      var fo = sel(['essentiel', 'pro'], ab ? ab.formule : 'essentiel'), stt = sel(['actif', 'impaye', 'suspendu', 'resilie'], ab ? ab.statut : 'actif');
      var ml = h('input', { type: 'number', min: '0', max: '50', value: ab ? ab.mails_sup : 0 }), mo = h('input', { type: 'text', maxlength: '200', placeholder: 'Motif (si résiliation)', value: ab ? ab.motif || '' : '' });
      g.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Abonnement' }), h('p', { class: 'sub', text: ab ? 'Début : ' + dOnly(ab.debut) + (ab.fin ? ' · fin : ' + dOnly(ab.fin) : '') : 'Aucun abonnement. Créez-le quand le client a accepté et payé.' }),
        h('div', { class: 'form' }, h('label', null, 'Formule', fo), h('label', null, 'Statut', stt), h('label', null, 'Mails pro en plus', ml), h('label', { class: 'wide' }, 'Motif', mo)),
        h('button', { type: 'button', class: 'btn', text: ab ? 'Enregistrer' : 'Créer l’abonnement', onclick: function () { api('/api/admin/abonnement', 'POST', { compte_id: c.id, formule: fo.value, statut: stt.value, mails_sup: ml.value, motif: mo.value }).then(function (x) { flash(x.j.ok ? 'Abonnement enregistré.' : 'Échec de l’enregistrement.', !x.j.ok); if (x.j.ok) loadAll().then(function () { detail(c.id); }); }); } })));
      main.appendChild(g);
      var g2 = h('div', { class: 'grid g2', style: 'margin-top:16px' });
      var pc = h('div', { class: 'card' }, h('h2', { text: 'Plaintes (' + r.j.plaintes.length + ')' }));
      r.j.plaintes.forEach(function (p) {
        var sl = sel(['ouverte', 'en_cours', 'resolue'], p.statut);
        sl.addEventListener('change', function () { api('/api/admin/plainte-statut', 'POST', { id: p.id, statut: sl.value }).then(function (x) { flash(x.j.ok ? 'Plainte mise à jour.' : 'Échec.', !x.j.ok); if (x.j.ok) loadAll(); }); });
        pc.appendChild(h('div', { class: 'row' }, h('div', null, h('b', { text: p.sujet }), h('div', { class: 'sub', text: dt(p.created_at) + (p.resolved_at ? ' · résolue le ' + dt(p.resolved_at) : '') }), p.message ? h('div', { class: 'sub', text: p.message }) : null), sl));
      });
      var sj = h('input', { type: 'text', maxlength: '120', placeholder: 'Sujet' }), ms = h('textarea', { rows: '2', maxlength: '1500', placeholder: 'Détails (facultatif)' });
      pc.appendChild(h('div', { class: 'form' }, h('label', { class: 'wide' }, 'Nouvelle plainte', sj), h('label', { class: 'wide' }, 'Détails', ms)));
      pc.appendChild(h('button', { type: 'button', class: 'btn ghost', text: 'Ajouter la plainte', onclick: function () { if (!sj.value.trim()) { flash('Indiquez un sujet.', true); return; } api('/api/admin/plainte', 'POST', { compte_id: c.id, sujet: sj.value, message: ms.value }).then(function (x) { flash(x.j.ok ? 'Plainte ajoutée.' : 'Échec.', !x.j.ok); if (x.j.ok) loadAll().then(function () { detail(c.id); }); }); } }));
      g2.appendChild(pc);
      g2.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Journal' }), r.j.journal.length ? h('ul', { class: 'log' }, r.j.journal.map(function (j) { return h('li', null, h('time', { text: dt(j.created_at) }), h('b', { text: j.type.replace(/_/g, ' ') }), h('span', { text: j.detail || '' }), j.admin_id ? h('span', { class: 'pill', text: 'admin' }) : null); })) : h('p', { class: 'empty', text: 'Rien pour le moment.' })));
      main.appendChild(g2);
      main = realMain; done(r.j, { acts: holder.children[1], dem: dc, abo: g.children[1], pl: pc, jr: g2.children[1] });
    });
  }
  /* ===== fiche client (page complète, onglets) ===== */
  var TAB = 'apercu';
  var LOGM = {
    inscription: ['Inscription du client', 'users', 'Compte', 'ok'], connexion: ['Connexion à l’espace client', 'key', 'Sécurité', ''],
    mot_de_passe: ['Mot de passe modifié', 'key', 'Sécurité', ''], mot_de_passe_reinit: ['Mot de passe réinitialisé', 'key', 'Sécurité', 'warn'], mot_de_passe_reinit_mail: ['Mail de réinitialisation envoyé', 'msg', 'E-mails', ''],
    admin_impersonation: ['Admin connecté à sa place', 'users', 'Sécurité', 'warn'], admin_fin_impersonation: ['Fin de la connexion admin', 'out', 'Sécurité', ''],
    abonnement_cree: ['Abonnement créé', 'card', 'Compte', 'ok'], abonnement_statut: ['Statut d’abonnement modifié', 'card', 'Compte', 'warn'], changement_formule: ['Changement de formule', 'repeat', 'Compte', ''], resiliation: ['Abonnement résilié', 'alert', 'Compte', 'bad'],
    site_statut: ['Statut du site modifié', 'globe', 'Site', ''], site_url: ['Adresse du site modifiée', 'globe', 'Site', ''], mise_en_ligne: ['Site mis en ligne', 'globe', 'Site', 'ok'],
    edition_site: ['Contenu du site modifié', 'repeat', 'Site', ''], modification: ['Modification demandée', 'repeat', 'Site', ''],
    notification: ['Notification envoyée', 'alert', 'E-mails', ''], communication: ['Message de communication', 'msg', 'E-mails', ''],
    plainte: ['Message envoyé au support', 'msg', 'Compte', 'warn'], plainte_statut: ['Message du support traité', 'check', 'Compte', 'ok']
  };
  var logm = function (t) { return LOGM[t] || [String(t || '').replace(/_/g, ' ').replace(/^./, function (x) { return x.toUpperCase(); }), 'alert', 'Système', '']; };
  var JCAT = function (t) { if (LOGM[t]) return LOGM[t][2]; t = String(t || ''); return /mdp|mot_de_passe|connexion|reset|securite|impersonation/.test(t) ? 'Sécurité' : /mail|notif|communication/.test(t) ? 'E-mails' : /site|modif|demande|mise_en_ligne/.test(t) ? 'Site' : /abonnement|resiliation|formule|compte|inscription|plainte/.test(t) ? 'Compte' : 'Système'; };
  function detail(id, tab) {
    if (tab) TAB = tab; else if (!detail.id || detail.id !== id) TAB = 'apercu'; detail.id = id;
    detailPieces(id, function (R, P) {
      var c = R.compte, ab = R.abonnement, dm = R.demandes, d = dm[0], pl = R.plaintes, jr = R.journal;
      var quota = ab && ab.formule === 'pro' ? 3 : 1;
      var plus = { modifs: [], opt: 0 };
      var live = d && d.statut === 'en_ligne';
      var st = ab ? ab.statut : '', stTxt = ab ? (st === 'actif' ? 'Client actif' : lab(st)) : 'Prospect';
      var ids = comR().map(function (x) { return x.id; }).sort(function (a, b) { return b - a; }), ix = ids.indexOf(c.id);
      var nav = function (dlt) { var t = ids[ix + dlt]; if (t) detail(t, 'apercu'); };
      var ib = function (t, ic, fn, cls) { return h('button', { type: 'button', class: 'btn sm ' + (cls || 'ghost'), onclick: fn }, ico(ic, 16), ' ', t); };
      var clickIn = function (box, txt) { var bs = box.querySelectorAll('button'); for (var i = 0; i < bs.length; i++) if (bs[i].textContent === txt) { bs[i].click(); return true; } return false; };
      var setTab = function (t) { TAB = t; detail(id, t); };
      main.textContent = '';
      /* en-tête */
      main.appendChild(h('div', { class: 'cf-crumb' }, h('a', { href: '#', text: 'Clients', onclick: function (e) { e.preventDefault(); top(clientsView); mark('clients'); } }), h('span', { text: ' › ' }), h('b', { text: c.nom })));
      main.appendChild(h('div', { class: 'cf-head' },
        h('div', { class: 'cf-id' }, h('div', { class: 'cf-name' }, h('h1', { text: c.nom }), h('span', { class: 'pill ' + (pillFor(st) || ''), text: stTxt })),
          h('div', { class: 'cf-meta' }, h('span', null, ico('msg', 15), c.email), d && d.tel ? h('span', null, ico('users', 15), d.tel) : null, h('span', null, ico('repeat', 15), 'Inscrit le ' + dt(c.created_at)), d ? h('span', null, ico('home', 15), d.commerce) : null)),
        h('div', { class: 'cf-act' }, h('button', { type: 'button', class: 'btn sm ghost iconbtn', 'aria-label': 'Client précédent', text: '‹', disabled: ids[ix - 1] ? null : 'disabled', onclick: function () { nav(-1); } }), h('button', { type: 'button', class: 'btn sm ghost iconbtn', 'aria-label': 'Client suivant', text: '›', disabled: ids[ix + 1] ? null : 'disabled', onclick: function () { nav(1); } }),
          ib('Se connecter à sa place', 'users', function () { impersonate(c.id); }), ib('Paramètres', 'key', function () { setTab('param'); }))));
      /* onglets */
      var TABS = [['apercu', 'Aperçu', 'home'], ['site', 'Site', 'globe'], ['suivi', 'Suivi & notes', 'check'], ['abo', 'Abonnement', 'card'], ['modifs', 'Modifications', 'repeat'], ['dem', 'Demandes', 'file'], ['msg', 'Messages', 'msg'], ['fact', 'Factures', 'euro'], ['jr', 'Journal & Logs', 'alert'], ['param', 'Paramètres', 'key']];
      var cnt = { modifs: 0, dem: dm.filter(function (x) { return ['nouvelle', 'en_creation', 'apercu'].indexOf(x.statut) >= 0; }).length, msg: pl.filter(function (x) { return x.statut !== 'resolue'; }).length }, tabs = h('div', { class: 'cf-tabs', role: 'tablist' }), tb = {};
      TABS.forEach(function (t) { var b = h('button', { type: 'button', role: 'tab', 'aria-selected': TAB === t[0] ? 'true' : 'false', onclick: function () { setTab(t[0]); } }, ico(t[2], 17), t[1]); tb[t[0]] = b; if (cnt[t[0]]) b.appendChild(h('span', { class: 'cnt', text: String(cnt[t[0]]) })); tabs.appendChild(b); });
      main.appendChild(tabs);
      setTimeout(function () { var sel = tabs.querySelector('[aria-selected=true]'); if (sel && sel.scrollIntoView) tabs.scrollLeft = Math.max(0, sel.offsetLeft - 40); }, 0);
      var body = h('div', { class: 'cf-body' }); main.appendChild(body);
      var card = function (title, ic, extra, kids, cls) { return h('div', { class: 'card cf-card ' + (cls || '') }, h('div', { class: 'cf-ch' }, h('h2', null, ico(ic, 20), title), extra || null), kids); };
      var kv = function (rows) { return h('dl', { class: 'cf-kv' }, rows.filter(Boolean).map(function (r) { return h('div', null, h('dt', { text: r[0] }), h('dd', null, r[1])); })); };
      var siteCard = function () {
        if (!d) return card('Son site', 'globe', null, h('p', { class: 'empty', text: 'Aucune demande de site.' }));
        var url = d.site_url, pv = url ? h('div', { class: 'cf-pv' }, h('iframe', { src: url, title: 'Aperçu du site', loading: 'lazy', tabindex: '-1' })) : h('div', { class: 'cf-pv nopv', text: 'Pas encore d’adresse de site' });
        return card('Son site', 'globe', null, h('div', { class: 'cf-site' }, pv, h('div', null, h('b', { class: 'cf-dom', text: d.domaine || d.commerce }), h('div', null, pillFor(d.statut) ? h('span', { class: 'pill ' + pillFor(d.statut), text: lab(d.statut) }) : h('span', { class: 'pill', text: lab(d.statut) })),
          kv([['Créé le', dt(d.created_at)], ['Formule', lab(d.formule)], ['Activité', d.activite], ['Ville', d.ville]]),
          h('div', { class: 'tools' }, url ? h('a', { class: 'btn sm', href: url, target: '_blank', rel: 'noopener' }, 'Voir le site ', ico('ext', 14)) : null, h('button', { type: 'button', class: 'btn sm ghost', text: 'Modifier le site', onclick: function () { impersonate(c.id); } })))));
      };
      var aboCard = function () {
        if (!ab) return card('Abonnement', 'card', null, h('div', null, h('p', { class: 'sub', text: 'Aucun abonnement pour le moment.' }), h('button', { type: 'button', class: 'btn sm', text: 'Créer l’abonnement', onclick: function () { setTab('abo'); } })));
        return card('Abonnement', 'card', h('button', { type: 'button', class: 'btn sm ghost', text: 'Gérer', onclick: function () { setTab('abo'); } }), h('div', null, h('div', { class: 'cf-plan' }, h('b', { text: lab(ab.formule) }), h('span', { class: 'pill ' + (pillFor(ab.statut) || ''), text: lab(ab.statut) })), h('div', { class: 'cf-price', text: eur(prixAbo(ab)) + ' HT / mois' }),
          kv([['Début', dOnly(ab.debut)], ab.fin ? ['Fin', dOnly(ab.fin)] : null, ['Mails pro en plus', String(ab.mails_sup || 0)]]), h('button', { type: 'button', class: 'btn sm ghost wide', text: 'Voir les détails de l’abonnement →', onclick: function () { setTab('abo'); } })));
      };
      var infoCard = function () { return card('Informations du client', 'users', null, kv([['Nom complet', c.nom], ['Entreprise', d ? d.commerce : '—'], ['E-mail', c.email], ['Téléphone', d && d.tel || '—'], ['Inscription', dt(c.created_at)], ['Dernière connexion', dt(c.derniere_connexion)], ['Statut du compte', stTxt]])); };
      var quick = function () {
        var q = function (t, ic, cls, fn) { return h('button', { type: 'button', class: 'cf-q ' + (cls || ''), onclick: fn }, ico(ic, 18), t); };
        var setAbo = function (statut, msg) { if (!ab) { flash('Ce client n’a pas d’abonnement.', true); return; } if (!window.confirm(msg)) return; api('/api/admin/abonnement', 'POST', { compte_id: c.id, formule: ab.formule, statut: statut, mails_sup: ab.mails_sup, motif: statut === 'resilie' ? 'Résilié par l’administrateur' : '' }).then(function (x) { flash(x.j.ok ? 'Abonnement mis à jour.' : 'Échec.', !x.j.ok); if (x.j.ok) loadAll().then(function () { detail(c.id, TAB); }); }); };
        return card('Actions rapides', 'alert', null, h('div', { class: 'cf-qs' },
          q('Suspendre le compte', 'alert', 'warn', function () { setAbo('suspendu', 'Suspendre l’abonnement de ' + c.nom + ' ?'); }),
          q('Résilier l’abonnement', 'out', 'bad', function () { setAbo('resilie', 'Résilier l’abonnement de ' + c.nom + ' ?'); }),
          q('Envoyer un e-mail', 'msg', '', function () { COMM.pre = [c.id]; top(commView); mark('com'); }),
          q('Envoyer une notification', 'alert', '', function () { setTab('param'); setTimeout(function () { var a = document.querySelector('.cf-body'); if (a) clickIn(a, 'Envoyer une notification'); }, 50); }),
          q('Réinitialiser le mot de passe', 'key', '', function () { clickIn(P.acts, 'Réinitialiser le mot de passe'); }),
          q('Se connecter à sa place', 'users', '', function () { impersonate(c.id); })));
      };
      var tools = function () {
        var sa = sel(['actif', 'impaye', 'suspendu', 'resilie'], st || 'actif'), ss = d ? sel(STATUTS_SITE, d.statut) : null;
        sa.disabled = !ab; sa.addEventListener('change', function () { api('/api/admin/abonnement', 'POST', { compte_id: c.id, formule: ab.formule, statut: sa.value, mails_sup: ab.mails_sup, motif: sa.value === 'resilie' ? 'Résilié par l’administrateur' : '' }).then(function (x) { flash(x.j.ok ? 'Statut du compte mis à jour.' : 'Échec.', !x.j.ok); if (x.j.ok) loadAll().then(function () { detail(c.id, TAB); }); }); });
        if (ss) ss.addEventListener('change', function () { api('/api/admin/demande', 'POST', { id: d.id, statut: ss.value }).then(function (x) { flash(x.j.ok ? 'Statut du site mis à jour.' : 'Échec.', !x.j.ok); if (x.j.ok) loadAll().then(function () { detail(c.id, TAB); }); }); });
        var sus = d ? h('label', { class: 'cf-sw' }, h('span', { text: 'Suspendre le site' }), h('input', { type: 'checkbox', checked: d.suspendu ? '' : null, onchange: function (e) { api('/api/admin/site', 'POST', { id: d.id, suspendu: e.target.checked }).then(function (x) { flash(x.j.ok ? (e.target.checked ? 'Site suspendu.' : 'Site réactivé.') : 'Échec.', !x.j.ok); if (x.j.ok) loadAll(); }); } })) : null;
        return card('Outils de gestion', 'key', null, h('div', { class: 'cf-tl' }, h('label', null, h('span', { text: 'Statut du compte' }), sa), ss ? h('label', null, h('span', { text: 'Statut du site' }), ss) : null, sus));
      };
      var summary = h('div', { class: 'cf-sum' });
      var summaryCard = function () { return card('Modifications & demandes', 'repeat', null, summary); };
      var jrnl = function (limit) {
        var wrap = h('div'), list = h('div', { class: 'cf-jl' }), cur2 = 'Tout', q = '', chips = h('div', { class: 'chips' }), find = h('input', { type: 'search', class: 'cf-find', placeholder: 'Rechercher dans le journal…', 'aria-label': 'Rechercher dans le journal' });
        var day = function (x) { return String(x || '').slice(0, 10); };
        var draw = function () {
          list.textContent = ''; var rows = jr.filter(function (j) { var m = logm(j.type); return (cur2 === 'Tout' || m[2] === cur2) && (!q || (m[0] + ' ' + (j.detail || '')).toLowerCase().indexOf(q) >= 0); }).slice(0, limit || 200), last = '';
          if (!rows.length) list.appendChild(h('p', { class: 'empty', text: 'Rien pour le moment.' }));
          rows.forEach(function (j) { var m = logm(j.type), dd = day(j.created_at);
            if (!limit && dd !== last) { last = dd; list.appendChild(h('div', { class: 'cf-day', text: dOnly(dd) })); }
            list.appendChild(h('div', { class: 'cf-jr' }, h('span', { class: 'cf-ji ' + m[3] }, ico(m[1], 16)), h('div', { class: 'cf-jt' }, h('b', { text: m[0] }), j.detail ? h('span', { class: 'sub', text: j.detail }) : null), h('span', { class: 'cf-cat', text: m[2] }), h('span', { class: 'cf-by', text: j.admin_id ? 'Admin' : 'Client / système' }), h('time', { text: dt(j.created_at) }))); });
        };
        ['Tout', 'Compte', 'Site', 'Sécurité', 'E-mails', 'Système'].forEach(function (k) { chips.appendChild(h('button', { type: 'button', class: 'chip' + (k === cur2 ? ' on' : ''), text: k, onclick: function () { cur2 = k; Array.prototype.forEach.call(chips.children, function (x) { x.className = 'chip' + (x.textContent === k ? ' on' : ''); }); draw(); } })); });
        find.addEventListener('input', function () { q = find.value.trim().toLowerCase(); draw(); });
        wrap.appendChild(chips); if (!limit) wrap.appendChild(find); wrap.appendChild(list); draw(); return wrap;
      };
      var activity = function () {
        var items = jr.slice(0, 4); return card('Dernière activité', 'trend', null, items.length ? h('div', { class: 'cf-tline' }, items.map(function (j) { return h('div', null, h('i'), h('div', null, h('b', { text: logm(j.type)[0] }), h('span', { class: 'sub', text: j.detail || '' }), h('time', { text: dt(j.created_at) }))); })) : h('p', { class: 'empty', text: 'Aucune activité.' }));
      };
      var facs = function () {
        var out = [], k = ab && ab.debut ? ab.debut : null; if (!k) return out;
        var y = +k.slice(0, 4), m = +k.slice(5, 7), day = k.slice(8, 10) || '01', now = new Date().toISOString().slice(0, 10), fin = ab.fin ? ab.fin.slice(0, 7) : now.slice(0, 7);
        for (var n = 0; n < 60; n++) { var key = y + '-' + (m < 10 ? '0' : '') + m; if (key > fin || key + '-' + day > now) break; var ht = prixAbo(ab); out.push([key, 'F-' + y + (m < 10 ? '0' : '') + m + '-' + String(c.id).padStart(4, '0'), day + '/' + (m < 10 ? '0' : '') + m + '/' + y, ht, Math.round(ht * 120) / 100]); m++; if (m > 12) { m = 1; y++; } }
        return out.reverse();
      };
      /* contenu par onglet */
      var show = {
        apercu: function () { body.appendChild(h('div', { class: 'cf-g3' }, infoCard(), siteCard(), aboCard())); body.appendChild(h('div', { class: 'cf-g3' }, quick(), tools(), summaryCard())); body.appendChild(h('div', { class: 'cf-g2' }, card('Journal & Logs', 'alert', h('button', { type: 'button', class: 'btn sm ghost', text: 'Tout voir', onclick: function () { setTab('jr'); } }), jrnl(5)), activity())); },
        site: function () { body.appendChild(siteCard()); body.appendChild(P.dem); },
        suivi: function () { suiviTab(body, c, d, card, setTab); },
        abo: function () { body.appendChild(h('div', { class: 'cf-g2' }, aboCard(), P.abo)); },
        modifs: function () { var box = card('Modifications demandées', 'repeat', null, h('div', { class: 'cf-ml' })); body.appendChild(box); api('/api/admin/compte-plus?id=' + c.id).then(function (x) { var l = box.querySelector('.cf-ml'); if (!x.j.ok) return; if (!x.j.modifs.length) l.appendChild(h('p', { class: 'empty', text: 'Aucune modification demandée.' })); x.j.modifs.forEach(function (m) { l.appendChild(h('div', { class: 'row' }, h('div', null, h('b', { text: m.type }), h('div', { class: 'sub', text: m.description }), h('small', { class: 'sub', text: dt(m.created_at) })), h('button', { type: 'button', class: 'btn sm ghost', text: m.statut === 'faite' ? 'Marquer à faire' : 'Marquer faite', onclick: function () { api('/api/admin/modif-statut', 'POST', { id: m.id, statut: m.statut === 'faite' ? 'demandee' : 'faite' }).then(function () { detail(c.id, 'modifs'); }); } }))); }); }); },
        dem: function () { body.appendChild(P.dem); },
        msg: function () { body.appendChild(P.pl); },
        fact: function () { var l = facs(); body.appendChild(card('Factures', 'euro', null, l.length ? h('div', { class: 'tablewrap' }, h('table', null, h('thead', null, h('tr', null, ['Facture', 'Date', 'Total HT', 'Total TTC', 'Statut', ''].map(function (x) { return h('th', { text: x }); }))), h('tbody', null, l.map(function (f) { return h('tr', null, h('td', null, h('b', { text: f[1] })), h('td', { text: f[2] }), h('td', { text: eur(f[3]) }), h('td', { text: eur(f[4]) }), h('td', null, h('span', { class: 'pill ' + (f[0] === l[0][0] && st === 'impaye' ? 'bad' : 'ok'), text: f[0] === l[0][0] && st === 'impaye' ? 'À régler' : 'Payée' })), h('td', null, h('button', { type: 'button', class: 'btn sm', text: 'Voir / PDF', onclick: function () { factureView(c, d, ab, f, l[0][0] === f[0] && st === 'impaye'); } }))); })))) : h('p', { class: 'empty', text: 'Aucune facture : l’abonnement n’a pas encore commencé.' }))); },
        jr: function () { body.appendChild(card('Journal & Logs', 'alert', null, jrnl(0))); },
        param: function () { body.appendChild(P.acts); }
      };
      (show[TAB] || show.apercu)();
      /* données asynchrones : résumé modifications, compteur d'onglet */
      api('/api/admin/compte-plus?id=' + c.id).then(function (x) {
        if (!x.j.ok) return; var ms = x.j.modifs, mois = new Date().toISOString().slice(0, 7), used = ms.filter(function (m) { return String(m.created_at).slice(0, 7) === mois; }).length, nl = pl.filter(function (p) { return p.statut !== 'resolue'; }).length;
        var b = tb.modifs; if (ms.length && b && !b.querySelector('.cnt')) b.appendChild(h('span', { class: 'cnt', text: String(ms.length) }));
        var row = function (ic, t, right, fn) { return h('button', { type: 'button', class: 'cf-sr', onclick: fn }, ico(ic, 18), h('span', { text: t }), right, h('em', { text: '›' })); };
        var bars = h('div', { class: 'cf-bars' }); for (var i = 0; i < quota; i++) bars.appendChild(h('i', { class: i < used ? 'on' : '' }));
        summary.appendChild(row('repeat', 'Modifications (' + used + ' / ' + quota + ')', bars, function () { setTab('modifs'); }));
        summary.appendChild(row('file', 'Demandes de site (' + dm.length + ')', d ? h('span', { class: 'pill ' + (pillFor(d.statut) || ''), text: lab(d.statut) }) : null, function () { setTab('dem'); }));
        summary.appendChild(row('msg', 'Messages (' + pl.length + ')', nl ? h('span', { class: 'pill bad', text: nl + ' non résolu' + (nl > 1 ? 's' : '') }) : null, function () { setTab('msg'); }));
      });
    });
  }
  var LOGO = '<svg width="54" height="54" viewBox="0 0 64 64" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M8 20 12 8h40l4 12"/><path d="M8 20a6 6 0 0 0 12 0 6 6 0 0 0 12 0 6 6 0 0 0 12 0 6 6 0 0 0 12 0"/><path d="M12 33v23h40V33"/><path d="M26 56V42h12v14"/><path d="M41 38l11 4.5-4.6 1.8-1.8 4.7z" fill="#17C26E" stroke="#17C26E" stroke-width="1.5"/></svg>';
  function factureView(c, d, ab, f, due) {
    var esc = function (t) { return String(t == null ? '' : t).replace(/[&<>"]/g, function (x) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[x]; }); };
    var fe = function (n) { return (Math.round(n * 100) / 100).toLocaleString('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' €'; };
    var MO = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'], mi = +f[0].slice(5, 7), per = MO[mi - 1].charAt(0).toUpperCase() + MO[mi - 1].slice(1) + ' ' + f[0].slice(0, 4);
    var base = ab.formule === 'pro' ? ['Abonnement Pro', 'Site web + nom de domaine + adresse mail pro · ' + per, 100] : ['Abonnement Essentiel', 'Site web + nom de domaine · ' + per, 60];
    var rows = '<tr><td><b>' + esc(base[0]) + '</b><small>' + esc(base[1]) + '</small></td><td class="n">1</td><td class="n">' + fe(base[2]) + '</td><td class="n">20 %</td><td class="n">' + fe(base[2]) + '</td></tr>';
    if (ab.mails_sup > 0) rows += '<tr><td><b>Adresses mail pro supplémentaires</b><small>Adresses en plus de celle incluse</small></td><td class="n">' + ab.mails_sup + '</td><td class="n">' + fe(4) + '</td><td class="n">20 %</td><td class="n">' + fe(4 * ab.mails_sup) + '</td></tr>';
    var ht = f[3], tva = Math.round(ht * 20) / 100;
    var html = '<div class="inv-ex">EXEMPLE DE FACTURE · informations de l’entreprise à compléter</div><div class="inv-top"><div class="inv-brand">' + LOGO + '<div><b>Devanture <em>Web</em></b><small>Site vitrine pour commerçants</small></div></div><div class="inv-ft"><h1>FACTURE</h1><p>N° ' + esc(f[1]) + '</p><p><span class="inv-badge' + (due ? ' warn' : '') + '">' + (due ? 'À régler' : 'Payée') + '</span></p></div></div>' +
      '<div class="inv-meta"><div><span>Date d’émission</span><b>' + esc(f[2]) + '</b></div><div><span>Échéance</span><b>' + esc(f[2]) + '</b></div><div><span>Période</span><b>' + esc(per) + '</b></div><div><span>Mode de paiement</span><b>Prélèvement SEPA</b></div></div>' +
      '<div class="inv-parties"><div><h2>Émetteur</h2><b>Devanture Web</b><p>[Raison sociale à compléter]</p><p>[Adresse à compléter]</p><p>SIRET : [à compléter]</p><p>N° TVA : [FR… à compléter]</p></div><div><h2>Facturé à</h2><b>' + esc(d ? d.commerce : c.nom) + '</b><p>' + esc(c.nom) + '</p><p>' + esc(d ? d.ville : '') + '</p><p>' + esc(c.email) + '</p></div></div>' +
      '<table class="inv-t"><thead><tr><th>Désignation</th><th class="n">Qté</th><th class="n">Prix unitaire HT</th><th class="n">TVA</th><th class="n">Total HT</th></tr></thead><tbody>' + rows + '</tbody></table>' +
      '<div class="inv-tot"><div><span>Total HT</span><b>' + fe(ht) + '</b></div><div><span>TVA 20 %</span><b>' + fe(tva) + '</b></div><div class="g"><span>Total TTC</span><span>' + fe(ht + tva) + '</span></div></div>' +
      '<div class="inv-legal"><b>Pénalités de retard :</b> 3 fois le taux d’intérêt légal. <b>Indemnité forfaitaire de recouvrement :</b> 40 €. <b>Escompte :</b> aucun pour paiement anticipé. Abonnement mensuel, engagement de 12 mois.</div>';
    main.textContent = '';
    main.appendChild(head('Facture ' + f[1], c.nom + ' · ' + per, [h('button', { type: 'button', class: 'btn ghost', text: '← Factures du client', onclick: function () { detail(c.id, 'fact'); } }), h('button', { type: 'button', class: 'btn', text: '⬇ Télécharger en PDF', onclick: function () { window.print(); } })]));
    var box = h('div', { class: 'invoice' }); box.innerHTML = html; main.appendChild(box); window.scrollTo(0, 0);
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
  function sel(opts, val) { var e = h('select'); opts.forEach(function (o) { var op = h('option', { value: o, text: lab(o) }); if (o === val) op.selected = true; e.appendChild(op); }); return e; }
  function head(title, sub, extra) { return h('div', { class: 'top' }, h('div', { class: 'hello' }, h('h1', { text: title }), sub ? h('p', { text: sub }) : null), h('div', { class: 'tools' }, extra || [])); }

  /* ===== données, navigation ===== */
  var PRIX = { essentiel: 60, pro: 100 }, MAILP = 4;
  var Sx = null, D = null, IX = null, cur = null, par = null;
  var prixAbo = function (a) { return (PRIX[a.formule] || 0) + MAILP * (a.mails_sup || 0); };
  var counts = function (a) { return a.statut === 'actif' || a.statut === 'impaye'; };
  /* comptes de démonstration : exclus des chiffres par défaut */
  var DEMO = { on: true };
  var keepId = function (id) { var c = IX && IX.c[id]; return DEMO.on || !(c && c.demo); };
  var abosR = function () { return D.abonnements.filter(function (a) { return keepId(a.compte_id); }); };
  var demR = function () { return D.demandes.filter(function (x) { return keepId(x.compte_id); }); };
  var plR = function () { return D.plaintes.filter(function (x) { return keepId(x.compte_id); }); };
  var comR = function () { return D.comptes.filter(function (c) { return DEMO.on || !c.demo; }); };
  var d10 = function (x) { return x ? String(x).slice(0, 10) : ''; };
  var ago = function (n) { return new Date(Date.now() - n * 864e5).toISOString().slice(0, 10); };
  function loadAll() {
    return Promise.all([api('/api/admin/stats'), api('/api/admin/donnees')]).then(function (r) {
      if (!r[0].j.ok || !r[1].j.ok) throw new Error('chargement');
      Sx = r[0].j; D = r[1].j; IX = { c: {}, abo: {}, dem: {}, pl: {} };
      D.comptes.forEach(function (c) { IX.c[c.id] = c; });
      D.abonnements.forEach(function (a) { IX.abo[a.compte_id] = a; });
      D.demandes.forEach(function (d) { (IX.dem[d.compte_id] = IX.dem[d.compte_id] || []).push(d); });
      D.plaintes.forEach(function (p) { (IX.pl[p.compte_id] = IX.pl[p.compte_id] || []).push(p); });
    });
  }
  function top(fn) { par = null; cur = fn; fn(); window.scrollTo(0, 0); }
  function open(fn) { par = cur; cur = fn; fn(); window.scrollTo(0, 0); }
  function backBtn() { return par ? h('button', { type: 'button', class: 'btn ghost', text: '← Retour', onclick: function () { var f = par; par = null; cur = f; f(); window.scrollTo(0, 0); } }) : null; }
  function click(node, fn) { node.classList.add('click'); node.setAttribute('role', 'button'); node.setAttribute('tabindex', '0'); node.addEventListener('click', fn); node.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fn(); } }); return node; }

  /* ===== lignes de données et colonnes ===== */
  var who = function (r) { return (IX && IX.c[r.compte_id]) || {}; };
  function cRow(c) {
    var a = IX.abo[c.id], ds = IX.dem[c.id] || [], d = ds[0], ps = IX.pl[c.id] || [];
    return { compte_id: c.id, optout: c.opt_out, demo: c.demo, nom: c.nom, email: c.email, inscrit: c.created_at, connexion: c.derniere_connexion, formule: a ? a.formule : '', abo: a ? a.statut : '', debut: a ? a.debut : '', fin: a ? a.fin : '', mails: a ? a.mails_sup : 0, prix: a && counts(a) ? prixAbo(a) : 0, site: d ? d.statut : '', commerce: d ? d.commerce : '', ville: d ? d.ville : '', activite: d ? d.activite : '', domaine: d ? d.domaine : '', tel: d ? d.tel : '', demandes: ds.length, plaintes: ps.length, plaintes_ouvertes: ps.filter(function (p) { return p.statut !== 'resolue'; }).length };
  }
  function aRow(a) { var c = IX.c[a.compte_id] || {}; return { compte_id: a.compte_id, nom: c.nom, email: c.email, formule: a.formule, abo: a.statut, debut: a.debut, fin: a.fin, mails: a.mails_sup, prix: counts(a) ? prixAbo(a) : 0, motif: a.motif || '' }; }
  function dRow(d) { var c = IX.c[d.compte_id] || {}; return { compte_id: d.compte_id, nom: c.nom, email: c.email, ref: d.ref, commerce: d.commerce, activite: d.activite, ville: d.ville, domaine: d.domaine, mails: d.mails, tel: d.tel, formule: d.formule, site: d.statut, date: d.created_at, source: srcOf(d) }; }
  function pRow(p) { var c = IX.c[p.compte_id] || {}; return { compte_id: p.compte_id, nom: c.nom, email: c.email, sujet: p.sujet, message: p.message, pl: p.statut, date: p.created_at, resolue: p.resolved_at }; }
  function jRow(j) { var c = IX.c[j.compte_id] || {}; return { compte_id: j.compte_id, nom: c.nom || '—', email: c.email || '', type: j.type.replace(/_/g, ' '), detail: j.detail, date: j.created_at }; }
  function srcOf(d) { try { var u = JSON.parse(d.utm || '{}'); return u.utm_source || u.ref || 'direct'; } catch (_) { return 'direct'; } }
  var C = function (k, l, t) { return { k: k, l: l, t: t || 'text' }; };
  var COLS = {
    clients: [C('nom', 'Nom', 'who'), C('email', 'E-mail'), C('inscrit', 'Inscrit le', 'date'), C('connexion', 'Dernière connexion', 'date'), C('commerce', 'Commerce'), C('activite', 'Activité'), C('ville', 'Ville'), C('tel', 'Téléphone'), C('domaine', 'Domaine'), C('site', 'Statut du site', 'site'), C('formule', 'Formule', 'formule'), C('abo', 'Abonnement', 'abo'), C('debut', 'Début abonnement', 'day'), C('fin', 'Fin abonnement', 'day'), C('mails', 'Mails pro en plus', 'int'), C('prix', 'Facturé par mois (HT)', 'eur'), C('demandes', 'Demandes', 'int'), C('plaintes', 'Plaintes', 'int'), C('plaintes_ouvertes', 'Plaintes ouvertes', 'int')],
    abonnements: [C('nom', 'Client', 'who'), C('email', 'E-mail'), C('formule', 'Formule', 'formule'), C('abo', 'Statut', 'abo'), C('debut', 'Début', 'day'), C('fin', 'Fin', 'day'), C('mails', 'Mails pro en plus', 'int'), C('prix', 'Prix par mois (HT)', 'eur'), C('motif', 'Motif de résiliation')],
    demandes: [C('commerce', 'Commerce'), C('nom', 'Client', 'who'), C('email', 'E-mail'), C('ref', 'Référence'), C('activite', 'Activité'), C('ville', 'Ville'), C('domaine', 'Domaine'), C('mails', 'Mails pro demandés', 'int'), C('tel', 'Téléphone'), C('formule', 'Formule', 'formule'), C('site', 'Statut', 'site'), C('source', 'Provenance'), C('date', 'Date', 'date')],
    plaintes: [C('nom', 'Client', 'who'), C('email', 'E-mail'), C('sujet', 'Sujet'), C('message', 'Détails'), C('pl', 'Statut', 'pl'), C('date', 'Date', 'date'), C('resolue', 'Résolue le', 'date')],
    journal: [C('date', 'Date', 'date'), C('type', 'Événement'), C('nom', 'Client', 'who'), C('email', 'E-mail'), C('detail', 'Détail')]
  };
  var DS = {
    clients: { l: 'Clients', rows: function () { return D.comptes.map(cRow); }, date: 'inscrit', filt: [['formule', 'Formule', ['essentiel', 'pro']], ['abo', 'Abonnement', ['actif', 'impaye', 'suspendu', 'resilie']], ['site', 'Statut du site', ['nouvelle', 'en_creation', 'apercu', 'en_ligne', 'abandonnee']]] },
    abonnements: { l: 'Abonnements', rows: function () { return abosR().map(aRow); }, date: 'debut', filt: [['formule', 'Formule', ['essentiel', 'pro']], ['abo', 'Statut', ['actif', 'impaye', 'suspendu', 'resilie']], ['mails', 'Mails pro en plus', ['oui', 'non']]] },
    demandes: { l: 'Demandes de site', rows: function () { return demR().map(dRow); }, date: 'date', filt: [['formule', 'Formule', ['essentiel', 'pro']], ['site', 'Statut', ['nouvelle', 'en_creation', 'apercu', 'en_ligne', 'abandonnee']], ['activite', 'Activité', 'auto'], ['ville', 'Ville', 'auto'], ['mails', 'Mails pro demandés', ['oui', 'non']]] },
    plaintes: { l: 'Plaintes', rows: function () { return plR().map(pRow); }, date: 'date', filt: [['pl', 'Statut', ['ouverte', 'en_cours', 'resolue']]] },
    journal: { l: 'Journal d’activité', rows: function () { return D.journal.map(jRow); }, date: 'date', filt: [] }
  };
  function cell(col, r) {
    var v = r[col.k];
    switch (col.t) {
      case 'who': return h('div', { class: 'who' }, h('div', { class: 'av', text: initials(r.nom) }), h('div', null, h('b', { text: r.nom || '—' }), r.email ? h('small', { text: r.email }) : null));
      case 'date': return document.createTextNode(dt(v));
      case 'day': return document.createTextNode(dOnly(v));
      case 'eur': return document.createTextNode(v ? eur(v) : '—');
      case 'int': return document.createTextNode(String(v || 0));
      case 'site': case 'abo': case 'pl': return v ? pillFor(v) : h('span', { class: 'pill', text: col.k === 'site' ? 'Aucune demande' : 'Aucun' });
      case 'formule': return v ? h('span', { class: 'pill pri', text: lab(v) }) : document.createTextNode('—');
      default: return document.createTextNode(v == null || v === '' ? '—' : String(v));
    }
  }
  function exval(col, r) {
    var v = r[col.k];
    if (v == null) return '';
    if (col.t === 'site' || col.t === 'abo' || col.t === 'pl' || col.t === 'formule') return v ? lab(v) : '';
    if (col.t === 'date' || col.t === 'day') return d10(v);
    return String(v);
  }
  function initials(n) { return (n || '?').trim().split(/\s+/).slice(0, 2).map(function (x) { return x[0]; }).join('').toUpperCase(); }

  /* ===== export CSV ===== */
  function csvText(cols, rows) {
    var esc = function (v) { v = String(v == null ? '' : v); if (/^[=+\-@\t\r]/.test(v)) v = "'" + v; return /[";\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
    var out = [cols.map(function (c) { return esc(c.l); }).join(';')];
    rows.forEach(function (r) { out.push(cols.map(function (c) { return esc(c.ex ? c.ex(r) : exval(c, r)); }).join(';')); });
    return '﻿' + out.join('\r\n');
  }
  function download(name, text) {
    var a = document.createElement('a'), u = URL.createObjectURL(new Blob([text], { type: 'text/csv;charset=utf-8' }));
    a.href = u; a.download = name; document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(u); a.remove(); }, 500);
  }
  var stamp = function () { return new Date().toISOString().slice(0, 10); };

  /* ===== briques graphiques ===== */
  function hero(color, icon, value, label, badge, down, fn) { var n = h('div', { class: 'card hero' }, h('div', { class: 'ic ' + color }, ico(icon, 22)), h('div', null, h('b', { text: value }), h('span', { text: label }), badge ? h('em', { class: down ? 'dn' : '', text: badge }) : null), h('span', { class: 'more', text: 'Détails →' })); return fn ? click(n, fn) : n; }
  function mini(items) { return h('div', { class: 'mini' }, items.map(function (i) { var n = h('div', null, h('b', { text: i[1] }), h('span', { text: i[0] })); return i[2] ? click(n, i[2]) : n; })); }
  function area(jours) {
    var map = {}; jours.forEach(function (j) { map[j.d] = j.n; });
    var days = [], now = new Date(), i;
    for (i = 29; i >= 0; i--) days.push(new Date(now.getTime() - i * 864e5).toISOString().slice(0, 10));
    var vals = days.map(function (d) { return map[d] || 0; }), max = Math.max.apply(null, vals.concat([3]));
    var W = 640, H = 190, L = 28, B = 24, T = 10, iw = W - L - 6, ih = H - B - T;
    var X = function (k) { return L + (iw * k) / 29; }, Y = function (v) { return T + ih - (ih * v) / max; };
    var svg = s('svg', { class: 'chart', viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Inscriptions des 30 derniers jours' });
    svg.appendChild(s('defs', null, (function () { var g = s('linearGradient', { id: 'ga', x1: 0, y1: 0, x2: 0, y2: 1 }); g.appendChild(s('stop', { offset: '0%', 'stop-color': COL.pri, 'stop-opacity': '.35' })); g.appendChild(s('stop', { offset: '100%', 'stop-color': COL.pri, 'stop-opacity': '0' })); return g; })()));
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
    var tot = parts.reduce(function (a, p) { return a + p.n; }, 0), R = 52, Cc = 2 * Math.PI * R, off = 0;
    var svg = s('svg', { viewBox: '0 0 140 140', role: 'img', 'aria-label': centerSub });
    svg.appendChild(s('circle', { cx: 70, cy: 70, r: R, fill: 'none', stroke: 'var(--soft)', 'stroke-width': 18 }));
    if (tot) parts.forEach(function (p) { if (!p.n) return; var len = (p.n / tot) * Cc; svg.appendChild(s('circle', { cx: 70, cy: 70, r: R, fill: 'none', stroke: p.c, 'stroke-width': 18, 'stroke-dasharray': len + ' ' + (Cc - len), 'stroke-dashoffset': -off, transform: 'rotate(-90 70 70)' })); off += len; });
    var t1 = s('text', { x: 70, y: 70, 'text-anchor': 'middle', style: "font:800 24px 'Plus Jakarta Sans',system-ui,sans-serif;fill:var(--ink)" }); t1.textContent = centerTop; svg.appendChild(t1);
    var t2 = s('text', { x: 70, y: 87, 'text-anchor': 'middle', style: "font:600 10px 'Plus Jakarta Sans',system-ui,sans-serif;fill:var(--mut)" }); t2.textContent = centerSub; svg.appendChild(t2);
    return h('div', { class: 'donutwrap' }, svg, h('ul', { class: 'legend' }, parts.map(function (p) { var li = h('li', null, h('i', { style: 'background:' + p.c }), p.l, h('b', { text: p.n })); return p.fn ? click(li, p.fn) : li; })));
  }
  function bars(rows, empty) {
    var mx = Math.max.apply(null, rows.map(function (r) { return r.n; }).concat([1]));
    if (!rows.length) return h('p', { class: 'empty', text: empty || 'Pas encore de données.' });
    return h('ul', { class: 'bars' }, rows.map(function (r) { var li = h('li', null, h('span', { text: r.l }), h('b', { text: r.n }), h('div', { class: 't' }, h('u', { style: 'width:' + Math.max(4, Math.round((r.n / mx) * 100)) + '%' }))); return r.fn ? click(li, r.fn) : li; }));
  }
  function funnel(steps) {
    var mx = Math.max.apply(null, steps.map(function (x) { return x.n; }).concat([1]));
    return h('div', { class: 'funnel' }, steps.map(function (x) { var n = h('div', null, h('span', { text: x.l }), h('div', { class: 'bar' }, h('u', { style: 'width:' + Math.max(8, Math.round((x.n / mx) * 100)) + '%;background:' + x.c, text: num(x.n) })), h('b', { text: x.p == null ? '' : x.p + ' %' })); return x.fn ? click(n, x.fn) : n; }));
  }
  function card(title, sub, body, fn) { var n = h('div', { class: 'card' }, h('h3', { text: title }), sub ? h('p', { class: 'sub', text: sub }) : null, body); return n; }

  /* ===== listes détaillées (clic sur une carte) ===== */
  function listView(dsKey, title, sub, pred, extra, isTop) {
    (isTop ? top : open)(function () {
      main.textContent = '';
      var rows = DS[dsKey].rows().filter(pred || function () { return true; });
      main.appendChild(head(title, sub || (rows.length + ' résultat(s)'), [backBtn(), h('button', { type: 'button', class: 'btn', text: '⬇ Exporter (CSV)', onclick: function () { download(dsKey + '-' + stamp() + '.csv', csvText(COLS[dsKey], rows)); flash('Export téléchargé : ' + rows.length + ' ligne(s).'); } })]));
      if (extra) main.appendChild(extra(rows));
      main.appendChild(dataTable(dsKey, rows));
    });
  }
  function dataTable(dsKey, rows) {
    var cols = COLS[dsKey].filter(function (c) { return c.k !== 'email' || dsKey === 'journal' && false; });
    var shown = { clients: ['nom', 'inscrit', 'connexion', 'site', 'formule', 'abo', 'plaintes_ouvertes'], abonnements: ['nom', 'formule', 'abo', 'debut', 'fin', 'mails', 'prix', 'motif'], demandes: ['commerce', 'nom', 'activite', 'ville', 'formule', 'site', 'date'], plaintes: ['nom', 'sujet', 'pl', 'date', 'resolue'], journal: ['date', 'type', 'nom', 'detail'] }[dsKey];
    cols = COLS[dsKey].filter(function (c) { return shown.indexOf(c.k) >= 0; });
    var box = h('input', { class: 'find', type: 'search', placeholder: 'Rechercher dans ce tableau…', 'aria-label': 'Rechercher' }), body = h('div', { class: 'tablewrap' }), count = h('span', { class: 'sub' });
    var FK = { formule: 'formule', abo: 'abo', site: 'site', pl: 'pl', activite: 'activite', ville: 'ville', mails: 'mails' }, OT = { oui: 'Oui', non: 'Non' }, filt = (DS[dsKey].filt || []).filter(function (f) { return FK[f[0]]; }), sel = {};
    var badge = h('span', { class: 'bdg', hidden: '' }), fbtn = h('button', { type: 'button', class: 'btn ghost iconbtn', 'aria-label': 'Filtrer', 'aria-expanded': 'false', title: 'Filtrer' }, ico('filter', 18), badge);
    var panel = h('div', { class: 'fpanel', hidden: '' }, h('div', { class: 'fgrid' }, filt.map(function (f) {
      var sl = h('select', { 'aria-label': f[1] }, h('option', { value: '', text: f[1] + ' : toutes' }), (f[2] === 'auto' ? distinct(rows, f[0]).map(function (x) { return x[0]; }) : f[2]).map(function (o) { return h('option', { value: o, text: OT[o] || lab(o) }); }));
      sl.addEventListener('change', function () { sel[f[0]] = sl.value; draw(); });
      return h('label', null, f[1], sl);
    })));
    if (filt.length) fbtn.addEventListener('click', function () { var o = panel.hidden; panel.hidden = !o; fbtn.setAttribute('aria-expanded', String(o)); });
    function draw() {
      var q = box.value.trim().toLowerCase(), nf = Object.keys(sel).filter(function (k) { return sel[k]; }).length; badge.textContent = nf ? String(nf) : ''; badge.hidden = !nf;
      var list = rows.filter(function (r) { if (q && JSON.stringify(r).toLowerCase().indexOf(q) < 0) return false; return filt.every(function (f) { if (!sel[f[0]]) return true; if (f[0] === 'mails') return (r.mails > 0) === (sel.mails === 'oui'); return String(r[FK[f[0]]] || '').trim() === sel[f[0]]; }); });
      count.textContent = list.length + ' ligne(s)'; body.textContent = '';
      if (!list.length) { body.appendChild(h('p', { class: 'empty', text: 'Rien à afficher pour le moment.' })); return; }
      var tb = h('tbody');
      list.slice(0, 500).forEach(function (r) {
        var tr = h('tr', null, cols.map(function (c) { return h('td', null, cell(c, r)); }));
        if (r.compte_id) { click(tr, function () { open(function () { detail(r.compte_id); }); }); tr.setAttribute('title', 'Ouvrir la fiche client'); }
        tb.appendChild(tr);
      });
      body.appendChild(h('table', null, h('thead', null, h('tr', null, cols.map(function (c) { return h('th', { text: c.l }); }))), tb));
    }
    box.addEventListener('input', draw); draw();
    return h('div', { class: 'card' }, h('div', { class: 'tbar' }, filt.length ? fbtn : null, box, count), filt.length ? panel : null, body);
  }
  var L = {
    comptes: function (t, p, sub) { listView('clients', t, sub, p); },
    demandes: function (t, p, sub) { listView('demandes', t, sub, p); },
    abos: function (t, p, sub) { listView('abonnements', t, sub, p); },
    plaintes: function (t, p, sub) { listView('plaintes', t, sub, p); },
    journal: function (t, p, sub) { listView('journal', t, sub, p); }
  };
  var recent = function (k, n) { return function (r) { return d10(r[k]) >= ago(n); }; };

  /* ===== revenus par période ===== */
  var REV = { mode: 'mois', depuis: '6' };
  var mKey = function (d) { return d.slice(0, 7); };
  function revCalc() {
    var nowM = mKey(new Date().toISOString()), abos = abosR();
    var first = abos.reduce(function (m, a) { var k = mKey(d10(a.debut) || d10(a.created_at) || nowM); return k < m ? k : m; }, nowM);
    var start;
    if (REV.depuis === 'tout') start = first; else { var d = new Date(); d.setUTCDate(1); d.setUTCMonth(d.getUTCMonth() - (parseInt(REV.depuis, 10) - 1)); start = mKey(d.toISOString()); }
    var months = [], y = +start.slice(0, 4), m = +start.slice(5, 7);
    for (;;) { var k = y + '-' + (m < 10 ? '0' : '') + m; months.push(k); if (k >= nowM) break; m++; if (m > 12) { m = 1; y++; } }
    var info = months.map(function (k) { return { k: k, ess: 0, pro: 0, mails: 0, nouveaux: 0, resilies: 0, actifs: 0, impayes: 0, abos: [] }; });
    var byK = {}; info.forEach(function (x) { byK[x.k] = x; });
    abos.forEach(function (a) {
      var ds = d10(a.debut) || d10(a.created_at), fin = d10(a.fin), kS = mKey(ds), kF = fin ? mKey(fin) : null;
      if (byK[kS]) byK[kS].nouveaux++;
      if (a.statut === 'resilie' && kF && byK[kF]) byK[kF].resilies++;
      if (a.statut === 'suspendu') return;
      info.forEach(function (x) {
        if (x.k < kS || (kF && x.k > kF)) return;
        x[a.formule === 'pro' ? 'pro' : 'ess'] += PRIX[a.formule] || 0; x.mails += MAILP * (a.mails_sup || 0); x.actifs++; x.abos.push(a);
        if (a.statut === 'impaye' && x.k === nowM) x.impayes += prixAbo(a);
      });
    });
    var groups = {}, order = [];
    info.forEach(function (x) {
      var y2 = x.k.slice(0, 4), q = Math.ceil(+x.k.slice(5, 7) / 3), key = REV.mode === 'annee' ? y2 : REV.mode === 'trimestre' ? y2 + ' T' + q : x.k;
      var lbl = REV.mode === 'mois' ? new Date(x.k + '-15').toLocaleDateString('fr-FR', { month: 'short', year: 'numeric' }) : key;
      var g = groups[key]; if (!g) { g = groups[key] = { periode: lbl, ess: 0, pro: 0, mails: 0, nouveaux: 0, resilies: 0, actifs: 0, impayes: 0, abos: [] }; order.push(key); }
      g.ess += x.ess; g.pro += x.pro; g.mails += x.mails; g.nouveaux += x.nouveaux; g.resilies += x.resilies; g.actifs = x.actifs; g.impayes += x.impayes;
      x.abos.forEach(function (a) { if (g.abos.indexOf(a) < 0) g.abos.push(a); });
    });
    return order.map(function (k) { var g = groups[k]; g.ca = g.ess + g.pro + g.mails; return g; });
  }
  var REVCOLS = [C('periode', 'Période'), C('ca', 'Facturé', 'eur'), C('ess', 'Essentiel', 'eur'), C('pro', 'Pro', 'eur'), C('mails', 'Mails pro', 'eur'), C('nouveaux', 'Nouveaux', 'int'), C('resilies', 'Partis', 'int'), C('actifs', 'Clients', 'int'), C('impayes', 'Impayés', 'eur')];
  function revBars(rows) {
    var W = 640, H = 210, Lm = 46, B = 28, T = 10, iw = W - Lm - 8, ih = H - B - T;
    var max = Math.max.apply(null, rows.map(function (r) { return r.ca; }).concat([100])), step = Math.pow(10, Math.floor(Math.log10(max))), top = Math.ceil(max / step) * step;
    var svg = s('svg', { class: 'chart', viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Chiffre d’affaires par période' });
    [0, 1, 2, 3].forEach(function (k) { var y = T + (ih * k) / 3; svg.appendChild(s('line', { x1: Lm, x2: W - 8, y1: y, y2: y, class: 'gl', 'stroke-dasharray': '3 4' })); var t = s('text', { x: 0, y: y + 3 }); t.textContent = Math.round(top - (top * k) / 3).toLocaleString('fr-FR') + ' €'; svg.appendChild(t); });
    var bw = iw / rows.length, pw = Math.min(46, bw * 0.62);
    rows.forEach(function (r, i) {
      var x = Lm + bw * i + (bw - pw) / 2, y = T + ih;
      [['ess', COL.pri], ['pro', COL.sky], ['mails', COL.ok]].forEach(function (p) { var hh = (r[p[0]] / top) * ih; if (hh <= 0) return; y -= hh; var rc = s('rect', { x: x, y: y, width: pw, height: hh, rx: 3, fill: p[1] }); var tt = s('title'); tt.textContent = r.periode + ' · ' + { ess: 'Essentiel', pro: 'Pro', mails: 'Mails pro' }[p[0]] + ' : ' + eur(r[p[0]]); rc.appendChild(tt); svg.appendChild(rc); });
      if (rows.length <= 7 || i % 2 === (rows.length - 1) % 2) { var t = s('text', { x: x + pw / 2, y: H - 8, 'text-anchor': 'middle' }); t.textContent = r.periode; svg.appendChild(t); }
    });
    return svg;
  }
  function revenueBlock() {
    var box = h('div', { class: 'card', id: 'revenus' });
    function draw() {
      box.textContent = '';
      var rows = revCalc(); while (rows.length > 1 && !rows[0].ca && !rows[0].nouveaux && !rows[0].actifs) rows.shift(); var tot = rows.reduce(function (a, r) { return a + r.ca; }, 0), nv = rows.reduce(function (a, r) { return a + r.nouveaux; }, 0), rs = rows.reduce(function (a, r) { return a + r.resilies; }, 0);
      var seg = function (key, opts, val, fn) { return h('div', { class: 'seg' }, opts.map(function (o) { return h('button', { type: 'button', text: o[1], 'aria-pressed': String(val === o[0]), onclick: function () { fn(o[0]); draw(); } }); })); };
      box.appendChild(h('div', { class: 'tbar' }, h('div', null, h('h2', { text: 'Revenus' }), h('p', { class: 'sub', text: 'Ce que vous facturez à vos clients, hors taxes. Un client compte pour chaque mois où son abonnement est actif.' })),
        h('div', { class: 'tools' }, seg('mode', [['mois', 'Mensuel'], ['trimestre', 'Trimestriel'], ['annee', 'Annuel']], REV.mode, function (v) { REV.mode = v; }), seg('depuis', [['6', '6 mois'], ['12', '12 mois'], ['24', '24 mois'], ['tout', 'Tout']], REV.depuis, function (v) { REV.depuis = v; }),
          h('button', { type: 'button', class: 'btn ghost sm', text: '⬇ CSV', onclick: function () { download('revenus-' + REV.mode + '-' + stamp() + '.csv', csvText(REVCOLS, rows)); flash('Export des revenus téléchargé.'); } }))));
      box.appendChild(h('div', { class: 'revsum' }, h('span', null, 'Total facturé sur cette période : ', h('b', { text: eur(tot) })), h('span', null, h('b', { text: String(nv) }), ' nouveau(x) client(s)'), h('span', null, h('b', { text: String(rs) }), ' client(s) parti(s)')));
      box.appendChild(h('div', { class: 'legendline' }, h('span', null, h('i', { style: 'background:' + COL.pri }), 'Essentiel'), h('span', null, h('i', { style: 'background:' + COL.sky }), 'Pro'), h('span', null, h('i', { style: 'background:' + COL.ok }), 'Mails pro')));
      box.appendChild(h('p', { class: 'sub', style: 'margin:0 0 8px', text: 'Chaque barre est un mois : sa hauteur est le total facturé, les couleurs montrent d’où il vient.' }));
      box.appendChild(revBars(rows));
      var tb = h('tbody');
      rows.slice().reverse().forEach(function (r) { var tr = h('tr', null, REVCOLS.map(function (c, ix) { return h('td', { class: ix ? 'num' : 'per' }, cell(c, r)); })); click(tr, function () { var abos = r.abos; open(function () { main.textContent = ''; var rr = abos.map(aRow); main.appendChild(head('Abonnements · ' + r.periode, rr.length + ' abonnement(s) facturé(s) sur la période', [backBtn(), h('button', { type: 'button', class: 'btn', text: '⬇ Exporter (CSV)', onclick: function () { download('abonnements-' + r.periode.replace(/\s/g, '-') + '.csv', csvText(COLS.abonnements, rr)); } })])); main.appendChild(dataTable('abonnements', rr)); }); }); tb.appendChild(tr); });
      box.appendChild(h('div', { class: 'tablewrap' }, h('table', { class: 'revt revm' }, h('thead', null, h('tr', null, REVCOLS.map(function (c, ix) { return h('th', { text: c.l, class: ix ? 'num' : '' }); }))), tb)));
      box.appendChild(h('p', { class: 'sub', style: 'margin-top:10px', text: 'Cliquez sur une ligne pour voir les clients concernés. Les mails pro en plus sont comptés au nombre actuel (pas d’historique). Les abonnements suspendus ne sont pas facturés.' }));
    }
    draw(); return box;
  }

  /* ===== tableau de bord ===== */
  function kpi() {
    var k = { actifs: 0, mrr: 0, ess: 0, pro: 0, nEss: 0, nPro: 0, mailsN: 0, nouveaux30: 0, recurrents: 0, resilies30: 0, resTot: 0, impayes: 0, suspendus: 0 };
    abosR().forEach(function (a) {
      if (counts(a)) {
        k.actifs++; k.mrr += prixAbo(a); k.mailsN += a.mails_sup || 0;
        if (a.formule === 'pro') { k.nPro++; k.pro += PRIX.pro; } else { k.nEss++; k.ess += PRIX.essentiel; }
        if (d10(a.debut) >= ago(30)) k.nouveaux30++; else if (a.statut === 'actif') k.recurrents++;
      }
      if (a.statut === 'resilie') { k.resTot++; if (d10(a.fin) >= ago(30)) k.resilies30++; }
      if (a.statut === 'impaye') k.impayes++;
      if (a.statut === 'suspendu') k.suspendus++;
    });
    k.mailsEur = k.mailsN * MAILP; k.arr = k.mrr * 12; k.panier = k.actifs ? Math.round(k.mrr / k.actifs) : 0;
    k.churn = (k.actifs + k.resilies30) ? Math.round((100 * k.resilies30) / (k.actifs + k.resilies30)) : 0;
    return k;
  }
  function groupN(list, keyFn) { var m = {}; list.forEach(function (x) { var k = keyFn(x) || '—'; m[k] = (m[k] || 0) + 1; }); return Object.keys(m).map(function (k) { return { l: k, n: m[k] }; }).sort(function (a, b) { return b.n - a.n; }).slice(0, 8); }
  function revLine(label, detail, value, strong) { return h('div', { class: 'revline' + (strong ? ' strong' : '') }, h('div', null, h('b', { text: label }), detail ? h('small', { text: detail }) : null), h('span', { text: value })); }
  function revCalcLast(n) { var sv = { m: REV.mode, d: REV.depuis }; REV.mode = 'mois'; REV.depuis = String(n); var r = revCalc(); REV.mode = sv.m; REV.depuis = sv.d; return r; }
  function monthCa() { var r = revCalcLast(1); return r.length ? r[r.length - 1].ca : 0; }
  function kpiRow(items) { return h('div', { class: 'kr' }, items.map(function (i) { return h('div', { class: 'card' }, h('div', { class: 'ic ' + (i[3] || 'c1') }, ico(i[2] || 'users', 20)), h('div', null, h('span', { text: i[0] }), h('b', { text: String(i[1]) }))); })); }
  function updBadges() { var d = demR(), n = function (f) { return d.filter(f).length; }; var set = function (id, v) { var e = $('#' + id); if (e) { e.textContent = v || ''; e.hidden = !v; } }; set('c-dem', n(function (x) { return x.statut === 'nouvelle'; })); set('c-crea', n(function (x) { return x.statut === 'en_creation' || x.statut === 'apercu'; })); set('c-ligne', n(function (x) { return x.statut === 'en_ligne'; })); }
  function sectionPage(t, sub, key, pred, kp) { listView(key, t, sub, pred, function () { return kpiRow(kp); }, true); }
  function pageDem() { var d = demR(), c = function (k) { return d.filter(function (x) { return x.statut === k; }).length; }; sectionPage('Demandes de site', 'Suivez et traitez les nouvelles demandes.', 'demandes', null, [['Total', d.length, 'file', 'c2'], ['Nouvelles', c('nouvelle'), 'file', 'c3'], ['En création', c('en_creation'), 'file', 'c4'], ['Aperçus envoyés', c('apercu'), 'file', 'c2'], ['Terminées', c('en_ligne'), 'file', 'c1']]); }
  function pageCrea() { var d = demR(), c = function (k) { return d.filter(function (x) { return x.statut === k; }).length; }; sectionPage('Sites en création', 'Les sites en cours de fabrication ou en attente de l’accord du client.', 'demandes', function (r) { return r.site === 'en_creation' || r.site === 'apercu'; }, [['En création', c('en_creation'), 'file', 'c4'], ['Aperçus envoyés', c('apercu'), 'file', 'c2']]); }
  function pageLigne() { var d = demR().filter(function (x) { return x.statut === 'en_ligne'; }); sectionPage('Sites en ligne', 'Les sites livrés et publiés.', 'demandes', function (r) { return r.site === 'en_ligne'; }, [['Sites en ligne', d.length, 'file', 'c1'], ['Formule Pro', d.filter(function (x) { return x.formule === 'pro'; }).length, 'file', 'c2'], ['Formule Essentiel', d.filter(function (x) { return x.formule !== 'pro'; }).length, 'file', 'c3']]); }
  function pageAbo() { var k = kpi(); sectionPage('Abonnements', 'Les formules et abonnements de vos clients.', 'abonnements', null, [['Abonnements actifs', k.actifs, 'repeat', 'c4'], ['Essentiel', k.nEss, 'repeat', 'c3'], ['Pro', k.nPro, 'repeat', 'c2'], ['Impayés', k.impayes, 'repeat', 'c1'], ['Partis (30 jours)', k.resilies30, 'repeat', 'c1']]); }
  function dashboard() {
    var k = kpi(), out = h('div'), dm = demR(), pl = plR(), cm = comR(), st = {}, plc = { ouverte: 0, en_cours: 0, resolue: 0 };
    dm.forEach(function (x) { st[x.statut] = (st[x.statut] || 0) + 1; });
    pl.forEach(function (x) { plc[x.statut] = (plc[x.statut] || 0) + 1; });
    var nbDemo = D.comptes.filter(function (c) { return c.demo; }).length;
    var cA = function (t, f, sub) { return function () { L.abos(t, f, sub); }; };
    var cC = function (t, f) { return function () { L.comptes(t, function (r) { return (DEMO.on || !r.demo) && (!f || f(r)); }); }; };
    var cD = function (t, f) { return function () { L.demandes(t, f); }; };
    var cP = function (t, f) { return function () { L.plaintes(t, f); }; };
    var actifsF = function (r) { return r.abo === 'actif' || r.abo === 'impaye'; };
    var j7 = cm.filter(function (c) { return d10(c.created_at) >= ago(7); }).length, j1 = cm.filter(function (c) { return d10(c.created_at) >= ago(1); }).length, j30 = cm.filter(function (c) { return d10(c.created_at) >= ago(30); }).length;
    var s7 = function (n, one, many) { return n + ' ' + (n > 1 ? many : one); };
    if (nbDemo) out.appendChild(h('label', { class: 'demonote' }, h('input', { type: 'checkbox', checked: DEMO.on ? 'checked' : null, onchange: function (e) { DEMO.on = e.target.checked; top(showStats); } }), h('span', null, h('b', { text: DEMO.on ? 'Les ' + nbDemo + ' comptes de test sont inclus dans les chiffres. ' : 'Les ' + nbDemo + ' comptes de test sont cachés. ' }), 'Décochez pour ne voir que les vrais clients.')));
    var enLigne = dm.filter(function (x) { return x.statut === 'en_ligne'; }).length, caMois = monthCa();
    out.appendChild(h('div', { class: 'grid g4' },
      hero('c3', 'euro', eur(k.mrr), 'Revenu récurrent par mois (HT)', k.actifs ? s7(k.actifs, 'client qui paie', 'clients qui paient') : null, false, function () { open(revenuePage); }),
      hero('c2', 'file', eur(caMois), 'Facturé ce mois-ci (HT)', null, false, function () { open(revenuePage); }),
      hero('c4', 'repeat', num(k.actifs), 'Clients actifs', k.nouveaux30 ? '+' + k.nouveaux30 + ' ce mois' : null, false, cA('Clients abonnés', actifsF)),
      hero('c1', 'users', num(enLigne), 'Sites en ligne', null, false, cD('Sites en ligne', function (r) { return r.site === 'en_ligne'; }))));
    var todo = [
      ['Demandes de site à traiter', st.nouvelle || 0, cD('Demandes à traiter', function (r) { return r.site === 'nouvelle'; })],
      ['Sites en création', st.en_creation || 0, cD('Sites en création', function (r) { return r.site === 'en_creation'; })],
      ['Aperçus en attente du client', st.apercu || 0, cD('Aperçus envoyés', function (r) { return r.site === 'apercu'; })],
      ['Paiements en attente', k.impayes, cA('Abonnements impayés', function (r) { return r.abo === 'impaye'; })],
      ['Messages de clients', (plc.ouverte || 0) + (plc.en_cours || 0), cP('Messages à traiter', function (r) { return r.pl !== 'resolue'; })]
    ];
    var rows6 = revCalcLast(6);
    out.appendChild(h('div', { class: 'dash2' },
      h('div', { class: 'card' }, h('h2', { text: 'Évolution des revenus' }), h('p', { class: 'sub', text: 'Facturé chaque mois, hors taxes. Bleu foncé : Essentiel · bleu clair : Pro · vert : mails pro.' }), revBars(rows6)),
      h('div', { class: 'card' }, h('h2', { text: 'À traiter aujourd’hui' }), h('ul', { class: 'todo' }, todo.map(function (t) { return click(h('li', { class: t[1] ? '' : 'zero' }, h('b', { text: String(t[1]) }), h('span', { text: t[0] }), h('em', { text: 'Voir →' })), t[2]); })))));

    out.appendChild(h('div', { class: 'sec', text: 'Vos revenus, expliqués' }));
    var rv = h('div', { class: 'card' },
      h('h2', { text: k.mrr ? 'Chaque mois, vous gagnez ' + eur(k.mrr) : 'Pas encore de revenus' }),
      h('p', { class: 'sub', text: k.mrr ? 'Voici d’où vient cette somme. Tous les montants sont hors taxes (HT).' : 'Dès qu’un client aura un abonnement actif, le détail apparaîtra ici.' }));
    if (k.mrr) {
      rv.appendChild(revLine('Formule Essentiel', s7(k.nEss, 'client', 'clients') + ' × ' + PRIX.essentiel + ' €', eur(k.ess)));
      rv.appendChild(revLine('Formule Pro', s7(k.nPro, 'client', 'clients') + ' × ' + PRIX.pro + ' €', eur(k.pro)));
      rv.appendChild(revLine('Adresses mail pro en plus', s7(k.mailsN, 'adresse', 'adresses') + ' × ' + MAILP + ' €', eur(k.mailsEur)));
      rv.appendChild(revLine('Total par mois', null, eur(k.mrr), true));
      rv.appendChild(revLine('Sur une année', 'si personne ne part et que personne n’arrive', eur(k.arr)));
      rv.appendChild(mini([['Prix moyen par client', eur(k.panier), cA('Clients abonnés', actifsF)], ['Clients partis (30 jours)', k.resilies30, cA('Clients partis ces 30 jours', function (r) { return r.abo === 'resilie' && d10(r.fin) >= ago(30); })], ['Impayés', k.impayes, cA('Abonnements impayés', function (r) { return r.abo === 'impaye'; })]]));
    }
    rv.appendChild(h('div', { style: 'margin-top:14px' }, h('button', { type: 'button', class: 'btn', text: 'Voir mois par mois →', onclick: function () { open(revenuePage); } })));
    out.appendChild(rv);

    var more = h('details', { class: 'more' }, h('summary', { text: 'Plus de statistiques' }));
    more.appendChild(h('div', { class: 'sec', text: 'Vos clients' }));
    var ins30 = {}; cm.forEach(function (c) { var d = d10(c.created_at); if (d >= ago(30)) ins30[d] = (ins30[d] || 0) + 1; });
    var jours = Object.keys(ins30).map(function (d) { return { d: d, n: ins30[d] }; });
    var avecDemande = cm.filter(function (c) { return (IX.dem[c.id] || []).length > 0; }).length, abonnes = k.actifs + k.resTot;
    more.appendChild(h('div', { class: 'grid g2' },
      card('Nouvelles inscriptions', '30 derniers jours · ' + s7(j30, 'personne', 'personnes') + ' · cliquez pour la liste', (function () { var w = h('div', null, area(jours)); return click(w, cC('Inscrits des 30 derniers jours', recent('inscrit', 30))); })()),
      card('De l’inscription à l’abonnement', 'Combien de personnes vont jusqu’au bout', funnel([
        { l: 'Inscrites', n: cm.length, c: COL.pri, p: 100, fn: cC('Toutes les personnes inscrites') },
        { l: 'Ont demandé un site', n: avecDemande, c: COL.sky, p: cm.length ? Math.round((100 * avecDemande) / cm.length) : 0, fn: cC('Inscrits ayant demandé un site', function (r) { return r.demandes > 0; }) },
        { l: 'Sont devenues clientes', n: abonnes, c: COL.ok, p: cm.length ? Math.min(100, Math.round((100 * abonnes) / cm.length)) : 0, fn: cA('Tous les abonnements (actifs et partis)', function () { return true; }) }]))));
    more.appendChild(h('div', { class: 'grid g2', style: 'margin-top:16px' },
      card('Formules choisies', 'Clients abonnés', donut([{ l: 'Essentiel', n: k.nEss, c: COL.pri, fn: cA('Clients Essentiel', function (r) { return actifsF(r) && r.formule === 'essentiel'; }) }, { l: 'Pro', n: k.nPro, c: COL.sky, fn: cA('Clients Pro', function (r) { return actifsF(r) && r.formule === 'pro'; }) }], String(k.actifs), 'clients')),
      card('Mouvements des 30 derniers jours', null, mini([
        ['Nouveaux clients', k.nouveaux30, cA('Nouveaux clients (30 jours)', function (r) { return d10(r.debut) >= ago(30); })],
        ['Clients depuis plus d’un mois', k.recurrents, cA('Clients depuis plus d’un mois', function (r) { return r.abo === 'actif' && d10(r.debut) < ago(30); })],
        ['Clients partis', k.resilies30, cA('Clients partis (30 jours)', function (r) { return r.abo === 'resilie' && d10(r.fin) >= ago(30); })],
        ['Partis depuis le début', k.resTot, cA('Tous les clients partis', function (r) { return r.abo === 'resilie'; })],
        ['Suspendus', k.suspendus, cA('Abonnements suspendus', function (r) { return r.abo === 'suspendu'; })],
        ['Connectés ces 7 jours', cm.filter(function (c) { return d10(c.derniere_connexion) >= ago(7); }).length, cC('Connectés ces 7 derniers jours', recent('connexion', 7))]]))));

    more.appendChild(h('div', { class: 'sec', text: 'Les sites' }));
    var sF = function (key) { return cD('Demandes · ' + lab(key), function (r) { return r.site === key; }); };
    more.appendChild(h('div', { class: 'grid g3' },
      card('Où en sont les sites', s7(dm.length, 'demande', 'demandes'), donut([{ l: 'À traiter', n: st.nouvelle || 0, c: COL.warn, fn: sF('nouvelle') }, { l: 'En création', n: st.en_creation || 0, c: COL.pri, fn: sF('en_creation') }, { l: 'Aperçu envoyé', n: st.apercu || 0, c: COL.sky, fn: sF('apercu') }, { l: 'En ligne', n: st.en_ligne || 0, c: COL.ok, fn: sF('en_ligne') }, { l: 'Abandonnées', n: st.abandonnee || 0, c: COL.gray, fn: sF('abandonnee') }], String(dm.length), 'demandes')),
      card('Types de commerces', 'Qui fait des demandes', bars(groupN(dm, function (x) { return x.activite; }).map(function (x) { return { l: x.l, n: x.n, fn: cD('Demandes · ' + x.l, function (r) { return (r.activite || '—') === x.l; }) }; }))),
      card('Villes', 'D’où viennent les demandes', bars(groupN(dm, function (x) { return (x.ville || '').trim(); }).map(function (x) { return { l: x.l, n: x.n, fn: cD('Demandes · ' + x.l, function (r) { return (r.ville || '—').trim().toLowerCase() === x.l.toLowerCase(); }) }; })))));

    more.appendChild(h('div', { class: 'sec', text: 'Service client' }));
    var motifs = groupN(abosR().filter(function (a) { return a.statut === 'resilie'; }), function (a) { return a.motif || 'non précisé'; });
    var pF = function (key) { return cP('Messages · ' + lab(key), function (r) { return r.pl === key; }); };
    more.appendChild(h('div', { class: 'grid g3' },
      card('Messages et plaintes', s7(pl.length, 'au total', 'au total'), donut([{ l: 'Ouvertes', n: plc.ouverte || 0, c: COL.bad, fn: pF('ouverte') }, { l: 'En cours', n: plc.en_cours || 0, c: COL.warn, fn: pF('en_cours') }, { l: 'Résolues', n: plc.resolue || 0, c: COL.ok, fn: pF('resolue') }], String(pl.length), 'messages')),
      card('Pourquoi ils partent', null, bars(motifs.map(function (x) { return { l: x.l, n: x.n, fn: cA('Départs · ' + x.l, function (r) { return r.abo === 'resilie' && (r.motif || 'non précisé') === x.l; }) }; }), 'Personne n’est parti.')),
      card('D’où viennent les demandes', 'Annonce, lien, accès direct…', bars(groupN(dm, function (x) { return srcOf(x); }).map(function (x) { return { l: x.l, n: x.n, fn: cD('Demandes · ' + x.l, function (r) { return r.source === x.l; }) }; })))));
    out.appendChild(more);
    return out;
  }
  function showStats() {
    var hr = new Date().getHours(), greet = hr < 18 ? 'Bonjour' : 'Bonsoir';
    main.textContent = '';
    main.appendChild(head(greet + ', Admin', new Date().toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }) + ' · cliquez sur un chiffre pour voir le détail.', [h('button', { type: 'button', class: 'btn ghost', text: 'Actualiser', onclick: function () { loadAll().then(function () { top(showStats); flash('Statistiques actualisées.'); }); } })]));
    main.appendChild(dashboard());
  }
  function revenuePage() {
    main.textContent = '';
    main.appendChild(head('Revenus', 'Ce que rapportent vos abonnements, en clair. Montants hors taxes (HT).', [backBtn()]));
    var k = kpi(), sv = { m: REV.mode, d: REV.depuis }; REV.mode = 'mois'; REV.depuis = 'tout'; var all = revCalc(); REV.mode = sv.m; REV.depuis = sv.d;
    var depuis = all.reduce(function (t, r) { return t + r.ca; }, 0), ce = all.length ? all[all.length - 1].ca : 0;
    main.appendChild(h('div', { class: 'totbox card' },
      h('div', null, h('span', { class: 'lbl', text: 'Revenu total par mois' }), h('b', { class: 'big', text: eur(k.mrr) }), h('small', { text: 'ce que vos clients actuels vous paient chaque mois' })),
      h('div', null, h('span', { class: 'lbl', text: 'Facturé ce mois-ci' }), h('b', { text: eur(ce) })),
      h('div', null, h('span', { class: 'lbl', text: 'Total depuis le début' }), h('b', { text: eur(depuis) })),
      h('div', null, h('span', { class: 'lbl', text: 'Sur 12 mois' }), h('b', { text: eur(k.arr) }))));
    var share = function (v) { return k.mrr ? Math.round((100 * v) / k.mrr) : 0; };
    var line = function (name, sub, n, unit, tot, color) { return h('tr', null, h('td', null, h('div', { class: 'tname' }, h('i', { style: 'background:' + color }), h('div', null, h('b', { text: name }), h('small', { text: sub })))), h('td', { class: 'num', text: String(n) }), h('td', { class: 'num', text: unit }), h('td', null, h('div', { class: 'meter' }, h('i', { style: 'width:' + share(tot) + '%;background:' + color }), h('small', { text: share(tot) + ' %' }))), h('td', { class: 'num strong', text: eur(tot) })); };
    main.appendChild(h('div', { class: 'card', style: 'margin-top:16px' },
      h('h2', { text: 'D’où viennent vos revenus' }), h('p', { class: 'sub', text: 'Chaque ligne : combien de clients ou d’adresses, le prix de chacun, et ce que ça rapporte par mois.' }),
      h('div', { class: 'tablewrap' }, h('table', { class: 'revt' },
        h('thead', null, h('tr', null, ['Type', 'Nombre', 'Prix unitaire', 'Part du total', 'Par mois'].map(function (x, i) { return h('th', { text: x, class: i ? 'num' : '' }); }))),
        h('tbody', null,
          line('Abonnement Essentiel', 'site vitrine, 1 modification par mois', k.nEss, PRIX.essentiel + ' €', k.ess, COL.pri),
          line('Abonnement Pro', 'réservation en ligne, éditeur, 1 mail pro inclus', k.nPro, PRIX.pro + ' €', k.pro, COL.sky),
          line('Adresses mail pro en plus', 'hors celle incluse avec le Pro', k.mailsN, MAILP + ' €', k.mailsEur, COL.ok)),
        h('tfoot', null, h('tr', null, h('td', { text: 'Total par mois' }), h('td', { class: 'num', text: String(k.nEss + k.nPro) + ' clients' }), h('td'), h('td'), h('td', { class: 'num strong', text: eur(k.mrr) }))))),
      h('div', { class: 'mailnote' }, h('b', { text: String(k.nPro + k.mailsN) }), ' adresse(s) mail pro au total : ', h('b', { text: String(k.nPro) }), ' incluse(s) avec le Pro + ', h('b', { text: String(k.mailsN) }), ' payante(s) en plus.')));
    main.appendChild(h('div', { class: 'sec', text: 'Mois par mois' }));
    main.appendChild(revenueBlock());
  }

  /* ===== clients : filtres, export, revenus ===== */
  var F = {};
  var FDEF = [['q', 'Recherche'], ['formule', 'Formule'], ['abo', 'Abonnement'], ['site', 'Statut du site'], ['plaintes', 'Plaintes'], ['activite', 'Activité'], ['ville', 'Ville'], ['connexion', 'Dernière connexion'], ['mails', 'Mails pro'], ['du', 'Inscrit après'], ['au', 'Inscrit avant']];
  function nbF() { return Object.keys(F).filter(function (k) { return F[k]; }).length; }
  function applyF(rows, f) {
    f = f || F;
    return rows.filter(function (r) {
      if (f.q) { var q = f.q.toLowerCase(); if ((r.nom + ' ' + r.email + ' ' + r.commerce + ' ' + r.ville + ' ' + r.tel).toLowerCase().indexOf(q) < 0) return false; }
      if (f.formule && r.formule !== f.formule) return false;
      if (f.abo) { if (f.abo === 'aucun') { if (r.abo) return false; } else if (r.abo !== f.abo) return false; }
      if (f.site) { if (f.site === 'aucune') { if (r.demandes) return false; } else if (r.site !== f.site) return false; }
      if (f.plaintes === 'ouvertes' && !r.plaintes_ouvertes) return false;
      if (f.plaintes === 'avec' && !r.plaintes) return false;
      if (f.plaintes === 'aucune' && r.plaintes) return false;
      if (f.activite && r.activite !== f.activite) return false;
      if (f.ville && (r.ville || '').toLowerCase() !== f.ville.toLowerCase()) return false;
      if (f.mails === 'oui' && !(r.mails > 0)) return false;
      if (f.du && d10(r.inscrit) < f.du) return false;
      if (f.au && d10(r.inscrit) > f.au) return false;
      if (f.connexion) { if (f.connexion === 'jamais') { if (r.connexion) return false; } else if (!r.connexion || d10(r.connexion) < ago(+f.connexion)) return false; }
      return true;
    });
  }
  function fSelect(key, label, options) { var e = h('select', { 'aria-label': label }); e.appendChild(h('option', { value: '', text: 'Tous' })); options.forEach(function (o) { e.appendChild(h('option', { value: o[0], text: o[1] })); }); e.value = F[key] || ''; e.addEventListener('change', function () { F[key] = e.value; }); return h('label', null, label, e); }
  function distinct(rows, k) { var m = {}; rows.forEach(function (r) { if (r[k]) m[(k === 'ville' ? r[k].trim() : r[k])] = 1; }); return Object.keys(m).sort().map(function (x) { return [x, x]; }); }
  function clientsView() {
    main.textContent = '';
    var all = D.comptes.map(cRow), tbody = h('div', { class: 'tablewrap' }), count = h('span', { class: 'sub' }), badge = h('span', { class: 'bdg' }), panel = h('div', { class: 'fpanel', hidden: '' });
    var fbtn = h('button', { type: 'button', class: 'btn ghost iconbtn', 'aria-label': 'Filtres', 'aria-expanded': 'false', title: 'Filtres' }, ico('filter', 18), badge);
    var qBox = h('input', { class: 'find', type: 'search', placeholder: 'Rechercher un nom, un e-mail, un commerce…', value: F.q || '', 'aria-label': 'Rechercher' });
    qBox.addEventListener('input', function () { F.q = qBox.value; draw(); });
    function upd() { var n = nbF(); badge.textContent = n ? String(n) : ''; badge.hidden = !n; }
    function draw() {
      upd(); var rows = applyF(all); count.textContent = rows.length + ' client(s) sur ' + all.length; tbody.textContent = '';
      if (!rows.length) { tbody.appendChild(h('p', { class: 'empty', text: all.length ? 'Aucun client ne correspond aux filtres.' : 'Aucun client pour le moment.' })); return; }
      var cols = ['nom', 'inscrit', 'connexion', 'site', 'formule', 'abo', 'mails', 'plaintes_ouvertes'].map(function (k) { var c = COLS.clients.filter(function (c) { return c.k === k; })[0], sh = { connexion: 'Connexion', site: 'Site', mails: 'Mails pro', plaintes_ouvertes: 'Plaintes', inscrit: 'Inscrit' }; return sh[k] ? { k: c.k, l: sh[k], t: c.t } : c; });
      var tb = h('tbody');
      rows.slice(0, 500).forEach(function (r) {
        var tr = h('tr', null, cols.map(function (c) { return h('td', null, cell(c, r)); }), h('td', { class: 'acts' }, h('button', { type: 'button', class: 'btn sm', text: 'Son espace', title: 'Voir le site en tant que ce client', onclick: function (e) { e.stopPropagation(); impersonate(r.compte_id); } })));
        click(tr, function () { open(function () { detail(r.compte_id); }); }); tb.appendChild(tr);
      });
      tbody.appendChild(h('table', null, h('thead', null, h('tr', null, cols.map(function (c) { return h('th', { text: c.l }); }), h('th'))), tb));
    }
    function buildPanel() {
      panel.textContent = '';
      var yes = function (a) { return a.map(function (x) { return [x, lab(x)]; }); };
      var du = h('input', { type: 'date', value: F.du || '' }), au = h('input', { type: 'date', value: F.au || '' });
      du.addEventListener('change', function () { F.du = du.value; }); au.addEventListener('change', function () { F.au = au.value; });
      panel.appendChild(h('div', { class: 'fgrid' },
        fSelect('formule', 'Formule', yes(['essentiel', 'pro'])), fSelect('abo', 'Abonnement', yes(['actif', 'impaye', 'suspendu', 'resilie']).concat([['aucun', 'Aucun abonnement']])),
        fSelect('site', 'Statut du site', yes(STATUTS_SITE).concat([['aucune', 'Aucune demande']])),
        fSelect('plaintes', 'Plaintes', [['ouvertes', 'Avec plainte ouverte'], ['avec', 'Avec au moins une plainte'], ['aucune', 'Aucune plainte']]),
        fSelect('activite', 'Activité', distinct(all, 'activite')), fSelect('ville', 'Ville', distinct(all, 'ville')),
        fSelect('connexion', 'Dernière connexion', [['1', 'Dans les 24 h'], ['7', 'Dans les 7 jours'], ['30', 'Dans les 30 jours'], ['jamais', 'Jamais connecté']]),
        fSelect('mails', 'Mails pro', [['oui', 'Avec mails pro en plus']]), h('label', null, 'Inscrit après le', du), h('label', null, 'Inscrit avant le', au)));
      panel.appendChild(h('div', { class: 'tools' }, h('button', { type: 'button', class: 'btn', text: 'Appliquer', onclick: function () { draw(); flash(applyF(all).length + ' client(s) trouvé(s).'); } }), h('button', { type: 'button', class: 'btn ghost', text: 'Réinitialiser', onclick: function () { F = {}; qBox.value = ''; buildPanel(); draw(); } })));
    }
    fbtn.addEventListener('click', function () { var o = panel.hidden; panel.hidden = !o; fbtn.setAttribute('aria-expanded', String(o)); if (o) buildPanel(); });
    main.appendChild(head('Clients', 'Tous les comptes inscrits · cliquez sur une ligne pour ouvrir la fiche', [h('button', { type: 'button', class: 'btn', text: '⬇ Exporter', onclick: function () { exportDialog('clients'); } })]));
    var cmR = D.comptes.map(cRow), nAbo = function (f) { return cmR.filter(f).length; };
    main.appendChild(kpiRow([['Tous les clients', cmR.length, 'users', 'c2'], ['Abonnement actif', nAbo(function (r) { return r.abo === 'actif'; }), 'repeat', 'c3'], ['Paiement en attente', nAbo(function (r) { return r.abo === 'impaye'; }), 'repeat', 'c4'], ['Sans abonnement', nAbo(function (r) { return !r.abo; }), 'users', 'c1']]));
    var chips = h('div', { class: 'chips' }), CH = [['', 'Tous'], ['actif', 'Actifs'], ['impaye', 'Impayés'], ['suspendu', 'Suspendus'], ['resilie', 'Résiliés'], ['aucun', 'Sans abonnement']];
    function drawChips() { chips.textContent = ''; CH.forEach(function (c) { chips.appendChild(h('button', { type: 'button', class: 'chip' + ((F.abo || '') === c[0] ? ' on' : ''), text: c[1], onclick: function () { F.abo = c[0]; drawChips(); draw(); } })); }); }
    drawChips();
    main.appendChild(h('div', { class: 'card' }, chips, h('div', { class: 'tbar' }, fbtn, qBox, count), panel, tbody));
    draw();
  }

  /* ===== fenêtre d'export ===== */
  function exportDialog(startKey) {
    var st = { ds: startKey || 'clients', cols: {}, f: {}, du: '', au: '', useF: true };
    var ov = h('div', { class: 'ov', role: 'dialog', 'aria-modal': 'true', 'aria-label': 'Exporter' }), bx = h('div', { class: 'modal' });
    ov.appendChild(bx); ov.addEventListener('click', function (e) { if (e.target === ov) ov.remove(); });
    function pick() { st.cols = {}; COLS[st.ds].forEach(function (c) { st.cols[c.k] = true; }); st.f = {}; }
    pick();
    function rowsNow() {
      var rows = DS[st.ds].rows();
      if (st.ds === 'clients' && st.useF) rows = applyF(rows);
      DS[st.ds].filt.forEach(function (f) { if (st.f[f[0]]) rows = rows.filter(function (r) { return r[f[0]] === st.f[f[0]]; }); });
      var dk = DS[st.ds].date; if (st.du) rows = rows.filter(function (r) { return d10(r[dk]) >= st.du; }); if (st.au) rows = rows.filter(function (r) { return d10(r[dk]) <= st.au; });
      return rows;
    }
    function draw() {
      bx.textContent = '';
      var sd = h('select', null, Object.keys(DS).map(function (k) { var o = h('option', { value: k, text: DS[k].l }); if (k === st.ds) o.selected = true; return o; }));
      sd.addEventListener('change', function () { st.ds = sd.value; pick(); draw(); });
      var du = h('input', { type: 'date', value: st.du }), au = h('input', { type: 'date', value: st.au });
      du.addEventListener('change', function () { st.du = du.value; draw(); }); au.addEventListener('change', function () { st.au = au.value; draw(); });
      var n = rowsNow().length;
      bx.appendChild(h('div', { class: 'tbar' }, h('h2', { text: 'Exporter les données' }), h('button', { type: 'button', class: 'btn ghost sm', text: 'Fermer', onclick: function () { ov.remove(); } })));
      bx.appendChild(h('div', { class: 'fgrid' }, h('label', null, 'Que voulez-vous exporter ?', sd), h('label', null, 'Du (date de création)', du), h('label', null, 'Au', au),
        DS[st.ds].filt.map(function (f) { var e = h('select', null, h('option', { value: '', text: 'Tous' }), f[2].map(function (o) { var op = h('option', { value: o, text: lab(o) }); if (st.f[f[0]] === o) op.selected = true; return op; })); e.addEventListener('change', function () { st.f[f[0]] = e.value; draw(); }); return h('label', null, f[1], e); })));
      if (st.ds === 'clients') { var cb = h('input', { type: 'checkbox' }); cb.checked = st.useF; cb.addEventListener('change', function () { st.useF = cb.checked; draw(); }); bx.appendChild(h('label', { class: 'chk' }, cb, 'Appliquer aussi les filtres de la liste Clients (' + nbF() + ' actif(s))')); }
      bx.appendChild(h('p', { class: 'sub', style: 'margin:14px 0 6px', text: 'Colonnes à inclure' }));
      bx.appendChild(h('div', { class: 'cols' }, COLS[st.ds].map(function (c) { var cb = h('input', { type: 'checkbox' }); cb.checked = !!st.cols[c.k]; cb.addEventListener('change', function () { st.cols[c.k] = cb.checked; }); return h('label', { class: 'chk' }, cb, c.l); })));
      bx.appendChild(h('div', { class: 'tools', style: 'margin-top:16px' }, h('button', { type: 'button', class: 'btn', text: '⬇ Télécharger le CSV (' + n + ' ligne' + (n > 1 ? 's' : '') + ')', onclick: function () { var cols = COLS[st.ds].filter(function (c) { return st.cols[c.k]; }); if (!cols.length) { flash('Choisissez au moins une colonne.', true); return; } download(st.ds + '-' + stamp() + '.csv', csvText(cols, rowsNow())); flash('Export téléchargé.'); ov.remove(); } }),
        h('button', { type: 'button', class: 'btn ghost', text: 'Tout cocher / décocher', onclick: function () { var all = COLS[st.ds].every(function (c) { return st.cols[c.k]; }); COLS[st.ds].forEach(function (c) { st.cols[c.k] = !all; }); draw(); } })));
      bx.appendChild(h('p', { class: 'sub', style: 'margin-top:10px', text: 'Fichier CSV compatible Excel (séparateur « ; »).' }));
    }
    draw(); document.body.appendChild(ov);
    document.addEventListener('keydown', function esc(e) { if (e.key === 'Escape') { ov.remove(); document.removeEventListener('keydown', esc); } });
  }

  /* ===== communication ===== */
  var COMM = { pre: null, f: {}, sel: null, canal: { mail: true, notif: true }, sujet: '', corps: '' };
  function commView() {
    main.textContent = '';
    main.appendChild(head('Communication', 'Écrivez à tous vos clients, ou choisissez qui reçoit le message. Rien ne part sans votre clic.', []));
    var holder = h('div'); main.appendChild(holder);
    api('/api/admin/communications').then(function (r) {
      var mailOk = !!(r.j && r.j.mail_ok), hist = (r.j && r.j.liste) || [], all = D.comptes.map(cRow);
      if (COMM.pre) { COMM.sel = {}; COMM.pre.forEach(function (i) { COMM.sel[i] = true; }); COMM.pre = null; COMM.f = {}; }
      if (!COMM.sel) { COMM.sel = {}; all.forEach(function (c) { COMM.sel[c.compte_id] = true; }); }
      var listBox = h('div', { class: 'tablewrap', style: 'max-height:340px;overflow:auto' }), cnt = h('span', { class: 'sub' }), btnSend;
      var visible = function () { return applyF(all, COMM.f); };
      var chosen = function () { return all.filter(function (c) { return COMM.sel[c.compte_id]; }); };
      var mailable = function (list) { return list.filter(function (c) { return !c.optout && !c.demo && !/\.invalid$/i.test(c.email || ''); }); };
      function upd() { var c = chosen(); cnt.textContent = c.length + ' sélectionné(s) sur ' + all.length + ' client(s)'; if (btnSend) { btnSend.textContent = '✉ Envoyer à ' + c.length + ' client(s)'; btnSend.disabled = !c.length; } }
      function drawList() {
        listBox.textContent = ''; var rows = visible();
        if (!rows.length) { listBox.appendChild(h('p', { class: 'empty', text: 'Aucun client ne correspond.' })); upd(); return; }
        var tb = h('tbody');
        rows.forEach(function (r) { var cb = h('input', { type: 'checkbox', 'aria-label': 'Choisir ' + r.nom }); cb.checked = !!COMM.sel[r.compte_id]; cb.addEventListener('change', function () { if (cb.checked) COMM.sel[r.compte_id] = true; else delete COMM.sel[r.compte_id]; upd(); });
          tb.appendChild(h('tr', null, h('td', { style: 'width:36px' }, cb), h('td', null, cell(COLS.clients[0], r)), h('td', null, cell(COLS.clients[10], r)), h('td', null, cell(COLS.clients[11], r)), h('td', null, r.optout ? h('span', { class: 'pill', text: 'STOP mails' }) : r.demo ? h('span', { class: 'pill', text: 'Démo' }) : null))); });
        listBox.appendChild(h('table', null, tb)); upd();
      }
      var fs = function (key, label, opts) { var e = h('select', { 'aria-label': label }); e.appendChild(h('option', { value: '', text: 'Tous' })); opts.forEach(function (o) { e.appendChild(h('option', { value: o[0], text: o[1] })); }); e.value = COMM.f[key] || ''; e.addEventListener('change', function () { COMM.f[key] = e.value; COMM.sel = {}; applyF(all, COMM.f).forEach(function (c) { COMM.sel[c.compte_id] = true; }); drawList(); }); return h('label', null, label, e); };
      var yes = function (a) { return a.map(function (x) { return [x, lab(x)]; }); };
      var filt = h('div', { class: 'fgrid' }, fs('formule', 'Formule', yes(['essentiel', 'pro'])), fs('abo', 'Abonnement', yes(['actif', 'impaye', 'suspendu', 'resilie']).concat([['aucun', 'Aucun abonnement']])), fs('site', 'Statut du site', yes(STATUTS_SITE).concat([['aucune', 'Aucune demande']])), fs('plaintes', 'Plaintes', [['ouvertes', 'Avec plainte ouverte'], ['avec', 'Avec au moins une plainte'], ['aucune', 'Aucune plainte']]), fs('activite', 'Activité', distinct(all, 'activite')), fs('ville', 'Ville', distinct(all, 'ville')), fs('connexion', 'Dernière connexion', [['7', 'Dans les 7 jours'], ['30', 'Dans les 30 jours'], ['jamais', 'Jamais connecté']]));
      holder.appendChild(h('div', { class: 'card' }, h('div', { class: 'tbar' }, h('div', null, h('h2', { text: '1. Qui reçoit le message ?' }), h('p', { class: 'sub', text: 'Choisissez un filtre, puis cochez ou décochez les clients à la main.' })), cnt), filt,
        h('div', { class: 'tools', style: 'margin-bottom:10px' }, h('button', { type: 'button', class: 'btn ghost sm', text: 'Tout cocher (liste affichée)', onclick: function () { visible().forEach(function (c) { COMM.sel[c.compte_id] = true; }); drawList(); } }), h('button', { type: 'button', class: 'btn ghost sm', text: 'Tout décocher', onclick: function () { COMM.sel = {}; drawList(); } }), h('button', { type: 'button', class: 'btn ghost sm', text: 'Réinitialiser les filtres', onclick: function () { COMM.f = {}; COMM.sel = {}; all.forEach(function (c) { COMM.sel[c.compte_id] = true; }); commView(); } })), listBox));
      var sj = h('input', { type: 'text', maxlength: '150', value: COMM.sujet, placeholder: 'Ex. : Nouveauté sur votre espace' }), co = h('textarea', { maxlength: '8000', style: 'min-height:200px', placeholder: 'Bonjour {prenom},\n\n…' });
      co.value = COMM.corps; sj.addEventListener('input', function () { COMM.sujet = sj.value; }); co.addEventListener('input', function () { COMM.corps = co.value; });
      var cm = h('input', { type: 'checkbox' }), cn = h('input', { type: 'checkbox' }); cm.checked = COMM.canal.mail; cn.checked = COMM.canal.notif;
      cm.addEventListener('change', function () { COMM.canal.mail = cm.checked; }); cn.addEventListener('change', function () { COMM.canal.notif = cn.checked; });
      var prev = h('div', { class: 'infobox', hidden: '' });
      btnSend = h('button', { type: 'button', class: 'btn', text: '✉ Envoyer', onclick: function () {
        var c = chosen(); if (!c.length) { flash('Choisissez au moins un client.', true); return; }
        if (!sj.value.trim() || co.value.trim().length < 5) { flash('Le sujet et le message sont obligatoires.', true); return; }
        if (!cm.checked && !cn.checked) { flash('Choisissez au moins un canal : e-mail ou notification.', true); return; }
        var nm = cm.checked ? mailable(c).length : 0;
        if (!window.confirm('Envoyer « ' + sj.value.trim() + ' » à ' + c.length + ' client(s) ?' + (cm.checked ? '\n' + (mailOk ? nm + ' e-mail(s) partiront réellement.' : 'Les e-mails ne partiront pas : l’envoi n’est pas encore configuré.') : '') + (cn.checked ? '\nUne notification apparaîtra dans leur espace.' : ''))) return;
        btnSend.disabled = true;
        api('/api/admin/communication', 'POST', { sujet: sj.value, corps: co.value, ids: c.map(function (x) { return x.compte_id; }), mail: cm.checked, notif: cn.checked, filtre: JSON.stringify(COMM.f) }).then(function (x) {
          btnSend.disabled = false;
          if (!x.j.ok) { flash('Envoi impossible : ' + (x.j.error === 'incomplet' ? 'champs manquants.' : x.j.error === 'canal' ? 'choisissez un canal.' : 'erreur.'), true); return; }
          flash(x.j.nb_mail ? x.j.nb_mail + ' e-mail(s) envoyé(s)' + (x.j.nb_notif ? ' et ' + x.j.nb_notif + ' notification(s).' : '.') : x.j.nb_notif ? x.j.nb_notif + ' notification(s) envoyée(s). Aucun e-mail (envoi non configuré).' : 'Aucun message envoyé.');
          COMM.sujet = COMM.corps = ''; commView();
        });
      } });
      holder.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h2', { text: '2. Le message' }),
        mailOk ? null : h('div', { class: 'infobox', style: 'margin-top:10px' }, h('b', { text: 'Envoi d’e-mails pas encore branché. ' }), 'Les notifications dans l’espace client fonctionnent déjà. Pour les e-mails, il faut relier un service d’envoi : dites-moi et je vous guide.'),
        h('div', { class: 'tools', style: 'margin:12px 0' }, h('label', { class: 'chk' }, cm, ' E-mail'), h('label', { class: 'chk' }, cn, ' Notification dans l’espace client')),
        h('div', { class: 'form' }, h('label', { class: 'wide' }, 'Sujet', sj), h('label', { class: 'wide' }, 'Message — vous pouvez écrire {prenom} (prénom) ou {nom} (nom complet)', co)), prev,
        h('div', { class: 'tools', style: 'margin-top:12px' }, h('button', { type: 'button', class: 'btn ghost', text: 'Aperçu', onclick: function () { var e = chosen()[0] || { nom: 'Marie Dupont' }; var p = function (t) { return t.replace(/\{prenom\}/gi, (e.nom || '').split(/\s+/)[0]).replace(/\{nom\}/gi, e.nom || ''); }; prev.hidden = !prev.hidden; prev.textContent = ''; prev.appendChild(h('b', { text: p(sj.value) || '(sans sujet)' })); prev.appendChild(h('div', { style: 'white-space:pre-wrap;margin-top:8px', text: p(co.value) })); prev.appendChild(h('div', { class: 'sub', style: 'margin-top:10px', text: 'Aperçu pour : ' + e.nom + ' · pied de message ajouté automatiquement : « Pour ne plus recevoir ces messages, répondez STOP. »' })); } }), btnSend)));
      holder.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h2', { text: 'Messages déjà envoyés' }), hist.length ? h('div', { class: 'tablewrap' }, h('table', null, h('thead', null, h('tr', null, ['Date', 'Sujet', 'Clients', 'E-mails', 'Notifications', 'Résultat'].map(function (t) { return h('th', { text: t }); }))), h('tbody', null, hist.map(function (x) { return h('tr', null, h('td', { text: dt(x.created_at) }), h('td', { text: x.sujet }), h('td', { text: String(x.nb) }), h('td', { text: String(x.nb_mail) }), h('td', { text: x.notif ? 'Oui' : 'Non' }), h('td', null, h('span', { class: 'pill ' + (x.statut === 'envoye' ? 'ok' : x.statut === 'notif_seule' ? 'pri' : 'warn'), text: { envoye: 'E-mails envoyés', notif_seule: 'Notifications seules', mail_non_configure: 'E-mail non configuré', partiel: 'Envoi partiel', echec: 'Échec' }[x.statut] || x.statut }))); })))) : h('p', { class: 'empty', text: 'Aucun message envoyé pour le moment.' })));
      drawList();
    });
  }

  /* ===== À traiter, tâches, suivi, avis, visites, sauvegarde ===== */
  var STATUTS_SITE = ['nouvelle', 'en_creation', 'apercu', 'en_ligne', 'hesite', 'a_rappeler', 'plus_tard', 'sans_reponse', 'trop_cher', 'concurrent', 'refusee', 'abandonnee'];
  var fd = function (iso) { return iso ? dOnly(String(iso).slice(0, 10)) : '—'; };
  var NIV = { urgent: ['Urgent', 'bad'], normal: ['À faire', 'warn'] };
  var CLE_ICO = { dossier_complet: 'file', nouvelle: 'file', creation: 'repeat', mettre_en_ligne: 'globe', ajustements: 'alert', relance: 'msg', relance15: 'alert', modif: 'repeat', resiliation: 'out', plainte: 'alert', impaye: 'euro', rappel: 'msg', tache: 'check', avis: 'trend' };
  function taskRow(t, after) {
    var cb = h('input', { type: 'checkbox', checked: t.fait ? '' : null, 'aria-label': 'Marquer comme fait : ' + t.titre });
    cb.addEventListener('change', function () { api('/api/admin/tache-fait', 'POST', { id: t.id, fait: cb.checked }).then(function (x) { if (!x.j.ok) { flash('Échec.', true); cb.checked = !cb.checked; } else after(); }); });
    return h('li', { class: 'task' + (t.fait ? ' done' : '') }, h('label', null, cb, h('span', null, h('b', { text: t.titre }), t.detail ? h('small', { text: t.detail }) : null, h('small', { class: 'meta', text: [t.nom || null, t.echeance ? 'pour le ' + fd(t.echeance) : null, t.fait && t.fait_at ? 'fait le ' + fd(t.fait_at) : null].filter(Boolean).join(' · ') }))),
      h('button', { type: 'button', class: 'btn sm ghost', text: 'Supprimer', 'aria-label': 'Supprimer la tâche ' + t.titre, onclick: function () { api('/api/admin/tache-suppr', 'POST', { id: t.id }).then(function () { after(); }); } }));
  }
  function taskForm(compteId, after) {
    var ti = h('input', { type: 'text', maxlength: '140', placeholder: 'Ex. : rappeler pour les photos', 'aria-label': 'Titre de la tâche' }), de = h('textarea', { rows: '2', maxlength: '800', placeholder: 'Détails, information interne (facultatif)', 'aria-label': 'Détails' }), ec = h('input', { type: 'date', 'aria-label': 'Pour le (facultatif)' });
    var cs = null;
    if (compteId === undefined) { cs = h('select', { 'aria-label': 'Client concerné' }, h('option', { value: '', text: 'Aucun client en particulier' })); D.comptes.slice().sort(function (a, b) { return String(a.nom).localeCompare(b.nom); }).forEach(function (c) { cs.appendChild(h('option', { value: c.id, text: c.nom })); }); }
    var go2 = function () { if (!ti.value.trim()) { flash('Donnez un titre à la tâche.', true); ti.focus(); return; } api('/api/admin/tache', 'POST', { titre: ti.value, detail: de.value, echeance: ec.value || null, compte_id: compteId === undefined ? (cs.value || null) : compteId }).then(function (x) { if (x.j.ok) { flash('Tâche ajoutée.'); after(); } else flash('Impossible d’ajouter la tâche.', true); }); };
    ti.addEventListener('keydown', function (e) { if (e.key === 'Enter') go2(); });
    return h('div', { class: 'form tform' }, h('label', { class: 'wide' }, 'Nouvelle tâche', ti), h('label', { class: 'wide' }, 'Information interne', de), h('label', null, 'Pour le (facultatif)', ec), cs ? h('label', null, 'Client', cs) : null, h('div', { class: 'wide' }, h('button', { type: 'button', class: 'btn', text: 'Ajouter', onclick: go2 })));
  }
  function updToday() { return api('/api/admin/atraiter').then(function (r) { var b = $('#c-today'); if (b) b.textContent = r.j.ok && r.j.urgents ? String(r.j.urgents) : ''; return r; }); }
  function todayView() {
    main.textContent = ''; main.appendChild(head('À traiter aujourd’hui', new Date().toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }), []));
    var box = h('div'); main.appendChild(box); box.appendChild(h('p', { class: 'empty', text: 'Chargement…' }));
    updToday().then(function (r) {
      box.textContent = '';
      if (!r.j.ok) { box.appendChild(h('p', { class: 'empty', text: 'Impossible de charger la liste.' })); return; }
      var items = r.j.items, ur = items.filter(function (i) { return i.niveau === 'urgent'; }), no = items.filter(function (i) { return i.niveau !== 'urgent'; });
      box.appendChild(h('div', { class: 'cf-g3', style: 'margin-bottom:16px' }, [[ur.length, 'urgent' + (ur.length > 1 ? 's' : ''), ur.length ? 'bad' : 'ok'], [no.length, 'à faire', no.length ? 'warn' : 'ok'], [items.length, 'au total', '']].map(function (k) { return h('div', { class: 'card kpi2' }, h('b', { class: k[2], text: String(k[0]) }), h('span', { text: k[1] })); })));
      var list = function (title, arr) {
        if (!arr.length) return null;
        return h('div', { class: 'card', style: 'margin-bottom:16px' }, h('h2', { text: title + ' (' + arr.length + ')' }), h('ul', { class: 'todol' }, arr.map(function (i) {
          var open2 = function () { if (i.compte_id) { mark('clients'); top(function () { detail(i.compte_id, i.cle === 'avis' || i.cle === 'dossier_complet' || i.cle === 'ajustements' || i.cle === 'resiliation' || i.cle === 'rappel' || i.cle === 'tache' || i.cle === 'nouvelle' || i.cle === 'creation' || i.cle === 'mettre_en_ligne' ? 'suivi' : 'apercu'); }); } };
          return h('li', null, h('span', { class: 'cf-ji ' + (i.niveau === 'urgent' ? 'bad' : 'warn') }, ico(CLE_ICO[i.cle] || 'alert', 16)), h('div', { class: 'tt' }, h('b', { text: i.titre }), i.detail ? h('small', { text: i.detail }) : null, h('small', { class: 'meta', text: [i.nom, i.date ? fd(i.date) : null].filter(Boolean).join(' · ') })),
            i.compte_id ? h('button', { type: 'button', class: 'btn sm', text: 'Ouvrir', 'aria-label': 'Ouvrir la fiche de ' + i.nom, onclick: open2 }) : null);
        })));
      };
      if (!items.length) box.appendChild(h('div', { class: 'card' }, h('h2', { text: 'Tout est à jour' }), h('p', { class: 'sub', text: 'Rien à traiter pour le moment. Profitez-en pour prospecter ou ajouter une tâche ci-dessous.' })));
      [list('Urgent', ur), list('À faire', no)].forEach(function (n) { if (n) box.appendChild(n); });
      var tasks = h('div', { class: 'card' }, h('h2', { text: 'Toutes mes tâches' }));
      var tl = h('div'); tasks.appendChild(tl); tasks.appendChild(taskForm(undefined, function () { todayView(); }));
      box.appendChild(tasks);
      api('/api/admin/taches').then(function (x) { var l = x.j.taches || []; tl.appendChild(l.length ? h('ul', { class: 'tasks' }, l.map(function (t) { return taskRow(t, function () { todayView(); }); })) : h('p', { class: 'empty', text: 'Aucune tâche. Ajoutez-en une ci-dessous.' })); });
    });
  }

  function suiviTab(body, c, d, card, setTab) {
    var box = h('div'); body.appendChild(box); box.appendChild(h('p', { class: 'empty', text: 'Chargement…' }));
    var redo = function () { loadAll().then(function () { updToday(); setTab('suivi'); }); };
    Promise.all([api('/api/admin/parcours?compte_id=' + c.id), api('/api/admin/taches?compte_id=' + c.id)]).then(function (rr) {
      var P2 = rr[0].j, T = rr[1].j.taches || []; box.textContent = '';
      if (!P2.ok) { box.appendChild(h('p', { class: 'empty', text: 'Impossible de charger ce suivi.' })); return; }
      var g = function (kids) { return h('div', { class: 'cf-g2' }, kids); };
      /* tâches */
      var tl = T.length ? h('ul', { class: 'tasks' }, T.map(function (t) { return taskRow(t, function () { setTab('suivi'); }); })) : h('p', { class: 'empty', text: 'Aucune tâche pour ce client.' });
      var cTasks = card('Notes et tâches', 'check', null, h('div', null, h('p', { class: 'sub', text: 'Ce que vous devez faire ou retenir pour ce client. Cochez quand c’est fait. Seul vous voyez ces notes.' }), tl, taskForm(c.id, function () { setTab('suivi'); })));
      /* suivi commercial */
      var ss = d ? sel(STATUTS_SITE, d.statut) : null, ra = h('input', { type: 'date', value: P2.suivi.rappel_le || '', 'aria-label': 'Date du rappel' }), rm = h('input', { type: 'text', maxlength: '200', value: P2.suivi.motif || '', placeholder: 'Ex. : veut réfléchir, rappeler après les vacances', 'aria-label': 'Note de rappel' });
      var cSuivi = card('Suivi commercial', 'trend', null, h('div', null, h('p', { class: 'sub', text: 'Où en est ce prospect ? Choisissez un statut, et programmez un rappel si besoin : il apparaîtra dans « À traiter aujourd’hui ».' }),
        h('div', { class: 'form' }, ss ? h('label', { class: 'wide' }, 'Statut du prospect', ss) : h('p', { class: 'sub', text: 'Aucune demande de site pour le moment.' }), h('label', null, 'Rappeler le', ra), h('label', null, 'Note', rm)),
        h('button', { type: 'button', class: 'btn', text: 'Enregistrer le suivi', onclick: function () {
          var p1 = d && ss.value !== d.statut ? api('/api/admin/demande', 'POST', { id: d.id, statut: ss.value }) : Promise.resolve({ j: { ok: true } });
          p1.then(function (x) { if (!x.j.ok) { flash('Échec du changement de statut.', true); return; } return api('/api/admin/suivi', 'POST', { compte_id: c.id, rappel_le: ra.value, motif: rm.value }).then(function (y) { flash(y.j.ok ? 'Suivi enregistré.' : 'Échec.', !y.j.ok); if (y.j.ok) redo(); }); });
        } })));
      box.appendChild(g([cTasks, cSuivi]));
      /* dossier */
      var dos = P2.dossier || {}, labs = { description: 'Présentation', horaires: 'Horaires', adresse_pub: 'Adresse', tel_pub: 'Téléphone', email_pub: 'E-mail', services: 'Prestations et tarifs', reseaux: 'Réseaux', couleurs: 'Couleurs et style', slogan: 'Slogan', domaine_choisi: 'Domaine souhaité', remarques: 'Remarques' };
      var kvs = Object.keys(labs).map(function (k) { return dos[k] ? h('div', null, h('dt', { text: labs[k] }), h('dd', { style: 'white-space:pre-wrap', text: dos[k] })) : null; }).filter(Boolean);
      var fl = (P2.fichiers || []).map(function (f) { var img = /^image\//.test(f.mime); return h('li', { class: 'fich' }, img ? h('img', { src: '/api/admin/fichier?id=' + f.id, alt: f.nom, width: '56', height: '56', loading: 'lazy' }) : h('span', { class: 'fico', text: 'PDF' }), h('div', null, h('b', { text: f.nom }), h('small', { text: f.categorie + ' · ' + Math.max(1, Math.round(f.taille / 1024)) + ' Ko' })), h('a', { class: 'btn sm ghost', href: '/api/admin/fichier?id=' + f.id, target: '_blank', rel: 'noopener', text: 'Ouvrir' }), h('a', { class: 'btn sm ghost', href: '/api/admin/fichier?id=' + f.id, download: f.nom, text: 'Télécharger' })); });
      var cDos = card('Dossier du client', 'file', dos._termine ? h('span', { class: 'pill ok', text: 'Complet le ' + fd(dos._termine) }) : h('span', { class: 'pill warn', text: P2.manquants.length ? 'Il manque : ' + P2.manquants.join(', ') : 'Pas encore terminé' }),
        h('div', null, kvs.length ? h('dl', { class: 'cf-kv' }, kvs) : h('p', { class: 'empty', text: 'Le client n’a rien rempli pour le moment.' }), h('h3', { style: 'margin-top:14px', text: 'Fichiers (' + fl.length + ')' }), fl.length ? h('ul', { class: 'fichs' }, fl) : h('p', { class: 'empty', text: 'Aucun fichier.' })));
      /* aperçu */
      var rt = P2.retours || [];
      var cRet = card('Retours sur l’aperçu', 'alert', null, rt.length ? h('ul', { class: 'tasks' }, rt.map(function (r) { return h('li', { class: 'task' }, h('div', { style: 'flex:1' }, h('b', { text: r.type === 'valide' ? 'Aperçu validé par le client' : 'Ajustements demandés' }), r.message ? h('small', { style: 'white-space:pre-wrap', text: r.message }) : null, h('small', { class: 'meta', text: fd(r.created_at) + (r.statut === 'traite' ? ' · traité' : '') })),
        r.statut === 'a_traiter' ? h('button', { type: 'button', class: 'btn sm', text: r.type === 'valide' ? 'Marquer vu' : 'Marquer comme traité', onclick: function () { api('/api/admin/retour-traite', 'POST', { id: r.id }).then(function (x) { flash(x.j.ok ? (r.type === 'valide' ? 'Noté.' : 'Marqué traité : le client est prévenu.') : 'Échec.', !x.j.ok); if (x.j.ok) redo(); }); } }) : null); })) : h('p', { class: 'empty', text: 'Aucun retour pour le moment.' }));
      box.appendChild(g([cDos, cRet]));
      /* résiliation */
      var rs = P2.resiliations || [], MO = { prix: 'Le prix', plus_besoin: 'N’en a plus besoin', insatisfait: 'Insatisfait', fermeture: 'Ferme son commerce', autre: 'Autre' };
      var cRes = card('Demandes de résiliation', 'out', null, rs.length ? h('ul', { class: 'tasks' }, rs.map(function (r) {
        var set = function (st, msg) { return h('button', { type: 'button', class: 'btn sm ' + (st === 'traitee' ? '' : 'ghost'), text: msg, onclick: function () { api('/api/admin/resiliation-statut', 'POST', { id: r.id, statut: st }).then(function (x) { flash(x.j.ok ? 'Mis à jour.' : 'Échec.', !x.j.ok); if (x.j.ok) redo(); }); } }); };
        return h('li', { class: 'task' }, h('div', { style: 'flex:1' }, h('b', { text: (MO[r.motif] || 'Motif non précisé') + ' · effet le ' + fd(r.effet) + (r.decale ? ' (préavis dépassé, décalée d’un an)' : '') }), r.message ? h('small', { style: 'white-space:pre-wrap', text: r.message }) : null, h('small', { class: 'meta', text: 'Demandée le ' + fd(r.created_at) + ' · ' + ({ demandee: 'à traiter', traitee: 'traitée', refusee: 'refusée', annulee: 'annulée par le client' }[r.statut] || r.statut) })),
          r.statut === 'demandee' ? h('span', { class: 'tools' }, set('traitee', 'Marquer traitée'), set('refusee', 'Refuser')) : r.statut === 'traitee' || r.statut === 'refusee' ? set('demandee', 'Remettre à traiter') : null);
      })) : h('p', { class: 'empty', text: 'Aucune demande de résiliation. La résiliation de l’abonnement se fait dans l’onglet Abonnement : la demande du client sera alors marquée traitée automatiquement.' }));
      /* avis */
      var av = P2.avis, cAvis = card('Avis du client', 'trend', av ? h('span', { class: 'pill ' + (av.statut === 'publie' ? 'ok' : av.statut === 'refuse' ? 'bad' : 'warn'), text: { publie: 'Publié', refuse: 'Refusé', en_attente: 'À modérer' }[av.statut] }) : null,
        av ? h('div', null, h('p', { class: 'stars', 'aria-label': av.note + ' sur 5', text: '★★★★★'.slice(0, av.note) + '☆☆☆☆☆'.slice(0, 5 - av.note) }), av.commentaire ? h('p', { style: 'white-space:pre-wrap', text: '« ' + av.commentaire + ' »' }) : h('p', { class: 'sub', text: 'Pas de commentaire.' }),
          h('div', { class: 'tools' }, [['publie', 'Publier', ''], ['refuse', 'Refuser', 'ghost'], ['en_attente', 'Remettre en attente', 'ghost']].filter(function (b) { return b[0] !== av.statut; }).map(function (b) { return h('button', { type: 'button', class: 'btn sm ' + b[2], text: b[1], onclick: function () { api('/api/admin/avis-statut', 'POST', { id: av.id, statut: b[0] }).then(function (x) { flash(x.j.ok ? 'Avis mis à jour.' : 'Échec.', !x.j.ok); if (x.j.ok) redo(); }); } }); }))) : h('p', { class: 'empty', text: 'Aucun avis pour le moment.' }));
      box.appendChild(g([cRes, cAvis]));
      /* parrainage */
      var pa = P2.parrainage, ci = h('input', { type: 'text', maxlength: '9', placeholder: 'DW-XXXXX', 'aria-label': 'Code de parrainage à appliquer', autocapitalize: 'characters' });
      var ST = { en_attente: 'En attente', valide: 'Validé', expire: 'Expiré' };
      var cPar = card('Parrainage', 'users', null, h('div', null, h('p', null, 'Code de ce client : ', h('b', { class: 'codep', text: pa.code })),
        pa.parrain ? h('p', { class: 'sub', text: 'Parrainé par ' + pa.parrain.nom + ' (code ' + pa.parrain.code + ') · ' + ST[pa.parrain.statut] }) : h('div', { class: 'form' }, h('label', { class: 'wide' }, 'Appliquer un code reçu par ce client (par téléphone, par exemple)', ci), h('div', { class: 'wide' }, h('button', { type: 'button', class: 'btn sm', text: 'Appliquer le code', onclick: function () { api('/api/admin/parrain-appliquer', 'POST', { compte_id: c.id, code: ci.value }).then(function (x) { var M = { inconnu: 'Code inconnu.', soi: 'C’est son propre code.', deja: 'Déjà parrainé.', client: 'Déjà client : un code est réservé aux nouveaux clients.', inactif: 'Le parrain n’a pas d’abonnement actif.' }; flash(x.j.ok ? 'Code appliqué.' : (M[x.j.error] || 'Échec.'), !x.j.ok); if (x.j.ok) redo(); }); } }))),
        h('h3', { style: 'margin-top:12px', text: 'Filleuls (' + pa.filleuls.length + ')' }), pa.filleuls.length ? h('ul', { class: 'tasks' }, pa.filleuls.map(function (f) { return h('li', { class: 'task' }, h('div', { style: 'flex:1' }, h('b', { text: f.nom }), h('small', { class: 'meta', text: 'Depuis le ' + fd(f.created_at) })), h('span', { class: 'pill ' + (f.statut === 'valide' ? 'ok' : f.statut === 'expire' ? 'bad' : 'warn'), text: ST[f.statut] })); })) : h('p', { class: 'empty', text: 'Aucun filleul.' }),
        h('h3', { style: 'margin-top:12px', text: 'Mois offerts' }), pa.credits.length ? h('ul', { class: 'tasks' }, pa.credits.map(function (cr) {
          var exp = !cr.utilise_at && cr.expire_at && cr.expire_at.slice(0, 10) < new Date().toISOString().slice(0, 10);
          return h('li', { class: 'task' + (cr.utilise_at || exp ? ' done' : '') }, h('div', { style: 'flex:1' }, h('b', { text: '1 mois offert (' + (cr.origine === 'filleul' ? 'bienvenue' : 'parrainage') + ')' }), h('small', { class: 'meta', text: cr.utilise_at ? 'Utilisé le ' + fd(cr.utilise_at) : exp ? 'Expiré le ' + fd(cr.expire_at) : 'Valable jusqu’au ' + fd(cr.expire_at) })), exp ? null : h('button', { type: 'button', class: 'btn sm ' + (cr.utilise_at ? 'ghost' : ''), text: cr.utilise_at ? 'Remettre disponible' : 'Marquer utilisé (déduit d’une facture)', onclick: function () { api('/api/admin/credit-utilise', 'POST', { id: cr.id, utilise: !cr.utilise_at }).then(function (x) { if (x.j.ok) redo(); }); } }));
        })) : h('p', { class: 'empty', text: 'Aucun mois offert.' })));
      box.appendChild(cPar);
    });
  }

  function avisView() {
    main.textContent = ''; main.appendChild(head('Avis clients', 'Relisez, publiez ou refusez. Seuls les avis publiés apparaissent sur la page d’accueil.', []));
    var box = h('div', { class: 'card' }); main.appendChild(box); box.appendChild(h('p', { class: 'empty', text: 'Chargement…' }));
    api('/api/admin/avis').then(function (r) {
      box.textContent = ''; var l = r.j.avis || [];
      if (!l.length) { box.appendChild(h('p', { class: 'empty', text: 'Aucun avis pour le moment. Les clients sont invités à en donner un quand leur site passe en ligne.' })); return; }
      box.appendChild(h('ul', { class: 'tasks' }, l.map(function (a) {
        var set = function (st, t, cls) { return h('button', { type: 'button', class: 'btn sm ' + (cls || ''), text: t, onclick: function () { api('/api/admin/avis-statut', 'POST', { id: a.id, statut: st }).then(function (x) { flash(x.j.ok ? 'Avis mis à jour.' : 'Échec.', !x.j.ok); if (x.j.ok) { updToday(); avisView(); } }); } }); };
        return h('li', { class: 'task' }, h('div', { style: 'flex:1' }, h('b', { text: ('★★★★★'.slice(0, a.note) + '☆☆☆☆☆'.slice(0, 5 - a.note)) + '  ' + a.nom + (a.commerce ? ', ' + a.commerce : '') }), a.commentaire ? h('small', { style: 'white-space:pre-wrap', text: '« ' + a.commentaire + ' »' }) : null, h('small', { class: 'meta', text: fd(a.created_at) })),
          h('span', { class: 'pill ' + (a.statut === 'publie' ? 'ok' : a.statut === 'refuse' ? 'bad' : 'warn'), text: { publie: 'Publié', refuse: 'Refusé', en_attente: 'À modérer' }[a.statut] }),
          h('span', { class: 'tools' }, a.statut !== 'publie' ? set('publie', 'Publier') : null, a.statut !== 'refuse' ? set('refuse', 'Refuser', 'ghost') : null));
      })));
    });
  }

  function outilsView() {
    main.textContent = ''; main.appendChild(head('Visites et sauvegarde', 'La fréquentation du site, et une copie de vos données.', []));
    var vis = h('div', { class: 'card' }, h('h2', { text: 'Visites du site public (30 derniers jours)' }), h('p', { class: 'empty', text: 'Chargement…' })); main.appendChild(vis);
    api('/api/admin/visites').then(function (r) {
      vis.textContent = ''; vis.appendChild(h('h2', { text: 'Visites du site public (30 derniers jours)' })); var j = r.j; if (!j.ok) { vis.appendChild(h('p', { class: 'empty', text: 'Impossible de charger les visites.' })); return; }
      vis.appendChild(h('p', { class: 'sub', text: 'Chaque page vue est comptée une fois, sans cookie et sans aucune donnée personnelle. Les visiteurs qui refusent le suivi (« Ne pas me suivre ») et les robots ne sont pas comptés, donc les chiffres sont un peu inférieurs à la réalité.' }));
      vis.appendChild(h('div', { class: 'cf-g3', style: 'margin:12px 0' }, [[j.total7, 'pages vues sur 7 jours'], [j.total30, 'pages vues sur 30 jours'], [j.jours.length ? Math.round(j.total30 / 30 * 10) / 10 : 0, 'par jour en moyenne']].map(function (k) { return h('div', { class: 'card kpi2' }, h('b', { text: num(k[0]) }), h('span', { text: k[1] })); })));
      if (!j.pages.length) { vis.appendChild(h('p', { class: 'empty', text: 'Aucune visite enregistrée pour le moment.' })); return; }
      var max = Math.max.apply(null, j.jours.map(function (x) { return x.n; }).concat([1]));
      vis.appendChild(h('div', { class: 'vbars', role: 'img', 'aria-label': 'Pages vues par jour' }, j.jours.map(function (x) { return h('i', { style: 'height:' + Math.max(4, Math.round(x.n / max * 100)) + '%', title: fd(x.jour) + ' : ' + x.n }); })));
      vis.appendChild(h('div', { class: 'tablewrap' }, h('table', null, h('thead', null, h('tr', null, h('th', { text: 'Page' }), h('th', { class: 'n', text: 'Pages vues' }))), h('tbody', null, j.pages.map(function (p) { return h('tr', null, h('td', { text: p.page }), h('td', { class: 'n', text: num(p.n) })); })))));
    });
    var sv = h('div', { class: 'card', style: 'margin-top:16px' }, h('h2', { text: 'Sauvegarde des données' }), h('p', { class: 'sub', text: 'Téléchargez une copie de toutes vos données (clients, demandes, abonnements, tâches, avis…). Faites-le régulièrement, par exemple chaque semaine, et gardez le fichier en lieu sûr.' }),
      h('div', { class: 'warnbox', style: 'margin:10px 0' }, h('div', null, h('b', { text: 'Ce fichier est confidentiel.' }), h('div', { text: 'Il contient les données de vos clients et les mots de passe chiffrés. Ne l’envoyez à personne et ne le laissez pas sur un ordinateur partagé.' }))));
    var msg = h('p', { class: 'sub', role: 'status' });
    var dl = function (lourd) { msg.textContent = 'Préparation de la sauvegarde…'; fetch('/api/admin/sauvegarde' + (lourd ? '?medias=1' : ''), { credentials: 'same-origin' }).then(function (r) { if (!r.ok) throw new Error('http'); return r.blob(); }).then(function (b) { var a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = 'sauvegarde-devanture-web-' + new Date().toISOString().slice(0, 10) + (lourd ? '-avec-fichiers' : '') + '.json'; document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000); msg.textContent = 'Sauvegarde téléchargée (' + Math.max(1, Math.round(b.size / 1024)) + ' Ko) le ' + new Date().toLocaleString('fr-FR') + '.'; }).catch(function () { msg.textContent = 'La sauvegarde a échoué. Réessayez dans un instant.'; }); };
    sv.appendChild(h('div', { class: 'tools', style: 'flex-wrap:wrap;gap:10px' }, h('button', { type: 'button', class: 'btn', text: 'Télécharger la sauvegarde', onclick: function () { dl(false); } }), h('button', { type: 'button', class: 'btn ghost', text: 'Avec les fichiers des clients (plus lourd)', onclick: function () { dl(true); } })));
    sv.appendChild(msg); sv.appendChild(h('p', { class: 'sub', text: 'En plus de cette copie, Cloudflare garde un historique récent de la base de données, qui permet de revenir en arrière depuis son tableau de bord en cas de fausse manipulation.' }));
    main.appendChild(sv);
  }

  /* ===== navigation latérale ===== */
  var navb = { today: $('#n-today'), avis: $('#n-avis'), outils: $('#n-outils'), stats: $('#n-stats'), clients: $('#n-clients'), dem: $('#n-dem'), crea: $('#n-crea'), ligne: $('#n-ligne'), abo: $('#n-abo'), rev: $('#n-rev'), com: $('#n-com'), mdp: $('#n-mdp') };
  function mark(k) { Object.keys(navb).forEach(function (x) { if (x === k) navb[x].setAttribute('aria-current', 'page'); else navb[x].removeAttribute('aria-current'); }); }
  function go(k, fn) { navb[k].addEventListener('click', function () { mark(k); top(fn); }); }
  go('today', todayView); go('avis', avisView); go('outils', outilsView); go('stats', showStats); go('clients', clientsView); go('dem', pageDem); go('crea', pageCrea); go('ligne', pageLigne); go('abo', pageAbo); go('rev', revenuePage); go('com', commView); go('mdp', motDePasse);
  $('#n-out').addEventListener('click', function () { api('/api/deconnexion', 'POST').then(function () { location.href = '/connexion'; }); });

  api('/api/moi').then(function (r) {
    var gate = $('#gate');
    if (r.s === 401) { gate.textContent = ''; gate.appendChild(h('h1', { text: 'Espace administrateur' })); gate.appendChild(h('p', { text: 'Connectez-vous avec votre compte administrateur.' })); gate.appendChild(h('a', { class: 'btn', href: '/connexion', text: 'Se connecter' })); return; }
    if (!r.j.admin) { gate.textContent = ''; gate.appendChild(h('h1', { text: 'Accès refusé' })); gate.appendChild(h('p', { text: 'Cet espace est réservé à l’administrateur.' })); gate.appendChild(h('a', { class: 'btn', href: '/', text: 'Retour au site' })); return; }
    gate.hidden = true; $('#app').hidden = false; main.appendChild(h('p', { class: 'empty', text: 'Chargement…' }));
    loadAll().then(function () { updBadges(); mark('today'); top(todayView); }).catch(function () { main.textContent = ''; main.appendChild(h('p', { class: 'empty', text: 'Impossible de charger les données. Réessayez dans un instant.' })); });
  }).catch(function () { $('#gate').textContent = 'Connexion impossible pour le moment.'; });
})();
