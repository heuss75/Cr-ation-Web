# Petit serveur local qui imite le routage du Worker (URLs sans .html). Usage : python3 tools/serve.py 8787
import http.server, os, sys, json
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
ROUTES = {"/": "index.html", "/offre": "offre.html", "/faq": "faq.html", "/commander": "commander.html", "/connexion": "connexion.html",
          "/mentions-legales": "mentions-legales.html", "/cgv": "cgv.html", "/confidentialite": "confidentialite.html", "/cookies": "cookies.html"}
TYPES = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".json": "application/json", ".txt": "text/plain"}
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        path = self.path.split("?")[0]
        f = ROUTES.get(path) or (path.lstrip("/") if path.startswith("/assets/") or path in ("/robots.txt", "/sitemap.xml") else None)
        code = 200
        if not f or not os.path.isfile(os.path.join(ROOT, f)):
            f, code = "404.html", 404
        data = open(os.path.join(ROOT, f), "rb").read()
        self.send_response(code); self.send_header("content-type", TYPES.get(os.path.splitext(f)[1], "application/octet-stream")); self.end_headers(); self.wfile.write(data)
    def do_POST(self):
        n = int(self.headers.get("content-length", 0)); body = json.loads(self.rfile.read(n) or b"{}")
        self.send_response(200); self.send_header("content-type", "application/json"); self.end_headers()
        self.wfile.write(json.dumps({"ok": True, "ref": "SVE-TEST42"}).encode())
http.server.ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 8787), H).serve_forever()
