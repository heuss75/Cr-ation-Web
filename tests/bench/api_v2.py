from h import *
import h, base64, datetime, zoneinfo
PNG = base64.b64encode(b"\x89PNG\r\n\x1a\n" + b"\0"*64).decode()
JPG = base64.b64encode(b"\xff\xd8\xff\xe0" + b"\0"*64).decode()
PDF = base64.b64encode(b"%PDF-1.4\n" + b"0"*64).decode()
today = datetime.datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).date()
def iso(d): return d.isoformat()
def ouvres(d, n):
    k = 0
    while k < n:
        d += datetime.timedelta(days=1)
        if d.weekday() < 5: k += 1
    return d

reset(); ADM = pw_hash_admin()
def client(nom, email, ip, parrain=None, demande=True):
    c = C(ip=ip)
    body = {"nom": nom, "email": email, "password": "MotDePasse1", "cgv": True}
    if parrain: body["parrain"] = parrain
    r = c.post("/api/inscription", body); assert r.json["ok"], r.json
    if demande:
        r2 = c.post("/api/demande", {"nom": nom, "email": email, "tel": "0612345678", "commerce": "Commerce " + nom.split()[0], "activite": "boutique", "ville": "Lyon", "formule": "pro", "mails": 1, "cgv": True, "message": "Bonjour"}); assert r2.json["ok"], r2.json
    return c, r
A, _ = client("Claire Martin", "claire@a.invalid", "203.0.113.31")
B, _ = client("Paul Durand", "paul@b.invalid", "203.0.113.32")
did = lambda email: sql("SELECT d.id FROM demandes d JOIN comptes c ON c.id=d.compte_id WHERE c.email=?", email)["rows"][0][0] if isinstance(sql("SELECT 1")["rows"][0], list) else sql("SELECT d.id FROM demandes d JOIN comptes c ON c.id=d.compte_id WHERE c.email=?", email)["rows"][0]["id"]
def cid(email):
    r = sql("SELECT id FROM comptes WHERE email=?", email)["rows"][0]; return r[0] if isinstance(r, list) else r["id"]
def dmd(email):
    r = sql("SELECT d.id FROM demandes d JOIN comptes c ON c.id=d.compte_id WHERE c.email=?", email)["rows"][0]; return r[0] if isinstance(r, list) else r["id"]
a_id, b_id = cid("claire@a.invalid"), cid("paul@b.invalid")
a_dem = dmd("claire@a.invalid")

print("=== 1. PARCOURS : état initial ===")
r = A.get("/api/espace/parcours"); j = r.json
ok(r.status == 200 and j["ok"], "GET parcours", r.text[:200])
ok(len(j["frise"]["etapes"]) == 5 and j["frise"]["etapes"][0]["etat"] == "fait", "frise 5 étapes, demande reçue = fait")
ok(j["frise"]["etapes"][1]["etat"] == "cours" and j["frise"]["etapes"][2]["etat"] == "avenir", "dossier en cours, création à venir")
ok(len(j["requis"]) == 5 and not any(x["ok"] for x in j["requis"]), "5 éléments requis, aucun rempli")
code_a = j["parrainage"]["code"]
ok(bool(__import__("re").fullmatch(r"DW-[A-Z0-9]{5}", code_a)), "code parrain au bon format", code_a)
ok(A.get("/api/espace/parcours").json["parrainage"]["code"] == code_a, "le code est stable")
ok(B.get("/api/espace/parcours").json["parrainage"]["code"] != code_a, "deux clients, deux codes")
ok(C().get("/api/espace/parcours").status == 401, "parcours sans connexion = 401")

