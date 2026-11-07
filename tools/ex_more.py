# -*- coding: utf-8 -*-
"""Trois sites d'exemple supplémentaires : fleuriste, garage auto, ostéopathe.
Chaque site a son propre langage visuel. Les emplacements photo acceptent une vraie photo : déposer assets/ex/<nom>.jpg."""
import math, random

H = {}          # rempli par examples.py : page, slot, svg, ico


# ============================================================ 2. GARAGE
def wheel(cx, cy, r=58):
    s = ['<g class="wh" style="transform-origin:%dpx %dpx">' % (cx, cy), '<circle cx="%d" cy="%d" r="%d" fill="#0a0a0b"/><circle cx="%d" cy="%d" r="%d" fill="#17181b"/>' % (cx, cy, r, cx, cy, r - 9),
         '<circle cx="%d" cy="%d" r="%d" fill="#2a2d33"/>' % (cx, cy, r - 18)]
    for k in range(5):
        a = k * 72 - 90
        x2 = cx + math.cos(math.radians(a)) * (r - 20); y2 = cy + math.sin(math.radians(a)) * (r - 20)
        s.append('<path d="M%d %d L%.1f %.1f" stroke="#c9ced6" stroke-width="7" stroke-linecap="round"/>' % (cx, cy, x2, y2))
        s.append('<path d="M%d %d L%.1f %.1f" stroke="#ffd400" stroke-width="1.6" stroke-linecap="round" opacity=".85"/>' % (cx, cy, x2, y2))
    s.append('<circle cx="%d" cy="%d" r="9" fill="#e5e8ed"/><circle cx="%d" cy="%d" r="3.5" fill="#0a0a0b"/>' % (cx, cy, cx, cy))
    s.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#3a3d44" stroke-width="2"/></g>' % (cx, cy, r - 9))
    return "".join(s)


def car_art(uid="car"):
    d = ('<defs><linearGradient id="%sb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3f48"/><stop offset=".55" stop-color="#1f2329"/><stop offset="1" stop-color="#121417"/></linearGradient>'
         '<linearGradient id="%sg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7fa0b8"/><stop offset=".5" stop-color="#2d4252"/><stop offset="1" stop-color="#111b24"/></linearGradient>'
         '<radialGradient id="%sl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffd400" stop-opacity=".55"/><stop offset="1" stop-color="#ffd400" stop-opacity="0"/></radialGradient>'
         '<filter id="%ss"><feGaussianBlur stdDeviation="8"/></filter></defs>' % (uid, uid, uid, uid))
    d += '<ellipse cx="410" cy="352" rx="330" ry="18" fill="#000" opacity=".7" filter="url(#%ss)"/>' % uid
    d += '<ellipse cx="410" cy="300" rx="380" ry="80" fill="url(#%sl)" opacity=".45"/>' % uid
    for i, y in enumerate((150, 175, 200, 232)):
        d += '<path d="M%d %d H%d" stroke="#ffd400" stroke-width="2.5" stroke-linecap="round" opacity="%.2f"/>' % (20 + i * 22, y, 80 + i * 20, .55 - i * .1)
    body = ('M86 292 L70 262 Q64 236 84 228 L150 218 Q205 214 242 160 Q262 128 300 124 L470 120 Q520 122 556 150 L640 214 Q712 220 748 244 Q770 262 764 292 L706 296 '
            'A58 58 0 0 0 594 296 L322 296 A58 58 0 0 0 206 296 Z')
    d += '<path d="%s" fill="url(#%sb)" stroke="#0a0a0b" stroke-width="2"/>' % (body, uid)
    d += '<path d="M268 164 Q286 140 310 138 L462 134 Q505 136 536 160 L608 214 L246 214 Q258 190 268 164 Z" fill="url(#%sg)" stroke="#0a0a0b" stroke-width="2"/>' % uid
    d += '<path d="M392 138 L402 214" stroke="#0a0a0b" stroke-width="5"/><path d="M286 160 Q330 150 392 150" stroke="#fff" stroke-width="2" opacity=".18" fill="none"/>'
    d += '<path d="M92 252 L750 252" stroke="#4a5059" stroke-width="1.5" opacity=".55"/><path d="M110 270 L296 270 M604 270 L728 270" stroke="#ffd400" stroke-width="5" stroke-linecap="round"/>'
    d += '<path d="M700 236 Q742 240 758 256 L710 256 Z" fill="#ffe8c2"/><path d="M700 236 Q742 240 758 256" stroke="#ffd400" stroke-width="3" fill="none"/><path d="M84 236 L110 232 L110 250 L82 250 Z" fill="#c4161c"/>'
    d += '<path d="M446 206 h38 M300 206 h38" stroke="#aab0ba" stroke-width="3" stroke-linecap="round"/>'
    d += wheel(264, 296) + wheel(650, 296)
    return d


def dial(uid="dl"):
    s = ['<defs><radialGradient id="%sr" cx=".5" cy=".5" r=".5"><stop offset=".7" stop-color="#16181c"/><stop offset="1" stop-color="#0b0c0e"/></radialGradient></defs>' % uid,
         '<circle cx="150" cy="150" r="144" fill="url(#%sr)" stroke="#3a3d44" stroke-width="3"/>' % uid]
    for i in range(41):
        a = 135 + i * 6.75; big = i % 5 == 0
        r1 = 120; r2 = 104 if big else 112
        x1 = 150 + math.cos(math.radians(a)) * r1; y1 = 150 + math.sin(math.radians(a)) * r1
        x2 = 150 + math.cos(math.radians(a)) * r2; y2 = 150 + math.sin(math.radians(a)) * r2
        col = "#ffd400" if i > 32 else "#e5e8ed"
        s.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="%d" stroke-linecap="round"/>' % (x1, y1, x2, y2, col, 3 if big else 1.5))
    s.append('<path d="M150 150 L%.1f %.1f" stroke="#ffd400" stroke-width="5" stroke-linecap="round"/>' % (150 + math.cos(math.radians(135 + 6.75 * 26)) * 96, 150 + math.sin(math.radians(135 + 6.75 * 26)) * 96))
    s.append('<circle cx="150" cy="150" r="14" fill="#e5e8ed"/><circle cx="150" cy="150" r="5" fill="#0b0c0e"/><text x="150" y="218" text-anchor="middle" font-family="Barlow Condensed,sans-serif" font-weight="700" font-size="22" letter-spacing="4" fill="#9ba1ac">KM/H</text>')
    return "".join(s)


