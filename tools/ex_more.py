# -*- coding: utf-8 -*-
"""Trois sites d'exemple supplémentaires : fleuriste, garage auto, ostéopathe.
Chaque site a son propre langage visuel. Les « photos » sont des illustrations dessinées en code ;
chaque emplacement accepte une vraie photo : il suffit de déposer assets/ex/<nom>.jpg."""
import math, random

H = {}          # rempli par examples.py : page, slot, svg, ico


# ============================================================ outils de dessin
def _mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def bloom(cx, cy, r, c1, c2, rot=0, rings=4):
    """Fleur à pétales superposés (pivoine / rose de jardin)."""
    s = []
    for i in range(rings):
        ri = r * (1 - i * 0.22); n = 9 - i
        col = _mix(c1, c2, i / max(1, rings - 1))
        edge = _mix(col, "#000000", .16)
        for k in range(n):
            a = rot + i * 17 + k * 360 / n
            s.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width=".8" transform="rotate(%.1f %.1f %.1f)"/>'
                     % (cx, cy - ri * .5, ri * .46, ri * .62, col, edge, a, cx, cy))
    s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r * .13, _mix(c2, "#5a2a00", .5)))
    for k in range(7):
        a = k * 51.4
        s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#f4c35a"/>' % (cx + math.cos(math.radians(a)) * r * .1, cy + math.sin(math.radians(a)) * r * .1, r * .022))
    return "".join(s)


def leaf(x, y, ln, ang, col="#4f6b45", rib="#cfe0bd"):
    return ('<g transform="translate(%.1f %.1f) rotate(%.1f)"><path d="M0 0Q%.1f %.1f %.1f 0Q%.1f %.1f 0 0Z" fill="%s"/>'
            '<path d="M0 0L%.1f 0" stroke="%s" stroke-width="1.2" opacity=".55"/></g>'
            % (x, y, ang, ln * .5, -ln * .32, ln, ln * .5, ln * .32, col, ln * .94, rib))


def bouquet(seed, c1, c2, bg1, bg2, vw=500, vh=560, uid="b"):
    R = random.Random(seed); s = []
    s.append('<defs><linearGradient id="%sbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
             '<linearGradient id="%spp" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c9a77a"/><stop offset=".5" stop-color="#e3c79c"/><stop offset="1" stop-color="#b8956a"/></linearGradient>'
             '<filter id="%ssh"><feGaussianBlur stdDeviation="9"/></filter></defs>' % (uid, bg1, bg2, uid, uid))
    s.append('<rect width="%d" height="%d" fill="url(#%sbg)"/>' % (vw, vh, uid))
    cx = vw / 2
    s.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="16" fill="#000" opacity=".18" filter="url(#%ssh)"/>' % (cx, vh - 36, vw * .22, uid))
    # tiges
    for k in range(9):
        x2 = cx + R.uniform(-vw * .2, vw * .2)
        s.append('<path d="M%.0f %.0f Q%.0f %.0f %.0f %.0f" stroke="#3f5a38" stroke-width="%.1f" fill="none" stroke-linecap="round"/>' % (cx + R.uniform(-8, 8), vh - 70, (cx + x2) / 2, vh * .62, x2, vh * .42, R.uniform(3, 5)))
    # feuillage
    for k in range(16):
        a = R.uniform(-150, -30); x = cx + R.uniform(-vw * .22, vw * .22); y = vh * R.uniform(.3, .55)
        s.append(leaf(x, y, R.uniform(70, 120), a, R.choice(["#4f6b45", "#5f7d52", "#3f5a38", "#7a9468"])))
    # papier kraft (cône)
    s.append('<path d="M%.0f %.0f L%.0f %.0f L%.0f %.0f Q%.0f %.0f %.0f %.0f Z" fill="url(#%spp)"/>' % (cx - vw * .30, vh * .62, cx + vw * .30, vh * .62, cx + 26, vh - 44, cx, vh - 30, cx - 26, vh - 44, uid))
    s.append('<path d="M%.0f %.0f L%.0f %.0f" stroke="#a4825a" stroke-width="1.5" opacity=".6"/><path d="M%.0f %.0f L%.0f %.0f" stroke="#a4825a" stroke-width="1.5" opacity=".6"/>' % (cx - vw * .12, vh * .62, cx - 8, vh - 50, cx + vw * .14, vh * .62, cx + 10, vh - 50))
    s.append('<rect x="%.0f" y="%.0f" width="%.0f" height="9" rx="4" fill="#e2502c" opacity=".92"/>' % (cx - vw * .2, vh * .74, vw * .4))
    # fleurs
    pos = [(cx, vh * .22, 74), (cx - vw * .2, vh * .3, 62), (cx + vw * .21, vh * .31, 64), (cx - vw * .08, vh * .42, 58), (cx + vw * .1, vh * .43, 56), (cx - vw * .28, vh * .46, 46), (cx + vw * .3, vh * .47, 44)]
    for i, (x, y, r) in enumerate(pos):
        t = (c1, c2) if i % 3 else (c2, c1)
        s.append(bloom(x, y, r * (vw / 500), t[0], t[1], rot=R.randint(0, 40), rings=4))
    for k in range(9):
        x = cx + R.uniform(-vw * .3, vw * .3); y = vh * R.uniform(.2, .5)
        s.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#fff" opacity=".85"/>' % (x, y, R.uniform(3, 6)))
    return H["svg"](vw, vh, "".join(s))


def card_art(seed, pal):
    return bouquet(seed, pal[0], pal[1], pal[2], pal[3], vw=400, vh=440, uid="c%d" % seed)


PALS = {
    "peche": ("#f7b79a", "#e4572e", "#fbe3d5", "#f3c3ae"),
    "rose": ("#f6c4d0", "#d8607f", "#fde8ee", "#f2bfcc"),
    "soleil": ("#fbe18f", "#e9a62e", "#fff3cf", "#f6d78a"),
    "lilas": ("#d7c5f2", "#8059c4", "#efe7fb", "#d3c0f0"),
    "ivoire": ("#fffaf0", "#e9d9bb", "#e8efe0", "#c9d9bd"),
    "rouge": ("#f08a84", "#b01e2b", "#fbe2df", "#f0b3ad"),
}