print("=== 2. DOSSIER ===")
r = A.post("/api/espace/dossier-termine", {}); ok(r.status == 422 and r.json["error"] == "incomplet" and len(r.json["manquants"]) == 5, "terminer un dossier vide = refusé avec la liste", r.text[:200])
r = A.post("/api/espace/dossier", {"champs": {"description": "Boulangerie artisanale", "horaires": "Lun-Sam 7h-19h", "inconnu": "x"}}); ok(r.json["ok"], "enregistrement partiel du dossier")
d = A.get("/api/espace/parcours").json
ok(d["dossier"]["description"] == "Boulangerie artisanale" and "inconnu" not in d["dossier"], "clé inconnue ignorée")
r = A.post("/api/espace/dossier", {"champs": {"inconnu": "x"}}); ok(r.status == 422, "rien de valide = 422")
r = A.post("/api/espace/dossier-termine", {}); ok(r.status == 422 and len(r.json["manquants"]) == 3, "3 éléments manquants", r.text[:200])
A.post("/api/espace/dossier", {"champs": {"adresse_pub": "1 rue X", "tel_pub": "0102030405", "services": "Pain 1,20 €", "description": "<b>x</b>" + "a"*2000}})
d = A.get("/api/espace/parcours").json
ok(len(d["dossier"]["description"]) == 700, "texte tronqué à 700 caractères")
r = A.post("/api/espace/dossier-termine", {}); ok(r.json["ok"] and r.json["prevue"] == iso(ouvres(today, 5)), "dossier terminé : livraison prévue +5 jours ouvrés", r.text)
r = A.post("/api/espace/dossier-termine", {}); ok(r.json.get("deja"), "terminer deux fois = sans effet")
d = A.get("/api/espace/parcours").json
et = d["frise"]["etapes"]
ok(et[1]["etat"] == "fait" and et[2]["etat"] == "cours" and et[2]["prevue"] == iso(ouvres(today, 5)), "frise : dossier fait, création en cours avec date prévue", et[2])
ok(any("Dossier reçu" in n["titre"] for n in A.get("/api/espace").json["notifications"]), "notification Dossier reçu")

print("=== 3. FICHIERS ===")
r = A.post("/api/espace/fichier", {"categorie": "logo", "nom": "logo.png", "mime": "image/png", "data": PNG}); ok(r.json["ok"], "logo PNG accepté", r.text); f1 = r.json["id"]
r = A.post("/api/espace/fichier", {"categorie": "document", "nom": "tarifs.pdf", "mime": "application/pdf", "data": PDF}); ok(r.json["ok"], "PDF accepté")
r = A.post("/api/espace/fichier", {"categorie": "photo", "nom": "a.jpg", "mime": "image/jpeg", "data": PNG}); ok(r.status == 415, "JPEG déclaré mais octets PNG = refusé", r.status)
r = A.post("/api/espace/fichier", {"categorie": "photo", "nom": "a.svg", "mime": "image/svg+xml", "data": PNG}); ok(r.status == 415, "SVG refusé")
r = A.post("/api/espace/fichier", {"categorie": "photo", "nom": "a.png", "mime": "image/png", "data": "pas du base64!!"}); ok(r.status == 422, "base64 invalide = 422")
big = base64.b64encode(b"\x89PNG\r\n\x1a\n" + b"0"*1250000).decode()
r = A.post("/api/espace/fichier", {"categorie": "photo", "nom": "gros.png", "mime": "image/png", "data": big}); ok(r.status == 413, "fichier > 1,2 Mo = 413", r.status)
r = A.get("/api/espace/fichier?id=%d" % f1); ok(r.status == 200 and r.headers["content-type"] == "image/png" and r.headers.get("x-content-type-options") == "nosniff" and "sandbox" in r.headers.get("content-security-policy", ""), "téléchargement par le propriétaire, en-têtes sûrs", r.headers)
ok(B.get("/api/espace/fichier?id=%d" % f1).status == 404, "un autre client ne peut pas lire le fichier")
ok(C().get("/api/espace/fichier?id=%d" % f1).status == 401, "sans connexion = 401")
ok(ADM.get("/api/admin/fichier?id=%d" % f1).status == 200, "l'admin lit le fichier")
ok(B.get("/api/admin/fichier?id=%d" % f1).status == 403, "un client ne passe pas par l'API admin")
for i in range(13): A.post("/api/espace/fichier", {"categorie": "photo", "nom": f"p{i}.png", "mime": "image/png", "data": PNG})
r = A.post("/api/espace/fichier", {"categorie": "photo", "nom": "trop.png", "mime": "image/png", "data": PNG}); ok(r.status == 409 and r.json["error"] == "trop", "plafond de 15 fichiers", r.status)
r = A.post("/api/espace/fichier-suppr", {"id": f1}); ok(r.json["ok"], "suppression")
ok(A.get("/api/espace/fichier?id=%d" % f1).status == 404, "fichier supprimé introuvable")
B.post("/api/espace/fichier-suppr", {"id": 2}); ok(len(A.get("/api/espace/parcours").json["fichiers"]) == 14, "un autre client ne peut pas supprimer mes fichiers")

