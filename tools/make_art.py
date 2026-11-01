# -*- coding: utf-8 -*-
"""Génère la scène « terrasse de bistrot la nuit » (SVG vectoriel) utilisée dans les maquettes de l'accueil.
Usage : python3 tools/make_art.py  (réécrit le bloc <g id="art"> de tools/src/home-v3.html)"""
import random, re, os, math
R = random.Random(7)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "tools", "src", "home-v3.html")

defs = """
    <linearGradient id="a-night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#04100e"/><stop offset=".6" stop-color="#0a1812"/><stop offset="1" stop-color="#050403"/></linearGradient>
    <linearGradient id="a-glow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2c4"/><stop offset=".3" stop-color="#ffc25e"/><stop offset=".75" stop-color="#c8701f"/><stop offset="1" stop-color="#6a300c"/></linearGradient>
    <linearGradient id="a-floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b130b"/><stop offset="1" stop-color="#050403"/></linearGradient>
    <linearGradient id="a-lit" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#eef27a"/><stop offset=".4" stop-color="#8fc83f"/><stop offset="1" stop-color="#2f8030"/></linearGradient>
    <linearGradient id="a-mid" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6fb23c"/><stop offset="1" stop-color="#1c5220"/></linearGradient>
    <linearGradient id="a-dark" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#25461d"/><stop offset="1" stop-color="#08140a"/></linearGradient>
    <linearGradient id="a-left" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#020807" stop-opacity=".62"/><stop offset=".5" stop-color="#020807" stop-opacity=".3"/><stop offset="1" stop-color="#020807" stop-opacity="0"/></linearGradient>
    <radialGradient id="a-vig" cx=".55" cy=".48" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".62"/></radialGradient>
    <radialGradient id="a-bk"><stop offset="0" stop-color="#fff3cf" stop-opacity=".95"/><stop offset=".45" stop-color="#ffc766" stop-opacity=".6"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
    <radialGradient id="a-spill" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffb552" stop-opacity=".55"/><stop offset="1" stop-color="#ffb552" stop-opacity="0"/></radialGradient>
    <filter id="a-b1" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="2.2"/></filter>
    <filter id="a-b2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>
    <g id="a-leaf"><path d="M0 0C18-17 60-19 94 0C60 19 18 17 0 0Z"/><path d="M2 0H88" stroke="#000" stroke-opacity=".28" stroke-width="1.4" fill="none"/></g>
"""

def leaves(cx, cy, n, spread, smin, smax, ang, fills, wts=None):
    out = []
    for _ in range(n):
        x = cx + R.gauss(0, spread); y = cy + R.gauss(0, spread * .8)
        a = ang + R.uniform(-70, 70); s = R.uniform(smin, smax)
        f = R.choices(fills, wts or [1] * len(fills))[0]
        out.append('<use href="#a-leaf" transform="translate(%.0f %.0f) rotate(%.0f) scale(%.2f)" fill="url(#%s)"/>' % (x, y, a, s, f))
    return "".join(out)