# ============================================================ 1. FLEURISTE
def fleuriste():
    page, slot, svg, ico = H["page"], H["slot"], H["svg"], H["ico"]
    css = r'''
:root{--bg:#f3ede2;--ink:#201c17;--mut:#6d6559;--co:#e2502c;--sg:#6f8467;--dk:#1f2a1c;--bl:#f3d6cc;--line:#ddd2bf}
html,body{overflow-x:clip}
body{background:var(--bg);color:var(--ink);font:400 17px/1.65 'Inter Tight',system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.f{font-family:'Fraunces',Georgia,serif;font-optical-sizing:auto}
.w{max-width:1240px;margin:0 auto;padding:0 28px}
header.fl{position:sticky;top:0;z-index:40;background:#f3ede2e8;backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
header.fl .w{display:flex;align-items:center;justify-content:space-between;height:74px;gap:18px}
.logo{display:flex;align-items:center;gap:11px;font:italic 600 1.55rem/1 'Fraunces',serif;letter-spacing:-.01em}
.logo i{display:grid;place-items:center;width:38px;height:38px;border-radius:50%;background:var(--co)}
nav.fl{display:flex;gap:26px;font-weight:500;font-size:15.5px}nav.fl a:hover{color:var(--co)}
.btn{display:inline-flex;align-items:center;gap:9px;background:var(--ink);color:#f3ede2;font:600 15.5px/1 'Inter Tight',sans-serif;padding:15px 24px;border-radius:99px;border:0;cursor:pointer;transition:transform .2s,background .2s}
.btn:hover{background:var(--co);transform:translateY(-2px)}.btn.o{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1.5px var(--ink)}.btn.o:hover{background:var(--ink);color:#f3ede2}.btn.c{background:var(--co);color:#fff}
.hero{padding:58px 0 0;position:relative;overflow:hidden}
.hero .w{display:grid;grid-template-columns:1.12fr .88fr;gap:30px;align-items:center}
.eyebrow{display:inline-flex;gap:10px;align-items:center;font:600 13px/1 'Inter Tight',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--sg)}
.eyebrow:before{content:"";width:34px;height:1.5px;background:currentColor}
h1.f{font-weight:400;font-size:clamp(3.1rem,7.6vw,7.2rem);line-height:.93;letter-spacing:-.035em;margin:22px 0 26px}
h1.f em{color:var(--co);font-style:italic;font-weight:300}
.lead{font-size:1.2rem;color:var(--mut);max-width:34em}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin:30px 0 34px}
.trust{display:flex;gap:26px;flex-wrap:wrap;font-weight:500;font-size:14.5px;color:var(--mut)}.trust b{color:var(--ink)}
.arch{position:relative;aspect-ratio:.84;border-radius:999px 999px 28px 28px;overflow:hidden;background:var(--bl);box-shadow:0 40px 80px -30px #5a2a1a55}
.arch .sl svg{width:100%;height:100%}
.badge{position:absolute;left:-26px;bottom:44px;width:132px;height:132px;animation:spin 22s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.herowrap{position:relative}.herowrap .badge{z-index:3}
.band{margin-top:64px;background:var(--ink);color:#f3ede2;overflow:hidden;white-space:nowrap;padding:18px 0;font:italic 400 1.6rem/1 'Fraunces',serif}
.band div{display:inline-block;animation:mq 38s linear infinite}.band span{margin:0 26px}.band b{color:var(--co);font-style:normal}
@keyframes mq{to{transform:translateX(-50%)}}
@media(prefers-reduced-motion:reduce){.band div,.badge{animation:none}}
section.s{padding:104px 0}
h2.f{font-weight:400;font-size:clamp(2.2rem,4.6vw,4rem);line-height:1;letter-spacing:-.03em;margin:14px 0 0}
h2.f em{font-style:italic;font-weight:300;color:var(--co)}
.sh{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;margin-bottom:42px}
.arrows{display:flex;gap:10px}.arrows button{width:52px;height:52px;border-radius:50%;border:1.5px solid var(--ink);background:transparent;cursor:pointer;display:grid;place-items:center;transition:.2s}.arrows button:hover{background:var(--ink);color:#fff}
.rail{display:flex;gap:22px;overflow-x:auto;scroll-snap-type:x mandatory;padding:4px 28px 26px;margin:0 -28px;scroll-padding-left:28px;scrollbar-width:none}.rail::-webkit-scrollbar{display:none}
.pc{flex:0 0 min(300px,78vw);scroll-snap-align:start}
.pc .ph{aspect-ratio:.9;border-radius:22px;overflow:hidden;position:relative;transition:transform .35s}
.pc:hover .ph{transform:translateY(-6px) rotate(-.6deg)}
.pc .ph .sl svg{width:100%;height:100%}
.tag{position:absolute;left:14px;top:14px;background:#fff;border-radius:99px;font:600 12px/1 'Inter Tight',sans-serif;padding:8px 12px;z-index:2}
.pc h3{font:500 1.5rem/1.1 'Fraunces',serif;margin:16px 0 4px;letter-spacing:-.01em}.pc p{color:var(--mut);font-size:15.5px;min-height:4.9em}
.pc .row{display:flex;align-items:center;justify-content:space-between;margin-top:12px}
.pc .pr{font:500 1.35rem/1 'Fraunces',serif}.pc .ad{border:1.5px solid var(--ink);background:transparent;border-radius:99px;padding:10px 18px;font:600 14px/1 'Inter Tight',sans-serif;cursor:pointer;transition:.2s}.pc .ad:hover,.pc .ad.ok{background:var(--co);border-color:var(--co);color:#fff}
.sub{background:var(--dk);color:#f3ede2;border-radius:36px;margin:0 20px;padding:96px 0}
.sub .eyebrow{color:#b8cbab}.sub h2 em{color:#f0a68b}
.plans{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:46px}
.plan{border:1px solid #ffffff2e;border-radius:26px;padding:34px 30px;display:flex;flex-direction:column;gap:6px;background:#ffffff08;transition:.3s}.plan:hover{background:#ffffff12;transform:translateY(-4px)}
.plan.pop{background:var(--co);border-color:var(--co);color:#fff}
.plan h3{font:italic 400 1.9rem/1 'Fraunces',serif}.plan .pr{font:300 3.6rem/1 'Fraunces',serif;letter-spacing:-.03em;margin:14px 0 4px}.plan .pr small{font:500 1rem 'Inter Tight',sans-serif;opacity:.7}
.plan ul{margin:14px 0 22px;display:grid;gap:9px;font-size:15.5px}.plan li{display:flex;gap:10px}.plan li:before{content:"✓";font-weight:700;color:#b8cbab}.plan.pop li:before{color:#fff}
.plan .btn{margin-top:auto;justify-content:center;background:#f3ede2;color:var(--ink)}.plan.pop .btn{background:#fff;color:var(--co)}
.ev{border-top:1.5px solid var(--ink)}
.evr{display:grid;grid-template-columns:90px 1.1fr 1.4fr auto;gap:28px;align-items:center;padding:36px 0;border-bottom:1.5px solid var(--ink);transition:.25s}.evr:hover{padding-left:14px;background:#fff6}
.evr .n{font:italic 300 2.6rem/1 'Fraunces',serif;color:var(--co)}.evr h3{font:400 2.1rem/1 'Fraunces',serif;letter-spacing:-.02em}.evr p{color:var(--mut)}.evr .fr{font-weight:600;white-space:nowrap}
.about{display:grid;grid-template-columns:.9fr 1.1fr;gap:70px;align-items:center}
.about .pt{aspect-ratio:.82;border-radius:999px 999px 24px 24px;overflow:hidden;background:#cfd9c1}.about .pt .sl svg{width:100%;height:100%}
.about p{margin-top:18px;color:#4d463c}.sig{font:italic 400 2rem/1 'Fraunces',serif;color:var(--co);margin-top:26px}
.stats{display:flex;gap:40px;margin-top:34px;flex-wrap:wrap}.stats b{display:block;font:300 3rem/1 'Fraunces',serif;letter-spacing:-.03em}.stats span{font-size:14px;color:var(--mut)}
.rv{background:var(--bl);border-radius:36px;margin:0 20px}
.rvs{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:42px}
.rc{background:#fff;border-radius:24px;padding:30px;display:flex;flex-direction:column;gap:14px}.rc .st{color:var(--co);letter-spacing:3px}.rc p{font:400 1.2rem/1.45 'Fraunces',serif}.rc small{color:var(--mut);font-size:14px}
.info{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.box{background:#fff;border-radius:28px;padding:36px}
.hrs li{display:flex;justify-content:space-between;padding:13px 0;border-bottom:1px solid var(--line);font-size:16px}.hrs li:last-child{border:0}.hrs b{font-weight:600}
.hrs li.today{color:var(--co);font-weight:700}
.map{border-radius:20px;overflow:hidden;aspect-ratio:1.5;background:#e9e2d3;margin-bottom:20px}.map svg{width:100%;height:100%;display:block}
.det details{border-bottom:1.5px solid var(--ink);padding:24px 0}.det summary{cursor:pointer;font:400 1.5rem/1.2 'Fraunces',serif;list-style:none;display:flex;justify-content:space-between;gap:20px}.det summary::-webkit-details-marker{display:none}.det summary:after{content:"+";font-size:1.8rem;line-height:1;color:var(--co);transition:.2s}.det details[open] summary:after{transform:rotate(45deg)}.det p{margin-top:14px;color:var(--mut);max-width:46em}
.order{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:start}
form.of{display:grid;gap:16px}.of label{display:grid;gap:7px;font-weight:600;font-size:14px}
.of input,.of select,.of textarea{font:400 16px 'Inter Tight',sans-serif;padding:15px 16px;border-radius:14px;border:1.5px solid var(--line);background:#fff;color:var(--ink)}.of input:focus,.of select:focus,.of textarea:focus{outline:0;border-color:var(--co);box-shadow:0 0 0 4px #e2502c22}
.of .two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.ok{display:none;background:#e6f0df;border-radius:16px;padding:18px 20px;font-weight:600}.ok.on{display:block}
.toast{position:fixed;left:50%;bottom:90px;transform:translate(-50%,30px);background:var(--ink);color:#fff;padding:14px 22px;border-radius:99px;font-weight:600;opacity:0;transition:.3s;z-index:90;pointer-events:none}.toast.on{opacity:1;transform:translate(-50%,0)}
footer.ft{background:var(--ink);color:#d9d1c2;padding:70px 0 40px;margin-top:104px}
footer.ft .w{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:40px}footer.ft h4{font:600 13px 'Inter Tight';letter-spacing:.14em;text-transform:uppercase;color:#f3ede2;margin-bottom:16px}footer.ft li{margin:8px 0;font-size:15px}footer.ft .big{font:italic 400 2.2rem/1.1 'Fraunces',serif;color:#f3ede2}.legal{grid-column:1/-1;border-top:1px solid #ffffff22;padding-top:26px;font-size:13px;color:#a59d8e}
@media(max-width:960px){.hero .w,.about,.order,.info{grid-template-columns:1fr}.plans,.rvs{grid-template-columns:1fr}.evr{grid-template-columns:60px 1fr;gap:14px}.evr p,.evr .fr{grid-column:2}nav.fl{display:none}footer.ft .w{grid-template-columns:1fr 1fr}.sub,.rv{margin:0 10px;border-radius:26px}.badge{left:6px;bottom:20px;width:104px;height:104px}h1.f{margin-top:16px}section.s{padding:72px 0}.arch{max-width:520px}}
'''
    pal = list(PALS.items())
    prods = [
        ("Le Matin", "Pivoines pêche, eucalyptus, brins de gypsophile. Un bouquet généreux et aérien.", 35, "peche", "Best-seller"),
        ("Pivoine d’été", "Dix pivoines roses en bouquet rond, feuillage de jardin. Saison : mai à juillet.", 48, "rose", "De saison"),
        ("Champêtre", "Marguerites, renoncules et graminées, noué à la main. Simple et lumineux.", 42, "soleil", ""),
        ("Brume lilas", "Delphiniums, lisianthus et lavande. Des tons doux, un parfum discret.", 44, "lilas", "Nouveau"),
        ("Nuage blanc", "Roses ivoire, hortensias et verdure fine. Pour offrir sans se tromper.", 52, "ivoire", ""),
        ("Grand Jardin", "Le bouquet signature de l’atelier : vingt tiges, trois formes, un papier kraft.", 78, "rouge", "Signature"),
    ]
    cards = ""
    for i, (nm, ds, pr, pk, tg) in enumerate(prods):
        art = slot("fleur-%d" % (i + 1), card_art(i + 3, PALS[pk]))
        cards += ('<article class="pc"><div class="ph">%s%s</div><h3>%s</h3><p>%s</p><div class="row"><span class="pr">%d €</span>'
                  '<button class="ad" type="button" data-n="%s">Ajouter</button></div></article>'
                  % (art, ('<span class="tag">%s</span>' % tg) if tg else "", nm, ds, pr, nm))
    options = "".join('<option>%s — %d €</option>' % (n, p) for n, _, p, _, _ in prods)
    hero_art = slot("fleur-hero", bouquet(11, "#f7b79a", "#e4572e", "#f8d9c9", "#f3c3ae", vw=560, vh=660, uid="h"))
    portrait = slot("fleur-atelier", svg(500, 610, '<defs><linearGradient id="pg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfe8d2"/><stop offset="1" stop-color="#b5c5a3"/></linearGradient></defs><rect width="500" height="610" fill="url(#pg)"/>'
        + "".join(leaf(250 + math.cos(math.radians(a)) * 20, 560, 330 - abs(a + 90) * 1.1, a, c) for a, c in [(-160, "#4f6b45"), (-135, "#5f7d52"), (-110, "#3f5a38"), (-90, "#6f8f60"), (-70, "#4f6b45"), (-45, "#5f7d52"), (-20, "#3f5a38")])
        + bloom(250, 250, 88, "#f6c4d0", "#d8607f", 10) + bloom(150, 330, 56, "#fbe18f", "#e9a62e", 30) + bloom(352, 340, 60, "#f7b79a", "#e4572e", 0)))
    badge = ('<svg class="badge" viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="58" fill="#e2502c"/><defs><path id="cp" d="M60 60m-40 0a40 40 0 1 1 80 0a40 40 0 1 1 -80 0"/></defs>'
             '<text font-family="Inter Tight,sans-serif" font-weight="700" font-size="10.5" fill="#fff"><textPath href="#cp" textLength="246" lengthAdjust="spacing">FAIT MAIN À LYON · DE SAISON · </textPath></text>'
             + '<g transform="translate(60 60) scale(.42)">' + bloom(0, 0, 40, "#ffffff", "#ffe1d5", 0, 3) + '</g></svg>')
    mapsvg = svg(600, 400, '<rect width="600" height="400" fill="#e9e2d3"/><path d="M0 120H600M0 260H600M140 0V400M330 0V400M470 0V400" stroke="#fff" stroke-width="16"/><path d="M0 330Q200 280 600 340" stroke="#cdd9bf" stroke-width="40" fill="none"/>'
                 '<path d="M250 200 q28-62 56 0 q0 34-28 62 q-28-28-28-62z" fill="#e2502c"/><circle cx="278" cy="198" r="11" fill="#fff"/>', "")
    order = '''<div class="det"><details><summary>Livrez-vous le jour même ?</summary><p>Oui, pour toute commande passée avant 14 h du mardi au samedi, à Lyon (1er au 9e) et Villeurbanne. Livraison à vélo cargo : 7 €, offerte dès 60 € d’achat.</p></details>
<details><summary>Puis-je ajouter un message ?</summary><p>Toujours. Camille l’écrit à la main sur une carte, sans le lire à voix haute au livreur : promis.</p></details>
<details><summary>Combien de temps durent mes fleurs ?</summary><p>Entre 7 et 10 jours avec une eau changée tous les deux jours et une tige recoupée en biais. Une petite fiche d’entretien est glissée dans chaque bouquet.</p></details>
<details><summary>Faites-vous les mariages et les deuils ?</summary><p>Oui. Mariages sur rendez-vous (trois mois avant, idéalement) et deuils sous 24 h, avec livraison au lieu de cérémonie.</p></details>
<details><summary>Puis-je changer ou arrêter mon abonnement ?</summary><p>À tout moment, en un message, jusqu’à 5 jours avant la prochaine livraison. Sans frais et sans engagement.</p></details></div>'''
    body = '''
<header class="fl"><div class="w"><a class="logo" href="#top"><i>@@LOGOI@@</i>Atelier Pivoine</a>
<nav class="fl"><a href="#bouquets">Bouquets</a><a href="#abo">Abonnements</a><a href="#events">Mariages &amp; deuils</a><a href="#atelier">L’atelier</a><a href="#infos">Horaires</a></nav>
<a class="btn" href="#commander">Commander</a></div></header>
<main id="top">
<section class="hero"><div class="w"><div><span class="eyebrow">Fleuriste indépendante · Lyon 1er</span>
<h1 class="f">Des fleurs qui <em>racontent</em> quelque chose.</h1>
<p class="lead">Bouquets composés le matin même avec des fleurs de saison, cultivées à moins de 150 km de l’atelier. Livrés à vélo dans tout Lyon, ou à emporter rue des Tables Claudiennes.</p>
<div class="cta"><a class="btn c" href="#commander">Commander un bouquet @@ARR@@</a><a class="btn o" href="#bouquets">Voir les bouquets</a></div>
<div class="trust"><span><b>4,9 / 5</b> · 126 avis</span><span><b>Livraison</b> à vélo, le jour même</span><span><b>Sans pesticide</b> ni importation lointaine</span></div></div>
<div class="herowrap"><div class="arch">@@HERO@@</div>@@BADGE@@</div></div>
<div class="band" aria-hidden="true"><div>@@MQ@@@@MQ@@</div></div></section>

<section class="s" id="bouquets"><div class="w"><div class="sh"><div><span class="eyebrow">Cette semaine</span><h2 class="f">Les bouquets <em>du moment</em></h2></div>
<div class="arrows"><button type="button" id="pv" aria-label="Précédent">@@L@@</button><button type="button" id="nx" aria-label="Suivant">@@ARR@@</button></div></div>
<div class="rail" id="rail">@@CARDS@@</div></div></section>

<section class="sub" id="abo"><div class="w"><span class="eyebrow">Abonnement floral</span><h2 class="f">Des fleurs fraîches, <em>sans y penser.</em></h2>
<p class="lead" style="color:#cfd8c6;margin-top:18px">Choisissez un rythme. Camille compose chaque bouquet selon la saison et vous le livre à domicile ou au bureau. Arrêt possible à tout moment.</p>
<div class="plans">
<div class="plan"><h3>Mensuel</h3><div class="pr">39 €<small> / mois</small></div><p style="opacity:.75">Un bouquet par mois</p><ul><li>Bouquet de saison, 15 tiges</li><li>Livraison incluse</li><li>Carte manuscrite</li></ul><a class="btn" href="#commander">Choisir</a></div>
<div class="plan pop"><h3>Quinzaine</h3><div class="pr">72 €<small> / mois</small></div><p style="opacity:.9">Deux bouquets par mois</p><ul><li>Bouquets de 18 tiges</li><li>Livraison incluse</li><li>Vase en grès offert au départ</li></ul><a class="btn" href="#commander">Choisir</a></div>
<div class="plan"><h3>Hebdo</h3><div class="pr">135 €<small> / mois</small></div><p style="opacity:.75">Un bouquet par semaine</p><ul><li>Idéal restaurants et bureaux</li><li>Livraison incluse</li><li>Facture mensuelle</li></ul><a class="btn" href="#commander">Choisir</a></div>
</div></div></section>

<section class="s" id="events"><div class="w"><div class="sh"><div><span class="eyebrow">Sur rendez-vous</span><h2 class="f">Les grands moments, <em>sans stress.</em></h2></div></div>
<div class="ev">
<div class="evr"><span class="n">01</span><h3>Mariages</h3><p>Bouquet de mariée, boutonnières, arche et centres de table. Rendez-vous gratuit à l’atelier pour choisir les couleurs.</p><span class="fr">dès 450 €</span></div>
<div class="evr"><span class="n">02</span><h3>Deuils</h3><p>Gerbes, coussins et compositions livrés au lieu de cérémonie sous 24 h, partout dans le Rhône.</p><span class="fr">dès 85 €</span></div>
<div class="evr"><span class="n">03</span><h3>Entreprises</h3><p>Accueil, réception, restaurants : un abonnement hebdomadaire et des compositions au rythme de vos événements.</p><span class="fr">sur devis</span></div>
</div></div></section>

<section class="s" id="atelier" style="padding-top:20px"><div class="w about"><div class="pt">@@PORTRAIT@@</div>
<div><span class="eyebrow">L’atelier</span><h2 class="f">Camille Roux, <em>fleuriste</em> depuis 2014.</h2>
<p>Après dix ans dans une grande maison parisienne, j’ai ouvert l’Atelier Pivoine pour faire simple : peu de fleurs, mais les meilleures, choisies chez trois producteurs de la région que je connais par leur prénom.</p>
<p>Chaque bouquet est composé le matin même, noué à la main et emballé dans du papier kraft recyclable. Pas de mousse florale, pas de plastique.</p>
<div class="stats"><div><b>150 km</b><span>rayon maximum des producteurs</span></div><div><b>10 ans</b><span>de métier</span></div><div><b>3 200</b><span>bouquets livrés l’an dernier</span></div></div>
<div class="sig">— Camille</div></div></div></section>

<section class="s rv"><div class="w"><span class="eyebrow" style="color:#9a4b32">Avis clients</span><h2 class="f">Ils en parlent <em>mieux que nous.</em></h2>
<div class="rvs">
<div class="rc"><span class="st">★★★★★</span><p>« Livré à vélo en 2 heures pour l’anniversaire de ma mère. Le bouquet était encore plus beau que sur la photo. »</p><small>Julie M. · Lyon 6e</small></div>
<div class="rc"><span class="st">★★★★★</span><p>« On a pris l’abonnement hebdo pour le restaurant. Les clients nous en parlent chaque semaine. »</p><small>Antoine R. · restaurateur</small></div>
<div class="rc"><span class="st">★★★★★</span><p>« Camille a tout géré pour notre mariage, avec une patience incroyable. Les fleurs ont tenu trois jours. »</p><small>Sarah &amp; Thomas · mariés en juin</small></div></div></div></section>

<section class="s" id="infos"><div class="w"><div class="sh"><div><span class="eyebrow">Passer nous voir</span><h2 class="f">Horaires <em>&amp; accès</em></h2></div></div>
<div class="info"><div class="box"><ul class="hrs" id="hrs"><li data-d="1"><span>Lundi</span><b>Fermé</b></li><li data-d="2"><span>Mardi</span><b>9 h 30 – 19 h</b></li><li data-d="3"><span>Mercredi</span><b>9 h 30 – 19 h</b></li><li data-d="4"><span>Jeudi</span><b>9 h 30 – 19 h</b></li><li data-d="5"><span>Vendredi</span><b>9 h 30 – 19 h</b></li><li data-d="6"><span>Samedi</span><b>9 h – 19 h</b></li><li data-d="0"><span>Dimanche</span><b>9 h 30 – 13 h</b></li></ul></div>
<div class="box"><div class="map">@@MAP@@</div><p><b>Atelier Pivoine</b><br>14 rue des Tables Claudiennes, 69001 Lyon<br>04 78 00 00 00 · bonjour@atelierpivoine.fr</p><p style="color:var(--mut);margin-top:10px;font-size:15px">Métro Croix-Paquet (ligne C) · Parking Terreaux à 4 min.</p></div></div></div></section>

<section class="s" style="padding-top:20px"><div class="w order"><div><span class="eyebrow">Questions fréquentes</span><h2 class="f">On vous <em>répond.</em></h2><div class="det" style="margin-top:34px">@@FAQ@@</div></div>
<div id="commander"><span class="eyebrow">Commander</span><h2 class="f">Un bouquet, <em>une adresse.</em></h2>
<form class="of" id="of" style="margin-top:30px"><label>Bouquet<select id="sel">@@OPT@@</select></label>
<div class="two"><label>Livraison ou retrait<select><option>Livraison à vélo (7 €)</option><option>Retrait à l’atelier (gratuit)</option></select></label><label>Date<input type="date" required></label></div>
<label>Nom et téléphone<input required placeholder="Camille Dupont · 06 00 00 00 00"></label><label>Message pour la carte<textarea rows="3" placeholder="Joyeux anniversaire…"></textarea></label>
<button class="btn c" type="submit" style="justify-content:center">Envoyer ma commande</button><div class="ok" id="ok">Merci ! Camille vous rappelle dans l’heure pour confirmer le créneau et régler.</div></form></div></div></section>
</main>
<footer class="ft"><div class="w"><div><div class="big">Atelier Pivoine</div><p style="margin-top:14px;max-width:26em;color:#a59d8e">Fleuriste indépendante, Lyon 1er. Des fleurs de saison, des producteurs de la région.</p></div>
<div><h4>Boutique</h4><ul><li><a href="#bouquets">Bouquets</a></li><li><a href="#abo">Abonnements</a></li><li><a href="#events">Mariages &amp; deuils</a></li></ul></div>
<div><h4>Contact</h4><ul><li>04 78 00 00 00</li><li>bonjour@atelierpivoine.fr</li><li>Instagram @atelierpivoine</li></ul></div>
<div><h4>Infos</h4><ul><li>Mentions légales</li><li>CGV</li><li>Livraison &amp; retours</li></ul></div>
<div class="legal">© 2026 Atelier Pivoine · SARL au capital de 5 000 € · SIRET 000 000 000 00000 (exemple) · Hébergeur : Cloudflare, Inc.</div></div></footer>
<div class="toast" id="toast" role="status"></div>
'''
    mq = "".join('<span>%s</span><b>✿</b>' % t for t in ["Bouquets du jour", "Mariages", "Abonnements", "Deuils", "Livraison à vélo", "Fleurs de saison", "Entreprises"])
    logoi = ico("leaf", 20, "#fff", 1.9)
    body = (body.replace("@@LOGOI@@", logoi).replace("@@ARR@@", ico("arrow", 18)).replace("@@L@@", '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>')
            .replace("@@HERO@@", hero_art).replace("@@BADGE@@", badge).replace("@@MQ@@", mq).replace("@@CARDS@@", cards).replace("@@PORTRAIT@@", portrait)
            .replace("@@MAP@@", mapsvg).replace("@@FAQ@@", order).replace("@@OPT@@", options))
    js = r'''<script>(function(){
var r=document.getElementById('rail');function go(d){r.scrollBy({left:d*(r.firstElementChild.offsetWidth+22),behavior:'smooth'})}
document.getElementById('pv').onclick=function(){go(-1)};document.getElementById('nx').onclick=function(){go(1)};
var t=document.getElementById('toast'),to;function say(m){t.textContent=m;t.classList.add('on');clearTimeout(to);to=setTimeout(function(){t.classList.remove('on')},2200)}
var sel=document.getElementById('sel');document.querySelectorAll('.ad').forEach(function(b){b.onclick=function(){b.classList.add('ok');b.textContent='Ajouté ✓';for(var i=0;i<sel.options.length;i++)if(sel.options[i].text.indexOf(b.dataset.n)===0)sel.selectedIndex=i;say(b.dataset.n+' ajouté à votre commande');setTimeout(function(){b.classList.remove('ok');b.textContent='Ajouter'},2200)}});
document.getElementById('of').onsubmit=function(e){e.preventDefault();document.getElementById('ok').classList.add('on')};
var d=new Date().getDay(),li=document.querySelector('#hrs li[data-d="'+d+'"]');if(li)li.classList.add('today');
})()</script>'''
    return page("Atelier Pivoine · Fleuriste à Lyon", "Fleuriste indépendante à Lyon 1er : bouquets de saison, abonnements, mariages et livraison à vélo.",
                "family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,300;1,9..144,400;1,9..144,600&family=Inter+Tight:wght@400;500;600;700",
                css, body, js)


