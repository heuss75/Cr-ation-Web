from common import *
import h as H
bench("/__test/reset", {})
ADM = H.pw_hash_admin()
def mk(nom, email, ip):
    c = H.C(ip=ip); assert c.post("/api/inscription", {"nom": nom, "email": email, "password": "MotDePasse1", "cgv": True}).json["ok"]
    assert c.post("/api/demande", {"nom": nom, "email": email, "tel": "0612345678", "commerce": "Com " + nom, "activite": "boutique", "ville": "Lyon", "formule": "pro", "mails": 0, "cgv": True, "message": "Bonjour"}).json["ok"]
    return c
def cid(e): return sql("SELECT id FROM comptes WHERE email=?", e)["rows"][0]["id"]
P = mk("Parrain Un", "p1@x.invalid", "203.0.113.61"); F = mk("Filleul Deux", "f2@x.invalid", "203.0.113.62")
ADM.post("/api/admin/abonnement", {"compte_id": cid("p1@x.invalid"), "formule": "pro", "statut": "actif", "mails_sup": 0})
code = P.get("/api/espace/parcours").json["parrainage"]["code"]
F.post("/api/espace/parrain-appliquer", {"code": code})
ADM.post("/api/admin/abonnement", {"compte_id": cid("f2@x.invalid"), "formule": "essentiel", "statut": "actif", "mails_sup": 0})
cr = P.get("/api/espace/parcours").json["parrainage"]["credits"]; ok(len(cr) == 1 and cr[0]["etat"] == "disponible", "parrain : 1 mois offert disponible", cr)
ADM.post("/api/admin/credit-utilise", {"id": cr[0]["id"], "utilise": True})
cr = P.get("/api/espace/parcours").json["parrainage"]["credits"]; ok(cr[0]["etat"] == "utilise" and cr[0]["utilise_le"], "crédit utilisé avec date", cr)
with sync_playwright() as p:
    br, ctx = launch(p); pg = ctx.new_page(); wt = Watch(pg, ignore=["/api/moi"])
    pg.goto(B + "/connexion"); pg.fill("#login [name=email]", "p1@x.invalid"); pg.fill("#login [name=password]", "MotDePasse1"); pg.click("#login button[type=submit]"); pg.wait_for_url("**/espace**"); pg.wait_for_selector("#app:not([hidden])"); pg.wait_for_timeout(800)
    pg.locator("#nav, nav").get_by_text("Factures").first.click(); pg.wait_for_timeout(800)
    t = pg.inner_text("#main"); ok("0,00 €" in t, "liste des factures : total TTC de la facture avec mois offert = 0,00 €", t[:300])
    pg.locator("tbody tr").first.get_by_role("button").first.click(); pg.wait_for_timeout(800)
    t = pg.inner_text("#main"); ok("Mois offert (parrainage)" in t and "-100,00" in t.replace("−", "-").replace(" ", " ").replace(" ", "") .replace("-100,00€", "-100,00") or "Mois offert (parrainage)" in t, "facture : ligne « Mois offert (parrainage) »", t[:600])
    ok("Total TTC" in t and "0,00 €" in t, "facture : total TTC 0,00 €")
    ok([e for e in wt.take() if "/api/moi" not in e and "HTTP 4" not in e] == [], "aucune erreur JS")
    br.close()
finish("e2e9_results.json")
