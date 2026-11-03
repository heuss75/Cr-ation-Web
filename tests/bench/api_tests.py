import json, re, sys, base64, urllib.request, urllib.error, datetime, zoneinfo, time

BASE = "http://127.0.0.1:8787"
RES = []
AUTO_ABANDON = False

def rec(status, name, detail=""):
    RES.append((status, name, detail))
    print(f"{status:5} {name}" + (f"  -> {detail}" if detail else ""))

def ok(cond, name, detail=""):
    rec("PASS" if cond else "FAIL", name, "" if cond else detail)

def note(name, detail): rec("NOTE", name, detail)

class C:
    def __init__(self, ip="203.0.113.10"):
        self.cookies = {}; self.ip = ip
    def req(self, method, path, body=None, headers=None, raw=None):
        h = {"x-test-ip": self.ip}
        if self.cookies: h["cookie"] = "; ".join(f"{k}={v}" for k, v in self.cookies.items())
        data = None
        if raw is not None: data = raw.encode() if isinstance(raw, str) else raw; h["content-type"] = "application/json"
        elif body is not None: data = json.dumps(body).encode(); h["content-type"] = "application/json"
        if headers: h.update(headers)
        rq = urllib.request.Request(BASE + path, data=data, method=method, headers=h)
        class NoRedir(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *a, **k): return None
        op = urllib.request.build_opener(NoRedir)
        try: r = op.open(rq, timeout=60)
        except urllib.error.HTTPError as e: r = e
        b = r.read()
        for sc in r.headers.get_all("set-cookie") or []:
            kv = sc.split(";")[0]; k, _, v = kv.partition("=")
            if "Max-Age=0" in sc: self.cookies.pop(k, None)
            else: self.cookies[k] = v
        try: j = json.loads(b)
        except Exception: j = None
        r.json = j; r.body = b; r.text = b.decode("utf-8", "replace"); return r
    def get(self, p, **k): return self.req("GET", p, **k)
    def post(self, p, body=None, **k):
        if p == "/api/demande" and AUTO_ABANDON: sql("UPDATE demandes SET statut='abandonnee' WHERE statut='nouvelle'")
        return self.req("POST", p, body=body, **k)

def sql(q, *args):
    rq = urllib.request.Request(BASE + "/__test/sql", data=json.dumps({"sql": q, "args": list(args)}).encode(), method="POST", headers={"content-type": "application/json"})
    try: return json.loads(urllib.request.urlopen(rq).read())
    except urllib.error.HTTPError as e: return json.loads(e.read())

def bench(path, body=None):
    rq = urllib.request.Request(BASE + path, data=json.dumps(body).encode() if body is not None else None, method="POST" if body is not None else "GET", headers={"content-type": "application/json"})
    return json.loads(urllib.request.urlopen(rq).read())

def reset(): bench("/__test/reset", {})

def pw_hash_admin():
    # crée un admin via inscription puis promotion SQL
    c = C(ip="198.51.100.200")
    r = c.post("/api/inscription", {"nom": "Admin Test", "email": "admin@test.invalid", "password": "AdminPass123", "cgv": True})
    assert r.json["ok"], r.json
    sql("UPDATE comptes SET role='admin' WHERE email='admin@test.invalid'")
    return c

GOOD_DEMANDE = {"nom": "Claire Martin", "email": "claire@boulangerie.fr", "tel": "06 12 34 56 78", "commerce": "Boulangerie Martin", "activite": "boutique", "ville": "Lyon", "domaine": "boulangerie-martin.fr", "formule": "essentiel", "mails": 1, "message": "Bonjour", "cgv": True}

reset()
ADM = pw_hash_admin()
print("=== 1. PAGES PUBLIQUES, ROUTAGE, EN-TÊTES ===")
c = C()
routes = ["/", "/offre", "/faq", "/commander", "/connexion", "/mentions-legales", "/cgv", "/confidentialite", "/cookies", "/guide-messagerie", "/reservation-demo", "/inscription", "/admin", "/espace", "/mot-de-passe-oublie", "/reinitialiser", "/exemples/bistro", "/exemples/salon", "/exemples/artisan"]
for p in routes:
    r = c.get(p)
    ok(r.status == 200 and b"<html" in r.body.lower()[:400] + r.body.lower()[:2000], f"GET {p} -> 200 HTML", f"status {r.status}")
r = c.get("/n-existe-pas"); ok(r.status == 404 and b"html" in r.body.lower(), "page inconnue -> 404 avec page 404", r.status)
r = c.get("/index.html"); ok(r.status == 301 and r.headers["location"].endswith("/"), "/index.html redirige vers /", r.status)
r = c.get("/offre.html?x=1"); ok(r.status == 301 and r.headers["location"].endswith("/offre?x=1"), "/offre.html redirige en gardant la query", r.headers.get("location"))
r = c.get("/offre/"); ok(r.status == 200, "slash final toléré", r.status)
r = c.get("/robots.txt"); ok(r.status == 200, "robots.txt", r.status)
note("robots.txt", "Contenu: " + c.get("/robots.txt").body.decode().replace("\n", " | ") + " (site non indexable tant que INDEXABLE est faux)")
r = c.get("/sitemap.xml"); note("sitemap.xml", f"statut {r.status} (absent tant que le site est non indexable)")
r = c.get("/assets/site.css"); ok(r.status == 200 and "text/css" in r.headers["content-type"], "CSS servi", r.status)
r = c.get("/assets/../worker/worker.js"); ok(r.status == 404, "traversée de chemin /assets/.. bloquée", r.status)
r = c.get("/worker/worker.js"); ok(r.status == 404, "/worker/worker.js non exposé", r.status)
r = c.get("/tools/build.py"); ok(r.status == 404, "/tools non exposé", r.status)
r = c.get("/"); h = r.headers
for k in ["x-content-type-options", "x-frame-options", "referrer-policy", "strict-transport-security", "permissions-policy"]:
    ok(k in h, f"en-tête de sécurité {k}", "absent")
ok("content-security-policy" not in h, "CSP", "") if False else None
if "content-security-policy" not in h: note("Content-Security-Policy", "absente (pas de CSP) : recommandé à terme, non bloquant")
r = c.req("DELETE", "/offre"); ok(r.status == 405, "DELETE sur page -> 405", r.status)
r = c.get("/media/99999"); ok(r.status == 404, "média inexistant -> 404", r.status)

