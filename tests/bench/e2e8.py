from common import *
import h as H
import re, os, json as J, datetime
FILES = os.path.abspath("files")
bench("/__test/reset", {})
ADM = H.pw_hash_admin()
def mk(nom, email, ip, commerce, parrain=None):
    c = H.C(ip=ip); body = {"nom": nom, "email": email, "password": "MotDePasse1", "cgv": True}
    if parrain: body["parrain"] = parrain
    assert c.post("/api/inscription", body).json["ok"]
    assert c.post("/api/demande", {"nom": nom, "email": email, "tel": "0612345678", "commerce": commerce, "activite": "boutique", "ville": "Lyon", "formule": "pro", "mails": 1, "cgv": True, "message": "Bonjour"}).json["ok"]
    return c
def q1(q, *a):
    r = sql(q, *a)["rows"][0]; return r[0] if isinstance(r, list) else list(r.values())[0]
def cid(e): return q1("SELECT id FROM comptes WHERE email=?", e)
def did(e): return q1("SELECT d.id FROM demandes d JOIN comptes c ON c.id=d.compte_id WHERE c.email=?", e)
import base64
PNG = base64.b64encode(open(FILES + "/logo.png", "rb").read()).decode()
A = mk("Claire Martin", "claire@a.invalid", "203.0.113.51", "Boulangerie Martin")      # dossier complet
Bp = mk("Paul Durand", "paul@b.invalid", "203.0.113.52", "Garage Durand")                 # nouvelle, sans dossier
Cc = mk("Léa Roy", "lea@c.invalid", "203.0.113.53", "Salon Léa")                         # aperçu + ajustements
Dd = mk("Tom Resto", "tom@d.invalid", "203.0.113.54", "Chez Tom")                        # en ligne, résiliation
Ee = mk("Eva Coach", "eva@e.invalid", "203.0.113.55", "<img src=x onerror=window.__xss=1>Eva Fit")  # XSS + avis
for k, v in {"description": "Boulangerie artisanale", "horaires": "Mar-Sam 7h-19h", "adresse_pub": "12 rue des Fleurs", "tel_pub": "0412345678", "services": "Baguette 1,20 €"}.items(): pass
A.post("/api/espace/dossier", {"champs": {"description": "Boulangerie artisanale", "horaires": "Mar-Sam 7h-19h", "adresse_pub": "12 rue des Fleurs", "tel_pub": "0412345678", "services": "Baguette 1,20 €"}})
A.post("/api/espace/fichier", {"categorie": "logo", "nom": "logo.png", "mime": "image/png", "data": PNG}); A.post("/api/espace/dossier-termine", {})
ADM.post("/api/admin/demande", {"id": did("lea@c.invalid"), "statut": "apercu"}); Cc.post("/api/espace/apercu", {"action": "changements", "message": "Agrandir le logo s'il vous plaît."})
ADM.post("/api/admin/abonnement", {"compte_id": cid("tom@d.invalid"), "formule": "pro", "statut": "actif", "mails_sup": 0})
ADM.post("/api/admin/demande", {"id": did("tom@d.invalid"), "statut": "en_ligne"}); Dd.post("/api/espace/resiliation", {"motif": "prix", "message": "Trop cher", "confirme": True})
ADM.post("/api/admin/abonnement", {"compte_id": cid("eva@e.invalid"), "formule": "pro", "statut": "actif", "mails_sup": 0})
ADM.post("/api/admin/demande", {"id": did("eva@e.invalid"), "statut": "en_ligne"}); Ee.post("/api/espace/avis", {"note": 5, "commentaire": "Génial <b>merci</b>", "publication": True})
ADM.post("/api/admin/tache", {"titre": "Relancer Paul <img src=x onerror=window.__xss=2>", "compte_id": cid("paul@b.invalid"), "echeance": (datetime.date.today() - datetime.timedelta(days=3)).isoformat()})
ADM.post("/api/admin/suivi", {"compte_id": cid("paul@b.invalid"), "rappel_le": datetime.date.today().isoformat(), "motif": "Rappeler pour les photos"})
vv = H.C(ip="203.0.113.99")
for p_ in ["/", "/", "/offre", "/faq"]: vv.post("/api/vue", {"p": p_})

def login(pg, email, pw):
    pg.goto(B_ + "/connexion"); pg.fill("#login [name=email]", email); pg.fill("#login [name=password]", pw); pg.click("#login button[type=submit]"); pg.wait_for_url("**/admin**", timeout=8000); pg.wait_for_selector("#app:not([hidden])")
