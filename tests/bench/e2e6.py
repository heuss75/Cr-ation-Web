import sys; from common import *
with sync_playwright() as p:
    br, ctx = launch(p); pg = ctx.new_page(); wt = Watch(pg, ignore=["/api/moi"])
    pg.goto(B + "/connexion"); pg.fill("#login [name=email]", "lea@salon.fr"); pg.fill("#login [name=password]", "MotDePasse1"); pg.click("#login button[type=submit]"); pg.wait_for_url("**/espace"); pg.wait_for_timeout(800)
    cid = sql("SELECT id FROM comptes WHERE email='lea@salon.fr'")["rows"][0]["id"]
    sql("UPDATE demandes SET site_url='/exemples/bistro' WHERE compte_id=?", cid)
    pg.goto(B + "/espace#resa"); pg.reload(); pg.wait_for_timeout(900); t = pg.inner_text("#main")
    ok("est sur votre site" in t and "pas ici" in t, "espace client: la réservation est présentée comme faisant partie du SITE du client", t[:200])
    ok(pg.locator("a[href='/exemples/bistro-reservation-interne']").count() == 1 and pg.locator("a[href='/exemples/bistro-reservation-client']").count() == 1, "espace client: liens vers planning/statistiques et page de réservation sur son site")
    ok("Aucune réservation pour le moment" not in t, "espace client: plus d'agenda de réservations hébergé ici")
    sql("UPDATE demandes SET site_url='/exemples/salon' WHERE compte_id=?", cid); pg.reload(); pg.wait_for_timeout(800); ok(pg.locator("a[href*='reservation']").count() == 0, "autre site d'exemple: pas de lien cassé")
    ok(not wt.take(), "aucune erreur", "")
    br.close()
finish(sys.argv[1])