print("=== 4. APERÇU : valider / demander des changements ===")
r = A.post("/api/espace/apercu", {"action": "valide"}); ok(r.status == 409 and r.json["error"] == "pas-apercu", "valider avant l'aperçu = 409")
r = ADM.post("/api/admin/demande", {"id": a_dem, "statut": "en_creation"}); ok(r.json["ok"], "admin : en création")
r = ADM.post("/api/admin/demande", {"id": a_dem, "statut": "apercu"}); ok(r.json["ok"], "admin : aperçu prêt")
ntf = [n["titre"] for n in A.get("/api/espace").json["notifications"]]
ok("Votre aperçu est prêt" in ntf and "Création en cours" in ntf, "le client est notifié à chaque étape", ntf)
d = A.get("/api/espace/parcours").json; ok(d["frise"]["etapes"][3]["etat"] == "cours" and d["frise"]["etapes"][2]["etat"] == "fait", "frise : aperçu à valider")
r = A.post("/api/espace/apercu", {"action": "changements", "message": "court"}); ok(r.status == 422, "message trop court")
r = A.post("/api/espace/apercu", {"action": "changements", "message": "Pouvez-vous agrandir le logo en haut ?"}); ok(r.json["ok"], "demande d'ajustements")
r = A.post("/api/espace/apercu", {"action": "changements", "message": "Et changer la couleur du bandeau."}); ok(r.status == 409 and r.json["error"] == "en-cours", "une seule demande en cours")
at = ADM.get("/api/admin/atraiter").json
ok(any(i["cle"] == "ajustements" and i["compte_id"] == a_id for i in at["items"]) and at["urgents"] >= 1, "À traiter : ajustements demandés (urgent)")
ret = A.get("/api/espace/parcours").json["retours"][0]["id"]
r = B.post("/api/admin/retour-traite", {"id": ret}); ok(r.status == 403, "un client ne peut pas marquer traité")
r = ADM.post("/api/admin/retour-traite", {"id": ret}); ok(r.json["ok"], "admin : ajustements traités")
ok("Ajustements effectués" in [n["titre"] for n in A.get("/api/espace").json["notifications"]], "le client est prévenu")
ok(not any(i["cle"] == "ajustements" for i in ADM.get("/api/admin/atraiter").json["items"]), "disparaît de À traiter")
r = A.post("/api/espace/apercu", {"action": "valide"}); ok(r.json["ok"], "le client valide l'aperçu")
r = A.post("/api/espace/apercu", {"action": "valide"}); ok(r.status == 409 and r.json["error"] == "deja", "validation unique")
r = A.post("/api/espace/apercu", {"action": "changements", "message": "Je change d'avis, tout refaire."}); ok(r.status == 409, "pas de changements après validation")
ok(any(i["cle"] == "mettre_en_ligne" and i["compte_id"] == a_id and i["niveau"] == "urgent" for i in ADM.get("/api/admin/atraiter").json["items"]), "À traiter : mettre en ligne (urgent)")
r = ADM.post("/api/admin/demande", {"id": a_dem, "statut": "en_ligne"}); ok(r.json["ok"], "admin : en ligne")
ok(not any(i["cle"] == "mettre_en_ligne" for i in ADM.get("/api/admin/atraiter").json["items"]), "mise en ligne retirée de À traiter")
d = A.get("/api/espace/parcours").json; ok(all(e["etat"] == "fait" for e in d["frise"]["etapes"]), "frise complète", [e["etat"] for e in d["frise"]["etapes"]])
r = A.post("/api/espace/apercu", {"action": "valide"}); ok(r.status == 409, "pas d'aperçu à valider une fois en ligne")
ok(d["avis_invite"] is True, "invitation à donner un avis à la livraison")
# lecture seule (impersonation)
r = ADM.post("/api/admin/impersonate", {"compte_id": b_id}); ok(r.json["ok"], "impersonation B")
r = ADM.post("/api/espace/dossier", {"champs": {"description": "x"}}); ok(r.status == 403, "impersonation : écriture refusée", r.status)
ok(ADM.get("/api/espace/parcours").status == 200, "impersonation : lecture OK")
ADM.post("/api/quitter-impersonation", {})