def garage():
    page, ico = H["page"], H["ico"]
    css = r'''
:root{--bg:#050607;--p:#0c0d0f;--p2:#111316;--ink:#f4f5f7;--mut:#9ea3ab;--red:#e11d2e;--red2:#ff3b4a;--ln:#23262b}
html,body{overflow-x:clip}
body{background:var(--bg);color:var(--ink);font:400 16px/1.65 'Montserrat',system-ui,sans-serif}
.w{max-width:1200px;margin:0 auto;padding:0 28px}
.view{display:none}.view.on{display:block;animation:vin .6s cubic-bezier(.2,.8,.2,1)}@keyframes vin{from{opacity:0;transform:translateY(14px)}}
/* ---- en-tête (pages intérieures) ---- */
header.gh{position:sticky;top:0;z-index:50;background:#050607e6;backdrop-filter:blur(14px);border-bottom:1px solid var(--ln)}body.home header.gh{display:none}
header.gh .w{display:flex;align-items:center;gap:26px;height:76px}
.lg{display:block;font:300 .8rem/1.1 'Montserrat',sans-serif;letter-spacing:.5em;color:var(--mut)}.lg b{display:block;font:500 1.25rem/1.1 'Montserrat',sans-serif;letter-spacing:.2em;color:#fff;margin-top:3px}
nav.mn{display:flex;gap:6px;margin:0 auto}nav.mn a{padding:10px 18px;font:500 12.5px 'Montserrat',sans-serif;letter-spacing:.18em;text-transform:uppercase;color:var(--mut);position:relative;white-space:nowrap;transition:.25s}nav.mn a:hover{color:#fff}nav.mn a.on{color:#fff;box-shadow:inset 0 -2px 0 var(--red)}
.pill{display:inline-flex;align-items:center;gap:14px;border:2px solid var(--red);border-radius:99px;padding:14px 30px;font:600 15px 'Montserrat',sans-serif;color:#fff;background:#0000;cursor:pointer;transition:.3s;box-shadow:0 0 0 #e11d2e00}.pill:hover{background:var(--red);box-shadow:0 0 38px #e11d2e66}.pill svg{transition:.3s}.pill:hover svg{transform:translateX(5px)}
.pill.sm{padding:11px 22px;font-size:12.5px;letter-spacing:.12em;text-transform:uppercase}.pill.f{background:var(--red)}.pill.f:hover{background:var(--red2)}
.bur{display:none;margin-left:auto;background:none;border:1.5px solid var(--ln);border-radius:10px;width:46px;height:46px;color:#fff;cursor:pointer}
/* ---- accueil / hero ---- */
.hero{position:relative;min-height:100vh;min-height:100svh;display:grid;place-items:center;overflow:hidden;background:#050607;isolation:isolate}
.hero .bg{position:absolute;inset:-30px;background:url(/assets/ex/gar-hero.jpg) 62% center/cover no-repeat;z-index:-2;transition:transform .25s ease-out;will-change:transform}
.hero:after{content:"";position:absolute;inset:0;background:radial-gradient(60% 60% at 40% 50%,#0000 0,#05060766 100%);z-index:-1}
.hero .glow{position:absolute;inset:0;z-index:-1;background:radial-gradient(420px 420px at var(--mx,70%) var(--my,40%),#e11d2e22,#0000 70%);pointer-events:none}
.ht{text-align:center;padding:0 22px;transform:translateX(-4%)}
.hk{display:flex;align-items:center;justify-content:center;gap:34px}.hk:before,.hk:after{content:"";height:1px;width:clamp(30px,8vw,120px);background:#ffffffa0}
.hk span{font:300 clamp(1.4rem,3.6vw,3.2rem)/1 'Montserrat',sans-serif;letter-spacing:.55em;margin-right:-.55em;color:#fff}
.hn{font:500 clamp(2.3rem,9.4vw,7.6rem)/1 'Montserrat',sans-serif;letter-spacing:.09em;margin:22px 0 0;color:#fff;text-shadow:0 0 60px #0008}
.hs{margin:34px 0 46px;font:400 clamp(.62rem,1.45vw,1.1rem)/1.9 'Montserrat',sans-serif;letter-spacing:.34em;text-transform:uppercase;color:#d7d9dd}
.chev{position:absolute;left:50%;bottom:26px;transform:translateX(-50%);width:44px;height:44px;display:grid;place-items:center;color:#fff;animation:bob 2.2s ease-in-out infinite;border:0;background:none;cursor:pointer}@keyframes bob{50%{transform:translate(-50%,8px)}}
.hero .ht>*{opacity:0;animation:rise .9s cubic-bezier(.2,.8,.2,1) forwards}.hero .hn{animation-delay:.15s}.hero .hs{animation-delay:.3s}.hero .pill{animation-delay:.45s}@keyframes rise{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}
.hero .ht .pill{padding:20px 60px;font-size:1.18rem}
@media(prefers-reduced-motion:reduce){.hero .ht>*{animation:none;opacity:1}.chev{animation:none}}
/* ---- sections ---- */
.sec{padding:100px 0}.sec.alt{background:var(--p)}
.eb{font:500 12px/1 'Montserrat',sans-serif;letter-spacing:.38em;text-transform:uppercase;color:var(--red2)}
h2.t{font:500 clamp(1.7rem,3.6vw,2.8rem)/1.15 'Montserrat',sans-serif;letter-spacing:.04em;margin:16px 0 0}
.sub{color:var(--mut);max-width:38em;margin-top:14px}
.ph{padding:90px 0 60px;background:radial-gradient(70% 120% at 85% 0%,#e11d2e24,#0000 60%),var(--bg);border-bottom:1px solid var(--ln)}
.ph h1{font:500 clamp(2rem,5vw,3.8rem)/1.1 'Montserrat',sans-serif;letter-spacing:.06em;margin-top:18px}.ph p{color:var(--mut);max-width:40em;margin-top:16px;font-size:1.08rem}
.tri{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;margin-top:48px}
.tc{display:block;position:relative;background:var(--p2);border:1px solid var(--ln);border-radius:22px;padding:38px 32px;overflow:hidden;transition:transform .25s ease-out,border-color .3s,box-shadow .3s;transform-style:preserve-3d;will-change:transform}.tc:hover{border-color:var(--red);box-shadow:0 20px 60px #e11d2e22}
.tc:before{content:"";position:absolute;inset:0;background:radial-gradient(300px 200px at var(--px,50%) var(--py,0%),#e11d2e20,#0000 70%);opacity:0;transition:.3s}.tc:hover:before{opacity:1}
.tc .n{font:300 3.4rem/1 'Montserrat',sans-serif;color:#ffffff1c;letter-spacing:.04em}.tc h3{font:500 1.35rem/1.2 'Montserrat',sans-serif;letter-spacing:.06em;margin:18px 0 10px;transform:translateZ(30px)}.tc p{color:var(--mut);font-size:15px}.tc .go{display:inline-block;margin-top:20px;font:600 12.5px 'Montserrat',sans-serif;letter-spacing:.18em;text-transform:uppercase;color:var(--red2)}
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:2px;background:var(--ln);border:1px solid var(--ln);border-radius:20px;overflow:hidden;margin-top:56px}.stats div{background:var(--p2);padding:30px 24px;text-align:center}.stats b{display:block;font:300 2.8rem/1 'Montserrat',sans-serif;color:#fff}.stats b i{font-style:normal;color:var(--red2)}.stats span{display:block;margin-top:10px;color:var(--mut);font-size:13px;letter-spacing:.1em;text-transform:uppercase}
/* ---- prestations ---- */
.tabs{display:flex;gap:10px;flex-wrap:wrap;margin:40px 0 28px}.tab{font:500 12.5px 'Montserrat',sans-serif;letter-spacing:.16em;text-transform:uppercase;border:1.5px solid var(--ln);background:none;color:var(--mut);padding:13px 24px;border-radius:99px;cursor:pointer;transition:.25s}.tab:hover{color:#fff;border-color:#fff4}.tab.on{background:var(--red);border-color:var(--red);color:#fff}
.sv{display:block}.sv[hidden]{display:none}
.sr{display:grid;grid-template-columns:64px minmax(0,1fr) 150px 140px;gap:24px;align-items:center;padding:28px 6px;border-top:1px solid var(--ln);transition:.3s}.sr:last-child{border-bottom:1px solid var(--ln)}.sr:hover{background:#ffffff06;padding-left:18px}
.sr .no{font:300 1.9rem/1 'Montserrat',sans-serif;color:var(--red2)}.sr h3{font:500 1.2rem/1.25 'Montserrat',sans-serif;letter-spacing:.04em}.sr p{color:var(--mut);font-size:14.5px;margin-top:6px}.sr .du{color:var(--mut);font-size:13.5px}.sr .pr{text-align:right;font:500 1.4rem/1.1 'Montserrat',sans-serif}.sr .pr small{display:block;color:var(--mut);font:400 11px 'Montserrat',sans-serif;letter-spacing:.14em;text-transform:uppercase;margin-bottom:4px}
.eng{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin-top:60px}.eng div{border:1px solid var(--ln);border-radius:18px;padding:26px 22px;background:var(--p2)}.eng svg{color:var(--red2);margin-bottom:12px}.eng b{display:block;font:500 1rem 'Montserrat',sans-serif;letter-spacing:.04em;margin-bottom:6px}.eng span{color:var(--mut);font-size:14px;display:block}
/* ---- véhicules ---- */
.vg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin-top:10px}
.vc{background:var(--p2);border:1px solid var(--ln);border-radius:22px;overflow:hidden;transition:transform .25s ease-out,border-color .3s,box-shadow .3s;will-change:transform}.vc:hover{border-color:var(--red);box-shadow:0 20px 60px #e11d2e22}
.vc .im{background:radial-gradient(70% 80% at 50% 100%,#e11d2e33,#0000 70%),#0a0b0d;padding:20px 14px 0}.vc .im svg{display:block;width:100%;height:auto}
.vc{display:flex;flex-direction:column}.vc .bd{padding:24px 26px 28px;display:flex;flex-direction:column;flex:1}.vc .pf{margin-top:auto}.vc .im svg.fl{transform:scaleX(-1)}.vc .tg{font:500 11px 'Montserrat',sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--red2)}.vc h3{font:500 1.25rem/1.2 'Montserrat',sans-serif;letter-spacing:.03em;margin:8px 0 12px}
.vc ul{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}.vc li{border:1px solid var(--ln);border-radius:99px;padding:5px 13px;font-size:12.5px;color:var(--mut)}
.vc .pf{display:flex;justify-content:space-between;align-items:center;gap:12px}.vc .pf b{font:500 1.55rem 'Montserrat',sans-serif}.vc .pf a{font:600 12px 'Montserrat',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--red2);cursor:pointer}
/* ---- à propos ---- */
.dual{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}.dual img{width:100%;border-radius:22px;display:block;aspect-ratio:4/3;object-fit:cover;object-position:75% 40%;border:1px solid var(--ln)}
.dual p{color:#cfd2d8;margin-top:18px}
.team{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;margin-top:44px}.tm{border:1px solid var(--ln);border-radius:20px;padding:30px 26px;background:var(--p2)}.tm i{display:grid;place-items:center;width:64px;height:64px;border-radius:50%;border:1.5px solid var(--red);font:500 1.15rem 'Montserrat',sans-serif;font-style:normal;margin-bottom:18px}.tm b{display:block;font:500 1.1rem 'Montserrat',sans-serif;letter-spacing:.04em}.tm em{display:block;font:400 12px 'Montserrat',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--red2);font-style:normal;margin:6px 0 12px}.tm span{display:block;color:var(--mut);font-size:14.5px}
.val{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;margin-top:44px}.val div{border-left:2px solid var(--red);padding:4px 0 4px 22px}.val b{display:block;font:500 1.1rem 'Montserrat',sans-serif;letter-spacing:.04em;margin-bottom:8px}.val span{color:var(--mut);font-size:15px;display:block}
.rev{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;margin-top:44px}.rev figure{border:1px solid var(--ln);border-radius:20px;padding:28px;background:var(--p2)}.rev .st{color:var(--red2);letter-spacing:.2em}.rev blockquote{margin:12px 0 16px;color:#d4d7dc;font-size:15.5px}.rev figcaption{color:var(--mut);font-size:13px}
/* ---- contact ---- */
.cg{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:34px;align-items:start;margin-top:10px}
.rv{background:var(--p2);border:1px solid var(--ln);border-radius:24px;padding:34px}.rv h2{font:500 1.5rem 'Montserrat',sans-serif;letter-spacing:.04em;margin-bottom:6px}.rv .lab{font:500 11.5px 'Montserrat',sans-serif;letter-spacing:.22em;text-transform:uppercase;color:var(--red2);margin:26px 0 12px}
.rv .days{display:flex;gap:8px;overflow-x:auto;padding-bottom:6px}.rv .dy{flex:none;min-width:64px;border:1.5px solid var(--ln);background:none;color:#fff;border-radius:14px;padding:10px 6px;text-align:center;font:500 11.5px/1.3 'Montserrat',sans-serif;cursor:pointer;text-transform:uppercase;letter-spacing:.08em;transition:.2s}.rv .dy b{display:block;font:300 1.7rem/1.15 'Montserrat',sans-serif}.rv .dy:hover{border-color:#fff6}.rv .dy.on{background:var(--red);border-color:var(--red)}.rv .dy.full{opacity:.3;pointer-events:none}
.rv .slots{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}.rv .sl2{border:1.5px solid var(--ln);background:none;color:#fff;border-radius:12px;padding:11px 0;font:500 14px 'Montserrat',sans-serif;cursor:pointer;transition:.2s}.rv .sl2:hover{border-color:#fff6}.rv .sl2.on{background:var(--red);border-color:var(--red)}.rv .sl2.x{opacity:.3;text-decoration:line-through;pointer-events:none}
.rv form{display:grid;grid-template-columns:1fr 1fr;gap:14px}.rv label{display:grid;gap:7px;font:500 11.5px 'Montserrat',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}.rv label.w2{grid-column:1/-1}
.rv input,.rv select,.rv textarea{font:400 16px 'Montserrat',sans-serif;padding:14px 16px;border:1.5px solid var(--ln);border-radius:12px;background:#0a0b0d;color:#fff;width:100%}.rv input:focus,.rv select:focus,.rv textarea:focus{outline:0;border-color:var(--red)}.rv textarea{min-height:90px}
.rv .rec{background:#0a0b0d;border:1px solid var(--ln);border-radius:14px;padding:14px 18px;margin-bottom:6px}.rv .rec b{display:block;font:500 1rem 'Montserrat',sans-serif}.rv .rec span{color:var(--mut);font-size:14px}
.rv .go{grid-column:1/-1;margin-top:6px;background:var(--red);color:#fff;border:0;border-radius:99px;padding:18px;font:600 15px 'Montserrat',sans-serif;letter-spacing:.08em;cursor:pointer;transition:.3s}.rv .go:hover:not(:disabled){background:var(--red2);box-shadow:0 0 38px #e11d2e66}.rv .go:disabled{opacity:.4;cursor:not-allowed}
.rv .done{display:none;text-align:center;padding:26px 6px}.rv .done.on{display:block}.rv .done .ok{width:68px;height:68px;border-radius:50%;border:1.5px solid var(--red);display:grid;place-items:center;margin:0 auto 16px;color:var(--red2);font-size:30px}.rv .done b{display:block;font:500 1.6rem 'Montserrat',sans-serif}.rv .done span{display:block;color:var(--mut);margin-top:10px}
.inf{display:grid;gap:18px}.inf .bx{background:var(--p2);border:1px solid var(--ln);border-radius:20px;padding:26px 28px}.inf .t{font:500 11.5px 'Montserrat',sans-serif;letter-spacing:.24em;text-transform:uppercase;color:var(--red2)}.inf h3{font:500 1.35rem 'Montserrat',sans-serif;margin:12px 0 6px}.inf p{color:var(--mut);font-size:15px}
.hrs{margin-top:12px}.hrs li{display:flex;justify-content:space-between;gap:12px;padding:9px 0;border-bottom:1px solid var(--ln);font-size:14.5px;color:#d4d7dc}.hrs li:last-child{border:0}.hrs li.today{color:#fff}.hrs li.today span:first-child:after{content:" · aujourd’hui";color:var(--red2)}
.live{display:inline-flex;align-items:center;gap:9px;margin-top:12px;font-size:14px;color:#d4d7dc}.live i{width:9px;height:9px;border-radius:50%;background:#2fd06a;box-shadow:0 0 0 0 #2fd06a99;animation:pl 2s infinite}.live.off i{background:var(--red);animation:none}@keyframes pl{70%{box-shadow:0 0 0 9px #2fd06a00}100%{box-shadow:0 0 0 0 #2fd06a00}}
.map{border-radius:20px;border:1px solid var(--ln);overflow:hidden}.map svg{display:block;width:100%;height:auto}
/* ---- pied ---- */
footer.ft{background:#030304;border-top:1px solid var(--ln);padding:64px 0 34px;color:var(--mut);font-size:14.5px}body.home footer.ft{display:none}
footer.ft .w{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:34px}footer.ft h4{font:500 11.5px 'Montserrat',sans-serif;letter-spacing:.24em;text-transform:uppercase;color:#fff;margin-bottom:14px}footer.ft li{padding:4px 0}footer.ft a:hover{color:#fff}.legal{grid-column:1/-1;border-top:1px solid var(--ln);padding-top:22px;margin-top:10px;font-size:12.5px}
.rise{opacity:0;transform:translateY(26px);transition:opacity .8s cubic-bezier(.2,.8,.2,1),transform .8s cubic-bezier(.2,.8,.2,1)}.rise.in{opacity:1;transform:none}
@media(max-width:1000px){nav.mn,header.gh .pill{display:none}.bur{display:grid;place-items:center}nav.mn.on{display:flex;flex-direction:column;position:absolute;left:0;right:0;top:76px;background:#050607;border-bottom:1px solid var(--ln);padding:14px 20px}.tri,.vg,.team,.val,.rev{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.stats,.eng{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.dual,.cg{grid-template-columns:minmax(0,1fr)}footer.ft .w{grid-template-columns:1fr 1fr}.sr{grid-template-columns:48px minmax(0,1fr) 120px}.sr .du{display:none}}
@media(max-width:640px){.w{padding:0 20px}.sec{padding:70px 0}.ph{padding:60px 0 40px}.tri,.vg,.team,.val,.rev,.eng{grid-template-columns:minmax(0,1fr)}.hk{gap:16px}.hk span{letter-spacing:.4em;margin-right:-.4em}.hero .bg{background-position:76% center}.ht{transform:none}.hero .ht .pill{padding:17px 36px;font-size:1rem}.hs{letter-spacing:.2em;margin:26px 0 36px}.sr{grid-template-columns:40px minmax(0,1fr);gap:14px;padding:22px 4px}.sr .pr{grid-column:2;text-align:left;margin-top:2px}.rv{padding:24px 18px}.rv form{grid-template-columns:minmax(0,1fr)}.rv .slots{grid-template-columns:repeat(3,minmax(0,1fr))}.stats b{font-size:2.1rem}header.gh .w{gap:12px}footer.ft .w{grid-template-columns:minmax(0,1fr)}}
'''
    chev = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 6l6 6 6-6M6 13l6 6 6-6"/></svg>'
    arr = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h16M14 6l6 6-6 6"/></svg>'
    sh = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 5-3.500 8-8 9-4.500-1-8-4-8-9V6z"/><path d="M8.500 12l2.500 2.500L16 9.500"/></svg>'
    car = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 16l1.500-5.500A2 2 0 0 1 8.400 9h7.200a2 2 0 0 1 1.900 1.500L19 16M3 16h18v3H3zM7 19v1.500M17 19v1.500"/><circle cx="7.500" cy="16" r=".6"/><circle cx="16.500" cy="16" r=".6"/></svg>'
    clk = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
    cash = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="2.500"/><path d="M6 9.500v5M18 9.500v5"/></svg>'

    def srv(n, t, d, du, p, pre="à partir de"):
        return '<div class="sr"><span class="no">%s</span><div><h3>%s</h3><p>%s</p></div><span class="du">%s</span><div class="pr"><small>%s</small>%s</div></div>' % (n, t, d, du, pre, p)
    ent = "".join([
        srv("01", "Vidange et filtres", "Huile moteur, filtre à huile, contrôle des niveaux et des 21 points de sécurité.", "45 min", "89 €"),
        srv("02", "Révision constructeur", "Entretien selon le carnet, pièces d’origine ou équivalentes, carnet d’entretien tamponné.", "2 h", "149 €"),
        srv("03", "Pneumatiques", "Montage, équilibrage, géométrie. Pneus été, hiver et toutes saisons de toutes marques.", "1 h", "25 € / pneu"),
        srv("04", "Freinage", "Plaquettes et disques, purge du liquide de frein, essai sur route.", "1 h 30", "119 €"),
        srv("05", "Climatisation", "Recharge, contrôle d’étanchéité, désinfection de l’habitacle.", "1 h", "79 €"),
        srv("06", "Batterie et démarrage", "Test gratuit, remplacement, reprogrammation si nécessaire.", "30 min", "99 €")])
    rep = "".join([
        srv("07", "Diagnostic électronique", "Lecture des défauts, valise multimarque, compte rendu écrit remis le jour même.", "45 min", "49 €"),
        srv("08", "Embrayage", "Kit complet, volant moteur contrôlé, garantie 12 mois pièces et main d’œuvre.", "1 jour", "590 €"),
        srv("09", "Distribution", "Courroie, galets, pompe à eau. Le remplacement qui évite la casse moteur.", "1 jour", "450 €"),
        srv("10", "Échappement et FAP", "Réparation, nettoyage ou remplacement du filtre à particules.", "½ jour", "120 €"),
        srv("11", "Suspension et direction", "Amortisseurs, rotules, biellettes, parallélisme.", "½ jour", "180 €"),
        srv("12", "Carrosserie légère", "Rayures, pare-chocs, débosselage sans peinture, devis photo sous 24 h.", "sur devis", "90 €")])
    ven = "".join([
        srv("13", "Véhicules d’occasion contrôlés", "Chaque voiture passe 120 points de contrôle et se vend avec son historique complet.", "—", "6 900 €", "à partir de"),
        srv("14", "Garantie 12 mois", "Incluse sur tous nos véhicules, pièces et main d’œuvre, valable dans tout le réseau.", "—", "incluse", ""),
        srv("15", "Reprise de votre véhicule", "Estimation gratuite en 15 minutes, paiement immédiat, démarches administratives faites par nos soins.", "15 min", "gratuite", ""),
        srv("16", "Financement", "Location longue durée ou crédit, réponse de principe le jour même.", "—", "dès 129 € / mois")])

    PAL = {"v1": ("#e9ebef", "#c3c8cf", "#8e949d"), "v2": ("#3f6d9c", "#264a73", "#14284a"), "v3": ("#4a4f58", "#2b2f36", "#15171b"), "v4": ("#7cae9c", "#4c7c6c", "#27453b"), "v5": ("#b33a2f", "#7e231d", "#4a1410"), "v6": ("#d9b26a", "#a8803f", "#6b4c20")}

    def vcar(uid, tag, name, spec, price, t):
        art = car_art(uid).replace("#ffd400", "#e11d2e")
        c1, c2, c3 = PAL[uid]
        art = art.replace("#3a3f48", c1).replace("#1f2329", c2).replace("#121417", c3)
        return ('<div class="vc" data-t="%s"><div class="im"><svg class="%s" viewBox="0 100 800 260" role="img" aria-label="%s">%s</svg></div><div class="bd"><div class="tg">%s</div><h3>%s</h3><ul>%s</ul><div class="pf"><b>%s</b><a data-v="%s">Je suis intéressé</a></div></div></div>'
                % (t, 'fl' if uid in ('v2', 'v4', 'v6') else '', name, art, tag, name, "".join("<li>%s</li>" % x for x in spec), price, name))
    veh = "".join([
        vcar("v1", "Citadine", "Peugeot 208 1.2 PureTech", ["2021", "38 000 km", "Essence", "Manuelle"], "13 490 €", "citadine"),
        vcar("v2", "SUV", "Renault Captur Intens", ["2020", "52 000 km", "Diesel", "Auto"], "15 900 €", "suv"),
        vcar("v3", "Berline", "Volkswagen Golf 8 Life", ["2022", "29 000 km", "Essence", "Auto"], "21 900 €", "berline"),
        vcar("v4", "Électrique", "Renault Zoé R135", ["2021", "41 000 km", "Électrique", "Batterie louée"], "11 800 €", "electrique"),
        vcar("v5", "SUV", "Toyota C-HR Hybride", ["2021", "47 000 km", "Hybride", "Auto"], "22 500 €", "suv"),
        vcar("v6", "Citadine", "Citroën C3 Feel", ["2019", "61 000 km", "Essence", "Manuelle"], "9 600 €", "citadine")])
    hrs = "".join('<li data-d="%d"><span>%s</span><span>%s</span></li>' % x for x in (
        (1, "Lundi", "8 h – 12 h · 14 h – 18 h 30"), (2, "Mardi", "8 h – 12 h · 14 h – 18 h 30"), (3, "Mercredi", "8 h – 12 h · 14 h – 18 h 30"),
        (4, "Jeudi", "8 h – 12 h · 14 h – 18 h 30"), (5, "Vendredi", "8 h – 12 h · 14 h – 17 h 30"), (6, "Samedi", "9 h – 12 h"), (0, "Dimanche", "Fermé")))
    mapsvg = ('<svg viewBox="0 0 400 220" role="img" aria-label="Plan"><rect width="400" height="220" fill="#0b0c0e"/><g stroke="#23262b" stroke-width="10" fill="none"><path d="M-10 60 L410 90"/><path d="M-10 160 L410 140"/><path d="M120 -10 L150 230"/><path d="M290 -10 L270 230"/></g>'
              '<g stroke="#1a1c20" stroke-width="3" fill="none"><path d="M-10 110 L410 118"/><path d="M200 -10 L205 230"/></g><circle cx="205" cy="116" r="28" fill="#e11d2e" opacity=".15"/><circle cx="205" cy="116" r="9" fill="#e11d2e"/><circle cx="205" cy="116" r="3.500" fill="#fff"/>'
              '<text x="222" y="108" fill="#fff" font-family="Montserrat,sans-serif" font-size="12" font-weight="600">Garage Marchand</text></svg>')
    nav = '<a href="#/prestations" data-n="prestations">Prestations</a><a href="#/vehicules" data-n="vehicules">Véhicules</a><a href="#/apropos" data-n="apropos">Qui sommes-nous</a><a href="#/contact" data-n="contact">Contact</a>'
    body = '''<header class="gh"><div class="w"><a class="lg" href="#/"><span>GARAGE</span><b>MARCHAND</b></a><nav class="mn" id="nv">@@NAV@@</nav><a class="pill sm" href="#/contact">Prendre rendez-vous</a><button class="bur" id="bu" aria-label="Menu"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button></div></header>
<main>
<div class="view on" data-v="home">
<section class="hero" id="hero"><div class="bg" id="hbg"></div><div class="glow" id="hgl"></div><div class="ht"><div class="hk"><span>GARAGE</span></div><h1 class="hn">MARCHAND</h1><p class="hs">Entretien · Réparation · Vente de véhicules</p><a class="pill" href="#/prestations"><span>Découvrir nos prestations</span>@@ARR@@</a></div><button class="chev" id="chv" aria-label="Voir la suite">@@CHEV@@</button></section>
<section class="sec" id="suite"><div class="w"><span class="eb">Notre savoir-faire</span><h2 class="t">Tout pour votre voiture, au même endroit.</h2><p class="sub">Depuis 1998 à Mérignac, nous entretenons, réparons et vendons des véhicules de toutes marques. Un devis clair avant chaque intervention, et votre voiture rendue propre.</p>
<div class="tri"><a class="tc" href="#/prestations" data-tab="ent"><span class="n">01</span><h3>Entretien</h3><p>Vidange, révision, pneus, freins, climatisation. Toutes marques, sans perdre la garantie constructeur.</p><span class="go">Voir les tarifs</span></a><a class="tc" href="#/prestations" data-tab="rep"><span class="n">02</span><h3>Réparation</h3><p>Diagnostic électronique, embrayage, distribution, carrosserie légère. Devis écrit, aucune surprise.</p><span class="go">Voir les tarifs</span></a><a class="tc" href="#/vehicules"><span class="n">03</span><h3>Vente de véhicules</h3><p>Occasions contrôlées en 120 points, garanties 12 mois, reprise et financement possibles.</p><span class="go">Voir les véhicules</span></a></div>
<div class="stats"><div><b>25<i>+</i></b><span>ans d’expérience</span></div><div><b>12 000</b><span>véhicules entretenus</span></div><div><b>4,9<i>/5</i></b><span>sur 380 avis</span></div><div><b>24<i> h</i></b><span>devis sous 24 heures</span></div></div>
<p style="text-align:center;margin-top:50px"><a class="pill f" href="#/contact"><span>Prendre rendez-vous</span>@@ARR@@</a></p></div></section>
</div>

<div class="view" data-v="prestations"><div class="ph"><div class="w"><span class="eb">Nos prestations</span><h1>Entretien, réparation, vente</h1><p>Des tarifs affichés, des délais annoncés et un devis écrit avant toute intervention.</p></div></div>
<section class="sec" style="padding-top:20px"><div class="w"><div class="tabs" id="tb"><button class="tab on" data-g="ent">Entretien</button><button class="tab" data-g="rep">Réparation</button><button class="tab" data-g="ven">Vente de véhicules</button></div>
<div class="sv" data-g="ent">@@ENT@@</div><div class="sv" data-g="rep" hidden>@@REP@@</div><div class="sv" data-g="ven" hidden>@@VEN@@</div>
<div class="eng"><div>@@SH@@<b>Garantie 12 mois</b><span>Pièces et main d’œuvre, sur toutes nos réparations.</span></div><div>@@CLK@@<b>Délais tenus</b><span>Une heure de restitution annoncée, respectée.</span></div><div>@@CAR@@<b>Véhicule de courtoisie</b><span>Sur réservation, pour les interventions d’une journée.</span></div><div>@@CASH@@<b>Paiement en 3 fois</b><span>Sans frais dès 300 € de facture.</span></div></div>
<p style="text-align:center;margin-top:54px"><a class="pill f" href="#/contact"><span>Demander un devis</span>@@ARR@@</a></p></div></section></div>

<div class="view" data-v="vehicules"><div class="ph"><div class="w"><span class="eb">Véhicules à vendre</span><h1>Occasions contrôlées</h1><p>120 points de contrôle, historique complet, garantie 12 mois incluse. Reprise de votre ancien véhicule possible.</p></div></div>
<section class="sec" style="padding-top:20px"><div class="w"><div class="tabs" id="vt"><button class="tab on" data-t="all">Tous</button><button class="tab" data-t="citadine">Citadines</button><button class="tab" data-t="berline">Berlines</button><button class="tab" data-t="suv">SUV</button><button class="tab" data-t="electrique">Électriques</button></div>
<div class="vg" id="vg">@@VEH@@</div></div></section></div>

<div class="view" data-v="apropos"><div class="ph"><div class="w"><span class="eb">Qui sommes-nous</span><h1>Un garage de famille, depuis 1998</h1><p>Trois mécaniciens, un carrossier, une hôtesse d’accueil. Et une idée simple : expliquer avant de facturer.</p></div></div>
<section class="sec"><div class="w"><div class="dual"><div><span class="eb">Notre histoire</span><h2 class="t">Ouvert par Alain, repris par Julien.</h2><p>Alain Marchand ouvre l’atelier en 1998, à Mérignac, avec un pont et un tableau noir. Son fils Julien prend la suite en 2018 et agrandit : quatre ponts, une valise de diagnostic multimarque, un espace d’exposition pour les véhicules d’occasion.</p><p>Nous gardons la même règle : vous montrer la pièce usée, expliquer la panne, annoncer le prix avant de toucher à quoi que ce soit.</p><p style="margin-top:28px"><a class="pill sm" href="#/contact"><span>Nous rencontrer</span>@@ARR@@</a></p></div><img src="/assets/ex/gar-car.jpg" alt=""></div>
<div class="team"><div class="tm"><i>JM</i><b>Julien Marchand</b><em>Gérant, mécanicien</em><span>Dix-sept ans d’atelier. Il reçoit chaque client et valide chaque devis.</span></div><div class="tm"><i>KB</i><b>Karim Benali</b><em>Chef d’atelier</em><span>Spécialiste diagnostic et électronique embarquée, formé hybride et électrique.</span></div><div class="tm"><i>ML</i><b>Marion Leroy</b><em>Accueil et ventes</em><span>Elle vous conseille sur les véhicules, la reprise et le financement.</span></div></div>
<div class="val"><div><b>Transparence</b><span>Devis écrit, pièces montrées, facture détaillée ligne par ligne.</span></div><div><b>Qualité</b><span>Pièces d’origine ou équivalentes de première monte, garanties 12 mois.</span></div><div><b>Proximité</b><span>Une heure de restitution tenue, et un appel si le planning change.</span></div></div>
<div class="rev"><figure><div class="st">★★★★★</div><blockquote>« Diagnostic clair, devis respecté et voiture rendue à l’heure. Je ne vais plus ailleurs. »</blockquote><figcaption>Sophie R. · révision</figcaption></figure><figure><div class="st">★★★★★</div><blockquote>« Ils m’ont montré la plaquette usée avant de la changer. Ça change tout. »</blockquote><figcaption>Nicolas B. · freinage</figcaption></figure><figure><div class="st">★★★★★</div><blockquote>« Acheté ma Golf ici, historique complet et garantie respectée. Aucun souci. »</blockquote><figcaption>Camille D. · achat</figcaption></figure></div></div></section></div>

<div class="view" data-v="contact"><div class="ph"><div class="w"><span class="eb">Contact</span><h1>Prendre rendez-vous</h1><p>Choisissez votre créneau, nous vous confirmons par SMS. Pour une panne urgente, appelez-nous.</p></div></div>
<section class="sec" style="padding-top:40px"><div class="w"><div class="cg"><div class="rv"><div id="rvf"><h2>Votre rendez-vous</h2><div class="lab">1 · Jour</div><div class="days" id="days"></div><div class="lab">2 · Heure</div><div class="slots" id="slots"></div>
<div class="lab">3 · Votre véhicule</div><div class="rec" id="rec"><b>Aucun créneau choisi</b><span>Sélectionnez un jour puis une heure.</span></div>
<form id="bf"><label>Prestation<select id="mot"><option>Entretien / révision</option><option>Vidange et filtres</option><option>Pneumatiques</option><option>Freinage</option><option>Climatisation</option><option>Diagnostic électronique</option><option>Embrayage / distribution</option><option>Carrosserie légère</option><option>Essayer un véhicule</option><option>Reprise de mon véhicule</option><option>Autre demande</option></select></label><label>Immatriculation<input placeholder="AB-123-CD"></label><label>Nom et prénom<input required placeholder="Marie Durand"></label><label>Téléphone<input required inputmode="tel" placeholder="06 00 00 00 00"></label><label class="w2">Message (facultatif)<textarea id="msg" placeholder="Voyant allumé, bruit au freinage, véhicule qui vous intéresse…"></textarea></label><button class="go" type="submit" id="bgo" disabled>Confirmer le rendez-vous</button></form></div>
<div class="done" id="done"><div class="ok">✓</div><b>C’est noté.</b><span id="dt"></span></div></div>
<div class="inf"><div class="bx"><span class="t">Horaires</span><ul class="hrs" id="hr">@@HRS@@</ul><div class="live" id="lv"><i></i><span id="lvt"></span></div></div><div class="bx"><span class="t">Adresse</span><h3>14 avenue de la Libération</h3><p>33700 Mérignac<br>Parking gratuit devant l’atelier.</p></div><div class="bx"><span class="t">Nous joindre</span><h3>05 56 00 00 00</h3><p>contact@garage-marchand.fr<br>Urgence panne : nous rappelons en moins de 30 minutes.</p></div><div class="map">@@MAP@@</div></div></div></div></section></div>
</main>
<footer class="ft"><div class="w"><div><a class="lg" href="#/"><span>GARAGE</span><b>MARCHAND</b></a><p style="margin-top:16px;max-width:24em">Entretien, réparation et vente de véhicules, à Mérignac depuis 1998.</p></div><div><h4>Pages</h4><ul><li><a href="#/prestations">Prestations</a></li><li><a href="#/vehicules">Véhicules</a></li><li><a href="#/apropos">Qui sommes-nous</a></li><li><a href="#/contact">Contact</a></li></ul></div><div><h4>Contact</h4><ul><li>05 56 00 00 00</li><li>contact@garage-marchand.fr</li></ul></div><div><h4>Infos</h4><ul><li>Mentions légales</li><li>Confidentialité</li><li>Conditions de vente</li></ul></div>
<div class="legal">© 2026 Garage Marchand · SARL au capital de 10 000 € (exemple) · SIRET 000 000 000 00000 (exemple) · Hébergeur : Cloudflare, Inc.</div></div></footer>
'''
    body = (body.replace("@@NAV@@", nav).replace("@@ARR@@", arr).replace("@@CHEV@@", chev).replace("@@ENT@@", ent).replace("@@REP@@", rep).replace("@@VEN@@", ven)
            .replace("@@VEH@@", veh).replace("@@HRS@@", hrs).replace("@@MAP@@", mapsvg).replace("@@SH@@", sh).replace("@@CLK@@", clk).replace("@@CAR@@", car).replace("@@CASH@@", cash))
    js = r"""<script>(function(){
var D=document,$=function(i){return D.getElementById(i)},views=[].slice.call(D.querySelectorAll('.view')),links=[].slice.call(D.querySelectorAll('nav.mn a'));
function tab(g){[].forEach.call(D.querySelectorAll('#tb .tab'),function(b){b.classList.toggle('on',b.dataset.g===g)});[].forEach.call(D.querySelectorAll('.sv'),function(s){s.hidden=s.dataset.g!==g})}
function route(){var p=(location.hash||'#/').replace(/^#\/?/,'').split('/'),v=p[0]||'home';if(!D.querySelector('.view[data-v="'+v+'"]'))v='home';
 views.forEach(function(x){x.classList.toggle('on',x.dataset.v===v)});links.forEach(function(a){a.classList.toggle('on',a.dataset.n===v)});D.body.classList.toggle('home',v==='home');$('nv').classList.remove('on');
 if(v==='prestations'&&p[1])tab(p[1]);window.scrollTo(0,0);rise()}
function rise(){[].forEach.call(D.querySelectorAll('.view.on .tc,.view.on .vc,.view.on .tm,.view.on .rev figure,.view.on .val div,.view.on .stats,.view.on .eng div'),function(e){e.classList.add('rise');requestAnimationFrame(function(){setTimeout(function(){e.classList.add('in')},40)})})}
window.addEventListener('hashchange',route);
$('bu').onclick=function(){$('nv').classList.toggle('on')};
D.querySelectorAll('[data-tab]').forEach(function(a){a.addEventListener('click',function(){var g=a.dataset.tab;setTimeout(function(){tab(g)},0)})});
$('tb').onclick=function(e){var b=e.target.closest('.tab');if(b)tab(b.dataset.g)};
$('vt').onclick=function(e){var b=e.target.closest('.tab');if(!b)return;[].forEach.call($('vt').children,function(x){x.classList.toggle('on',x===b)});[].forEach.call(D.querySelectorAll('#vg .vc'),function(c){c.hidden=!(b.dataset.t==='all'||c.dataset.t===b.dataset.t)})};
$('vg').onclick=function(e){var a=e.target.closest('a[data-v]');if(!a)return;$('mot').value='Essayer un véhicule';$('msg').value='Je suis intéressé(e) par : '+a.dataset.v;location.hash='#/contact'};
$('chv').onclick=function(){$('suite').scrollIntoView({behavior:'smooth'})};
/* effets 3D : parallaxe du fond, lueur qui suit le curseur, inclinaison des cartes */
var reduce=window.matchMedia('(prefers-reduced-motion:reduce)').matches,hero=$('hero'),bg=$('hbg'),gl=$('hgl');
if(!reduce&&window.matchMedia('(hover:hover)').matches){
 hero.addEventListener('mousemove',function(e){var r=hero.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;bg.style.transform='translate('+(-x*26)+'px,'+(-y*16)+'px) scale(1.03)';gl.style.setProperty('--mx',(e.clientX-r.left)+'px');gl.style.setProperty('--my',(e.clientY-r.top)+'px')});
 hero.addEventListener('mouseleave',function(){bg.style.transform=''});
 D.addEventListener('mousemove',function(e){var c=e.target.closest&&e.target.closest('.tc,.vc');if(!c)return;var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;c.style.transform='perspective(900px) rotateY('+((x-.5)*8)+'deg) rotateX('+((.5-y)*8)+'deg) translateY(-4px)';c.style.setProperty('--px',x*100+'%');c.style.setProperty('--py',y*100+'%')});
 D.addEventListener('mouseout',function(e){var c=e.target.closest&&e.target.closest('.tc,.vc');if(c&&!c.contains(e.relatedTarget))c.style.transform=''})}
/* rendez-vous */
var days=$('days'),slots=$('slots'),rec=$('rec'),go=$('bgo'),sel={d:null,t:null};
var M={1:[8,9,10,11,14,15,16,17,18],2:[8,9,10,11,14,15,16,17,18],3:[8,9,10,11,14,15,16,17,18],4:[8,9,10,11,14,15,16,17,18],5:[8,9,10,11,14,15,16,17],6:[9,10,11],0:[]};
function hash(s){var h=0;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return Math.abs(h)}
function fmt(d){return d.toLocaleDateString('fr-FR',{weekday:'long',day:'numeric',month:'long'})}
var out=[],n=new Date();n.setHours(12);for(var i=1;out.length<9&&i<30;i++){var d=new Date(n);d.setDate(n.getDate()+i);if(d.getDay()!==0)out.push(d)}
function avail(d){var key=d.toISOString().slice(0,10);return(M[d.getDay()]||[]).filter(function(h){return hash(key+h)%100<64})}
out.forEach(function(d){var b=D.createElement('button');b.type='button';b.className='dy'+(avail(d).length?'':' full');b.innerHTML=d.toLocaleDateString('fr-FR',{weekday:'short'}).replace('.','')+'<b>'+d.getDate()+'</b>'+d.toLocaleDateString('fr-FR',{month:'short'}).replace('.','');
 b.onclick=function(){sel.d=d;sel.t=null;[].forEach.call(days.children,function(x){x.classList.remove('on')});b.classList.add('on');draw();upd()};days.appendChild(b)});
function draw(){slots.innerHTML='';var a=avail(sel.d);(M[sel.d.getDay()]||[]).forEach(function(h){var b=D.createElement('button');b.type='button';var ok=a.indexOf(h)>-1;b.className='sl2'+(ok?'':' x');b.textContent=h+' h 00';b.onclick=function(){sel.t=h;[].forEach.call(slots.children,function(x){x.classList.remove('on')});b.classList.add('on');upd()};slots.appendChild(b)})}
function upd(){if(sel.d&&sel.t){rec.innerHTML='<b>'+fmt(sel.d)+'</b><span>à '+sel.t+' h 00</span>';go.disabled=false}else{rec.innerHTML='<b>'+(sel.d?fmt(sel.d):'Aucun créneau choisi')+'</b><span>'+(sel.d?'Choisissez maintenant une heure.':'Sélectionnez un jour puis une heure.')+'</span>';go.disabled=true}}
for(var k=0;k<days.children.length;k++){if(days.children[k].className.indexOf('full')<0){days.children[k].click();break}}
$('bf').onsubmit=function(e){e.preventDefault();if(!sel.t)return;$('rvf').style.display='none';$('done').classList.add('on');$('dt').textContent=fmt(sel.d)+' à '+sel.t+' h 00. Un SMS de confirmation vous est envoyé, avec un rappel la veille.'};
var li=D.querySelector('#hr li[data-d="'+new Date().getDay()+'"]');if(li)li.classList.add('today');
(function(){var now=new Date(),dd=now.getDay(),m=now.getHours()*60+now.getMinutes(),op=false,t='Fermé actuellement';
 if(dd>=1&&dd<=5){op=(m>=480&&m<720)||(m>=840&&m<(dd===5?1050:1110))}else if(dd===6){op=m>=540&&m<720}
 if(op)t='Ouvert actuellement';$('lvt').textContent=t;if(!op)$('lv').classList.add('off')})();
route()})()</script>"""
    return page("Garage Marchand · Entretien, réparation, vente à Mérignac", "Garage à Mérignac : entretien, réparation et vente de véhicules d’occasion contrôlés. Rendez-vous en ligne.",
                "family=Montserrat:wght@300;400;500;600", css, body, js)



