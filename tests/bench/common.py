import json, re, sys, urllib.request, time
from playwright.sync_api import sync_playwright, expect

B = "http://localhost:8787"
RES = []
OUT = None

def rec(status, name, detail=""):
    RES.append((status, name, detail)); print(f"{status:5} {name}" + (f"  -> {detail}" if detail else ""), flush=True)

def ok(cond, name, detail=""): rec("PASS" if cond else "FAIL", name, "" if cond else str(detail)[:400])
def note(name, detail): rec("NOTE", name, detail)

def bench(path, body=None):
    rq = urllib.request.Request(B + path, data=json.dumps(body).encode() if body is not None else None, method="POST" if body is not None else "GET", headers={"content-type": "application/json"})
    return json.loads(urllib.request.urlopen(rq).read())

def sql(q, *args):
    rq = urllib.request.Request(B + "/__test/sql", data=json.dumps({"sql": q, "args": list(args)}).encode(), method="POST", headers={"content-type": "application/json"})
    try: return json.loads(urllib.request.urlopen(rq).read())
    except urllib.error.HTTPError as e: return json.loads(e.read())

class Watch:
    """Capture erreurs JS, console error, requêtes en échec pendant un bloc."""
    def __init__(self, page, ignore=()):
        self.errs = []; self.page = page; self.ignore = ignore
        page.on("pageerror", lambda e: self.errs.append("JS: " + str(e)[:200]))
        page.on("console", lambda m: self.errs.append("console.error: " + m.text[:200]) if m.type == "error" and not any(i in m.text for i in ignore) and not m.text.startswith("Failed to load resource") else None)
        page.on("requestfailed", lambda r: self.errs.append("requestfailed: " + r.url[-80:]) if "fonts.g" not in r.url else None)
        page.on("response", lambda r: self.errs.append(f"HTTP {r.status}: " + r.url.replace(B, "")[:90]) if r.status >= 400 and not any(i in r.url for i in ignore) else None)
    def take(self):
        e = self.errs[:]; self.errs.clear(); return e

def step(name):
    def deco(fn):
        try:
            fn();
        except Exception as e:
            rec("FAIL", name, "exception: " + str(e).split("\n")[0][:300])
        return fn
    return deco

def launch(p, w=1280, h=900, mobile=False):
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    ctx = br.new_context(viewport={"width": w, "height": h}, locale="fr-FR", timezone_id="Europe/Paris", has_touch=mobile, is_mobile=mobile)
    ctx.set_default_timeout(6000)
    import os
    if os.environ.get('NOPOP'): ctx.add_init_script("try{localStorage.setItem('dw-avis-plus-tard',String(Date.now()))}catch(e){}")
    return br, ctx

def finish(path):
    p = sum(1 for r in RES if r[0] == "PASS"); f = [r for r in RES if r[0] == "FAIL"]; n = [r for r in RES if r[0] == "NOTE"]
    print(f"\nBILAN: PASS {p}  FAIL {len(f)}  NOTES {len(n)}")
    for r in f: print("FAIL:", r[1], "|", r[2])
    json.dump(RES, open(path, "w"), ensure_ascii=False, indent=1)