B_ = "http://localhost:8787"
def toast(pg):
    try: return pg.inner_text("#toast")
    except Exception: return ""
def tab(pg, name): pg.locator(".cf-tabs button", has_text=name).first.click(); pg.wait_for_timeout(900)

with sync_playwright() as p:
    br, ctx = launch(p, 1366, 900); pg = ctx.new_page(); wt = Watch(pg, ignore=["/api/moi"])
    clean = lambda: [e for e in wt.take() if "/api/moi" not in e and "HTTP 40" not in e and "HTTP 41" not in e and "HTTP 42" not in e]
    pg.on("dialog", lambda d: d.accept())
    login(pg, "admin@test.invalid", "AdminPass123"); pg.wait_for_timeout(1200)

    print("=== A. ÉCRAN « À TRAITER AUJOURD'HUI » ===")
    t = pg.inner_text("#main")
    ok("À traiter aujourd’hui" in pg.inner_text("#main h1"), "l'admin arrive directement sur « À traiter aujourd'hui »", t[:80])
    for needle, name in [("Dossier complet : créer le site de Boulangerie Martin", "dossier complet"), ("Nouvelle demande : Garage Durand", "nouvelle demande"), ("Ajustements demandés : Salon Léa", "ajustements"), ("Résiliation demandée", "résiliation"), ("Avis à modérer (5/5)", "avis"), ("Relancer Paul", "tâche en retard"), ("À rappeler", "rappel du jour")]:
        ok(needle in t, f"À traiter contient : {name}", t[:200])
    ok(pg.inner_text("#c-today").strip() not in ("", "0"), "pastille du menu = nombre d'urgents", pg.inner_text("#c-today"))
    ok(pg.evaluate("window.__xss") is None, "titre de tâche et nom de commerce piégés : aucun script exécuté")
    ok("Urgent (" in t and "À faire (" in t, "deux groupes : Urgent / À faire")
    pg.locator(".todol li", has_text="Ajustements demandés").get_by_role("button", name="Ouvrir").click(); pg.wait_for_timeout(1200)
    ok(pg.locator(".cf-tabs [aria-selected=true]").inner_text().startswith("Suivi"), "« Ouvrir » mène à l'onglet Suivi & notes de la fiche", pg.locator(".cf-tabs [aria-selected=true]").inner_text())

    print("=== B. FICHE CLIENT : SUIVI, TÂCHES, DOSSIER ===")
    t = pg.inner_text("#main")
    ok("Ajustements demandés" in t and "Agrandir le logo" in t, "retour d'aperçu visible")
    pg.get_by_role("button", name="Marquer comme traité").click(); pg.wait_for_timeout(1200)
    ok("le client est prévenu" in toast(pg), "ajustements marqués traités", toast(pg))
    ok(any("Ajustements effectués" in n["titre"] for n in Cc.get("/api/espace").json["notifications"]), "le client reçoit la notification")
    # tâche / to-do
    pg.get_by_label("Titre de la tâche").fill("Appeler Léa pour les photos"); pg.get_by_label("Détails").fill("Elle préfère l'après-midi. Numéro perso : 06…"); pg.get_by_role("button", name="Ajouter", exact=True).click(); pg.wait_for_timeout(1200)
    ok("Appeler Léa pour les photos" in pg.inner_text(".task"), "tâche ajoutée avec information interne")
    ok("Elle préfère l'après-midi" in pg.inner_text("#main"), "information interne affichée")
    cb = pg.get_by_label("Marquer comme fait : Appeler Léa pour les photos"); cb.check(); pg.wait_for_timeout(1000)
    ok("done" in pg.locator("li.task", has_text="Appeler Léa pour les photos").get_attribute("class") and pg.evaluate("getComputedStyle(document.querySelector('li.task.done b')).textDecorationLine") == "line-through", "cocher = tâche barrée")
    pg.get_by_label("Marquer comme fait : Appeler Léa pour les photos").uncheck(); pg.wait_for_timeout(800)
    ok("done" not in (pg.locator("li.task", has_text="Appeler Léa pour les photos").get_attribute("class") or ""), "décocher = tâche active")
    pg.get_by_role("button", name="Supprimer la tâche Appeler Léa pour les photos").click(); pg.wait_for_timeout(900)
    ok("Appeler Léa pour les photos" not in pg.inner_text("#main"), "suppression de la tâche")
    # statuts prospect
    opts = pg.locator("select[aria-label='x']").count()
    sel = pg.get_by_label("Statut du prospect"); labels = sel.locator("option").all_inner_texts()
    ok(len(labels) == 12 and all(x in labels for x in ["Hésite", "À rappeler", "Reviendra plus tard", "A refusé", "Sans réponse", "Trouve ça trop cher", "Parti chez un concurrent", "Abandonnée"]), "12 statuts de prospect proposés", labels)
    sel.select_option("plus_tard"); d = (datetime.date.today() + datetime.timedelta(days=14)).isoformat(); pg.get_by_label("Date du rappel").fill(d); pg.get_by_label("Note de rappel").fill("Veut réfléchir, rappeler après les vacances"); pg.get_by_role("button", name="Enregistrer le suivi").click(); pg.wait_for_timeout(1500)
    ok("Suivi enregistré" in toast(pg) or "Suivi" in pg.inner_text("#main"), "suivi enregistré", toast(pg))
    ok(q1("SELECT statut FROM demandes WHERE id=?", did("lea@c.invalid")) == "plus_tard" and q1("SELECT rappel_le FROM suivi WHERE compte_id=?", cid("lea@c.invalid")) == d, "statut et rappel bien enregistrés en base")
    # dossier de Claire
    pg.locator("#n-clients").click(); pg.wait_for_timeout(800); pg.get_by_text("Claire Martin").first.click(); pg.wait_for_timeout(1200); tab(pg, "Suivi")
    t = pg.inner_text("#main"); ok("Boulangerie artisanale" in t and "Mar-Sam 7h-19h" in t and "Complet le" in t, "dossier du client lisible par l'admin")
    ok(pg.locator(".fich img").evaluate("i => i.complete && i.naturalWidth > 0"), "miniature du logo chargée")
    with pg.expect_popup() as pu: pg.locator(".fich").get_by_role("link", name="Ouvrir").click()
    ok(pu.value.url.endswith("/api/admin/fichier?id=1") or "/api/admin/fichier" in pu.value.url, "« Ouvrir » ouvre le fichier"); pu.value.close()
    ok(pg.locator(".fich a[download]").count() == 1, "lien Télécharger présent")

    print("=== C. RÉSILIATION, AVIS, PARRAINAGE (fiche) ===")
    pg.locator("#n-clients").click(); pg.wait_for_timeout(800); pg.get_by_text("Tom Resto").first.click(); pg.wait_for_timeout(1200); tab(pg, "Suivi")
    t = pg.inner_text("#main"); ok("Le prix" in t and "effet le" in t and "Trop cher" in t, "demande de résiliation affichée : motif, date, message", t[-700:])
    pg.get_by_role("button", name="Marquer traitée").click(); pg.wait_for_timeout(1200); ok("traitée" in pg.inner_text("#main"), "résiliation marquée traitée")
    pg.get_by_role("button", name="Remettre à traiter").click(); pg.wait_for_timeout(1000); ok("à traiter" in pg.inner_text("#main"), "remise à traiter")
    pg.locator("#n-clients").click(); pg.wait_for_timeout(800); pg.get_by_text("Eva Coach").first.click(); pg.wait_for_timeout(1200); tab(pg, "Suivi")
    ok("Génial" in pg.inner_text("#main") and pg.evaluate("window.__xss") is None and pg.locator("#main b:has-text('merci')").count() == 0, "avis affiché sans interpréter le HTML")
    pg.get_by_role("button", name="Publier").first.click(); pg.wait_for_timeout(1200)
    ok(H.C().get("/api/avis").json["nb"] == 1, "avis publié depuis la fiche client")
    t = pg.inner_text("#main"); code = re.search(r"DW-[A-Z0-9]{5}", t); ok(bool(code), "code de parrainage du client visible")
    pg.locator("#n-clients").click(); pg.wait_for_timeout(800); pg.get_by_text("Paul Durand").first.click(); pg.wait_for_timeout(1200); tab(pg, "Suivi")
    tom_code = q1("SELECT code FROM parrains WHERE compte_id=?", cid("tom@d.invalid")) if sql("SELECT COUNT(*) FROM parrains WHERE compte_id=?", cid("tom@d.invalid")) else None
    Dd.get("/api/espace/parcours"); tom_code = q1("SELECT code FROM parrains WHERE compte_id=?", cid("tom@d.invalid"))
    pg.get_by_label("Code de parrainage à appliquer").fill(tom_code); pg.get_by_role("button", name="Appliquer le code").click(); pg.wait_for_timeout(1200)
    ok("Code appliqué" in toast(pg) and "Parrainé par Tom Resto" in pg.inner_text("#main"), "admin applique un code de parrainage pour un client", toast(pg))
    ADM.post("/api/admin/abonnement", {"compte_id": cid("paul@b.invalid"), "formule": "essentiel", "statut": "actif", "mails_sup": 0})
    pg.reload(); pg.wait_for_selector("#app:not([hidden])"); pg.locator("#n-clients").click(); pg.wait_for_timeout(800); pg.get_by_text("Paul Durand").first.click(); pg.wait_for_timeout(1200); tab(pg, "Suivi")
    ok("1 mois offert (bienvenue)" in pg.inner_text("#main"), "à l'activation de l'abonnement : mois offert crédité", pg.inner_text("#main")[-500:])
    pg.get_by_role("button", name="Marquer utilisé (déduit d’une facture)").click(); pg.wait_for_timeout(1000); ok("Utilisé le" in pg.inner_text("#main"), "mois offert marqué utilisé")

    print("=== D. AVIS, VISITES, SAUVEGARDE ===")
    pg.locator("#n-avis").click(); pg.wait_for_timeout(900); ok("Eva Fit" in pg.inner_text("#main") or "Eva F" in pg.inner_text("#main"), "page Avis : liste", pg.inner_text("#main")[:200])
    pg.get_by_role("button", name="Refuser").first.click(); pg.wait_for_timeout(900); ok(H.C().get("/api/avis").json["nb"] == 0, "avis refusé retiré du public")
    pg.get_by_role("button", name="Publier").first.click(); pg.wait_for_timeout(900); ok(H.C().get("/api/avis").json["nb"] == 1, "avis republié")
    pg.locator("#n-outils").click(); pg.wait_for_timeout(1200); t = pg.inner_text("#main")
    ok("4" in t and "pages vues sur 7 jours" in t and "/offre" in t and "sans cookie" in t, "visites : 4 pages vues, détail par page, mention sans cookie", t[:400])
    with pg.expect_download() as dl: pg.get_by_role("button", name="Télécharger la sauvegarde").click()
    path = dl.value.path(); data = J.load(open(path)); ok(dl.value.suggested_filename.startswith("sauvegarde-devanture-web-") and data["ok"] and len(data["tables"]["comptes"]) >= 6 and "dossier_fichiers" not in data["tables"], "sauvegarde téléchargée et lisible", dl.value.suggested_filename)
    ok("Sauvegarde téléchargée" in pg.inner_text("#main"), "confirmation affichée avec la date")
    with pg.expect_download() as dl2: pg.get_by_role("button", name="Avec les fichiers des clients").click()
    d2 = J.load(open(dl2.value.path())); ok(len(d2["tables"]["dossier_fichiers"]) == 1, "sauvegarde avec fichiers")
    ok("confidentiel" in pg.inner_text("#main"), "avertissement de confidentialité")

    print("=== E. ÉCRAN À TRAITER : TÂCHES GLOBALES ===")
    pg.locator("#n-today").click(); pg.wait_for_timeout(1200)
    pg.get_by_label("Titre de la tâche").fill("Acheter le nom de domaine devantureweb.fr"); pg.get_by_role("button", name="Ajouter", exact=True).click(); pg.wait_for_timeout(1200)
    ok("Acheter le nom de domaine" in pg.inner_text("#main"), "tâche générale ajoutée")
    pg.get_by_label("Marquer comme fait : Acheter le nom de domaine devantureweb.fr").first.check(); pg.wait_for_timeout(1200)
    ok(pg.locator("li.task.done", has_text="Acheter le nom de domaine").count() >= 1, "tâche cochée = barrée")
    ok("Relancer Paul" in pg.inner_text("#main"), "tâche liée à un client visible dans la liste globale")
    ok(clean() == [], "aucune erreur JS dans l'admin", clean())

    print("=== F. MOBILE ===")
    mctx = br.new_context(viewport={"width": 390, "height": 800}, locale="fr-FR", has_touch=True, is_mobile=True); mp = mctx.new_page(); mw = Watch(mp, ignore=["/api/moi"])
    login(mp, "admin@test.invalid", "AdminPass123"); mp.wait_for_timeout(1000)
    for k in ["#n-today", "#n-avis", "#n-outils", "#n-clients"]:
        mp.locator(k).click(); mp.wait_for_timeout(700)
        ok(mp.evaluate("document.documentElement.scrollWidth - window.innerWidth") <= 1, f"mobile 390px : pas de défilement horizontal ({k})", mp.evaluate("document.documentElement.scrollWidth - window.innerWidth"))
    mp.locator("#n-today").click(); mp.wait_for_timeout(500); mp.screenshot(path="a_mobile.png")
    pg.locator("#n-today").click(); pg.wait_for_timeout(800); pg.screenshot(path="a_today.png")
    br.close()
finish("e2e8_results.json")