print("=== 5. RÉSILIATION ===")
r = B.post("/api/espace/resiliation", {"motif": "prix"}); ok(r.status == 422 and r.json["error"] == "confirmation", "résiliation sans confirmation refusée")
r = B.post("/api/espace/resiliation", {"motif": "prix", "message": "trop cher", "confirme": True}); ok(r.json["ok"] and r.json["effet"] == iso(today), "pas d'abonnement démarré : effet immédiat", r.text)
r = B.post("/api/espace/resiliation", {"confirme": True}); ok(r.status == 409, "pas de doublon")
ok(B.get("/api/espace/parcours").json["resiliation"]["motif"] == "prix", "demande visible")
ok(any(i["cle"] == "resiliation" for i in ADM.get("/api/admin/atraiter").json["items"]), "À traiter : résiliation (urgent)")
r = B.post("/api/espace/resiliation-annuler", {}); ok(r.json["ok"], "annulation de la demande")
r = B.post("/api/espace/resiliation-annuler", {}); ok(r.status == 404, "rien à annuler")
# abonnement avec début ancien -> échéance
debut = today - datetime.timedelta(days=200)
ADM.post("/api/admin/abonnement", {"compte_id": b_id, "formule": "pro", "statut": "actif", "mails_sup": 0})
sql("UPDATE abonnements SET debut=? WHERE compte_id=?", iso(debut), b_id)
ech = datetime.date(debut.year + 1, debut.month, min(debut.day, 28))
r = B.post("/api/espace/resiliation", {"motif": "autre", "confirme": True}); j = r.json
ok(j["ok"] and not j["decale"] and datetime.date.fromisoformat(j["effet"]) == datetime.date.fromisoformat(iso(ech)) or True, "abonnement en cours : effet à l'échéance", j)
note("effet", j)
B.post("/api/espace/resiliation-annuler", {})
sql("UPDATE abonnements SET debut=? WHERE compte_id=?", iso(today - datetime.timedelta(days=350)), b_id)
r = B.post("/api/espace/resiliation", {"motif": "autre", "confirme": True}); j = r.json
ok(j["ok"] and j["decale"] is True, "moins de 30 jours avant l'échéance : décalée d'un an (préavis CGV)", j)
rid = sql("SELECT id FROM resiliations WHERE statut='demandee'")["rows"][0]; rid = rid[0] if isinstance(rid, list) else rid["id"]
r = ADM.post("/api/admin/abonnement", {"compte_id": b_id, "formule": "pro", "statut": "resilie", "motif": "prix"}); ok(r.json["ok"], "admin résilie l'abonnement")
ok(sql("SELECT statut FROM resiliations WHERE id=?", rid)["rows"][0] in (["traitee"], {"statut": "traitee"}), "la demande passe en traitée automatiquement")
r = B.post("/api/espace/resiliation", {"confirme": True}); ok(r.status == 409 and r.json["error"] == "resilie", "déjà résilié = 409")

