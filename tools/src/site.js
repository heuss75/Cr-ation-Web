(function () {
  'use strict';
  var D = document, W = window;
  var SITE = W.SITE || {};
  function $(s, r) { return (r || D).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || D).querySelectorAll(s)); }
  function ls(k, v) {
    try {
      if (v === undefined) return localStorage.getItem(k);
      if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v);
    } catch (e) { return null; }
  }
  var reduce = W.matchMedia && W.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function norm(s) { return String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }

  /* ---------- 20. petit message de confirmation (toast) ---------- */
  var toastT;
  function toast(msg) {
    var t = $('#toast'); if (!t) return;
    t.textContent = msg; t.classList.add('on');
    clearTimeout(toastT); toastT = setTimeout(function () { t.classList.remove('on'); }, 2200);
  }

  /* ---------- 1. mode sombre ---------- */
  function setTheme(t, save) {
    D.documentElement.setAttribute('data-theme', t);
    var m = $('meta[name=theme-color]'); if (m) m.content = t === 'dark' ? '#0E0F10' : '#F5F6F6';
    if (save) ls('sv_theme', t);
    var b = $('#theme');
    if (b) {
      b.setAttribute('aria-pressed', t === 'dark' ? 'true' : 'false');
      b.setAttribute('aria-label', t === 'dark' ? 'Passer en mode clair' : 'Passer en mode sombre');
    }
  }
  var themeBtn = $('#theme');
  setTheme(D.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light', false);
  if (themeBtn) themeBtn.addEventListener('click', function () {
    setTheme(D.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark', true);
  });
  if (W.matchMedia) {
    var mq = W.matchMedia('(prefers-color-scheme: dark)');
    var onMq = function (e) { if (!ls('sv_theme')) setTheme(e.matches ? 'dark' : 'light', false); };
    if (mq.addEventListener) mq.addEventListener('change', onMq);
  }

  /* ---------- 5. menu mobile ---------- */
  var burger = $('#burger'), menu = $('#menu');
  function setMenu(open) {
    if (!burger || !menu) return;
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    menu.classList.toggle('open', open);
    if (open) menu.removeAttribute('inert'); else menu.setAttribute('inert', '');
    D.body.classList.toggle('lock', open);
    var u = burger.querySelector('use'); if (u) u.setAttribute('href', open ? '#i-x' : '#i-menu');
  }
  if (burger && menu) {
    setMenu(false);
    burger.addEventListener('click', function () { setMenu(burger.getAttribute('aria-expanded') !== 'true'); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    W.addEventListener('resize', function () { if (W.innerWidth >= 1040) setMenu(false); });
  }

  /* ---------- 8. barre de progression, 4. retour en haut, en-tête ---------- */
  var prog = $('#prog i'), topBtn = $('#top'), ticking = false;
  function onScroll() {
    var h = D.documentElement, max = h.scrollHeight - h.clientHeight, y = W.scrollY || h.scrollTop;
    var p = max > 0 ? Math.min(1, y / max) : 0;
    if (prog) prog.style.transform = 'scaleX(' + p + ')';
    if (topBtn) topBtn.classList.toggle('on', y > 600);
    D.body.classList.toggle('scrolled', y > 8);
    ticking = false;
  }
  W.addEventListener('scroll', function () { if (!ticking) { ticking = true; W.requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (topBtn) topBtn.addEventListener('click', function () { W.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  /* ---------- 6 et 7. apparition au défilement ---------- */
  if (!reduce && 'IntersectionObserver' in W) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    $$('main .sec > *, main .doc > *, main .cmp > *, main .tline li, .cta-band').forEach(function (el, i) {
      if (el.getBoundingClientRect().top < W.innerHeight * 0.9) return;
      el.classList.add('rv'); io.observe(el);
    });
  }

  /* ---------- 20. contact flottant ---------- */
  var fab = $('#fab'), fpanel = $('#fpanel');
  function setFab(open) {
    if (!fab || !fpanel) return;
    fab.setAttribute('aria-expanded', open ? 'true' : 'false');
    fpanel.hidden = !open;
  }
  if (fab && fpanel) {
    fab.addEventListener('click', function (e) { e.stopPropagation(); setFab(fpanel.hidden); });
    D.addEventListener('click', function (e) { if (!fpanel.hidden && !e.target.closest('.fab-wrap')) setFab(false); });
  }

  /* ---------- 9. boutons copier ---------- */
  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).catch(function () { return legacyCopy(text); });
    }
    return legacyCopy(text);
  }
  function legacyCopy(text) {
    return new Promise(function (res) {
      var ta = D.createElement('textarea'); ta.value = text; ta.setAttribute('readonly', '');
      ta.style.cssText = 'position:fixed;opacity:0;top:0;left:0'; D.body.appendChild(ta); ta.select();
      try { D.execCommand('copy'); } catch (e) { }
      D.body.removeChild(ta); res();
    });
  }
  function absUrl(v) {
    if (!v || v === 'page') return location.origin + location.pathname;
    if (v.charAt(0) === '#') return location.origin + location.pathname + v;
    if (v.charAt(0) === '/') return location.origin + v;
    return v;
  }
  D.addEventListener('click', function (e) {
    var b = e.target.closest('[data-copy],[data-copy-url]'); if (!b) return;
    var text = b.hasAttribute('data-copy') ? b.getAttribute('data-copy') : absUrl(b.getAttribute('data-copy-url'));
    copyText(text).then(function () {
      toast(b.hasAttribute('data-copy-url') ? 'Lien copié' : 'Copié');
      var l = b.querySelector('.lbl');
      if (l) { var o = l.textContent; l.textContent = 'Copié'; setTimeout(function () { l.textContent = o; }, 1600); }
    });
  });
  $$('.prose h2[id],.prose h3[id]').forEach(function (h) {
    var a = D.createElement('button'); a.type = 'button'; a.className = 'anchor'; a.textContent = '#';
    a.setAttribute('data-copy-url', '#' + h.id); a.setAttribute('aria-label', 'Copier le lien vers cette section');
    h.appendChild(a);
  });

  /* ---------- 10. version imprimable ---------- */
  D.addEventListener('click', function (e) {
    if (e.target.closest('[data-print]')) { e.preventDefault(); W.print(); }
  });

  /* ---------- 2. bandeau cookies et 14. suivi UTM ---------- */
  var CK = 'sv_consent', UK = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  function getConsent() {
    try {
      var c = JSON.parse(ls(CK) || 'null');
      if (c && Date.now() - c.t > 396 * 864e5) return null; /* on redemande au bout de 13 mois */
      return c;
    } catch (e) { return null; }
  }
  function captureUtm() {
    var p = new URLSearchParams(location.search), o = {}, any = false;
    UK.forEach(function (k) { var v = p.get(k); if (v) { o[k] = v.slice(0, 100); any = true; } });
    if (!any) return;
    var ref = ''; try { ref = D.referrer ? new URL(D.referrer).hostname : ''; } catch (e) { }
    o.ref = ref; o.landing = location.pathname; o.ts = Date.now();
    var old = null; try { old = JSON.parse(ls('sv_utm') || 'null'); } catch (e) { }
    if (!old || Date.now() - old.ts > 30 * 864e5) ls('sv_utm', JSON.stringify(o));
  }
  W.svUtm = function () {
    var c = getConsent(); if (!c || !c.utm) return null;
    try { return JSON.parse(ls('sv_utm') || 'null'); } catch (e) { return null; }
  };
  function applyConsent() {
    var c = getConsent();
    if (c && c.utm) captureUtm(); else ls('sv_utm', null);
  }
  var cookie = $('#cookie');
  function showCookie(custom) {
    if (!cookie) return;
    var c = getConsent();
    $('#ck-utm').checked = !!(c && c.utm);
    $('#ck-opts').hidden = !custom;
    cookie.hidden = false; D.body.classList.add('ck-open');
    if (custom) $('#ck-utm').focus();
  }
  function saveConsent(utm) {
    ls(CK, JSON.stringify({ v: 1, utm: !!utm, t: Date.now() }));
    cookie.hidden = true; D.body.classList.remove('ck-open');
    applyConsent();
    toast(utm ? 'Préférences enregistrées' : 'Cookies optionnels refusés');
  }
  if (cookie) {
    $('#ck-no').addEventListener('click', function () { saveConsent(false); });
    $('#ck-yes').addEventListener('click', function () { saveConsent(true); });
    $('#ck-cfg').addEventListener('click', function () {
      var o = $('#ck-opts');
      if (o.hidden) { o.hidden = false; $('#ck-save').hidden = false; } else { o.hidden = true; $('#ck-save').hidden = true; }
    });
    $('#ck-save').addEventListener('click', function () { saveConsent($('#ck-utm').checked); });
    D.addEventListener('click', function (e) {
      if (e.target.closest('[data-cookies]')) { e.preventDefault(); showCookie(true); $('#ck-save').hidden = false; }
    });
    if (!getConsent()) setTimeout(function () { showCookie(false); $('#ck-save').hidden = true; }, 600); else applyConsent();
  }

  /* ---------- 3. recherche sur le site ---------- */
  var sdlg = $('#search'), sin = $('#sq'), sres = $('#sres'), idx = null, idxP = null, active = -1, lastRes = [];
  function loadIdx() {
    if (idxP) return idxP;
    idxP = fetch('/assets/search-index.json?v=' + (SITE.v || '')).then(function (r) { return r.json(); }).then(function (j) {
      idx = j.map(function (e) { e._t = norm(e.t); e._x = norm(e.x); e._p = norm(e.p || ''); return e; }); return idx;
    }).catch(function () { idxP = null; idx = []; return idx; });
    return idxP;
  }
  function hl(text, terms) {
    var out = esc(text), n = norm(text);
    // surbrillance simple, sans accent
    var ranges = [];
    terms.forEach(function (t) { var i = n.indexOf(t); if (i > -1) ranges.push([i, i + t.length]); });
    if (!ranges.length) return out;
    ranges.sort(function (a, b) { return a[0] - b[0]; });
    var res = '', pos = 0;
    ranges.forEach(function (r) { if (r[0] < pos) return; res += esc(text.slice(pos, r[0])) + '<mark>' + esc(text.slice(r[0], r[1])) + '</mark>'; pos = r[1]; });
    return res + esc(text.slice(pos));
  }
  function doSearch(q) {
    var terms = norm(q).split(/\s+/).filter(Boolean), res = [];
    if (!terms.length) return { terms: terms, res: [] };
    idx.forEach(function (e) {
      var s = 0;
      for (var i = 0; i < terms.length; i++) {
        var t = terms[i], sc = 0, it = e._t.indexOf(t);
        if (it > -1) sc += it === 0 ? 7 : 5;
        if (e._x.indexOf(t) > -1) sc += 2;
        if (e._p.indexOf(t) > -1) sc += 1;
        if (!sc) { s = 0; break; }
        s += sc;
      }
      if (s) res.push([s, e]);
    });
    res.sort(function (a, b) { return b[0] - a[0]; });
    return { terms: terms, res: res.slice(0, 8).map(function (r) { return r[1]; }) };
  }
  function suggestions() {
    return '<p class="sempty">Essayez : </p><div class="sugg">' +
      ['prix', 'modification', 'nom de domaine', 'résilier', 'délai', 'mail pro', 'cookies'].map(function (s) {
        return '<button type="button" class="chip" data-q="' + esc(s) + '">' + esc(s) + '</button>';
      }).join('') + '</div>';
  }
  function renderRes(q) {
    if (!q.trim()) { sres.innerHTML = suggestions(); lastRes = []; active = -1; return; }
    if (!idx) { sres.innerHTML = '<div class="skel"></div><div class="skel"></div><div class="skel"></div>'; return; }
    var r = doSearch(q); lastRes = r.res; active = r.res.length ? 0 : -1;
    if (!r.res.length) { sres.innerHTML = '<p class="sempty">Aucun résultat pour « ' + esc(q) + ' ». Essayez un autre mot, ou <a href="/faq">parcourez la FAQ</a>.</p>'; return; }
    sres.innerHTML = r.res.map(function (e, i) {
      return '<a href="' + esc(e.u) + '" role="option" aria-selected="' + (i === 0 ? 'true' : 'false') + '"><span class="pg">' + esc(e.p) + '</span><b>' + hl(e.t, r.terms) + '</b><small>' + hl(e.x.slice(0, 150) + (e.x.length > 150 ? '…' : ''), r.terms) + '</small></a>';
    }).join('');
  }
  function setActive(n) {
    var items = $$('#sres a'); if (!items.length) return;
    active = (n + items.length) % items.length;
    items.forEach(function (a, i) { a.setAttribute('aria-selected', i === active ? 'true' : 'false'); });
    items[active].scrollIntoView({ block: 'nearest' });
  }
  function openSearch() {
    if (!sdlg) return;
    setMenu(false);
    if (sdlg.showModal) { if (!sdlg.open) sdlg.showModal(); } else sdlg.setAttribute('open', '');
    sin.value = ''; renderRes(''); sin.focus();
    loadIdx().then(function () { if (sin.value) renderRes(sin.value); });
  }
  if (sdlg) {
    $$('[data-search]').forEach(function (b) { b.addEventListener('click', openSearch); });
    sin.addEventListener('input', function () { renderRes(sin.value); });
    sin.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); setActive(active + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(active - 1); }
      else if (e.key === 'Escape') { e.preventDefault(); sdlg.close(); }
      else if (e.key === 'Enter') { var a = $$('#sres a')[active]; if (a) { e.preventDefault(); a.click(); } }
    });
    sres.addEventListener('click', function (e) {
      var c = e.target.closest('[data-q]');
      if (c) { sin.value = c.getAttribute('data-q'); renderRes(sin.value); sin.focus(); return; }
      var a = e.target.closest('a'); if (a) { sdlg.close(); }
    });
    sdlg.addEventListener('click', function (e) { if (e.target === sdlg) sdlg.close(); });
    D.addEventListener('keydown', function (e) {
      var tag = (e.target.tagName || '').toLowerCase();
      var typing = tag === 'input' || tag === 'textarea' || tag === 'select' || e.target.isContentEditable;
      if ((e.key === '/' && !typing) || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k')) { e.preventDefault(); openSearch(); }
      if (e.key === 'Escape') { setMenu(false); setFab(false); }
    });
  }

  /* ---------- 19. FAQ dépliable avec filtre ---------- */
  var ql = $('#qlist');
  if (ql) {
    var qs = $$('details.q', ql), cat = 'all', qin = $('#qfilter'), qempty = $('#qempty'), qcount = $('#qcount'), tog = $('#qtoggle');
    var applyF = function () {
      var t = norm(qin.value).split(/\s+/).filter(Boolean), n = 0;
      qs.forEach(function (d) {
        var txt = norm(d.textContent), ok = (cat === 'all' || d.getAttribute('data-cat') === cat) && t.every(function (w) { return txt.indexOf(w) > -1; });
        d.hidden = !ok; if (ok) n++;
      });
      qempty.classList.toggle('on', n === 0);
      qcount.textContent = n + ' question' + (n > 1 ? 's' : '');
    };
    qin.addEventListener('input', applyF);
    $$('.cats [data-cat]').forEach(function (c) {
      c.addEventListener('click', function () {
        cat = c.getAttribute('data-cat');
        $$('.cats [data-cat]').forEach(function (o) { o.setAttribute('aria-pressed', o === c ? 'true' : 'false'); });
        applyF();
      });
    });
    var allOpen = false;
    tog.addEventListener('click', function () {
      allOpen = !allOpen; qs.forEach(function (d) { if (!d.hidden) d.open = allOpen; });
      tog.querySelector('.lbl').textContent = allOpen ? 'Tout replier' : 'Tout déplier';
    });
    var openHash = function () {
      var id = location.hash.slice(1); if (!id) return;
      var d = D.getElementById(id);
      if (d && d.tagName === 'DETAILS') { d.hidden = false; d.open = true; setTimeout(function () { d.scrollIntoView({ block: 'start' }); }, 50); }
    };
    W.addEventListener('hashchange', openHash); openHash(); applyF();
    qs.forEach(function (d) {
      var s = d.querySelector('summary'); var b = D.createElement('button');
      b.type = 'button'; b.className = 'anchor'; b.textContent = '#'; b.setAttribute('data-copy-url', '#' + d.id);
      b.setAttribute('aria-label', 'Copier le lien vers cette question');
      d.querySelector('.a').appendChild(b); b.style.opacity = '.6'; b.style.marginLeft = '-6px';
    });
  }

  /* ---------- offre : calculateur ---------- */
  var rg = $('#mails');
  if (rg) {
    var upd = function () {
      var pro = ($('input[name=fm]:checked') || {}).value === 'pro';
      var n = +rg.value, tot = pro ? Math.max(n, 1) : n, extra = pro ? tot - 1 : tot;
      var base = pro ? 100 : 60, mc = 4 * extra, m = base + mc;
      $('#c-n').textContent = tot;
      $('#c-n2').textContent = tot > 1 ? 'adresses mail pro' : 'adresse mail pro';
      $('#c-m').textContent = m.toLocaleString('fr-FR');
      $('#c-basel').textContent = pro ? 'Formule Pro (1 mail et réservation inclus)' : 'Formule Essentiel';
      $('#c-base').textContent = base + ' €';
      $('#c-maill').textContent = pro ? 'Mails en plus de la 1re' : 'Options mail';
      $('#c-mail').textContent = mc + ' €';
      var cy = $('#c-y'); if (cy) cy.textContent = (m * 12).toLocaleString('fr-FR') + ' €';
    };
    rg.addEventListener('input', upd); $$('input[name=fm]').forEach(function (r) { r.addEventListener('change', upd); }); upd();
  }

  /* ---------- 13. afficher le mot de passe ---------- */
  $$('.pwrap .eye').forEach(function (b) {
    b.addEventListener('click', function () {
      var i = b.parentNode.querySelector('input'), show = i.type === 'password';
      i.type = show ? 'text' : 'password';
      b.setAttribute('aria-pressed', show ? 'true' : 'false');
      b.setAttribute('aria-label', show ? 'Masquer le mot de passe' : 'Afficher le mot de passe');
      i.focus();
    });
  });

  /* ---------- 15, 16, 17. formulaires ---------- */
  function setErr(f, msg) {
    var field = f.closest('.field'); if (!field) return;
    var m = field.querySelector('.errmsg');
    if (msg) { field.classList.add('err'); m.textContent = msg; f.setAttribute('aria-invalid', 'true'); }
    else { field.classList.remove('err'); f.removeAttribute('aria-invalid'); }
  }
  var RE_MAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function check(f) {
    var v = (f.type === 'checkbox') ? f.checked : f.value.trim(), n = f.name, msg = '';
    if (f.hasAttribute('data-req') && (f.type === 'checkbox' ? !v : !v)) {
      msg = f.type === 'checkbox' ? 'Merci de cocher cette case pour continuer.' : 'Ce champ est obligatoire.';
    } else if (v && f.type !== 'checkbox') {
      if (f.type === 'email' && !RE_MAIL.test(v)) msg = 'Cette adresse e-mail ne semble pas valide (exemple : nom@domaine.fr).';
      else if (n === 'tel' && !/^[0-9+().\s-]{8,20}$/.test(v)) msg = 'Numéro invalide : utilisez 8 à 20 chiffres (espaces et + acceptés).';
      else if (n === 'domaine' && !/^[a-z0-9][a-z0-9-]{0,61}(\.[a-z]{2,10})?$/i.test(v)) msg = 'Utilisez des lettres, chiffres et tirets, par exemple : maisonolive ou maisonolive.fr.';
      else if (f.minLength > 0 && v.length < f.minLength) msg = 'Merci de saisir au moins ' + f.minLength + ' caractères.';
      else if (f.type === 'password' && v.length < 8) msg = 'Le mot de passe contient au moins 8 caractères.';
    }
    setErr(f, msg); return !msg;
  }
  function wire(form) {
    $$('input,select,textarea', form).forEach(function (f) {
      f.addEventListener('blur', function () { if (f.value || f.type === 'checkbox' || f.closest('.err')) check(f); });
      f.addEventListener('input', function () { if (f.closest('.field.err')) check(f); });
    });
  }
  function validateAll(form) {
    var first = null;
    $$('input[name],select[name],textarea[name]', form).forEach(function (f) {
      if (f.closest('.hp')) return;
      if (!check(f) && !first) first = f;
    });
    if (first) first.focus();
    return !first;
  }
  function busy(btn, on) { btn.disabled = on; btn.classList.toggle('busy', on); }

  var df = $('#demande');
  if (df) {
    wire(df);
    var cdlg = $('#confirm'), alertBad = $('#d-bad'), sendBtn = $('#d-send');
    try { var qf = new URLSearchParams(location.search).get('formule'); if (qf === 'pro' || qf === 'essentiel') df.elements.formule.value = qf; } catch (_) {}
    var vals = function () {
      var o = {}; $$('input[name],select[name],textarea[name]', df).forEach(function (f) { o[f.name] = f.type === 'checkbox' ? f.checked : f.value.trim(); }); return o;
    };
    df.addEventListener('submit', function (e) {
      e.preventDefault(); alertBad.classList.remove('on');
      if (!validateAll(df)) { toast('Corrigez les champs signalés'); return; }
      var v = vals();
      $('#cf-nom').textContent = v.nom; $('#cf-mail').textContent = v.email;
      $('#cf-com').textContent = v.commerce + ' (' + v.ville + ')';
      $('#cf-act').textContent = df.elements.activite.options[df.elements.activite.selectedIndex].text;
      $('#cf-formule').textContent = df.elements.formule.options[df.elements.formule.selectedIndex].text;
      $('#cf-mails').textContent = v.mails ? v.mails + ' adresse(s) mail pro' : 'aucune';
      if (cdlg.showModal) cdlg.showModal(); else cdlg.setAttribute('open', '');
    });
    $('#cf-cancel').addEventListener('click', function () { cdlg.close(); });
    $('#cf-ok').addEventListener('click', function () {
      cdlg.close(); busy(sendBtn, true);
      var v = vals(); v.utm = W.svUtm(); v.page = location.pathname;
      fetch('/api/demande', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(v) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { s: r.status, j: j }; }); })
        .then(function (r) {
          busy(sendBtn, false);
          if (r.s === 200 && r.j.ok) {
            $('#d-ref').textContent = r.j.ref;
            $('#d-ref-btn').setAttribute('data-copy', r.j.ref);
            df.hidden = true; $('#d-done').classList.add('on');
            $('#d-done').setAttribute('tabindex', '-1'); $('#d-done').focus();
            $('#d-done').scrollIntoView({ block: 'start', behavior: reduce ? 'auto' : 'smooth' });
          } else if (r.s === 401) {
            location.replace('/inscription' + location.search);
          } else if (r.s === 429) {
            alertBad.querySelector('span').textContent = 'Trop de demandes depuis votre connexion. Patientez une heure puis réessayez.'; alertBad.classList.add('on');
          } else if (r.s === 422 && r.j.errors) {
            Object.keys(r.j.errors).forEach(function (k) { var f = df.elements[k]; if (f) setErr(f, r.j.errors[k]); });
            alertBad.querySelector('span').textContent = 'Certains champs ne sont pas valides. Vérifiez les messages en rouge.'; alertBad.classList.add('on');
          } else {
            alertBad.querySelector('span').textContent = 'Votre demande n’a pas pu être envoyée (erreur ' + r.s + '). Vos réponses sont conservées : vous pouvez réessayer.'; alertBad.classList.add('on');
          }
        })
        .catch(function () {
          busy(sendBtn, false);
          alertBad.querySelector('span').textContent = 'Connexion impossible pour le moment. Vos réponses sont conservées : vérifiez votre réseau puis réessayez.'; alertBad.classList.add('on');
        });
    });
  }
  /* ----- comptes : inscription, connexion, accès à la demande ----- */
  function api(path, method, body) {
    return fetch(path, { method: method, credentials: 'same-origin', headers: body ? { 'content-type': 'application/json' } : {}, body: body ? JSON.stringify(body) : undefined })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { s: r.status, j: j }; }); });
  }
  /* ----- bandeau « vous consultez le compte d'un client » (administrateur) ----- */
  if (/(?:^|;\s*)sv_imp=1/.test(document.cookie)) {
    api('/api/moi', 'GET').then(function (r) {
      if (r.s === 200 && r.j.impersonation) {
        document.body.classList.add('imp');
        var bar = document.createElement('div'); bar.className = 'impbar'; bar.setAttribute('role', 'status');
        var tx = document.createElement('span'); tx.textContent = 'Vous consultez le compte de ' + (r.j.nom || 'ce client') + ' en tant qu’administrateur (lecture seule).';
        var bt = document.createElement('button'); bt.type = 'button'; bt.textContent = 'Revenir à l’admin';
        bt.addEventListener('click', function () { api('/api/quitter-impersonation', 'POST').then(function () { document.cookie = 'sv_imp=; Path=/; Max-Age=0; Secure; SameSite=Lax'; location.href = '/admin'; }); });
        bar.appendChild(tx); bar.appendChild(bt); document.body.appendChild(bar);
      } else { document.cookie = 'sv_imp=; Path=/; Max-Age=0; Secure; SameSite=Lax'; }
    }).catch(function () {});
  }
  var NEXT = '/commander' + location.search;
  function bad(box, msg) { box.querySelector('span').textContent = msg; box.classList.add('on'); box.focus(); }
  var sf = $('#signup'), lf = $('#login');
  if (sf || lf) {
    api('/api/moi', 'GET').then(function (r) { if (r.s === 200 && r.j.ok) location.replace(r.j.admin ? '/admin' : '/espace'); }).catch(function () {});
  }
  if (sf) {
    wire(sf);
    var sbad = $('#s-bad'), sbtn = sf.querySelector('button[type=submit]');
    sf.addEventListener('submit', function (e) {
      e.preventDefault(); sbad.classList.remove('on');
      var okv = validateAll(sf);
      if (sf.elements.password2.value && sf.elements.password.value !== sf.elements.password2.value) { setErr(sf.elements.password2, 'Les deux mots de passe ne sont pas identiques.'); okv = false; }
      if (!okv) { toast('Corrigez les champs signalés'); return; }
      busy(sbtn, true);
      var o = { nom: sf.elements.nom.value.trim(), email: sf.elements.email.value.trim(), password: sf.elements.password.value, cgv: sf.elements.cgv.checked, site_web_url: sf.elements.site_web_url.value };
      api('/api/inscription', 'POST', o).then(function (r) {
        busy(sbtn, false);
        if (r.s === 200 && r.j.ok) { location.href = NEXT; }
        else if ((r.s === 422 || r.s === 409) && r.j.errors) {
          Object.keys(r.j.errors).forEach(function (k) { var f = sf.elements[k]; if (f) setErr(f, r.j.errors[k]); });
          bad(sbad, r.s === 409 ? 'Un compte existe déjà avec cette adresse. Connectez-vous.' : 'Certains champs ne sont pas valides. Vérifiez les messages en rouge.');
        } else if (r.s === 429) bad(sbad, 'Trop de créations de compte depuis votre connexion. Patientez une heure puis réessayez.');
        else bad(sbad, 'Le compte n’a pas pu être créé (erreur ' + r.s + '). Vos réponses sont conservées : vous pouvez réessayer.');
      }).catch(function () { busy(sbtn, false); bad(sbad, 'Connexion impossible pour le moment. Vérifiez votre réseau puis réessayez.'); });
    });
  }
  if (lf) {
    wire(lf);
    var lbad = $('#l-bad'), lbtn = lf.querySelector('button[type=submit]');
    lf.addEventListener('submit', function (e) {
      e.preventDefault(); lbad.classList.remove('on');
      if (!validateAll(lf)) return;
      busy(lbtn, true);
      api('/api/connexion', 'POST', { email: lf.elements.email.value.trim(), password: lf.elements.password.value }).then(function (r) {
        busy(lbtn, false);
        if (r.s === 200 && r.j.ok) { api('/api/moi', 'GET').then(function (m) { location.href = (m.j && m.j.admin) ? '/admin' : '/espace'; }).catch(function () { location.href = '/espace'; }); }
        else if (r.s === 401) bad(lbad, 'E-mail ou mot de passe incorrect.');
        else if (r.s === 429) bad(lbad, 'Trop d’essais. Patientez quelques minutes puis réessayez.');
        else bad(lbad, 'Connexion impossible (erreur ' + r.s + '). Réessayez.');
      }).catch(function () { busy(lbtn, false); bad(lbad, 'Connexion impossible pour le moment. Vérifiez votre réseau puis réessayez.'); });
    });
  }
  if (df) {
    /* la demande exige un compte : sinon on renvoie vers l'inscription */
    df.style.visibility = 'hidden';
    api('/api/moi', 'GET').then(function (r) {
      if (r.s === 200 && r.j.ok) {
        df.style.visibility = '';
        if (!df.elements.nom.value) df.elements.nom.value = r.j.nom || '';
        if (!df.elements.email.value) df.elements.email.value = r.j.email || '';
        var who = document.createElement('p'); who.className = 'sub'; who.style.marginBottom = '14px';
        who.innerHTML = 'Connecté : <strong></strong> · <button type="button" class="lnk" id="logout">Se déconnecter</button>';
        who.querySelector('strong').textContent = r.j.email;
        df.parentNode.insertBefore(who, df);
        $('#logout').addEventListener('click', function () { api('/api/deconnexion', 'POST', {}).then(function () { location.href = '/connexion'; }); });
      } else location.replace('/inscription' + location.search);
    }).catch(function () { df.style.visibility = ''; });
  }
})();
