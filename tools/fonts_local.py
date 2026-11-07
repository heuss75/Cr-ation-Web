# -*- coding: utf-8 -*-
"""Polices hébergées sur notre propre site (plus aucun appel à Google Fonts : pas de transfert d'adresse IP).

- `python3 tools/fonts_local.py <dossier google/fonts>` : (re)génère site/assets/fonts/*.woff et fonts.css
  à partir des fichiers d'origine (licence SIL Open Font License, copiée avec les polices).
- `rewrite(dossier)` : remplace dans les pages les liens vers fonts.googleapis.com par /assets/fonts/fonts.css.
"""
import os, re, sys, glob, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "site", "assets", "fonts")
CSS_URL = "/assets/fonts/fonts.css"

# famille : [(dossier, fichier, style, poids)] ; poids "100 900" pour les polices variables
FAMILIES = {
    "Plus Jakarta Sans": [("plusjakartasans", "PlusJakartaSans[wght].ttf", "normal", "200 800"), ("plusjakartasans", "PlusJakartaSans-Italic[wght].ttf", "italic", "200 800")],
    "Playfair Display": [("playfairdisplay", "PlayfairDisplay[wght].ttf", "normal", "400 900"), ("playfairdisplay", "PlayfairDisplay-Italic[wght].ttf", "italic", "400 900")],
    "Geist Mono": [("geistmono", "GeistMono[wght].ttf", "normal", "100 900")],
    "Hanken Grotesk": [("hankengrotesk", "HankenGrotesk[wght].ttf", "normal", "100 900")],
    "IBM Plex Mono": [("ibmplexmono", "IBMPlexMono-Regular.ttf", "normal", "400"), ("ibmplexmono", "IBMPlexMono-Medium.ttf", "normal", "500")],
    "Syne": [("syne", "Syne[wght].ttf", "normal", "400 800")],
    "Caveat": [("caveat", "Caveat[wght].ttf", "normal", "400 700")],
    "Barlow Condensed": [("barlowcondensed", "BarlowCondensed-Medium.ttf", "normal", "500"), ("barlowcondensed", "BarlowCondensed-SemiBold.ttf", "normal", "600"), ("barlowcondensed", "BarlowCondensed-Bold.ttf", "normal", "700")],
    "Cormorant Garamond": [("cormorantgaramond", "CormorantGaramond[wght].ttf", "normal", "300 700"), ("cormorantgaramond", "CormorantGaramond-Italic[wght].ttf", "italic", "300 700")],
    "Anton": [("anton", "Anton-Regular.ttf", "normal", "400")],
    "Fraunces": [("fraunces", "Fraunces[SOFT,WONK,opsz,wght].ttf", "normal", "100 900")],
    "DM Sans": [("dmsans", "DMSans[opsz,wght].ttf", "normal", "100 1000"), ("dmsans", "DMSans-Italic[opsz,wght].ttf", "italic", "100 1000")],
    "Inter": [("inter", "Inter[opsz,wght].ttf", "normal", "100 900")],
    "Jost": [("jost", "Jost[wght].ttf", "normal", "100 900")],
    "Montserrat": [("montserrat", "Montserrat[wght].ttf", "normal", "100 900")],
    "Newsreader": [("newsreader", "Newsreader[opsz,wght].ttf", "normal", "200 800")],
}
# latin + latin étendu courant (français, €, guillemets, tirets, flèches, puces)
UNICODES = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD"


def build(src):
    from fontTools import subset
    os.makedirs(DEST, exist_ok=True)
    for f in glob.glob(os.path.join(DEST, "*.woff")):
        os.remove(f)
    faces, lic = [], set()
    ranges = [(int(a, 16), int(b or a, 16)) for a, b in re.findall(r"U\+([0-9A-F]+)(?:-([0-9A-F]+))?", UNICODES)]
    cps = [c for a, b in ranges for c in range(a, b + 1)]
    for fam, files in FAMILIES.items():
        for d, fn, style, wt in files:
            out = re.sub(r"[^A-Za-z0-9-]", "", fn.replace(".ttf", "")) + ".woff"
            opts = subset.Options(); opts.flavor = "woff"; opts.layout_features = ["*"]; opts.name_IDs = ["*"]; opts.notdef_outline = True
            font = subset.load_font(os.path.join(src, "ofl", d, fn), opts)
            s = subset.Subsetter(opts); s.populate(unicodes=cps); s.subset(font)
            subset.save_font(font, os.path.join(DEST, out), opts)
            faces.append("@font-face{font-family:'%s';font-style:%s;font-weight:%s;font-display:swap;src:url(/assets/fonts/%s) format('woff');unicode-range:%s}"
                         % (fam, style, wt, out, UNICODES))
            lic.add(d)
    with open(os.path.join(DEST, "fonts.css"), "w", encoding="utf-8") as fh:
        fh.write("/* Polices sous licence SIL Open Font License 1.1 (voir /assets/fonts/LICENCES.txt), hébergées sur ce site. */\n" + "\n".join(faces) + "\n")
    with open(os.path.join(DEST, "LICENCES.txt"), "w", encoding="utf-8") as fh:
        for d in sorted(lic):
            fh.write("===== %s =====\n" % d + open(os.path.join(src, "ofl", d, "OFL.txt"), encoding="utf-8").read() + "\n\n")


GLINK = re.compile(r'(<noscript>)?<link[^>]+fonts\.(?:googleapis|gstatic)\.com[^>]*>(</noscript>)?\s*')


def rewrite_html(s):
    if "fonts.googleapis.com" not in s and "fonts.gstatic.com" not in s:
        return s
    first = [True]

    def rep(m):
        if first[0] and "stylesheet" in m.group(0):
            first[0] = False
            return '<link rel="stylesheet" href="%s">\n' % CSS_URL
        return ""
    s = GLINK.sub(rep, s)
    assert "fonts.googleapis.com" not in s and "fonts.gstatic.com" not in s
    return s


def rewrite(folder):
    n = 0
    for p in glob.glob(os.path.join(folder, "**", "*.html"), recursive=True):
        s = open(p, encoding="utf-8").read()
        t = rewrite_html(s)
        if t != s:
            open(p, "w", encoding="utf-8").write(t); n += 1
    return n


if __name__ == "__main__":
    build(sys.argv[1])
    print("polices :", len(os.listdir(DEST)), "fichiers")
