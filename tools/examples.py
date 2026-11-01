# -*- coding: utf-8 -*-
"""Génère 3 sites d'exemple complets (site/exemples/<nom>.html). Usage : python3 tools/examples.py"""
import os, random, math
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "exemples"); os.makedirs(OUT, exist_ok=True)
BISTRO_SVG = open(os.path.join(ROOT, "tools", "src", "bistro-scene.svg")).read()

def slot(name, art):
    return f'<span class="sl">{art}<img src="/assets/ex/{name}.jpg" alt="" loading="lazy" onerror="this.remove()"></span>'

def svg(w, h, inner, extra=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" {extra} aria-hidden="true">{inner}</svg>'

# ---------- illustrations ----------
def plate(seed, kind):
    R = random.Random(seed); s = []
    s.append('<defs><radialGradient id="pw%d" cx=".4" cy=".35" r=".9"><stop offset="0" stop-color="#8a5a33"/><stop offset="1" stop-color="#3a2212"/></radialGradient><radialGradient id="pp%d"><stop offset=".7" stop-color="#fbfaf6"/><stop offset="1" stop-color="#d9d5ca"/></radialGradient><filter id="ps%d"><feGaussianBlur stdDeviation="9"/></filter></defs>' % (seed, seed, seed))
    s.append('<rect width="400" height="400" fill="url(#pw%d)"/>' % seed)
    for i in range(14):
        y = i * 30 + R.randint(-6, 6)
        s.append('<path d="M0 %d Q200 %d 400 %d" stroke="#20120a" stroke-opacity=".28" stroke-width="%.1f" fill="none"/>' % (y, y + R.randint(-14, 14), y + R.randint(-8, 8), R.uniform(1, 3)))
    s.append('<ellipse cx="212" cy="222" rx="150" ry="150" fill="#000" opacity=".5" filter="url(#ps%d)"/>' % seed)
    s.append('<circle cx="200" cy="200" r="150" fill="url(#pp%d)"/><circle cx="200" cy="200" r="112" fill="none" stroke="#cfcabd" stroke-width="2"/>' % seed)
    if kind == "salade":
        for _ in range(46):
            a = R.uniform(0, 6.28); d = R.uniform(0, 88); x = 200 + math.cos(a) * d; y = 200 + math.sin(a) * d
            c = R.choice(["#4f8f2e", "#79b83a", "#2f6b22", "#a7d44b"])
            s.append('<ellipse cx="%.0f" cy="%.0f" rx="%d" ry="%d" fill="%s" transform="rotate(%d %.0f %.0f)"/>' % (x, y, R.randint(14, 24), R.randint(7, 11), c, R.randint(0, 180), x, y))
        for _ in range(7):
            a = R.uniform(0, 6.28); d = R.uniform(10, 80); x = 200 + math.cos(a) * d; y = 200 + math.sin(a) * d
            s.append('<circle cx="%.0f" cy="%.0f" r="11" fill="#d9362b"/><circle cx="%.0f" cy="%.0f" r="4" fill="#fff" opacity=".35"/>' % (x, y, x - 3, y - 4))
        for _ in range(4):
            x = 200 + R.uniform(-60, 60); y = 200 + R.uniform(-60, 60)
            s.append('<rect x="%.0f" y="%.0f" width="24" height="24" rx="5" fill="#f2e6c2" transform="rotate(%d %.0f %.0f)"/>' % (x, y, R.randint(0, 80), x, y))
    elif kind == "viande":
        s.append('<path d="M120 190q10-50 80-52t84 46q6 52-60 62t-96-10z" fill="#5b2a17"/><path d="M135 188q14-38 66-40t72 36" fill="none" stroke="#8a4a2a" stroke-width="7" stroke-linecap="round"/>')
        for k in range(5):
            s.append('<path d="M%d 178 q30 8 64 -2" stroke="#2c130a" stroke-width="5" fill="none" opacity=".6" transform="translate(0 %d)"/>' % (140 + k * 4, k * 14))
        s.append('<path d="M108 262q60 30 160 -10" stroke="#3c1a0d" stroke-width="9" fill="none" stroke-linecap="round" opacity=".85"/>')
        for _ in range(26):
            x = R.uniform(240, 300); y = R.uniform(120, 160)
            s.append('<ellipse cx="%.0f" cy="%.0f" rx="14" ry="6" fill="#4a8c2a" transform="rotate(%d %.0f %.0f)"/>' % (x, y, R.randint(0, 180), x, y))
        for _ in range(6): s.append('<circle cx="%.0f" cy="%.0f" r="9" fill="#e8b04a"/>' % (R.uniform(110, 150), R.uniform(230, 280)))
    elif kind == "dessert":
        s.append('<circle cx="200" cy="205" r="72" fill="#4a2414"/><circle cx="200" cy="205" r="72" fill="none" stroke="#2d130a" stroke-width="4"/><path d="M148 190q50-40 104 0" stroke="#7a4326" stroke-width="10" fill="none" stroke-linecap="round" opacity=".8"/>')
        s.append('<path d="M120 270q80 26 168 -4" stroke="#b3202c" stroke-width="12" fill="none" stroke-linecap="round" opacity=".85"/>')
        for _ in range(9):
            a = R.uniform(0, 6.28); x = 200 + math.cos(a) * 80; y = 205 + math.sin(a) * 80
            s.append('<circle cx="%.0f" cy="%.0f" r="10" fill="#c3162b"/><circle cx="%.0f" cy="%.0f" r="3" fill="#fff" opacity=".45"/>' % (x, y, x - 3, y - 3))
        s.append('<ellipse cx="248" cy="178" rx="30" ry="22" fill="#fff4dc"/><ellipse cx="244" cy="172" rx="14" ry="8" fill="#fff" opacity=".6"/>')
    elif kind == "tarte":
        s.append('<circle cx="200" cy="200" r="98" fill="#d8923a"/><circle cx="200" cy="200" r="98" fill="none" stroke="#a8631b" stroke-width="6"/>')
        for k in range(14):
            a = k * 6.283 / 14
            for d in (62, 38):
                x = 200 + math.cos(a + d / 100) * d; y = 200 + math.sin(a + d / 100) * d
                s.append('<ellipse cx="%.0f" cy="%.0f" rx="22" ry="9" fill="#f6e3a8" stroke="#c98f3a" stroke-width="2" transform="rotate(%d %.0f %.0f)"/>' % (x, y, math.degrees(a) + 90, x, y))
        s.append('<circle cx="200" cy="200" r="12" fill="#a8531b"/><ellipse cx="300" cy="120" rx="30" ry="24" fill="#fff4dc"/>')
    elif kind == "creme":
        s.append('<circle cx="200" cy="200" r="92" fill="#f4f1ea" stroke="#d8d2c4" stroke-width="5"/><circle cx="200" cy="200" r="76" fill="#d9952a"/><circle cx="200" cy="200" r="76" fill="url(#pp%d)" opacity=".18"/>' % seed)
        for _ in range(9): s.append('<path d="M%d %d l%d %d" stroke="#8a4a10" stroke-width="2" opacity=".6"/>' % (R.randint(150, 250), R.randint(150, 250), R.randint(-30, 30), R.randint(-30, 30)))
        s.append('<ellipse cx="170" cy="170" rx="26" ry="14" fill="#fff" opacity=".35"/><circle cx="315" cy="285" r="16" fill="#b3202c"/>')
    elif kind == "cafe":
        s.append('<circle cx="165" cy="175" r="70" fill="#fff" stroke="#d5d0c3" stroke-width="3"/><circle cx="165" cy="175" r="50" fill="#2a140a"/><circle cx="165" cy="175" r="50" fill="none" stroke="#6b3a1d" stroke-width="4"/><path d="M232 160q34 0 28 30t-34 20" stroke="#fff" stroke-width="12" fill="none"/>')
        for i, (x, y, c) in enumerate(((120, 285, "#4a2414"), (200, 300, "#c3162b"), (280, 280, "#e9c46a"))):
            s.append('<rect x="%d" y="%d" width="52" height="52" rx="10" fill="%s"/><circle cx="%d" cy="%d" r="8" fill="#fff" opacity=".35"/>' % (x - 26, y - 26, c, x - 8, y - 8))
    elif kind == "poisson":
        s.append('<path d="M110 200q60-62 170-8q20 30-6 52q-100 34-164-44z" fill="#f4ddb8"/><path d="M130 205q50-30 124-2" stroke="#e0b878" stroke-width="5" fill="none"/><path d="M150 228q40 12 100-6" stroke="#e0b878" stroke-width="4" fill="none" opacity=".7"/>')
        s.append('<path d="M120 275q80 28 168 -4" stroke="#f1e29a" stroke-width="14" fill="none" stroke-linecap="round" opacity=".9"/>')
        for _ in range(16): s.append('<ellipse cx="%.0f" cy="%.0f" rx="13" ry="6" fill="#4a8c2a" transform="rotate(%d)"/>' % (R.uniform(240, 300), R.uniform(130, 170), R.randint(0, 150)))
        for _ in range(5): s.append('<circle cx="%.0f" cy="%.0f" r="9" fill="#e8742a"/>' % (R.uniform(120, 160), R.uniform(130, 150)))
    elif kind == "risotto":
        s.append('<circle cx="200" cy="200" r="98" fill="#f1e5c4"/>')
        for _ in range(120): s.append('<ellipse cx="%.0f" cy="%.0f" rx="5" ry="2.4" fill="#fff8e2" transform="rotate(%d)"/>' % (200 + R.uniform(-85, 85), 200 + R.uniform(-60, 60), R.randint(0, 180)))
        for _ in range(9): s.append('<ellipse cx="%.0f" cy="%.0f" rx="15" ry="9" fill="#8a6a45"/><ellipse cx="%.0f" cy="%.0f" rx="9" ry="4" fill="#b99468"/>' % ((x := 200 + R.uniform(-60, 60)), (y := 200 + R.uniform(-50, 50)), x, y - 3))
        for _ in range(6): s.append('<ellipse cx="%.0f" cy="%.0f" rx="10" ry="4" fill="#3f7d27"/>' % (200 + R.uniform(-50, 50), 200 + R.uniform(-40, 40)))
    else:  # soupe
        s.append('<circle cx="200" cy="200" r="104" fill="#e3822a"/><circle cx="200" cy="200" r="104" fill="none" stroke="#b9591b" stroke-width="6"/>')
        s.append('<path d="M120 200q40-40 80 0t80 0" stroke="#fff4dc" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M135 232q30-28 60 0t60 0" stroke="#fff4dc" stroke-width="6" fill="none" stroke-linecap="round" opacity=".8"/>')
        for _ in range(20):
            a = R.uniform(0, 6.28); d = R.uniform(0, 90); x = 200 + math.cos(a) * d; y = 200 + math.sin(a) * d
            s.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#2f6b22"/>' % (x, y, R.uniform(2, 4.5)))
    s.append('<circle cx="200" cy="200" r="150" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="3" stroke-dasharray="60 400" transform="rotate(-50 200 200)"/>')
    return svg(400, 400, "".join(s))

def hair(seed, c1, c2, bg1, bg2):
    R = random.Random(seed); s = [f'<defs><linearGradient id="hb{seed}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/></linearGradient><linearGradient id="hh{seed}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect width="400" height="500" fill="url(#hb{seed})"/>']
    s.append('<ellipse cx="200" cy="470" rx="120" ry="90" fill="#e9c6ab"/><rect x="170" y="330" width="60" height="120" fill="#e0b99c"/>')
    s.append('<path d="M104 250C84 70 316 70 296 250C300 340 280 420 250 450L150 450C120 420 100 340 104 250Z" fill="url(#hh%d)"/>' % seed)
    for i in range(30):
        x0 = R.uniform(108, 292); y0 = R.uniform(110, 190)
        s.append('<path d="M%.0f %.0f C%.0f %.0f %.0f %.0f %.0f %.0f" stroke="%s" stroke-opacity="%.2f" stroke-width="%.1f" fill="none" stroke-linecap="round"/>' % (x0, y0, x0 + R.uniform(-40, 40), y0 + 100, x0 + R.uniform(-50, 50), y0 + 200, x0 + R.uniform(-30, 30), y0 + R.uniform(250, 330), R.choice([c1, c2, "#fff"]), R.uniform(.15, .4), R.uniform(2, 6)))
    s.append('<ellipse cx="200" cy="268" rx="76" ry="96" fill="#f0cdb2"/>')
    s.append('<path d="M122 262C112 120 288 120 278 262C268 200 240 160 200 160S132 200 122 262Z" fill="url(#hh%d)"/>' % seed)
    s.append('<ellipse cx="172" cy="274" rx="8" ry="4.5" fill="#3a2a22"/><ellipse cx="228" cy="274" rx="8" ry="4.5" fill="#3a2a22"/><path d="M182 322q18 12 36 0" stroke="#b5604e" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M160 262q12-6 24 0M216 262q12-6 24 0" stroke="#3a2a22" stroke-width="3" fill="none" opacity=".6"/>')
    return svg(400, 500, "".join(s))

def blueprint(seed):
    s = ['<rect width="600" height="400" fill="#0f3a5c"/>']
    for x in range(0, 600, 24): s.append('<path d="M%d 0V400" stroke="#6fb2e3" stroke-opacity=".16"/>' % x)
    for y in range(0, 400, 24): s.append('<path d="M0 %d H600" stroke="#6fb2e3" stroke-opacity=".16"/>' % y)
    s.append('<g fill="none" stroke="#e8f4ff" stroke-width="2.4" stroke-linejoin="round"><path d="M120 300V170L300 70L480 170V300Z"/><path d="M120 170H480M300 70V300"/><rect x="170" y="200" width="70" height="50"/><rect x="360" y="200" width="70" height="50"/><path d="M265 300V235H335V300"/><path d="M96 300H504"/></g>')
    s.append('<g stroke="#f2a900" stroke-width="1.6" fill="none"><path d="M120 330H480M120 322V338M480 322V338"/><path d="M520 300V70M512 300H528M512 70H528"/></g><g fill="#f2a900" font-family="monospace" font-size="13"><text x="270" y="326">8,40 m</text><text x="528" y="190">5,20 m</text></g>')
    return svg(600, 400, "".join(s))

def tools_art():
    s = ['<defs><linearGradient id="tg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6d27a"/><stop offset="1" stop-color="#c78a12"/></linearGradient></defs><rect width="600" height="400" fill="#e9edf1"/><rect y="270" width="600" height="130" fill="#b7915f"/>']
    for i in range(10): s.append('<path d="M0 %d H600" stroke="#8f6c3f" stroke-opacity=".5"/>' % (278 + i * 13))
    s.append('<g transform="rotate(-18 190 210)"><rect x="60" y="195" width="260" height="30" rx="5" fill="url(#tg)"/>' + "".join('<path d="M%d 195v%d" stroke="#6b4a08" stroke-width="2"/>' % (80 + i * 20, 10 + (i % 2) * 6) for i in range(12)) + '</g>')
    s.append('<g transform="rotate(24 420 200)"><rect x="400" y="80" width="26" height="230" rx="10" fill="#222"/><rect x="380" y="60" width="66" height="44" rx="8" fill="#d8341e"/></g>')
    s.append('<circle cx="110" cy="320" r="46" fill="#14202B"/><circle cx="110" cy="320" r="30" fill="none" stroke="#f2a900" stroke-width="6" stroke-dasharray="8 6"/><circle cx="110" cy="320" r="9" fill="#e9edf1"/>')
    s.append('<path d="M260 330h130v34H260z" fill="#f2a900"/><path d="M260 330l20-30h90l20 30" fill="#14202B"/>')
    return svg(600, 400, "".join(s))

def marche():
    R = random.Random(3); s = ['<defs><linearGradient id="mk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f1d9a8"/><stop offset="1" stop-color="#c98d4a"/></linearGradient></defs><rect width="400" height="500" fill="url(#mk)"/><rect y="360" width="400" height="140" fill="#6a4423"/>']
    for i in range(7): s.append('<path d="M0 %d H400" stroke="#4a2d14" stroke-opacity=".5" stroke-width="2"/>' % (380 + i * 18))
    s.append('<rect x="30" y="250" width="340" height="150" rx="10" fill="#8a5a2c"/><path d="M30 290H370M30 340H370" stroke="#5a3a18" stroke-width="3"/>')
    for _ in range(26):
        x = R.uniform(50, 350); y = R.uniform(215, 275); c = R.choice(["#d9362b", "#e8742a", "#f2b632", "#7bb53a"]); r = R.randint(18, 28)
        s.append('<circle cx="%.0f" cy="%.0f" r="%d" fill="%s"/><circle cx="%.0f" cy="%.0f" r="%d" fill="#fff" opacity=".28"/>' % (x, y, r, c, x - r / 3, y - r / 3, r / 4))
    for _ in range(14):
        x = R.uniform(60, 340)
        s.append('<path d="M%.0f 230l%d -%d" stroke="#e8742a" stroke-width="12" stroke-linecap="round"/><path d="M%.0f 160q-12-30 0-50M%.0f 160q12-30 24-44" stroke="#3f7d27" stroke-width="5" fill="none"/>' % (x, R.randint(-10, 10), R.randint(50, 90), x, x))
    s.append('<path d="M90 120q10-70 70-60q40 10 30 60z" fill="#3f7d27" opacity=".9"/><rect x="34" y="40" width="332" height="30" rx="6" fill="#d9362b"/>' + "".join('<rect x="%d" y="40" width="28" height="30" fill="#fff" opacity=".9"/>' % (60 + i * 56) for i in range(5)))
    return svg(400, 500, "".join(s))

def bathroom():
    R = random.Random(8); s = ['<rect width="600" height="400" fill="#e8eef0"/>']
    for x in range(0, 600, 40):
        for y in range(0, 300, 40): s.append('<rect x="%d" y="%d" width="38" height="38" fill="#fff" stroke="#c5d2d6"/>' % (x, y))
    s.append('<rect y="300" width="600" height="100" fill="#8d9aa0"/><rect x="40" y="20" width="200" height="300" fill="#bfe3ee" opacity=".55" stroke="#14202B" stroke-width="5"/><path d="M60 40V250" stroke="#fff" stroke-width="6" opacity=".6"/>')
    s.append('<path d="M140 30v40M140 70h60" stroke="#aeb7bd" stroke-width="8" fill="none"/><circle cx="200" cy="74" r="20" fill="#c9d1d6"/>' + "".join('<path d="M%d 100v%d" stroke="#8fd1ea" stroke-width="2" opacity=".8"/>' % (180 + i * 9, 60 + R.randint(0, 40)) for i in range(5)))
    s.append('<rect x="320" y="190" width="220" height="60" rx="10" fill="#fff" stroke="#c5d2d6" stroke-width="3"/><path d="M360 190V150h20v-24M360 150h40" stroke="#aeb7bd" stroke-width="8" fill="none"/><rect x="330" y="250" width="200" height="50" fill="#8a5a2c"/><rect x="300" y="110" width="140" height="56" rx="4" fill="#f2a900" opacity=".9"/><circle cx="370" cy="138" r="18" fill="#fff" opacity=".9"/>')
    return svg(600, 400, "".join(s))

def boiler():
    s = ['<rect width="600" height="400" fill="#dfe5ea"/><rect y="320" width="600" height="80" fill="#9aa6af"/>']
    s.append('<rect x="210" y="40" width="180" height="270" rx="16" fill="#f7f9fa" stroke="#b5c0c8" stroke-width="4"/><rect x="236" y="70" width="128" height="62" rx="8" fill="#14202B"/><text x="300" y="112" text-anchor="middle" font-family="monospace" font-size="30" fill="#7ee08a">58°C</text><circle cx="258" cy="180" r="22" fill="#d8341e"/><circle cx="342" cy="180" r="22" fill="#2a6fd8"/><rect x="250" y="236" width="100" height="14" rx="7" fill="#c9d1d6"/>')
    s.append('<g stroke="#c78a12" stroke-width="16" fill="none" stroke-linecap="round"><path d="M240 310V360H80"/><path d="M360 310V350H520"/></g><g stroke="#d8341e" stroke-width="10" fill="none" stroke-linecap="round"><path d="M290 310V380H60"/></g>')
    return svg(600, 400, "".join(s))

def tile(seed, c1, c2, glyph):
    R = random.Random(seed); s = [f'<defs><linearGradient id="t{seed}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect width="400" height="400" fill="url(#t{seed})"/>']
    for _ in range(6): s.append('<circle cx="%d" cy="%d" r="%d" fill="#fff" opacity="%.2f"/>' % (R.randint(0, 400), R.randint(0, 400), R.randint(30, 140), R.uniform(.04, .12)))
    s.append(glyph)
    return svg(400, 400, "".join(s))

BK_CSS = '''
.bk{display:grid;gap:14px}.bk h3{margin:0}.bk .lab{font-size:12.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--bkm,var(--mut));margin-bottom:6px;display:block}
.bk .chips{display:flex;gap:8px;flex-wrap:wrap}.bk button.c{font:700 14px inherit;font-family:inherit;padding:10px 14px;border-radius:12px;border:1.5px solid var(--bkl,var(--line));background:transparent;color:inherit;cursor:pointer;min-width:46px}
.bk button.c.on{background:var(--acc);color:var(--acct);border-color:var(--acc)}.bk button.c[disabled]{text-decoration:line-through;opacity:.4;border-style:dashed;cursor:not-allowed}
.bk .d{display:grid;line-height:1.15;text-align:center;font-size:13px}.bk .d small{font-weight:500;opacity:.75}
.bk input,.bk select,.bk textarea{width:100%;font:500 15px inherit;font-family:inherit;padding:12px 14px;border-radius:12px;border:1.5px solid var(--bkl,var(--line));background:transparent;color:inherit}
.bk textarea{min-height:84px}.bk .row2{display:grid;grid-template-columns:1fr 1fr;gap:10px}.bk .go{border:0;cursor:pointer;font-family:inherit}
.bk .ok{display:none;padding:18px;border-radius:14px;background:var(--acc);color:var(--acct)}.bk .ok b{display:block;font-size:1.15rem;margin-bottom:4px}.bk.done .ok{display:block}.bk.done .f{display:none!important}
.bk .err{color:#ff8a7a;font-size:13px;min-height:18px}.bk small.n{font-size:12.5px;opacity:.7}
'''
BK_JS = '''<script>
(function(){
function pad(n){return n<10?'0'+n:''+n}
function hash(s){var h=0;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return Math.abs(h)}
var MOIS=['janv.','févr.','mars','avr.','mai','juin','juil.','août','sept.','oct.','nov.','déc.'],JOURS=['dim','lun','mar','mer','jeu','ven','sam'];
document.querySelectorAll('.bk[data-mode]').forEach(function(bk){
  var closed=(bk.dataset.closed||'').split(',').filter(Boolean).map(Number),slots=bk.dataset.slots.split(',');
  var day=null,slot=null,days=[],now=new Date();now.setHours(12,0,0,0);
  for(var i=0;days.length<7&&i<30;i++){var d=new Date(now.getTime()+(i+(bk.dataset.today?0:1))*864e5);if(closed.indexOf(d.getDay())<0)days.push(d)}
  var dEl=bk.querySelector('.days'),sEl=bk.querySelector('.slotz'),err=bk.querySelector('.err');
  function key(d){return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate())}
  function label(d){return JOURS[d.getDay()]+' '+d.getDate()+' '+MOIS[d.getMonth()]}
  function drawDays(){dEl.innerHTML='';days.forEach(function(d,i){var b=document.createElement('button');b.type='button';b.className='c d'+(day===i?' on':'');b.innerHTML=JOURS[d.getDay()]+'<small>'+d.getDate()+' '+MOIS[d.getMonth()]+'</small>';b.onclick=function(){day=i;slot=null;drawDays();drawSlots()};dEl.appendChild(b)})}
  function drawSlots(){sEl.innerHTML='';if(day===null){sEl.innerHTML='<small class="n">Choisissez d’abord un jour.</small>';return}
    slots.forEach(function(h){var b=document.createElement('button');b.type='button';b.className='c'+(slot===h?' on':'');b.textContent=h.replace(':',' h ').replace(' h 00',' h');
      if(hash(key(days[day])+h)%4===0)b.disabled=true;b.onclick=function(){slot=h;drawSlots()};sEl.appendChild(b)})}
  drawDays();drawSlots();
  bk.querySelector('.go').onclick=function(){
    var nom=bk.querySelector('[name=nom]').value.trim(),tel=bk.querySelector('[name=tel]').value.trim();
    if(day===null||!slot){err.textContent='Choisissez un jour et une heure.';return}
    if(nom.length<2){err.textContent='Indiquez votre nom.';return}
    err.textContent='';var opt=bk.querySelector('[name=opt]');var o=opt?(opt.tagName==='SELECT'?opt.options[opt.selectedIndex].text:opt.value):'';
    bk.querySelector('.ok').innerHTML='<b>Réservation confirmée</b>'+label(days[day])+' à '+slot.replace(':',' h ').replace(' h 00',' h')+(o?' · '+o:'')+'<br>Merci '+nom.replace(/</g,'')+(tel?', nous vous rappelons au '+tel.replace(/</g,''):'')+'. <small class="n">(Démonstration : rien n’est enregistré.)</small>';
    bk.classList.add('done')};
});
document.querySelectorAll('form.quote').forEach(function(f){f.onsubmit=function(e){e.preventDefault();
  var n=f.querySelector('[name=nom]').value.trim(),t=f.querySelector('[name=tel]').value.trim(),er=f.querySelector('.err');
  if(n.length<2||t.length<8){er.textContent='Indiquez votre nom et un téléphone valide.';return}
  f.innerHTML='<div class="ok" style="display:block"><b>Demande envoyée</b>Merci '+n.replace(/</g,'')+', nous vous rappelons sous 48 h pour fixer la visite. <small class="n">(Démonstration : rien n’est enregistré.)</small></div>'}});
})();
</script>'''

# ---------- gabarit commun ----------
def page(title, desc, fonts, css, body, js=""):
    return f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}"><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&display=swap">