def panes():
    s = []
    x0, x1, yt, yb = 318, 1000, 70, 470
    pw = (x1 - x0) / 6
    # intérieur éclairé
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="url(#a-glow)"/>' % (x0, yt, x1 - x0, yb - yt))
    # lueurs intérieures : suspensions, étagères
    for i in range(6):
        cx = x0 + pw * i + pw / 2
        s.append('<circle cx="%.0f" cy="%d" r="46" fill="url(#a-bk)" opacity=".85"/>' % (cx + R.uniform(-8, 8), 150 + R.randint(-12, 12)))
        s.append('<path d="M%.0f 100V%d" stroke="#2a1608" stroke-width="2"/><path d="M%.0f %d a16 12 0 0 1 32 0z" fill="#2a1608"/>' % (cx, 140, cx - 16, 150))
    for y in (232, 300):
        s.append('<rect x="%d" y="%d" width="%d" height="5" fill="#2b1708" opacity=".75"/>' % (x0, y, x1 - x0))
        bx = x0 + 6
        while bx < x1 - 10:
            h = R.randint(18, 40); w = R.randint(7, 12)
            s.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="#2b1708" opacity=".7"/>' % (bx, y - h, w, h))
            bx += w + R.randint(4, 16)
    # silhouettes de tables et chaises à l'intérieur
    for cx in (x0 + 120, x0 + 330, x0 + 560):
        s.append('<ellipse cx="%d" cy="428" rx="62" ry="10" fill="#1d0f05" opacity=".9"/><rect x="%d" y="428" width="6" height="42" fill="#1d0f05"/>' % (cx, cx - 3))
        s.append('<rect x="%d" y="380" width="30" height="48" rx="6" fill="#1d0f05" opacity=".8"/>' % (cx - 90))
    # reflets sur les vitres
    s.append('<path d="M330 70L470 70L330 330Z" fill="#fff" opacity=".07"/><path d="M640 70L760 70L560 470L500 470Z" fill="#fff" opacity=".05"/><path d="M900 70L1000 70V260Z" fill="#fff" opacity=".06"/>')
    # menuiseries noires
    fr = []
    for i in range(7):
        x = x0 + pw * i
        fr.append('<rect x="%.1f" y="%d" width="9" height="%d"/>' % (x - 4.5, yt - 8, yb - yt + 16))
    fr.append('<rect x="%d" y="%d" width="%d" height="9"/><rect x="%d" y="%d" width="%d" height="9"/><rect x="%d" y="%d" width="%d" height="12"/><rect x="%d" y="%d" width="%d" height="10"/>'
              % (x0 - 6, yt - 8, x1 - x0 + 12, x0 - 6, 140, x1 - x0 + 12, x0 - 6, yb - 4, x1 - x0 + 12, x0 - 6, 330, x1 - x0 + 12))
    s.append('<g fill="#060908">%s</g>' % "".join(fr))
    return "".join(s)

def strings():
    s = []
    for (xa, ya, xb, yb_, sag) in ((300, 52, 1010, 70, 34), (330, 128, 1010, 134, 20)):
        mx = (xa + xb) / 2
        s.append('<path d="M%d %d Q%d %d %d %d" fill="none" stroke="#0b0b0b" stroke-width="2"/>' % (xa, ya, mx, ya + sag * 2, xb, yb_))
        for i in range(1, 15):
            t = i / 15.0
            x = (1 - t) ** 2 * xa + 2 * (1 - t) * t * mx + t * t * xb
            y = (1 - t) ** 2 * ya + 2 * (1 - t) * t * (ya + sag * 2) + t * t * yb_
            s.append('<circle cx="%.0f" cy="%.0f" r="34" fill="url(#a-bk)" opacity=".85"/><circle cx="%.0f" cy="%.0f" r="4.6" fill="#fff3cf"/>' % (x, y + 4, x, y + 4))
    return "".join(s)

def chair(x, y, sc, flip=1):
    return ('<g transform="translate(%d %d) scale(%.2f %.2f)" fill="none" stroke="#070504" stroke-width="5" stroke-linecap="round">'
            '<path d="M-26 0H26M-24 0L-30 74M24 0L30 74M-22 28L-28 74M22 28L28 74"/><path d="M-24 -4C-26 -50 -16 -76 0 -80C16 -76 26 -50 24 -4" stroke-width="5"/><path d="M-14 -52H14" stroke-width="4"/>'
            '</g><g transform="translate(%d %d) scale(%.2f %.2f)" fill="none" stroke="#ffb552" stroke-opacity=".38" stroke-width="1.6"><path d="M-24 -4C-26 -50 -16 -76 0 -80"/></g>') % (x, y, sc * flip, sc, x, y, sc * flip, sc)