# ============================================================ 1. FLEURISTE : « le nuancier »
def fleuriste():
    import json
    page = H["page"]
    V = [  # id, nom, latin, cat, photo, prix, origine, reste
        ("pi", "Pivoine Sarah Bernhardt", "Paeonia lactiflora", "pivoine", "fl-d-pivoine", 4.5, "Saint-Genis-Laval · 11 km", 46),
        ("ps", "Pivoine Shirley Temple", "Paeonia lactiflora", "pivoine", "fl-d-haut", 4.2, "Millery · 21 km", 38),
        ("ro", "Rose ancienne Eden", "Rosa × hybrida", "saison", "fl-d-rose", 3.2, "Charly · 18 km", 120),
        ("ly", "Lys oriental blanc", "Lilium orientalis", "saison", "fl-d-lys", 3.8, "Irigny · 14 km", 54),
        ("st", "Limonium rose", "Limonium sinuatum", "saison", "fl-d-bouton", 2.1, "Vourles · 16 km", 90),
        ("eu", "Eucalyptus cinerea", "Feuillage", "feuillage", "fl-d-eucalyptus", 1.5, "Brignais · 19 km", 150),
    ]
    B = [("Bouquet Passion", "Roses rouges, feuillage et papier kraft", 39.9, "fl-passion"),
         ("Pivoines de saison", "Pivoines roses, ruban de soie rose", 45.0, "fl-pivoines"),
         ("Élégance Blanche", "Roses et lisianthus blancs, verdure", 42.0, "fl-blanc"),
         ("Bouquet Vitaminé", "Roses orange et roses, feuillage frais", 38.0, "fl-vitamine"),
         ("Le Grand Atelier", "Pivoines, roses, lys et eucalyptus", 68.0, "fl-hero"),
         ("Roses poudrées", "Roses anciennes rose pâle, à offrir", 36.0, "fl-d-rose")]
    def fm(n): return ("%.2f" % n).replace(".", ",") + " €"
    heart = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.600-7 10-7 10z"/></svg>'
    def card(i, b, extra=""):
        n, d, p, ph = b
        return ('<article class="pc"><div class="im"><img src="/assets/ex/%s.jpg" alt="%s" loading="lazy"></div><div class="pb"><div class="pt"><h3>%s</h3><button type="button" class="hrt" aria-label="Ajouter aux favoris" aria-pressed="false">%s</button></div>'
                '<p class="ds">%s</p><div class="pf"><b>%s</b><button type="button" class="add" data-b="%d">Ajouter</button></div></div></article>' % (ph, n, n, heart, d, fm(p), i))
    home_cards = "".join(card(i, B[i]) for i in range(4))
    all_cards = "".join(card(i, b) for i, b in enumerate(B))
    vcards = ""
    for k, n, la, cat, ph, p, o, r in V:
        vcards += ('<article class="vc" data-c="%s"><div class="im"><img src="/assets/ex/%s.jpg" alt="%s" loading="lazy"><span class="tag">%s km · %s</span></div><div class="pb"><h3>%s</h3><p class="la">%s</p>'
                   '<p class="ds">Cultivée à %s<br>Il en reste <i data-r="%d">%d</i> ce matin</p><div class="pf"><b>%s <small>la tige</small></b>'
                   '<span class="stp" data-k="%s"><button type="button" class="mn" data-a="-1" aria-label="Retirer une tige">−</button><output>0</output><button type="button" class="mn" data-a="1" aria-label="Ajouter une tige">+</button></span></div></div></article>'
                   % (cat, ph, n, o.split("· ")[1].replace(" km", ""), o.split(" · ")[0], n, la, o.split(" · ")[0], r, r, fm(p), k))
    mk = "".join('<tr><td>%s</td><td>%s</td><td><span class="brr"><u data-t="%d"></u></span></td><td class="rt" data-s2>%d</td></tr>' % (n, o.split(" · ")[0], r, r) for k, n, la, cat, ph, p, o, r in V)
    css = r'''
:root{--g:#1b2d25;--g2:#12201a;--cr:#f6f1ed;--cr2:#efe7e0;--pk:#bb4565;--pk2:#e9bbc6;--ink:#1d211f;--mut:#6c6a65;--ln:#e5dcd3}
body{background:var(--cr);color:var(--ink);font:400 16.5px/1.6 'DM Sans',system-ui,sans-serif}
h1,h2,h3,h4,.serif{font-family:'Playfair Display',Georgia,'Times New Roman',serif;font-weight:600;letter-spacing:-.01em}
.w{max-width:1240px;margin:0 auto;padding:0 28px}
.top{background:var(--g2);color:#e8dfd6;font:500 12.5px/1 'DM Sans',sans-serif;padding:10px 0;letter-spacing:.03em;overflow:hidden;white-space:nowrap}.top .tk{display:inline-block;animation:tk 52s linear infinite}.top .tk span{margin:0 28px}.top .tk b{color:var(--pk2);font-weight:500}.top:hover .tk{animation-play-state:paused}@keyframes tk{to{transform:translateX(-50%)}}
header.f{position:sticky;top:0;z-index:60;background:var(--g);color:#fff;box-shadow:0 6px 20px #0003}header.f .w{display:flex;align-items:center;gap:30px;height:86px}
.logo{display:flex;align-items:center;gap:12px;color:#fff}.logo img{width:52px;height:auto;display:block;border-radius:6px}.logo b{display:block;font:600 1.75rem/1 'Playfair Display',Georgia,serif;letter-spacing:.09em}.logo small{display:block;font:500 .6rem/1 'DM Sans',sans-serif;letter-spacing:.32em;color:#c9bdb2;margin-top:6px}
nav.mn2{display:flex;gap:30px;margin:0 auto;font:500 15px 'DM Sans',sans-serif}nav.mn2>a,nav.mn2 .dd>a{color:#f1e9e1;padding:8px 0;position:relative;display:block;white-space:nowrap}nav.mn2 a:hover,nav.mn2 a.on{color:#fff}nav.mn2>a.on,nav.mn2 .dd>a.on{box-shadow:inset 0 -2px 0 var(--pk2)}
.dd{position:relative}.dd>a:after{content:"";display:inline-block;width:6px;height:6px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:rotate(45deg) translateY(-2px);margin-left:7px}.dd .sub{position:absolute;left:-16px;top:100%;background:#fff;color:var(--ink);border-radius:14px;box-shadow:0 20px 40px #0003;padding:10px;min-width:220px;opacity:0;visibility:hidden;transform:translateY(8px);transition:.2s}.dd:hover .sub,.dd:focus-within .sub{opacity:1;visibility:visible;transform:none}.sub a{display:block;padding:10px 14px;border-radius:9px;font-size:15px}.sub a:hover{background:var(--cr)}
.ic{display:flex;gap:6px;align-items:center}.ib{position:relative;width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:none;border:0;color:#fff;cursor:pointer}.ib:hover{background:#ffffff1c}.ib svg{width:23px;height:23px}.bdg{position:absolute;top:2px;right:0;min-width:19px;height:19px;border-radius:99px;background:var(--pk);font:700 11px/19px 'DM Sans',sans-serif;text-align:center;padding:0 5px}
.bur{display:none}
.view{display:none;animation:vin .5s cubic-bezier(.2,.8,.2,1)}.view.on{display:block}@keyframes vin{from{opacity:0;transform:translateY(14px)}}
.hero{position:relative;overflow:hidden;background:radial-gradient(ellipse 70% 90% at 30% 20%,#fffaf6,var(--cr))}.hero .w{display:grid;grid-template-columns:1.05fr 1fr;gap:20px;align-items:center;min-height:660px}
.eb{font:700 13px/1 'DM Sans',sans-serif;letter-spacing:.14em;color:var(--pk);text-transform:uppercase}
h1{font-size:clamp(3rem,6.4vw,5.6rem);line-height:1.02;margin:22px 0 22px}h1 u{text-decoration:none;background:linear-gradient(transparent 86%,var(--pk) 86% 91%,transparent 91%)}
.lead{font-size:1.2rem;max-width:26em;color:#3d3f3b}
.cta{display:flex;gap:16px;flex-wrap:wrap;margin:34px 0}.btn{display:inline-flex;align-items:center;gap:12px;border-radius:14px;padding:18px 26px;font:600 16px/1 'DM Sans',sans-serif;cursor:pointer;border:2px solid var(--ink);background:transparent;color:var(--ink);transition:.2s}.btn:hover{background:var(--ink);color:#fff}.btn.p{background:var(--pk);border-color:var(--pk);color:#fff}.btn.p:hover{background:#9f3453;border-color:#9f3453;transform:translateY(-2px);box-shadow:0 12px 24px #bb456544}.btn.w2{background:#fff;border-color:#fff;color:var(--g)}.btn.w2:hover{background:var(--pk2);border-color:var(--pk2);color:var(--g)}
.pr3{display:flex;gap:34px;margin-top:14px}.pr3 div{text-align:center;font:500 14px/1.35 'DM Sans',sans-serif;max-width:150px}.pr3 svg{width:34px;height:34px;color:var(--g);display:block;margin:0 auto 8px}
.hi{position:relative;align-self:stretch;margin-right:-28px}.hi .im2{position:absolute;inset:0 0 0 0;overflow:hidden;border-radius:0 0 0 220px}.hi img{width:100%;height:100%;object-fit:cover;display:block;animation:kb 18s ease-in-out infinite alternate}@keyframes kb{to{transform:scale(1.08) translateY(-1.5%)}}
.sec{padding:80px 0 0}.sec h2{font-size:clamp(2rem,3.6vw,3rem);text-align:center}.sec h2:after{content:"";display:block;width:60px;height:2px;background:var(--pk);margin:16px auto 0}.sec .sb{text-align:center;color:var(--mut);margin-top:16px}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin-top:40px}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:40px}
.pc,.vc{background:#fff;border-radius:22px;overflow:hidden;box-shadow:0 10px 30px #5a3d2b14;transition:transform .35s,box-shadow .35s;display:flex;flex-direction:column}.pc:hover,.vc:hover{transform:translateY(-8px);box-shadow:0 26px 44px #5a3d2b26}
.im{position:relative;aspect-ratio:4/3;overflow:hidden;background:var(--cr2)}.im img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .8s}.pc:hover .im img,.vc:hover .im img{transform:scale(1.07)}
.tag{position:absolute;left:12px;top:12px;background:#fffffff0;border-radius:99px;font:600 12px/1 'DM Sans',sans-serif;padding:8px 12px}
.pb{padding:18px 20px 20px;display:flex;flex-direction:column;gap:6px;flex:1}.pt{display:flex;justify-content:space-between;align-items:center;gap:10px}.pb h3{font:600 1.18rem/1.2 'DM Sans',sans-serif;letter-spacing:0}.la{font:italic 400 .98rem 'Playfair Display',Georgia,serif;color:var(--mut)}.ds{font-size:14.5px;color:var(--mut)}.ds i{font-style:normal;font-weight:700;color:var(--ink)}
.hrt{background:none;border:0;cursor:pointer;color:var(--pk);padding:4px;border-radius:50%;transition:.25s}.hrt:hover{transform:scale(1.2)}.hrt[aria-pressed=true] svg{fill:var(--pk)}
.pf{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:10px}.pf b{font:700 1.1rem 'DM Sans',sans-serif}.pf small{font-weight:400;color:var(--mut);font-size:13px}
.add{border:1.5px solid var(--g);background:transparent;color:var(--g);border-radius:99px;padding:10px 18px;font:600 14px 'DM Sans',sans-serif;cursor:pointer;transition:.2s}.add:hover{background:var(--g);color:#fff}
.stp{display:flex;align-items:center;border:1.5px solid var(--g);border-radius:99px;overflow:hidden}.stp .mn{width:36px;height:36px;border:0;background:none;font:500 1.3rem 'DM Sans',sans-serif;cursor:pointer;color:var(--g)}.stp .mn:hover{background:var(--g);color:#fff}.stp output{min-width:28px;text-align:center;font:700 15px 'DM Sans',sans-serif}
.band{position:relative;margin:70px auto 0;border-radius:26px;overflow:hidden;background:var(--g2);color:#fff;display:grid;grid-template-columns:1.1fr 1fr;align-items:center;max-width:1184px}.band .tx{padding:44px 50px}.band h2{font-size:2.4rem;text-align:left}.band h2:after{display:none}.band p{color:#d5cbc1;margin:12px 0 26px;max-width:24em}.band img{width:100%;height:100%;min-height:220px;object-fit:cover;display:block}
.bw{padding:0 28px}
.chips{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:26px}.chip{border:1.5px solid var(--ln);background:#fff;border-radius:99px;padding:10px 20px;font:600 14.5px 'DM Sans',sans-serif;cursor:pointer;color:var(--ink)}.chip.on,.chip:hover{background:var(--g);border-color:var(--g);color:#fff}
.ph{background:var(--g);color:#fff;padding:56px 0 50px;text-align:center}.ph h1{font-size:clamp(2.4rem,4.6vw,3.8rem);margin:8px 0 10px}.ph p{color:#d5cbc1;max-width:34em;margin:0 auto}.ph .eb{color:var(--pk2)}
.plans{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:40px}.plan{background:#fff;border-radius:24px;padding:34px 30px;box-shadow:0 10px 30px #5a3d2b14;display:flex;flex-direction:column;gap:10px;position:relative;transition:.3s}.plan:hover{transform:translateY(-8px);box-shadow:0 26px 44px #5a3d2b26}.plan.hot{background:var(--g);color:#fff}.plan.hot p,.plan.hot li{color:#d5cbc1}.plan .tg2{position:absolute;right:20px;top:20px;background:var(--pk);color:#fff;border-radius:99px;padding:6px 12px;font:700 12px 'DM Sans',sans-serif}.plan h3{font-size:1.6rem}.plan .pz{font:600 3rem/1 'Playfair Display',Georgia,serif}.plan .pz small{font:500 .95rem 'DM Sans',sans-serif;color:var(--mut)}.plan.hot .pz small{color:#c9bdb2}.plan ul{margin:8px 0 18px;display:grid;gap:8px;font-size:15px}.plan li{padding-left:24px;position:relative}.plan li:before{content:"✿";position:absolute;left:0;color:var(--pk)}.plan .btn{margin-top:auto;justify-content:center}.plan.hot .btn{background:#fff;color:var(--g);border-color:#fff}
.sp{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;margin-top:56px}.sp.r .tx{order:2}.sp img{width:100%;border-radius:26px;display:block;aspect-ratio:5/4;object-fit:cover;box-shadow:0 20px 44px #5a3d2b2a}.sp h3{font-size:2rem;margin-bottom:12px}.sp p{color:#43463f}.sp ol{margin-top:20px;display:grid;gap:12px}.sp ol li{display:flex;gap:16px;align-items:flex-start}.sp ol b{width:34px;height:34px;flex:none;border-radius:50%;background:var(--pk2);color:var(--g);display:grid;place-items:center;font:700 14px 'DM Sans',sans-serif}
.card{background:#fff;border-radius:24px;padding:34px;box-shadow:0 10px 30px #5a3d2b14}
.fm{display:grid;grid-template-columns:1.05fr 1fr;gap:34px;margin-top:40px}.fm h3{font-size:1.5rem;margin-bottom:14px}
#recap{border-top:1px solid var(--ln)}#recap li{display:flex;justify-content:space-between;gap:12px;padding:14px 0;border-bottom:1px solid var(--ln)}#recap .vide{color:var(--mut)}#recap button{background:none;border:0;color:var(--pk);cursor:pointer;font:600 13px 'DM Sans',sans-serif;margin-left:10px}
.tot{display:flex;justify-content:space-between;align-items:baseline;padding:20px 0 0;font:600 2rem/1 'Playfair Display',Georgia,serif}.tot small{font:500 13px 'DM Sans',sans-serif;color:var(--mut)}
form.o{display:grid;gap:16px}.o label{display:grid;gap:7px;font:600 13px 'DM Sans',sans-serif;color:var(--mut)}.o input,.o select,.o textarea{font:400 16px 'DM Sans',sans-serif;padding:14px 16px;border:1.5px solid var(--ln);border-radius:12px;background:var(--cr);color:var(--ink)}.o input:focus,.o select:focus,.o textarea:focus{outline:0;border-color:var(--pk);background:#fff}
.mode{display:grid;grid-template-columns:1fr 1fr;gap:10px}.mode label{padding:14px 16px;border:1.5px solid var(--ln);border-radius:14px;cursor:pointer;color:var(--ink);font:600 15px 'DM Sans',sans-serif}.mode input{display:none}.mode label:has(input:checked){border-color:var(--pk);background:#fbeef2}.mode small{display:block;font:400 12.5px 'DM Sans',sans-serif;color:var(--mut);margin-top:3px}
.go{background:var(--pk);color:#fff;border:0;padding:18px;font:700 16px 'DM Sans',sans-serif;border-radius:14px;cursor:pointer;transition:.2s}.go:hover{background:#9f3453}.go:disabled{opacity:.4;cursor:not-allowed}
.ok{display:none;background:#eef6ef;border-radius:16px;padding:26px}.ok.on{display:block}.ok b{font:600 1.5rem 'Playfair Display',Georgia,serif;display:block;margin-bottom:6px}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:44px;text-align:center}.stats b{display:block;font:600 3rem/1 'Playfair Display',Georgia,serif;color:var(--pk)}.stats span{color:var(--mut);font-size:15px}
.quote{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:40px}.quote .card p{font:italic 400 1.15rem/1.5 'Playfair Display',Georgia,serif}.quote small{display:block;margin-top:14px;color:var(--mut);font-size:14px}
.tb{width:100%;border-collapse:collapse;margin-top:30px;background:#fff;border-radius:18px;overflow:hidden}.tb td{padding:15px 20px;border-bottom:1px solid var(--ln)}.rt{text-align:right}.brr{display:block;height:6px;background:var(--cr2);border-radius:9px;overflow:hidden}.brr u{display:block;height:100%;background:var(--pk);border-radius:9px;transition:width .6s}
.hr li{display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid var(--ln)}.hr li.today{font-weight:700;color:var(--pk)}
.faq details{border-bottom:1px solid var(--ln);padding:18px 0}.faq summary{cursor:pointer;font:600 1.08rem 'DM Sans',sans-serif;list-style:none;display:flex;justify-content:space-between;gap:16px}.faq summary::-webkit-details-marker{display:none}.faq summary:after{content:"+";color:var(--pk);font-size:1.5rem;line-height:1}.faq details[open] summary:after{content:"–"}.faq p{margin-top:10px;color:var(--mut)}
.bar2{position:fixed;left:16px;right:16px;bottom:18px;z-index:90;max-width:640px;margin:0 auto;background:var(--g);color:#fff;border-radius:18px;transform:translateY(160%);visibility:hidden;transition:.4s cubic-bezier(.2,.8,.2,1),visibility 0s .4s;padding:12px 12px 12px 22px;box-shadow:0 18px 40px #0005}.bar2.on{transform:none;visibility:visible;transition:.4s cubic-bezier(.2,.8,.2,1)}.bar2>div{display:flex;justify-content:space-between;align-items:center;gap:14px}.bar2 b{font:600 1rem 'DM Sans',sans-serif}.bar2 a{background:var(--pk);color:#fff;padding:13px 22px;font:700 15px 'DM Sans',sans-serif;border-radius:12px}
.toast{position:fixed;left:50%;top:104px;transform:translate(-50%,-20px);background:#fff;color:var(--ink);border-radius:99px;padding:13px 22px;font:600 14px 'DM Sans',sans-serif;box-shadow:0 14px 34px #0004;opacity:0;pointer-events:none;transition:.3s;z-index:100}.toast.on{opacity:1;transform:translate(-50%,0)}
footer.ft{margin-top:100px;background:var(--g2);color:#cfc5bb;padding:60px 0 34px}footer.ft .w{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:34px}footer.ft h4{font:700 12px 'DM Sans',sans-serif;letter-spacing:.14em;color:var(--pk2);margin-bottom:14px;text-transform:uppercase}footer.ft li{margin:8px 0;font-size:15px}.legal{grid-column:1/-1;border-top:1px solid #ffffff22;padding-top:22px;font-size:13px;color:#8d867f;margin-top:16px}
@media(prefers-reduced-motion:reduce){.top .tk,.hi img{animation:none}.view{animation:none}}
@media(max-width:980px){.grid4{grid-template-columns:repeat(2,1fr)}.grid3,.plans,.quote,.stats{grid-template-columns:1fr}.hero .w{grid-template-columns:1fr;min-height:0;gap:0}.hi{margin:30px -28px 0;height:420px;order:2}.hi .im2{border-radius:0}.band{grid-template-columns:1fr;margin-left:16px;margin-right:16px}.band img{height:200px}.sp,.fm{grid-template-columns:1fr;gap:30px}.sp.r .tx{order:0}footer.ft .w{grid-template-columns:1fr 1fr}
 nav.mn2{position:fixed;left:0;right:0;top:86px;background:var(--g);flex-direction:column;gap:0;padding:8px 24px 22px;margin:0;transform:translateY(-130%);transition:transform .35s;z-index:55}nav.mn2.on{transform:none}nav.mn2>a,nav.mn2 .dd>a{padding:14px 0;border-bottom:1px solid #ffffff1f}.dd .sub{position:static;opacity:1;visibility:visible;transform:none;background:none;box-shadow:none;padding:0 0 0 14px;display:none}.dd .sub a{color:#d8cec4;padding:10px 0}.dd.o .sub{display:block}.dd>a:after{display:none}
 .bur{display:grid}.ic{margin-left:auto}}
@media(max-width:600px){.w{padding:0 18px}header.f .w{height:72px;gap:10px}nav.mn2{top:72px}.logo img{width:40px}.logo b{font-size:1.3rem}.logo small{display:none}.pr3{gap:14px}.pr3 div{font-size:12.5px}.grid4{grid-template-columns:1fr 1fr;gap:12px}.pb{padding:14px 14px 16px}.pb h3{font-size:1rem}.pf{flex-wrap:wrap;gap:8px}.add{padding:9px 14px}.sec{padding-top:56px}.band .tx{padding:30px 24px}.card{padding:24px 20px}.btn{padding:16px 20px}.toast{top:90px}.tb td{padding:12px 10px}.tb td:nth-child(2){display:none}.hero .w{padding-top:34px}.cta .btn{flex:1;justify-content:center}}
'''
    ico = lambda p: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">%s</svg>' % p
    I_search = ico('<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>')
    I_user = ico('<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>')
    I_bag = ico('<path d="M5 8h14l-1 12H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>')
    I_bur = ico('<path d="M4 7h16M4 12h16M4 17h16"/>')
    I_truck = ico('<path d="M2 6h11v10H2zM13 9h4l3 3v4h-7"/><circle cx="7" cy="17.500" r="1.800"/><circle cx="17" cy="17.500" r="1.800"/>')
    I_flower = ico('<path d="M12 22v-8"/><path d="M12 14c-4 0-6-3-6-6 3 0 6 1 6 6zM12 14c4 0 6-3 6-6-3 0-6 1-6 6z"/><path d="M12 10c-2-2-2-5 0-7 2 2 2 5 0 7z"/>')
    I_msg = ico('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>')
    ticker = ["● Ce matin : 6 variétés arrivées du marché", "Nouveau : pivoines Sarah Bernhardt, 4,50 € la tige", "Spécial Saint-Valentin : lot de 12 roses rouges à précommander", "Arrivage de lys, roses anciennes et limonium", "Livraison à vélo avant 18 h · commande jusqu’à 11 h", "Abonnement bouquet de la semaine : premier mois offert"]
    tk = "".join('<span>%s</span><b>✿</b>' % t for t in ticker) * 2
    body = '''
<div class="top" aria-label="Annonces de la boutique"><div class="tk">@@TK@@</div></div>
<header class="f"><div class="w"><a class="logo" href="#/"><img src="/assets/ex/fl-logo.png" alt=""><span><b>PIVOINE</b><small>ATELIER FLORAL</small></span></a>
<nav class="mn2" id="nv"><div class="dd" id="dd"><a href="#/fleurs" data-n="fleurs">Fleurs</a><div class="sub"><a href="#/fleurs">Toutes les fleurs</a><a href="#/fleurs/pivoine">Pivoines</a><a href="#/fleurs/saison">Fleurs de saison</a><a href="#/fleurs/feuillage">Feuillages</a></div></div><a href="#/bouquets" data-n="bouquets">Bouquets</a><a href="#/abonnements" data-n="abonnements">Abonnements</a><a href="#/mariage" data-n="mariage">Mariage &amp; Événements</a><a href="#/apropos" data-n="apropos">À propos</a></nav>
<div class="ic"><button class="ib" type="button" id="sr" aria-label="Rechercher">@@SE@@</button><button class="ib" type="button" id="us" aria-label="Mon compte">@@US@@</button><a class="ib" href="#/panier" aria-label="Panier">@@BG@@<span class="bdg" id="cn">0</span></a><button class="ib bur" type="button" id="bu" aria-label="Menu">@@BU@@</button></div></div></header>
<div class="toast" id="ts"></div>
<main id="top">

<div class="view" data-v="home"><section class="hero"><div class="w"><div><span class="eb">Fleuriste à Lyon</span><h1>Des fleurs,<br>à la <u>tige.</u></h1><p class="lead">Bouquets, compositions et créations sur mesure pour toutes les occasions. Cultivées à moins de 40 km, coupées la veille.</p>
<div class="cta"><a class="btn p" href="#/bouquets">Commander en ligne <span>→</span></a><a class="btn" href="#/bouquets">Nos bouquets</a></div>
<div class="pr3"><div>@@TR@@Livraison à vélo<br>à Lyon et environs</div><div>@@FL@@Fleurs fraîches<br>et de saison</div><div>@@MS@@Message personnalisé<br>offert</div></div></div>
<div class="hi"><div class="im2"><img src="/assets/ex/fl-hero.jpg" alt="Bouquet de pivoines et roses"></div></div></div></section>
<section class="sec"><div class="w"><h2>Nos créations du moment</h2><div class="grid4">@@HC@@</div></div>
<div class="bw"><div class="band"><div class="tx"><h2>Un bouquet chaque mois ?</h2><p>Découvrez nos abonnements floraux et recevez des fleurs fraîches régulièrement.</p><a class="btn w2" href="#/abonnements">Découvrir les abonnements →</a></div><img src="/assets/ex/fl-abo.jpg" alt=""></div></div></section></div>

<div class="view" data-v="fleurs"><div class="ph"><div class="w"><span class="eb">À la tige</span><h1>Nos fleurs</h1><p>Choisissez vos fleurs une par une, au nombre de tiges que vous voulez. Cultivées à moins de 40 km, coupées la veille.</p></div></div>
<section class="sec" style="padding-top:44px"><div class="w"><div class="chips" id="ch"><button class="chip on" data-c="">Toutes</button><button class="chip" data-c="pivoine">Pivoines</button><button class="chip" data-c="saison">Fleurs de saison</button><button class="chip" data-c="feuillage">Feuillages</button></div><div class="grid3" id="vg">@@VC@@</div>
<h2 style="margin-top:80px">Au marché ce matin</h2><p class="sb" id="dj">—</p><table class="tb"><tr style="color:var(--mut);font-size:13px"><td>Variété</td><td>Ferme</td><td style="width:32%">Reste en boutique</td><td class="rt">Tiges</td></tr>@@MK@@</table></div></section></div>

<div class="view" data-v="bouquets"><div class="ph"><div class="w"><span class="eb">Composés ce matin</span><h1>Nos bouquets</h1><p>Prêts à offrir, emballés dans du papier kraft et un ruban de soie. Prix TTC, livraison à vélo ou retrait en boutique.</p></div></div>
<section class="sec" style="padding-top:20px"><div class="w"><div class="grid3">@@AC@@</div></div></section></div>

<div class="view" data-v="abonnements"><div class="ph"><div class="w"><span class="eb">Sans engagement</span><h1>Abonnements</h1><p>Un bouquet de saison à intervalle régulier. Pause ou arrêt en un clic.</p></div></div>
<section class="sec" style="padding-top:20px"><div class="w"><div class="plans"><div class="plan"><span class="eb">Pour soi</span><h3>Le petit</h3><div class="pz">29 €<small> / mois</small></div><p>Un bouquet de saison par mois, déposé ou à retirer.</p><ul><li>Choisi selon l’arrivage</li><li>Papier kraft et ruban</li><li>Pause en un clic</li></ul><button class="btn" data-abo="Abonnement Le petit · 29 €/mois">Je m’abonne</button></div>
<div class="plan hot"><span class="tg2">Le plus choisi</span><span class="eb" style="color:var(--pk2)">Pour offrir</span><h3>Le généreux</h3><div class="pz">49 €<small> / mois</small></div><p>Deux bouquets par mois, dont un pour quelqu’un d’autre.</p><ul><li>Carte écrite à la main</li><li>Livraison à vélo incluse</li><li>Premier mois offert</li></ul><button class="btn" data-abo="Abonnement Le généreux · 49 €/mois">Je m’abonne</button></div>
<div class="plan"><span class="eb">Pour l’accueil</span><h3>L’entreprise</h3><div class="pz">79 €<small> / semaine</small></div><p>Un grand bouquet chaque lundi pour votre accueil, restaurant ou cabinet.</p><ul><li>Facture mensuelle</li><li>Composition sur mesure</li><li>Remplacement offert</li></ul><button class="btn" data-abo="Abonnement L’entreprise · 79 €/semaine">Je m’abonne</button></div></div>
<div class="band" style="margin-top:60px"><div class="tx"><h2>Un cadeau qui dure</h2><p>Offrez 3, 6 ou 12 mois de fleurs. Nous envoyons une carte pour annoncer la surprise.</p><a class="btn w2" href="#/mariage">Nous écrire →</a></div><img src="/assets/ex/fl-abo.jpg" alt=""></div></div></section></div>

<div class="view" data-v="mariage"><div class="ph"><div class="w"><span class="eb">Sur rendez-vous · 04 78 00 00 00</span><h1>Mariage &amp; Événements</h1><p>Mariages, deuils, anniversaires, entreprises : une composition pensée avec vous, installée à l’heure.</p></div></div>
<section class="sec" style="padding-top:30px"><div class="w"><div class="sp"><img src="/assets/ex/fl-d-kraft.jpg" alt=""><div class="tx"><h3>Mariages</h3><p>Bouquet de mariée, boutonnières, arche, tables. Nous venons voir le lieu, choisissons les fleurs de votre mois, puis installons la veille.</p><ol><li><b>1</b><span>Rendez-vous à l’atelier, une heure, café offert</span></li><li><b>2</b><span>Devis détaillé sous 5 jours, sans surprise</span></li><li><b>3</b><span>Installation la veille, récupération le lendemain</span></li></ol></div></div>
<div class="sp r"><img src="/assets/ex/fl-d-haut.jpg" alt=""><div class="tx"><h3>Deuils et cérémonies</h3><p>Gerbes, coussins, couronnes et bouquets. Nous répondons au téléphone toute la semaine et livrons le jour même quand c’est possible.</p><ol><li><b>1</b><span>Un appel suffit, devis immédiat</span></li><li><b>2</b><span>Ruban personnalisé, écrit sans faute</span></li><li><b>3</b><span>Livraison à l’heure de la cérémonie</span></li></ol></div></div>
<div class="card" style="margin-top:70px;max-width:720px;margin-left:auto;margin-right:auto"><h3 class="serif" style="font-size:1.8rem;margin-bottom:6px">Demander un devis</h3><p style="color:var(--mut);margin-bottom:20px">Réponse sous 24 h, du mardi au samedi.</p><form class="o" id="qf"><label>Type d’événement<select><option>Mariage</option><option>Deuil</option><option>Anniversaire</option><option>Entreprise</option></select></label><label>Date<input type="date" id="qd" required></label><label>Nom<input required placeholder="Camille Roux"></label><label>Téléphone<input required inputmode="tel" placeholder="06 00 00 00 00"></label><button class="go">Envoyer ma demande</button></form><div class="ok" id="qok"><b>Demande envoyée.</b>Nous vous rappelons sous 24 h pour fixer un rendez-vous.</div></div></div></section></div>

<div class="view" data-v="apropos"><div class="ph"><div class="w"><span class="eb">Depuis 2014</span><h1>À propos</h1><p>Une fleuriste indépendante, des fleurs locales et de saison, sans mousse florale.</p></div></div>
<section class="sec" style="padding-top:30px"><div class="w"><div class="sp"><img src="/assets/ex/fl-hero.jpg" alt=""><div class="tx"><h3>L’atelier Pivoine</h3><p>Nous travaillons avec huit producteurs à moins de 40 km de Lyon. Les fleurs sont coupées la veille, composées le matin et livrées à vélo dans l’après-midi. Rien n’est stocké, rien n’est surgelé.</p><p style="margin-top:12px">Chaque bouquet est emballé dans du papier kraft recyclable et un ruban de soie, sans plastique.</p></div></div>
<div class="stats"><div><b>8</b><span>producteurs locaux</span></div><div><b>12 j</b><span>de tenue en moyenne</span></div><div><b>4,9 / 5</b><span>126 avis Google</span></div></div>
<h2 style="margin-top:80px">Ce qu’ils en disent</h2><div class="quote"><div class="card"><p>« Mon bouquet a tenu douze jours. Je n’avais jamais vu ça. »</p><small>Camille R. · Lyon 1er</small></div><div class="card"><p>« Livré à vélo, sonné à 17 h 05. La carte était écrite à la main, ma mère a pleuré. »</p><small>Antoine D. · Croix-Rousse</small></div><div class="card"><p>« Le mariage de ma sœur : exactement la couleur que je décrivais mal. Ils ont compris. »</p><small>Inès B. · Lyon 6e</small></div></div>
<h2 style="margin-top:80px">Atelier &amp; horaires</h2><div class="fm"><div class="card"><ul class="hr" id="hr"><li data-d="1"><span>Lundi</span><span>Fermé</span></li><li data-d="2"><span>Mardi</span><span>8 h 30 – 19 h 30</span></li><li data-d="3"><span>Mercredi</span><span>8 h 30 – 19 h 30</span></li><li data-d="4"><span>Jeudi</span><span>8 h 30 – 19 h 30</span></li><li data-d="5"><span>Vendredi</span><span>8 h 30 – 20 h</span></li><li data-d="6"><span>Samedi</span><span>8 h – 20 h</span></li><li data-d="0"><span>Dimanche</span><span>9 h – 13 h</span></li></ul><p style="margin-top:18px;color:var(--mut)">14 rue des Tables Claudiennes, Lyon 1er · Métro Hôtel de Ville (ligne A) · 04 78 00 00 00</p></div>
<div class="card faq"><details><summary>Jusqu’à quelle heure commander pour le jour même ?</summary><p>Jusqu’à 11 h pour une livraison avant 18 h, du mardi au samedi.</p></details><details><summary>Combien de temps tiennent les fleurs ?</summary><p>Entre 7 et 14 jours selon la variété. Une fiche d’entretien est glissée dans chaque bouquet.</p></details><details><summary>Livrez-vous en dehors de Lyon ?</summary><p>Lyon 1er à 9e, Villeurbanne et Caluire à vélo. Au-delà, un coursier dès 12 €.</p></details><details><summary>Pouvez-vous choisir pour moi ?</summary><p>Oui. Donnez un budget et une occasion : nous composons avec le plus beau de la matinée.</p></details></div></div></div></section></div>

<div class="view" data-v="panier"><div class="ph"><div class="w"><span class="eb">Paiement à la livraison ou en boutique</span><h1>Ma commande</h1></div></div>
<section class="sec" style="padding-top:20px"><div class="w"><div class="fm"><div class="card"><h3 class="serif">Récapitulatif</h3><ul id="recap"></ul><div class="tot"><span>Total <small id="tsub"></small></span><b id="tt">0 €</b></div><p style="margin-top:20px"><a class="btn" href="#/bouquets">← Continuer mes achats</a></p></div>
<div class="card"><form class="o" id="of"><div class="mode"><label><input type="radio" name="m" value="liv" checked>Livraison à vélo<small>6 € · offerte dès 45 €</small></label><label><input type="radio" name="m" value="ret">Retrait boutique<small>Gratuit · prêt en 1 h</small></label></div>
<label>Jour<select id="dj2"></select></label><label id="adl">Adresse de livraison<input placeholder="12 rue de la République, Lyon 2e"></label>
<label>Nom<input required placeholder="Camille Roux"></label><label>Téléphone<input required inputmode="tel" placeholder="06 00 00 00 00"></label><label>Mot pour la carte (facultatif)<textarea rows="2" placeholder="Pour toi, avec tout mon amour"></textarea></label>
<button class="go" id="go" disabled>Commander</button></form><div class="ok" id="ok"><b>Commande reçue.</b><span id="okt"></span></div></div></div></div></section></div>

</main>
<div class="bar2" id="bar2"><div><b id="b2t"></b><a href="#/panier">Voir mon panier →</a></div></div>
<footer class="ft"><div class="w"><div><a class="logo" href="#/"><img src="/assets/ex/fl-logo.png" alt=""><span><b>PIVOINE</b><small>ATELIER FLORAL</small></span></a><p style="max-width:22em;margin-top:16px">Fleuriste indépendante à Lyon. Fleurs locales et de saison, sans mousse florale.</p></div><div><h4>Boutique</h4><ul><li>14 rue des Tables Claudiennes</li><li>69001 Lyon</li></ul></div><div><h4>Contact</h4><ul><li>04 78 00 00 00</li><li>bonjour@atelier-pivoine.fr</li></ul></div><div><h4>Infos</h4><ul><li>Mentions légales</li><li>CGV</li><li>Confidentialité</li></ul></div>
<div class="legal">© 2026 Atelier Pivoine · SIRET 000 000 000 00000 (exemple) · Hébergeur : Cloudflare, Inc.</div></div></footer>
'''
    for a, b in (("@@TK@@", tk), ("@@SE@@", I_search), ("@@US@@", I_user), ("@@BG@@", I_bag), ("@@BU@@", I_bur), ("@@TR@@", I_truck), ("@@FL@@", I_flower), ("@@MS@@", I_msg),
                 ("@@HC@@", home_cards), ("@@VC@@", vcards), ("@@MK@@", mk), ("@@AC@@", all_cards)):
        body = body.replace(a, b)
    js = r'''<script>(function(){
var V=@@VJS@@,B=@@BJS@@,D=document,cart={},ab=null,$=function(i){return D.getElementById(i)},fav={};
function eur(n){return n.toFixed(2).replace('.',',')+' €'}
function toast(t){var x=$('ts');x.textContent=t;x.classList.add('on');clearTimeout(toast.t);toast.t=setTimeout(function(){x.classList.remove('on')},2200)}
var views=[].slice.call(D.querySelectorAll('.view')),links=[].slice.call(D.querySelectorAll('nav.mn2 a[data-n]'));
function route(){var p=(location.hash||'#/').replace(/^#\/?/,'').split('/'),v=p[0]||'home';if(!D.querySelector('.view[data-v="'+v+'"]'))v='home';
 views.forEach(function(x){x.classList.toggle('on',x.dataset.v===v)});links.forEach(function(a){a.classList.toggle('on',a.dataset.n===v)});
 if(v==='fleurs')filt(p[1]||'');$('nv').classList.remove('on');window.scrollTo(0,0);if(v==='home')D.title='Atelier Pivoine · Fleuriste à Lyon'}
window.addEventListener('hashchange',route);
function filt(c){[].forEach.call(D.querySelectorAll('.chip'),function(x){x.classList.toggle('on',x.dataset.c===c)});[].forEach.call(D.querySelectorAll('.vc'),function(x){x.style.display=(!c||x.dataset.c===c)?'':'none'})}
$('ch').onclick=function(e){var c=e.target.closest('.chip');if(c)location.hash='#/fleurs'+(c.dataset.c?'/'+c.dataset.c:'')};
$('bu').onclick=function(){$('nv').classList.toggle('on')};$('dd').firstChild.addEventListener('click',function(e){if(innerWidth<=980){e.preventDefault();$('dd').classList.toggle('o')}});
$('us').onclick=function(){toast('Espace client : exemple de site, non actif')};$('sr').onclick=function(){location.hash='#/fleurs'};
D.querySelectorAll('.vc .stp').forEach(function(s){s.onclick=function(e){var m=e.target.closest('.mn');if(m)step(s.dataset.k,+m.dataset.a)}});
function step(k,a){k='v:'+k;cart[k]=Math.max(0,(cart[k]||0)+a);if(!cart[k])delete cart[k];draw()}
D.querySelectorAll('.add').forEach(function(b){b.onclick=function(){var k='b:'+b.dataset.b;cart[k]=(cart[k]||0)+1;draw();b.textContent='Ajouté ✓';setTimeout(function(){b.textContent='Ajouter'},1200)}});
D.querySelectorAll('.hrt').forEach(function(h){h.onclick=function(){var on=h.getAttribute('aria-pressed')!=='true';h.setAttribute('aria-pressed',on)}});
D.querySelectorAll('[data-abo]').forEach(function(b){b.onclick=function(){ab=b.dataset.abo;draw();location.hash='#/panier'}});
function lines(){var L=[];V.forEach(function(v){var q=cart['v:'+v[0]];if(q)L.push({id:'v:'+v[0],t:q+' × '+v[1],p:q*v[2]})});B.forEach(function(b,i){var q=cart['b:'+i];if(q)L.push({id:'b:'+i,t:q+' × '+b[0],p:q*b[1]})});if(ab)L.push({id:'ab',t:ab,p:+(/(\d+) €/.exec(ab)||[0,0])[1]});return L}
function mode(){return D.querySelector('input[name=m]:checked').value}
function draw(){var L=lines(),sub=L.reduce(function(s,l){return s+l.p},0),liv=mode()==='liv'&&sub>0&&sub<45?6:0,tot=sub+liv,n=Object.keys(cart).reduce(function(s,k){return s+cart[k]},0)+(ab?1:0);
 V.forEach(function(v){var o=D.querySelector('.stp[data-k='+v[0]+'] output');if(o)o.textContent=cart['v:'+v[0]]||0});
 $('cn').textContent=n;$('cn').style.display=n?'':'none';$('bar2').classList.toggle('on',n>0&&(location.hash||'#/').indexOf('panier')<0);$('b2t').textContent=n+(n>1?' articles · ':' article · ')+eur(tot);
 $('recap').innerHTML=L.length?L.map(function(l){return '<li><span>'+l.t+'<button type="button" data-x="'+l.id+'">retirer</button></span><span>'+eur(l.p)+'</span></li>'}).join('')+(liv?'<li><span>Livraison à vélo</span><span>6,00 €</span></li>':''):'<li class="vide">Votre panier est vide. Ajoutez un bouquet ou des fleurs à la tige.</li>';
 $('tt').textContent=eur(tot);$('tsub').textContent=sub>=45&&mode()==='liv'?'· livraison offerte':'';$('go').disabled=!L.length;$('adl').style.display=mode()==='liv'?'':'none'}
window.addEventListener('hashchange',draw);
$('recap').onclick=function(e){var x=e.target.getAttribute('data-x');if(!x)return;if(x==='ab')ab=null;else delete cart[x];draw()};
D.querySelectorAll('input[name=m]').forEach(function(r){r.onchange=draw});
var j=$('dj2'),n=new Date();for(var i=0;i<6;i++){var d=new Date(n);d.setDate(n.getDate()+i);if(d.getDay()===1)continue;var o=D.createElement('option');o.textContent=(i===0?'Aujourd’hui':i===1?'Demain':d.toLocaleDateString('fr-FR',{weekday:'long',day:'numeric',month:'long'}));j.appendChild(o)}
$('of').onsubmit=function(e){e.preventDefault();$('of').style.display='none';$('ok').classList.add('on');$('okt').textContent='Merci ! Nous préparons votre commande pour '+j.value.toLowerCase()+'. Un SMS vous prévient au départ du coursier.'};
$('qf').onsubmit=function(e){e.preventDefault();$('qf').style.display='none';$('qok').classList.add('on')};
var q=$('qd');if(q){var t=new Date();t.setDate(t.getDate()+1);q.min=t.toISOString().slice(0,10)}
function h(s){var x=0;for(var i=0;i<s.length;i++)x=(x*31+s.charCodeAt(i))|0;return Math.abs(x)}
var day=new Date().toISOString().slice(0,10);D.querySelectorAll('.tb .brr u').forEach(function(u,i){var t=+u.dataset.t,r=Math.round(t*(.35+(h(day+i)%55)/100));u.style.width=Math.min(100,r/t*100)+'%';u.parentNode.parentNode.parentNode.querySelector('[data-s2]').textContent=r;var s=D.querySelectorAll('.vc i[data-r]')[i];if(s)s.textContent=r});
$('dj').textContent='Mis à jour à 8 h 30 · '+new Date().toLocaleDateString('fr-FR',{weekday:'long',day:'numeric',month:'long'});
var li=D.querySelector('#hr li[data-d="'+new Date().getDay()+'"]');if(li)li.classList.add('today');
route();draw()})()</script>'''
    vj = json.dumps([[v[0], v[1], v[5]] for v in V], ensure_ascii=False)
    bj = json.dumps([[b[0], b[2]] for b in B], ensure_ascii=False)
    js = js.replace("@@VJS@@", vj).replace("@@BJS@@", bj)
    return page("Atelier Pivoine · Fleuriste à Lyon", "Fleuriste indépendante à Lyon : bouquets, fleurs à la tige, abonnements, mariages, livraison à vélo.",
                "family=Playfair+Display:wght@500;600;700&family=DM+Sans:wght@400;500;600;700", css, body, js)


