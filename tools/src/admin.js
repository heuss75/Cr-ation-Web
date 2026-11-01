/* Espace admin : statistiques, clients, abonnements, plaintes, connexion « en tant que ». Tout le texte venant de la base est inséré via textContent. */
(function () {
  'use strict';
  var root = document.getElementById('adm');
  if (!root) return;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  function h(tag, attrs) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'class') e.className = attrs[k]; else if (k === 'text') e.textContent = attrs[k];
      else if (k.slice(0, 2) === 'on') e.addEventListener(k.slice(2), attrs[k]); else if (attrs[k] !== null && attrs[k] !== undefined) e.setAttribute(k, attrs[k]);
    });
    (function add(list) {
      for (var i = 0; i < list.length; i++) {
        var c = list[i]; if (c === null || c === undefined || c === false) continue;
        if (Array.isArray(c)) add(c); else e.appendChild(typeof c === 'string' || typeof c === 'number' ? document.createTextNode(String(c)) : c);
      }
    })(Array.prototype.slice.call(arguments, 2));
    return e;
  }
  function api(path, method, body) {
    return fetch(path, { method: method || 'GET', credentials: 'same-origin', headers: body ? { 'content-type': 'application/json' } : {}, body: body ? JSON.stringify(body) : undefined })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { s: r.status, j: j }; }); });
  }
  var LBL = {
    nouvelle: 'Nouvelle demande', en_creation: 'En création', apercu: 'Aperçu envoyé', en_ligne: 'En ligne', abandonnee: 'Abandonnée',
    actif: 'Actif', impaye: 'Impayé', suspendu: 'Suspendu', resilie: 'Résilié', ouverte: 'Ouverte', en_cours: 'En cours', resolue: 'Résolue',
    essentiel: 'Essentiel', pro: 'Pro'
  };
  var lab = function (k) { return LBL[k] || k || '—'; };
  var eur = function (n) { return (Math.round((n || 0) * 10) / 10).toLocaleString('fr-FR') + ' €'; };
  var day = function (s) { if (!s) return '—'; var d = new Date(s.replace(' ', 'T') + 'Z'); return isNaN(d) ? s : d.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: '2-digit' }) + ' ' + d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }); };
  var dateOnly = function (s) { if (!s) return '—'; var d = new Date(s + 'T12:00:00Z'); return isNaN(d) ? s : d.toLocaleDateString('fr-FR'); };

  function kpi(label, value, sub) { return h('div', { class: 'kpi' }, h('b', { text: value }), h('span', { text: label }), sub ? h('small', { text: sub }) : null); }
  function group(title, kpis) { return h('section', { class: 'agrp' }, h('h2', { text: title }), h('div', { class: 'kpis2' }, kpis)); }
  function list(title, rows, empty) {
    var tot = rows.reduce(function (a, r) { return a + r.n; }, 0) || 1;
    return h('div', { class: 'acard' }, h('h3', { text: title }), rows.length ? h('ul', { class: 'blist' }, rows.map(function (r) {
      return h('li', null, h('span', { text: r.label }), h('i', null, h('u', { style: 'width:' + Math.round((r.n / tot) * 100) + '%' })), h('b', { text: r.n }));
    })) : h('p', { class: 'sub', text: empty || 'Aucune donnée pour le moment.' }));
  }
  function chart(jours) {
    var map = {}; jours.forEach(function (j) { map[j.d] = j.n; });
    var days = [], now = new Date();
    for (var i = 29; i >= 0; i--) { var d = new Date(now.getTime() - i * 864e5); days.push(d.toISOString().slice(0, 10)); }
    var max = Math.max.apply(null, days.map(function (d) { return map[d] || 0; }).concat([1]));
    var W = 600, H = 120, bw = W / 30, svgns = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(svgns, 'svg'); svg.setAttribute('viewBox', '0 0 ' + W + ' ' + (H + 18)); svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', 'Inscriptions des 30 derniers jours'); svg.setAttribute('class', 'achart');
    days.forEach(function (d, i) {
      var n = map[d] || 0, bh = Math.round((n / max) * H);
      var r = document.createElementNS(svgns, 'rect'); r.setAttribute('x', i * bw + 2); r.setAttribute('width', bw - 4); r.setAttribute('y', H - bh); r.setAttribute('height', Math.max(bh, 1)); r.setAttribute('rx', 2);
      var t = document.createElementNS(svgns, 'title'); t.textContent = d + ' : ' + n + ' inscrit(s)'; r.appendChild(t); svg.appendChild(r);
    });
    [0, 14, 29].forEach(function (i) { var t = document.createElementNS(svgns, 'text'); t.setAttribute('x', i * bw + 2); t.setAttribute('y', H + 14); t.textContent = days[i].slice(5).split('-').reverse().join('/'); svg.appendChild(t); });
    return h('div', { class: 'acard' }, h('h3', { text: 'Inscriptions des 30 derniers jours' }), svg);
  }

  /* ---------- tableau de bord ---------- */
  function dashboard(s) {
    var c = s.comptes, d = s.demandes, a = s.abonnements, p = s.plaintes, cv = s.conversion;
    var sc = {}; d.statut.forEach(function (x) { sc[x.statut] = x.n; });
    var f = {}; d.formule.forEach(function (x) { f[x.formule] = x.n; });
    var out = h('div');
    out.appendChild(group('Revenus', [kpi('Revenu mensuel récurrent (HT)', eur(a.mrr)), kpi('Revenu annuel prévu (HT)', eur(a.arr)), kpi('Panier moyen par abonné', eur(a.panier)), kpi('Taux de résiliation (30 j)', a.churn + ' %')]));
    out.appendChild(group('Inscrits', [kpi('Inscrits au total', c.total), kpi('Dernières 24 h', c.j1), kpi('7 derniers jours', c.j7), kpi('30 derniers jours', c.j30), kpi('Connectés (7 j)', c.actifs7), kpi('Session ouverte maintenant', c.connectes), kpi('Inscrits sans demande', c.sansDemande)]));
    out.appendChild(group('Demandes et sites', [kpi('Demandes au total', d.total), kpi('7 derniers jours', d.j7), kpi('30 derniers jours', d.j30), kpi('À traiter', sc.nouvelle || 0), kpi('Sites en création', sc.en_creation || 0), kpi('Aperçus envoyés', sc.apercu || 0), kpi('Sites en ligne', sc.en_ligne || 0), kpi('Abandonnées', sc.abandonnee || 0), kpi('Mails pro demandés', d.mailsDemandes)]));
    out.appendChild(group('Abonnements', [kpi('Abonnements actifs', a.actifs), kpi('Essentiel', a.parFormule.essentiel || 0), kpi('Pro', a.parFormule.pro || 0), kpi('Nouveaux (30 j)', a.nouveaux30), kpi('Récurrents (plus de 30 j)', a.recurrents), kpi('Résiliations (30 j)', a.resilies30), kpi('Résiliations au total', a.resiliesTotal), kpi('Impayés', a.impayes), kpi('Suspendus', a.suspendus), kpi('Mails pro en plus', a.mailsSup)]));
    out.appendChild(group('Plaintes', [kpi('Ouvertes', p.ouvertes), kpi('En cours', p.en_cours), kpi('Résolues', p.resolues), kpi('Au total', p.total), kpi('30 derniers jours', p.j30), kpi('Délai moyen de résolution', p.delai_h == null ? '—' : p.delai_h + ' h')]));
    out.appendChild(group('Conversion', [kpi('Inscrit → demande', cv.inscritDemande + ' %'), kpi('Demande → abonnement', cv.demandeAbonne + ' %'), kpi('Demandes Essentiel', f.essentiel || 0), kpi('Demandes Pro', f.pro || 0), kpi('Réservations de démo (24 h)', s.divers.reservationsDemo)]));
    var g = h('div', { class: 'agrid' });
    g.appendChild(chart(c.jours));
    g.appendChild(list('Demandes par activité', d.activite.map(function (x) { return { label: x.activite || '—', n: x.n }; })));
    g.appendChild(list('Demandes par ville', d.ville.map(function (x) { return { label: x.ville, n: x.n }; })));
    g.appendChild(list('Provenance des demandes', d.sources.map(function (x) { return { label: x.s, n: x.n }; })));
    g.appendChild(list('Motifs de résiliation', a.motifs.map(function (x) { return { label: x.motif, n: x.n }; }), 'Aucune résiliation.'));
    g.appendChild(list('Activité des 30 derniers jours', s.divers.evenements30.map(function (x) { return { label: x.type.replace(/_/g, ' '), n: x.n }; })));
    out.appendChild(g);
    return out;
  }

  /* ---------- clients ---------- */
  var view = $('#adm-view'), msg = $('#adm-msg');
  function flash(t, bad) { msg.textContent = t; msg.className = 'alert ' + (bad ? 'bad' : 'ok') + ' on'; msg.setAttribute('tabindex', '-1'); setTimeout(function () { msg.className = 'alert'; }, 4500); }
  function sel(name, opts, val) { var s = h('select', { name: name }); opts.forEach(function (o) { var op = h('option', { value: o, text: lab(o) }); if (o === val) op.selected = true; s.appendChild(op); }); return s; }

  function clients(q) {
    view.textContent = '';
    var box = h('input', { type: 'search', placeholder: 'Rechercher un nom ou un e-mail', value: q || '', 'aria-label': 'Rechercher un client' });
    var body = h('div');
    function load() {
      api('/api/admin/comptes?q=' + encodeURIComponent(box.value)).then(function (r) {
        body.textContent = '';
        if (!r.j.ok) { body.appendChild(h('p', { text: 'Erreur de chargement.' })); return; }
        if (!r.j.comptes.length) { body.appendChild(h('p', { class: 'sub', text: 'Aucun client.' })); return; }
        var t = h('table', { class: 'atab' }, h('thead', null, h('tr', null, ['Client', 'Inscrit le', 'Dernière connexion', 'Site', 'Abonnement', 'Plaintes', ''].map(function (x) { return h('th', { text: x }); }))));
        var tb = h('tbody');
        r.j.comptes.forEach(function (c) {
          tb.appendChild(h('tr', null,
            h('td', null, h('b', { text: c.nom }), h('br'), h('small', { text: c.email })),
            h('td', { text: day(c.created_at) }), h('td', { text: day(c.derniere_connexion) }),
            h('td', { text: c.demandes ? lab(c.statut_site) : 'Pas de demande' }),
            h('td', { text: c.formule ? lab(c.formule) + ' · ' + lab(c.abo) : '—' }),
            h('td', { text: c.plaintes_ouvertes ? String(c.plaintes_ouvertes) : '—' }),
            h('td', { class: 'acts' }, h('button', { type: 'button', class: 'btn ghost sm', text: 'Ouvrir', onclick: function () { detail(c.id); } }), h('button', { type: 'button', class: 'btn sm', text: 'Voir en tant que', onclick: function () { impersonate(c.id); } }))));
        });
        t.appendChild(tb); body.appendChild(h('div', { class: 'scroll' }, t));
      });
    }
    var tm; box.addEventListener('input', function () { clearTimeout(tm); tm = setTimeout(load, 250); });
    view.appendChild(h('div', { class: 'acard' }, h('h2', { text: 'Clients' }), h('div', { class: 'afind' }, box), body));
    load();
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
      view.textContent = '';
      view.appendChild(h('p', null, h('button', { type: 'button', class: 'btn ghost sm', text: '← Tous les clients', onclick: function () { clients(); } })));
      view.appendChild(h('div', { class: 'acard' }, h('h2', { text: c.nom }), h('p', { class: 'sub', text: c.email + ' · inscrit le ' + day(c.created_at) + ' · dernière connexion : ' + day(c.derniere_connexion) }),
        h('button', { type: 'button', class: 'btn', text: 'Se connecter en tant que ce client', onclick: function () { impersonate(c.id); } })));
      // demandes
      var dc = h('div', { class: 'acard' }, h('h3', { text: 'Demandes de site (' + r.j.demandes.length + ')' }));
      if (!r.j.demandes.length) dc.appendChild(h('p', { class: 'sub', text: 'Aucune demande.' }));
      r.j.demandes.forEach(function (d) {
        var s = sel('statut', ['nouvelle', 'en_creation', 'apercu', 'en_ligne', 'abandonnee'], d.statut);
        s.addEventListener('change', function () { api('/api/admin/demande', 'POST', { id: d.id, statut: s.value }).then(function (x) { flash(x.j.ok ? 'Statut du site mis à jour.' : 'Échec de la mise à jour.', !x.j.ok); }); });
        dc.appendChild(h('div', { class: 'arow' }, h('div', null, h('b', { text: d.commerce + ' · ' + d.ref }), h('br'), h('small', { text: [lab(d.formule), d.activite, d.ville, d.domaine && ('domaine : ' + d.domaine), d.mails ? d.mails + ' mail(s) pro' : '', d.tel, day(d.created_at)].filter(Boolean).join(' · ') }), d.message ? h('p', { class: 'sub', text: d.message }) : null), s));
      });
      view.appendChild(dc);
      // abonnement
      var fo = sel('formule', ['essentiel', 'pro'], ab ? ab.formule : 'essentiel'), st = sel('statut', ['actif', 'impaye', 'suspendu', 'resilie'], ab ? ab.statut : 'actif');
      var ml = h('input', { type: 'number', name: 'mails_sup', min: '0', max: '50', value: ab ? ab.mails_sup : 0 }), mo = h('input', { type: 'text', name: 'motif', maxlength: '200', placeholder: 'Motif de résiliation (facultatif)', value: ab ? ab.motif || '' : '' });
      var sv = h('button', { type: 'button', class: 'btn', text: ab ? 'Enregistrer l’abonnement' : 'Créer l’abonnement', onclick: function () {
        api('/api/admin/abonnement', 'POST', { compte_id: c.id, formule: fo.value, statut: st.value, mails_sup: ml.value, motif: mo.value }).then(function (x) { flash(x.j.ok ? 'Abonnement enregistré.' : 'Échec de l’enregistrement.', !x.j.ok); if (x.j.ok) detail(c.id); });
      } });
      view.appendChild(h('div', { class: 'acard' }, h('h3', { text: 'Abonnement' }), ab ? h('p', { class: 'sub', text: 'Début : ' + dateOnly(ab.debut) + (ab.fin ? ' · fin : ' + dateOnly(ab.fin) : '') }) : h('p', { class: 'sub', text: 'Aucun abonnement. Créez-le quand le client a accepté et payé.' }),
        h('div', { class: 'aform' }, h('label', null, 'Formule', fo), h('label', null, 'Statut', st), h('label', null, 'Mails pro en plus', ml), h('label', { class: 'wide' }, 'Motif', mo)), sv));
      // plaintes
      var pc = h('div', { class: 'acard' }, h('h3', { text: 'Plaintes (' + r.j.plaintes.length + ')' }));
      r.j.plaintes.forEach(function (p) {
        var s = sel('statut', ['ouverte', 'en_cours', 'resolue'], p.statut);
        s.addEventListener('change', function () { api('/api/admin/plainte-statut', 'POST', { id: p.id, statut: s.value }).then(function (x) { flash(x.j.ok ? 'Plainte mise à jour.' : 'Échec.', !x.j.ok); }); });
        pc.appendChild(h('div', { class: 'arow' }, h('div', null, h('b', { text: p.sujet }), h('br'), h('small', { text: day(p.created_at) + (p.resolved_at ? ' · résolue le ' + day(p.resolved_at) : '') }), p.message ? h('p', { class: 'sub', text: p.message }) : null), s));
      });
      var sj = h('input', { type: 'text', maxlength: '120', placeholder: 'Sujet de la plainte' }), ms = h('textarea', { rows: '2', maxlength: '1500', placeholder: 'Détails (facultatif)' });
      pc.appendChild(h('div', { class: 'aform' }, h('label', { class: 'wide' }, 'Nouvelle plainte', sj), h('label', { class: 'wide' }, 'Détails', ms)));
      pc.appendChild(h('button', { type: 'button', class: 'btn ghost', text: 'Ajouter la plainte', onclick: function () { if (!sj.value.trim()) { flash('Indiquez un sujet.', true); return; } api('/api/admin/plainte', 'POST', { compte_id: c.id, sujet: sj.value, message: ms.value }).then(function (x) { flash(x.j.ok ? 'Plainte ajoutée.' : 'Échec.', !x.j.ok); if (x.j.ok) detail(c.id); }); } }));
      view.appendChild(pc);
      // journal
      var jc = h('div', { class: 'acard' }, h('h3', { text: 'Journal (30 derniers événements)' }));
      if (!r.j.journal.length) jc.appendChild(h('p', { class: 'sub', text: 'Rien pour le moment.' }));
      else jc.appendChild(h('ul', { class: 'jlist' }, r.j.journal.map(function (j) { return h('li', null, h('time', { text: day(j.created_at) }), h('b', { text: j.type.replace(/_/g, ' ') }), h('span', { text: j.detail || '' }), j.admin_id ? h('em', { text: 'par admin' }) : null); })));
      view.appendChild(jc);
    });
  }

  /* ---------- mot de passe ---------- */
  function motDePasse() {
    view.textContent = '';
    var a = h('input', { type: 'password', autocomplete: 'current-password' }), n = h('input', { type: 'password', autocomplete: 'new-password', minlength: '8' }), n2 = h('input', { type: 'password', autocomplete: 'new-password', minlength: '8' });
    view.appendChild(h('div', { class: 'acard' }, h('h2', { text: 'Changer mon mot de passe' }),
      h('div', { class: 'aform' }, h('label', { class: 'wide' }, 'Mot de passe actuel', a), h('label', { class: 'wide' }, 'Nouveau mot de passe (8 caractères minimum)', n), h('label', { class: 'wide' }, 'Confirmez le nouveau mot de passe', n2)),
      h('button', { type: 'button', class: 'btn', text: 'Changer le mot de passe', onclick: function () {
        if (n.value.length < 8) { flash('Le nouveau mot de passe doit contenir au moins 8 caractères.', true); return; }
        if (n.value !== n2.value) { flash('Les deux mots de passe ne sont pas identiques.', true); return; }
        api('/api/mot-de-passe', 'POST', { actuel: a.value, nouveau: n.value }).then(function (r) {
          if (r.j.ok) { flash('Mot de passe changé. Les autres appareils sont déconnectés.'); a.value = n.value = n2.value = ''; }
          else flash(r.s === 401 ? 'Le mot de passe actuel est incorrect.' : 'Impossible de changer le mot de passe.', true);
        });
      } })));
  }

  /* ---------- navigation ---------- */
  var tabs = { stats: $('#t-stats'), clients: $('#t-clients'), mdp: $('#t-mdp') };
  function active(k) { Object.keys(tabs).forEach(function (x) { tabs[x].setAttribute('aria-pressed', x === k ? 'true' : 'false'); }); }
  function showStats() {
    active('stats'); view.textContent = ''; view.appendChild(h('p', { class: 'sub', text: 'Chargement…' }));
    api('/api/admin/stats').then(function (r) { view.textContent = ''; if (r.j.ok) view.appendChild(dashboard(r.j)); else view.appendChild(h('p', { text: 'Impossible de charger les statistiques.' })); });
  }
  tabs.stats.addEventListener('click', showStats);
  tabs.clients.addEventListener('click', function () { active('clients'); clients(); });
  tabs.mdp.addEventListener('click', function () { active('mdp'); motDePasse(); });
  $('#adm-out').addEventListener('click', function () { api('/api/deconnexion', 'POST').then(function () { location.href = '/connexion'; }); });
  $('#adm-refresh').addEventListener('click', function () { showStats(); });

  api('/api/moi').then(function (r) {
    var gate = $('#adm-gate'), app = $('#adm-app');
    if (r.s === 401) { gate.textContent = ''; gate.appendChild(h('p', null, 'Connectez-vous avec votre compte administrateur. ', h('a', { href: '/connexion', text: 'Se connecter' }))); return; }
    if (!r.j.admin) { gate.textContent = 'Accès réservé à l’administrateur.'; return; }
    gate.hidden = true; app.hidden = false; showStats();
  }).catch(function () { $('#adm-gate').textContent = 'Connexion impossible pour le moment.'; });
})();