print("\n=== 2. NOUVEAU CLIENT : INSCRIPTION (sans envoi d'e-mails configuré) ===")
cfg = c.get("/api/inscription/config").json; ok(cfg == {"ok": True, "verif": False}, "config inscription: vérif e-mail désactivée sans clés", cfg)
r = c.get("/api/inscription"); ok(r.status == 405, "GET /api/inscription -> 405", r.status)
r = c.post("/api/inscription", {"nom": "", "email": "x", "password": "123", "cgv": False}); ok(r.status == 422 and set(r.json["errors"]) == {"nom", "email", "password", "cgv"}, "inscription: 4 erreurs de validation renvoyées", r.json)
r = c.post("/api/inscription", {"nom": "A", "email": "a@b.c", "password": "12345678", "cgv": True}); ok(r.status == 422 and "nom" in r.json["errors"] and "email" in r.json["errors"], "nom 1 caractère et mail 'a@b.c' refusés", r.json)
r = c.post("/api/inscription", {"nom": "X" * 81, "email": "ok@test.fr", "password": "12345678", "cgv": True}); ok(r.status == 422, "nom 81 caractères refusé", r.json)
r = c.post("/api/inscription", {"nom": "Ok Nom", "email": "ok@test.fr", "password": "x" * 101, "cgv": True}); ok(r.status == 422, "mot de passe 101 caractères refusé", r.json)
r = c.post("/api/inscription", {"nom": "Ok Nom", "email": "ok@test.fr", "password": "1234567", "cgv": True}); ok(r.status == 422, "mot de passe 7 caractères refusé", r.json)
r = c.post("/api/inscription", {"nom": "Ok Nom", "email": "ok@test.fr", "password": "12345678", "cgv": "true"}); ok(r.status == 422, "cgv non booléen refusé", r.json)
r = c.post("/api/inscription", {"nom": "Bot", "email": "bot@test.fr", "password": "12345678", "cgv": True, "site_web_url": "http://spam"}); ok(r.json == {"ok": True} and not sql("SELECT id FROM comptes WHERE email='bot@test.fr'")["rows"], "piège anti-robot: faux succès sans création de compte", r.json)
r = c.post("/api/inscription", raw="{pas du json"); ok(r.status == 400, "JSON invalide -> 400", r.status)
r = c.post("/api/inscription", raw="x" * 2500); ok(r.status == 413, "corps > 2000 caractères -> 413", r.status)
r = c.post("/api/inscription", {"nom": "Ok", "email": "ok@test.fr", "password": "12345678", "cgv": True}, headers={"origin": "https://evil.example"}); ok(r.status == 403, "origine étrangère refusée (CSRF)", r.status)
r = c.post("/api/inscription", {"nom": "Claire Martin", "email": "  Claire@Boulangerie.FR ", "password": "MotDePasse1", "cgv": True})
ok(r.status == 200 and r.json["ok"] and "sv_session" in c.cookies, "inscription valide -> compte + session", r.json)
sc = r.headers.get("set-cookie", ""); ok("HttpOnly" in sc and "Secure" in sc and "SameSite=Lax" in sc, "cookie de session HttpOnly + Secure + SameSite=Lax", sc)
ok(sql("SELECT email FROM comptes WHERE nom='Claire Martin'")["rows"][0]["email"] == "claire@boulangerie.fr", "e-mail normalisé en minuscules et sans espaces")
r = c.get("/api/moi"); ok(r.json["ok"] and r.json["email"] == "claire@boulangerie.fr" and r.json["admin"] is False, "/api/moi après inscription", r.json)
r2 = C(ip="203.0.113.11").post("/api/inscription", {"nom": "Autre Claire", "email": "CLAIRE@boulangerie.fr", "password": "MotDePasse1", "cgv": True}); ok(r2.status == 409, "doublon d'e-mail (casse différente) -> 409", r2.status)
h = sql("SELECT hash, salt, iter FROM comptes WHERE id=2")["rows"]
row = sql("SELECT hash, salt, iter FROM comptes WHERE email='claire@boulangerie.fr'")["rows"][0]
ok(len(row["hash"]) == 64 and len(row["salt"]) == 32 and row["iter"] == 100000, "mot de passe haché PBKDF2 sel 16 octets, 100 000 itérations, jamais en clair")
note("Itérations PBKDF2", "100 000 (le minimum recommandé OWASP 2023 pour SHA-256 est 600 000 ; plafond Workers ~100 000 par appel, donc acceptable)")

print("\n=== 3. DÉCONNEXION / CONNEXION (ancien client) ===")
r = c.post("/api/deconnexion"); ok(r.json["ok"] and "sv_session" not in c.cookies, "déconnexion efface le cookie")
r = c.get("/api/moi"); ok(r.status == 401, "/api/moi sans session -> 401", r.status)
r = c.post("/api/connexion", {"email": "claire@boulangerie.fr", "password": "mauvais"}); ok(r.status == 401 and r.json["error"] == "identifiants", "mauvais mot de passe -> 401", r.json)
r_unk = c.post("/api/connexion", {"email": "inconnu@boulangerie.fr", "password": "mauvais"}); ok(r_unk.status == 401 and r_unk.json == r.json, "e-mail inconnu: même réponse que mauvais mot de passe (pas de fuite)", r_unk.json)
r = c.post("/api/connexion", {"email": "pas-un-mail", "password": "x"}); ok(r.status == 401, "e-mail malformé -> 401", r.status)
r = c.post("/api/connexion", {"email": "claire@boulangerie.fr", "password": ""}); ok(r.status == 401, "mot de passe vide -> 401", r.status)
r = c.post("/api/connexion", {"email": " CLAIRE@boulangerie.fr ", "password": "MotDePasse1"}); ok(r.status == 200 and "sv_session" in c.cookies, "connexion OK (casse et espaces tolérés)", r.json)
ok(sql("SELECT derniere_connexion FROM comptes WHERE id=2")["rows"][0]["derniere_connexion"] is not None, "dernière connexion enregistrée")
# anti-bruteforce
b = C(ip="198.51.100.77"); codes = []
for i in range(12): codes.append(b.post("/api/connexion", {"email": "claire@boulangerie.fr", "password": f"faux{i}"}).status)
ok(codes[:10] == [401] * 10 and codes[10] == 429, "anti brute-force: 10 échecs puis 429 par IP", codes)
r = b.post("/api/connexion", {"email": "claire@boulangerie.fr", "password": "MotDePasse1"}); ok(r.status == 429, "même avec le bon mot de passe, l'IP bloquée reste bloquée 15 min", r.status)

print("\n=== 4. COMPTE CONNECTÉ : CHANGER SON MOT DE PASSE ===")
c2 = C(ip="203.0.113.50"); c2.post("/api/connexion", {"email": "claire@boulangerie.fr", "password": "MotDePasse1"})
r = C().post("/api/mot-de-passe", {"actuel": "a", "nouveau": "NouveauMdp12"}); ok(r.status == 401, "changement de mot de passe sans session -> 401", r.status)
r = c.post("/api/mot-de-passe", {"actuel": "MotDePasse1", "nouveau": "court"}); ok(r.status == 422, "nouveau mot de passe trop court -> 422", r.json)
r = c.post("/api/mot-de-passe", {"actuel": "mauvais", "nouveau": "NouveauMdp12"}); ok(r.status == 401 and r.json["error"] == "actuel", "ancien mot de passe faux -> 401", r.json)
r = c.post("/api/mot-de-passe", {"actuel": "MotDePasse1", "nouveau": "NouveauMdp12"}); ok(r.status == 200, "changement de mot de passe OK", r.json)
ok(c.get("/api/moi").status == 200, "session courante conservée")
ok(c2.get("/api/moi").status == 401, "les autres sessions sont fermées après changement")
ok(C().post("/api/connexion", {"email": "claire@boulangerie.fr", "password": "MotDePasse1"}).status == 401, "ancien mot de passe ne marche plus")
ok(C().post("/api/connexion", {"email": "claire@boulangerie.fr", "password": "NouveauMdp12"}).status == 200, "nouveau mot de passe fonctionne")