# ============================================================ 2. GARAGE
def wheel(cx, cy, r=58):
    s = ['<circle cx="%d" cy="%d" r="%d" fill="#0a0a0b"/><circle cx="%d" cy="%d" r="%d" fill="#17181b"/>' % (cx, cy, r, cx, cy, r - 9),
         '<circle cx="%d" cy="%d" r="%d" fill="#2a2d33"/>' % (cx, cy, r - 18)]
    for k in range(5):
        a = k * 72 - 90
        x2 = cx + math.cos(math.radians(a)) * (r - 20); y2 = cy + math.sin(math.radians(a)) * (r - 20)
        s.append('<path d="M%d %d L%.1f %.1f" stroke="#c9ced6" stroke-width="7" stroke-linecap="round"/>' % (cx, cy, x2, y2))
        s.append('<path d="M%d %d L%.1f %.1f" stroke="#ff5a1f" stroke-width="1.6" stroke-linecap="round" opacity=".85"/>' % (cx, cy, x2, y2))
    s.append('<circle cx="%d" cy="%d" r="9" fill="#e5e8ed"/><circle cx="%d" cy="%d" r="3.5" fill="#0a0a0b"/>' % (cx, cy, cx, cy))
    s.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#3a3d44" stroke-width="2"/>' % (cx, cy, r - 9))
    return "".join(s)