<style>*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0}}img,svg{{max-width:100%}}a{{color:inherit;text-decoration:none}}h1,h2,h3,h4,p,ul,figure{{margin:0;padding:0}}ul{{list-style:none}}
.demo-bar{{position:sticky;left:0;right:0;bottom:0;margin-top:40px;z-index:99;background:#111;color:#fff;font:500 12.5px/1.3 system-ui,sans-serif;padding:9px 14px;display:flex;gap:12px;justify-content:center;align-items:center;flex-wrap:wrap}}.demo-bar a{{text-decoration:underline}}
{css}{BK_CSS}.sl{{position:relative;display:block;width:100%;height:100%}}.sl img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}</style></head><body>{body}
{BK_JS}
<div class="demo-bar"><span>Exemple de site réalisé par SiteVitrine Express · noms, prix et photos fictifs</span><a href="/" target="_top">← Retour à l’offre</a></div>
{js}</body></html>'''

# ======================= BISTRO =======================
def bistro():
    css = '''
:root{--bg:#0d0f0c;--card:#15180f;--ink:#f4efe4;--mut:#b9b3a4;--gold:#e9b45f;--line:#2a2d22;--acc:#e9b45f;--acct:#1a1205}
body{background:var(--bg);color:var(--ink);font:400 16px/1.6 'DM Sans',system-ui,sans-serif;padding-bottom:50px}
.serif{font-family:'Playfair Display',Georgia,serif}.w{max-width:1180px;margin:0 auto;padding:0 24px}
header{position:absolute;inset:0 0 auto;z-index:5}header .w{display:flex;align-items:center;gap:26px;padding-block:20px}
.logo{font:italic 600 1.45rem 'Playfair Display',serif}nav{margin-left:auto;display:flex;gap:26px;font-size:14.5px}nav a{opacity:.9}
.btn{display:inline-block;padding:13px 26px;border-radius:99px;background:var(--gold);color:#1a1205;font-weight:700;font-size:14.5px;border:0}.btn.o{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1.5px #ffffff88}
.hero{position:relative;min-height:640px;display:flex;align-items:center;overflow:hidden}.hero .bg{position:absolute;inset:0}.hero .bg svg{width:100%;height:100%}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#000d 0,#000a 50%,#0004 100%)}
.hero .w{position:relative;z-index:2;padding-block:120px 80px}.hero h1{font:italic 600 clamp(3rem,7vw,5.6rem)/1 'Playfair Display',serif;max-width:9ch}
.hero p{max-width:440px;margin:18px 0 28px;color:#e9e3d4;font-size:17px}.hero .cta{display:flex;gap:12px;flex-wrap:wrap}
.hero .badge{margin-top:34px;display:flex;gap:22px;font-size:13px;color:#ddd;flex-wrap:wrap}.hero .badge b{color:var(--gold);font-size:20px;display:block}
section{padding-block:70px}.eb{font:700 11.5px 'DM Sans';letter-spacing:.2em;text-transform:uppercase;color:var(--gold)}
h2{font:italic 600 clamp(2rem,4vw,3rem)/1.1 'Playfair Display',serif;margin-top:10px}
.about{display:grid;grid-template-columns:1.05fr 1fr;gap:56px;align-items:center}.about p{color:var(--mut);margin-top:16px}.about .img{border-radius:20px;overflow:hidden;aspect-ratio:4/5;position:relative}.about .img svg{width:100%;height:100%;display:block}
.sig{display:flex;gap:30px;margin-top:26px}.sig b{font:600 2rem 'Playfair Display',serif;color:var(--gold);display:block}.sig span{font-size:13px;color:var(--mut)}
.menu{background:#101309}.tabs{display:flex;gap:8px;margin:26px 0;flex-wrap:wrap}.tabs button{background:transparent;border:1.5px solid var(--line);color:var(--ink);padding:9px 18px;border-radius:99px;font:600 14px 'DM Sans';cursor:pointer}.tabs button.on{background:var(--gold);color:#1a1205;border-color:var(--gold)}
.dishes{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}.dish{background:var(--card);border-radius:18px;overflow:hidden;border:1px solid var(--line)}.dish .im{aspect-ratio:1;overflow:hidden}.dish .im svg{width:100%;height:100%;display:block}
.dish div.t{padding:16px}.dish h3{font:600 1.15rem 'Playfair Display',serif}.dish p{font-size:13.5px;color:var(--mut);margin-top:4px}.dish .pr{display:flex;justify-content:space-between;margin-top:10px;font-weight:700;color:var(--gold)}.dish .pr small{color:var(--mut);font-weight:400}
.formule{margin-top:26px;display:flex;justify-content:space-between;gap:18px;align-items:center;background:linear-gradient(100deg,#2a1d0b,#1a1408);border:1px solid #5a4217;border-radius:18px;padding:22px 26px;flex-wrap:wrap}.formule b{font:italic 600 1.5rem 'Playfair Display',serif}
.gal{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:190px;gap:12px;margin-top:28px}.gal figure{border-radius:16px;overflow:hidden}.gal svg{width:100%;height:100%;display:block}.gal .big{grid-column:span 2;grid-row:span 2}
.rev{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px}.rev blockquote{margin:0;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:22px}.rev .st{color:var(--gold);letter-spacing:3px}.rev p{margin:10px 0 14px;color:#e8e2d3}.rev cite{font-style:normal;font-size:13px;color:var(--mut)}
.res{display:grid;grid-template-columns:1fr 1fr;gap:26px}.box{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:26px}.hrs li{display:flex;justify-content:space-between;padding:9px 0;border-top:1px solid var(--line);font-size:15px}.hrs li:first-child{border:0}.hrs .c{color:#8b8575}
.slots{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}.slots span{padding:9px 14px;border-radius:12px;border:1.5px solid #3b3a2e;font-weight:700;font-size:14px}.slots span.on{background:var(--gold);color:#1a1205;border-color:var(--gold)}.slots span.x{text-decoration:line-through;color:#6a675c;border-style:dashed}
.map{margin-top:16px;border-radius:14px;height:150px;background:#1b2417;position:relative;overflow:hidden}.map:before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(35deg,transparent 0 38px,#2c3a25 38px 42px),repeating-linear-gradient(-55deg,transparent 0 56px,#2c3a25 56px 59px)}.map i{position:absolute;left:50%;top:44%;width:20px;height:20px;border-radius:50% 50% 50% 0;background:var(--gold);transform:rotate(-45deg)}
footer{border-top:1px solid var(--line);padding-block:30px;color:var(--mut);font-size:14px}footer .w{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
@media(max-width:900px){nav{display:none}.dishes,.gal{grid-template-columns:repeat(2,1fr)}.about,.res,.rev{grid-template-columns:1fr}.hero{min-height:560px}.hero:after{background:#0008}.gal .big{grid-column:span 2}}
'''
    dishes = {
        "Entrées": [("Velouté de potimarron", "Éclats de noisette, crème d’échalote", "9 €", "soupe", 1), ("Salade de chèvre chaud", "Miel de lavande, noix, croûtons", "11 €", "salade", 2), ("Tartare de saison", "Légumes croquants, vinaigrette citron", "12 €", "salade", 3), ("Œuf parfait", "Crème de cèpes, copeaux de parmesan", "10 €", "risotto", 4)],
        "Plats": [("Onglet de bœuf, échalotes", "Frites maison, sauce au poivre", "22 €", "viande", 5), ("Magret de canard rôti", "Purée de patate douce, jus corsé", "24 €", "viande", 6), ("Risotto aux champignons", "Parmesan 24 mois, huile de truffe", "19 €", "risotto", 7), ("Pavé de cabillaud", "Légumes de saison, beurre blanc", "23 €", "poisson", 8)],
        "Desserts": [("Fondant au chocolat", "Cœur coulant, crème anglaise", "9 €", "dessert", 9), ("Tarte fine aux pommes", "Caramel beurre salé, glace vanille", "8 €", "tarte", 10), ("Crème brûlée", "Vanille de Madagascar", "7 €", "creme", 11), ("Café gourmand", "Trois mignardises du jour", "9 €", "cafe", 12)],
    }
    panels = ""
    for i, (cat, items) in enumerate(dishes.items()):
        cards = "".join(f'<article class="dish"><div class="im">{slot("plat-%d" % sd, plate(sd, k))}</div><div class="t"><h3>{n}</h3><p>{d}</p><div class="pr"><span>{p}</span><small>fait maison</small></div></div></article>' for n, d, p, k, sd in items)
        panels += f'<div class="dishes" data-p="{i}" {"" if i == 0 else "hidden"}>{cards}</div>'
    tabs = "".join(f'<button class="{"on" if i == 0 else ""}" data-t="{i}">{c}</button>' for i, c in enumerate(dishes))
    glyph_wine = '<path d="M170 90h60l-6 120q-24 22-48 0z" fill="#fff" opacity=".85"/><rect x="196" y="210" width="8" height="80" fill="#fff" opacity=".85"/><rect x="170" y="290" width="60" height="8" rx="4" fill="#fff" opacity=".85"/>'
    glyph_cup = '<ellipse cx="200" cy="260" rx="110" ry="22" fill="#fff" opacity=".6"/><path d="M120 150h160q0 100-80 110q-80-10-80-110z" fill="#fff" opacity=".9"/><path d="M280 170q50 0 40 40t-50 30" stroke="#fff" stroke-width="12" fill="none" opacity=".9"/>'
    gal = (f'<figure class="big">{slot("bistro-salle", BISTRO_SVG)}</figure><figure>{slot("ambiance-1", tile(21,"#7a2e12","#2b0f06",glyph_wine))}</figure><figure>{slot("ambiance-2", plate(31,"dessert"))}</figure><figure>{slot("ambiance-3", tile(23,"#2f4a2a","#0e1a0e",glyph_cup))}</figure><figure>{slot("ambiance-4", plate(32,"viande"))}</figure>')
    reviews = [("Une cuisine de marché vraiment généreuse, le magret était parfait. Service chaleureux, on reviendra.", "Marion L. · Google"), ("Le cadre le soir avec les guirlandes est magique. Réservation en ligne très simple.", "Thomas B. · TripAdvisor"), ("Formule du midi à 17 € imbattable pour la qualité. Les desserts sont une tuerie.", "Sandrine P. · Google")]
    rev = "".join(f'<blockquote><div class="st">★★★★★</div><p>« {t} »</p><cite>{a}</cite></blockquote>' for t, a in reviews)
    body = f'''<header><div class="w"><a class="logo" href="#top">Le Bistro du Marché</a><nav><a href="#carte">La carte</a><a href="#maison">La maison</a><a href="#galerie">Galerie</a><a href="#avis">Avis</a><a href="#contact">Réserver</a></nav><a class="btn" href="#contact">Réserver une table</a></div></header>
<main id="top"><div class="hero"><div class="bg">{slot("bistro-hero", BISTRO_SVG)}</div><div class="w"><p class="eb">Restaurant · Cuisine de marché</p><h1>Le Bistro du Marché</h1><p>Une cuisine généreuse, des produits des producteurs voisins et des vins de vignerons, servis sous les guirlandes de la terrasse.</p><div class="cta"><a class="btn" href="#contact">Réserver une table</a><a class="btn o" href="#carte">Voir la carte</a></div><div class="badge"><span><b>4,8 ★</b>412 avis</span><span><b>17 €</b>formule midi</span><span><b>Terrasse</b>chauffée</span></div></div></div>
<section id="maison"><div class="w about"><div><p class="eb">La maison</p><h2>Du marché à l’assiette, chaque jour</h2><p>Depuis 2014, Camille et son équipe cuisinent ce que le marché leur apporte le matin. La carte change avec les saisons, les fournisseurs sont à moins de 80 km, et tout est préparé sur place.</p><p>Le soir, la terrasse s’allume sous les guirlandes : on y vient pour un verre, un dîner en amoureux ou une grande tablée entre amis.</p><div class="sig"><div><b>10 ans</b><span>de cuisine maison</span></div><div><b>12</b><span>producteurs locaux</span></div><div><b>45</b><span>couverts en salle</span></div></div></div><div class="img">{slot("bistro-maison", marche())}</div></div></section>
<section class="menu" id="carte"><div class="w"><p class="eb">La carte</p><h2>Cuisine de saison</h2><div class="tabs">{tabs}</div>{panels}<div class="formule"><div><b>Formule du midi · 17 €</b><p style="color:var(--mut);font-size:14px">Entrée + plat ou plat + dessert, du mardi au vendredi.</p></div><a class="btn" href="#contact">Réserver</a></div></div></section>
<section id="galerie"><div class="w"><p class="eb">Galerie</p><h2>L’ambiance du Bistro</h2><div class="gal">{gal}</div></div></section>
<section id="avis" style="background:#101309"><div class="w"><p class="eb">Ils en parlent</p><h2>Des clients conquis</h2><div class="rev">{rev}</div></div></section>
<section id="contact"><div class="w"><p class="eb">Réservation et accès</p><h2>Réservez votre table</h2><div class="res" style="margin-top:26px"><div class="box"><div class="bk" data-mode="table" data-closed="1" data-slots="12:00,12:30,13:00,13:30,19:00,19:30,20:00,20:30,21:00"><h3 class="serif" style="font-size:1.4rem">Réserver une table</h3><div class="f" style="display:grid;gap:14px"><div><span class="lab">Couverts</span><select name="opt"><option>2 personnes</option><option>3 personnes</option><option>4 personnes</option><option>5 personnes</option><option>6 personnes</option><option>7 personnes</option><option>8 personnes</option></select></div><div><span class="lab">Jour</span><div class="chips days"></div></div><div><span class="lab">Heure</span><div class="chips slotz"></div></div><div class="row2"><input name="nom" placeholder="Prénom et nom" autocomplete="off"><input name="tel" placeholder="Téléphone" inputmode="tel" autocomplete="off"></div><div class="err" role="alert"></div><button class="btn go" type="button">Confirmer la réservation</button><small class="n">Confirmation immédiate · annulation gratuite jusqu’à 2 h avant.</small></div><div class="ok"></div></div></div>
<div class="box"><h3 class="serif" style="font-size:1.4rem">Horaires</h3><ul class="hrs" style="margin-top:8px"><li><span>Lundi</span><span class="c">Fermé</span></li><li><span>Mardi – Vendredi</span><span>12 h – 14 h 30 · 19 h – 22 h 30</span></li><li><span>Samedi</span><span>12 h – 15 h · 19 h – 23 h</span></li><li><span>Dimanche</span><span>12 h – 15 h</span></li></ul><p style="margin-top:12px;color:var(--mut);font-size:14px">12 rue du Marché, 69003 Lyon · 04 00 00 00 00</p><div class="map"><i></i></div></div></div></div></section></main>
<footer><div class="w"><span>© 2026 Le Bistro du Marché</span><span>Instagram · Facebook · Mentions légales</span></div></footer>'''
    js = '''<script>document.querySelectorAll('.tabs button').forEach(function(b){b.onclick=function(){document.querySelectorAll('.tabs button').forEach(function(x){x.classList.toggle('on',x===b)});document.querySelectorAll('.dishes').forEach(function(d){d.hidden=d.dataset.p!==b.dataset.t})}})</script>'''
    return page("Le Bistro du Marché · Restaurant", "Exemple de site restaurant", "family=DM+Sans:wght@400;500;700&family=Playfair+Display:ital,wght@0,600;1,600", css, body, js)

# ======================= SALON =======================
def salon():
    css = '''
:root{--bg:#f6f1ea;--ink:#1f2a24;--mut:#68716b;--sage:#2f4a3c;--clay:#d98e73;--line:#e2d9cc;--card:#fffdf9;--acc:#2f4a3c;--acct:#fff}
body{background:var(--bg);color:var(--ink);font:400 16px/1.6 'Manrope',system-ui,sans-serif;padding-bottom:50px}.w{max-width:1180px;margin:0 auto;padding:0 24px}
.disp{font-family:'Fraunces',Georgia,serif}header{position:sticky;top:0;z-index:5;background:#f6f1eacc;backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}header .w{display:flex;align-items:center;gap:24px;padding-block:14px}
.logo{font:600 1.4rem 'Fraunces',serif}.logo i{color:var(--clay)}nav{margin-left:auto;display:flex;gap:26px;font-size:14.5px;font-weight:500}
.btn{display:inline-block;padding:13px 24px;border-radius:99px;background:var(--sage);color:#fff;font-weight:700;font-size:14.5px}.btn.o{background:transparent;color:var(--sage);box-shadow:inset 0 0 0 1.5px var(--sage)}
.hero{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center;padding-block:60px 70px}.hero h1{font:600 clamp(2.8rem,6vw,4.9rem)/1 'Fraunces',serif;letter-spacing:-.02em}.hero h1 em{color:var(--clay);font-style:italic}
.hero p.l{max-width:470px;margin:20px 0 28px;color:var(--mut);font-size:17px}.cta{display:flex;gap:12px;flex-wrap:wrap}.meta{display:flex;gap:28px;margin-top:34px;font-size:13px;color:var(--mut);flex-wrap:wrap}.meta b{display:block;font:600 1.5rem 'Fraunces',serif;color:var(--ink)}
.imgs{position:relative;height:520px}.imgs .a{position:absolute;right:0;top:0;width:68%;height:86%;border-radius:200px 200px 24px 24px;overflow:hidden}.imgs .b{position:absolute;left:0;bottom:0;width:46%;height:46%;border-radius:24px;overflow:hidden;border:6px solid var(--bg)}.imgs svg{width:100%;height:100%;display:block}
.pill{position:absolute;left:4%;top:10%;background:var(--card);padding:12px 16px;border-radius:16px;box-shadow:0 14px 30px #0002;font-size:13px}.pill b{display:block;font-size:15px}
section{padding-block:64px}.eb{font:800 11.5px 'Manrope';letter-spacing:.18em;text-transform:uppercase;color:var(--clay)}h2{font:600 clamp(1.9rem,3.6vw,2.8rem)/1.1 'Fraunces',serif;margin-top:8px}
.tarifs{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px}.tc{background:var(--card);border:1px solid var(--line);border-radius:22px;padding:24px}.tc h3{font:600 1.3rem 'Fraunces',serif;margin-bottom:6px}.tc li{display:flex;justify-content:space-between;gap:10px;padding:11px 0;border-top:1px dashed var(--line);font-size:15px}.tc li small{display:block;color:var(--mut);font-size:12.5px}.tc li b{color:var(--sage);white-space:nowrap}
.team{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:28px}.m{border-radius:22px;overflow:hidden;background:var(--card);border:1px solid var(--line)}.m .ph{aspect-ratio:4/5}.m svg{width:100%;height:100%;display:block}.m div.t{padding:14px 16px}.m h3{font:600 1.1rem 'Fraunces',serif}.m span{font-size:13px;color:var(--mut)}
.band{background:var(--sage);color:#f3efe6}.band .eb{color:#f0b9a5}.sg{display:grid;grid-template-columns:1.4fr 1fr;gap:16px;margin-top:26px;height:380px}.sg figure{margin:0;border-radius:22px;overflow:hidden}.sg svg{width:100%;height:100%}.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin-top:28px}.steps div{border-top:1px solid #ffffff44;padding-top:14px}.steps b{font:600 2rem 'Fraunces',serif;color:#f0b9a5}.steps p{font-size:14.5px;color:#dfe6df}
.rev{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px}.rev blockquote{margin:0;background:var(--card);border:1px solid var(--line);border-radius:22px;padding:24px}.rev .st{color:var(--clay);letter-spacing:3px}.rev p{margin:10px 0 14px}.rev cite{font-style:normal;font-size:13px;color:var(--mut)}
.res{display:grid;grid-template-columns:1.1fr .9fr;gap:22px;margin-top:28px}.box{background:var(--card);border:1px solid var(--line);border-radius:22px;padding:26px}.cal{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin:14px 0}.cal span{padding:10px 0;text-align:center;border-radius:12px;border:1.5px solid var(--line);font-size:13px;font-weight:700}.cal small{display:block;font-weight:500;color:var(--mut)}.cal .on{background:var(--sage);border-color:var(--sage);color:#fff}.cal .on small{color:#d6e2da}
.slots{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px}.slots span{padding:9px 14px;border-radius:12px;border:1.5px solid var(--line);font-weight:700;font-size:14px}.slots .on{background:var(--clay);color:#fff;border-color:var(--clay)}.slots .x{text-decoration:line-through;color:#aaa;border-style:dashed}
.hrs li{display:flex;justify-content:space-between;padding:9px 0;border-top:1px solid var(--line);font-size:15px}.hrs li:first-child{border:0}
footer{border-top:1px solid var(--line);padding-block:30px;color:var(--mut);font-size:14px}footer .w{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
@media(max-width:900px){.sg{grid-template-columns:1fr;height:auto}.sg figure{height:240px}nav{display:none}.hero,.res{grid-template-columns:1fr}.tarifs,.rev{grid-template-columns:1fr}.team,.steps{grid-template-columns:repeat(2,1fr)}.imgs{height:420px}}
'''
    def tc(title, rows): return f'<div class="tc"><h3>{title}</h3><ul>' + "".join(f'<li><span>{n}<small>{d}</small></span><b>{p}</b></li>' for n, d, p in rows) + '</ul></div>'
    tarifs = tc("Coupes", [("Coupe femme", "Shampoing, coupe, coiffage · 45 min", "38 €"), ("Coupe homme", "Shampoing, coupe · 30 min", "24 €"), ("Coupe enfant", "Moins de 12 ans · 30 min", "16 €"), ("Brushing", "Sur cheveux mi-longs · 30 min", "26 €")]) + tc("Couleurs", [("Racines", "Coloration + soin · 1 h 15", "55 €"), ("Couleur complète", "Longueur et pointes · 1 h 45", "68 €"), ("Balayage", "Technique à la main · 2 h 30", "dès 90 €"), ("Patine / gloss", "Brillance et reflets · 30 min", "28 €")]) + tc("Soins", [("Soin profond", "Masque + massage crânien · 30 min", "24 €"), ("Lissage kératine", "Effet 3 mois · 2 h 30", "dès 120 €"), ("Chignon / mariée", "Essai inclus · 1 h", "dès 70 €"), ("Barbe", "Taille et contours · 20 min", "14 €")])
    team = "".join(f'<div class="m"><div class="ph">{slot("equipe-%d" % sd, hair(sd, c1, c2, b1, b2))}</div><div class="t"><h3>{n}</h3><span>{r}</span></div></div>' for sd, c1, c2, b1, b2, n, r in [(41, "#3b2418", "#7a4a2c", "#e8d4c0", "#c99d82", "Thomas", "Coupe homme et barbe"), (42, "#d8b36a", "#f2dca0", "#d7e1d8", "#9db7a6", "Élodie", "Fondatrice · coloriste"), (43, "#8c3a1d", "#d9693a", "#f1d9cf", "#d98e73", "Lucas", "Coupe et balayage"), (44, "#1c1512", "#4a3a30", "#cfd6dc", "#8c9aa5", "Sophie", "Soins et chignons")])
    reviews = [("Élodie a compris exactement ce que je voulais. Mon balayage est lumineux, naturel. Je n’irai plus ailleurs.", "Camille R. · Google"), ("Salon apaisant, produits qui sentent bon, et la réservation en ligne m’évite d’appeler.", "Julie M. · Google"), ("Mon fils adore Thomas. Coupe nette à chaque fois et toujours à l’heure.", "Karim D. · Google")]
    rev = "".join(f'<blockquote><div class="st">★★★★★</div><p>« {t} »</p><cite>{a}</cite></blockquote>' for t, a in reviews)
    steps = "".join(f'<div><b>0{i+1}</b><p><strong>{t}</strong><br>{d}</p></div>' for i, (t, d) in enumerate([("Choisissez", "Votre prestation et sa durée."), ("Réservez", "Un créneau libre, en 30 secondes."), ("Confirmation", "Vous recevez le récapitulatif."), ("Détendez-vous", "On s’occupe du reste.")]))
    body = f'''<header><div class="w"><a class="logo" href="#top">Maison <i>Olive</i></a><nav><a href="#tarifs">Tarifs</a><a href="#equipe">L’équipe</a><a href="#avis">Avis</a><a href="#rdv">Rendez-vous</a></nav><a class="btn" href="#rdv">Prendre rendez-vous</a></div></header>
<main id="top"><div class="w hero"><div><p class="eb">Salon de coiffure · Bordeaux Chartrons</p><h1>Des cheveux qui vous <em>ressemblent</em>.</h1><p class="l">Coupes, couleurs et soins dans un salon lumineux, avec ou sans rendez-vous. Des produits végétaux et une équipe qui prend le temps.</p><div class="cta"><a class="btn" href="#rdv">Prendre rendez-vous</a><a class="btn o" href="#tarifs">Voir les tarifs</a></div><div class="meta"><span><b>4,9 ★</b>286 avis</span><span><b>Du mardi au samedi</b>9 h – 18 h</span><span><b>Produits</b>végétaux</span></div></div>
<div class="imgs"><div class="a">{slot("salon-hero", hair(40,"#7a3a1c","#d98a4a","#f1d9cf","#d98e73"))}</div><div class="b">{slot("salon-interieur", tile(9,"#2f4a3c","#14241b",'<g fill="none" stroke="#f3efe6" stroke-width="10" stroke-linecap="round"><circle cx="150" cy="260" r="40"/><circle cx="250" cy="260" r="40"/><path d="M180 232L300 90M220 232L100 90"/></g>'))}</div><div class="pill"><b>Ouvert aujourd’hui</b>jusqu’à 18 h</div></div></div>
<section id="tarifs"><div class="w"><p class="eb">Prestations et tarifs</p><h2>Des prix clairs, affichés d’avance</h2><div class="tarifs">{tarifs}</div></div></section>
<section id="equipe" style="padding-top:0"><div class="w"><p class="eb">L’équipe</p><h2>Quatre coiffeurs passionnés</h2><div class="team">{team}</div></div></section>
<section style="padding-top:0"><div class="w"><p class="eb">Le salon</p><h2>Un lieu lumineux, des mains expertes</h2><div class="sg"><figure class="sg1">{slot("salon-interieur", tile(9,"#2f4a3c","#14241b",""))}</figure><figure>{slot("salon-coloriste", tile(10,"#d98e73","#7a3a1c",""))}</figure></div></div></section>
<section class="band"><div class="w"><p class="eb">Comment ça se passe</p><h2>Réserver prend 30 secondes</h2><div class="steps">{steps}</div></div></section>
<section id="avis"><div class="w"><p class="eb">Avis clients</p><h2>Ce qu’en disent nos clientes</h2><div class="rev">{rev}</div></div></section>
<section id="rdv" style="padding-top:0"><div class="w"><p class="eb">Rendez-vous</p><h2>Choisissez votre créneau</h2><div class="res"><div class="box"><div class="bk" data-mode="service" data-closed="0,1" data-slots="09:00,09:30,10:15,11:00,11:45,14:00,14:45,15:30,16:30,17:15"><h3 class="disp" style="font-size:1.3rem">Prendre rendez-vous</h3><div class="f" style="display:grid;gap:14px"><div><span class="lab">Prestation</span><select name="opt"><option>Coupe femme · 45 min · 38 €</option><option>Coupe homme · 30 min · 24 €</option><option>Brushing · 30 min · 26 €</option><option>Couleur racines · 1 h 15 · 55 €</option><option>Balayage · 2 h 30 · dès 90 €</option></select></div><div><span class="lab">Jour</span><div class="chips days"></div></div><div><span class="lab">Heure</span><div class="chips slotz"></div></div><div class="row2"><input name="nom" placeholder="Prénom" autocomplete="off"><input name="tel" placeholder="Téléphone" inputmode="tel" autocomplete="off"></div><div class="err" role="alert"></div><button class="btn go" type="button">Confirmer mon rendez-vous</button></div><div class="ok"></div></div></div>
<div class="box"><h3 class="disp" style="font-size:1.3rem">Horaires et accès</h3><ul class="hrs" style="margin-top:8px"><li><span>Lundi</span><span>Fermé</span></li><li><span>Mardi – Vendredi</span><span>9 h – 12 h · 14 h – 18 h</span></li><li><span>Samedi</span><span>9 h – 17 h</span></li></ul><p style="margin-top:12px;color:var(--mut);font-size:14px">18 cours Journu-Auber, 33300 Bordeaux<br>05 00 00 00 00 · Tram C, arrêt Chartrons</p></div></div></div></section></main>
<footer><div class="w"><span>© 2026 Maison Olive</span><span>Instagram · Mentions légales</span></div></footer>'''
    return page("Maison Olive · Salon de coiffure", "Exemple de site salon de coiffure", "family=Manrope:wght@400;500;700;800&family=Fraunces:ital,opsz,wght@0,9..144,600;1,9..144,600", css, body)

# ======================= ARTISAN =======================
def artisan():
    css = '''
:root{--bg:#f3f5f7;--ink:#14202b;--mut:#5b6875;--y:#f2a900;--line:#d5dce3;--card:#fff}
body{background:var(--bg);color:var(--ink);font:400 16px/1.55 'Inter',system-ui,sans-serif;padding-bottom:50px}.w{max-width:1180px;margin:0 auto;padding:0 24px}
.cond{font-family:'Barlow Condensed',Impact,sans-serif;text-transform:uppercase}
.top{background:var(--ink);color:#fff;font-size:13px}.top .w{display:flex;justify-content:space-between;gap:12px;padding-block:8px;flex-wrap:wrap}.top b{color:var(--y)}
header{background:#fff;border-bottom:3px solid var(--y);position:sticky;top:0;z-index:5}header .w{display:flex;align-items:center;gap:24px;padding-block:14px}.logo{font:800 1.9rem/1 'Barlow Condensed';text-transform:uppercase}.logo i{color:var(--y);font-style:normal}nav{margin-left:auto;display:flex;gap:24px;font-weight:600;font-size:14.5px}
.btn{display:inline-block;padding:14px 26px;background:var(--y);color:var(--ink);font:800 1.05rem 'Barlow Condensed';letter-spacing:.04em;text-transform:uppercase;border-radius:3px}.btn.d{background:var(--ink);color:#fff}
.hero{background:var(--ink);color:#fff;position:relative;overflow:hidden}.hero .w{display:grid;grid-template-columns:1.1fr .9fr;gap:30px;align-items:center;padding-block:56px}.hero h1{font:800 clamp(3rem,6.4vw,5.4rem)/.92 'Barlow Condensed';text-transform:uppercase}.hero h1 span{color:var(--y)}
.hero p{max-width:480px;margin:18px 0 26px;color:#c9d3dc;font-size:17px}.hero .img{border-radius:6px;overflow:hidden;border:3px solid var(--y);aspect-ratio:3/2}.hero .img svg{width:100%;height:100%;display:block}
.stats{display:grid;grid-template-columns:repeat(4,1fr);background:var(--y)}.stats div{padding:20px;border-right:2px solid #14202b33;text-align:center}.stats div:last-child{border:0}.stats b{font:800 2.5rem/1 'Barlow Condensed'}.stats span{display:block;font-size:12.5px;font-weight:600;text-transform:uppercase;letter-spacing:.06em}
section{padding-block:60px}.eb{font:700 13px 'Inter';letter-spacing:.16em;text-transform:uppercase;color:var(--mut)}h2{font:800 clamp(2.2rem,4vw,3.2rem)/1 'Barlow Condensed';text-transform:uppercase;margin-top:8px}
.serv{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px}.sv{background:var(--card);border:1px solid var(--line);border-top:5px solid var(--y);padding:22px}.sv h3{font:800 1.5rem 'Barlow Condensed';text-transform:uppercase}.sv p{font-size:14.5px;color:var(--mut);margin:6px 0 12px}.sv li{font-size:14px;padding:5px 0 5px 20px;position:relative}.sv li:before{content:"";position:absolute;left:0;top:11px;width:9px;height:9px;background:var(--y)}
.proj{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px}.pj{background:var(--card);border:1px solid var(--line)}.pj .ph{aspect-ratio:3/2;overflow:hidden}.pj svg{width:100%;height:100%;display:block}.pj div.t{padding:16px}.pj h3{font:800 1.35rem 'Barlow Condensed';text-transform:uppercase}.pj span{font-size:13px;color:var(--mut)}.pj .tag{display:inline-block;background:var(--ink);color:#fff;padding:2px 8px;font-size:11.5px;margin-top:8px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:28px}.box{background:var(--card);border:1px solid var(--line);padding:26px}.tb li{display:flex;justify-content:space-between;gap:12px;padding:11px 0;border-bottom:1px dashed #14202b55;font:500 14.5px 'IBM Plex Mono',monospace}.tb li:first-child{padding-top:0}
.form{display:grid;gap:12px;margin-top:14px}.form div{border:1.5px solid var(--line);padding:12px 14px;color:#8a95a0;font-size:14.5px;background:#fafbfc}
.urg{background:var(--ink);color:#fff;padding:20px 26px;display:flex;justify-content:space-between;gap:16px;align-items:center;flex-wrap:wrap;margin-top:26px;border-left:8px solid var(--y)}.urg b{font:800 1.8rem 'Barlow Condensed';text-transform:uppercase}
.rev{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px}.rev blockquote{margin:0;background:var(--card);border:1px solid var(--line);padding:22px}.rev .st{color:var(--y);letter-spacing:3px}.rev p{margin:8px 0 12px}.rev cite{font-style:normal;font-size:13px;color:var(--mut)}
.lab{display:flex;gap:14px;flex-wrap:wrap;margin-top:22px}.lab span{border:2px solid var(--ink);padding:8px 14px;font:800 1rem 'Barlow Condensed';text-transform:uppercase}
footer{background:var(--ink);color:#aeb9c4;padding-block:30px;font-size:14px}footer .w{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
@media(max-width:900px){nav{display:none}.hero .w,.grid2{grid-template-columns:1fr}.serv,.proj,.rev{grid-template-columns:1fr}.stats{grid-template-columns:repeat(2,1fr)}}
'''
    serv = [("Plomberie", "Dépannage et installation, 7 j/7.", ["Fuites et débouchage", "Chauffe-eau, ballon", "Robinetterie, WC", "Recherche de fuite"]), ("Chauffage", "Chaudières et pompes à chaleur.", ["Entretien annuel", "Remplacement chaudière", "Radiateurs, plancher chauffant", "Dossier MaPrimeRénov’"]), ("Salle de bains", "Du plan à la dernière joint.", ["Douche à l’italienne", "Carrelage, faïence", "Meubles vasque", "Accessibilité PMR"])]
    sv = "".join(f'<div class="sv"><h3>{t}</h3><p>{d}</p><ul>' + "".join(f"<li>{i}</li>" for i in it) + '</ul></div>' for t, d, it in serv)
    projs = [(bathroom(), "Salle de bains complète", "Lyon 6e · 4 jours", "Rénovation"), (boiler(), "Remplacement de chaudière", "Villeurbanne · 1 jour", "Chauffage"), (blueprint(2), "Extension et plomberie neuve", "Caluire · 3 semaines", "Neuf")]
    pj = "".join(f'<div class="pj"><div class="ph">{slot("chantier-%d" % i, a)}</div><div class="t"><h3>{n}</h3><span>{l}</span><br><span class="tag">{g}</span></div></div>' for i, (a, n, l, g) in enumerate(projs))
    reviews = [("Fuite réparée en 40 minutes un dimanche soir. Prix annoncé respecté, chantier propre.", "M. Garnier · Google"), ("Nouvelle salle de bains livrée dans les délais, finitions impeccables. Je recommande.", "Mme Roux · Google"), ("Devis clair, pas de surprise. Équipe ponctuelle et soigneuse.", "A. Benali · Pages Jaunes")]
    rev = "".join(f'<blockquote><div class="st">★★★★★</div><p>« {t} »</p><cite>{a}</cite></blockquote>' for t, a in reviews)
    body = f'''<div class="top"><div class="w"><span>Dépannage <b>7 j/7</b> · Intervention sous 2 h dans l’agglomération de Lyon</span><span>04 00 00 00 00</span></div></div>
<header><div class="w"><a class="logo" href="#top">Durand <i>Plomberie</i></a><nav><a href="#services">Services</a><a href="#realisations">Réalisations</a><a href="#tarifs">Tarifs</a><a href="#avis">Avis</a><a href="#devis">Devis</a></nav><a class="btn" href="#devis">Devis gratuit</a></div></header>
<main id="top"><div class="hero"><div class="w"><div><p class="eb" style="color:#9fb0bf">Plombier chauffagiste · Lyon et alentours</p><h1>Votre plombier,<br><span>sans mauvaise surprise.</span></h1><p>Dépannage urgent, chauffage, salle de bains. Devis gratuit sous 48 h, prix annoncé avant l’intervention, chantier laissé propre.</p><a class="btn" href="#devis">Demander un devis</a> <a class="btn d" href="#urgence" style="box-shadow:inset 0 0 0 2px #fff">Urgence fuite</a></div><div class="img">{slot("artisan-hero", bathroom())}</div></div></div>
<div class="stats"><div><b>48 h</b><span>devis gratuit</span></div><div><b>2 h</b><span>dépannage urgent</span></div><div><b>10 ans</b><span>garantie décennale</span></div><div><b>1 200+</b><span>chantiers réalisés</span></div></div>
<section id="services"><div class="w"><p class="eb">Nos métiers</p><h2>Ce que nous faisons pour vous</h2><div class="serv">{sv}</div><div class="lab"><span>RGE Qualibat</span><span>QualiPAC</span><span>Décennale incluse</span><span>Artisan depuis 2009</span></div></div></section>
<section id="realisations" style="background:#e9edf1"><div class="w"><p class="eb">Réalisations</p><h2>Des chantiers récents</h2><div class="proj">{pj}</div></div></section>
<section id="tarifs"><div class="w"><p class="eb">Tarifs indicatifs</p><h2>Des prix annoncés d’avance</h2><div class="grid2"><div class="box"><ul class="tb"><li><span>Déplacement dépannage</span><b>49 €</b></li><li><span>Débouchage canalisation</span><b>dès 120 €</b></li><li><span>Remplacement mitigeur</span><b>dès 95 €</b></li><li><span>Chauffe-eau 200 L posé</span><b>dès 890 €</b></li><li><span>Entretien chaudière</span><b>110 €</b></li><li><span>Salle de bains clé en main</span><b>sur devis</b></li></ul><p style="margin-top:12px;font-size:13px;color:var(--mut)">Prix TTC indicatifs, devis ferme avant toute intervention.</p></div>
<div class="box" id="devis"><h3 class="cond" style="font-size:1.7rem;font-weight:800">Demandez votre devis gratuit</h3><form class="quote form" style="display:grid;gap:12px;margin-top:14px"><input name="nom" placeholder="Votre nom" autocomplete="off" style="padding:13px;border:1.5px solid var(--line);font:inherit"><input name="tel" placeholder="Téléphone" inputmode="tel" autocomplete="off" style="padding:13px;border:1.5px solid var(--line);font:inherit"><select style="padding:13px;border:1.5px solid var(--line);font:inherit;background:#fff"><option>Dépannage / fuite</option><option>Chauffe-eau, chaudière</option><option>Salle de bains</option><option>Autre projet</option></select><textarea placeholder="Décrivez votre projet…" style="padding:13px;border:1.5px solid var(--line);font:inherit;min-height:80px"></textarea><div class="err" style="color:#c0301f;font-size:13px"></div><button class="btn" type="submit" style="border:0;cursor:pointer">Envoyer ma demande</button></form></div></div>
<div class="urg" id="urgence"><div><b>Fuite, panne de chauffage ?</b><p style="color:#c9d3dc">Nous intervenons en moins de 2 heures, 7 jours sur 7.</p></div><a class="btn" href="#devis">04 00 00 00 00</a></div></div></section>
<section id="avis" style="padding-top:0"><div class="w"><p class="eb">Avis clients</p><h2>Ils nous font confiance</h2><div class="rev">{rev}</div></div></section></main>
<footer><div class="w"><span>© 2026 Durand Plomberie · SIRET fictif</span><span>Mentions légales · Zone : Lyon, Villeurbanne, Caluire</span></div></footer>'''
    return page("Durand Plomberie · Plombier chauffagiste", "Exemple de site artisan", "family=Inter:wght@400;500;600;700&family=Barlow+Condensed:wght@500;700;800&family=IBM+Plex+Mono:wght@500", css, body)

for name, fn in (("bistro", bistro), ("salon", salon), ("artisan", artisan)):
    open(os.path.join(OUT, name + ".html"), "w").write(fn())
print("exemples OK")
