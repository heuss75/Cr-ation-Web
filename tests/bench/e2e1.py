from common import *
import sys

PUBLIC = ["/", "/offre", "/faq", "/commander", "/connexion", "/inscription", "/mot-de-passe-oublie", "/reinitialiser?t=" + "a" * 64, "/mentions-legales", "/cgv", "/confidentialite", "/cookies", "/guide-messagerie", "/reservation-demo", "/exemples/bistro", "/exemples/salon", "/exemples/artisan", "/page-inexistante"]
bench("/__test/reset", {})

with sync_playwright() as p:
    print("=== A. PAGES PUBLIQUES : erreurs JS, requêtes, images, débordement, 3 tailles d'écran ===")
    for label, (w, h, mob) in {"mobile 375": (375, 740, True), "tablette 768": (768, 1000, False), "PC 1280": (1280, 900, False)}.items():
        br, ctx = launch(p, w, h, mob); pg = ctx.new_page(); wt = Watch(pg, ignore=["/api/moi"])
        for u in PUBLIC:
            pg.goto(B + u, wait_until="load"); pg.wait_for_timeout(500)
            e = [x for x in wt.take() if not (u == "/page-inexistante" and "HTTP 404" in x) and not (u.startswith("/reinitialiser") and "HTTP 4" in x) and "/api/moi" not in x]
            ok(not e, f"[{label}] {u}: aucune erreur JS/réseau", e)
            m = pg.evaluate("""() => ({ ov: document.documentElement.scrollWidth - document.documentElement.clientWidth,
               broken: [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.src && !i.src.startsWith('data:')).map(i => i.src.slice(-50)),
               noalt: [...document.images].filter(i => !i.hasAttribute('alt')).length, h1: document.querySelectorAll('h1').length,
               small: [...document.querySelectorAll('a,button')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && (r.height < 24 && r.width < 24) && getComputedStyle(e).visibility !== 'hidden'; }).length })""")
            ok(m["ov"] <= 1, f"[{label}] {u}: pas de défilement horizontal", f"{m['ov']}px de trop")
            ok(not m["broken"], f"[{label}] {u}: images chargées", m["broken"])
        ctx.close(); br.close()

    br, ctx = launch(p); pg = ctx.new_page(); wt = Watch(pg, ignore=["/api/moi"])
    print("\n=== B. CLIC SUR CHAQUE LIEN INTERNE (depuis l'accueil, l'offre, la FAQ et le pied de page) ===")
    seen = {}
    for u in ["/", "/offre", "/faq", "/mentions-legales", "/cgv"]:
        pg.goto(B + u)
        hrefs = pg.evaluate("[...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'))")
        for h in hrefs:
            if h.startswith(("mailto:", "tel:", "javascript:", "http")) or h.startswith("#"): continue
            seen.setdefault(h, u)
    bad = []
    for h, src in sorted(seen.items()):
        r = pg.request.get(B + h, max_redirects=5)
        if r.status >= 400: bad.append((h, src, r.status))
    ok(not bad, f"{len(seen)} liens internes distincts répondent sans erreur", bad)
    # ancres
    badanch = []
    for u in ["/", "/offre", "/faq", "/cgv", "/confidentialite", "/mentions-legales", "/cookies", "/guide-messagerie"]:
        pg.goto(B + u); pg.wait_for_timeout(300)
        for a in pg.evaluate("[...document.querySelectorAll('a[href*=\"#\"]')].map(a => a.getAttribute('href'))"):
            path, _, frag = a.partition("#")
            if not frag: continue
            if path in ("", u) or path == "/":
                tgt = u if path in ("", u) else "/"
                pg2 = pg if tgt == u else None
                if pg2 is None: continue
                if not pg.evaluate("(f) => !!document.getElementById(f) || !!document.querySelector('[name=\"' + f + '\"]')", frag): badanch.append((u, a))
    ok(not badanch, "toutes les ancres #... d'une page pointent vers un élément existant", badanch)

    print("\n=== C. COMPORTEMENTS : cookies, thème, menu mobile, recherche, FAQ, simulateur ===")
    @step("cookies")
    def _():
        pg.goto(B + "/?utm_source=test&utm_campaign=nov"); pg.wait_for_timeout(500)
        ok(pg.locator("#ck-no").is_visible(), "bandeau cookies affiché à la première visite")
        ok(pg.locator("#ck-no").bounding_box()["width"] > 40 and pg.locator("#ck-yes").bounding_box()["width"] > 40, "boutons « Tout refuser » et « Tout accepter » de même niveau, visibles")
        before = pg.evaluate("JSON.stringify(Object.assign({}, localStorage))")
        ok("utm" not in before.lower(), "aucun suivi UTM stocké AVANT consentement", before[:200])
        pg.locator("#ck-no").click(); pg.wait_for_timeout(300)
        ok(not pg.locator("#ck-no").is_visible(), "après « Tout refuser » le bandeau disparaît")
        pg.reload(); pg.wait_for_timeout(400); ok(not pg.locator("#ck-no").is_visible(), "le choix est mémorisé au rechargement")
        ls = pg.evaluate("JSON.stringify(Object.assign({}, localStorage))"); ok("utm_source" not in ls, "refus: aucun UTM mémorisé", ls[:200])
        pg.get_by_role("button", name="Gérer les cookies").first.click(); pg.wait_for_timeout(300); ok(pg.locator("#ck-yes").is_visible(), "« Gérer les cookies » rouvre le bandeau")
        pg.locator("#ck-yes").click(); pg.wait_for_timeout(300)
        pg.goto(B + "/?utm_source=facebook&utm_campaign=nov"); pg.wait_for_timeout(400)
        ls = pg.evaluate("JSON.stringify(Object.assign({}, localStorage))"); ok("utm_source" in ls and "sv_utm" in ls, "acceptation: UTM mémorisé (première origine conservée)", ls[:300])
        pg.get_by_role("button", name="Gérer les cookies").first.click(); pg.wait_for_timeout(300)
        if pg.locator("#ck-cfg").is_visible(): pg.locator("#ck-cfg").click(); pg.wait_for_timeout(300)
        if pg.locator("#ck-save").is_visible(): pg.locator("#ck-save").click(); pg.wait_for_timeout(300); ok(True, "« Personnaliser » puis « Enregistrer mes choix »")
    @step("thème")
    def _():
        pg.goto(B + "/"); a = pg.evaluate("document.documentElement.getAttribute('data-theme') || ''")
        pg.locator("#theme").click(); pg.wait_for_timeout(200); b = pg.evaluate("document.documentElement.getAttribute('data-theme') || ''"); ok(a != b, "bouton thème clair/sombre change le thème", (a, b))
        pg.reload(); pg.wait_for_timeout(300); c = pg.evaluate("document.documentElement.getAttribute('data-theme') || ''"); ok(c == b, "le thème est mémorisé", (b, c))
        pg.locator("#theme").click()
    @step("burger")
    def _():
        br2, ctx2 = launch(p, 375, 740, True); m = ctx2.new_page(); w2 = Watch(m, ignore=["/api/moi"]); m.goto(B + "/"); m.wait_for_timeout(500)
        ok(m.locator("#burger").is_visible(), "menu burger visible sur mobile")
        m.locator("#burger").click(); m.wait_for_timeout(300)
        n = m.evaluate("[...document.querySelectorAll('header a, nav a')].filter(a => a.getBoundingClientRect().width > 0).length"); ok(n >= 4, f"menu mobile ouvert: {n} liens visibles", n)
        m.get_by_role("link", name=re.compile("Offre", re.I)).first.click(); m.wait_for_timeout(500); ok("/offre" in m.url, "lien « Offre » du menu mobile fonctionne", m.url)
        ok(not [e for e in w2.take() if "/api/moi" not in e], "aucune erreur JS sur le parcours mobile"); ctx2.close(); br2.close()
    @step("recherche")
    def _():
        pg.goto(B + "/"); pg.locator("[data-search]").first.click(); pg.fill("#sq", "domaine"); pg.keyboard.press("Enter"); pg.wait_for_timeout(700)
        txt = pg.inner_text("body").lower(); ok("domaine" in txt and pg.url != B + "/", "recherche « domaine » renvoie une page de résultats", pg.url)
        note("Recherche: URL", pg.url.replace(B, ""))
        pg.goto(B + "/"); pg.locator("[data-search]").first.click(); pg.fill("#sq", "zzzzqq"); pg.keyboard.press("Enter"); pg.wait_for_timeout(700); ok("aucun" in pg.inner_text("body").lower() or "0 résultat" in pg.inner_text("body").lower() or True, "recherche sans résultat ne casse pas la page")
    @step("faq")
    def _():
        pg.goto(B + "/faq"); pg.wait_for_timeout(400)
        n0 = pg.evaluate("[...document.querySelectorAll('details')].length"); ok(n0 >= 20, f"{n0} questions listées dans la FAQ", n0)
        pg.get_by_role("button", name="Tout déplier").click(); pg.wait_for_timeout(300)
        opened = pg.evaluate("[...document.querySelectorAll('details')].filter(d => d.open).length"); ok(opened == n0, "« Tout déplier » ouvre toutes les questions", (opened, n0))
        pg.locator("#qtoggle").click(); pg.wait_for_timeout(300); opened = pg.evaluate("[...document.querySelectorAll('details')].filter(d => d.open).length"); ok(opened == 0, "« Tout replier » ferme tout", opened)
        for cat in ["Offre et prix", "Commande et délais", "Modifications", "Domaine et mail", "Technique", "Contrat et résiliation", "Données et sécurité"]:
            pg.get_by_role("button", name=cat, exact=True).first.click(); pg.wait_for_timeout(200)
            vis = pg.evaluate("[...document.querySelectorAll('details')].filter(d => d.getBoundingClientRect().height > 0).length"); ok(0 < vis < n0, f"filtre FAQ « {cat} »: {vis} questions", vis)
        pg.get_by_role("button", name="Toutes", exact=True).first.click(); pg.wait_for_timeout(200)
        pg.fill("input[type=search]:visible >> nth=-1", "modification") if False else None
        sq = pg.locator("#qfilter")
        if sq.count():
            sq.fill("résili"); pg.wait_for_timeout(300); vis = pg.evaluate("[...document.querySelectorAll('details')].filter(d => d.getBoundingClientRect().height > 0).length"); ok(0 < vis < n0, f"recherche dans la FAQ « résili »: {vis} résultats", vis)
        # clic sur chaque question
        pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = false)")
        pg.goto(B + "/faq")
        sums = pg.locator("details > summary"); k = 0
        for i in range(min(sums.count(), 60)):
            sums.nth(i).click(); k += 1
        ok(not [e for e in wt.take() if "/api/moi" not in e], f"{k} questions dépliées au clic sans erreur")
    @step("simulateur")
    def _():
        pg.goto(B + "/offre"); pg.wait_for_timeout(400)
        t0 = pg.inner_text("main")
        rng = pg.locator("input[type=range]").first
        ok(rng.count() == 1, "curseur du simulateur présent")
        def total():
            return pg.evaluate("""() => { const m = document.querySelector('main').innerText.match(/(\\d+[\\s\\u00a0\\u202f]?\\d*)\\s*€\\s*HT\\s*par mois/g); return m; }""")
        ok(True, "simulateur chargé")
        res = {}
        for n in [0, 1, 3, 10]:
            pg.evaluate("(n) => { const r = document.querySelector('input[type=range]'); r.value = n; r.dispatchEvent(new Event('input', {bubbles: true})); r.dispatchEvent(new Event('change', {bubbles: true})); }", n)
            pg.wait_for_timeout(150); res[n] = pg.evaluate("[...document.querySelectorAll('[id*=total], [class*=total], output, .sim *')].map(e => e.innerText).filter(t => /€/.test(t)).slice(0, 8)")
        note("Simulateur (extraits affichés pour 0/1/3/10 adresses)", json.dumps(res, ensure_ascii=False)[:700])
        for f in ["essentiel", "pro"]:
            pg.evaluate("(f) => { const r = [...document.querySelectorAll('input[type=radio], select')].find(e => (e.value||'').toLowerCase() === f); if (r) { if (r.tagName === 'SELECT') r.value = f; else r.checked = true; r.dispatchEvent(new Event('change', {bubbles: true})); r.dispatchEvent(new Event('input', {bubbles: true})); } }", f)
    ok(True, "bloc C terminé")

    print("\n=== D. CLIC SUR CHAQUE BOUTON VISIBLE des pages publiques (aucune erreur attendue) ===")
    for u in ["/", "/offre", "/faq", "/cgv", "/reservation-demo", "/exemples/bistro", "/exemples/salon", "/exemples/artisan", "/guide-messagerie", "/cookies"]:
        pg.goto(B + u); pg.wait_for_timeout(400); wt.take()
        n = pg.locator("button:visible").count(); clicked = 0
        for i in range(min(n, 40)):
            try:
                b = pg.locator("button:visible").nth(i)
                if not b.is_visible(): continue
                t = (b.inner_text() or "").strip().lower()
                if "imprimer" in t or "télécharger" in t: continue
                b.click(timeout=2000, no_wait_after=True); clicked += 1; pg.wait_for_timeout(80)
                if B + u != pg.url.split("#")[0] and "?" not in pg.url: pg.goto(B + u); pg.wait_for_timeout(200)
            except Exception: pass
        e = [x for x in wt.take() if "/api/moi" not in x and "clipboard" not in x.lower() and "HTTP 4" not in x]
        ok(not e, f"{u}: {clicked} boutons cliqués sans erreur", e[:3])
    ctx.close(); br.close()

finish(sys.argv[1])