def car_art(uid="car"):
    d = ('<defs><linearGradient id="%sb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3f48"/><stop offset=".55" stop-color="#1f2329"/><stop offset="1" stop-color="#121417"/></linearGradient>'
         '<linearGradient id="%sg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7fa0b8"/><stop offset=".5" stop-color="#2d4252"/><stop offset="1" stop-color="#111b24"/></linearGradient>'
         '<radialGradient id="%sl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ff5a1f" stop-opacity=".55"/><stop offset="1" stop-color="#ff5a1f" stop-opacity="0"/></radialGradient>'
         '<filter id="%ss"><feGaussianBlur stdDeviation="8"/></filter></defs>' % (uid, uid, uid, uid))
    d += '<ellipse cx="410" cy="352" rx="330" ry="18" fill="#000" opacity=".7" filter="url(#%ss)"/>' % uid
    d += '<ellipse cx="410" cy="300" rx="380" ry="80" fill="url(#%sl)" opacity=".45"/>' % uid
    for i, y in enumerate((150, 175, 200, 232)):
        d += '<path d="M%d %d H%d" stroke="#ff5a1f" stroke-width="2.5" stroke-linecap="round" opacity="%.2f"/>' % (20 + i * 22, y, 80 + i * 20, .55 - i * .1)
    body = ('M86 292 L70 262 Q64 236 84 228 L150 218 Q205 214 242 160 Q262 128 300 124 L470 120 Q520 122 556 150 L640 214 Q712 220 748 244 Q770 262 764 292 L706 296 '
            'A58 58 0 0 0 594 296 L322 296 A58 58 0 0 0 206 296 Z')
    d += '<path d="%s" fill="url(#%sb)" stroke="#0a0a0b" stroke-width="2"/>' % (body, uid)
    d += '<path d="M268 164 Q286 140 310 138 L462 134 Q505 136 536 160 L608 214 L246 214 Q258 190 268 164 Z" fill="url(#%sg)" stroke="#0a0a0b" stroke-width="2"/>' % uid
    d += '<path d="M392 138 L402 214" stroke="#0a0a0b" stroke-width="5"/><path d="M286 160 Q330 150 392 150" stroke="#fff" stroke-width="2" opacity=".18" fill="none"/>'
    d += '<path d="M92 252 L750 252" stroke="#4a5059" stroke-width="1.5" opacity=".55"/><path d="M110 270 L296 270 M604 270 L728 270" stroke="#ff5a1f" stroke-width="5" stroke-linecap="round"/>'
    d += '<path d="M700 236 Q742 240 758 256 L710 256 Z" fill="#ffe8c2"/><path d="M700 236 Q742 240 758 256" stroke="#ff5a1f" stroke-width="3" fill="none"/><path d="M84 236 L110 232 L110 250 L82 250 Z" fill="#c4161c"/>'
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
        col = "#ff5a1f" if i > 32 else "#e5e8ed"
        s.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="%d" stroke-linecap="round"/>' % (x1, y1, x2, y2, col, 3 if big else 1.5))
    s.append('<path d="M150 150 L%.1f %.1f" stroke="#ff5a1f" stroke-width="5" stroke-linecap="round"/>' % (150 + math.cos(math.radians(135 + 6.75 * 26)) * 96, 150 + math.sin(math.radians(135 + 6.75 * 26)) * 96))
    s.append('<circle cx="150" cy="150" r="14" fill="#e5e8ed"/><circle cx="150" cy="150" r="5" fill="#0b0c0e"/><text x="150" y="218" text-anchor="middle" font-family="Barlow Condensed,sans-serif" font-weight="700" font-size="22" letter-spacing="4" fill="#9ba1ac">KM/H</text>')
    return "".join(s)