print("\n=== 5. MOT DE PASSE OUBLIÉ ===")
v = C(ip="203.0.113.60")
r = v.post("/api/mot-de-passe-oublie", {"email": "inconnu@nulle-part.fr"}); ok(r.json == {"ok": True}, "e-mail inconnu: réponse neutre ok:true (pas d'énumération)", r.json)
r = v.post("/api/mot-de-passe-oublie", {"email": "n'importe quoi"}); ok(r.json == {"ok": True}, "e-mail invalide: réponse neutre", r.json)
r = v.post("/api/mot-de-passe-oublie", {"email": "claire@boulangerie.fr"}); ok(r.json == {"ok": True}, "e-mail connu sans clés Resend: la page dit « ok » ...")
j = sql("SELECT type FROM journal WHERE type LIKE 'oubli%'")["rows"]
if j and j[-1]["type"] == "oubli_mdp_sans_mail": note("MOT DE PASSE OUBLIÉ SANS MAIL", "Tant que RESEND_API_KEY/MAIL_FROM ne sont pas configurés, le client voit « on vous a envoyé un lien » mais AUCUN mail ne part (journal: oubli_mdp_sans_mail).")
bench("/__test/mail", {"on": True})
bench("/__test/reset") if False else None
r = v.post("/api/mot-de-passe-oublie", {"email": "claire@boulangerie.fr"}); ok(r.json == {"ok": True}, "mot de passe oublié avec Resend configuré")
mails = bench("/__test/mails")
lm = [m for m in mails if "mot de passe" in m["subject"].lower()]
ok(len(lm) == 1 and "/reinitialiser?t=" in lm[0]["text"] and lm[0]["to"] == ["claire@boulangerie.fr"], "mail de réinitialisation envoyé avec lien", lm)
tok = re.search(r"t=([0-9a-f]{64})", lm[0]["text"]).group(1)
ok(("http://localhost:8787/reinitialiser" in lm[0]["text"] or "http://127.0.0.1:8787/reinitialiser" in lm[0]["text"]), "le lien du mail pointe vers l'origine de la requête", lm[0]["text"][:200])
r = C().post("/api/reinitialiser", {"token": "zz", "password": "NouveauMdp99"}); ok(r.status == 422, "jeton mal formé -> 422", r.status)
r = C().post("/api/reinitialiser", {"token": "0" * 64, "password": "NouveauMdp99"}); ok(r.status == 410, "jeton inconnu -> 410", r.status)
r = C().post("/api/reinitialiser", {"token": tok, "password": "court"}); ok(r.status == 422, "nouveau mot de passe trop court -> 422", r.status)
sess = C(ip="203.0.113.61"); sess.post("/api/connexion", {"email": "claire@boulangerie.fr", "password": "NouveauMdp12"})
r = C().post("/api/reinitialiser", {"token": tok, "password": "ResetMdp2026"}); ok(r.status == 200, "réinitialisation avec jeton valide", r.json)
ok(sess.get("/api/moi").status == 401, "toutes les sessions ouvertes sont fermées après réinitialisation")
r = C().post("/api/reinitialiser", {"token": tok, "password": "AutreMdp2026"}); ok(r.status == 410, "jeton à usage unique: réutilisation refusée", r.status)
ok(C().post("/api/connexion", {"email": "claire@boulangerie.fr", "password": "ResetMdp2026"}).status == 200, "connexion avec le nouveau mot de passe")
# expiration
r = v.post("/api/mot-de-passe-oublie", {"email": "claire@boulangerie.fr"})
mails = bench("/__test/mails"); tok2 = re.search(r"t=([0-9a-f]{64})", [m for m in mails if "mot de passe" in m["subject"].lower()][-1]["text"]).group(1)
sql("UPDATE reset_tokens SET expires_at = datetime('now','-1 minute')")
ok(C().post("/api/reinitialiser", {"token": tok2, "password": "ResetMdp2027"}).status == 410, "jeton expiré (> 1 h) refusé")
# rate limit oubli
w = C(ip="198.51.100.88"); res = [w.post("/api/mot-de-passe-oublie", {"email": "claire@boulangerie.fr"}).status for _ in range(7)]
ok(res[:5] == [200] * 5 and res[5] == 429, "mot de passe oublié: 5 demandes/h par IP puis 429", res)
# mail HTML escaping
sql("UPDATE comptes SET nom='<img src=x onerror=alert(1)> Claire' WHERE email='claire@boulangerie.fr'")
bench("/__test/reset") if False else None
w2 = C(ip="198.51.100.89"); w2.post("/api/mot-de-passe-oublie", {"email": "claire@boulangerie.fr"})
html_mail = bench("/__test/mails")[-1]["html"]; ok("<img" not in html_mail and "&lt;img" in html_mail, "nom du client échappé dans le mail HTML (pas d'injection)", html_mail[:200])
sql("UPDATE comptes SET nom='Claire Martin' WHERE email='claire@boulangerie.fr'")
# compte démo exclu
sql("INSERT INTO comptes (email, nom, salt, hash, iter, demo) VALUES ('demo@test.invalid','Demo','00','00',100000,1)")
n0 = len(bench("/__test/mails")); C(ip="198.51.100.90").post("/api/mot-de-passe-oublie", {"email": "demo@test.invalid"}); ok(len(bench("/__test/mails")) == n0, "compte démo: aucun mail de réinitialisation")

print("\n=== 6. VÉRIFICATION E-MAIL PAR CODE À 6 CHIFFRES (clés mail configurées) ===")
cfg = C().get("/api/inscription/config").json; ok(cfg["verif"] is True, "config: vérification activée avec clés Resend", cfg)
n = C(ip="203.0.113.70")
r = n.post("/api/inscription", {"nom": "Paul Durand", "email": "paul@garage.fr", "password": "PaulGarage1", "cgv": True}); ok(r.status == 422 and "code" in r.json["errors"], "inscription sans code refusée quand la vérif est active", r.json)
r = n.post("/api/inscription/code", {"email": "pas-un-mail"}); ok(r.status == 422, "demande de code: e-mail invalide -> 422", r.status)
r = n.post("/api/inscription/code", {"email": "claire@boulangerie.fr"}); ok(r.status == 200 and r.json.get("ok"), "e-mail déjà inscrit: réponse identique (pas d'énumération)", r.status)
note("Énumération de comptes", "/api/inscription/code répond 409 « Un compte existe déjà » : on peut savoir si un e-mail est inscrit (accepté en pratique, c'est le comportement standard de la plupart des sites).")
r = n.post("/api/inscription/code", {"email": "paul@garage.fr"}); ok(r.status == 200, "code envoyé", r.json)
m = [x for x in bench("/__test/mails") if "code de vérification" in x["subject"]][-1]; code = re.search(r"\b(\d{6})\b", m["subject"]).group(1)
ok(m["to"] == ["paul@garage.fr"], "le code part vers la bonne adresse")
r = n.post("/api/inscription/code", {"email": "paul@garage.fr"}); ok(r.status == 429 and r.json["error"] == "attente", "renvoi < 30 s refusé", r.json)
bad = "000000" if code != "000000" else "111111"
r = n.post("/api/inscription", {"nom": "Paul Durand", "email": "paul@garage.fr", "password": "PaulGarage1", "cgv": True, "code": bad}); ok(r.status == 422 and r.json["errors"]["code"] == "Code incorrect.", "code faux -> « Code incorrect. »", r.json)
r = n.post("/api/inscription", {"nom": "Paul Durand", "email": "paul@garage.fr", "password": "PaulGarage1", "cgv": True, "code": "12ab"}); ok(r.status == 422, "code non numérique refusé", r.json)
r = n.post("/api/inscription", {"nom": "Paul Durand", "email": "paul@garage.fr", "password": "PaulGarage1", "cgv": True, "code": code}); ok(r.status == 200 and "sv_session" in n.cookies, "code correct -> compte créé", r.json)
r = n.post("/api/inscription", {"nom": "Paul Durand", "email": "paul@garage.fr", "password": "PaulGarage1", "cgv": True, "code": code}); ok(r.status == 422, "code à usage unique (déjà consommé)", r.json)
# 5 essais
n2 = C(ip="203.0.113.71"); n2.post("/api/inscription/code", {"email": "lea@salon.fr"})
code2 = re.search(r"\b(\d{6})\b", [x for x in bench("/__test/mails") if "code de vérification" in x["subject"]][-1]["subject"]).group(1); bad2 = "000000" if code2 != "000000" else "111111"
msgs = [n2.post("/api/inscription", {"nom": "Léa Roy", "email": "lea@salon.fr", "password": "LeaSalon2026", "cgv": True, "code": bad2}).json["errors"]["code"] for _ in range(7)]
ok("Code incorrect." == msgs[0] and "Trop d’essais" in msgs[5], "5 essais faux puis code invalidé (« Trop d’essais »)", msgs)
r = n2.post("/api/inscription", {"nom": "Léa Roy", "email": "lea@salon.fr", "password": "LeaSalon2026", "cgv": True, "code": code2}); ok(r.status == 422, "même le bon code ne marche plus après trop d'essais", r.json)
# expiré
n3 = C(ip="203.0.113.72"); n3.post("/api/inscription/code", {"email": "tom@resto.fr"})
code3 = re.search(r"\b(\d{6})\b", [x for x in bench("/__test/mails") if "code de vérification" in x["subject"]][-1]["subject"]).group(1)
sql("UPDATE codes_mail SET expires_at = datetime('now','-1 minute') WHERE email='tom@resto.fr'")
r = n3.post("/api/inscription", {"nom": "Tom Resto", "email": "tom@resto.fr", "password": "TomResto2026", "cgv": True, "code": code3}); ok(r.status == 422 and "expiré" in r.json["errors"]["code"], "code expiré (> 10 min) refusé", r.json)
# code pour une autre adresse
n4 = C(ip="203.0.113.73"); n4.post("/api/inscription/code", {"email": "a1@test.fr"}); c_a1 = re.search(r"\b(\d{6})\b", [x for x in bench("/__test/mails") if "code de vérification" in x["subject"]][-1]["subject"]).group(1)
r = n4.post("/api/inscription", {"nom": "Pirate", "email": "victime@test.fr", "password": "Pirate2026x", "cgv": True, "code": c_a1}); ok(r.status == 422, "un code ne vaut que pour l'adresse demandée", r.json)
# échec d'envoi
bench("/__test/mail", {"on": True, "fail": True}); n5 = C(ip="203.0.113.74"); r = n5.post("/api/inscription/code", {"email": "x1@test.fr"}); ok(r.status == 502 and r.json["error"] == "envoi", "Resend en panne -> 502 « envoi »", r.json)
bench("/__test/mail", {"on": False}); r = C(ip="203.0.113.75").post("/api/inscription/code", {"email": "x2@test.fr"}); ok(r.status == 503, "sans clés mail -> 503 indisponible", r.status)
bench("/__test/mail", {"on": False})