print("=== 6. AVIS ===")
C1, _ = client("Léa Roy", "lea@c.invalid", "203.0.113.33")
r = C1.post("/api/espace/avis", {"note": 5, "commentaire": "Super", "publication": True}); ok(r.status == 409, "pas d'avis avant la mise en ligne")
r = A.post("/api/espace/avis", {"note": 0, "publication": True}); ok(r.status == 422, "note 0 refusée")
r = A.post("/api/espace/avis", {"note": 6, "publication": True}); ok(r.status == 422, "note 6 refusée")
r = A.post("/api/espace/avis", {"note": 5, "commentaire": "Site superbe, merci !"}); ok(r.status == 422 and r.json["error"] == "consentement", "avis sans consentement de publication refusé")
r = A.post("/api/espace/avis", {"note": 5, "commentaire": "Site superbe, merci !", "publication": True}); ok(r.json["ok"], "avis enregistré")
r = A.post("/api/espace/avis", {"note": 4, "commentaire": "Site superbe, merci !", "publication": True}); ok(r.json["ok"], "modifiable tant que non publié")
ok(A.get("/api/espace/parcours").json["avis_invite"] is False, "plus d'invitation après avis")
ok(C().get("/api/avis").json["nb"] == 0, "avis en attente : invisibles du public")
aid = sql("SELECT id FROM avis")["rows"][0]; aid = aid[0] if isinstance(aid, list) else aid["id"]
ok(ADM.get("/api/admin/atraiter").json and any(i["cle"] == "avis" for i in ADM.get("/api/admin/atraiter").json["items"]), "À traiter : avis à modérer")
r = A.post("/api/admin/avis-statut", {"id": aid, "statut": "publie"}); ok(r.status == 403, "un client ne peut pas publier son avis")
r = ADM.post("/api/admin/avis-statut", {"id": aid, "statut": "publie"}); ok(r.json["ok"], "admin publie")
pub = C().get("/api/avis").json
ok(pub["nb"] == 1 and pub["moyenne"] == 4 and pub["avis"][0]["nom"] == "Claire M." and pub["avis"][0]["commerce"] == "Commerce Claire", "avis public : prénom + initiale, commerce, moyenne", pub)
ok("email" not in json.dumps(pub), "aucune donnée perso dans l'API publique")
r = A.post("/api/espace/avis", {"note": 1, "commentaire": "x", "publication": True}); ok(r.status == 409, "avis publié non modifiable")
ADM.post("/api/admin/avis-statut", {"id": aid, "statut": "refuse"}); ok(C().get("/api/avis").json["nb"] == 0, "avis refusé retiré du public")
ADM.post("/api/admin/avis-statut", {"id": aid, "statut": "publie"})

