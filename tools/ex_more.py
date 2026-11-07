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
    page, slot, svg, ico = H["page"], H["slot"], H["svg"], H["ico"]
    css = r'''
:root{--bg:#fff;--p:#f3f1ea;--p2:#fff;--ink:#111;--mut:#555a63;--or:#1a3cff;--y:#ffd400;--ln:#dcd9cf}
html,body{overflow-x:clip}
body{background:var(--bg);color:var(--ink);font:400 17px/1.6 'Barlow',system-ui,sans-serif}
.c{font-family:'Barlow Condensed','Arial Narrow','Liberation Sans Narrow',sans-serif;text-transform:uppercase;letter-spacing:.01em}
.w{max-width:1280px;margin:0 auto;padding:0 28px}
.top{background:#111;font-size:14px}.top .w{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-top:9px;padding-bottom:9px;color:#c9ccd2}.top .live{color:#fff}
.live{display:inline-flex;align-items:center;gap:8px;font-weight:600;color:var(--ink)}.live i{width:9px;height:9px;border-radius:50%;background:#2fd06a;box-shadow:0 0 0 0 #2fd06a99;animation:pl 2s infinite}.live.off i{background:#e0483a;animation:none}
@keyframes pl{70%{box-shadow:0 0 0 9px #2fd06a00}100%{box-shadow:0 0 0 0 #2fd06a00}}
@media(prefers-reduced-motion:reduce){.live i,.mq div{animation:none}}
header.g{position:sticky;top:0;z-index:40;background:#fffffff2;backdrop-filter:blur(12px);border-bottom:1px solid var(--ln)}
header.g .w{display:flex;justify-content:space-between;align-items:center;height:78px;gap:20px}@media(max-width:600px){header.g .w{height:64px;gap:10px;padding:0 14px}header.g .lg{font-size:1.25rem;gap:8px}header.g .lg small{display:none}header.g .bt{padding:12px 14px;font-size:14px}header.o .lg{font-size:1.4rem}}
.lg{display:flex;align-items:center;gap:12px;font:800 1.9rem/1 'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.04em}.lg small{display:block;font:600 .62rem/1 'Barlow',sans-serif;letter-spacing:.3em;color:var(--mut);margin-top:5px}
.lg i{display:grid;place-items:center;width:44px;height:44px;background:var(--y);clip-path:polygon(0 0,100% 0,100% 70%,70% 100%,0 100%)}
nav.g{display:flex;gap:30px;font:600 15px 'Barlow',sans-serif;text-transform:uppercase;letter-spacing:.1em}nav.g a{color:var(--mut)}nav.g a:hover{color:var(--or)}
.bt{display:inline-flex;align-items:center;gap:10px;background:var(--y);color:#111;font:700 16px/1 'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.08em;padding:17px 26px;border:0;cursor:pointer;clip-path:polygon(0 0,100% 0,100% calc(100% - 12px),calc(100% - 12px) 100%,0 100%);transition:.2s}
.bt:hover{background:#111;color:#fff}.bt.o{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 2px var(--ln);clip-path:none}.bt.o:hover{box-shadow:inset 0 0 0 2px var(--or);background:transparent;color:var(--or)}
.hero{position:relative;overflow:hidden;background:#1a3cff;color:#fff}.hero .lead{color:#dbe3ff}.hero .tg{border-color:#ffffff66;color:#fff}.hero .tg b{color:var(--y)}.hero h1.c em{color:var(--y)}.hero .lb{color:var(--y)}
.hero:before{content:"";position:absolute;inset:0;background:radial-gradient(900px 520px at 78% 40%,#ffffff22,transparent 60%),repeating-linear-gradient(90deg,#ffffff0f 0 1px,transparent 1px 90px)}
.hero .w{position:relative;display:grid;grid-template-columns:1.05fr 1fr;gap:20px;align-items:center;padding-top:70px;padding-bottom:40px}
.tg{display:inline-flex;gap:10px;align-items:center;border:1px solid var(--ln);padding:8px 14px;font:600 13px/1 'Barlow',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}.tg b{color:var(--or)}
h1.c{font-weight:800;font-size:clamp(3.2rem,7.4vw,7.4rem);line-height:.88;margin:26px 0 22px;letter-spacing:-.005em}h1.c em{font-style:normal;color:var(--or)}
.lead{color:var(--mut);font-size:1.18rem;max-width:30em}
.devis{margin-top:32px;background:#fff;color:#111;box-shadow:8px 8px 0 #111;padding:22px;display:grid;grid-template-columns:auto 1fr 1fr auto;gap:12px;align-items:end;max-width:760px}
.devis label{display:grid;gap:7px;font:600 12px 'Barlow',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.plate{display:flex;align-items:stretch;background:#fff;border-radius:6px;overflow:hidden;height:50px;min-width:190px;box-shadow:0 0 0 2px #111}.plate b{width:30px;background:#133b9c;color:#fff;display:grid;place-items:end center;padding-bottom:4px;font:700 11px 'Barlow'}.plate input{border:0;outline:0;font:800 1.55rem 'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.12em;text-align:center;width:100%;color:#111;background:#fff}
.devis select{height:50px;background:var(--p2);color:var(--ink);border:1px solid var(--ln);font:500 16px 'Barlow',sans-serif;padding:0 12px}
.est{grid-column:1/-1;display:none;align-items:center;gap:16px;border-top:1px dashed var(--ln);padding-top:16px;flex-wrap:wrap}.est.on{display:flex}.est b{font:800 2.4rem/1 'Barlow Condensed',sans-serif;color:var(--or)}.est .bt{margin-left:auto}.est span{color:var(--mut);font-size:15px}
.stage{position:relative}.stage>svg:not(.dl){display:block;width:100%;height:auto}.stage .dl{position:absolute;right:3%;top:-16%;width:27%;height:auto;opacity:.96;z-index:2}
.kpi{position:relative;display:grid;grid-template-columns:repeat(4,1fr);background:#111;color:#fff}
.kpi div{padding:24px 28px;border-right:1px solid #2b2e35}.kpi div:last-child{border:0}.kpi b{display:block;font:800 2.5rem/1 'Barlow Condensed',sans-serif;color:var(--y)}.kpi span{color:#aeb2ba;font-size:15px}
section.s{padding:100px 0;border-bottom:1px solid var(--ln)}#forfaits,#equipe{background:var(--p)}.sg{border-color:#111}.sv{background:#fff}
.lb{font:600 13px/1 'Barlow',sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--or);display:flex;gap:10px;align-items:center}.lb:before{content:"";width:28px;height:2px;background:var(--or)}
h2.c{font-weight:800;font-size:clamp(2.6rem,5.4vw,4.8rem);line-height:.92;margin:16px 0 0}
.sg{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--ln);border:1px solid var(--ln);margin-top:48px}
.sv{background:var(--bg);padding:34px 30px 30px;position:relative;display:flex;flex-direction:column;gap:10px;transition:background .25s}.sv:hover{background:var(--y)}.sv:hover .n,.sv:hover p,.sv:hover small{color:#111}
.sv .n{font:700 .95rem 'Barlow Condensed',sans-serif;color:var(--or);letter-spacing:.2em}.sv h3{font:800 2rem/1 'Barlow Condensed',sans-serif;text-transform:uppercase}.sv p{color:var(--mut);font-size:15.5px}
.sv .pr{margin-top:auto;padding-top:14px;display:flex;align-items:baseline;justify-content:space-between;border-top:1px solid var(--ln)}.sv .pr b{font:800 2.2rem/1 'Barlow Condensed',sans-serif}.sv .pr small{color:var(--mut)}
.sv .du{position:absolute;right:24px;top:30px;font:600 12px 'Barlow';letter-spacing:.14em;text-transform:uppercase;border:1px solid var(--ln);padding:6px 9px;color:var(--mut)}
.why{display:grid;grid-template-columns:1fr 1fr;gap:70px;align-items:center}
.pt{display:grid;gap:0;margin-top:36px;border-top:1px solid var(--ln)}.pt div{display:grid;grid-template-columns:60px 1fr;gap:18px;padding:22px 0;border-bottom:1px solid var(--ln)}.pt i{display:grid;place-items:center;width:52px;height:52px;border:1px solid var(--ln);color:var(--or)}.pt h4{font:700 1.5rem/1 'Barlow Condensed',sans-serif;text-transform:uppercase}.pt p{color:var(--mut);font-size:15.5px;margin-top:4px}
.bay{position:relative;aspect-ratio:1.05;background:#111;box-shadow:10px 10px 0 var(--y);overflow:hidden}.bay .sl svg{width:100%;height:100%}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin-top:52px;position:relative}.steps:before{content:"";position:absolute;left:0;right:0;top:34px;height:2px;background:var(--ln)}
.st{position:relative;padding-right:30px}.st .nb{width:70px;height:70px;background:var(--bg);border:2px solid var(--or);display:grid;place-items:center;font:800 2rem 'Barlow Condensed',sans-serif;color:var(--or);position:relative}.st h4{font:800 1.7rem/1 'Barlow Condensed',sans-serif;text-transform:uppercase;margin:20px 0 8px}.st p{color:var(--mut);font-size:15.5px}
.mq{overflow:hidden;white-space:nowrap;padding:26px 0;background:var(--y);color:#111}.mq div{display:inline-block;animation:mqa 44s linear infinite}.mq span{font:700 2rem/1 'Barlow Condensed',sans-serif;text-transform:uppercase;color:#111;margin:0 34px;letter-spacing:.06em}.mq b{color:#1a3cff}
@keyframes mqa{to{transform:translateX(-50%)}}
.rev{display:grid;grid-template-columns:.8fr 1.2fr;gap:50px;margin-top:48px;align-items:stretch}
.score{background:var(--p);border:1px solid var(--ln);padding:36px;display:flex;flex-direction:column;justify-content:center}.score b{font:800 7rem/.9 'Barlow Condensed',sans-serif;color:var(--or)}.score span{color:var(--or);letter-spacing:5px;font-size:1.4rem}.score p{color:var(--mut);margin-top:10px}
.rl{display:grid;gap:14px}.rq{background:var(--p);border:1px solid var(--ln);padding:24px 28px;border-left:3px solid var(--or)}.rq p{font-size:1.1rem}.rq small{display:block;margin-top:10px;color:var(--mut)}
.team{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:48px}.tm{background:var(--p);border:1px solid var(--ln)}.tm .av{aspect-ratio:1.2;background:linear-gradient(160deg,#2a2d33,#14161a);position:relative;overflow:hidden}.tm .av .sl svg{width:100%;height:100%}.tm div.t{padding:22px 24px}.tm h4{font:800 1.7rem/1 'Barlow Condensed',sans-serif;text-transform:uppercase}.tm p{color:var(--mut);font-size:15px;margin-top:6px}
.contact{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:48px}.bx{background:var(--p);border:1px solid var(--ln);padding:34px}
.hr li{display:flex;justify-content:space-between;padding:13px 0;border-bottom:1px solid var(--ln)}.hr li:last-child{border:0}.hr li.today{color:var(--or);font-weight:700}
.map{aspect-ratio:1.7;background:#15181c;border:1px solid var(--ln);margin-bottom:18px;overflow:hidden}.map svg{width:100%;height:100%;display:block}
form.rd{display:grid;gap:14px}.rd label{display:grid;gap:7px;font:600 12px 'Barlow',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}.rd input,.rd select,.rd textarea{font:500 16px 'Barlow',sans-serif;background:var(--p2);color:var(--ink);border:1px solid var(--ln);padding:14px;border-radius:0}.rd input:focus,.rd select:focus,.rd textarea:focus{outline:0;border-color:var(--or)}.rd .two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.slots{display:flex;gap:8px;flex-wrap:wrap}.slots button{background:var(--p2);color:var(--ink);border:1px solid var(--ln);padding:11px 14px;font:600 15px 'Barlow',sans-serif;cursor:pointer}.slots button.on,.slots button:hover{border-color:var(--or);color:var(--or)}
.ok{display:none;border:1px solid #0a8a3c;color:#0a8a3c;padding:16px 18px;font-weight:600}.ok.on{display:block}
.faq details{border-bottom:1px solid var(--ln);padding:22px 0}.faq summary{cursor:pointer;font:700 1.6rem/1.1 'Barlow Condensed',sans-serif;text-transform:uppercase;list-style:none;display:flex;justify-content:space-between;gap:20px}.faq summary::-webkit-details-marker{display:none}.faq summary:after{content:"+";color:var(--or);font-size:1.8rem;line-height:1}.faq details[open] summary:after{content:"–"}.faq p{color:var(--mut);margin-top:12px;max-width:48em}
footer.ft{background:#111;color:#fff;padding:64px 0 36px}footer.ft .w{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:36px}footer.ft h4{font:700 1.1rem 'Barlow Condensed',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--y);margin-bottom:14px}footer.ft li{margin:8px 0;color:#aeb2ba;font-size:15px}.lg2{font:800 2.4rem/1 'Barlow Condensed',sans-serif;text-transform:uppercase}.legal{grid-column:1/-1;border-top:1px solid #2b2e35;padding-top:24px;color:#6f7580;font-size:13px}
/* ===== effets 3D ===== */
.stage{perspective:1200px;padding-bottom:46px}
.stage>svg:not(.dl){transform:perspective(1100px) rotateY(calc(var(--ry,0)*1deg)) rotateX(calc(var(--rx,0)*1deg)) translateZ(30px);will-change:transform;filter:drop-shadow(0 30px 24px #0007)}
.stage .dl{transform:translate3d(calc(var(--ry,0)*-5px),calc(var(--rx,0)*5px),0) rotateY(calc(var(--ry,0)*-1deg));will-change:transform}
.stage:after{content:"";position:absolute;left:-10%;right:-10%;bottom:-6px;height:150px;z-index:-1;background:repeating-linear-gradient(90deg,#ffffff33 0 2px,transparent 2px 60px),repeating-linear-gradient(0deg,#ffffff33 0 2px,transparent 2px 38px);transform:perspective(500px) rotateX(68deg);transform-origin:50% 100%;-webkit-mask:linear-gradient(0deg,#000,transparent);mask:linear-gradient(0deg,#000,transparent);animation:fl 1.6s linear infinite}
@keyframes fl{to{background-position:0 0,0 38px}}
.wh{animation:sp 1.5s linear infinite}@keyframes sp{to{transform:rotate(360deg)}}
.hero h1.c{text-shadow:1px 1px 0 #0d28b8,2px 2px 0 #0d28b8,3px 3px 0 #0d28b8,4px 4px 0 #0d28b8,5px 5px 0 #0d28b8,6px 6px 0 #0d28b8,7px 7px 14px #0006}
.hero h1.c em{text-shadow:1px 1px 0 #b39500,2px 2px 0 #b39500,3px 3px 0 #b39500,4px 4px 0 #b39500,5px 5px 0 #b39500,6px 6px 0 #b39500,7px 7px 14px #0006}
.sv,.tm{transform-style:preserve-3d;will-change:transform}.sv{transition:background .25s,box-shadow .25s}.sv.tl,.tm.tl{z-index:3;box-shadow:0 26px 40px -14px #0007}
.sv:after,.tm:after{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(240px circle at var(--gx,50%) var(--gy,50%),#ffffff55,transparent 60%);opacity:0;transition:opacity .25s}.sv.tl:after,.tm.tl:after{opacity:1}.tm{position:relative}
.st .nb{transition:transform .7s cubic-bezier(.2,.8,.2,1),background .3s,color .3s;transform-style:preserve-3d}.st:hover .nb{transform:rotateY(360deg);background:var(--or);color:#fff}
.score b{display:inline-block;text-shadow:1px 1px 0 #0d28b8,2px 2px 0 #0d28b8,3px 3px 0 #0d28b8,4px 4px 0 #0d28b8,5px 5px 0 #0d28b8,6px 6px 12px #0005}
.bay{transform:perspective(1000px) rotateY(-9deg) rotateX(3deg);transition:transform .5s}.bay:hover{transform:perspective(1000px) rotateY(0) rotateX(0)}
.rq{transition:transform .35s}.rq:hover{transform:perspective(700px) translateZ(20px) rotateX(-3deg) translateX(8px);box-shadow:0 18px 30px -12px #0005}
.rv{opacity:0;transform:perspective(900px) rotateX(16deg) translateY(46px);transform-origin:50% 100%;transition:opacity .8s,transform .9s cubic-bezier(.2,.8,.2,1)}.rv.in{opacity:1;transform:none}
.sg .rv.in{transform:none}
@media(max-width:980px){.bay{transform:none}.stage:after{height:90px}}
@media(prefers-reduced-motion:reduce){.wh,.stage:after{animation:none}.rv{opacity:1;transform:none}.stage>svg:not(.dl){transform:none}}
@media(max-width:980px){.hero .w,.why,.rev,.contact{grid-template-columns:1fr}.devis{grid-template-columns:1fr}.plate{min-width:0}.sg,.team{grid-template-columns:1fr}.kpi{grid-template-columns:1fr 1fr}.steps{grid-template-columns:1fr 1fr;row-gap:36px}.steps:before{display:none}nav.g{display:none}footer.ft .w{grid-template-columns:1fr 1fr}.dl{display:none}section.s{padding:68px 0}}
'''
    svc = [("Vidange + filtres", "Huile moteur, filtre à huile, à air et d’habitacle. Niveaux et contrôle visuel offerts.", "79", "1 h"),
           ("Freinage avant", "Plaquettes et disques, purge du liquide, essai routier. Pièces de marque garanties.", "189", "2 h"),
           ("Pneus ×4", "Montage, équilibrage et géométrie inclus. Toutes marques, devis comparatif sur demande.", "229", "1 h 30"),
           ("Climatisation", "Recharge, contrôle d’étanchéité et traitement antibactérien de l’habitacle.", "69", "1 h"),
           ("Pré-contrôle technique", "On vérifie les 133 points du contrôle et on corrige avant de passer. Zéro mauvaise surprise.", "39", "45 min"),
           ("Courroie de distribution", "Kit complet, pompe à eau et galets. Garantie 24 mois pièces et main-d’œuvre.", "449", "4 h")]
    cards = "".join('<article class="sv"><span class="n">0%d</span><span class="du">%s</span><h3>%s</h3><p>%s</p><div class="pr"><small>à partir de</small><b>%s €</b></div></article>' % (i + 1, du, t, d, p) for i, (t, d, p, du) in enumerate(svc))
    brands = "".join('<span>%s</span><b>/</b>' % b for b in ["Renault", "Peugeot", "Citroën", "Dacia", "Volkswagen", "Toyota", "Ford", "Fiat", "Opel", "BMW", "Mercedes", "Audi", "Kia", "Hyundai", "Nissan", "Seat", "Skoda", "Mini", "Volvo", "Tesla"])
    team = [("Thomas Marchand", "Gérant · mécanicien depuis 22 ans", "#ffd400"), ("Inès Boudaoud", "Diagnostic électronique & hybrides", "#1a3cff"), ("Karim Lopes", "Freinage, pneus et trains roulants", "#ffc61a")]
    tms = ""
    for i, (n, r, c) in enumerate(team):
        ini = "".join(w[0] for w in n.split())
        av = svg(400, 330, '<defs><linearGradient id="av%d" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#23262c"/><stop offset="1" stop-color="#0f1013"/></linearGradient></defs><rect width="400" height="330" fill="url(#av%d)"/>'
                 '<g opacity=".16" stroke="%s" stroke-width="2">%s</g><path d="M-20 330 L140 -10 L200 -10 L40 330Z" fill="%s" opacity=".9"/>'
                 '<text x="212" y="226" font-family="Barlow Condensed,Arial Narrow,sans-serif" font-weight="800" font-size="190" fill="none" stroke="#f2f3f5" stroke-width="2.5" letter-spacing="2">%s</text>'
                 '<path d="M250 52 l54 0 M250 70 l30 0" stroke="%s" stroke-width="4"/>' % (i, i, c, "".join('<path d="M%d 0 V330"/>' % x for x in range(0, 400, 26)), c, ini, c))
        tms += '<div class="tm"><div class="av">%s</div><div class="t"><h4>%s</h4><p>%s</p></div></div>' % (slot("garage-equipe-%d" % (i + 1), av), n, r)
    bay = slot("garage-atelier", svg(600, 570, '<defs><linearGradient id="fl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1e23"/><stop offset="1" stop-color="#0d0e10"/></linearGradient></defs><rect width="600" height="570" fill="url(#fl)"/>'
        + "".join('<rect x="%d" y="70" width="12" height="260" fill="#2a2d33"/>' % x for x in (90, 498))
        + '<rect x="60" y="62" width="480" height="22" fill="#2f333a"/><path d="M60 62H540" stroke="#ffd400" stroke-width="3"/>'
        + '<g transform="translate(-60 190) scale(.78)">' + car_art("bay") + '</g>'
        + '<rect x="0" y="470" width="600" height="100" fill="#0a0b0d"/><path d="M0 470H600" stroke="#ffd400" stroke-width="2" stroke-dasharray="26 18"/>'))
    mapsvg = svg(600, 350, '<rect width="600" height="350" fill="#14171b"/><path d="M0 110H600M0 240H600M170 0V350M390 0V350" stroke="#232830" stroke-width="22"/><path d="M0 300Q300 250 600 300" stroke="#1a2a3a" stroke-width="34" fill="none"/><path d="M0 110H600M170 0V350" stroke="#ffd400" stroke-width="2" opacity=".5"/>'
                 '<path d="M270 160 q26-58 52 0 q0 32-26 58 q-26-26-26-58z" fill="#ffd400"/><circle cx="296" cy="158" r="10" fill="#0b0c0e"/>')
    faq = '''<details><summary>Faut-il prendre rendez-vous ?</summary><p>Pour les entretiens oui, c’est plus simple pour tout le monde. Pour une panne ou un voyant allumé, venez directement : on vous prend en charge dans la journée.</p></details>
<details><summary>Mon entretien annule-t-il la garantie constructeur ?</summary><p>Non. Depuis le règlement européen, vous pouvez entretenir votre véhicule dans le garage de votre choix sans perdre la garantie, à condition de suivre le carnet. Nous utilisons des pièces de qualité équivalente d’origine et tamponnons votre carnet.</p></details>
<details><summary>Prêtez-vous un véhicule ?</summary><p>Oui, une citadine de courtoisie est prêtée gratuitement pour les réparations de plus de deux heures, sur réservation.</p></details>
<details><summary>Le devis est-il gratuit et définitif ?</summary><p>Il est gratuit, écrit, détaillé pièce par pièce. Nous ne lançons aucun travail supplémentaire sans votre accord signé ou par message.</p></details>
<details><summary>Travaillez-vous sur les véhicules hybrides et électriques ?</summary><p>Oui. Inès est habilitée pour les véhicules hybrides et électriques (habilitation B2VL / BR). Diagnostic, freinage, climatisation et batterie 12 V.</p></details>'''
    body = '''
<header class="g"><div class="w"><a class="lg" href="#top"><i>@@GEAR@@</i><span>Garage Marchand<small>MÉCANIQUE &amp; PNEUS · NANTES</small></span></a>
<nav class="g"><a href="#forfaits">Forfaits</a><a href="#garanties">Garanties</a><a href="#equipe">Équipe</a><a href="#avis">Avis</a><a href="#rdv">Contact</a></nav><a class="bt" href="#rdv">Prendre rendez-vous</a></div></header>
<main id="top"><section class="hero"><div class="w"><div>
<span class="tg"><b>●</b> Garage indépendant · toutes marques</span>
<h1 class="c">Une réparation <em>claire,</em> un prix annoncé.</h1>
<p class="lead">Devis écrit avant d’ouvrir le capot, pièces de marque, véhicule de courtoisie. Chez Marchand, la facture finale est celle du devis.</p>
<form class="devis" id="dv"><label>Immatriculation<span class="plate"><b>F</b><input id="im" placeholder="AB-123-CD" maxlength="9" aria-label="Plaque"></span></label>
<label>Intervention<select id="sv"><option value="79">Vidange + filtres</option><option value="189">Freinage avant</option><option value="229">Pneus ×4</option><option value="69">Climatisation</option><option value="39">Pré-contrôle technique</option><option value="449">Courroie de distribution</option></select></label>
<label>Véhicule<select id="vh"><option value="1">Citadine</option><option value="1.2">Berline / break</option><option value="1.45">SUV / utilitaire</option></select></label>
<button class="bt" type="submit">Estimer</button>
<div class="est" id="est"><b id="ev">—</b><span>Estimation tout compris, main-d’œuvre incluse. Le devis définitif est écrit et gratuit.</span><a class="bt" href="#rdv">Réserver ce créneau</a></div></form></div>
<div class="stage"><svg class="dl" viewBox="0 0 300 300" aria-hidden="true">@@DIAL@@</svg>@@CAR@@</div></div>
<div class="kpi"><div><b>4,8 / 5</b><span>312 avis Google</span></div><div><b>Devis écrit</b><span>gratuit et sans surprise</span></div><div><b>12 mois</b><span>garantie pièces et main-d’œuvre</span></div><div><b>Citadine</b><span>de courtoisie offerte</span></div></div></section>

<section class="s" id="forfaits"><div class="w"><span class="lb">Nos forfaits</span><h2 class="c">Des prix affichés,<br>pas des « à partir de… peut-être ».</h2><div class="sg">@@CARDS@@</div>
<p style="color:var(--mut);margin-top:22px;font-size:15px">Tarifs TTC pour une citadine, pièces et main-d’œuvre comprises. Berlines, SUV et utilitaires : voir l’estimation ci-dessus.</p></div></section>

<div class="mq" aria-hidden="true"><div>@@BR@@@@BR@@</div></div>

<section class="s" id="garanties"><div class="w why"><div><span class="lb">Pourquoi Marchand</span><h2 class="c">Ce que vous ne verrez pas<br>ailleurs.</h2>
<div class="pt"><div><i>@@I1@@</i><span><h4>Devis écrit, signé, définitif</h4><p>Aucun travail supplémentaire sans votre accord. Vous recevez le détail pièce par pièce.</p></span></div>
<div><i>@@I2@@</i><span><h4>Garantie 12 mois</h4><p>Pièces et main-d’œuvre, dans tout notre réseau de garages partenaires en France.</p></span></div>
<div><i>@@I3@@</i><span><h4>Vos anciennes pièces rendues</h4><p>Sur demande, on vous rend les pièces remplacées : vous voyez ce qui a vraiment été changé.</p></span></div></div></div>
<div class="bay">@@BAY@@</div></div></section>

<section class="s"><div class="w"><span class="lb">Comment ça se passe</span><h2 class="c">Quatre étapes, aucune surprise.</h2>
<div class="steps"><div class="st"><div class="nb">1</div><h4>Vous réservez</h4><p>En ligne, par téléphone ou en passant. Créneau confirmé par SMS.</p></div><div class="st"><div class="nb">2</div><h4>Diagnostic</h4><p>Contrôle complet et devis écrit envoyé sur votre téléphone.</p></div><div class="st"><div class="nb">3</div><h4>Réparation</h4><p>Après votre accord uniquement. Un message à chaque étape.</p></div><div class="st"><div class="nb">4</div><h4>Remise des clés</h4><p>Essai routier, facture conforme au devis, pièces anciennes rendues.</p></div></div></div></section>

<section class="s" id="equipe"><div class="w"><span class="lb">L’équipe</span><h2 class="c">Trois mécaniciens,<br>un seul interlocuteur.</h2><div class="team">@@TEAM@@</div></div></section>

<section class="s" id="avis"><div class="w"><span class="lb">Avis clients</span><h2 class="c">Ils reviennent. C’est bon signe.</h2>
<div class="rev"><div class="score"><b>4,8</b><span>★★★★★</span><p>312 avis Google · 96 % de clients qui nous recommandent</p></div>
<div class="rl"><div class="rq"><p>« Devis reçu par SMS en 20 minutes, voiture rendue le soir même. Le prix était exactement celui annoncé. »</p><small>Nadia K. · Peugeot 308</small></div>
<div class="rq"><p>« Enfin un garage qui m’explique ce qui est urgent et ce qui peut attendre. Je n’irai plus ailleurs. »</p><small>Marc D. · Renault Clio</small></div>
<div class="rq"><p>« Inès a trouvé la panne électrique que deux autres garages n’avaient pas vue. Chapeau. »</p><small>Hugo L. · Toyota Yaris hybride</small></div></div></div></div></section>

<section class="s" id="rdv"><div class="w"><span class="lb">Horaires &amp; rendez-vous</span><h2 class="c">Passez nous voir<br>ou réservez en 30 secondes.</h2>
<div class="contact"><div class="bx"><div class="map">@@MAP@@</div><ul class="hr" id="hr"><li data-d="1"><span>Lundi</span><b>8 h – 12 h 30 · 14 h – 18 h 30</b></li><li data-d="2"><span>Mardi</span><b>8 h – 12 h 30 · 14 h – 18 h 30</b></li><li data-d="3"><span>Mercredi</span><b>8 h – 12 h 30 · 14 h – 18 h 30</b></li><li data-d="4"><span>Jeudi</span><b>8 h – 12 h 30 · 14 h – 18 h 30</b></li><li data-d="5"><span>Vendredi</span><b>8 h – 12 h 30 · 14 h – 17 h 30</b></li><li data-d="6"><span>Samedi</span><b>9 h – 12 h</b></li><li data-d="0"><span>Dimanche</span><b>Fermé</b></li></ul>
<p style="color:var(--mut);margin-top:16px;font-size:15px">12 rue de la Forge, 44000 Nantes · Tram ligne 1, arrêt Commerce · Parking gratuit devant l’atelier.</p></div>
<div class="bx"><form class="rd" id="rd"><label>Votre nom et téléphone<input required placeholder="Nadia Kaci · 06 00 00 00 00"></label><div class="two"><label>Plaque<input placeholder="AB-123-CD"></label><label>Intervention<select><option>Entretien / vidange</option><option>Freinage</option><option>Pneus</option><option>Climatisation</option><option>Pré-contrôle technique</option><option>Panne / voyant allumé</option></select></label></div>
<label>Jour<input type="date" required id="dt"></label><label>Créneau</label><div class="slots" id="sl"><button type="button">8 h 30</button><button type="button">10 h</button><button type="button">11 h 30</button><button type="button">14 h 30</button><button type="button">16 h</button><button type="button">17 h</button></div>
<button class="bt" type="submit" style="justify-self:start;margin-top:8px">Confirmer le rendez-vous</button><div class="ok" id="ok">Rendez-vous demandé. Vous recevez un SMS de confirmation sous 15 minutes.</div></form></div></div></div></section>

<section class="s faq"><div class="w"><span class="lb">Questions fréquentes</span><h2 class="c" style="margin-bottom:34px">On répond avant que vous demandiez.</h2>@@FAQ@@</div></section></main>
<footer class="ft"><div class="w"><div><div class="lg2">Garage Marchand</div><p style="color:var(--mut);margin-top:12px;max-width:26em">Garage indépendant toutes marques à Nantes depuis 2009.</p></div>
<div><h4>Atelier</h4><ul><li>Entretien &amp; vidange</li><li>Freinage</li><li>Pneus</li><li>Climatisation</li></ul></div><div><h4>Contact</h4><ul><li>02 40 00 00 00</li><li>contact@garage-marchand.fr</li><li>12 rue de la Forge, Nantes</li></ul></div><div><h4>Infos</h4><ul><li>Mentions légales</li><li>CGV</li><li>Médiation de la consommation</li></ul></div>
<div class="legal">© 2026 Garage Marchand SAS · SIRET 000 000 000 00000 (exemple) · RCS Nantes · Hébergeur : Cloudflare, Inc.</div></div></footer>
'''
    gear = ico("alarm", 22, "#0b0c0e", 2.2)
    body = (body.replace("@@GEAR@@", gear).replace("@@DIAL@@", dial()).replace("@@CAR@@", svg(800, 300, '<g transform="translate(0 -78)">' + car_art() + "</g>"))
            .replace("@@CARDS@@", cards).replace("@@BR@@", brands).replace("@@BAY@@", bay).replace("@@TEAM@@", tms).replace("@@MAP@@", mapsvg).replace("@@FAQ@@", faq)
            .replace("@@I1@@", ico("check", 24, "currentColor", 2)).replace("@@I2@@", ico("shield", 24, "currentColor", 2)).replace("@@I3@@", ico("hands", 24, "currentColor", 2)))
    js = r'''<script>(function(){
var H={1:[[8,12.5],[14,18.5]],2:[[8,12.5],[14,18.5]],3:[[8,12.5],[14,18.5]],4:[[8,12.5],[14,18.5]],5:[[8,12.5],[14,17.5]],6:[[9,12]],0:[]};
function f(h){var m=Math.round((h%1)*60);return Math.floor(h)+' h'+(m?(' '+(m<10?'0'+m:m)):'')}
function live(){var n=new Date(),d=n.getDay(),h=n.getHours()+n.getMinutes()/60,o=null,nx=null,i,r;
 for(i=0;i<(H[d]||[]).length;i++){r=H[d][i];if(h>=r[0]&&h<r[1])o=r;else if(h<r[0]&&!nx)nx=r}
 var L=document.getElementById('live'),T=document.getElementById('livet');
 if(L&&T){if(o){L.classList.remove('off');T.textContent='Ouvert · ferme à '+f(o[1])}else{L.classList.add('off');T.textContent=nx?('Fermé · ouvre à '+f(nx[0])):'Fermé · réouverture demain'}}
 var li=document.querySelector('#hr li[data-d="'+d+'"]');if(li)li.classList.add('today')}
live();
document.getElementById('dv').onsubmit=function(e){e.preventDefault();var p=+document.getElementById('sv').value*+document.getElementById('vh').value;
 document.getElementById('ev').textContent=Math.round(p/5)*5+' € TTC';document.getElementById('est').classList.add('on')};
var im=document.getElementById('im');im.oninput=function(){var v=im.value.toUpperCase().replace(/[^A-Z0-9]/g,'');var o=v.slice(0,2);if(v.length>2)o+='-'+v.slice(2,5);if(v.length>5)o+='-'+v.slice(5,7);im.value=o};
var sl=document.getElementById('sl');sl.onclick=function(e){if(e.target.tagName==='BUTTON'){Array.prototype.forEach.call(sl.children,function(b){b.classList.remove('on')});e.target.classList.add('on')}};
document.getElementById('rd').onsubmit=function(e){e.preventDefault();document.getElementById('ok').classList.add('on')};
var st=document.querySelector('.stage'),hero=document.querySelector('.hero'),px=null,pt=0,cx=0,cy=0,rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
if(hero)hero.addEventListener('pointermove',function(e){var r=hero.getBoundingClientRect();px=[(e.clientX-r.left)/r.width-.5,(e.clientY-r.top)/r.height-.5];pt=Date.now()});
function tick(t){if(st&&!rm&&hero.getBoundingClientRect().bottom>0){var tx,ty;if(px&&Date.now()-pt<2500){tx=px[0]*26;ty=-px[1]*14}else{tx=Math.sin(t/1800)*14;ty=Math.cos(t/2600)*5}
 cx+=(tx-cx)*.07;cy+=(ty-cy)*.07;st.style.setProperty('--ry',cx.toFixed(2));st.style.setProperty('--rx',cy.toFixed(2))}requestAnimationFrame(tick)}
requestAnimationFrame(tick);
if(matchMedia('(hover:hover)').matches&&!rm)Array.prototype.forEach.call(document.querySelectorAll('.sv,.tm'),function(c){
 c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;c.classList.add('tl');c.style.transform='perspective(800px) rotateY('+((x-.5)*14).toFixed(1)+'deg) rotateX('+((.5-y)*14).toFixed(1)+'deg) translateZ(14px)';c.style.setProperty('--gx',(x*100)+'%');c.style.setProperty('--gy',(y*100)+'%')});
 c.addEventListener('pointerleave',function(){c.classList.remove('tl');c.style.transform=''})});
if('IntersectionObserver' in window&&!rm){var els=document.querySelectorAll('.sv,.tm,.st,.rq,.score,.pt>div,.faq details,section.s h2.c');var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{threshold:.12});
 Array.prototype.forEach.call(els,function(el,i){el.classList.add('rv');el.style.transitionDelay=((i%3)*90)+'ms';io.observe(el)})}
var dt=document.getElementById('dt');if(dt){var t=new Date();t.setDate(t.getDate()+1);dt.min=t.toISOString().slice(0,10)}
})()</script>'''
    return page("Garage Marchand · Mécanique, pneus et entretien à Nantes", "Garage indépendant toutes marques à Nantes : entretien, freinage, pneus, climatisation. Devis écrit gratuit, garantie 12 mois.",
                "family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600;700", css, body, js)




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
    portrait = slot("osteo-portrait", svg(420, 520, '<rect width="420" height="520" fill="#15181d"/><text x="210" y="320" text-anchor="middle" font-family="system-ui,sans-serif" font-weight="800" font-size="200" fill="#f5f2ea" letter-spacing="-10">LL</text><text x="30" y="494" font-family="ui-monospace,monospace" font-size="15" fill="#8b8a84">Photo de la praticienne</text>'))
    css = r'''
:root{--b:#c4552d;--y:#eaa55e;--ink:#15181d;--mut:#6b6a64;--ln:#dcd6c8;--bg:#f5f2ea}
body{background:var(--bg);color:var(--ink);font:400 17px/1.65 'Figtree',system-ui,sans-serif;padding-bottom:50px}
.mono{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:.78em;letter-spacing:.04em;text-transform:uppercase}
.w{max-width:1240px;margin:0 auto;padding:0 28px}
.hero{background:radial-gradient(ellipse 60% 70% at 50% 58%,#232830 0,#0d0f12 72%);color:#f5f2ea;position:relative;overflow:hidden}.hero header{position:absolute;top:0;left:0;right:0;z-index:5}.hero header .w{display:flex;justify-content:space-between;align-items:center;height:84px}
.lg{font:700 1.35rem/1 'Familjen Grotesk','Figtree',system-ui,sans-serif;letter-spacing:-.02em}.lg small{display:block;font:500 .64rem/1 'JetBrains Mono',monospace;letter-spacing:.1em;text-transform:uppercase;opacity:.7;margin-top:6px}
header nav{display:flex;gap:30px;font-size:15px;font-weight:500}header nav a{opacity:.85}header nav a:hover{opacity:1;text-decoration:underline;text-underline-offset:5px}
.cta{background:var(--b);color:#fff;font:700 15px/1 'Figtree',sans-serif;padding:15px 22px;border-radius:3px;border:0;cursor:pointer;display:inline-block}.cta:hover{background:var(--ink)}
.hg{display:grid;grid-template-columns:.9fr 1.3fr .9fr;gap:20px;padding-top:110px;padding-bottom:40px;min-height:min(100vh,860px);align-items:center}.hl{align-self:center}
h1{font:700 clamp(2.8rem,5.2vw,5.4rem)/.92 'Familjen Grotesk','Figtree',system-ui,sans-serif;letter-spacing:-.045em}h1 u{text-decoration:none;color:var(--b)}
.lead{font-size:1.15rem;max-width:26em;margin:22px 0 10px;color:#b9b5a8;font-size:1.05rem}
.pan{border-top:2px solid #f5f2ea;padding-top:18px;max-width:34em;min-height:260px;align-self:center}.pan .mono{color:var(--b)}.pan h2{color:#fff;font:700 1.9rem/1.05 'Familjen Grotesk','Figtree',sans-serif;letter-spacing:-.03em;margin:8px 0 10px}.pan p{color:#cfcabd;font-size:16.5px}
.pan .mt{display:flex;gap:28px;margin:14px 0 18px;font-size:14.5px;color:#f5f2ea}.pan .mt b{display:block;font:700 1.5rem 'Familjen Grotesk','Figtree',sans-serif;color:var(--b)}.pan .mt span{opacity:.85}
.body{position:relative;height:min(84vh,780px);min-height:460px}.body .cv{position:absolute;inset:0}.body .fb{display:none;height:100%;justify-content:center}.body.nogl .fb{display:flex}.body.nogl .cv{display:none}.body svg{width:min(100%,340px);height:auto;max-height:100%}.tip{position:absolute;left:0;right:0;bottom:6px;text-align:center;font:500 11.5px 'JetBrains Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:#8e8a7e;pointer-events:none}.rs{position:absolute;top:8px;right:0;background:transparent;border:1.5px solid #5c5a52;color:#f5f2ea;font:600 13px 'Figtree',sans-serif;padding:9px 14px;border-radius:2px;cursor:pointer;display:none;z-index:3}.rs.on{display:block}.rs:hover{background:#f5f2ea;color:var(--ink)}
.hs{cursor:pointer}.hs .pl{fill:var(--b);opacity:.28;transform-box:fill-box;transform-origin:center;animation:pu 2.2s ease-out infinite}.hs .dt{fill:var(--b);stroke:#0d0f12;stroke-width:2.5;transition:.2s}.hs text{font:700 9px 'JetBrains Mono',monospace;fill:#fff;text-anchor:middle;pointer-events:none}.hs:hover .dt,.hs:focus .dt{r:9}.hs.on .dt{fill:#fff;stroke:var(--b);stroke-width:3}.hs.on text{fill:var(--b)}.hs.on .pl{animation:none;opacity:.35;fill:var(--b)}.hs:focus{outline:0}
@keyframes pu{0%{transform:scale(.7);opacity:.5}100%{transform:scale(1.9);opacity:0}}
.bar{background:#ece6d8;color:var(--ink)}.bar .w{display:grid;grid-template-columns:repeat(4,1fr)}.bar div{padding:24px 24px 24px 0;border-right:1px solid #cfc7b4;margin-right:24px}.bar div:last-child{border:0}.bar b{display:block;font:700 2.2rem/1 'Familjen Grotesk','Figtree',sans-serif;letter-spacing:-.03em}.bar span{font-size:14px;color:#6b6a64}
.row{display:grid;grid-template-columns:230px 1fr;gap:40px;border-top:2px solid var(--ink);padding:56px 0 20px;margin-top:70px}.row>.lb{font:500 13px 'JetBrains Mono',monospace;letter-spacing:.05em;text-transform:uppercase;color:var(--b);position:sticky;top:20px;align-self:start}.row>.lb .n{font-style:normal;display:block;font:700 3.4rem/1 'Familjen Grotesk','Figtree',sans-serif;letter-spacing:-.05em;color:var(--ink);margin-bottom:6px}
h2.t{font:700 clamp(2rem,4vw,3.4rem)/1 'Familjen Grotesk','Figtree',sans-serif;letter-spacing:-.04em;max-width:15em;margin-bottom:34px}
.st li{display:grid;grid-template-columns:110px 1fr;gap:24px;padding:24px 0;border-top:1px solid var(--ln)}.st li:last-child{border-bottom:1px solid var(--ln)}.st b{white-space:nowrap;font:700 2.4rem/1 'Familjen Grotesk','Figtree',sans-serif;letter-spacing:-.04em;color:var(--b)}.st h3{font:700 1.5rem 'Familjen Grotesk','Figtree',sans-serif;letter-spacing:-.02em}.st p{color:#55534d;max-width:36em}
.pt li{display:flex;justify-content:space-between;align-items:baseline;padding:18px 0;border-top:1px solid var(--ln);font-size:18px}.pt li:last-child{border-bottom:1px solid var(--ln)}.pt b{font:700 2rem 'Familjen Grotesk','Figtree',sans-serif;letter-spacing:-.03em}.note{margin-top:22px;color:var(--mut);font-size:15px;max-width:38em}
.pr{display:grid;grid-template-columns:260px 1fr;gap:40px;align-items:start}.pr .ph{aspect-ratio:.82;background:var(--b);overflow:hidden}.pr .ph .sl svg{width:100%;height:100%}.pr p{max-width:34em;color:#46443f;margin-bottom:14px}
.dp{margin-top:20px}.dp li{display:grid;grid-template-columns:70px 1fr;padding:11px 0;border-top:1px solid var(--ln);font-size:15.5px}.dp li b{font:500 13px 'JetBrains Mono',monospace;color:var(--b);padding-top:2px}
.qt{display:grid;grid-template-columns:1fr 1fr 1fr;gap:40px}.qt p{font:600 1.45rem/1.25 'Familjen Grotesk','Figtree',sans-serif;letter-spacing:-.02em}.qt small{display:block;margin-top:14px;font:500 12px 'JetBrains Mono',monospace;color:var(--mut);text-transform:uppercase}
.rdv{background:var(--ink);color:#f5f2ea;margin-top:90px;padding:80px 0 90px}.rdv h2{font:700 clamp(2.4rem,5.5vw,5rem)/.92 'Familjen Grotesk','Figtree',sans-serif;letter-spacing:-.045em;margin-bottom:12px}.rdv .sub{color:#cfcabd;margin-bottom:44px}
.bk{display:grid;grid-template-columns:1.25fr .75fr;gap:60px}.bk>div{min-width:0}.lab{font:500 12px 'JetBrains Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--y);margin-bottom:12px}
.days{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding-bottom:4px}.days::-webkit-scrollbar{display:none}
.dy{flex:0 0 auto;min-width:76px;border:1.5px solid #ffffff66;background:transparent;color:#fff;padding:12px 6px;text-align:center;cursor:pointer;font:500 12.5px/1.3 'Figtree',sans-serif;border-radius:2px;transition:.15s}.dy b{display:block;font:700 2rem/1.1 'Familjen Grotesk','Figtree',sans-serif}.dy:hover{border-color:#fff}.dy.on{background:#f5f2ea;color:var(--ink);border-color:#fff}.dy.full{opacity:.35;pointer-events:none}
.slots{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:8px}.sl2{border:1.5px solid #ffffff66;background:transparent;color:#fff;padding:14px 0;font:600 16px 'Figtree',sans-serif;cursor:pointer;border-radius:2px}.sl2:hover{border-color:#fff}.sl2.on{background:var(--y);color:var(--ink);border-color:var(--y)}.sl2.x{opacity:.3;text-decoration:line-through;pointer-events:none}
.rec{border-top:2px solid #fff;padding:16px 0;margin-bottom:12px;min-height:84px}.rec b{display:block;font:700 1.7rem/1.1 'Familjen Grotesk','Figtree',sans-serif;letter-spacing:-.02em}.rec span{color:#cfcabd;font-size:15px}
.bk form{display:grid;gap:16px}.bk label{display:grid;gap:5px;font:500 12px 'JetBrains Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#bdb8aa}.bk input,.bk select{font:400 17px 'Figtree',sans-serif;background:transparent;color:#fff;border:0;border-bottom:1.5px solid #fff;padding:11px 0;border-radius:0;text-transform:none;letter-spacing:0}.bk select option{color:#111}.bk input::placeholder{color:#8a8678}.bk input:focus,.bk select:focus{outline:0;border-bottom-width:3px}
.go{background:var(--y);color:var(--ink);border:0;padding:17px;font:700 16px 'Figtree',sans-serif;cursor:pointer;border-radius:2px;margin-top:6px}.go:disabled{opacity:.4;cursor:not-allowed}.go:not(:disabled):hover{background:#fff}
.done{display:none;border:2px solid var(--y);padding:24px}.done.on{display:block}.done b{font:700 1.8rem 'Familjen Grotesk','Figtree',sans-serif;display:block;margin-bottom:6px;color:var(--y)}
.hr li{display:flex;justify-content:space-between;padding:13px 0;border-top:1px solid var(--ln)}.hr li:last-child{border-bottom:1px solid var(--ln)}.hr li.today{font-weight:700;color:var(--b)}.hr li.today:before{content:"● ";}.hr li.today span:first-child{margin-right:auto}
.ac{display:grid;grid-template-columns:1fr 1fr;gap:50px}.ac h3{font:700 1.4rem 'Familjen Grotesk','Figtree',sans-serif;margin-bottom:10px}.ac p{color:#55534d}
.faq details{border-top:1px solid var(--ln);padding:22px 0}.faq details:last-child{border-bottom:1px solid var(--ln)}.faq summary{cursor:pointer;font:700 1.4rem/1.2 'Familjen Grotesk','Figtree',sans-serif;letter-spacing:-.02em;list-style:none;display:flex;justify-content:space-between;gap:20px}.faq summary::-webkit-details-marker{display:none}.faq summary:after{content:"+";font:400 1.6rem 'JetBrains Mono',monospace;color:var(--b)}.faq details[open] summary:after{content:"–"}.faq p{margin-top:10px;color:#55534d;max-width:44em}
footer.ft{background:var(--ink);color:#aaa69a;padding:64px 0 38px}footer.ft .w{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:34px}footer.ft .big{font:700 clamp(2.6rem,7vw,6rem)/.9 'Familjen Grotesk','Figtree',sans-serif;letter-spacing:-.05em;color:#fff;grid-column:1/-1;margin-bottom:26px}footer.ft h4{font:500 12px 'JetBrains Mono',monospace;color:var(--y);margin-bottom:12px;text-transform:uppercase}footer.ft li{margin:7px 0;font-size:15px}.legal{grid-column:1/-1;border-top:1px solid #33363c;padding-top:22px;font-size:13px;color:#85817a;margin-top:20px}
@media(max-width:900px){.hg{grid-template-columns:1fr;padding-top:84px;padding-bottom:30px;min-height:0;gap:6px}.hl{order:1}.body{order:2;height:min(62vh,520px);min-height:380px;margin:0 -18px}.pan{order:3;min-height:0}.rs{right:18px}h1{font-size:2.7rem!important}.hero header .w{height:70px}.lg{font-size:1.1rem}.lg small{display:none}.cta{padding:12px 14px;font-size:14px}h1{font-size:3.4rem}header nav{display:none}.bar .w{grid-template-columns:1fr 1fr}.bar div:nth-child(2){border:0}.row,.pr,.bk,.ac,.qt{grid-template-columns:1fr;gap:28px}.row>.lb{position:static}.row>.lb .n{display:inline;font-size:2.6rem;margin-right:12px}.st li{grid-template-columns:104px 1fr}.lead{display:none}.pan{min-height:0}.hg h1{font-size:3.1rem}.slots{grid-template-columns:repeat(3,1fr)}.pr .ph{max-width:240px}footer.ft .w{grid-template-columns:1fr 1fr}.w{padding-left:18px;padding-right:18px}.rdv{padding:56px 0 64px}}
'''
    body = '''
<div class="hero"><header><div class="w"><a class="lg" href="#top">Cabinet Lemaire<small>Ostéopathie · Bordeaux</small></a><nav><a href="#seance">La séance</a><a href="#tarifs">Tarifs</a><a href="#lea">Léa Lemaire</a><a href="#acces">Accès</a></nav><a class="cta" href="#rdv">Prendre rendez-vous</a></div></header>
<div class="w hg" id="top"><div class="hl"><span class="mono" style="color:var(--b)">Ostéopathe D.O. · Bordeaux Chartrons</span><h1 style="margin-top:14px">Où avez-vous <u>mal</u> ?</h1><p class="lead">Faites tourner le squelette, touchez la zone qui vous gêne : je vous dis ce que l’on y voit le plus souvent et combien de séances il faut.</p></div>
<div class="body" id="bd"><div class="cv" id="cv"></div><div class="fb">@@FIG@@</div><button class="rs" id="rs" type="button">Vue d’ensemble</button><div class="tip">Glissez pour tourner · touchez un point</div></div>
<div class="pan" id="pan" aria-live="polite"><span class="mono">Choisissez un point sur le corps</span><h2>Huit zones, une seule question.</h2><p>Chaque point est une raison fréquente de consultation. Si votre douleur est ailleurs, prenez rendez-vous : on la trouvera ensemble.</p></div></div></div>
<div class="bar"><div class="w"><div><b>1 h</b><span>de consultation, sans chronomètre</span></div><div><b>4,9 / 5</b><span>87 avis Google</span></div><div><b>48 h</b><span>pour un premier rendez-vous</span></div><div><b>12 ans</b><span>de pratique à Bordeaux</span></div></div></div>

<main class="w">
<section class="row" id="seance"><div class="lb"><i class="n">01</i>La séance</div><div><h2 class="t">Une heure, trois temps. Pas de précipitation.</h2><ul class="st"><li><b>15 min</b><div><h3>L’échange</h3><p>Vous racontez votre douleur, votre histoire, votre quotidien. Je vous écoute avant de toucher.</p></div></li><li><b>10 min</b><div><h3>L’examen</h3><p>Tests de mobilité, observation de la posture, palpation : je cherche ce qui se bloque vraiment.</p></div></li><li><b>35 min</b><div><h3>Le soin</h3><p>Techniques douces, adaptées à votre état. J’explique ce que je fais, et je vous donne des gestes simples pour la maison.</p></div></li></ul></div></section>

<section class="row" id="tarifs"><div class="lb"><i class="n">02</i>Tarifs</div><div><h2 class="t">Des prix affichés d’avance, sans supplément.</h2><ul class="pt"><li><span>Adulte</span><b>60 €</b></li><li><span>Enfant de 2 à 12 ans</span><b>45 €</b></li><li><span>Nourrisson (moins de 2 ans)</span><b>50 €</b></li><li><span>Femme enceinte</span><b>55 €</b></li></ul><p class="note">Paiement par carte, espèces ou chèque. Facture remise à chaque séance pour votre mutuelle (la Sécurité sociale ne rembourse pas l’ostéopathie). Annulation gratuite jusqu’à 24 h avant ; un rendez-vous manqué sans prévenir est facturé 30 €.</p></div></section>

<section class="row" id="lea"><div class="lb"><i class="n">03</i>Votre praticienne</div><div class="pr"><div class="ph">@@PT@@</div><div><h2 class="t" style="margin-bottom:20px">Léa Lemaire, ostéopathe D.O.</h2><p>Diplômée en 2014 après cinq ans d’études, j’ai accompagné une équipe de handball avant d’ouvrir mon cabinet aux Chartrons. J’aime les consultations longues, les questions simples et les explications claires.</p><p>Je me forme chaque année. Et je préfère vous revoir une fois de moins que de vous faire revenir pour rien.</p><ul class="dp"><li><b>2014</b><span>Diplôme d’ostéopathe D.O., Bordeaux</span></li><li><b>2017</b><span>Formation en ostéopathie pédiatrique</span></li><li><b>2021</b><span>Périnatalité et suivi post-partum</span></li></ul></div></div></section>

<section class="row"><div class="lb"><i class="n">04</i>Avis patients</div><div><h2 class="t">4,9 sur 5, 87 avis.</h2><div class="qt"><div><p>« Enfin une consultation où l’on prend le temps. Mon mal de dos chronique s’est apaisé dès la deuxième séance. »</p><small>Claire B. · Chartrons</small></div><div><p>« Très douce avec mon bébé de trois semaines. Tout est expliqué avec calme, et ça a marché. »</p><small>Julien M. · papa d’Éloïse</small></div><div><p>« Je cours des marathons : elle a trouvé l’origine de mon genou en vingt minutes. »</p><small>Thomas R. · coureur</small></div></div></div></section>

<section class="row" id="acces"><div class="lb"><i class="n">05</i>Accès &amp; questions</div><div><div class="ac"><div><h3>Horaires</h3><ul class="hr" id="hr"><li data-d="1"><span>Lundi</span><span>9 h – 12 h · 14 h – 19 h</span></li><li data-d="2"><span>Mardi</span><span>9 h – 12 h · 14 h – 19 h</span></li><li data-d="3"><span>Mercredi</span><span>9 h – 12 h · 14 h – 18 h</span></li><li data-d="4"><span>Jeudi</span><span>9 h – 12 h · 14 h – 19 h</span></li><li data-d="5"><span>Vendredi</span><span>9 h – 12 h · 14 h – 17 h</span></li><li data-d="6"><span>Samedi</span><span>9 h – 13 h</span></li><li data-d="0"><span>Dimanche</span><span>Fermé</span></li></ul></div>
<div><h3>Le cabinet</h3><p>27 cours Saint-Louis, 33300 Bordeaux<br>05 56 00 00 00<br>cabinet@lemaire-osteo.fr</p><h3 style="margin-top:22px">Venir</h3><p>Tram C, arrêt Chartrons, à 3 minutes à pied. Parking Saint-Louis à 100 m. Cabinet de plain-pied, accessible aux personnes à mobilité réduite.</p></div></div>
<div class="faq" style="margin-top:46px"><details><summary>Combien de séances faut-il prévoir ?</summary><p>Une à trois suffisent le plus souvent. Si le problème est ancien, nous convenons d’un rythme ensemble, jamais d’un forfait imposé.</p></details><details><summary>Faut-il une ordonnance ?</summary><p>Non. Apportez vos radios, IRM et comptes rendus récents s’il y en a : ils m’aident à adapter le soin.</p></details><details><summary>Est-ce douloureux ?</summary><p>Non. Les techniques sont douces ; vous pouvez m’arrêter à tout moment.</p></details><details><summary>Recevez-vous les bébés et les femmes enceintes ?</summary><p>Oui, dès les premières semaines de vie et pendant toute la grossesse, avec des techniques et une table adaptées.</p></details></div></div></section></main>

<section class="rdv" id="rdv"><div class="w"><span class="mono" style="color:var(--y)">Rendez-vous en ligne</span><h2 style="margin-top:12px">Choisissez votre créneau.</h2><p class="sub">Un SMS de confirmation, un rappel la veille. Annulation gratuite jusqu’à 24 h avant.</p>
<div class="bk"><div><div class="lab">1 · Jour</div><div class="days" id="days"></div><div class="lab" style="margin-top:26px">2 · Heure</div><div class="slots" id="slots"></div></div>
<div><div class="lab">3 · Vous</div><div class="rec" id="rec"><b>Aucun créneau choisi</b><span>Sélectionnez un jour puis une heure.</span></div>
<form id="bf"><label>Nom et prénom<input required placeholder="Marie Durand"></label><label>Téléphone<input required placeholder="06 00 00 00 00" inputmode="tel"></label><label>Motif<select id="mot"><option>Tête / mâchoire</option><option>Nuque / cervicales</option><option>Épaule</option><option>Haut du dos</option><option>Bas du dos / lombaires</option><option>Coude / poignet</option><option>Hanche / bassin</option><option>Genou / jambe</option><option>Bébé / enfant</option><option>Grossesse</option><option>Autre</option></select></label><button class="go" type="submit" id="bgo" disabled>Confirmer le rendez-vous</button></form><div class="done" id="done"><b>C’est noté.</b><span id="dt"></span></div></div></div></div></section>

<footer class="ft"><div class="w"><div class="big">Cabinet Lemaire</div><div><h4>Cabinet</h4><p style="max-width:22em">Ostéopathie pour adultes, enfants et nourrissons, à Bordeaux Chartrons.</p></div><div><h4>Contact</h4><ul><li>05 56 00 00 00</li><li>cabinet@lemaire-osteo.fr</li></ul></div><div><h4>Adresse</h4><ul><li>27 cours Saint-Louis</li><li>33300 Bordeaux</li></ul></div><div><h4>Infos</h4><ul><li>Mentions légales</li><li>Confidentialité</li><li>Données de santé</li></ul></div>
<div class="legal">© 2026 Cabinet Lemaire · Ostéopathe D.O., n° ADELI 33 00 00000 (exemple) · SIRET 000 000 000 00000 (exemple) · Hébergeur : Cloudflare, Inc.</div></div></footer>
'''
    body = body.replace("@@FIG@@", figure).replace("@@PT@@", portrait)
    js = r'''<script>(function(){
var Z=@@ZJ@@,D=document,$=function(i){return D.getElementById(i)},pan=$('pan'),hs=[].slice.call(D.querySelectorAll('.hs'));
function show(id){var z=Z.filter(function(x){return x[0]===id})[0];hs.forEach(function(h){h.classList.toggle('on',h.dataset.z===id)});
 pan.innerHTML='<span class="mono">Zone '+(Z.indexOf(z)+1)+' sur '+Z.length+'</span><h2>'+z[1]+'</h2><p>'+z[2]+'</p><div class="mt"><div><b>'+z[3]+'</b><span>séances en général</span></div></div><p style="font-size:15px;opacity:.9">'+z[4]+'</p><p style="margin-top:14px"><a class="cta" href="#rdv" data-m="'+z[5]+'">Réserver pour cette zone</a></p>'}
var api=null;function show3(id){if(!id){pan.innerHTML='<span class="mono">Choisissez un point sur le corps</span><h2>Huit zones, une seule question.</h2><p>Chaque point est une raison fréquente de consultation. Si votre douleur est ailleurs, prenez rendez-vous : on la trouvera ensemble.</p>';$('rs').classList.remove('on');hs.forEach(function(h){h.classList.remove('on')});return}show(id);$('rs').classList.add('on')}
import('/assets/ex/osteo3d.js').then(function(m){api=m.init({el:$('cv'),onSelect:show3});window.osteo3d=api;if(!api)$('bd').classList.add('nogl')}).catch(function(){$('bd').classList.add('nogl')});
$('rs').onclick=function(){if(api)api.reset()};
hs.forEach(function(h){h.onclick=function(){show(h.dataset.z);$('rs').classList.add('on');if(api)api.select(h.dataset.z,true)};h.onkeydown=function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();show(h.dataset.z)}}});
pan.onclick=function(e){var m=e.target.getAttribute&&e.target.getAttribute('data-m');if(m)$('mot').value=m};
var days=$('days'),slots=$('slots'),rec=$('rec'),go=$('bgo'),sel={d:null,t:null};
var M={1:[9,10,11,14,15,16,17,18],2:[9,10,11,14,15,16,17,18],3:[9,10,11,14,15,16,17],4:[9,10,11,14,15,16,17,18],5:[9,10,11,14,15,16],6:[9,10,11,12],0:[]};
function hash(s){var h=0;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return Math.abs(h)}
function fmt(d){return d.toLocaleDateString('fr-FR',{weekday:'long',day:'numeric',month:'long'})}
var out=[],n=new Date();n.setHours(12);for(var i=1;out.length<8&&i<30;i++){var d=new Date(n);d.setDate(n.getDate()+i);if(d.getDay()!==0)out.push(d)}
function avail(d){var key=d.toISOString().slice(0,10);return (M[d.getDay()]||[]).filter(function(h){return hash(key+h)%100<62})}
out.forEach(function(d){var b=D.createElement('button');b.type='button';b.className='dy'+(avail(d).length?'':' full');b.innerHTML=d.toLocaleDateString('fr-FR',{weekday:'short'}).replace('.','')+'<b>'+d.getDate()+'</b>'+d.toLocaleDateString('fr-FR',{month:'short'}).replace('.','');
 b.onclick=function(){sel.d=d;sel.t=null;[].forEach.call(days.children,function(x){x.classList.remove('on')});b.classList.add('on');draw();upd()};days.appendChild(b)});
function draw(){slots.innerHTML='';var a=avail(sel.d);(M[sel.d.getDay()]||[]).forEach(function(h){var b=D.createElement('button');b.type='button';var ok=a.indexOf(h)>-1;b.className='sl2'+(ok?'':' x');b.textContent=h+' h 00';b.onclick=function(){sel.t=h;[].forEach.call(slots.children,function(x){x.classList.remove('on')});b.classList.add('on');upd()};slots.appendChild(b)})}
function upd(){if(sel.d&&sel.t){rec.innerHTML='<b>'+fmt(sel.d)+'</b><span>à '+sel.t+' h 00 · consultation d’une heure</span>';go.disabled=false}else{rec.innerHTML='<b>'+(sel.d?fmt(sel.d):'Aucun créneau choisi')+'</b><span>'+(sel.d?'Choisissez maintenant une heure.':'Sélectionnez un jour puis une heure.')+'</span>';go.disabled=true}}
for(var k=0;k<days.children.length;k++){if(days.children[k].className.indexOf('full')<0){days.children[k].click();break}}
$('bf').onsubmit=function(e){e.preventDefault();if(!sel.t)return;$('bf').style.display='none';$('done').classList.add('on');$('dt').textContent=fmt(sel.d)+' à '+sel.t+' h 00. Un SMS de confirmation vous est envoyé, avec un rappel la veille.'};
var li=D.querySelector('#hr li[data-d="'+new Date().getDay()+'"]');if(li)li.classList.add('today');
})()</script>'''
    js = js.replace("@@ZJ@@", zj)
    return page("Cabinet Lemaire · Ostéopathe à Bordeaux Chartrons", "Ostéopathe D.O. à Bordeaux Chartrons : adultes, enfants, nourrissons, femmes enceintes. Rendez-vous en ligne.",
                "family=Familjen+Grotesk:wght@500;700&family=Figtree:wght@400;500;600;700&family=JetBrains+Mono:wght@500", css, body, js)