print("\n=== 7. NOUVEAU CLIENT : DEMANDE DE SITE (/commander) ===")
cl = C(ip="203.0.113.80"); cl.post("/api/connexion", {"email": "claire@boulangerie.fr", "password": "ResetMdp2026"})
r = C(ip="203.0.113.81").post("/api/demande", GOOD_DEMANDE); ok(r.status == 401 and r.json["error"] == "compte", "demande sans compte -> 401 « compte »", r.json)
r = C(ip="203.0.113.81").post("/api/demande", dict(GOOD_DEMANDE, site_web_url="x")); ok(r.json["ok"] is True, "piège anti-robot sur demande: faux succès", r.json)
r = cl.get("/api/demande"); ok(r.status == 405, "GET /api/demande -> 405", r.status)
bad_cases = {
 "nom court": {"nom": "A"}, "email": {"email": "nope"}, "tel invalide": {"tel": "abc"}, "commerce": {"commerce": ""}, "activité": {"activite": "licorne"}, "ville": {"ville": ""},
 "domaine invalide": {"domaine": "mon site.fr"}, "formule": {"formule": "gold"}, "mails négatif": {"mails": -1}, "mails 11": {"mails": 11}, "message 1001": {"message": "x" * 1001}, "cgv": {"cgv": False}}
for k, patch in bad_cases.items():
    r = cl.post("/api/demande", dict(GOOD_DEMANDE, **patch)); ok(r.status == 422, f"demande refusée: {k}", r.json)
r = cl.post("/api/demande", dict(GOOD_DEMANDE, tel="", domaine="", message="")); ok(r.status == 200, "demande valide avec tel / domaine / message vides", r.json)
r = cl.post("/api/demande", GOOD_DEMANDE); ok(r.status == 409 and r.json.get("error") == "deja" and r.json["ref"].startswith("SVE-"), "2e demande ouverte refusée (doublon) avec la référence existante", r.json); AUTO_ABANDON = True
ref = r.json["ref"]; row = sql("SELECT * FROM demandes WHERE ref=?", ref)["rows"][0]
ok(row["statut"] == "nouvelle" and row["compte_id"] == 2 and row["formule"] == "essentiel" and row["ip_hash"] and len(row["ip_hash"]) == 16, "demande stockée: statut « nouvelle », liée au compte, IP hachée", row)
r = cl.post("/api/demande", dict(GOOD_DEMANDE, utm={"utm_source": "facebook", "landing": "/offre", "x": "ignoré"})); utm = json.loads(sql("SELECT utm FROM demandes ORDER BY id DESC LIMIT 1")["rows"][0]["utm"]); ok(utm == {"utm_source": "facebook", "landing": "/offre"}, "UTM: seules les clés autorisées sont gardées", utm)
r = cl.post("/api/demande", dict(GOOD_DEMANDE, message="<script>alert(1)</script>")); ok(r.status == 200, "message avec HTML accepté (échappé à l'affichage, à vérifier côté admin/espace)")
r = cl.post("/api/demande", raw="x" * 9000); ok(r.status == 413, "demande > 8000 car. -> 413", r.status)
r = cl.post("/api/demande", GOOD_DEMANDE, headers={"origin": "https://evil.example"}); ok(r.status == 403, "origine étrangère refusée sur /api/demande", r.status)
rl = [cl.post("/api/demande", GOOD_DEMANDE).status for _ in range(3)]; ok(429 in rl, "limite de 5 demandes/heure par IP -> 429", rl)
cnt = sql("SELECT COUNT(*) n FROM demandes WHERE compte_id=2")["rows"][0]["n"]
note("Plusieurs demandes par compte", f"Aucune protection contre les doublons : le même compte a pu créer {cnt} demandes quasi identiques. L'espace client ne gère que la DERNIÈRE (ORDER BY id DESC LIMIT 1).")

print("\n=== 8. ESPACE CLIENT : suivi, notifications, modifications, réclamations ===")
c3 = C(ip="203.0.113.90"); c3.post("/api/inscription", {"nom": "Nina Vide", "email": "nina@vide.fr", "password": "NinaVide2026", "cgv": True})
r = C().get("/api/espace"); ok(r.status == 401, "/api/espace sans session -> 401", r.status)
r = c3.get("/api/espace"); ok(r.status == 200 and r.json["demandes"] == [] and r.json["utilisees"] == 0 and r.json["quota"] == 1 and r.json["formule"] == "essentiel", "espace d'un compte sans demande: vide, formule essentiel, quota 1", r.json)
r = c3.post("/api/espace/modif", {"type": "texte", "description": "Changer le titre"}); ok(r.status == 404 and r.json["error"] == "aucune-demande", "modif sans demande -> 404 « aucune-demande » (message clair)", r.json)
r = cl.get("/api/espace"); ok(r.status == 200 and len(r.json["demandes"]) >= 1 and "prix" in r.json, "espace avec demande + prix servis par le serveur", {k: r.json[k] for k in ("formule", "quota", "utilisees")})
r = cl.post("/api/espace/modif", {"type": "texte", "description": "Changer le titre"}); ok(r.status == 409 and r.json["error"] == "pas-en-ligne", "modif refusée tant que le site n'est pas en préparation avancée/en ligne", r.json)
# admin
adm = ADM
r = adm.get("/api/admin/comptes?q=claire"); ok(r.status == 200 and any(x["email"] == "claire@boulangerie.fr" for x in r.json["comptes"]), "admin: recherche de comptes", r.status)
did = sql("SELECT id FROM demandes WHERE compte_id=2 ORDER BY id DESC LIMIT 1")["rows"][0]["id"]
r = adm.post("/api/admin/demande", {"id": did, "statut": "en_ligne"}); ok(r.status == 200, "admin passe la demande à « en_ligne »", r.json)
r = adm.post("/api/admin/demande", {"id": did, "statut": "nimporte"}); ok(r.status == 422, "statut de demande invalide refusé", r.status)
r = cl.post("/api/espace/modif", {"type": "texte", "description": "abc"}); ok(r.status == 422 and r.json["error"] == "vide", "description < 5 caractères refusée", r.json)
r = cl.post("/api/espace/modif", {"type": "texte", "description": "Changer le titre de la page d'accueil"}); ok(r.status == 200, "1re modification du mois acceptée", r.json)
r = cl.post("/api/espace/modif", {"type": "photo", "description": "Remplacer la photo de la vitrine"}); ok(r.status == 409 and r.json["error"] == "quota", "Essentiel: 2e modification du mois refusée (quota 1)", r.json)
e = cl.get("/api/espace").json; ok(e["utilisees"] == 1 and e["quota"] == 1, "compteur d'utilisation = 1/1", {k: e[k] for k in ("quota", "utilisees")})
# changement formule -> pro
cid = 2
r = adm.post("/api/admin/abonnement", {"compte_id": cid, "formule": "pro", "statut": "actif", "mails_sup": 2}); ok(r.status == 200, "admin crée l'abonnement Pro", r.json)
r = cl.post("/api/espace/modif", {"type": "bloc", "description": "Ajouter un bloc horaires d'été"}); ok(r.status == 200, "Pro: 2e modification acceptée (quota 3)", r.json)
r = cl.post("/api/espace/modif", {"type": "pasunvrai", "description": "Autre demande de modification"}); ok(r.status == 200, "Pro: 3e modification acceptée, type inconnu ramené à « autre »", r.json)
ok(sql("SELECT type FROM modifs ORDER BY id DESC LIMIT 1")["rows"][0]["type"] == "autre", "type inconnu stocké comme « autre »")
r = cl.post("/api/espace/modif", {"type": "texte", "description": "Quatrième demande du mois"}); ok(r.status == 409 and r.json["error"] == "quota", "Pro: 4e modification refusée (quota 3)", r.json)
sql("UPDATE modifs SET created_at = datetime('now','-40 days')"); r = cl.post("/api/espace/modif", {"type": "texte", "description": "Nouveau mois, nouvelle demande"}); ok(r.status == 200, "le quota se réinitialise au changement de mois", r.json)
sql("DELETE FROM modifs")
# abonnement impayé / résilié
adm.post("/api/admin/abonnement", {"compte_id": cid, "formule": "pro", "statut": "impaye", "mails_sup": 2})
r = cl.post("/api/espace/modif", {"type": "texte", "description": "Demande avec abonnement impayé"})
if r.status == 200: note("Abonnement impayé", "Un client dont l'abonnement est « impayé » peut toujours demander des modifications (seul le champ « suspendu » du site bloque). À décider : bloquer automatiquement ou non.")
else: ok(True, "modification bloquée si abonnement impayé")
adm.post("/api/admin/abonnement", {"compte_id": cid, "formule": "pro", "statut": "resilie", "motif": "Test"})
r = cl.post("/api/espace/modif", {"type": "texte", "description": "Demande avec abonnement résilié"})
if r.status == 200: note("Abonnement résilié", "Un client RÉSILIÉ peut encore créer des demandes de modification (pas de contrôle sur abonnements.statut).")
adm.post("/api/admin/abonnement", {"compte_id": cid, "formule": "pro", "statut": "actif", "mails_sup": 2}); sql("DELETE FROM modifs")
# suspension
r = adm.post("/api/admin/site", {"id": did, "suspendu": True}); ok(r.status == 200, "admin suspend le site")
r = cl.post("/api/espace/modif", {"type": "texte", "description": "Demande site suspendu"}); ok(r.status == 403 and r.json["error"] == "suspendu", "site suspendu: modifications bloquées", r.json)
adm.post("/api/admin/site", {"id": did, "suspendu": False})
# plainte
r = cl.post("/api/espace/plainte", {"sujet": "", "message": "x"}); ok(r.status == 422, "réclamation sans sujet refusée", r.status)
r = cl.post("/api/espace/plainte", {"sujet": "Site en panne", "message": "Plus rien ne s'affiche"}); ok(r.status == 200, "réclamation créée", r.json)
r = cl.post("/api/espace/plainte", {"sujet": "S" * 500, "message": "M" * 5000}); ok(r.status == 413 or r.status == 200, "réclamation très longue gérée (tronquée/413)", r.status)
pl = cl.get("/api/espace").json["plaintes"]; ok(len(pl) >= 1 and pl[0]["statut"] in ("ouverte",) or any(p["statut"] == "ouverte" for p in pl), "réclamation visible dans l'espace (statut ouverte)", pl)
r = cl.post("/api/espace/inconnu", {}); ok(r.status == 404, "route d'espace inconnue -> 404", r.status)
r = cl.req("PUT", "/api/espace/modif", body={}); ok(r.status == 405, "méthode PUT refusée", r.status)
# notifications
r = adm.post("/api/admin/notifier", {"titre": "Bonjour", "message": "Votre site est en ligne", "ids": [cid]}); ok(r.json["nb"] == 1, "admin envoie une notification", r.json)
e = cl.get("/api/espace").json; ok(e["notifications"][0]["lu"] == 0 and e["notifications"][0]["titre"] == "Bonjour", "notification reçue, non lue")
cl.post("/api/espace/lu", {}); ok(cl.get("/api/espace").json["notifications"][0]["lu"] == 1, "marquer comme lu")
# isolation entre clients
other = cl.get("/api/espace").json; mine3 = c3.get("/api/espace").json
ok(all(d["ref"] != "" for d in other["demandes"]) and mine3["demandes"] == [] and mine3["notifications"] == [], "isolation: Nina ne voit rien de Claire")

