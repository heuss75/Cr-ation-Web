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