def garage():
    page, slot, svg, ico = H["page"], H["slot"], H["svg"], H["ico"]
    css = r'''
:root{--bg:#0b0c0e;--p:#14161a;--p2:#1b1e23;--ink:#f2f3f5;--mut:#9ba1ac;--or:#ff5a1f;--ln:#262a31}
html,body{overflow-x:clip}
body{background:var(--bg);color:var(--ink);font:400 17px/1.6 'Barlow',system-ui,sans-serif}
.c{font-family:'Barlow Condensed','Arial Narrow','Liberation Sans Narrow',sans-serif;text-transform:uppercase;letter-spacing:.01em}
.w{max-width:1280px;margin:0 auto;padding:0 28px}
.top{background:#000;border-bottom:1px solid var(--ln);font-size:14px}.top .w{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-top:9px;padding-bottom:9px;color:var(--mut)}
.live{display:inline-flex;align-items:center;gap:8px;font-weight:600;color:var(--ink)}.live i{width:9px;height:9px;border-radius:50%;background:#2fd06a;box-shadow:0 0 0 0 #2fd06a99;animation:pl 2s infinite}.live.off i{background:#e0483a;animation:none}
@keyframes pl{70%{box-shadow:0 0 0 9px #2fd06a00}100%{box-shadow:0 0 0 0 #2fd06a00}}
@media(prefers-reduced-motion:reduce){.live i,.mq div{animation:none}}
header.g{position:sticky;top:0;z-index:40;background:#0b0c0ef0;backdrop-filter:blur(12px);border-bottom:1px solid var(--ln)}
header.g .w{display:flex;justify-content:space-between;align-items:center;height:78px;gap:20px}@media(max-width:600px){header.g .w{height:64px;gap:10px;padding:0 14px}header.g .lg{font-size:1.25rem;gap:8px}header.g .lg small{display:none}header.g .bt{padding:12px 14px;font-size:14px}header.o .lg{font-size:1.4rem}}
.lg{display:flex;align-items:center;gap:12px;font:800 1.9rem/1 'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.04em}.lg small{display:block;font:600 .62rem/1 'Barlow',sans-serif;letter-spacing:.3em;color:var(--mut);margin-top:5px}
.lg i{display:grid;place-items:center;width:44px;height:44px;background:var(--or);clip-path:polygon(0 0,100% 0,100% 70%,70% 100%,0 100%)}
nav.g{display:flex;gap:30px;font:600 15px 'Barlow',sans-serif;text-transform:uppercase;letter-spacing:.1em}nav.g a{color:var(--mut)}nav.g a:hover{color:var(--or)}
.bt{display:inline-flex;align-items:center;gap:10px;background:var(--or);color:#0b0c0e;font:700 16px/1 'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.08em;padding:17px 26px;border:0;cursor:pointer;clip-path:polygon(0 0,100% 0,100% calc(100% - 12px),calc(100% - 12px) 100%,0 100%);transition:.2s}
.bt:hover{background:#fff}.bt.o{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 2px var(--ln);clip-path:none}.bt.o:hover{box-shadow:inset 0 0 0 2px var(--or);background:transparent;color:var(--or)}
.hero{position:relative;overflow:hidden;border-bottom:1px solid var(--ln)}
.hero:before{content:"";position:absolute;inset:0;background:radial-gradient(900px 520px at 78% 40%,#ff5a1f26,transparent 60%),repeating-linear-gradient(90deg,#ffffff05 0 1px,transparent 1px 90px)}
.hero .w{position:relative;display:grid;grid-template-columns:1.05fr 1fr;gap:20px;align-items:center;padding-top:70px;padding-bottom:40px}
.tg{display:inline-flex;gap:10px;align-items:center;border:1px solid var(--ln);padding:8px 14px;font:600 13px/1 'Barlow',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}.tg b{color:var(--or)}
h1.c{font-weight:800;font-size:clamp(3.2rem,7.4vw,7.4rem);line-height:.88;margin:26px 0 22px;letter-spacing:-.005em}h1.c em{font-style:normal;color:var(--or)}
.lead{color:var(--mut);font-size:1.18rem;max-width:30em}
.devis{margin-top:32px;background:var(--p);border:1px solid var(--ln);padding:22px;display:grid;grid-template-columns:auto 1fr 1fr auto;gap:12px;align-items:end;max-width:760px}
.devis label{display:grid;gap:7px;font:600 12px 'Barlow',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.plate{display:flex;align-items:stretch;background:#fff;border-radius:6px;overflow:hidden;height:50px;min-width:190px;box-shadow:0 0 0 2px #111}.plate b{width:30px;background:#133b9c;color:#fff;display:grid;place-items:end center;padding-bottom:4px;font:700 11px 'Barlow'}.plate input{border:0;outline:0;font:800 1.55rem 'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.12em;text-align:center;width:100%;color:#111;background:#fff}
.devis select{height:50px;background:var(--p2);color:var(--ink);border:1px solid var(--ln);font:500 16px 'Barlow',sans-serif;padding:0 12px}
.est{grid-column:1/-1;display:none;align-items:center;gap:16px;border-top:1px dashed var(--ln);padding-top:16px;flex-wrap:wrap}.est.on{display:flex}.est b{font:800 2.4rem/1 'Barlow Condensed',sans-serif;color:var(--or)}.est span{color:var(--mut);font-size:15px}
.stage{position:relative}.stage>svg:not(.dl){display:block;width:100%;height:auto}.stage .dl{position:absolute;right:3%;top:-16%;width:27%;height:auto;opacity:.96;z-index:2}
.kpi{position:relative;border-top:1px solid var(--ln);display:grid;grid-template-columns:repeat(4,1fr);background:var(--p)}
.kpi div{padding:24px 28px;border-right:1px solid var(--ln)}.kpi div:last-child{border:0}.kpi b{display:block;font:800 2.5rem/1 'Barlow Condensed',sans-serif;color:var(--or)}.kpi span{color:var(--mut);font-size:15px}
section.s{padding:100px 0;border-bottom:1px solid var(--ln)}
.lb{font:600 13px/1 'Barlow',sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--or);display:flex;gap:10px;align-items:center}.lb:before{content:"";width:28px;height:2px;background:var(--or)}
h2.c{font-weight:800;font-size:clamp(2.6rem,5.4vw,4.8rem);line-height:.92;margin:16px 0 0}
.sg{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--ln);border:1px solid var(--ln);margin-top:48px}
.sv{background:var(--bg);padding:34px 30px 30px;position:relative;display:flex;flex-direction:column;gap:10px;transition:background .25s}.sv:hover{background:var(--p2)}
.sv .n{font:700 .95rem 'Barlow Condensed',sans-serif;color:var(--or);letter-spacing:.2em}.sv h3{font:800 2rem/1 'Barlow Condensed',sans-serif;text-transform:uppercase}.sv p{color:var(--mut);font-size:15.5px}
.sv .pr{margin-top:auto;padding-top:14px;display:flex;align-items:baseline;justify-content:space-between;border-top:1px solid var(--ln)}.sv .pr b{font:800 2.2rem/1 'Barlow Condensed',sans-serif}.sv .pr small{color:var(--mut)}
.sv .du{position:absolute;right:24px;top:30px;font:600 12px 'Barlow';letter-spacing:.14em;text-transform:uppercase;border:1px solid var(--ln);padding:6px 9px;color:var(--mut)}
.why{display:grid;grid-template-columns:1fr 1fr;gap:70px;align-items:center}
.pt{display:grid;gap:0;margin-top:36px;border-top:1px solid var(--ln)}.pt div{display:grid;grid-template-columns:60px 1fr;gap:18px;padding:22px 0;border-bottom:1px solid var(--ln)}.pt i{display:grid;place-items:center;width:52px;height:52px;border:1px solid var(--ln);color:var(--or)}.pt h4{font:700 1.5rem/1 'Barlow Condensed',sans-serif;text-transform:uppercase}.pt p{color:var(--mut);font-size:15.5px;margin-top:4px}
.bay{position:relative;aspect-ratio:1.05;background:var(--p);border:1px solid var(--ln);overflow:hidden}.bay .sl svg{width:100%;height:100%}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin-top:52px;position:relative}.steps:before{content:"";position:absolute;left:0;right:0;top:34px;height:2px;background:var(--ln)}
.st{position:relative;padding-right:30px}.st .nb{width:70px;height:70px;background:var(--bg);border:2px solid var(--or);display:grid;place-items:center;font:800 2rem 'Barlow Condensed',sans-serif;color:var(--or);position:relative}.st h4{font:800 1.7rem/1 'Barlow Condensed',sans-serif;text-transform:uppercase;margin:20px 0 8px}.st p{color:var(--mut);font-size:15.5px}
.mq{overflow:hidden;white-space:nowrap;border-bottom:1px solid var(--ln);padding:26px 0;background:var(--p)}.mq div{display:inline-block;animation:mqa 44s linear infinite}.mq span{font:700 2rem/1 'Barlow Condensed',sans-serif;text-transform:uppercase;color:#4a4f58;margin:0 34px;letter-spacing:.06em}.mq b{color:var(--or)}
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
.ok{display:none;border:1px solid #2fd06a;color:#2fd06a;padding:16px 18px;font-weight:600}.ok.on{display:block}
.faq details{border-bottom:1px solid var(--ln);padding:22px 0}.faq summary{cursor:pointer;font:700 1.6rem/1.1 'Barlow Condensed',sans-serif;text-transform:uppercase;list-style:none;display:flex;justify-content:space-between;gap:20px}.faq summary::-webkit-details-marker{display:none}.faq summary:after{content:"+";color:var(--or);font-size:1.8rem;line-height:1}.faq details[open] summary:after{content:"–"}.faq p{color:var(--mut);margin-top:12px;max-width:48em}
footer.ft{background:#000;padding:64px 0 36px}footer.ft .w{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:36px}footer.ft h4{font:700 1.1rem 'Barlow Condensed',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--or);margin-bottom:14px}footer.ft li{margin:8px 0;color:var(--mut);font-size:15px}.lg2{font:800 2.4rem/1 'Barlow Condensed',sans-serif;text-transform:uppercase}.legal{grid-column:1/-1;border-top:1px solid var(--ln);padding-top:24px;color:#6f7580;font-size:13px}
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
    team = [("Thomas Marchand", "Gérant · mécanicien depuis 22 ans", "#ff5a1f"), ("Inès Boudaoud", "Diagnostic électronique & hybrides", "#4fa3ff"), ("Karim Lopes", "Freinage, pneus et trains roulants", "#ffc61a")]
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
        + '<rect x="60" y="62" width="480" height="22" fill="#2f333a"/><path d="M60 62H540" stroke="#ff5a1f" stroke-width="3"/>'
        + '<g transform="translate(-60 190) scale(.78)">' + car_art("bay") + '</g>'
        + '<rect x="0" y="470" width="600" height="100" fill="#0a0b0d"/><path d="M0 470H600" stroke="#ff5a1f" stroke-width="2" stroke-dasharray="26 18"/>'))
    mapsvg = svg(600, 350, '<rect width="600" height="350" fill="#14171b"/><path d="M0 110H600M0 240H600M170 0V350M390 0V350" stroke="#232830" stroke-width="22"/><path d="M0 300Q300 250 600 300" stroke="#1a2a3a" stroke-width="34" fill="none"/><path d="M0 110H600M170 0V350" stroke="#ff5a1f" stroke-width="2" opacity=".5"/>'
                 '<path d="M270 160 q26-58 52 0 q0 32-26 58 q-26-26-26-58z" fill="#ff5a1f"/><circle cx="296" cy="158" r="10" fill="#0b0c0e"/>')
    faq = '''<details><summary>Faut-il prendre rendez-vous ?</summary><p>Pour les entretiens oui, c’est plus simple pour tout le monde. Pour une panne ou un voyant allumé, venez directement : on vous prend en charge dans la journée.</p></details>
<details><summary>Mon entretien annule-t-il la garantie constructeur ?</summary><p>Non. Depuis le règlement européen, vous pouvez entretenir votre véhicule dans le garage de votre choix sans perdre la garantie, à condition de suivre le carnet. Nous utilisons des pièces de qualité équivalente d’origine et tamponnons votre carnet.</p></details>
<details><summary>Prêtez-vous un véhicule ?</summary><p>Oui, une citadine de courtoisie est prêtée gratuitement pour les réparations de plus de deux heures, sur réservation.</p></details>
<details><summary>Le devis est-il gratuit et définitif ?</summary><p>Il est gratuit, écrit, détaillé pièce par pièce. Nous ne lançons aucun travail supplémentaire sans votre accord signé ou par message.</p></details>
<details><summary>Travaillez-vous sur les véhicules hybrides et électriques ?</summary><p>Oui. Inès est habilitée pour les véhicules hybrides et électriques (habilitation B2VL / BR). Diagnostic, freinage, climatisation et batterie 12 V.</p></details>'''
    body = '''
<div class="top"><div class="w"><span class="live" id="live"><i></i><span id="livet">Ouvert</span></span><span>12 rue de la Forge, 44000 Nantes · 02 40 00 00 00</span></div></div>
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
 if(o){L.classList.remove('off');T.textContent='Ouvert · ferme à '+f(o[1])}else{L.classList.add('off');T.textContent=nx?('Fermé · ouvre à '+f(nx[0])):'Fermé · réouverture demain'}
 var li=document.querySelector('#hr li[data-d="'+d+'"]');if(li)li.classList.add('today')}
live();
document.getElementById('dv').onsubmit=function(e){e.preventDefault();var p=+document.getElementById('sv').value*+document.getElementById('vh').value;
 document.getElementById('ev').textContent=Math.round(p/5)*5+' € TTC';document.getElementById('est').classList.add('on')};