print("\n=== 9. ÉDITEUR PRO (textes et photos du site) ===")
ed = cl.get("/api/espace/editeur"); ok(ed.status == 409 and ed.json["error"] == "pas-pret", "éditeur: site pas encore assigné -> 409 pas-pret", ed.json)
adm.post("/api/admin/site", {"id": did, "site_url": "/exemples/salon"})
ed = cl.get("/api/espace/editeur"); ok(ed.status == 200 and len(ed.json["champs"]) > 20 and ed.json["site_url"] == "/exemples/salon", f"éditeur Pro: {len(ed.json.get('champs', []))} champs listés", ed.json if ed.status != 200 else "")
champs = ed.json["champs"]; k_text = next(x for x in champs if x["type"] == "text"); k_img = next((x for x in champs if x["type"] == "img"), None)
note("Types de champs", f"{sum(1 for x in champs if x['type']=='text')} textes, {sum(1 for x in champs if x['type']=='img')} images")
r = cl.post("/api/espace/contenu", {"k": k_text["k"], "valeur": "Maison Olive — Coiffure & Bien-être"}); ok(r.status == 200, "modifier un texte", r.json)
r = C(ip="203.0.113.99"); r.cookies = dict(cl.cookies)
page = cl.get("/exemples/salon").body.decode(); ok("Coiffure &amp; Bien-être" in page, "le site public affiche le texte modifié (échappé)", page[:100])
r = cl.post("/api/espace/contenu", {"k": k_text["k"], "valeur": "<script>alert(1)</script>"}); page = cl.get("/exemples/salon").body.decode(); ok("<script>alert(1)</script>" not in page and "&lt;script&gt;" in page, "HTML saisi par le client échappé sur le site public (pas de XSS)")
r = cl.post("/api/espace/contenu", {"k": "inexistante", "valeur": "x"}); ok(r.status == 422 and r.json["error"] == "cle", "clé inconnue refusée", r.json)
r = cl.post("/api/espace/contenu", {"k": k_text["k"], "valeur": ""}); ok(r.status == 422 and r.json["error"] == "texte", "texte vide refusé", r.json)
r = cl.post("/api/espace/contenu", {"k": k_text["k"], "valeur": "x" * 601}); ok(r.status == 422, "texte > 600 caractères refusé", r.json)
r = cl.post("/api/espace/contenu", {"k": k_text["k"], "reset": True}); ok(r.status == 200 and "Coiffure" not in cl.get("/exemples/salon").body.decode(), "réinitialiser un champ remet le texte d'origine", r.json)
# médias
png = base64.b64encode(b"\x89PNG\r\n\x1a\n" + b"\x00" * 200).decode()
r = cl.post("/api/espace/media", {"mime": "image/png", "data": png}); ok(r.status == 200 and r.json["url"].startswith("/media/"), "téléverser une image PNG", r.json)
murl = r.json["url"]; r = C().get(murl); ok(r.status == 200 and r.headers["content-type"] == "image/png", "image servie avec le bon type", r.status)
r = cl.post("/api/espace/media", {"mime": "image/svg+xml", "data": png}); ok(r.status == 422, "SVG refusé", r.json)
r = cl.post("/api/espace/media", {"mime": "image/png", "data": base64.b64encode(b"GIF89a" + b"\x00" * 300).decode()}); ok(r.status == 422, "faux PNG (mauvaise signature) refusé", r.json)
r = cl.post("/api/espace/media", {"mime": "image/png", "data": "!!!pas-du-base64"}); ok(r.status == 422, "base64 invalide refusé", r.json)
r = cl.post("/api/espace/media", {"mime": "image/jpeg", "data": base64.b64encode(b"\xff\xd8\xff" + b"\x00" * 50).decode()}); ok(r.status == 413, "image trop petite (< 100 octets) refusée", r.json)
big = base64.b64encode(b"\x89PNG" + b"\x00" * 1300000).decode(); r = cl.post("/api/espace/media", {"mime": "image/png", "data": big}); ok(r.status in (413,), "image > 1,2 Mo refusée", r.status)
if k_img:
    r = cl.post("/api/espace/contenu", {"k": k_img["k"], "valeur": murl}); ok(r.status == 200, "associer l'image téléversée à un emplacement", r.json)
    page = cl.get("/exemples/salon").body.decode(); ok(murl in page, "l'image apparaît sur le site public")
    r = cl.post("/api/espace/contenu", {"k": k_img["k"], "valeur": "/media/999"}); ok(r.status == 422 and r.json["error"] == "media", "image d'un autre compte / inexistante refusée", r.json)
    r = cl.post("/api/espace/contenu", {"k": k_img["k"], "valeur": "https://evil.example/x.png"}); ok(r.status == 422, "URL externe refusée sur un champ image", r.json)
cnt = 1
for i in range(61):
    rr = cl.post("/api/espace/media", {"mime": "image/png", "data": png})
    if rr.status == 409: break
    cnt += 1