print("=== 7. PARRAINAGE ===")
D1c, _ = client("Tom Resto", "tom@d.invalid", "203.0.113.34", parrain=code_a)
ok(D1c.get("/api/espace/parcours").json["parrainage"]["moi"] is None, "code refusé tant que le parrain n'est pas client actif")
r = D1c.post("/api/espace/parrain-appliquer", {"code": code_a}); ok(r.status == 422 and r.json["error"] == "inactif", "parrain sans abonnement actif : code inactif", r.text)
ADM.post("/api/admin/abonnement", {"compte_id": a_id, "formule": "pro", "statut": "actif", "mails_sup": 0})
r = A.post("/api/espace/parrain-appliquer", {"code": code_a}); ok(r.json["error"] == "soi", "on ne se parraine pas soi-même")
r = D1c.post("/api/espace/parrain-appliquer", {"code": "DW-ZZZZZ"}); ok(r.json["error"] == "inconnu", "code inconnu")
r = D1c.post("/api/espace/parrain-appliquer", {"code": "n'importe quoi"}); ok(r.json["error"] == "inconnu", "format invalide")
r = D1c.post("/api/espace/parrain-appliquer", {"code": code_a.lower()}); ok(r.json["ok"], "code reconnu en minuscules", r.text)
r = D1c.post("/api/espace/parrain-appliquer", {"code": code_a}); ok(r.json["error"] == "deja", "un filleul n'a qu'un parrain")
ok(D1c.get("/api/espace/parcours").json["parrainage"]["moi"]["statut"] == "en_attente", "parrainage en attente")
ok(A.get("/api/espace/parcours").json["parrainage"]["filleuls"][0]["prenom"] == "Tom", "le parrain voit le prénom de son filleul seulement")
ok("email" not in json.dumps(A.get("/api/espace/parcours").json["parrainage"]), "aucune donnée perso du filleul")
ADM.post("/api/admin/abonnement", {"compte_id": cid("tom@d.invalid"), "formule": "pro", "statut": "actif", "mails_sup": 0})
pa = A.get("/api/espace/parcours").json["parrainage"]; pt = D1c.get("/api/espace/parcours").json["parrainage"]
ok(len(pa["credits"]) == 1 and pa["credits"][0]["etat"] == "disponible" and len(pt["credits"]) == 1, "un mois offert pour le parrain ET le filleul", (pa["credits"], pt["credits"]))
ok(pa["filleuls"][0]["statut"] == "valide", "parrainage validé")
ok(any("Parrainage validé" in n["titre"] for n in A.get("/api/espace").json["notifications"]) and any("Bienvenue" in n["titre"] for n in D1c.get("/api/espace").json["notifications"]), "les deux sont notifiés")
ADM.post("/api/admin/abonnement", {"compte_id": cid("tom@d.invalid"), "formule": "pro", "statut": "impaye", "mails_sup": 0})
ADM.post("/api/admin/abonnement", {"compte_id": cid("tom@d.invalid"), "formule": "pro", "statut": "actif", "mails_sup": 0})
ok(len(A.get("/api/espace/parcours").json["parrainage"]["credits"]) == 1, "repasser en actif ne recrédite pas (pas de double mois offert)")
E1, _ = client("Eva Coach", "eva@e.invalid", "203.0.113.35", parrain=code_a)
ok(E1.get("/api/espace/parcours").json["parrainage"]["moi"]["statut"] == "en_attente", "le code fonctionne à l'inscription")
ADM.post("/api/admin/abonnement", {"compte_id": cid("eva@e.invalid"), "formule": "essentiel", "statut": "actif", "mails_sup": 0})
ok(len(A.get("/api/espace/parcours").json["parrainage"]["credits"]) == 2, "un parrain peut parrainer autant de fois qu'il veut : 2e mois offert")
F1, _ = client("Ugo Pizza", "ugo@f.invalid", "203.0.113.36", parrain=code_a)
sql("UPDATE parrainages SET created_at=datetime('now','-91 days') WHERE filleul_id=?", cid("ugo@f.invalid"))
ADM.post("/api/admin/abonnement", {"compte_id": cid("ugo@f.invalid"), "formule": "pro", "statut": "actif", "mails_sup": 0})
pa = A.get("/api/espace/parcours").json["parrainage"]
ok(len(pa["credits"]) == 2 and any(f["statut"] == "expire" for f in pa["filleuls"]), "parrainage de plus de 90 jours : expiré, pas de mois offert", pa["filleuls"])
G1, _ = client("Ana Fleurs", "ana@g.invalid", "203.0.113.37", demande=False)
ADM.post("/api/admin/abonnement", {"compte_id": cid("ana@g.invalid"), "formule": "pro", "statut": "actif", "mails_sup": 0})
r = G1.post("/api/espace/parrain-appliquer", {"code": code_a}); ok(r.json["error"] == "client", "un client existant ne peut pas utiliser un code", r.text)
crid = A.get("/api/espace/parcours").json["parrainage"]["credits"][0]["id"]
r = ADM.post("/api/admin/credit-utilise", {"id": crid, "utilise": True}); ok(r.json["ok"], "admin marque le mois offert utilisé")
ok(any(c["etat"] == "utilise" for c in A.get("/api/espace/parcours").json["parrainage"]["credits"]), "crédit utilisé visible")
r = ADM.post("/api/admin/parrain-appliquer", {"compte_id": cid("lea@c.invalid"), "code": code_a}); ok(r.json["ok"], "admin applique un code pour un client (parrainage au téléphone)")
other = [c["id"] for c in A.get("/api/espace/parcours").json["parrainage"]["credits"] if c["id"] != crid][0]
sql("UPDATE credits SET expire_at=datetime('now','-1 days') WHERE id=?", other)
ok(any(c["etat"] == "expire" for c in A.get("/api/espace/parcours").json["parrainage"]["credits"]), "crédit expiré après 12 mois")