var im=document.getElementById('im');im.oninput=function(){var v=im.value.toUpperCase().replace(/[^A-Z0-9]/g,'');var o=v.slice(0,2);if(v.length>2)o+='-'+v.slice(2,5);if(v.length>5)o+='-'+v.slice(5,7);im.value=o};
var sl=document.getElementById('sl');sl.onclick=function(e){if(e.target.tagName==='BUTTON'){Array.prototype.forEach.call(sl.children,function(b){b.classList.remove('on')});e.target.classList.add('on')}};
document.getElementById('rd').onsubmit=function(e){e.preventDefault();document.getElementById('ok').classList.add('on')};
var dt=document.getElementById('dt');if(dt){var t=new Date();t.setDate(t.getDate()+1);dt.min=t.toISOString().slice(0,10)}
})()</script>'''
    return page("Garage Marchand · Mécanique, pneus et entretien à Nantes", "Garage indépendant toutes marques à Nantes : entretien, freinage, pneus, climatisation. Devis écrit gratuit, garantie 12 mois.",
                "family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600;700", css, body, js)


# ============================================================ 3. OSTÉOPATHE
def zen(uid="z"):
    R = random.Random(7)
    s = ['<defs><linearGradient id="%sa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d4e4d7"/><stop offset="1" stop-color="#b6cfbd"/></linearGradient>'
         '<linearGradient id="%sb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f0d4bb"/><stop offset="1" stop-color="#dfae8e"/></linearGradient>'
         '<linearGradient id="%sc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f8a72"/><stop offset="1" stop-color="#245748"/></linearGradient>'
         '<radialGradient id="%ss" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#f4f1ea"/><stop offset="1" stop-color="#b8b2a4"/></radialGradient>'
         '<filter id="%sf"><feGaussianBlur stdDeviation="7"/></filter></defs>' % (uid, uid, uid, uid, uid)]
    s.append('<rect width="560" height="680" fill="#f4f6f1"/>')
    s.append('<path d="M30 640 V280 A130 130 0 0 1 290 280 V640Z" fill="url(#%sa)"/>' % uid)
    s.append('<path d="M250 640 V210 A145 145 0 0 1 540 210 V640Z" fill="url(#%sb)"/>' % uid)
    s.append('<circle cx="395" cy="250" r="58" fill="#fbf1e6" opacity=".92"/>')
    s.append('<path d="M120 640 V420 A62 62 0 0 1 244 420 V640Z" fill="url(#%sc)"/>' % uid)
    s.append('<path d="M0 640 H560 V680 H0Z" fill="#e9e3d6"/>')
    # branche
    pts = []
    for k in range(11):
        t = k / 10
        x = 520 - 330 * t; y = 120 + 90 * math.sin(t * 2.2) + 60 * t
        pts.append((x, y))
    s.append('<path d="M%.0f %.0f ' % pts[0] + " ".join("L%.0f %.0f" % p for p in pts[1:]) + '" stroke="#2c5a48" stroke-width="3" fill="none" stroke-linecap="round"/>')
    for i, (x, y) in enumerate(pts[1:], 1):
        for sd in (-1, 1):
            r = 17 - i * .8
            s.append('<ellipse cx="%.0f" cy="%.0f" rx="%.1f" ry="%.1f" fill="%s" transform="rotate(%d %.0f %.0f)" opacity=".95"/>' % (x + sd * 4, y + sd * 16, r * .86, r, R.choice(["#4f8f78", "#3f7c66", "#6aa88d"]), sd * 35, x, y))
    # galets empilés
    base = 640
    ell = [(86, 26, "#ece6d9"), (68, 22, "#d6cbb8"), (52, 19, "#e2d6c3"), (38, 16, "#c9bda9"), (26, 13, "#ece6d9")]
    s.append('<ellipse cx="418" cy="%d" rx="100" ry="10" fill="#000" opacity=".16" filter="url(#%sf)"/>' % (base, uid))
    y = base
    for rx, ry, col in ell:
        y -= ry * 1.55
        s.append('<ellipse cx="%d" cy="%.0f" rx="%d" ry="%d" fill="%s"/><ellipse cx="%d" cy="%.0f" rx="%d" ry="%d" fill="url(#%ss)" opacity=".5"/>' % (418 + R.randint(-3, 3), y, rx, ry, col, 418, y - ry * .3, rx * .8, ry * .6, uid))
    return "".join(s)


def osteo():
    page, slot, svg, ico = H["page"], H["slot"], H["svg"], H["ico"]
    css = r'''