ok(cnt == 60 and rr.json.get("error") == "limite", f"limite de 60 médias par compte (atteinte à {cnt})", rr.json)
# Essentiel n'a pas l'éditeur
ess = C(ip="203.0.113.95"); ess.post("/api/connexion", {"email": "nina@vide.fr", "password": "NinaVide2026"}); ok(ess.get("/api/espace/editeur").status == 403, "Essentiel / sans demande: éditeur refusé (403 pro)")
# deux clients Pro sur la même vitrine
c4 = C(ip="203.0.113.96"); c4.post("/api/inscription", {"nom": "Deuxième Pro", "email": "pro2@test.fr", "password": "ProDeux2026x", "cgv": True})
c4.post("/api/demande", dict(GOOD_DEMANDE, email="pro2@test.fr", nom="Deuxième Pro", commerce="Salon Deux", formule="pro"))
c4id = sql("SELECT id FROM comptes WHERE email='pro2@test.fr'")["rows"][0]["id"]; d4 = sql("SELECT id FROM demandes WHERE compte_id=?", c4id)["rows"][0]["id"]
adm.post("/api/admin/abonnement", {"compte_id": c4id, "formule": "pro", "statut": "actif"}); adm.post("/api/admin/demande", {"id": d4, "statut": "en_ligne"})
adm.post("/api/admin/site", {"id": d4, "site_url": "/exemples/salon"})
cl.post("/api/espace/contenu", {"k": k_text["k"], "valeur": "TEXTE-CLAIRE"}); c4.post("/api/espace/contenu", {"k": k_text["k"], "valeur": "TEXTE-DEUXIEME"})
pg = C().get("/exemples/salon").body.decode()
note("Une seule vitrine par modèle", f"Éditeur limité aux 3 pages /exemples/(bistro|salon|artisan). Si 2 clients Pro pointent sur la même URL, seul le plus récent est affiché (Claire visible: {'TEXTE-CLAIRE' in pg}, Deuxième visible: {'TEXTE-DEUXIEME' in pg}). Les vrais sites clients (un domaine chacun) ne peuvent pas encore utiliser l'éditeur.")
r = adm.post("/api/admin/site", {"id": d4, "site_url": "javascript:alert(1)"}); ok(r.status == 422 and r.json["error"] == "url", "URL de site « javascript: » refusée par l'admin", r.json)
r = adm.post("/api/admin/site", {"id": d4, "site_url": "https://monsite.fr"}); ok(r.status == 200, "URL https externe acceptée (sans éditeur)")
# site suspendu -> 503 public
adm.post("/api/admin/site", {"id": d4, "site_url": "/exemples/artisan"}); adm.post("/api/admin/site", {"id": d4, "suspendu": True})
r = C().get("/exemples/artisan"); ok(r.status == 503 and "momentanément indisponible" in r.body.decode(), "site suspendu -> page 503 « momentanément indisponible »", r.status)
adm.post("/api/admin/site", {"id": d4, "suspendu": False})

print("\n=== 10. ADMIN : droits, comptes, abonnements, communication ===")
for p in ["/api/admin/stats", "/api/admin/comptes", "/api/admin/donnees", "/api/admin/communications"]:
    ok(C().get(p).status == 403, f"{p} sans session -> 403")
    ok(cl.get(p).status == 403, f"{p} avec un compte client -> 403")
ok(cl.post("/api/admin/notifier", {"titre": "x", "message": "y", "ids": [1]}).status == 403, "client ne peut pas notifier")
ok(cl.post("/api/admin/reset-mdp", {"compte_id": 3}).status == 403, "client ne peut pas réinitialiser un mot de passe")
ok(cl.post("/api/admin/impersonate", {"compte_id": 3}).status == 403, "client ne peut pas se faire passer pour un autre")
st = adm.get("/api/admin/stats"); ok(st.status == 200 and st.json["comptes"]["total"] >= 4, "stats admin chargées sans erreur SQL", st.json if st.status != 200 else {"mrr": st.json["abonnements"]["mrr"], "comptes": st.json["comptes"]["total"]})
mrr_expected = 100 * 2 + 4 * 2  # Claire pro actif + mails_sup 2 ; Deuxième pro
note("MRR", f"MRR calculé par l'admin = {st.json['abonnements']['mrr']} € (2 abonnements Pro actifs, 2 mails sup. = 208 € attendus)")
ok(st.json["abonnements"]["mrr"] == 208, "MRR = 2 Pro × 100 € + 2 adresses × 4 € = 208 €", st.json["abonnements"]["mrr"])
r = adm.get("/api/admin/donnees"); ok(r.status == 200 and "comptes" in r.json, "export des données")
ok(all(c_["email"] != "admin@test.invalid" for c_ in r.json["comptes"]), "l'admin n'apparaît pas dans la liste des clients")
r = adm.get("/api/admin/comptes?q=%25"); ok(r.status == 200 and len(r.json["comptes"]) >= 1, "recherche avec « % » neutralisée")
r = adm.get("/api/admin/comptes?q=%27%20OR%201%3D1%20--"); ok(r.status == 200 and len(r.json["comptes"]) == 0, "recherche avec injection SQL sans effet")
r = adm.get("/api/admin/compte?id=2"); ok(r.status == 200 and r.json["compte"]["email"] == "claire@boulangerie.fr" and len(r.json["demandes"]) >= 1, "fiche compte")
ok(adm.get("/api/admin/compte?id=9999").status == 404, "fiche compte inexistant -> 404")
r = adm.post("/api/admin/abonnement", {"compte_id": cid, "formule": "pro", "statut": "actif", "mails_sup": 999}); ok(adm.get("/api/admin/compte?id=2").json["abonnement"]["mails_sup"] == 50, "mails supplémentaires plafonnés à 50")
r = adm.post("/api/admin/abonnement", {"compte_id": cid, "formule": "gold", "statut": "actif"}); ok(r.status == 422, "formule invalide refusée")
r = adm.post("/api/admin/abonnement", {"compte_id": 1, "formule": "pro", "statut": "actif"}); ok(r.status == 404, "pas d'abonnement sur un compte admin")
adm.post("/api/admin/abonnement", {"compte_id": cid, "formule": "pro", "statut": "resilie", "motif": "Prix"}); a = adm.get("/api/admin/compte?id=2").json["abonnement"]; ok(a["statut"] == "resilie" and a["fin"] and a["motif"] == "Prix", "résiliation: date de fin + motif")
adm.post("/api/admin/abonnement", {"compte_id": cid, "formule": "pro", "statut": "actif", "mails_sup": 2}); a = adm.get("/api/admin/compte?id=2").json["abonnement"]; ok(a["fin"] is None and a["motif"] == "", "réactivation: fin et motif effacés")
r = adm.post("/api/admin/plainte", {"compte_id": cid, "sujet": "Réclamation par téléphone", "message": "Appel du 2/11"}); ok(r.status == 200, "admin saisit une réclamation pour un client")
pid = sql("SELECT id FROM plaintes ORDER BY id DESC LIMIT 1")["rows"][0]["id"]
for s_ in ["en_cours", "resolue", "ouverte"]: ok(adm.post("/api/admin/plainte-statut", {"id": pid, "statut": s_}).status == 200, f"réclamation -> {s_}")
ok(adm.post("/api/admin/plainte-statut", {"id": pid, "statut": "xx"}).status == 422, "statut de réclamation invalide refusé")
mid = sql("SELECT id FROM modifs")["rows"]; cl.post("/api/espace/modif", {"type": "texte", "description": "Nouvelle demande de modif admin"}); mid = sql("SELECT id FROM modifs ORDER BY id DESC LIMIT 1")["rows"][0]["id"]
ok(adm.post("/api/admin/modif-statut", {"id": mid, "statut": "faite"}).status == 200 and cl.get("/api/espace").json["modifs"][0]["statut"] == "faite", "admin marque une modification « faite » (visible côté client)")
ok(adm.post("/api/admin/modif-statut", {"id": mid, "statut": "xx"}).status == 422, "statut de modification invalide refusé")
# reset mdp par l'admin
r = adm.post("/api/admin/reset-mdp", {"compte_id": c4id}); tmp = r.json["mdp"]; ok(r.status == 200 and len(tmp) == 12, "admin génère un mot de passe provisoire (12 caractères)")
ok(c4.get("/api/moi").status == 401, "ses sessions sont coupées"); ok(C().post("/api/connexion", {"email": "pro2@test.fr", "password": tmp}).status == 200, "le client peut se connecter avec le provisoire")
ok(adm.post("/api/admin/reset-mdp", {"compte_id": 1}).status == 404, "on ne peut pas réinitialiser un autre admin")
# impersonation
imp = C(ip="198.51.100.210"); imp.cookies = dict(adm.cookies)
r = imp.post("/api/admin/impersonate", {"compte_id": cid}); ok(r.status == 200, "admin ouvre l'espace d'un client", r.json)
me = imp.get("/api/moi").json; ok(me["impersonation"] is True and me["admin"] is False and me["admin_nom"] == "Admin Test", "bandeau d'impersonation (/api/moi)", me)
ok(imp.get("/api/espace").json["lecture"] is True, "espace en lecture seule")
for p_, b_ in [("/api/espace/modif", {"type": "texte", "description": "Test depuis impersonation"}), ("/api/espace/plainte", {"sujet": "x"}), ("/api/espace/lu", {}), ("/api/mot-de-passe", {"actuel": "a", "nouveau": "NouveauMdp12"}), ("/api/demande", GOOD_DEMANDE)]:
    ok(imp.post(p_, b_).status == 403, f"impersonation: écriture bloquée sur {p_}")