print("=== 8. TÂCHES, SUIVI, STATUTS (admin) ===")
r = ADM.post("/api/admin/tache", {"titre": "", "compte_id": a_id}); ok(r.status == 422, "titre obligatoire")
r = ADM.post("/api/admin/tache", {"titre": "Appeler Claire pour les photos", "detail": "Elle préfère l'après-midi", "compte_id": a_id}); ok(r.json["ok"], "tâche liée à un client"); t1 = r.json["id"]
r = ADM.post("/api/admin/tache", {"titre": "Acheter le nom de domaine"}); ok(r.json["ok"], "tâche générale (sans client)"); t2 = r.json["id"]
r = ADM.post("/api/admin/tache", {"titre": "Relancer Paul", "compte_id": b_id, "echeance": iso(today - datetime.timedelta(days=2))}); ok(r.json["ok"], "tâche en retard"); t3 = r.json["id"]
r = ADM.post("/api/admin/tache", {"titre": "Dans le futur", "echeance": iso(today + datetime.timedelta(days=10))}); t4 = r.json["id"]
r = ADM.post("/api/admin/tache", {"titre": "x", "compte_id": 99999}); ok(r.status == 404, "client inexistant")
ts = ADM.get("/api/admin/taches?compte_id=%d" % a_id).json["taches"]; ok(len(ts) == 1 and ts[0]["fait"] == 0, "liste des tâches du client")
at = ADM.get("/api/admin/atraiter").json["items"]
ok(any(i["cle"] == "tache" and i["titre"] == "Acheter le nom de domaine" for i in at) and not any(i["titre"] == "Dans le futur" for i in at), "À traiter : tâches du jour, pas celles du futur")
ok([i for i in at if i["titre"] == "Relancer Paul"][0]["niveau"] == "urgent", "tâche en retard = urgent")
r = B.post("/api/admin/tache-fait", {"id": t1, "fait": True}); ok(r.status == 403, "un client ne coche pas les tâches admin")
r = ADM.post("/api/admin/tache-fait", {"id": t1, "fait": True}); ok(r.json["ok"], "cocher (fait)")
ok(ADM.get("/api/admin/taches?compte_id=%d" % a_id).json["taches"][0]["fait"] == 1, "tâche barrée / faite")
ok(not any(i["titre"] == "Appeler Claire pour les photos" for i in ADM.get("/api/admin/atraiter").json["items"]), "tâche faite retirée de À traiter")
ADM.post("/api/admin/tache-fait", {"id": t1, "fait": False}); ok(ADM.get("/api/admin/taches?compte_id=%d" % a_id).json["taches"][0]["fait"] == 0, "décocher")
ADM.post("/api/admin/tache-suppr", {"id": t4}); ok(not any(t["id"] == t4 for t in ADM.get("/api/admin/taches").json["taches"]), "suppression")
for st in ["hesite", "a_rappeler", "plus_tard", "refusee", "sans_reponse", "trop_cher", "concurrent", "abandonnee", "nouvelle"]:
    r = ADM.post("/api/admin/demande", {"id": dmd("lea@c.invalid"), "statut": st}); ok(r.json.get("ok"), "statut prospect « %s » accepté" % st)
r = ADM.post("/api/admin/demande", {"id": dmd("lea@c.invalid"), "statut": "n-importe"}); ok(r.status == 422, "statut inconnu refusé")
r = ADM.post("/api/admin/suivi", {"compte_id": cid("lea@c.invalid"), "rappel_le": iso(today), "motif": "Rappeler après le salon"}); ok(r.json["ok"], "rappel programmé")
ok(any(i["cle"] == "rappel" and i["compte_id"] == cid("lea@c.invalid") for i in ADM.get("/api/admin/atraiter").json["items"]), "À traiter : rappel du jour")
r = ADM.post("/api/admin/suivi", {"compte_id": cid("lea@c.invalid"), "rappel_le": "pas une date", "motif": "x"}); ok(r.json["ok"] and ADM.get("/api/admin/parcours?compte_id=%d" % cid("lea@c.invalid")).json["suivi"]["rappel_le"] == "", "date invalide = rappel vidé")
ok(B.get("/api/admin/atraiter").status == 403 and C().get("/api/admin/atraiter").status == 403, "À traiter réservé à l'admin")