def table(x, y, sc):
    return ('<g transform="translate(%d %d) scale(%.2f)">'
            '<ellipse cx="0" cy="26" rx="130" ry="22" fill="url(#a-spill)" opacity=".8"/>'
            '<path d="M-5 14H5L7 118H-7z" fill="#060403"/><ellipse cx="0" cy="124" rx="40" ry="7" fill="#060403"/>'
            '<ellipse cx="0" cy="8" rx="96" ry="19" fill="#0e0905"/><ellipse cx="0" cy="4" rx="96" ry="18" fill="#2a1a0c"/><ellipse cx="0" cy="2" rx="90" ry="14" fill="#3a2511"/>'
            '<ellipse cx="0" cy="3" rx="94" ry="17" fill="none" stroke="#ffcf85" stroke-opacity=".5" stroke-width="1.4"/>'
            '<circle cx="0" cy="-6" r="34" fill="url(#a-bk)"/><rect x="-6" y="-16" width="12" height="16" rx="2" fill="#e9d9b8"/><path d="M0-26c4 6 4 10 0 14c-4-4-4-8 0-14z" fill="#fff0b8"/>'
            '<path d="M-52 2l-5-30h12l-5 30z" fill="#bcd6d0" opacity=".55"/><path d="M40 2l-4-26h11l-4 26z" fill="#bcd6d0" opacity=".5"/></g>') % (x, y, sc)

art = []
art.append('<rect width="1000" height="625" fill="url(#a-night)"/>')
# feuillage lointain, flou
art.append('<g filter="url(#a-b2)" opacity=".9">%s</g>' % leaves(120, 300, 14, 90, 1.2, 2.0, -20, ["a-dark", "a-mid"]))
# façade
art.append('<rect x="0" y="40" width="1000" height="440" fill="#0b110f"/>')
art.append(panes())
art.append('<rect x="0" y="40" width="1000" height="26" fill="#050807"/>')
# lueur sur le sol
art.append('<rect y="470" width="1000" height="155" fill="url(#a-floor)"/>')
art.append('<ellipse cx="660" cy="500" rx="420" ry="46" fill="url(#a-spill)"/>')
art.append('<g opacity=".35" fill="#ffc66b">%s</g>' % "".join('<rect x="%d" y="%d" width="%d" height="2"/>' % (R.randint(300, 900), R.randint(486, 600), R.randint(30, 160)) for _ in range(14)))
art.append(strings())
# tables et chaises, du fond vers le premier plan
art.append(table(520, 508, .68)); art.append(chair(408, 520, .8, 1)); art.append(chair(626, 520, .8, -1))
art.append(table(850, 530, .82)); art.append(chair(716, 548, .95, 1)); art.append(chair(986, 548, .95, -1))
art.append(table(690, 580, 1.0))
# bokeh
bk = []
for _ in range(60):
    x = R.uniform(0, 1000); y = R.uniform(10, 470); r = R.choice([7, 9, 12, 16, 22, 30])
    bk.append('<circle cx="%.0f" cy="%.0f" r="%d" fill="url(#a-bk)" opacity="%.2f"/>' % (x, y, r, R.uniform(.25, .75)))
art.append('<g filter="url(#a-b1)">%s</g>' % "".join(bk))
# feuillage premier plan : haut gauche, haut droit, bas gauche
fills = ["a-lit", "a-mid", "a-lit", "a-dark", "a-lit"]
art.append(leaves(60, 20, 34, 70, 1.3, 2.6, 40, fills, [2, 3, 2, 2, 2]))
art.append(leaves(230, 0, 16, 60, 1.2, 2.2, 78, fills, [2, 2, 2, 1, 2]))
art.append(leaves(960, 10, 18, 60, 1.1, 2.1, 140, fills, [2, 2, 2, 1, 2]))
art.append(leaves(10, 200, 12, 40, 1.2, 2.0, -10, fills, [1, 3, 1, 3, 1]))
art.append('<g filter="url(#a-b1)">%s</g>' % leaves(30, 610, 12, 60, 1.6, 2.6, -50, ["a-dark", "a-mid"]))
art.append('<g filter="url(#a-b1)">%s</g>' % leaves(985, 600, 8, 40, 1.6, 2.4, -130, ["a-dark", "a-mid"]))
art.append('<rect width="1000" height="625" fill="url(#a-left)"/><rect width="1000" height="625" fill="url(#a-vig)"/>')

block = '<g id="art">' + defs.replace("\n    ", "\n      ") + "".join(art) + "</g>"
s = open(P, encoding="utf-8").read()
new, n = re.subn(r'<g id="art">.*?</g>\n  </defs>', lambda m: block + "\n  </defs>", s, count=1, flags=re.S)
assert n == 1, "bloc art introuvable"
open(P, "w", encoding="utf-8").write(new)
print("art ok", len(block) // 1024, "ko")