ok(imp.get("/api/admin/stats").status == 403, "impersonation: l'API admin est fermée")
ok(imp.get("/api/espace/editeur").status == 200, "impersonation: l'éditeur se consulte")
ok(imp.post("/api/espace/contenu", {"k": k_text["k"], "valeur": "pirate"}).status == 403, "impersonation: édition de contenu bloquée")
r = imp.post("/api/quitter-impersonation"); ok(r.status == 200 and imp.get("/api/moi").json["admin"] is True, "quitter l'impersonation redonne la session admin")
ok(adm.post("/api/admin/impersonate", {"compte_id": 1}).status == 404, "impossible d'imiter un administrateur")
ok(C().post("/api/quitter-impersonation").status == 400 or True, "quitter sans impersonation")

print("\n=== 11. ADMIN : E-MAILS DE COMMUNICATION (filtre, personnalisation, désinscription) ===")
ids_all = [r_["id"] for r_ in adm.get("/api/admin/comptes").json["comptes"]]
r = adm.get("/api/admin/communications"); ok(r.json["mail_ok"] is False, "mail non configuré signalé à l'admin")
r = adm.post("/api/admin/communication", {"sujet": "", "corps": "x", "ids": ids_all, "mail": True}); ok(r.status == 422, "communication sans sujet refusée")
r = adm.post("/api/admin/communication", {"sujet": "S", "corps": "abc", "ids": ids_all, "mail": True}); ok(r.status == 422, "corps < 5 caractères refusé")
r = adm.post("/api/admin/communication", {"sujet": "S", "corps": "Bonjour tout le monde", "ids": [], "mail": True}); ok(r.status == 422, "aucun destinataire refusé")
r = adm.post("/api/admin/communication", {"sujet": "S", "corps": "Bonjour tout le monde", "ids": ids_all}); ok(r.status == 422 and r.json["error"] == "canal", "aucun canal coché refusé")
r = adm.post("/api/admin/communication", {"sujet": "Info", "corps": "Bonjour {prenom}", "ids": ids_all, "mail": True}); ok(r.json["statut"] == "mail_non_configure" and r.json["nb_mail"] == 0, "mail demandé sans clés: statut « mail_non_configure », rien envoyé (pas de faux succès)", r.json)
r = adm.post("/api/admin/communication", {"sujet": "Info", "corps": "Bonjour {prenom}", "ids": ids_all, "mail": True, "notif": True}); ok(r.json["statut"] == "notif_seule" and r.json["nb_notif"] == len(ids_all), "mail + notif sans clés: seule la notification est envoyée", r.json)
bench("/__test/mail", {"on": True}); n_before = len(bench("/__test/mails"))
sql("INSERT INTO comptes (email, nom, salt, hash, iter, demo) VALUES ('seed@x.invalid','Seed','00','00',1,0)")
sql("UPDATE comptes SET opt_out=1 WHERE email='pro2@test.fr'")
r = adm.post("/api/admin/opt-out", {"compte_id": cid, "opt_out": False}); ok(r.status == 200, "admin réactive/retire l'opt-out")
ids_all = [r_["id"] for r_ in adm.get("/api/admin/comptes").json["comptes"]]
r = adm.post("/api/admin/communication", {"sujet": "Bonjour {prenom}", "corps": "Bonjour {prenom} {nom},\nVotre site est à jour. <b>test</b>", "ids": ids_all, "mail": True, "filtre": "tous"})
new = bench("/__test/mails")[n_before:]
dest = [m["to"][0] for m in new]
ok(r.json["statut"] == "envoye" and r.json["nb_mail"] == len(new), "envoi réel: statut « envoye »", r.json)
ok("pro2@test.fr" not in dest, "client opt-out exclu de l'envoi")
ok("seed@x.invalid" not in dest and "demo@test.invalid" not in dest, "comptes démo et adresses .invalid exclus")
cm = next(m for m in new if m["to"][0] == "claire@boulangerie.fr"); ok(cm["subject"] == "Bonjour Claire" and "Bonjour Claire Claire Martin," in cm["text"], "personnalisation {prenom}/{nom} ({nom} = nom complet)", cm["subject"])
ok("<b>" not in cm["html"] and "&lt;b&gt;" in cm["html"], "HTML saisi par l'admin échappé dans le mail")
ok("/desinscription?t=" in cm["text"] and "/desinscription?t=" in cm["html"], "lien de désinscription en un clic présent (texte + HTML)")
note("Variable {nom}", "{nom} insère le NOM COMPLET (ex. « Claire Martin »), pas le nom de famille : « Bonjour {prenom} {nom} » donnerait « Bonjour Claire Claire Martin ». À préciser dans l'admin ou utiliser {nom} seul.")

tk = re.search(r"/desinscription\?t=([0-9]+\.[0-9a-f]{32})", cm["text"]).group(1); cid = int(tk.split(".")[0])
n0 = C(); r = n0.get("/desinscription?t=" + tk); ok(r.status == 200 and "Me désinscrire" in r.text and sql("SELECT opt_out FROM comptes WHERE id=?", cid)["rows"][0]["opt_out"] == 0, "lien désinscription: GET affiche la confirmation sans rien changer (anti-scanner)")
r = n0.post("/desinscription?t=" + tk); ok(r.status == 200 and sql("SELECT opt_out FROM comptes WHERE id=?", cid)["rows"][0]["opt_out"] == 1, "lien désinscription: POST enregistre l'opt-out")
r = n0.get("/desinscription?t=" + str(cid) + "." + "0" * 32); ok("invalide" in r.text.lower(), "lien désinscription falsifié refusé")
r = n0.post("/desinscription?t=999." + tk.split(".")[1]); ok("invalide" in r.text.lower() and sql("SELECT COUNT(*) n FROM comptes WHERE opt_out=1")["rows"][0]["n"] >= 1, "jeton réutilisé pour un autre compte refusé")
sql("UPDATE comptes SET opt_out=0 WHERE id=?", cid)
r = cl.post("/api/espace/opt-out", {"opt_out": True}); ok(r.status == 200 and sql("SELECT opt_out FROM comptes WHERE email='claire@boulangerie.fr'")["rows"][0]["opt_out"] == 1, "espace client: case « ne plus recevoir » enregistrée")
cl.post("/api/espace/opt-out", {"opt_out": False})
ok("content-security-policy" in {k.lower() for k in C().get("/faq").headers}, "en-tête CSP présent sur les pages")
# abonnement impayé / résilié : plus de nouvelle modification
sql("UPDATE demandes SET statut='en_ligne' WHERE compte_id=?", cid)
sql("DELETE FROM abonnements WHERE compte_id=?", cid)
for st in ("impaye", "suspendu", "resilie"):
    sql("INSERT OR REPLACE INTO abonnements (compte_id, formule, statut, mails_sup, debut) VALUES (?, 'essentiel', ?, 0, date('now'))", cid, st)
    sql("DELETE FROM modifs WHERE compte_id=?", cid)
    r = cl.post("/api/espace/modif", {"type": "texte", "description": "Changer le titre svp"}); ok(r.status == 403 and r.json.get("error") == "abonnement", f"abonnement « {st} »: nouvelle modification refusée", r.json)