# ============================================================ 3. OSTÉOPATHE : « où avez-vous mal ? »
def osteo():
    page, slot, svg = H["page"], H["slot"], H["svg"]
    import json
    Z = [  # id, x, y, titre, ce qu'on voit, séances, à savoir, motif du formulaire
        ("tete", 150, 50, "Tête et mâchoire", "Maux de tête de tension, mâchoire serrée, sensation de pression derrière les yeux.", "1 à 3", "Très souvent lié à la nuque et au stress. Nous cherchons d’abord la cause cervicale.", "Tête / mâchoire"),
        ("nuque", 150, 98, "Nuque et cervicales", "Torticolis, raideur du matin, fourmillements dans le bras, vertiges d’origine cervicale.", "1 à 3", "Les écrans et le sommeil sont les premiers suspects. Je vous montre deux gestes à refaire chez vous.", "Nuque / cervicales"),
        ("epaule", 80, 140, "Épaule", "Douleur en levant le bras, épaule gelée, tendinite, gêne en dormant sur le côté.", "2 à 4", "En cas de chute ou de perte de force soudaine, passez d’abord par une radio.", "Épaule"),
        ("dos", 150, 178, "Haut du dos", "Brûlure entre les omoplates, douleur en respirant profondément, dos « coincé ».", "1 à 3", "Souvent une tension du diaphragme ou des côtes. Rarement grave, toujours soulageable.", "Haut du dos"),
        ("lombes", 150, 285, "Bas du dos", "Lumbago, sciatique, douleur en se levant d’une chaise, blocage après un effort.", "1 à 3", "Si la douleur descend sous le genou avec perte de force, consultez en urgence.", "Bas du dos / lombaires"),
        ("poignet", 44, 352, "Coude et poignet", "Épicondylite, canal carpien, douleur de souris ou de clavier, tennis elbow.", "2 à 4", "Je regarde aussi la nuque et l’épaule : la cause est rarement là où ça fait mal.", "Coude / poignet"),
        ("hanche", 120, 352, "Hanche et bassin", "Douleur dans le pli de l’aine, bassin bloqué, douleurs de grossesse ou post-partum.", "1 à 3", "Techniques adaptées aux femmes enceintes, avec une table réglable.", "Hanche / bassin"),
        ("genou", 124, 492, "Genou et jambe", "Genou de coureur, douleur après un faux mouvement, tendinite, jambe lourde.", "2 à 4", "Apportez vos baskets de sport : je regarde comment vous courez ou marchez.", "Genou / jambe"),
    ]
    zj = json.dumps([[z[0], z[3], z[4], z[5], z[6], z[7]] for z in Z], ensure_ascii=False)
    hot = "".join('<g class="hs" data-z="%s" tabindex="0" role="button" aria-label="%s"><circle class="pl" cx="%d" cy="%d" r="11"/><circle class="dt" cx="%d" cy="%d" r="7"/><text x="%d" y="%d">%d</text></g>' % (z[0], z[3], z[1], z[2], z[1], z[2], z[1], z[2] + 3.5, i + 1) for i, z in enumerate(Z))
    leg = '<path d="M100 335 Q96 420 104 480 Q108 540 112 600 L110 626 L142 626 L144 600 Q148 540 148 480 Q150 430 150 380 L150 340Z"/>'
    arm = '<path d="M72 128 Q52 138 50 176 L40 300 Q34 340 38 372 L46 440 Q55 448 63 440 L69 372 Q75 340 77 300 L90 190Z"/>'
    mir = 'transform="translate(300 0) scale(-1 1)"'
    figure = svg(300, 640, '<g fill="#e3dbc9"><ellipse cx="150" cy="52" rx="27" ry="33"/><path d="M134 78 L134 108 Q150 116 166 108 L166 78Z"/>'
                 '<path d="M108 110 Q150 124 192 110 Q216 118 220 150 L214 262 Q210 300 202 336 L198 352 L102 352 L98 336 Q90 300 86 262 L80 150 Q84 118 108 110Z"/>'
                 + leg + arm + '<g ' + mir + '>' + leg + arm + '</g></g>' + hot).replace('xMidYMid slice', 'xMidYMid meet').replace('aria-hidden="true"', 'role="group" aria-label="Schéma du corps"')
    zj = json.dumps([[z[0], z[3], z[4], z[5], z[6], z[7]] for z in Z], ensure_ascii=False)
    hot = "".join('<g class="hs" data-z="%s" tabindex="0" role="button" aria-label="%s"><circle class="pl" cx="%d" cy="%d" r="11"/><circle class="dt" cx="%d" cy="%d" r="7"/><text x="%d" y="%d">%d</text></g>' % (z[0], z[3], z[1], z[2], z[1], z[2], z[1], z[2] + 3.5, i + 1) for i, z in enumerate(Z))
    leg = '<path d="M100 335 Q96 420 104 480 Q108 540 112 600 L110 626 L142 626 L144 600 Q148 540 148 480 Q150 430 150 380 L150 340Z"/>'
    arm = '<path d="M72 128 Q52 138 50 176 L40 300 Q34 340 38 372 L46 440 Q55 448 63 440 L69 372 Q75 340 77 300 L90 190Z"/>'
    mir = 'transform="translate(300 0) scale(-1 1)"'
    figure = svg(300, 640, '<g fill="#e3dbc9"><ellipse cx="150" cy="52" rx="27" ry="33"/><path d="M134 78 L134 108 Q150 116 166 108 L166 78Z"/>'
                 '<path d="M108 110 Q150 124 192 110 Q216 118 220 150 L214 262 Q210 300 202 336 L198 352 L102 352 L98 336 Q90 300 86 262 L80 150 Q84 118 108 110Z"/>'
                 + leg + arm + '<g ' + mir + '>' + leg + arm + '</g></g>' + hot).replace('xMidYMid slice', 'xMidYMid meet').replace('aria-hidden="true"', 'role="group" aria-label="Schéma du corps"')
    css = r"""
:root{--g:#032a2a;--g2:#0a3d3b;--gold:#b99c64;--gold2:#e8dcc2;--bg:#f9f7f3;--card:#fff;--ink:#0f2a29;--mut:#5f6b69;--ln:#e4ded2}
body{background:var(--bg);color:var(--ink);font:400 17px/1.65 'Inter',system-ui,sans-serif}
h1,h2,h3,h4,.serif{font-family:'Newsreader',Georgia,'Times New Roman',serif;font-weight:500;letter-spacing:-.015em;color:var(--g)}
.w{max-width:1240px;margin:0 auto;padding:0 28px}
header.f{position:sticky;top:0;z-index:60;background:#fefdfa;border-bottom:1px solid #00000008}header.f .w{display:flex;align-items:center;gap:28px;height:96px}
.lg{display:flex;align-items:center;gap:14px;color:var(--g)}.lg img{height:62px;width:auto;mix-blend-mode:multiply;display:block}.lg b{display:block;font:500 1.85rem/1 'Newsreader',Georgia,serif;letter-spacing:-.01em}.lg small{display:block;font:500 .66rem/1 'Inter',sans-serif;letter-spacing:.34em;color:var(--gold);margin-top:8px}
nav.mn2{display:flex;gap:6px;margin:0 auto}nav.mn2 a{padding:10px 20px;font:500 15.5px 'Inter',sans-serif;color:var(--ink);position:relative;white-space:nowrap}nav.mn2 a:hover{color:var(--gold)}nav.mn2 a.on{box-shadow:inset 0 -2px 0 var(--gold)}
.cta{display:inline-flex;align-items:center;gap:12px;background:var(--g);color:#fff;font:500 16px/1 'Inter',sans-serif;padding:18px 26px;border-radius:7px;border:0;cursor:pointer;transition:.25s;white-space:nowrap}.cta:hover{background:var(--g2);transform:translateY(-2px);box-shadow:0 14px 26px #032a2a33}.cta svg{width:20px;height:20px}.cta.o{background:transparent;color:var(--g);box-shadow:inset 0 0 0 1.5px var(--g)}.cta.o:hover{background:var(--g);color:#fff}
.bur{display:none;background:none;border:0;width:46px;height:46px;color:var(--g);cursor:pointer;margin-left:auto}.bur svg{width:26px;height:26px}
.view{display:none;animation:vin .55s cubic-bezier(.2,.8,.2,1)}.view.on{display:block}@keyframes vin{from{opacity:0;transform:translateY(14px)}}
.eb{font:500 13px/1 'Inter',sans-serif;letter-spacing:.26em;text-transform:uppercase;color:var(--ink)}.eb:after{content:"";display:block;width:76px;height:2px;background:var(--gold);margin-top:22px}.eb.c{text-align:center}.eb.c:after{margin:20px auto 0}
.hero{position:relative;overflow:hidden;min-height:690px;display:flex;align-items:center}.hero .ph{position:absolute;right:0;top:0;bottom:0;width:66%}.hero .ph img{width:100%;height:100%;object-fit:cover;object-position:left center;display:block;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 34%);mask-image:linear-gradient(90deg,transparent 0,#000 34%);animation:kb 22s ease-in-out infinite alternate;transform-origin:70% 60%}@keyframes kb{to{transform:scale(1.07)}}
.hero .w{position:relative;width:100%}.hero .tx{max-width:620px;padding:70px 0}
h1{font-size:clamp(2.9rem,5.4vw,4.8rem);line-height:1.06;margin:34px 0 28px}
.lead{font-size:1.28rem;line-height:1.55;max-width:25em;color:var(--ink)}
.hero .cta{margin-top:42px}
.ind{background:#f5f3ef}.ind .w{display:grid;grid-template-columns:repeat(4,1fr)}.ind a{display:flex;align-items:center;justify-content:center;gap:18px;padding:34px 18px;font:500 1.12rem/1.35 'Newsreader',Georgia,serif;color:var(--g);transition:.3s;position:relative}.ind a+a:before{content:"";position:absolute;left:0;top:28%;bottom:28%;width:1px;background:#d9d1c1}.ind a:hover{color:var(--gold)}.ind a:hover img{transform:translateY(-4px) scale(1.08)}.ind img{height:58px;width:auto;mix-blend-mode:multiply;transition:.3s}
.sec{padding:96px 0 0}.sec h2{font-size:clamp(2.1rem,3.8vw,3.2rem);line-height:1.1;margin:0 0 20px}.sub{color:var(--mut);max-width:38em;font-size:1.1rem}.c{text-align:center}.c .sub{margin:0 auto}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:46px}.box{background:var(--card);border-radius:20px;padding:34px 30px;box-shadow:0 8px 30px #032a2a0d;transition:.35s;position:relative}.box:hover{transform:translateY(-6px);box-shadow:0 22px 44px #032a2a1c}.box .t{font:500 12px 'Inter',sans-serif;letter-spacing:.22em;text-transform:uppercase;color:var(--gold)}.box h3{font-size:1.6rem;margin:12px 0 10px}.box p{color:var(--mut);font-size:16px}.box .big{font:500 3.2rem/1 'Newsreader',Georgia,serif;color:var(--gold)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center;margin-top:20px}.split img{width:100%;border-radius:24px;display:block;aspect-ratio:4/3;object-fit:cover;box-shadow:0 24px 50px #032a2a22}.split h2{margin-top:6px}.split p{color:var(--mut);margin-bottom:14px}
.ph2{padding:70px 0 56px;text-align:center;background:linear-gradient(180deg,#f4f1ea,var(--bg))}.ph2 h1{margin:26px auto 16px}.ph2 .sub{margin:0 auto}
.qt{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:44px}.qt .box p{font:italic 400 1.2rem/1.5 'Newsreader',Georgia,serif;color:var(--g)}.qt small{display:block;margin-top:16px;color:var(--mut);font-size:14px}
.cb{margin:90px auto 0;max-width:1184px;background:var(--g);color:#fff;border-radius:28px;padding:56px 60px;display:flex;justify-content:space-between;align-items:center;gap:30px;flex-wrap:wrap}.cb h2{color:#fff;margin:0;max-width:16em}.cb .cta{background:var(--gold);color:var(--g)}.cb .cta:hover{background:#fff}.bw{padding:0 28px}
.pt{margin-top:30px}.pt li{display:flex;justify-content:space-between;align-items:baseline;padding:20px 0;border-bottom:1px solid var(--ln);font-size:18px}.pt b{font:500 2rem 'Newsreader',Georgia,serif;color:var(--g)}.note{margin-top:22px;color:var(--mut);font-size:15px;max-width:40em}
.stp li{display:grid;grid-template-columns:120px 1fr;gap:24px;padding:26px 0;border-bottom:1px solid var(--ln)}.stp b{font:500 2.6rem/1 'Newsreader',Georgia,serif;color:var(--gold)}.stp h3{font-size:1.5rem;margin-bottom:4px}.stp p{color:var(--mut);max-width:38em}
.faq details{border-bottom:1px solid var(--ln);padding:22px 0}.faq summary{cursor:pointer;font:500 1.35rem/1.25 'Newsreader',Georgia,serif;color:var(--g);list-style:none;display:flex;justify-content:space-between;gap:20px}.faq summary::-webkit-details-marker{display:none}.faq summary:after{content:"+";color:var(--gold);font-size:1.7rem;line-height:1}.faq details[open] summary:after{content:"–"}.faq p{margin-top:10px;color:var(--mut);max-width:44em}
.stage{display:grid;grid-template-columns:1.05fr .95fr;background:radial-gradient(ellipse 70% 80% at 35% 50%,#0f4a46 0,#032a2a 75%);border-radius:30px;overflow:hidden;margin-top:44px;color:#f4efe4;min-height:640px}
.body{position:relative;min-height:620px}.body .cv{position:absolute;inset:0}.body .fb{display:none;height:100%;justify-content:center;align-items:center}.body.nogl .fb{display:flex}.body.nogl .cv{display:none}.body svg{width:min(100%,300px);height:auto;max-height:100%}.tip{position:absolute;left:0;right:0;bottom:12px;text-align:center;font:500 11.5px 'Inter',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#a9bdb8;pointer-events:none}.rs{position:absolute;top:16px;left:16px;background:transparent;border:1.5px solid #ffffff55;color:#fff;font:500 13px 'Inter',sans-serif;padding:10px 16px;border-radius:99px;cursor:pointer;display:none;z-index:3}.rs.on{display:block}.rs:hover{background:#fff;color:var(--g)}
.pan{padding:46px 44px;align-self:center}.pan .t{font:500 12px 'Inter',sans-serif;letter-spacing:.22em;text-transform:uppercase;color:var(--gold)}.pan h2{color:#fff;font-size:2.2rem;margin:12px 0 12px}.pan p{color:#cbd9d5;font-size:16.5px}.pan .mt{display:flex;gap:28px;margin:18px 0}.pan .mt b{display:block;font:500 2.4rem/1 'Newsreader',Georgia,serif;color:var(--gold)}.pan .mt span{color:#cbd9d5;font-size:14px}.pan .cta{background:var(--gold);color:var(--g);margin-top:12px}.pan .cta:hover{background:#fff}
.hs{cursor:pointer}.hs .pl{fill:var(--gold);opacity:.28;transform-box:fill-box;transform-origin:center;animation:pu 2.2s ease-out infinite}.hs .dt{fill:var(--gold);stroke:#032a2a;stroke-width:2.5}.hs text{font:700 9px 'Inter',sans-serif;fill:#fff;text-anchor:middle;pointer-events:none}.hs.on .dt{fill:#fff;stroke:var(--gold);stroke-width:3}.hs.on text{fill:var(--g)}.hs:focus{outline:0}@keyframes pu{0%{transform:scale(.7);opacity:.5}100%{transform:scale(1.9);opacity:0}}
.zl{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:26px}.zl button{border:1.5px solid var(--ln);background:#fff;border-radius:99px;padding:10px 18px;font:500 14.5px 'Inter',sans-serif;color:var(--g);cursor:pointer;transition:.2s}.zl button:hover,.zl button.on{background:var(--g);border-color:var(--g);color:#fff}
.hr li{display:flex;justify-content:space-between;padding:14px 0;border-bottom:1px solid var(--ln)}.hr li.today{font-weight:600;color:var(--gold)}
.pr{display:grid;grid-template-columns:300px 1fr;gap:44px;align-items:start;margin-top:30px}.pr .pp{aspect-ratio:.82;border-radius:24px;overflow:hidden;background:var(--g)}.pr .pp .sl svg{width:100%;height:100%}.pr p{color:var(--mut);margin-bottom:14px}.dp li{display:grid;grid-template-columns:70px 1fr;padding:12px 0;border-bottom:1px solid var(--ln);font-size:15.5px}.dp li b{font:500 1.2rem 'Newsreader',Georgia,serif;color:var(--gold)}
.bk{display:grid;grid-template-columns:1.2fr .8fr;gap:34px;margin-top:44px}.bk>div{min-width:0}.lab{font:500 12px 'Inter',sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:14px}
.days{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding:4px 2px}.days::-webkit-scrollbar{display:none}
.dy{flex:0 0 auto;min-width:78px;border:1.5px solid var(--ln);background:#fff;color:var(--g);padding:12px 6px;text-align:center;cursor:pointer;font:500 12.5px/1.3 'Inter',sans-serif;border-radius:14px;transition:.2s}.dy b{display:block;font:500 2rem/1.1 'Newsreader',Georgia,serif}.dy:hover{border-color:var(--gold)}.dy.on{background:var(--g);color:#fff;border-color:var(--g)}.dy.full{opacity:.35;pointer-events:none}
.slots{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}.sl2{border:1.5px solid var(--ln);background:#fff;color:var(--g);padding:14px 0;font:500 16px 'Inter',sans-serif;cursor:pointer;border-radius:12px;transition:.2s}.sl2:hover{border-color:var(--gold)}.sl2.on{background:var(--gold);color:var(--g);border-color:var(--gold)}.sl2.x{opacity:.3;text-decoration:line-through;pointer-events:none}
.card{background:#fff;border-radius:24px;padding:34px;box-shadow:0 8px 30px #032a2a0d}.rec{padding:6px 0 16px;margin-bottom:12px;border-bottom:1px solid var(--ln);min-height:84px}.rec b{display:block;font:500 1.6rem/1.15 'Newsreader',Georgia,serif;color:var(--g)}.rec span{color:var(--mut);font-size:15px}
.card form{display:grid;gap:16px}.card label{display:grid;gap:6px;font:500 13px 'Inter',sans-serif;color:var(--mut)}.card input,.card select{font:400 16px 'Inter',sans-serif;padding:14px 16px;border:1.5px solid var(--ln);border-radius:12px;background:var(--bg);color:var(--ink)}.card input:focus,.card select:focus{outline:0;border-color:var(--gold);background:#fff}
.go{background:var(--g);color:#fff;border:0;padding:18px;font:500 16px 'Inter',sans-serif;border-radius:10px;cursor:pointer;transition:.2s}.go:disabled{opacity:.4;cursor:not-allowed}.go:not(:disabled):hover{background:var(--g2)}
.done{display:none;background:#eef4ef;border-radius:16px;padding:24px}.done.on{display:block}.done b{font:500 1.7rem 'Newsreader',Georgia,serif;display:block;margin-bottom:6px;color:var(--g)}
.ct{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:40px}
footer.ft{margin-top:100px;background:var(--g);color:#bccdc9;padding:60px 0 34px}footer.ft .w{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:34px}footer.ft .lg,footer.ft .lg b{color:#fff}footer.ft .lg img{mix-blend-mode:screen;filter:grayscale(1) invert(1) brightness(1.5)}footer.ft h4{font:500 12px 'Inter',sans-serif;letter-spacing:.2em;color:var(--gold);margin-bottom:14px;text-transform:uppercase}footer.ft li{margin:8px 0;font-size:15px}.legal{grid-column:1/-1;border-top:1px solid #ffffff22;padding-top:22px;font-size:13px;color:#8aa09b;margin-top:16px}
@media(prefers-reduced-motion:reduce){.hero .ph img{animation:none}.view{animation:none}}
@media(max-width:980px){header.f .w{height:78px;gap:10px}.lg img{height:50px}.lg b{font-size:1.5rem}.lg small{font-size:.58rem}.bur{display:grid;place-items:center}header.f .cta{display:none}
 nav.mn2{position:fixed;left:0;right:0;top:78px;background:#fefdfa;flex-direction:column;gap:0;padding:6px 24px 22px;margin:0;transform:translateY(-130%);transition:transform .35s;z-index:55;box-shadow:0 20px 30px #0002}nav.mn2.on{transform:none}nav.mn2 a{padding:16px 0;border-bottom:1px solid var(--ln)}nav.mn2 a.on{box-shadow:none;color:var(--gold)}
 .hero{min-height:0;flex-direction:column;align-items:stretch}.hero .ph{position:relative;width:100%;height:340px;order:2}.hero .ph img{-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 30%);mask-image:linear-gradient(180deg,transparent 0,#000 30%);object-position:center}.hero .tx{padding:44px 0 14px}.ind .w{grid-template-columns:1fr 1fr}.ind a:nth-child(3):before{display:none}.three,.qt,.ct{grid-template-columns:1fr}.split,.pr,.bk{grid-template-columns:1fr;gap:30px}.stage{grid-template-columns:1fr}.body{min-height:460px}.pan{padding:30px 24px 38px}.pr{max-width:none}.pr .pp{max-width:260px}footer.ft .w{grid-template-columns:1fr 1fr}.cb{padding:38px 28px;margin-left:16px;margin-right:16px}.slots{grid-template-columns:repeat(3,1fr)}.sec{padding-top:70px}.stp li{grid-template-columns:90px 1fr}}
@media(max-width:600px){.w{padding:0 18px}.hero .tx{padding:30px 0 10px}.eb:after{margin-top:14px}h1{margin:22px 0 18px}.lead{font-size:1.1rem}.hero .cta{margin-top:28px;width:100%;justify-content:center}.ind a{flex-direction:column;gap:10px;text-align:center;padding:26px 10px;font-size:1rem}.card{padding:24px 20px}h1{font-size:2.6rem}}
"""
    ico_cal = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3.500" y="5" width="17" height="15" rx="2"/><path d="M3.500 10h17M8 3v4M16 3v4"/><path d="M8 14h.01M12 14h.01M16 14h.01M8 17h.01M12 17h.01"/></svg>'
    ico_bur = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
    arrow = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h16M14 6l6 6-6 6"/></svg>'
    portrait = slot("osteo-portrait", svg(420, 520, '<rect width="420" height="520" fill="#032a2a"/><text x="210" y="320" text-anchor="middle" font-family="Georgia,serif" font-weight="500" font-size="190" fill="#e8dcc2">LL</text><text x="30" y="494" font-family="system-ui,sans-serif" font-size="15" fill="#8aa09b">Photo de la praticienne</text>'))
    zb = "".join('<button type="button" data-z="%s">%s</button>' % (z[0], z[3]) for z in Z)
    body = """
<header class="f"><div class="w"><a class="lg" href="#/"><img src="/assets/ex/os-logo.png" alt=""><span><b>Cabinet Lemaire</b><small>OSTÉOPATHE D.O.</small></span></a>
<nav class="mn2" id="nv"><a href="#/" data-n="home">Accueil</a><a href="#/osteopathie" data-n="osteopathie">L’ostéopathie</a><a href="#/indications" data-n="indications">Indications</a><a href="#/cabinet" data-n="cabinet">Le cabinet</a><a href="#/contact" data-n="contact">Contact</a></nav>
<a class="cta" href="#/contact">@@CAL@@Prendre rendez-vous</a><button class="bur" type="button" id="bu" aria-label="Menu">@@BUR@@</button></div></header>
<main id="top">

<div class="view" data-v="home"><section class="hero"><div class="ph"><img src="/assets/ex/os-hero.jpg" alt="Salle de soin du cabinet"></div><div class="w"><div class="tx"><span class="eb">Ostéopathie</span><h1>Un accompagnement<br>pour votre équilibre</h1><p class="lead">Soulager les douleurs, améliorer la mobilité et prévenir les déséquilibres, à chaque étape de la vie.</p><a class="cta" href="#/contact">@@CAL@@Prendre rendez-vous <span style="margin-left:14px">@@AR@@</span></a></div></div></section>
<div class="ind"><div class="w"><a href="#/indications/nuque"><img src="/assets/ex/os-i1.png" alt=""><span class="lt">Douleurs du dos<br>et des cervicales</span></a><a href="#/indications/genou"><img src="/assets/ex/os-i2.png" alt=""><span class="lt">Troubles<br>articulaires</span></a><a href="#/indications/genou"><img src="/assets/ex/os-i3.png" alt=""><span class="lt">Suivi sportif<br>et prévention</span></a><a href="#/indications/hanche"><img src="/assets/ex/os-i4.png" alt=""><span class="lt">Grossesse<br>et post-partum</span></a></div></div>
<section class="sec"><div class="w c"><span class="eb c">Une séance</span><h2>Une heure, trois temps.<br>Pas de précipitation.</h2><div class="three" style="text-align:left"><div class="box"><span class="t">15 min</span><h3>L’échange</h3><p>Vous racontez votre douleur, votre histoire, votre quotidien. J’écoute avant de toucher.</p></div><div class="box"><span class="t">10 min</span><h3>L’examen</h3><p>Tests de mobilité, observation de la posture, palpation : je cherche ce qui se bloque vraiment.</p></div><div class="box"><span class="t">35 min</span><h3>Le soin</h3><p>Techniques douces, adaptées à votre état, et des gestes simples à refaire chez vous.</p></div></div></div></section>
<section class="sec"><div class="w c"><span class="eb c">Avis patients</span><h2>4,9 sur 5, 87 avis</h2><div class="qt" style="text-align:left"><div class="box"><p>« Enfin une consultation où l’on prend le temps. Mon mal de dos chronique s’est apaisé dès la deuxième séance. »</p><small>Claire B. · Chartrons</small></div><div class="box"><p>« Très douce avec mon bébé de trois semaines. Tout est expliqué avec calme, et ça a marché. »</p><small>Julien M. · papa d’Éloïse</small></div><div class="box"><p>« Je cours des marathons : elle a trouvé l’origine de mon genou en vingt minutes. »</p><small>Thomas R. · coureur</small></div></div></div>
<div class="bw"><div class="cb"><h2>Un premier rendez-vous sous 48 h</h2><a class="cta" href="#/contact">@@CAL@@Choisir mon créneau</a></div></div></section></div>

<div class="view" data-v="osteopathie"><div class="ph2"><div class="w"><span class="eb c">L’ostéopathie</span><h1>Une approche douce et globale</h1><p class="sub">Un corps est un ensemble : la douleur est rarement là où se trouve la cause. Je cherche l’origine, je ne traite pas que le symptôme.</p></div></div>
<section class="sec" style="padding-top:30px"><div class="w"><div class="split"><img src="/assets/ex/os-cabinet.jpg" alt=""><div><h2>Comment se passe une séance</h2><ul class="stp"><li><b>15 min</b><div><h3>L’échange</h3><p>Votre histoire, vos douleurs, votre quotidien.</p></div></li><li><b>10 min</b><div><h3>L’examen</h3><p>Mobilité, posture, palpation.</p></div></li><li><b>35 min</b><div><h3>Le soin</h3><p>Techniques douces et conseils pour la maison.</p></div></li></ul></div></div>
<div style="margin-top:80px;max-width:760px"><span class="eb">Tarifs</span><h2 style="margin-top:26px">Des prix affichés d’avance, sans supplément.</h2><ul class="pt"><li><span>Adulte</span><b>60 €</b></li><li><span>Enfant de 2 à 12 ans</span><b>45 €</b></li><li><span>Nourrisson (moins de 2 ans)</span><b>50 €</b></li><li><span>Femme enceinte</span><b>55 €</b></li></ul><p class="note">Paiement par carte, espèces ou chèque. Facture remise à chaque séance pour votre mutuelle (la Sécurité sociale ne rembourse pas l’ostéopathie). Annulation gratuite jusqu’à 24 h avant ; un rendez-vous manqué sans prévenir est facturé 30 €.</p></div>
<div style="margin-top:80px;max-width:820px" class="faq"><span class="eb">Questions fréquentes</span><h2 style="margin:26px 0 10px">On répond avant que vous demandiez.</h2><details><summary>Combien de séances faut-il prévoir ?</summary><p>Une à trois suffisent le plus souvent. Si le problème est ancien, nous convenons d’un rythme ensemble, jamais d’un forfait imposé.</p></details><details><summary>Faut-il une ordonnance ?</summary><p>Non. Apportez vos radios, IRM et comptes rendus récents s’il y en a : ils m’aident à adapter le soin.</p></details><details><summary>Est-ce douloureux ?</summary><p>Non. Les techniques sont douces ; vous pouvez m’arrêter à tout moment.</p></details><details><summary>Recevez-vous les bébés et les femmes enceintes ?</summary><p>Oui, dès les premières semaines de vie et pendant toute la grossesse, avec des techniques et une table adaptées.</p></details></div></div></section></div>

<div class="view" data-v="indications"><div class="ph2"><div class="w"><span class="eb c">Indications</span><h1>Où avez-vous mal ?</h1><p class="sub">Faites tourner le squelette, touchez la zone qui vous gêne : je vous dis ce que l’on y voit le plus souvent et combien de séances il faut.</p></div></div>
<section class="sec" style="padding-top:0"><div class="w"><div class="stage"><div class="body" id="bd"><div class="cv" id="cv"></div><div class="fb">@@FIG@@</div><button class="rs" id="rs" type="button">Vue d’ensemble</button><div class="tip">Glissez pour tourner · touchez un point</div></div>
<div class="pan" id="pan" aria-live="polite"></div></div><div class="zl" id="zl">@@ZB@@</div></div></section></div>

<div class="view" data-v="cabinet"><div class="ph2"><div class="w"><span class="eb c">Le cabinet</span><h1>Léa Lemaire, ostéopathe D.O.</h1><p class="sub">Un cabinet lumineux de plain-pied, aux Chartrons, pensé pour prendre le temps.</p></div></div>
<section class="sec" style="padding-top:20px"><div class="w"><div class="pr"><div class="pp">@@PT@@</div><div><h2 style="margin:0 0 16px">Ma pratique</h2><p>Diplômée en 2014 après cinq ans d’études, j’ai accompagné une équipe de handball avant d’ouvrir mon cabinet aux Chartrons. J’aime les consultations longues, les questions simples et les explications claires.</p><p>Je me forme chaque année. Et je préfère vous revoir une fois de moins que de vous faire revenir pour rien.</p><ul class="dp"><li><b>2014</b><span>Diplôme d’ostéopathe D.O., Bordeaux</span></li><li><b>2017</b><span>Formation en ostéopathie pédiatrique</span></li><li><b>2021</b><span>Périnatalité et suivi post-partum</span></li></ul></div></div>
<div class="split" style="margin-top:80px"><div><h2>Venir au cabinet</h2><p>27 cours Saint-Louis, 33300 Bordeaux<br>Tram C, arrêt Chartrons, à 3 minutes à pied. Parking Saint-Louis à 100 m. Cabinet de plain-pied, accessible aux personnes à mobilité réduite.</p><p>05 56 00 00 00<br>cabinet@lemaire-osteo.fr</p><p style="margin-top:18px"><a class="cta" href="#/contact">@@CAL@@Prendre rendez-vous</a></p></div><img src="/assets/ex/os-hero.jpg" alt="" style="object-position:left center"></div></div></section></div>

<div class="view" data-v="contact"><div class="ph2"><div class="w"><span class="eb c">Rendez-vous en ligne</span><h1>Choisissez votre créneau</h1><p class="sub">Un SMS de confirmation, un rappel la veille. Annulation gratuite jusqu’à 24 h avant.</p></div></div>
<section class="sec" style="padding-top:10px"><div class="w">@@RZ@@<div class="resa-demo" style="margin-top:34px;border-radius:14px">Vous êtes le cabinet ? Voyez ce que vous recevez de votre côté : agenda, statistiques de réservation. <a href="/exemples/osteo-reservation-interne" target="_blank" rel="noopener">Ouvrir l’espace du cabinet →</a></div><div class="ct"><div class="box"><span class="t">Horaires</span><ul class="hr" id="hr" style="margin-top:10px"><li data-d="1"><span>Lundi</span><span>9 h – 19 h</span></li><li data-d="2"><span>Mardi</span><span>9 h – 19 h</span></li><li data-d="3"><span>Mercredi</span><span>9 h – 18 h</span></li><li data-d="4"><span>Jeudi</span><span>9 h – 19 h</span></li><li data-d="5"><span>Vendredi</span><span>9 h – 17 h</span></li><li data-d="6"><span>Samedi</span><span>9 h – 13 h</span></li><li data-d="0"><span>Dimanche</span><span>Fermé</span></li></ul></div>
<div class="box"><span class="t">Adresse</span><h3>27 cours Saint-Louis</h3><p>33300 Bordeaux<br>Tram C, arrêt Chartrons<br>Parking Saint-Louis à 100 m</p></div><div class="box"><span class="t">Nous joindre</span><h3>05 56 00 00 00</h3><p>cabinet@lemaire-osteo.fr<br>Réponse sous 24 h, du lundi au samedi.</p></div></div></div></section></div>

</main>
<footer class="ft"><div class="w"><div><a class="lg" href="#/"><img src="/assets/ex/os-logo.png" alt=""><span><b>Cabinet Lemaire</b><small>OSTÉOPATHE D.O.</small></span></a><p style="max-width:22em;margin-top:16px">Ostéopathie pour adultes, enfants et nourrissons, à Bordeaux Chartrons.</p></div><div><h4>Contact</h4><ul><li>05 56 00 00 00</li><li>cabinet@lemaire-osteo.fr</li></ul></div><div><h4>Adresse</h4><ul><li>27 cours Saint-Louis</li><li>33300 Bordeaux</li></ul></div><div><h4>Infos</h4><ul><li>Mentions légales</li><li>Confidentialité</li><li>Données de santé</li></ul></div>
<div class="legal">© 2026 Cabinet Lemaire · Ostéopathe D.O., n° ADELI 33 00 00000 (exemple) · SIRET 000 000 000 00000 (exemple) · Hébergeur : Cloudflare, Inc.</div></div></footer>
"""
    body = body.replace("@@CAL@@", ico_cal).replace("@@BUR@@", ico_bur).replace("@@AR@@", arrow).replace("@@FIG@@", figure).replace("@@PT@@", portrait).replace("@@ZB@@", zb)
    js = r"""<script>(function(){
var Z=@@ZJ@@,D=document,$=function(i){return D.getElementById(i)},pan=$('pan'),hs=[].slice.call(D.querySelectorAll('.hs')),zl=[].slice.call(D.querySelectorAll('#zl button'));
var views=[].slice.call(D.querySelectorAll('.view')),links=[].slice.call(D.querySelectorAll('nav.mn2 a'));
var api=null,loaded=false,cur=null;
function intro(){pan.innerHTML='<span class="t">Choisissez un point sur le corps</span><h2>Huit zones, une seule question.</h2><p>Chaque point est une raison fréquente de consultation. Si votre douleur est ailleurs, prenez rendez-vous : on la trouvera ensemble.</p>'}
function show(id){var z=Z.filter(function(x){return x[0]===id})[0];if(!z)return;cur=id;hs.forEach(function(h){h.classList.toggle('on',h.dataset.z===id)});zl.forEach(function(b){b.classList.toggle('on',b.dataset.z===id)});
 pan.innerHTML='<span class="t">Zone '+(Z.indexOf(z)+1)+' sur '+Z.length+'</span><h2>'+z[1]+'</h2><p>'+z[2]+'</p><div class="mt"><div><b>'+z[3]+'</b><span>séances en général</span></div></div><p style="font-size:15px">'+z[4]+'</p><p><a class="cta" href="#/contact" data-m="'+z[5]+'">Réserver pour cette zone</a></p>';$('rs').classList.add('on')}
function show3(id){if(!id){cur=null;intro();$('rs').classList.remove('on');hs.forEach(function(h){h.classList.remove('on')});zl.forEach(function(b){b.classList.remove('on')});return}show(id)}
function load3(){if(loaded)return;loaded=true;import('/assets/ex/osteo3d.js').then(function(m){api=m.init({el:$('cv'),onSelect:show3});window.osteo3d=api;if(!api)$('bd').classList.add('nogl')}).catch(function(){$('bd').classList.add('nogl')})}
function route(){var p=(location.hash||'#/').replace(/^#\/?/,'').split('/'),v=p[0]||'home';if(!D.querySelector('.view[data-v="'+v+'"]'))v='home';
 views.forEach(function(x){x.classList.toggle('on',x.dataset.v===v)});links.forEach(function(a){a.classList.toggle('on',a.dataset.n===v)});$('nv').classList.remove('on');window.scrollTo(0,0);
 if(v==='indications'){load3();if(p[1]){show(p[1]);if(api)api.select(p[1],true);else setTimeout(function(){if(api)api.select(p[1],true)},900)}}}
window.addEventListener('hashchange',route);
$('bu').onclick=function(){$('nv').classList.toggle('on')};
$('rs').onclick=function(){if(api)api.reset();else{intro();$('rs').classList.remove('on')}};
hs.forEach(function(h){h.onclick=function(){show(h.dataset.z);if(api)api.select(h.dataset.z,true)};h.onkeydown=function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();show(h.dataset.z)}}});
$('zl').onclick=function(e){var b=e.target.closest('button');if(b){show(b.dataset.z);if(api)api.select(b.dataset.z,true)}};
pan.onclick=function(e){var m=e.target.getAttribute&&e.target.getAttribute('data-m');if(m)D.dispatchEvent(new CustomEvent('osteo-motif',{detail:m}))};
intro();
var li=D.querySelector('#hr li[data-d="'+new Date().getDay()+'"]');if(li)li.classList.add('today');
route()})()</script>"""
    js = js.replace("@@ZJ@@", zj)
    import osteo_resa
    _wh, _wc, _wj = osteo_resa.widget()
    body = body.replace("@@RZ@@", _wh)
    css += _wc
    js += "<script>" + _wj + "</script>"
    return page("Cabinet Lemaire · Ostéopathe à Bordeaux Chartrons", "Ostéopathe D.O. à Bordeaux Chartrons : adultes, enfants, nourrissons, femmes enceintes. Rendez-vous en ligne.",
                "family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=Inter:wght@400;500;600", css, body, js)
