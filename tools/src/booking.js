/* Démo de réservation : même règles que le Worker (worker/worker.js). */
(function () {
  'use strict';
  var f = document.getElementById('resa');
  if (!f) return;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  var SERV = { 'coupe-femme': ['Coupe femme', 2], 'coupe-homme': ['Coupe homme', 1], 'couleur': ['Couleur', 3], 'brushing': ['Brushing', 1] };
  var UNITS = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30'];
  var JOURS = ['dim', 'lun', 'mar', 'mer', 'jeu', 'ven', 'sam'];
  var MOIS = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.'];
  var JOURS_L = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];

  var st = { date: '', heure: '', taken: [], mine: null };
  var daysEl = $('#r-days'), slotsEl = $('#r-slots'), help = $('#r-slot-help'), sum = $('#r-sum'), bad = $('#r-bad'), send = $('#r-send');

  function add(m, i) { return heureAdd(m, i * 30); }
  function heureAdd(h, min) { var p = h.split(':'), t = (+p[0]) * 60 + (+p[1]) + min; return ('0' + Math.floor(t / 60)).slice(-2) + ':' + ('0' + (t % 60)).slice(-2); }
  function parisToday() {
    try { return new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Paris' }).format(new Date()); } catch (_) { return new Date().toISOString().slice(0, 10); }
  }
  function addDays(iso, n) { var d = new Date(iso + 'T12:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); }
  function dow(iso) { return new Date(iso + 'T12:00:00Z').getUTCDay(); }
  function label(iso) { var d = new Date(iso + 'T12:00:00Z'); return JOURS_L[d.getUTCDay()] + ' ' + d.getUTCDate() + ' ' + MOIS[d.getUTCMonth()]; }
  function svc() { return ($('input[name=svc]:checked', f) || {}).value || 'coupe-femme'; }

  /* ---- jours : 14 prochains jours ouverts (mardi au samedi), à partir de demain ---- */
  var t0 = parisToday(), list = [];
  for (var i = 1; list.length < 14 && i < 40; i++) { var d = addDays(t0, i), w = dow(d); if (w >= 2 && w <= 6) list.push(d); }
  list.forEach(function (iso) {
    var b = document.createElement('button'), dd = new Date(iso + 'T12:00:00Z');
    b.type = 'button'; b.setAttribute('aria-pressed', 'false'); b.dataset.d = iso;
    b.innerHTML = JOURS[dd.getUTCDay()] + '<small>' + dd.getUTCDate() + ' ' + MOIS[dd.getUTCMonth()] + '</small>';
    b.setAttribute('aria-label', label(iso));
    b.addEventListener('click', function () { pickDay(iso); });
    daysEl.appendChild(b);
  });

  function summary() {
    if (st.date && st.heure) sum.textContent = SERV[svc()][0] + ', ' + label(st.date) + ' à ' + st.heure.replace(':', ' h ').replace(' h 00', ' h') + '.';
    else sum.textContent = '';
  }

  function renderSlots() {
    slotsEl.innerHTML = '';
    if (!st.date) return;
    var n = SERV[svc()][1];
    var free = 0;
    UNITS.forEach(function (h) {
      var ok = true;
      for (var k = 0; k < n; k++) { var u = add(h, k); if (UNITS.indexOf(u) < 0 || st.taken.indexOf(u) >= 0) { ok = false; break; } }
      var b = document.createElement('button');
      b.type = 'button'; b.textContent = h.replace(':', ' h ').replace(' h 00', ' h'); b.disabled = !ok; b.dataset.h = h;
      b.setAttribute('aria-pressed', st.heure === h ? 'true' : 'false');
      if (!ok) b.setAttribute('aria-label', h + ', indisponible');
      if (ok) free++;
      b.addEventListener('click', function () { st.heure = h; renderSlots(); summary(); });
      slotsEl.appendChild(b);
    });
    help.textContent = free ? 'Créneaux de ' + label(st.date) + ' (les barrés sont pris ou trop courts pour cette prestation).' : 'Plus de créneau ce jour-là pour cette prestation. Essayez un autre jour.';
  }

  function loadTaken() {
    help.textContent = 'Chargement des créneaux…';
    return fetch('/api/creneaux?date=' + encodeURIComponent(st.date))
      .then(function (r) { return r.json().catch(function () { return {}; }); })
      .then(function (j) { st.taken = (j && j.taken) || []; if (st.heure && st.taken.indexOf(st.heure) >= 0) st.heure = ''; renderSlots(); summary(); })
      .catch(function () { st.taken = []; renderSlots(); help.textContent = 'Les créneaux n’ont pas pu être vérifiés : réessayez dans un instant.'; });
  }

  function pickDay(iso) {
    st.date = iso; st.heure = '';
    $$('button', daysEl).forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.d === iso ? 'true' : 'false'); });
    loadTaken();
  }
  $$('input[name=svc]', f).forEach(function (r) { r.addEventListener('change', function () { st.heure = ''; renderSlots(); summary(); }); });

  function err(id, m) { var e = $('#' + id); if (e) e.textContent = m || ''; }
  function showBad(m) { bad.querySelector('span').textContent = m; bad.classList.add('on'); bad.focus(); }

  f.addEventListener('submit', function (e) {
    e.preventDefault(); bad.classList.remove('on'); err('r-nom-e'); err('r-tel-e');
    var nom = f.elements.nom.value.trim(), tel = f.elements.tel.value.trim();
    if (!st.date) { showBad('Choisissez un jour.'); return; }
    if (!st.heure) { showBad('Choisissez un créneau.'); return; }
    if (nom.length < 2) { err('r-nom-e', 'Indiquez un prénom (2 lettres au moins).'); f.elements.nom.focus(); return; }
    if (tel && !/^[0-9+().\s-]{8,20}$/.test(tel)) { err('r-tel-e', 'Numéro invalide.'); f.elements.tel.focus(); return; }
    send.disabled = true; send.classList.add('busy');
    var sk = svc();
    fetch('/api/reservation', { method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ date: st.date, heure: st.heure, service: sk, nom: nom, tel: tel, site_web_url: f.elements.site_web_url.value }) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { s: r.status, j: j }; }); })
      .then(function (r) {
        send.disabled = false; send.classList.remove('busy');
        if (r.s === 200 && r.j.ok) {
          st.mine = { date: st.date, heure: st.heure, service: SERV[sk][0], nom: nom };
          $('#r-ref').textContent = r.j.ref;
          $('#r-done-p').textContent = SERV[sk][0] + ', ' + label(st.date) + ' à ' + st.heure.replace(':', ' h ') + ', au nom de ' + nom + '.';
          f.hidden = true; $('#r-done').classList.add('on'); $('#r-done').setAttribute('tabindex', '-1'); $('#r-done').focus();
          renderAgenda();
        } else if (r.s === 409) {
          showBad('Ce créneau vient d’être pris par quelqu’un d’autre. Choisissez-en un autre.'); st.heure = ''; loadTaken();
        } else if (r.s === 429) {
          showBad('Trop de réservations de test depuis votre connexion. Patientez une heure.');
        } else if (r.s === 422) {
          showBad((r.j && r.j.error) || 'Certaines informations ne sont pas valides.');
        } else {
          showBad('La réservation n’a pas pu être enregistrée (erreur ' + r.s + '). Réessayez.');
        }
      })
      .catch(function () { send.disabled = false; send.classList.remove('busy'); showBad('Connexion impossible pour le moment. Réessayez.'); });
  });

  $('#r-again').addEventListener('click', function () {
    $('#r-done').classList.remove('on'); f.hidden = false; st.heure = ''; loadTaken(); f.scrollIntoView({ block: 'start' });
  });

  /* ---- onglets + agenda d'exemple ---- */
  var tc = $('#t-client'), ta = $('#t-agenda'), pc = $('#p-client'), pa = $('#p-agenda');
  function tab(a) {
    tc.setAttribute('aria-selected', a ? 'false' : 'true'); ta.setAttribute('aria-selected', a ? 'true' : 'false');
    tc.tabIndex = a ? -1 : 0; ta.tabIndex = a ? 0 : -1; pc.hidden = a; pa.hidden = !a;
    if (a) renderAgenda();
  }
  tc.addEventListener('click', function () { tab(false); }); ta.addEventListener('click', function () { tab(true); });
  $('#r-see').addEventListener('click', function () { tab(true); ta.focus(); });
  [tc, ta].forEach(function (b) { b.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { var a = b === tc; tab(a); (a ? ta : tc).focus(); } }); });

  function renderAgenda() {
    var ul = $('#ag-list'), day = st.mine ? st.mine.date : list[0];
    var rows = [['09:30', 'Julie', 'Brushing'], ['11:00', 'Karim', 'Coupe homme'], ['14:30', 'Nadia', 'Couleur'], ['16:00', 'Paul', 'Coupe homme']]
      .filter(function (r) { return !st.mine || r[0] !== st.mine.heure; })
      .map(function (r) { return { h: r[0], t: r[1] + ' · ' + r[2], cls: 'fake' }; });
    if (st.mine) rows.push({ h: st.mine.heure, t: st.mine.nom + ' · ' + st.mine.service + ' (votre réservation de test)', cls: 'mine' });
    rows.sort(function (a, b) { return a.h < b.h ? -1 : 1; });
    ul.innerHTML = '<li style="grid-template-columns:minmax(0,1fr);background:none;border:0;padding:0 2px"><b style="font-family:var(--body);font-weight:700;color:var(--ink)">' + label(day) + '</b></li>';
    rows.forEach(function (r) { var li = document.createElement('li'); li.className = r.cls; li.innerHTML = '<b></b><span></span>'; li.firstChild.textContent = r.h; li.lastChild.textContent = r.t; ul.appendChild(li); });
  }
  renderAgenda();
  if (list.length) pickDay(list[0]);
})();