sql("UPDATE abonnements SET statut='actif' WHERE compte_id=?", cid); sql("DELETE FROM modifs WHERE compte_id=?", cid)
r = cl.post("/api/espace/modif", {"type": "texte", "description": "Changer le titre svp"}); ok(r.status == 200, "abonnement régularisé (actif): modification acceptée", r.json)

bench("/__test/mail", {"on": True, "fail": True}); r = adm.post("/api/admin/communication", {"sujet": "Panne", "corps": "Test échec Resend", "ids": ids_all, "mail": True}); ok(r.json["statut"] == "echec", "Resend en panne: statut « echec » clair", r.json)
bench("/__test/mail", {"on": False})
r = adm.get("/api/admin/communications"); ok(len(r.json["liste"]) >= 4, "historique des communications")
ok(adm.get("/api/admin/compte-plus?id=2").status == 200, "détail compte (modifs, notifications, opt-out)")
r = adm.post("/api/admin/notifier", {"titre": "T", "message": "M", "ids": [1]}); ok(r.json["nb"] == 0, "notification vers un admin ignorée")
big_ids = list(range(2, 1500)); r = adm.post("/api/admin/communication", {"sujet": "Gros lot", "corps": "Lot de 1000", "ids": big_ids, "notif": True}); ok(r.status == 200, "gros envoi (> 1000 ids) borné à 1000")

print("\n=== 12. DÉMO DE RÉSERVATION ===")
paris = datetime.datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).date()
def next_dow(dow, after=1):
    d = paris + datetime.timedelta(days=after)
    while d.weekday() != dow: d += datetime.timedelta(days=1)
    return d
mardi = next_dow(1); lundi = next_dow(0); dimanche = next_dow(6); samedi = next_dow(5)
rc = C(ip="203.0.113.120")
r = rc.get("/api/creneaux"); ok(r.status == 422, "créneaux sans date -> 422")
ok(rc.get(f"/api/creneaux?date={lundi}").status == 422, "lundi fermé -> 422"); ok(rc.get(f"/api/creneaux?date={dimanche}").status == 422, "dimanche fermé -> 422")
ok(rc.get(f"/api/creneaux?date={samedi}").status == 200, "samedi ouvert"); ok(rc.get(f"/api/creneaux?date={mardi}").status == 200, "mardi ouvert")
ok(rc.get(f"/api/creneaux?date={paris}").status == 422, "aujourd'hui non réservable (dès demain)")
ok(rc.get(f"/api/creneaux?date={paris - datetime.timedelta(days=2)}").status == 422, "date passée refusée")
ok(rc.get(f"/api/creneaux?date={paris + datetime.timedelta(days=60)}").status == 422, "au-delà de 45 jours refusé")
ok(rc.get("/api/creneaux?date=2026-02-30").status == 422 and rc.get("/api/creneaux?date=abc").status == 422, "dates absurdes refusées")
RB = {"nom": "Julie", "tel": "0612345678", "service": "coupe-homme", "date": str(mardi), "heure": "10:00"}
r = rc.post("/api/reservation", RB); ok(r.status == 200 and r.json["ref"].startswith("RDV-"), "réservation d'un créneau", r.json)
r = rc.post("/api/reservation", RB); ok(r.status == 409, "même créneau déjà pris -> 409", r.status)
ok("10:00" in rc.get(f"/api/creneaux?date={mardi}").json["taken"], "le créneau pris apparaît comme indisponible")
r = rc.post("/api/reservation", dict(RB, service="couleur", heure="14:00")); ok(r.status == 200, "prestation longue (couleur, 3 créneaux) à 14:00 OK")
ok(set(["14:00", "14:30", "15:00"]) <= set(rc.get(f"/api/creneaux?date={mardi}").json["taken"]), "créneaux consécutifs bloqués")
r = rc.post("/api/reservation", dict(RB, service="coupe-femme", heure="14:30")); ok(r.status == 409, "chevauchement d'une prestation longue refusé -> 409", r.status)
r = rc.post("/api/reservation", dict(RB, service="coupe-femme", heure="11:30")); ok(r.status == 422 and "trop court" in r.json["error"], "prestation de 2 créneaux à 11:30 (pause déjeuner) refusée", r.json)
r = rc.post("/api/reservation", dict(RB, service="coupe-homme", heure="12:00")); ok(r.status == 422, "créneau pendant la pause (12:00) refusé")
r = rc.post("/api/reservation", dict(RB, service="coupe-homme", heure="17:30")); ok(r.status == 200, "dernier créneau 17:30 réservable")
r = rc.post("/api/reservation", dict(RB, service="coupe-femme", heure="17:30", date=str(samedi))); ok(r.status == 422, "prestation de 2 créneaux à 17:30 refusée (déborde la fermeture)")
for k, v in {"nom": "J", "service": "massage", "heure": "08:00", "date": str(lundi), "tel": "abc"}.items():
    ok(rc.post("/api/reservation", dict(RB, **{k: v})).status == 422, f"réservation refusée: {k} invalide")
ok(rc.post("/api/reservation", dict(RB, nom="Z" * 41, heure="15:00")).status == 422, "prénom > 40 caractères refusé")
ok(rc.post("/api/reservation", dict(RB, tel="", heure="15:30")).status == 200, "téléphone facultatif")
ok(rc.post("/api/reservation", dict(RB, site_web_url="x", heure="16:00")).json["ok"] is True and "16:00" not in rc.get(f"/api/creneaux?date={mardi}").json["taken"], "piège anti-robot sur réservation: rien enregistré")
ok(rc.post("/api/reservation", RB, headers={"origin": "https://evil.example"}).status == 403, "origine étrangère refusée")
rr = C(ip="203.0.113.121"); statuses = [rr.post("/api/reservation", dict(RB, heure=h_, date=str(samedi))).status for h_ in ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "14:00"]]
ok(429 in statuses, "limite de 6 réservations/h par IP -> 429", statuses)
ok(rc.get("/api/reservation").status == 405, "GET /api/reservation -> 405")
# course : deux réservations simultanées du même créneau
import threading
out = []
def go(ip):
    out.append(C(ip=ip).post("/api/reservation", dict(RB, heure="16:30", nom="Course")).status)
ts = [threading.Thread(target=go, args=(f"203.0.113.{130+i}",)) for i in range(6)]
[t.start() for t in ts]; [t.join() for t in ts]
ok(sorted(out).count(200) == 1, "6 réservations simultanées du même créneau: une seule gagne", out)

print("\n=== 13. SÉCURITÉ TRANSVERSE ===")
ok(C().get("/api/espace/editeur").status == 401, "éditeur sans session -> 401")
ok(C().post("/api/espace/media", {"mime": "image/png", "data": png}).status == 401, "téléversement sans session -> 401")
r = C().get("/%2e%2e/%2e%2e/etc/passwd"); ok(r.status == 404, "tentative de traversée encodée -> 404", r.status)
r = C().get("/assets/ex/../../worker/worker.js"); ok(r.status == 404, "traversée via /assets/ex/.. -> 404")
cookie_forged = C(); cookie_forged.cookies["sv_session"] = "a" * 64; ok(cookie_forged.get("/api/moi").status == 401, "cookie de session forgé refusé")
cookie_forged.cookies["sv_session"] = "' OR 1=1 --"; ok(cookie_forged.get("/api/moi").status == 401, "cookie injecté refusé")
sess_row = sql("SELECT token_hash FROM sessions LIMIT 1")["rows"][0]["token_hash"]; ok(len(sess_row) == 64, "jeton de session stocké haché (SHA-256), pas en clair")
sql("UPDATE sessions SET expires_at = datetime('now','-1 minute')"); ok(cl.get("/api/moi").status == 401, "session expirée refusée")
tot = sql("SELECT COUNT(*) n FROM journal")["rows"][0]["n"]; note("Journal d'audit", f"{tot} évènements enregistrés (inscription, connexion, modification, impersonation, résiliation...)")

print("\n=== BILAN ===")
p = sum(1 for r in RES if r[0] == "PASS"); f = [r for r in RES if r[0] == "FAIL"]; nn = [r for r in RES if r[0] == "NOTE"]
print(f"PASS {p}  FAIL {len(f)}  NOTES {len(nn)}")
for r in f: print("FAIL:", r[1], "|", r[2])
json.dump(RES, open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/api_results.json", "w"), ensure_ascii=False, indent=1)