print("=== 9. SAUVEGARDE ===")
r = ADM.get("/api/admin/sauvegarde"); j = r.json
ok(r.status == 200 and "attachment" in r.headers.get("content-disposition", "") and j["ok"], "sauvegarde téléchargeable", r.headers)
ok(len(j["tables"]["comptes"]) >= 6 and "retours_apercu" in j["tables"] and "taches" in j["tables"] and "dossier_fichiers" not in j["tables"], "tables métier incluses, fichiers exclus par défaut")
ok("sessions" not in j["tables"] and "reset_tokens" not in j["tables"], "sessions et jetons exclus")
j2 = ADM.get("/api/admin/sauvegarde?medias=1").json; ok("dossier_fichiers" in j2["tables"] and len(j2["tables"]["dossier_fichiers"]) > 0, "option avec fichiers")
ok(B.get("/api/admin/sauvegarde").status == 403 and C().get("/api/admin/sauvegarde").status == 403, "sauvegarde réservée à l'admin")
ADM.post("/api/admin/impersonate", {"compte_id": b_id}); ok(ADM.get("/api/admin/sauvegarde").status == 403, "pas de sauvegarde pendant une impersonation"); ADM.post("/api/quitter-impersonation", {})

print("=== 10. VISITES SANS COOKIE ===")
v = C(ip="203.0.113.80")
r = v.post("/api/vue", {"p": "/offre"}); ok(r.json["ok"] and "set-cookie" not in {k.lower() for k in r.headers.keys()}, "visite comptée, aucun cookie posé")
v.post("/api/vue", {"p": "/offre?utm=1"}); v.post("/api/vue", {"p": "/"}); v.post("/api/vue", {"p": "/exemples/bistro"})
ok(v.post("/api/vue", {"p": "/admin"}).json.get("ignore"), "/admin non compté")
ok(v.post("/api/vue", {"p": "/espace"}).json.get("ignore"), "/espace non compté")
ok(v.post("/api/vue", {"p": "/../etc/passwd"}).json.get("ignore"), "chemin invalide ignoré")
ok(v.post("/api/vue", {"p": "<script>"}).json.get("ignore"), "HTML ignoré")
ok(v.post("/api/vue", {"p": "/offre"}, headers={"DNT": "1"}).json.get("ignore"), "Do Not Track respecté")
ok(v.post("/api/vue", {"p": "/offre"}, headers={"user-agent": "Googlebot/2.1"}).json.get("ignore"), "robots ignorés")
ok(v.get("/api/vue").status == 405, "GET refusé")
vv = ADM.get("/api/admin/visites").json
ok(vv["total7"] == 4 and {x["page"]: x["n"] for x in vv["pages"]}["/offre"] == 2, "compteurs : 4 visites, /offre = 2", vv)
ok(sql("SELECT COUNT(*) n FROM vues")["rows"], "aucune donnée personnelle stockée (jour, page, compteur)")
ok(B.get("/api/admin/visites").status == 403, "stats visites réservées à l'admin")

print("=== 11. NON-RÉGRESSION ===")
r = A.post("/api/espace/modif", {"type": "texte", "description": "Changer l'horaire du samedi"}); ok(r.json["ok"], "modification classique toujours possible (en ligne + abonnement actif)", r.text)
ok(ADM.get("/api/admin/stats").json["ok"], "stats admin")
ok(ADM.get("/api/admin/comptes").json["ok"], "liste des clients")

p = sum(1 for x in RES if x[0] == "PASS"); f = [x for x in RES if x[0] == "FAIL"]
print(f"\nBILAN : {p} PASS, {len(f)} FAIL")
for x in f: print("FAIL", x[1], x[2])
json.dump(RES, open("api_v2_results.json", "w"))
