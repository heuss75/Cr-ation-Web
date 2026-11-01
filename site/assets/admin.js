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
  function detail(id) {
    api('/api/admin/compte?id=' + id).then(function (r) {
      if (!r.j.ok) { flash('Compte introuvable.', true); return; }
      var c = r.j.compte, ab = r.j.abonnement;
      main.textContent = '';
      main.appendChild(head(c.nom, c.email + ' · inscrit le ' + dt(c.created_at), [h('button', { type: 'button', class: 'btn ghost', text: '← Clients', onclick: function () { top(clientsView); } }), h('button', { type: 'button', class: 'btn', text: 'Voir en tant que ce client', onclick: function () { impersonate(c.id); } })]));
      actionsCard(c, r.j.demandes);
      var g = h('div', { class: 'grid g2' });
      var dc = h('div', { class: 'card' }, h('h2', { text: 'Demandes de site (' + r.j.demandes.length + ')' }));
      if (!r.j.demandes.length) dc.appendChild(h('p', { class: 'empty', text: 'Aucune demande.' }));
      r.j.demandes.forEach(function (d) {
        var sl = sel(['nouvelle', 'en_creation', 'apercu', 'en_ligne', 'abandonnee'], d.statut);
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
  function sel(opts, val) { var e = h('select'); opts.forEach(function (o) { var op = h('option', { value: o, text: lab(o) }); if (o === val) op.selected = true; e.appendChild(op); }); return e; }
  function head(title, sub, extra) { return h('div', { class: 'top' }, h('div', { class: 'hello' }, h('h1', { text: title }), sub ? h('p', { text: sub }) : null), h('div', { class: 'tools' }, extra || [])); }

  /* ===== données, navigation ===== */
  var PRIX = { essentiel: 60, pro: 100 }, MAILP = 4;
  var Sx = null, D = null, IX = null, cur = null, par = null;
  var prixAbo = function (a) { return (PRIX[a.formule] || 0) + MAILP * (a.mails_sup || 0); };
  var counts = function (a) { return a.statut === 'actif' || a.statut === 'impaye'; };
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
    abonnements: { l: 'Abonnements', rows: function () { return D.abonnements.map(aRow); }, date: 'debut', filt: [['formule', 'Formule', ['essentiel', 'pro']], ['abo', 'Statut', ['actif', 'impaye', 'suspendu', 'resilie']]] },
    demandes: { l: 'Demandes de site', rows: function () { return D.demandes.map(dRow); }, date: 'date', filt: [['formule', 'Formule', ['essentiel', 'pro']], ['site', 'Statut', ['nouvelle', 'en_creation', 'apercu', 'en_ligne', 'abandonnee']]] },
    plaintes: { l: 'Plaintes', rows: function () { return D.plaintes.map(pRow); }, date: 'date', filt: [['pl', 'Statut', ['ouverte', 'en_cours', 'resolue']]] },
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
  function listView(dsKey, title, sub, pred, extra) {
    open(function () {
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
    function draw() {
      var q = box.value.trim().toLowerCase(), list = rows.filter(function (r) { return !q || JSON.stringify(r).toLowerCase().indexOf(q) >= 0; });
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
    return h('div', { class: 'card' }, h('div', { class: 'tbar' }, box, count), body);
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
  var REV = { mode: 'mois', depuis: '12' };
  var mKey = function (d) { return d.slice(0, 7); };
  function revCalc() {
    var nowM = mKey(new Date().toISOString()), abos = D.abonnements;
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
  var REVCOLS = [C('periode', 'Période'), C('ca', 'Chiffre d’affaires HT', 'eur'), C('ess', 'dont Essentiel', 'eur'), C('pro', 'dont Pro', 'eur'), C('mails', 'dont mails pro', 'eur'), C('nouveaux', 'Nouveaux', 'int'), C('resilies', 'Résiliés', 'int'), C('actifs', 'Abonnés en fin de période', 'int'), C('impayes', 'Impayés (en cours)', 'eur')];
  function revBars(rows) {
    var W = 640, H = 210, Lm = 46, B = 28, T = 10, iw = W - Lm - 8, ih = H - B - T;
    var max = Math.max.apply(null, rows.map(function (r) { return r.ca; }).concat([100])), step = Math.pow(10, Math.floor(Math.log10(max))), top = Math.ceil(max / step) * step;
    var svg = s('svg', { class: 'chart', viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Chiffre d’affaires par période' });
    [0, 1, 2, 3].forEach(function (k) { var y = T + (ih * k) / 3; svg.appendChild(s('line', { x1: Lm, x2: W - 8, y1: y, y2: y, class: 'gl', 'stroke-dasharray': '3 4' })); var t = s('text', { x: 0, y: y + 3 }); t.textContent = Math.round(top - (top * k) / 3).toLocaleString('fr-FR') + ' €'; svg.appendChild(t); });
    var bw = iw / rows.length, pw = Math.min(46, bw * 0.62);
    rows.forEach(function (r, i) {
      var x = Lm + bw * i + (bw - pw) / 2, y = T + ih;
      [['ess', COL.pri], ['pro', COL.sky], ['mails', COL.ok]].forEach(function (p) { var hh = (r[p[0]] / top) * ih; if (hh <= 0) return; y -= hh; var rc = s('rect', { x: x, y: y, width: pw, height: hh, rx: 3, fill: p[1] }); var tt = s('title'); tt.textContent = r.periode + ' · ' + { ess: 'Essentiel', pro: 'Pro', mails: 'Mails pro' }[p[0]] + ' : ' + eur(r[p[0]]); rc.appendChild(tt); svg.appendChild(rc); });
      if (rows.length <= 14 || i % 2 === 0) { var t = s('text', { x: x + pw / 2, y: H - 8, 'text-anchor': 'middle' }); t.textContent = r.periode; svg.appendChild(t); }
    });
    return svg;
  }
  function revenueBlock() {
    var box = h('div', { class: 'card', id: 'revenus' });
    function draw() {
      box.textContent = '';
      var rows = revCalc(), tot = rows.reduce(function (a, r) { return a + r.ca; }, 0), nv = rows.reduce(function (a, r) { return a + r.nouveaux; }, 0), rs = rows.reduce(function (a, r) { return a + r.resilies; }, 0);
      var seg = function (key, opts, val, fn) { return h('div', { class: 'seg' }, opts.map(function (o) { return h('button', { type: 'button', text: o[1], 'aria-pressed': String(val === o[0]), onclick: function () { fn(o[0]); draw(); } }); })); };
      box.appendChild(h('div', { class: 'tbar' }, h('div', null, h('h2', { text: 'Revenus' }), h('p', { class: 'sub', text: 'Détail du chiffre d’affaires hors taxes, calculé à partir des abonnements saisis.' })),
        h('div', { class: 'tools' }, seg('mode', [['mois', 'Mensuel'], ['trimestre', 'Trimestriel'], ['annee', 'Annuel']], REV.mode, function (v) { REV.mode = v; }), seg('depuis', [['6', '6 mois'], ['12', '12 mois'], ['24', '24 mois'], ['tout', 'Tout']], REV.depuis, function (v) { REV.depuis = v; }),
          h('button', { type: 'button', class: 'btn ghost sm', text: '⬇ CSV', onclick: function () { download('revenus-' + REV.mode + '-' + stamp() + '.csv', csvText(REVCOLS, rows)); flash('Export des revenus téléchargé.'); } }))));
      box.appendChild(mini([['CA sur la période', eur(tot)], ['Revenu mensuel actuel', eur(Sx.abonnements.mrr)], ['Revenu annuel prévu', eur(Sx.abonnements.arr)], ['Nouveaux abonnés', String(nv)], ['Résiliations', String(rs)], ['Panier moyen', eur(Sx.abonnements.panier)]]));
      box.appendChild(h('div', { class: 'legendline' }, h('span', null, h('i', { style: 'background:' + COL.pri }), 'Essentiel'), h('span', null, h('i', { style: 'background:' + COL.sky }), 'Pro'), h('span', null, h('i', { style: 'background:' + COL.ok }), 'Mails pro')));
      box.appendChild(revBars(rows));
      var tb = h('tbody');
      rows.slice().reverse().forEach(function (r) { var tr = h('tr', null, REVCOLS.map(function (c) { return h('td', null, cell(c, r)); })); click(tr, function () { var abos = r.abos; open(function () { main.textContent = ''; var rr = abos.map(aRow); main.appendChild(head('Abonnements · ' + r.periode, rr.length + ' abonnement(s) facturé(s) sur la période', [backBtn(), h('button', { type: 'button', class: 'btn', text: '⬇ Exporter (CSV)', onclick: function () { download('abonnements-' + r.periode.replace(/\s/g, '-') + '.csv', csvText(COLS.abonnements, rr)); } })])); main.appendChild(dataTable('abonnements', rr)); }); }); tb.appendChild(tr); });
      box.appendChild(h('div', { class: 'tablewrap' }, h('table', null, h('thead', null, h('tr', null, REVCOLS.map(function (c) { return h('th', { text: c.l }); }))), tb)));
      box.appendChild(h('p', { class: 'sub', style: 'margin-top:10px', text: 'Les mails pro supplémentaires sont comptés au nombre actuel (pas d’historique). Les abonnements suspendus ne sont pas facturés.' }));
    }
    draw(); return box;
  }

  /* ===== tableau de bord ===== */
  function dashboard() {
    var c = Sx.comptes, d = Sx.demandes, a = Sx.abonnements, p = Sx.plaintes, cv = Sx.conversion, out = h('div'), st = {};
    d.statut.forEach(function (x) { st[x.statut] = x.n; });
    var cA = function (t, f, sub) { return function () { L.abos(t, f, sub); }; };
    var cC = function (t, f) { return function () { L.comptes(t, f); }; };
    var cD = function (t, f) { return function () { L.demandes(t, f); }; };
    var cP = function (t, f) { return function () { L.plaintes(t, f); }; };
    var actifsF = function (r) { return r.abo === 'actif' || r.abo === 'impaye'; };
    out.appendChild(h('div', { class: 'grid g4' },
      hero('c3', 'euro', eur(a.mrr), 'Revenu mensuel (HT)', a.nouveaux30 ? '+' + a.nouveaux30 + ' ce mois' : null, false, function () { open(revenuePage); }),
      hero('c1', 'users', num(c.total), 'Inscrits', c.j7 ? '+' + c.j7 + ' / 7 j' : null, false, cC('Tous les inscrits')),
      hero('c2', 'file', num(d.total), 'Demandes de site', d.j7 ? '+' + d.j7 + ' / 7 j' : null, false, cD('Toutes les demandes de site')),
      hero('c4', 'repeat', num(a.actifs), 'Abonnements actifs', a.resilies30 ? '-' + a.resilies30 + ' résilié(s)' : null, true, cA('Abonnements actifs', actifsF))));
    out.appendChild(h('div', { class: 'sec', text: 'Croissance' }));
    out.appendChild(h('div', { class: 'grid g2' },
      card('Inscriptions', '30 derniers jours · ' + c.j30 + ' nouveau(x) · cliquez pour la liste', (function () { var w = h('div', null, area(c.jours)); return click(w, cC('Inscrits des 30 derniers jours', recent('inscrit', 30))); })()),
      card('Tunnel de conversion', 'De l’inscription à l’abonnement', funnel([
        { l: 'Inscrits', n: c.total, c: COL.pri, p: 100, fn: cC('Tous les inscrits') },
        { l: 'Ont fait une demande', n: Math.round(c.total * cv.inscritDemande / 100), c: COL.sky, p: cv.inscritDemande, fn: cC('Inscrits ayant fait une demande', function (r) { return r.demandes > 0; }) },
        { l: 'Abonnés', n: a.actifs + a.resiliesTotal, c: COL.ok, p: cv.demandeAbonne, fn: cA('Tous les abonnements (actifs et résiliés)', function () { return true; }) }]))));
    out.appendChild(h('div', { class: 'sec', text: 'Revenus et abonnements' }));
    out.appendChild(h('div', { class: 'grid g3' },
      card('Chiffre d’affaires', 'Hors taxes · cliquez pour le détail', mini([['Revenu annuel prévu', eur(a.arr), function () { open(revenuePage); }], ['Panier moyen', eur(a.panier), cA('Abonnements actifs', actifsF)], ['Taux de résiliation', a.churn + ' %', cA('Résiliés (30 j)', function (r) { return r.abo === 'resilie' && d10(r.fin) >= ago(30); })], ['Mails pro en plus', num(a.mailsSup), cA('Abonnements avec mails pro en plus', function (r) { return r.mails > 0; })]])),
      card('Formules', 'Abonnements actifs', donut([{ l: 'Essentiel', n: a.parFormule.essentiel || 0, c: COL.pri, fn: cA('Abonnements Essentiel actifs', function (r) { return actifsF(r) && r.formule === 'essentiel'; }) }, { l: 'Pro', n: a.parFormule.pro || 0, c: COL.sky, fn: cA('Abonnements Pro actifs', function (r) { return actifsF(r) && r.formule === 'pro'; }) }], String(a.actifs), 'abonnés')),
      card('Mouvements', '30 derniers jours', mini([
        ['Nouveaux', a.nouveaux30, cA('Nouveaux abonnés (30 j)', function (r) { return d10(r.debut) >= ago(30); })],
        ['Récurrents (+30 j)', a.recurrents, cA('Abonnés récurrents', function (r) { return r.abo === 'actif' && d10(r.debut) < ago(30); })],
        ['Résiliés (30 j)', a.resilies30, cA('Résiliations des 30 derniers jours', function (r) { return r.abo === 'resilie' && d10(r.fin) >= ago(30); })],
        ['Résiliés au total', a.resiliesTotal, cA('Toutes les résiliations', function (r) { return r.abo === 'resilie'; })],
        ['Impayés', a.impayes, cA('Abonnements impayés', function (r) { return r.abo === 'impaye'; })],
        ['Suspendus', a.suspendus, cA('Abonnements suspendus', function (r) { return r.abo === 'suspendu'; })]]))));
    out.appendChild(h('div', { class: 'sec', text: 'Sites en cours' }));
    var sF = function (k) { return cD('Demandes · ' + lab(k), function (r) { return r.site === k; }); };
    out.appendChild(h('div', { class: 'grid g3' },
      card('Avancement des sites', d.total + ' demande(s)', donut([{ l: 'À traiter', n: st.nouvelle || 0, c: COL.warn, fn: sF('nouvelle') }, { l: 'En création', n: st.en_creation || 0, c: COL.pri, fn: sF('en_creation') }, { l: 'Aperçu envoyé', n: st.apercu || 0, c: COL.sky, fn: sF('apercu') }, { l: 'En ligne', n: st.en_ligne || 0, c: COL.ok, fn: sF('en_ligne') }, { l: 'Abandonnées', n: st.abandonnee || 0, c: COL.gray, fn: sF('abandonnee') }], String(d.total), 'demandes')),
      card('Activité des demandeurs', 'Par type de commerce', bars(d.activite.map(function (x) { return { l: x.activite || '—', n: x.n, fn: cD('Demandes · ' + (x.activite || '—'), function (r) { return r.activite === x.activite; }) }; }))),
      card('Villes', 'D’où viennent les demandes', bars(d.ville.map(function (x) { return { l: x.ville, n: x.n, fn: cD('Demandes · ' + x.ville, function (r) { return (r.ville || '').toLowerCase() === x.ville.toLowerCase(); }) }; })))));
    out.appendChild(h('div', { class: 'sec', text: 'Clients et service' }));
    var pF = function (k) { return cP('Plaintes · ' + lab(k), function (r) { return r.pl === k; }); };
    out.appendChild(h('div', { class: 'grid g3' },
      card('Plaintes', p.total + ' au total · délai moyen ' + (p.delai_h == null ? '—' : p.delai_h + ' h'), donut([{ l: 'Ouvertes', n: p.ouvertes, c: COL.bad, fn: pF('ouverte') }, { l: 'En cours', n: p.en_cours, c: COL.warn, fn: pF('en_cours') }, { l: 'Résolues', n: p.resolues, c: COL.ok, fn: pF('resolue') }], String(p.total), 'plaintes')),
      card('Motifs de résiliation', null, bars(a.motifs.map(function (x) { return { l: x.motif, n: x.n, fn: cA('Résiliations · ' + x.motif, function (r) { return r.abo === 'resilie' && (r.motif || 'non précisé') === x.motif; }) }; }), 'Aucune résiliation.')),
      card('Provenance des demandes', null, bars(d.sources.map(function (x) { return { l: x.s, n: x.n, fn: cD('Demandes · ' + x.s, function (r) { return r.source === x.s; }) }; })))));
    out.appendChild(h('div', { class: 'grid g2', style: 'margin-top:16px' },
      card('Activité des visiteurs', 'Inscrits', mini([['Dernières 24 h', c.j1, cC('Inscrits des dernières 24 h', recent('inscrit', 1))], ['7 jours', c.j7, cC('Inscrits des 7 derniers jours', recent('inscrit', 7))], ['30 jours', c.j30, cC('Inscrits des 30 derniers jours', recent('inscrit', 30))], ['Connectés (7 j)', c.actifs7, cC('Connectés ces 7 derniers jours', recent('connexion', 7))], ['Connectés (24 h)', c.connectes, cC('Connectés ces dernières 24 h', recent('connexion', 1))], ['Sans demande', c.sansDemande, cC('Inscrits sans demande', function (r) { return !r.demandes; })]])),
      card('Événements (30 jours)', 'Journal du site', bars(Sx.divers.evenements30.map(function (x) { return { l: x.type.replace(/_/g, ' '), n: x.n, fn: function () { L.journal('Événements · ' + x.type.replace(/_/g, ' '), function (r) { return r.type === x.type.replace(/_/g, ' '); }); } }; }), 'Aucun événement.'))));
    return out;
  }
  function showStats() {
    var hr = new Date().getHours(), greet = hr < 18 ? 'Bonjour' : 'Bonsoir';
    main.textContent = '';
    main.appendChild(head(greet + ', Admin', new Date().toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }) + ' · cliquez sur n’importe quel chiffre ou graphique pour voir le détail.', [h('button', { type: 'button', class: 'btn ghost', text: 'Actualiser', onclick: function () { loadAll().then(function () { top(showStats); flash('Statistiques actualisées.'); }); } })]));
    main.appendChild(dashboard());
  }
  function revenuePage() { main.textContent = ''; main.appendChild(head('Revenus', 'Détail par mois, trimestre ou année', [backBtn()])); main.appendChild(revenueBlock()); }

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
      var cols = ['nom', 'inscrit', 'connexion', 'site', 'formule', 'abo', 'plaintes_ouvertes'].map(function (k) { return COLS.clients.filter(function (c) { return c.k === k; })[0]; });
      var tb = h('tbody');
      rows.slice(0, 500).forEach(function (r) {
        var tr = h('tr', null, cols.map(function (c) { return h('td', null, cell(c, r)); }), h('td', { class: 'acts' }, h('button', { type: 'button', class: 'btn sm', text: 'Voir en tant que', onclick: function (e) { e.stopPropagation(); impersonate(r.compte_id); } })));
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
        fSelect('site', 'Statut du site', yes(['nouvelle', 'en_creation', 'apercu', 'en_ligne', 'abandonnee']).concat([['aucune', 'Aucune demande']])),
        fSelect('plaintes', 'Plaintes', [['ouvertes', 'Avec plainte ouverte'], ['avec', 'Avec au moins une plainte'], ['aucune', 'Aucune plainte']]),
        fSelect('activite', 'Activité', distinct(all, 'activite')), fSelect('ville', 'Ville', distinct(all, 'ville')),
        fSelect('connexion', 'Dernière connexion', [['1', 'Dans les 24 h'], ['7', 'Dans les 7 jours'], ['30', 'Dans les 30 jours'], ['jamais', 'Jamais connecté']]),
        fSelect('mails', 'Mails pro', [['oui', 'Avec mails pro en plus']]), h('label', null, 'Inscrit après le', du), h('label', null, 'Inscrit avant le', au)));
      panel.appendChild(h('div', { class: 'tools' }, h('button', { type: 'button', class: 'btn', text: 'Appliquer', onclick: function () { draw(); flash(applyF(all).length + ' client(s) trouvé(s).'); } }), h('button', { type: 'button', class: 'btn ghost', text: 'Réinitialiser', onclick: function () { F = {}; qBox.value = ''; buildPanel(); draw(); } })));
    }
    fbtn.addEventListener('click', function () { var o = panel.hidden; panel.hidden = !o; fbtn.setAttribute('aria-expanded', String(o)); if (o) buildPanel(); });
    main.appendChild(head('Clients', 'Tous les comptes inscrits · cliquez sur une ligne pour ouvrir la fiche', [h('button', { type: 'button', class: 'btn', text: '⬇ Exporter', onclick: function () { exportDialog('clients'); } })]));
    main.appendChild(h('div', { class: 'card' }, h('div', { class: 'tbar' }, qBox, fbtn, count), panel, tbody));
    main.appendChild(h('div', { class: 'sec', text: 'Revenus' }));
    main.appendChild(revenueBlock());
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
      var filt = h('div', { class: 'fgrid' }, fs('formule', 'Formule', yes(['essentiel', 'pro'])), fs('abo', 'Abonnement', yes(['actif', 'impaye', 'suspendu', 'resilie']).concat([['aucun', 'Aucun abonnement']])), fs('site', 'Statut du site', yes(['nouvelle', 'en_creation', 'apercu', 'en_ligne', 'abandonnee']).concat([['aucune', 'Aucune demande']])), fs('plaintes', 'Plaintes', [['ouvertes', 'Avec plainte ouverte'], ['avec', 'Avec au moins une plainte'], ['aucune', 'Aucune plainte']]), fs('activite', 'Activité', distinct(all, 'activite')), fs('ville', 'Ville', distinct(all, 'ville')), fs('connexion', 'Dernière connexion', [['7', 'Dans les 7 jours'], ['30', 'Dans les 30 jours'], ['jamais', 'Jamais connecté']]));
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
        h('div', { class: 'form' }, h('label', { class: 'wide' }, 'Sujet', sj), h('label', { class: 'wide' }, 'Message — vous pouvez écrire {prenom} ou {nom}', co)), prev,
        h('div', { class: 'tools', style: 'margin-top:12px' }, h('button', { type: 'button', class: 'btn ghost', text: 'Aperçu', onclick: function () { var e = chosen()[0] || { nom: 'Marie Dupont' }; var p = function (t) { return t.replace(/\{prenom\}/gi, (e.nom || '').split(/\s+/)[0]).replace(/\{nom\}/gi, e.nom || ''); }; prev.hidden = !prev.hidden; prev.textContent = ''; prev.appendChild(h('b', { text: p(sj.value) || '(sans sujet)' })); prev.appendChild(h('div', { style: 'white-space:pre-wrap;margin-top:8px', text: p(co.value) })); prev.appendChild(h('div', { class: 'sub', style: 'margin-top:10px', text: 'Aperçu pour : ' + e.nom + ' · pied de message ajouté automatiquement : « Pour ne plus recevoir ces messages, répondez STOP. »' })); } }), btnSend)));
      holder.appendChild(h('div', { class: 'card', style: 'margin-top:16px' }, h('h2', { text: 'Messages déjà envoyés' }), hist.length ? h('div', { class: 'tablewrap' }, h('table', null, h('thead', null, h('tr', null, ['Date', 'Sujet', 'Clients', 'E-mails', 'Notifications', 'Résultat'].map(function (t) { return h('th', { text: t }); }))), h('tbody', null, hist.map(function (x) { return h('tr', null, h('td', { text: dt(x.created_at) }), h('td', { text: x.sujet }), h('td', { text: String(x.nb) }), h('td', { text: String(x.nb_mail) }), h('td', { text: x.notif ? 'Oui' : 'Non' }), h('td', null, h('span', { class: 'pill ' + (x.statut === 'envoye' ? 'ok' : x.statut === 'notif_seule' ? 'pri' : 'warn'), text: { envoye: 'E-mails envoyés', notif_seule: 'Notifications seules', mail_non_configure: 'E-mail non configuré', partiel: 'Envoi partiel', echec: 'Échec' }[x.statut] || x.statut }))); })))) : h('p', { class: 'empty', text: 'Aucun message envoyé pour le moment.' })));
      drawList();
    });
  }

  /* ===== navigation latérale ===== */
  var navb = { stats: $('#n-stats'), clients: $('#n-clients'), rev: $('#n-rev'), com: $('#n-com'), mdp: $('#n-mdp') };
  function mark(k) { Object.keys(navb).forEach(function (x) { if (x === k) navb[x].setAttribute('aria-current', 'page'); else navb[x].removeAttribute('aria-current'); }); }
  function go(k, fn) { navb[k].addEventListener('click', function () { mark(k); top(fn); }); }
  go('stats', showStats); go('clients', clientsView); go('rev', revenuePage); go('com', commView); go('mdp', motDePasse);
  $('#n-out').addEventListener('click', function () { api('/api/deconnexion', 'POST').then(function () { location.href = '/connexion'; }); });

  api('/api/moi').then(function (r) {
    var gate = $('#gate');
    if (r.s === 401) { gate.textContent = ''; gate.appendChild(h('h1', { text: 'Espace administrateur' })); gate.appendChild(h('p', { text: 'Connectez-vous avec votre compte administrateur.' })); gate.appendChild(h('a', { class: 'btn', href: '/connexion', text: 'Se connecter' })); return; }
    if (!r.j.admin) { gate.textContent = ''; gate.appendChild(h('h1', { text: 'Accès refusé' })); gate.appendChild(h('p', { text: 'Cet espace est réservé à l’administrateur.' })); gate.appendChild(h('a', { class: 'btn', href: '/', text: 'Retour au site' })); return; }
    gate.hidden = true; $('#app').hidden = false; main.appendChild(h('p', { class: 'empty', text: 'Chargement…' }));
    loadAll().then(function () { top(showStats); }).catch(function () { main.textContent = ''; main.appendChild(h('p', { class: 'empty', text: 'Impossible de charger les données. Réessayez dans un instant.' })); });
  }).catch(function () { $('#gate').textContent = 'Connexion impossible pour le moment.'; });
})();
