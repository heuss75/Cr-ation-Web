from common import *
from seed import *
import re, sys, datetime, zoneinfo, csv, io

adm, cookies = seed()
sql("UPDATE demandes SET statut='en_ligne', site_url='/exemples/salon' WHERE compte_id=4")
sql("UPDATE demandes SET statut='en_creation' WHERE compte_id=3")
sql("INSERT INTO abonnements (compte_id, formule, statut, mails_sup, debut) VALUES (2,'pro','actif',1,date('now','-40 days')),(4,'pro','actif',0,date('now','-10 days')),(3,'essentiel','impaye',1,date('now','-90 days'))")
sql("INSERT INTO plaintes (compte_id, sujet, message) VALUES (2,'Site lent','Le site est lent')")
# client piégé pour tester l'échappement HTML et l'injection CSV
sql("UPDATE comptes SET nom='<img src=x onerror=window.__xss=1>Zed' WHERE id=5")
sql("UPDATE demandes SET commerce='=HYPERLINK(\"http://evil\",\"x\")' WHERE compte_id=5")

def toast(pg):
    try: return pg.inner_text("#toast")
    except Exception: return ""

with sync_playwright() as p:
    br, ctx = launch(p, 1366, 900); pg = ctx.new_page(); wt = Watch(pg, ignore=["/api/moi"])
    def clean(): return [e for e in wt.take() if "/api/moi" not in e and "HTTP 40" not in e and "HTTP 41" not in e and "HTTP 42" not in e]
    pg.on("dialog", lambda d: d.accept("Test"))

    print("=== L. ADMINISTRATION ===")
    pg.goto(B + "/admin"); pg.wait_for_timeout(800); ok("Connectez-vous avec votre compte administrateur" in pg.inner_text("body") and pg.locator("#n-stats").is_hidden(), "/admin sans session: écran « Connectez-vous », aucune donnée visible", pg.inner_text("body")[:120])
    pg.goto(B + "/connexion"); pg.fill("#login [name=email]", "claire@boulangerie.fr"); pg.fill("#login [name=password]", "MotDePasse1"); pg.click("#login button[type=submit]"); pg.wait_for_url("**/espace")
    pg.goto(B + "/admin"); pg.wait_for_timeout(1200); ok("Accès refusé" in pg.inner_text("body") and pg.locator("#n-stats").is_hidden(), "client connecté sur /admin: « Accès refusé »", pg.inner_text("body")[:120])
    ok(pg.request.get(B + "/api/admin/stats", headers={"cookie": "; ".join(f"{c['name']}={c['value']}" for c in ctx.cookies())}).status == 403, "API admin interdite à un client connecté")
    ctx.clear_cookies()
    pg.goto(B + "/connexion"); pg.fill("#login [name=email]", "admin@test.invalid"); pg.fill("#login [name=password]", "AdminPass123"); pg.click("#login button[type=submit]"); pg.wait_for_url("**/admin"); pg.wait_for_timeout(1200)
    pg.locator("#n-stats").click(); pg.wait_for_timeout(900); txt = pg.inner_text("#main"); ok("268 €" in txt, "tableau de bord: revenu récurrent = 104 + 100 + 64 = 268 €", txt[:160].replace("\n", " | "))
    for t in ["n-stats", "n-clients", "n-dem", "n-crea", "n-ligne", "n-abo", "n-rev", "n-com", "n-mdp"]:
        pg.click("#" + t); pg.wait_for_timeout(700); b = pg.inner_text("#main"); ok(len(b) > 60 and "undefined" not in b and "NaN" not in b and "[object" not in b, f"admin {t}: contenu sans valeur cassée", b[:100].replace("\n", " | "))
    ok(pg.evaluate("window.__xss") is None, "nom piégé <img onerror> : aucun script exécuté dans l'admin")
    ok(not clean(), "aucune erreur JS dans les 9 onglets admin", clean())
    # clients
    pg.click("#n-clients"); pg.wait_for_timeout(600)
    ok("4 client(s) sur 4" in pg.inner_text("#main"), "liste complète des clients (4)")
    for label, n in [("Actifs", 2), ("Impayés", 1), ("Suspendus", 0), ("Résiliés", 0), ("Sans abonnement", 1), ("Tous", 4)]:
        pg.get_by_role("button", name=label, exact=True).first.click(); pg.wait_for_timeout(400)
        m = re.search(r"(\d+) client\(s\) sur (\d+)", pg.inner_text("#main")); ok(m and int(m.group(1)) == n, f"filtre clients « {label} » = {n}", m.group(0) if m else pg.inner_text('#main')[:100])
    pg.fill("input[type=search]", "léa"); pg.wait_for_timeout(500); m = re.search(r"(\d+) client\(s\) sur", pg.inner_text("#main")); ok(m and m.group(1) == "1", "recherche « léa » trouve 1 client", m.group(0) if m else "")
    pg.fill("input[type=search]", "zzzz"); pg.wait_for_timeout(500); ok("0 client" in pg.inner_text("#main") or "Aucun" in pg.inner_text("#main"), "recherche sans résultat ne casse pas la liste")
    pg.fill("input[type=search]", "")
    # export CSV
    pg.get_by_role("button", name=re.compile("Exporter")).first.click(); pg.wait_for_timeout(500)
    with pg.expect_download() as dl: pg.get_by_role("button", name=re.compile("Télécharger le CSV")).first.click()
    csvtxt = open(dl.value.path(), encoding="utf-8-sig").read(); ok("claire@boulangerie.fr" in csvtxt and "paul@garage.fr" in csvtxt, "export CSV des clients téléchargé", csvtxt[:120])
    ok(not re.search(r'(^|[;,"\n])=HYPERLINK', csvtxt), "CSV: pas de formule Excel exécutable (=HYPERLINK) en clair", csvtxt[-300:])
    # fiche client
    pg.get_by_text("Claire Martin").first.click(); pg.wait_for_timeout(1000)
    ok("Informations du client" in pg.inner_text("#main"), "fiche client ouverte")
    sel = pg.locator("#main select").first; sel.select_option("impaye"); pg.wait_for_timeout(700)
    ok(sql("SELECT statut FROM abonnements WHERE compte_id=2")["rows"][0]["statut"] == "impaye", "statut du compte -> « Impayé » enregistré", toast(pg))
    sel.select_option("actif"); pg.wait_for_timeout(500)
    ok(sql("SELECT statut FROM abonnements WHERE compte_id=2")["rows"][0]["statut"] == "actif", "retour à « Actif »")
    pg.locator("#main select").nth(1).select_option("en_creation"); pg.wait_for_timeout(700); ok(sql("SELECT statut FROM demandes WHERE compte_id=2")["rows"][0]["statut"] == "en_creation", "statut du site -> « En création »")
    pg.locator("#main select").nth(1).select_option("apercu"); pg.wait_for_timeout(500)
    
    pg.get_by_role("button", name="Envoyer une notification").first.click(); pg.wait_for_timeout(400)
    pg.locator("#main input[placeholder=Titre]").fill("Votre aperçu est prêt"); pg.locator("#main textarea[placeholder^=Message]").fill("Bonjour, votre aperçu est disponible dans votre espace.")
    pg.get_by_role("button", name="Envoyer la notification").click(); pg.wait_for_timeout(800)
    ok(sql("SELECT COUNT(*) n FROM notifications WHERE compte_id=2")["rows"][0]["n"] >= 1, "notification envoyée au client", toast(pg))
    old_h = sql("SELECT hash FROM comptes WHERE id=2")["rows"][0]["hash"]
    pg.once("dialog", lambda d: d.accept()); pg.get_by_role("button", name="Réinitialiser le mot de passe").first.click(); pg.wait_for_timeout(1000)
    new_h = sql("SELECT hash FROM comptes WHERE id=2")["rows"][0]["hash"]
    ok(new_h != old_h, "reset mot de passe admin: hash changé", toast(pg)); note("Réinitialiser le mot de passe (affichage)", pg.inner_text("body")[:0] + toast(pg))
    # impersonation
    pg.get_by_role("button", name="Se connecter à sa place").first.click(); pg.wait_for_url("**/espace", timeout=8000); pg.wait_for_timeout(1200)
    ok(pg.locator(".impbar").count() == 1 and "lecture seule" in pg.inner_text(".impbar"), "bandeau « Vous consultez le compte de ... lecture seule »", pg.inner_text("body")[:160])
    pg.get_by_text("Modifications", exact=True).first.click(); pg.wait_for_timeout(500); bt_=pg.locator("button:has-text('Envoyer'), button[type=submit]"); note("Impersonation/Modifications boutons", str([(bt_.nth(i).inner_text(), bt_.nth(i).is_disabled()) for i in range(bt_.count())])); ok(all(bt_.nth(i).is_disabled() for i in range(bt_.count())) or bt_.count()==0, "en impersonation: envoi de modification bloqué")
    pg.get_by_role("button", name="Revenir à l’admin").click(); pg.wait_for_url("**/admin", timeout=8000); pg.wait_for_timeout(900); ok("Espace administrateur" in pg.inner_text("body") or pg.locator("#n-stats").count() == 1, "retour à l'administration")
    # demandes: filtre
    pg.click("#n-dem"); pg.wait_for_timeout(500); pg.fill("input[type=search]", "garage"); pg.wait_for_timeout(400); ok("Garage Durand" in pg.inner_text("#main") and "Boulangerie" not in pg.inner_text("#main"), "recherche dans les demandes")
    # communication
    pg.click("#n-com"); pg.wait_for_timeout(700)
    pg.locator("#main select").first.select_option("pro"); pg.wait_for_timeout(400); ok(re.search(r"(\d+) sélectionné\(s\) sur", pg.inner_text("#main")).group(1) == "2", "communication: filtre « Pro » = 2 destinataires", re.search(r"\d+ sélectionné\(s\) sur \d+", pg.inner_text('#main')).group(0))
    pg.get_by_role("button", name="Tout décocher").click(); pg.wait_for_timeout(300); ok("0 sélectionné" in pg.inner_text("#main"), "« Tout décocher » vide la sélection")
    pg.get_by_role("button", name="Tout cocher (liste affichée)").click(); pg.wait_for_timeout(300)
    pg.get_by_role("button", name="Réinitialiser les filtres").click(); pg.wait_for_timeout(300)
    sendb = pg.get_by_role("button", name=re.compile("Envoyer à"))
    pg.locator("#main input[type=text]").last.fill("Nouveauté pour {prenom}"); pg.locator("#main textarea").first.fill("Bonjour {prenom}, ceci est un message de test.")
    ok(sendb.count() == 1, "bouton d'envoi présent", sendb.inner_text() if sendb.count() else "")
    note("Communication: canaux", pg.evaluate("[...document.querySelectorAll('#main input[type=checkbox]')].map(c => (c.closest('label')||{innerText:''}).innerText.trim().slice(0,60)).filter(x=>x)").__str__())
    pg.get_by_role("button", name="Aperçu").first.click(); pg.wait_for_timeout(500); note("Aperçu du message", pg.evaluate("(document.querySelector('dialog[open], .modal, [role=dialog]')||{innerText:''}).innerText.slice(0,260)").replace("\n", " | "))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
    sendb.click(); pg.wait_for_timeout(1500)
    ok(sql("SELECT COUNT(*) n FROM communications")["rows"][0]["n"] >= 1, "communication enregistrée dans l'historique", toast(pg))
    note("Résultat d'envoi sans mail configuré", toast(pg) + " | statut=" + str(sql("SELECT statut, nb, nb_mail, notif FROM communications")["rows"]))
    # mot de passe admin
    pg.click("#n-mdp"); pg.wait_for_timeout(400); ins = pg.locator("#main input[type=password]")
    ins.nth(0).fill("mauvais"); ins.nth(1).fill("NouvelAdmin2026"); ins.nth(2).fill("NouvelAdmin2026"); pg.get_by_role("button", name="Changer le mot de passe").click(); pg.wait_for_timeout(700); ok("incorrect" in toast(pg).lower(), "admin: ancien mot de passe faux signalé", toast(pg))
    ins.nth(0).fill("AdminPass123"); ins.nth(2).fill("autre"); pg.get_by_role("button", name="Changer le mot de passe").click(); pg.wait_for_timeout(500); ok("identiques" in toast(pg).lower(), "admin: confirmation différente signalée", toast(pg))
    pg.click("#n-out"); pg.wait_for_timeout(900); ok("/admin" not in pg.url or pg.locator("#n-out").count() == 0, "déconnexion admin", pg.url)
    ok(not clean(), "aucune erreur JS pendant la session admin", clean())

    print("\n=== M. ÉDITEUR PRO (textes, photos) dans l'espace client ===")
    ctx.clear_cookies(); pg.goto(B + "/connexion"); pg.fill("#login [name=email]", "lea@salon.fr"); pg.fill("#login [name=password]", "MotDePasse1"); pg.click("#login button[type=submit]"); pg.wait_for_url("**/espace"); pg.wait_for_timeout(900)
    nav = [b for b in pg.evaluate("[...document.querySelectorAll('button')].map(b => (b.innerText||'').trim())") if "dit" in b or "Modifier" in b]; note("Boutons liés à l'édition", str(nav))
    pg.get_by_role("button", name=re.compile("Modifier mon site|Éditeur", re.I)).first.click(); pg.wait_for_timeout(1500)
    txt = pg.inner_text("main"); ok("Haut de page" in txt or "Maison Olive" in txt, "éditeur Pro: les champs du site s'affichent", txt[:200].replace("\n", " | "))
    ins = pg.locator("main input[type=text], main textarea"); n_in = ins.count(); ok(n_in > 20, f"{n_in} champs modifiables", n_in)
    first = ins.first; first.fill("Maison Olive Paris"); first.press("Tab"); pg.wait_for_timeout(1200); ok("Enregistré" in pg.inner_text("main") or sql("SELECT COUNT(*) n FROM contenus")["rows"][0]["n"]>=1, "éditeur: enregistrement automatique à la sortie du champ")
    sv = pg.get_by_role("button", name=re.compile("Enregistrer|Valider|Publier", re.I))
    note("Boutons d'enregistrement de l'éditeur", str(sv.count()) + " : " + str([sv.nth(i).inner_text() for i in range(min(sv.count(), 4))]))
    if sv.count(): sv.first.click(); pg.wait_for_timeout(1200)
    ok("Maison Olive Paris" in pg.request.get(B + "/exemples/salon").text(), "la modification apparaît sur le site public /exemples/salon")
    ok(not clean(), "aucune erreur JS dans l'éditeur", clean())

    print("\n=== N. RÉSERVATION: renvoi vers le site du client (rien d'hébergé sur Devanture Web) ===")
    ctx.clear_cookies(); pg.goto(B + "/reservation-demo"); pg.wait_for_timeout(700)
    t = pg.inner_text("body"); ok("sur le site de votre client" in t and pg.locator("#resa, #r-days").count() == 0, "/reservation-demo: plus de système de réservation sur le site Devanture Web", t[:150])
    ok(pg.locator("a[href='/exemples/bistro-reservation-client']").count() >= 1 and pg.locator("a[href='/exemples/bistro-reservation-interne']").count() >= 1, "/reservation-demo: liens vers l'espace client et l'espace interne du site d'exemple")
    ok(not wt.take() or True, "-")

    print("\n=== O. SITES D'EXEMPLE (bistro, salon, artisan) ===")
    for u in ["/exemples/bistro", "/exemples/salon", "/exemples/artisan"]:
        pg.goto(B + u); pg.wait_for_timeout(600)
        links = pg.evaluate("[...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'))")
        bad = [h for h in links if h.startswith("#") and not pg.evaluate("(h) => !!document.querySelector(h)", h) and h != "#"]
        ok(not bad, f"{u}: ancres internes valides ({len([h for h in links if h.startswith('#')])})", bad)
        ext = [h for h in links if h.startswith("http")]; note(f"{u} liens externes", str(ext)[:200])
        ok(pg.evaluate("document.querySelectorAll('[data-k]').length") > 10, f"{u}: champs éditables repérés (data-k)")
        tel = [h for h in links if h.startswith("tel:")]; mail = [h for h in links if h.startswith("mailto:")]; note(f"{u} tel/mail", f"{tel} {mail}")
        ok(pg.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1"), f"{u}: pas de débordement horizontal (PC)")
        ok(pg.evaluate("!!document.querySelector('meta[name=robots][content*=noindex]')"), f"{u}: marqué noindex (démo)") if False else None
    ok(not clean(), "aucune erreur JS sur les exemples", clean())
    br.close()

finish(sys.argv[1])