:root{--bg:#f4f6f1;--ink:#142520;--mut:#5c6b64;--g:#2f6f5a;--g2:#e2ece5;--cl:#d6a98c;--sd:#ebe5da;--ln:#d9dfd6}
body{background:var(--bg);color:var(--ink);font:400 17px/1.7 'Figtree',system-ui,sans-serif}
.s2{font-family:'Instrument Serif',Georgia,serif;font-weight:400}
.w{max-width:1180px;margin:0 auto;padding:0 28px}
header.o{position:sticky;top:0;z-index:40;background:#f4f6f1ee;backdrop-filter:blur(10px)}header.o .w{display:flex;justify-content:space-between;align-items:center;height:80px}
.lg{display:flex;align-items:center;gap:12px;font:400 1.7rem/1 'Instrument Serif',serif}.lg i{width:30px;height:38px;border-radius:15px 15px 3px 3px;background:var(--g);display:block;position:relative}.lg i:after{content:"";position:absolute;left:8px;right:8px;top:9px;bottom:0;border-radius:8px 8px 0 0;background:var(--cl)}
.lg small{display:block;font:500 .66rem/1 'Figtree',sans-serif;letter-spacing:.22em;text-transform:uppercase;color:var(--mut);margin-top:5px}
nav.o{display:flex;gap:30px;font-weight:500;font-size:15.5px;color:var(--mut)}nav.o a:hover{color:var(--g)}
.b{display:inline-flex;align-items:center;gap:10px;background:var(--g);color:#fff;font:600 15.5px/1 'Figtree',sans-serif;padding:16px 26px;border-radius:99px;border:0;cursor:pointer;transition:.2s}.b:hover{background:var(--ink)}.b.o2{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1.5px var(--ink)}.b.o2:hover{background:var(--ink);color:#fff}
.hero .w{display:grid;grid-template-columns:1.05fr .95fr;gap:50px;align-items:center;padding-top:44px;padding-bottom:30px}
.ey{font:600 13px/1 'Figtree',sans-serif;letter-spacing:.18em;text-transform:uppercase;color:var(--g)}
h1.s2{font-size:clamp(3.2rem,6.6vw,6rem);line-height:.98;letter-spacing:-.02em;margin:22px 0 24px}h1.s2 em{color:var(--g)}
.lead{font-size:1.2rem;color:var(--mut);max-width:31em}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin:32px 0 36px}
.mini{display:flex;gap:30px;flex-wrap:wrap;font-size:14.5px;color:var(--mut)}.mini span{display:flex;gap:9px;align-items:center}.mini i{width:8px;height:8px;border-radius:50%;background:var(--g)}
.art{aspect-ratio:.82;border-radius:999px 999px 20px 20px;overflow:hidden;background:var(--g2)}.art .sl svg{width:100%;height:100%}
.facts{border-top:1px solid var(--ln);border-bottom:1px solid var(--ln);margin-top:40px}.facts .w{display:grid;grid-template-columns:repeat(3,1fr);padding-top:0;padding-bottom:0}
.facts div{padding:26px 24px;border-right:1px solid var(--ln)}.facts div:last-child{border:0}.facts b{display:block;font:400 2.1rem/1 'Instrument Serif',serif}.facts span{font-size:14.5px;color:var(--mut)}
section.s{padding:112px 0}
h2.s2{font-size:clamp(2.4rem,4.6vw,4rem);line-height:1.02;letter-spacing:-.02em;margin:16px 0 0}h2.s2 em{color:var(--g)}
.two{display:grid;grid-template-columns:.8fr 1.2fr;gap:80px;align-items:start}
.mot{border-top:1px solid var(--ink)}.mr{display:grid;grid-template-columns:56px 1fr auto;gap:20px;align-items:center;padding:26px 0;border-bottom:1px solid var(--ln);transition:.25s}.mr:hover{padding-left:12px;background:var(--g2)}
.mr i{display:grid;place-items:center;width:48px;height:48px;border-radius:50%;background:var(--g2);color:var(--g)}.mr h3{font:400 1.7rem/1.1 'Instrument Serif',serif}.mr p{color:var(--mut);font-size:15.5px;margin-top:2px}.mr em{font-style:normal;font-size:13px;color:var(--g);font-weight:600;letter-spacing:.1em;text-transform:uppercase}
.sess{background:var(--ink);color:#e7efe9;border-radius:40px;margin:0 20px}.sess .ey{color:#9fd2bd}.sess h2 em{color:#9fd2bd}
.tl{margin-top:50px;display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-top:1px solid #ffffff30}.tl div{padding:34px 30px 10px 0;position:relative}.tl div:before{content:"";position:absolute;left:0;top:-6px;width:11px;height:11px;border-radius:50%;background:#9fd2bd}
.tl b{font:400 1.2rem/1 'Instrument Serif',serif;color:#9fd2bd;letter-spacing:.04em}.tl h3{font:400 2.3rem/1.05 'Instrument Serif',serif;margin:10px 0}.tl p{color:#b7c8bf;font-size:16px;max-width:22em}
.tar{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:44px}.tc{background:#fff;border-radius:28px;padding:36px;display:grid;gap:4px}.tc.f{background:var(--g);color:#fff}
.tc li{display:flex;justify-content:space-between;align-items:baseline;padding:15px 0;border-bottom:1px solid #00000014;font-size:17px}.tc.f li{border-color:#ffffff30}.tc li:last-child{border:0}.tc li b{font:400 2rem/1 'Instrument Serif',serif}
.tc h3{font:400 1.9rem/1 'Instrument Serif',serif;margin-bottom:8px}.tc p{font-size:15px;opacity:.8;margin-top:12px}
.pr{display:grid;grid-template-columns:.85fr 1.15fr;gap:80px;align-items:center}.pr .pt{aspect-ratio:.88;border-radius:999px 999px 20px 20px;overflow:hidden;background:var(--sd)}.pr .pt .sl svg{width:100%;height:100%}
.pr p{color:#40514a;margin-top:18px}.dip{margin-top:28px;display:grid;gap:12px}.dip div{display:flex;gap:14px;align-items:baseline;border-top:1px solid var(--ln);padding-top:12px}.dip b{min-width:64px;font:400 1.3rem 'Instrument Serif',serif;color:var(--g)}
.bk{background:#fff;border-radius:36px;box-shadow:0 40px 90px -50px #14252066;display:grid;grid-template-columns:1.2fr .8fr;overflow:hidden;margin-top:44px}
.bk>div{min-width:0}.bk .l{padding:40px}.bk .r{background:var(--g2);padding:40px;display:flex;flex-direction:column;gap:16px}
.days{display:flex;gap:10px;overflow-x:auto;padding-bottom:6px;scrollbar-width:none}.days::-webkit-scrollbar{display:none}
.dy{flex:0 0 auto;min-width:74px;border:1.5px solid var(--ln);background:#fff;border-radius:18px;padding:12px 8px;text-align:center;cursor:pointer;transition:.2s;font:500 13px/1.2 'Figtree',sans-serif;color:var(--mut)}.dy b{display:block;font:400 1.9rem/1 'Instrument Serif',serif;color:var(--ink);margin-top:4px}.dy:hover{border-color:var(--g)}.dy.on{background:var(--ink);border-color:var(--ink);color:#c7d6cf}.dy.on b{color:#fff}.dy.full{opacity:.4;pointer-events:none}
.slots{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:22px}.sl2{border:1.5px solid var(--ln);background:#fff;border-radius:14px;padding:14px 0;text-align:center;font:600 15.5px 'Figtree',sans-serif;cursor:pointer;transition:.2s}.sl2:hover{border-color:var(--g);color:var(--g)}.sl2.on{background:var(--g);border-color:var(--g);color:#fff}.sl2.x{opacity:.35;text-decoration:line-through;pointer-events:none}
.lab{font:600 12px 'Figtree',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--mut);margin-bottom:12px}
.bk form{display:grid;gap:12px}.bk label{display:grid;gap:6px;font-weight:600;font-size:14px}.bk input,.bk select{font:400 16px 'Figtree',sans-serif;padding:14px 15px;border-radius:12px;border:1.5px solid #cdd8d0;background:#fff;color:var(--ink)}.bk input:focus,.bk select:focus{outline:0;border-color:var(--g);box-shadow:0 0 0 4px #2f6f5a22}
.rec{background:#fff;border-radius:18px;padding:18px 20px;font-size:15.5px;min-height:92px}.rec b{font:400 1.5rem/1.1 'Instrument Serif',serif;display:block;margin-bottom:4px}
.done{display:none;background:var(--g);color:#fff;border-radius:18px;padding:22px}.done.on{display:block}.done b{font:400 1.7rem/1.1 'Instrument Serif',serif;display:block;margin-bottom:6px}
.qt{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin-top:48px;border-top:1px solid var(--ink)}.qt blockquote{margin:0;padding:34px 34px 10px 0}.qt p{font:400 1.55rem/1.3 'Instrument Serif',serif}.qt small{display:block;margin-top:16px;color:var(--mut);font-size:14px}
.sc{display:flex;align-items:baseline;gap:14px;margin-top:20px}.sc b{font:400 4.5rem/1 'Instrument Serif',serif;color:var(--g)}.sc span{color:var(--mut)}
.faq{margin-top:34px;border-top:1px solid var(--ink)}.faq details{border-bottom:1px solid var(--ln);padding:24px 0}.faq summary{cursor:pointer;font:400 1.7rem/1.15 'Instrument Serif',serif;list-style:none;display:flex;justify-content:space-between;gap:20px}.faq summary::-webkit-details-marker{display:none}.faq summary:after{content:"+";color:var(--g);font-size:1.8rem;line-height:1;transition:.2s}.faq details[open] summary:after{transform:rotate(45deg)}.faq p{color:var(--mut);margin-top:12px;max-width:46em}
.ac{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:44px}.bx{background:#fff;border-radius:28px;padding:36px}
.hr li{display:flex;justify-content:space-between;padding:13px 0;border-bottom:1px solid var(--ln)}.hr li:last-child{border:0}.hr li.today{color:var(--g);font-weight:700}
.map{border-radius:18px;overflow:hidden;aspect-ratio:1.7;background:#dfe7dc;margin-bottom:18px}.map svg{width:100%;height:100%;display:block}
.ul{display:grid;gap:12px;margin-top:6px}.ul div{display:flex;gap:12px;align-items:flex-start;font-size:15.5px;color:#40514a}.ul i{flex:0 0 22px;color:var(--g)}
footer.ft{background:var(--ink);color:#b9c9c1;padding:70px 0 38px;margin-top:100px}footer.ft .w{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:36px}footer.ft h4{font:600 12px 'Figtree';letter-spacing:.18em;text-transform:uppercase;color:#9fd2bd;margin-bottom:14px}footer.ft li{margin:8px 0;font-size:15px}.big{font:400 2.3rem/1 'Instrument Serif',serif;color:#fff}.legal{grid-column:1/-1;border-top:1px solid #ffffff22;padding-top:24px;font-size:13px;color:#8fa198}
@media(max-width:980px){.hero .w,.two,.pr,.bk,.ac,.tar{grid-template-columns:1fr}.facts .w,.tl,.qt{grid-template-columns:1fr}.facts div{border-right:0;border-bottom:1px solid var(--ln)}nav.o{display:none}.sess{margin:0 10px;border-radius:28px}.slots{grid-template-columns:repeat(3,1fr)}section.s{padding:72px 0}.art{max-width:480px}footer.ft .w{grid-template-columns:1fr 1fr}.tl div{padding-bottom:26px}.bk .l,.bk .r{padding:26px}}
'''
    mot = [("Dos &amp; lombaires", "Lumbagos, sciatiques, tensions du bureau ou du port de charges.", "leaf", "Le plus fréquent"),
           ("Nuque &amp; cervicales", "Raideurs, maux de tête de tension, vertiges d’origine cervicale.", "hands", ""),
           ("Sport &amp; tendinites", "Reprise, douleurs d’épaule ou de genou, préparation avant compétition.", "timer", ""),
           ("Bébés &amp; enfants", "Reflux, coliques, plagiocéphalie, troubles du sommeil. Soin très doux.", "shield", "Dès 15 jours"),
           ("Grossesse &amp; post-partum", "Douleurs du bassin, du dos ; récupération après l’accouchement.", "drop", ""),
           ("Stress &amp; sommeil", "Tensions du diaphragme, respiration courte, fatigue nerveuse.", "alarm", "")]
    rows = "".join('<div class="mr"><i>%s</i><span><h3>%s</h3><p>%s</p></span><em>%s</em></div>' % (ico(ic, 22, "currentColor", 1.7), t, d, tg) for t, d, ic, tg in mot)
    hero = slot("osteo-hero", svg(560, 680, zen()))
    pt = slot("osteo-portrait", svg(500, 570, '<defs><linearGradient id="pq" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#efe4d3"/><stop offset="1" stop-color="#d8c4a6"/></linearGradient></defs><rect width="500" height="570" fill="url(#pq)"/>'
        '<path d="M60 570 V300 A190 190 0 0 1 440 300 V570Z" fill="#fbf7ef" opacity=".7"/><path d="M130 570 Q250 330 370 570Z" fill="#2f6f5a"/><circle cx="250" cy="236" r="70" fill="#e1b896"/>'
        '<path d="M178 226 Q190 150 262 156 Q326 164 322 236 Q312 190 250 184 Q200 184 178 226Z" fill="#3b2a1f"/><path d="M210 296 L250 360 L290 296" fill="#e1b896"/><path d="M226 330 L250 378 L274 330 L250 342Z" fill="#fbf7ef"/>'
        '<path d="M60 560 H440" stroke="#bfa985" stroke-width="3"/>'))
    mapsvg = svg(600, 350, '<rect width="600" height="350" fill="#dfe7dc"/><path d="M0 100H600M0 230H600M140 0V350M330 0V350M480 0V350" stroke="#fff" stroke-width="18"/><path d="M0 320Q300 270 600 320" stroke="#b9d3d9" stroke-width="38" fill="none"/><path d="M0 100H600" stroke="#2f6f5a" stroke-width="3" stroke-dasharray="10 8"/>'
                 '<path d="M232 150 q26-58 52 0 q0 32-26 58 q-26-26-26-58z" fill="#2f6f5a"/><circle cx="258" cy="148" r="10" fill="#fff"/>')
    faq = '''<details><summary>Combien de séances faut-il prévoir ?</summary><p>Une à trois séances suffisent le plus souvent. Si le problème est ancien, nous convenons ensemble d’un rythme, jamais d’un forfait imposé.</p></details>
<details><summary>La séance est-elle remboursée ?</summary><p>La Sécurité sociale ne rembourse pas l’ostéopathie, mais la plupart des mutuelles proposent un forfait (souvent 3 à 5 séances par an). Une facture détaillée vous est remise à chaque séance.</p></details>
<details><summary>Faut-il une ordonnance ou apporter des examens ?</summary><p>Non, mais apportez vos radios, IRM et comptes rendus récents s’ils existent. Ils m’aident à adapter le soin.</p></details>
<details><summary>Est-ce douloureux ?</summary><p>Non. Les techniques sont douces et adaptées à votre état. Vous pouvez m’arrêter à tout moment.</p></details>
<details><summary>Recevez-vous les bébés et les femmes enceintes ?</summary><p>Oui, dès les premières semaines de vie et pendant toute la grossesse, avec des techniques spécifiques et une table adaptée.</p></details>'''
    body = '''
<header class="o"><div class="w"><a class="lg" href="#top"><i></i><span>Cabinet Lemaire<small>Ostéopathie · Bordeaux</small></span></a>
<nav class="o"><a href="#motifs">Motifs</a><a href="#seance">La séance</a><a href="#tarifs">Tarifs</a><a href="#praticienne">Praticienne</a><a href="#infos">Accès</a></nav><a class="b" href="#rdv">Prendre rendez-vous</a></div></header>
<main id="top"><section class="hero"><div class="w"><div><span class="ey">Ostéopathe D.O. · Bordeaux Chartrons</span>
<h1 class="s2">Retrouvez le plaisir de <em>bouger.</em></h1>
<p class="lead">Un cabinet calme, une séance d’une heure sans précipitation, et un soin doux pour comprendre l’origine de votre douleur, pas seulement la calmer.</p>
<div class="cta"><a class="b" href="#rdv">Réserver un créneau @@ARR@@</a><a class="b o2" href="#motifs">Pourquoi consulter</a></div>
<div class="mini"><span><i></i>Premier rendez-vous sous 48 h</span><span><i></i>Cabinet accessible PMR</span><span><i></i>Feuille de soins pour la mutuelle</span></div></div>
<div class="art">@@HERO@@</div></div>
<div class="facts"><div class="w"><div><b>1 h</b><span>de consultation, sans chronomètre</span></div><div><b>4,9 / 5</b><span>87 avis Google</span></div><div><b>12 ans</b><span>de pratique à Bordeaux</span></div></div></div></section>

<section class="s" id="motifs"><div class="w two"><div><span class="ey">Pourquoi consulter</span><h2 class="s2">Ce que je <em>soigne,</em> et ce que je ne soigne pas.</h2>
<p style="color:var(--mut);margin-top:22px;max-width:23em">L’ostéopathie soulage des troubles fonctionnels. Je ne remplace pas votre médecin : en cas de signe d’alerte (fièvre, perte de force, douleur thoracique), je vous oriente aussitôt.</p></div>
<div class="mot">@@ROWS@@</div></div></section>

<section class="s sess" id="seance"><div class="w"><span class="ey">Votre première séance</span><h2 class="s2">Une heure, <em>trois temps.</em></h2>
<div class="tl"><div><b>15 min</b><h3>L’échange</h3><p>Vous me racontez votre douleur, votre histoire, votre quotidien. Je vous écoute avant de toucher.</p></div>
<div><b>10 min</b><h3>L’examen</h3><p>Tests de mobilité, observation de la posture et palpation pour comprendre ce qui se bloque.</p></div>
<div><b>35 min</b><h3>Le soin</h3><p>Techniques douces et adaptées. Je vous explique ce que je fais et vous donne des gestes simples pour la maison.</p></div></div></div></section>

<section class="s" id="tarifs"><div class="w"><span class="ey">Tarifs</span><h2 class="s2">Des prix clairs, <em>affichés d’avance.</em></h2>
<div class="tar"><div class="tc f"><h3>Consultations</h3><ul><li>Adulte<b>60 €</b></li><li>Enfant de 2 à 12 ans<b>45 €</b></li><li>Nourrisson (moins de 2 ans)<b>50 €</b></li><li>Femme enceinte<b>55 €</b></li></ul></div>
<div class="tc"><h3>Bon à savoir</h3><ul><li>Moyens de paiement<span>CB · espèces · chèque</span></li><li>Mutuelle<span>Facture fournie</span></li><li>Annulation<span>Gratuite jusqu’à 24 h avant</span></li></ul><p>Un rendez-vous manqué sans prévenir est facturé 30 €. Ce n’est pas un piège : un créneau libre est précieux pour un autre patient.</p></div></div></div></section>

<section class="s" id="praticienne" style="padding-top:20px"><div class="w pr"><div class="pt">@@PT@@</div>
<div><span class="ey">Votre praticienne</span><h2 class="s2">Léa Lemaire, <em>ostéopathe D.O.</em></h2>
<p>Diplômée en 2014 après cinq ans d’études, j’ai exercé dans un club de handball avant d’ouvrir mon cabinet aux Chartrons. J’aime les consultations longues, les questions simples et les explications claires.</p>
<p>Je me forme chaque année : pédiatrie, périnatalité, douleur chronique. Et je préfère vous revoir une fois de moins que de vous fidéliser à tout prix.</p>
<div class="dip"><div><b>2014</b><span>Diplôme d’ostéopathe D.O., Bordeaux</span></div><div><b>2017</b><span>Formation en ostéopathie pédiatrique</span></div><div><b>2021</b><span>Périnatalité et suivi post-partum</span></div></div></div></div></section>

<section class="s" id="rdv" style="padding-top:20px"><div class="w"><span class="ey">Rendez-vous en ligne</span><h2 class="s2">Choisissez <em>votre créneau.</em></h2>
<div class="bk"><div class="l"><div class="lab">1 · Jour</div><div class="days" id="days"></div><div class="lab" style="margin-top:26px" id="slab">2 · Heure</div><div class="slots" id="slots"></div></div>
<div class="r"><div class="lab">3 · Vos coordonnées</div><div class="rec" id="rec"><b>Aucun créneau choisi</b>Sélectionnez un jour puis une heure.</div>
<form id="bf"><label>Nom et prénom<input required placeholder="Marie Durand"></label><label>Téléphone<input required placeholder="06 00 00 00 00" inputmode="tel"></label><label>Motif<select><option>Dos / lombaires</option><option>Nuque / cervicales</option><option>Sport</option><option>Bébé / enfant</option><option>Grossesse</option><option>Autre</option></select></label>
<button class="b" type="submit" id="bgo" disabled style="justify-content:center;opacity:.5">Confirmer</button></form><div class="done" id="done"><b>C’est noté.</b><span id="dt"></span></div></div></div></div></section>

<section class="s" style="padding-top:20px"><div class="w"><span class="ey">Avis patients</span><div class="sc"><b>4,9</b><span>sur 5 · 87 avis Google</span></div>
<div class="qt"><blockquote><p>« Enfin une consultation où l’on prend le temps. Mon mal de dos chronique s’est apaisé dès la deuxième séance. »</p><small>Claire B. · Chartrons</small></blockquote>
<blockquote><p>« Très douce avec mon bébé de trois semaines. Léa explique tout avec calme, et c’était efficace. »</p><small>Julien M. · papa d’Éloïse</small></blockquote>
<blockquote><p>« Je cours le marathon : elle a trouvé l’origine de ma douleur au genou en vingt minutes. »</p><small>Thomas R. · coureur</small></blockquote></div></div></section>

<section class="s" id="infos" style="padding-top:20px"><div class="w"><span class="ey">Accès &amp; horaires</span><h2 class="s2">Venir au <em>cabinet.</em></h2>
<div class="ac"><div class="bx"><ul class="hr" id="hr"><li data-d="1"><span>Lundi</span><b>9 h – 12 h · 14 h – 19 h</b></li><li data-d="2"><span>Mardi</span><b>9 h – 12 h · 14 h – 19 h</b></li><li data-d="3"><span>Mercredi</span><b>9 h – 12 h · 14 h – 18 h</b></li><li data-d="4"><span>Jeudi</span><b>9 h – 12 h · 14 h – 19 h</b></li><li data-d="5"><span>Vendredi</span><b>9 h – 12 h · 14 h – 17 h</b></li><li data-d="6"><span>Samedi</span><b>9 h – 13 h</b></li><li data-d="0"><span>Dimanche</span><b>Fermé</b></li></ul></div>
<div class="bx"><div class="map">@@MAP@@</div><p><b>Cabinet Lemaire</b><br>27 cours Saint-Louis, 33300 Bordeaux · 05 56 00 00 00</p>
<div class="ul"><div><i>@@PIN@@</i><span>Tram C, arrêt Chartrons (3 min à pied) · Parking Saint-Louis à 100 m</span></div><div><i>@@CK@@</i><span>Cabinet de plain-pied, accessible aux personnes à mobilité réduite</span></div></div></div></div>
<div class="faq"><h2 class="s2" style="font-size:2.4rem;margin:40px 0 0">Questions <em>fréquentes</em></h2>@@FAQ@@</div></div></section></main>
<footer class="ft"><div class="w"><div><div class="big">Cabinet Lemaire</div><p style="margin-top:14px;max-width:24em">Ostéopathie pour adultes, enfants et nourrissons, à Bordeaux Chartrons.</p></div>
<div><h4>Cabinet</h4><ul><li>Motifs de consultation</li><li>La séance</li><li>Tarifs</li></ul></div><div><h4>Contact</h4><ul><li>05 56 00 00 00</li><li>cabinet@lemaire-osteo.fr</li><li>27 cours Saint-Louis</li></ul></div><div><h4>Infos</h4><ul><li>Mentions légales</li><li>Confidentialité</li><li>Données de santé</li></ul></div>
<div class="legal">© 2026 Cabinet Lemaire · Ostéopathe D.O., n° ADELI 33 00 00000 (exemple) · SIRET 000 000 000 00000 (exemple) · Hébergeur : Cloudflare, Inc.</div></div></footer>
'''
    body = (body.replace("@@ARR@@", ico("arrow", 18)).replace("@@HERO@@", hero).replace("@@ROWS@@", rows).replace("@@PT@@", pt).replace("@@MAP@@", mapsvg).replace("@@FAQ@@", faq)
            .replace("@@PIN@@", ico("pin", 20, "currentColor", 1.7)).replace("@@CK@@", ico("check", 20, "currentColor", 1.9)))
    js = r'''<script>(function(){
var D=document,days=D.getElementById('days'),slots=D.getElementById('slots'),rec=D.getElementById('rec'),go=D.getElementById('bgo'),sel={d:null,t:null};
var M={1:[9,10,11,14,15,16,17,18],2:[9,10,11,14,15,16,17,18],3:[9,10,11,14,15,16,17],4:[9,10,11,14,15,16,17,18],5:[9,10,11,14,15,16],6:[9,10,11,12],0:[]};
function hash(s){var h=0;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return Math.abs(h)}
function fmt(d){return d.toLocaleDateString('fr-FR',{weekday:'long',day:'numeric',month:'long'})}
var out=[],n=new Date();n.setHours(12);for(var i=1;out.length<8&&i<30;i++){var d=new Date(n);d.setDate(n.getDate()+i);if(d.getDay()!==0)out.push(d)}
function avail(d){var key=d.toISOString().slice(0,10);return (M[d.getDay()]||[]).filter(function(h,i){return hash(key+h)%100<62})}
out.forEach(function(d,i){var b=D.createElement('button');b.type='button';b.className='dy'+(avail(d).length?'':' full');b.innerHTML=d.toLocaleDateString('fr-FR',{weekday:'short'}).replace('.','')+'<b>'+d.getDate()+'</b>'+d.toLocaleDateString('fr-FR',{month:'short'}).replace('.','');
 b.onclick=function(){sel.d=d;sel.t=null;Array.prototype.forEach.call(days.children,function(x){x.classList.remove('on')});b.classList.add('on');draw();upd()};days.appendChild(b)});
function draw(){slots.innerHTML='';var a=avail(sel.d);(M[sel.d.getDay()]||[]).forEach(function(h){var b=D.createElement('button');b.type='button';var ok=a.indexOf(h)>-1;b.className='sl2'+(ok?'':' x');b.textContent=h+' h 00';
 b.onclick=function(){sel.t=h;Array.prototype.forEach.call(slots.children,function(x){x.classList.remove('on')});b.classList.add('on');upd()};slots.appendChild(b)})}
function upd(){if(sel.d&&sel.t){rec.innerHTML='<b>'+fmt(sel.d)+'</b>à '+sel.t+' h 00 · consultation d’une heure';go.disabled=false;go.style.opacity=1}else{rec.innerHTML='<b>'+(sel.d?fmt(sel.d):'Aucun créneau choisi')+'</b>'+(sel.d?'Choisissez maintenant une heure.':'Sélectionnez un jour puis une heure.');go.disabled=true;go.style.opacity=.5}}
for(var k=0;k<days.children.length;k++){if(days.children[k].className.indexOf('full')<0){days.children[k].click();break}}
D.getElementById('bf').onsubmit=function(e){e.preventDefault();if(!sel.t)return;D.getElementById('bf').style.display='none';var x=D.getElementById('done');x.classList.add('on');D.getElementById('dt').textContent=fmt(sel.d)+' à '+sel.t+' h 00. Un SMS de confirmation vous est envoyé, avec un rappel la veille.'};
var li=D.querySelector('#hr li[data-d="'+new Date().getDay()+'"]');if(li)li.classList.add('today');
})()</script>'''
    return page("Cabinet Lemaire · Ostéopathe à Bordeaux Chartrons", "Ostéopathe D.O. à Bordeaux Chartrons : adultes, enfants, nourrissons, femmes enceintes. Rendez-vous en ligne.",
                "family=Instrument+Serif:ital@0;1&family=Figtree:wght@400;500;600;700", css, body, js)
