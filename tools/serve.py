# Petit serveur local qui imite le routage du Worker (URLs sans .html). Usage : python3 tools/serve.py 8787
import http.server, os, sys, json
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
ROUTES = {"/": "index.html", "/offre": "offre.html", "/faq": "faq.html", "/commander": "commander.html", "/connexion": "connexion.html",
          "/mentions-legales": "mentions-legales.html", "/cgv": "cgv.html", "/confidentialite": "confidentialite.html", "/cookies": "cookies.html", "/guide-messagerie": "guide-messagerie.html", "/reservation-demo": "reservation-demo.html", "/inscription": "inscription.html", "/admin": "admin.html", "/espace": "espace.html", "/exemples/bistro": "exemples/bistro.html", "/exemples/salon": "exemples/salon.html", "/exemples/artisan": "exemples/artisan.html"}
TYPES = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".json": "application/json", ".txt": "text/plain"}
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _j(self, obj, code=200, cookie=None):
        self.send_response(code); self.send_header("content-type", "application/json")
        if cookie is not None: self.send_header("set-cookie", cookie)
        self.end_headers(); self.wfile.write(json.dumps(obj).encode())
    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/api/moi":
            if "sv_session=1" in (self.headers.get("cookie") or ""): return self._j({"ok": True, "nom": "Test", "email": "test@exemple.fr"})
            return self._j({"ok": False}, 401)
        f = ROUTES.get(path) or (path.lstrip("/") if path.startswith("/assets/") or path in ("/robots.txt", "/sitemap.xml") else None)
        code = 200
        if not f or not os.path.isfile(os.path.join(ROOT, f)):
            f, code = "404.html", 404
        data = open(os.path.join(ROOT, f), "rb").read()
        self.send_response(code); self.send_header("content-type", TYPES.get(os.path.splitext(f)[1], "application/octet-stream")); self.end_headers(); self.wfile.write(data)
    def do_POST(self):
        n = int(self.headers.get("content-length", 0)); body = json.loads(self.rfile.read(n) or b"{}")
        p = self.path.split("?")[0]
        if p == "/api/inscription": return self._j({"ok": True, "nom": "Test"}, 200, "sv_session=1; Path=/")
        if p == "/api/connexion":
            return self._j({"ok": True}, 200, "sv_session=1; Path=/") if body.get("password") == "password123" else self._j({"ok": False}, 401)
        if p == "/api/deconnexion": return self._j({"ok": True}, 200, "sv_session=0; Path=/")
        if "sv_session=1" not in (self.headers.get("cookie") or ""): return self._j({"ok": False}, 401)
        self._j({"ok": True, "ref": "SVE-TEST42"})
http.server.ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 8787), H).serve_forever()
