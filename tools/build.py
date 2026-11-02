# -*- coding: utf-8 -*-
"""Génère le site statique dans ../site à partir de tools/src et des contenus.
Usage : python3 tools/build.py"""
import os, re, json, hashlib, html, sys
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from content_faq import CATS, FAQ
from content_legal import mk as legal_pages

OUT = os.path.join(ROOT, "site")
SRC = os.path.join(ROOT, "tools", "src")

# ------------------------------------------------------------------ réglages
SITE_NAME = "Devanture Web"
BASE_URL = "https://accueil.ouvert.workers.dev"   # à remplacer par le vrai domaine
INDEXABLE = False                                  # passer à True au lancement (retire le noindex)
UPDATED_HUMAN = "1 novembre 2026"
UPDATED_ISO = "2026-11-01"
CONTACT_EMAIL = ""                                 # adresse pro, quand elle existe (active les boutons « copier »)

# Identité de l'éditeur : tout champ vide apparaît en jaune « À compléter » dans les textes légaux.
EDITOR = dict(site_name=SITE_NAME, nom="", statut="", siret="", adresse="", tel="", email=CONTACT_EMAIL,
              directeur="", tva="", tribunal="")


def rd(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def wr(rel, s):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


# ------------------------------------------------------------------ source de l'accueil
home = rd(os.path.join(SRC, "home-v3.html"))
base_css = re.search(r"<style>([\s\S]*?)</style>", home).group(1)
sprite = re.search(r'<svg width="0"[\s\S]*?</svg>', home).group(0)
home_main = re.search(r'<main id="haut">([\s\S]*?)</main>', home).group(1)
demo_js = re.search(r"<script>([\s\S]*?)</script>", home).group(1)

# jetons : clair + variables supplémentaires (le sombre est dans site-extra.css)
base_css = re.sub(r":root\{[\s\S]*?\n\}\n", lambda m: m.group(0), base_css, count=1)
reps = [
    ("background:rgba(255,255,255,.93);-webkit-backdrop-filter", "background:var(--hdr);-webkit-backdrop-filter"),
    (".btn.ghost{background:#fff;", ".btn.ghost{background:var(--surface);"),
    ("background:#E3E3E3;color:var(--ink2)", "background:var(--soft);color:var(--ink2)"),
    (".proof{background:#fff;", ".proof{background:var(--surface);"),
    (".bar{margin-top:16px;background:#0B0B0C;", ".bar{margin-top:16px;background:var(--bar);"),
    (".big{background:var(--ink);color:var(--bg);", ".big{background:var(--big-bg);color:var(--big-ink);"),
    (".big .btn{margin-top:24px;width:100%;background:var(--bg);color:var(--ink)}", ".big .btn{margin-top:24px;width:100%;background:#fff;color:#0B0B0C}"),
    ("box-shadow:0 12px 34px rgba(0,0,0,.08)", "box-shadow:0 12px 34px var(--shadow)"),
]
for a, b in reps:
    if a not in base_css:
        raise SystemExit("remplacement CSS introuvable : " + a)
    base_css = base_css.replace(a, b)
# la barre du haut (sécurité iPhone) doit suivre le thème : déjà var(--bg)
css = base_css + "\n" + rd(os.path.join(SRC, "site-extra.css"))

NEW_SYMBOLS = """
<defs>
<symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></symbol>
<symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></symbol>
<symbol id="i-moon" viewBox="0 0 24 24"><path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>
<symbol id="i-x" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></symbol>
<symbol id="i-up" viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></symbol>
<symbol id="i-chat" viewBox="0 0 24 24"><path d="M21 12a8 8 0 0 1-11.7 7.1L4 20.5l1.4-4.6A8 8 0 1 1 21 12z"/></symbol>
<symbol id="i-copy" viewBox="0 0 24 24"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 0 1 2-2h9"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path d="m5 12.5 4.5 4.5L19 7.5"/></symbol>
<symbol id="i-eye" viewBox="0 0 24 24"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></symbol>
<symbol id="i-eyeoff" viewBox="0 0 24 24"><path d="M3 3l18 18M10.6 5.1A10 10 0 0 1 12 5c6.4 0 10 7 10 7a17 17 0 0 1-3.2 4M6.3 6.4A17 17 0 0 0 2 12s3.6 7 10 7a10 10 0 0 0 4.2-.9M9.9 9.9a3 3 0 0 0 4.2 4.2"/></symbol>
<symbol id="i-print" viewBox="0 0 24 24"><path d="M7 9V3h10v6M7 17H4v-6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v6h-3"/><rect x="7" y="14" width="10" height="7"/></symbol>
<symbol id="i-loader" viewBox="0 0 24 24"><path d="M12 3a9 9 0 1 0 9 9"/></symbol>
<symbol id="i-link" viewBox="0 0 24 24"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></symbol>
<symbol id="i-help" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 1-1 1.7M12 17h.01"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 7 8.5 6 8.5-6"/></symbol>
</defs>
"""
sprite = sprite.replace("</svg>", NEW_SYMBOLS + "</svg>", 1)

# ------------------------------------------------------------------ gabarit
NAV = [("Accueil", "/", "home"), ("Exemples", "/#avant", None), ("Offre &amp; Prix", "/offre", "offre"),
       ("Comment ça marche", "/#etapes", None), ("FAQ", "/faq", "faq")]


def icon(n, cls="ic"):
    return '<svg class="%s" aria-hidden="true"><use href="#i-%s"/></svg>' % (cls, n)


def nav_html(cur, mobile=False):
    out = []
    for label, href, key in NAV:
        a = ' aria-current="page"' if (key and key == cur and not mobile) else ""
        out.append('<a href="%s"%s>%s</a>' % (href, a, label))
    return "".join(out)


EMAIL_BTNS_FAB = ""
EMAIL_FOOT = ""
if CONTACT_EMAIL:
    EMAIL_BTNS_FAB = '<button type="button" data-copy="%s">%s<span class="lbl">Copier l’e-mail</span></button>' % (CONTACT_EMAIL, icon("mail"))
    EMAIL_FOOT = '<li><button type="button" class="lnk" data-copy="%s">Copier l’e-mail de contact</button></li>' % CONTACT_EMAIL

HEADER = """
<a class="skip" href="#contenu">Aller au contenu</a>
<header class="hdr">
  <div class="wrap">
    <a class="logo" href="/" aria-label="%(name)s, accueil">
      <svg class="mark" viewBox="0 0 64 64" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M8 20 12 8h40l4 12"/><path d="M8 20a6 6 0 0 0 12 0 6 6 0 0 0 12 0 6 6 0 0 0 12 0 6 6 0 0 0 12 0"/><path d="M12 33v23h40V33"/><path d="M26 56V42h12v14"/><path d="M41 38l11 4.5-4.6 1.8-1.8 4.7z" fill="#17C26E" stroke="#17C26E" stroke-width="1.5"/></svg>
      <span><b>Devanture <em>Web</em></b><small>Site vitrine pour commerçants</small></span>
    </a>
    <nav class="nav" aria-label="Sections">%(nav)s</nav>
    <div class="acts">
      <button type="button" class="ibtn" data-search aria-label="Rechercher sur le site" title="Rechercher (touche /)">%(i_search)s</button>
      <button type="button" class="ibtn" id="theme" aria-label="Passer en mode sombre" aria-pressed="false">%(i_moon)s%(i_sun)s</button>
      <a class="btn ghost sm" href="/connexion">%(i_user)sSe connecter</a>
      <a class="btn sm" href="/inscription">Je veux mon site%(i_arrow)s</a>
      <button type="button" class="ibtn" id="burger" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu">%(i_menu)s</button>
    </div>
    <div class="prog" id="prog" aria-hidden="true"><i></i></div>
  </div>
</header>
<div class="menu" id="menu" inert>
  <nav aria-label="Menu principal">%(mnav)s<a href="/connexion">Se connecter</a></nav>
  <div class="mcta"><a class="btn" href="/inscription">Je veux mon site%(i_arrow)s</a><button type="button" class="btn ghost" data-search>%(i_search)sRechercher</button></div>
</div>
""" % dict(name=SITE_NAME, nav="%(nav)s", mnav="%(mnav)s", i_monitor=icon("monitor"), i_search=icon("search"), i_moon=icon("moon", "ic ic-moon"),
           i_sun=icon("sun", "ic ic-sun"), i_user=icon("user"), i_arrow=icon("arrow"), i_menu=icon("menu"))

FOOTER = """
<footer class="ft">
  <div class="ftg">
    <div class="brand"><b>Devanture <em>Web</em></b><p>Des sites vitrines clé en main pour les commerces et les indépendants : domaine, hébergement, espace client et guide pub inclus.</p></div>
    <div><h3>Offre</h3><ul><li><a href="/offre">Offre et prix</a></li><li><a href="/#etapes">Comment ça marche</a></li><li><a href="/faq">FAQ</a></li></ul></div>
    <div><h3>Légal</h3><ul><li><a href="/mentions-legales">Mentions légales</a></li><li><a href="/cgv">Conditions générales de vente</a></li><li><a href="/confidentialite">Confidentialité</a></li><li><a href="/cookies">Cookies</a></li><li><button type="button" class="lnk" data-cookies>Gérer les cookies</button></li></ul></div>
    <div><h3>Contact</h3><ul><li><a href="/inscription">Faire une demande</a></li><li><a href="/connexion">Espace client</a></li>%(email)s<li><button type="button" class="lnk" data-copy-url="page">Copier le lien de cette page</button></li></ul></div>
  </div>
  <div class="ftbot"><span>© 2026 %(name)s</span><span>Site mis à jour le <time datetime="%(iso)s">%(human)s</time></span></div>
</footer>
<div class="fab-wrap">
  <div class="fpanel" id="fpanel" hidden>
    <p>Une question ? Une demande ?</p>
    <a href="/commander">%(i_chat)sFaire une demande</a>
    <a href="/faq">%(i_help)sLire la FAQ</a>
    %(emailfab)s
    <button type="button" data-copy-url="/">%(i_link)s<span class="lbl">Copier le lien du site</span></button>
  </div>
  <button type="button" class="fab" id="fab" aria-expanded="false" aria-controls="fpanel">%(i_chat)s<span>Contact</span></button>
</div>
<button type="button" class="top" id="top" aria-label="Retour en haut de la page">%(i_up)s</button>
<div class="toast" id="toast" role="status" aria-live="polite"></div>

<div class="cookie" id="cookie" role="dialog" aria-labelledby="ck-t" hidden>
  <h2 id="ck-t">Vos choix sur les cookies</h2>
  <p>Ce site n’utilise ni publicité ni outil de mesure tiers. Nous vous proposons un seul réglage optionnel : mémoriser d’où vient votre visite (suivi UTM), pour savoir quelle annonce ou quel lien vous a amené. <a href="/cookies">En savoir plus</a></p>
  <div class="opts" id="ck-opts" hidden>
    <label class="switch"><input type="checkbox" checked disabled><span><b>Nécessaires</b><small>Mémoriser vos choix et le thème clair ou sombre. Toujours actifs.</small></span></label>
    <label class="switch"><input type="checkbox" id="ck-utm"><span><b>Suivi des campagnes (UTM)</b><small>Garde 30 jours l’origine de votre visite et la joint à votre demande.</small></span></label>
  </div>
  <div class="row">
    <button type="button" class="btn ghost" id="ck-no">Tout refuser</button>
    <button type="button" class="btn ghost" id="ck-cfg">Personnaliser</button>
    <button type="button" class="btn" id="ck-yes">Tout accepter</button>
  </div>
  <div class="row"><button type="button" class="btn" id="ck-save" hidden>Enregistrer mes choix</button></div>
</div>

<dialog class="sdlg" id="search" aria-label="Recherche sur le site">
  <form method="dialog">
    <div class="sbar">%(i_search)s<input type="search" id="sq" placeholder="Rechercher : prix, modification, résilier…" autocomplete="off" aria-label="Rechercher sur le site"><kbd>Échap</kbd>
      <button type="submit" class="ibtn" aria-label="Fermer la recherche">%(i_x)s</button></div>
    <div class="sres" id="sres" role="listbox" aria-live="polite"></div>
  </form>
</dialog>
""" % dict(name=SITE_NAME, iso=UPDATED_ISO, human=UPDATED_HUMAN, email=EMAIL_FOOT, emailfab=EMAIL_BTNS_FAB, i_chat=icon("chat"), i_help=icon("help"),
           i_link=icon("link"), i_up=icon("up"), i_search=icon("search"), i_x=icon("x"))

THEME_INIT = "(function(){try{var t=localStorage.getItem('sv_theme');if(!t)t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.setAttribute('data-theme',t)}catch(e){}})()"

# empreinte des fichiers pour vider le cache à chaque changement
js_common = rd(os.path.join(SRC, "site.js"))
VER = hashlib.sha1((css + js_common + demo_js + rd(os.path.join(SRC, "booking.js")) + rd(os.path.join(SRC, "admin.js")) + rd(os.path.join(SRC, "admin.css")) + rd(os.path.join(SRC, "espace.js")) + rd(os.path.join(SRC, "espace.css"))).encode("utf-8")).hexdigest()[:8]

search_entries = []   # rempli après


def page(slug, title, desc, body, cur=None, page_js="", head_extra="", mainclass="", full_title=None):
    path = "/" if slug == "index" else "/" + slug
    t = full_title or ("%s | %s" % (title, SITE_NAME))
    robots = "" if INDEXABLE else '<meta name="robots" content="noindex, nofollow">\n'
    nav = nav_html(cur)
    mnav = nav_html(cur, True)
    header = HEADER % dict(nav=nav, mnav=mnav)
    s = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%(t)s</title>
<meta name="description" content="%(d)s">
%(robots)s<meta name="theme-color" content="#F5F6F6">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:title" content="%(t)s">
<meta property="og:description" content="%(d)s">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<link rel="canonical" href="%(base)s%(path)s">
<script>%(init)s</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,700&family=Playfair+Display:ital,wght@1,600&family=Geist+Mono:wght@400;500&family=Hanken+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Syne:wght@600;800&family=Caveat:wght@600;700&family=Barlow+Condensed:wght@500;600;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Anton&family=Fraunces:opsz,wght@9..144,500;9..144,700&display=swap">
<link rel="stylesheet" href="/assets/site.css?v=%(v)s">
%(head_extra)s</head>
<body>
%(sprite)s
%(header)s
<main id="contenu" tabindex="-1">
<span id="haut"></span>
%(body)s
</main>
%(footer)s
<script>window.SITE={v:"%(v)s",email:%(email)s};</script>
<script src="/assets/site.js?v=%(v)s" defer></script>
%(page_js)s</body>
</html>
""" % dict(t=html.escape(t), d=html.escape(desc, quote=True), robots=robots, base=BASE_URL, path=path, init=THEME_INIT, v=VER,
           head_extra=head_extra, sprite=sprite, header=header, body=body, footer=FOOTER, email=json.dumps(CONTACT_EMAIL),
           page_js=page_js)
    wr(slug + ".html", s)
    return s


def phead(crumb, h1, lede, extra=""):
    return ('<div class="wrap"><header class="phead"><p class="crumb"><a href="/">Accueil</a> / %s</p><h1>%s</h1><p class="lede">%s</p>%s</header></div>'
            % (crumb, h1, lede, extra))


# ------------------------------------------------------------------ accueil
hm = home_main
hm = hm.replace('href="#commander"', 'href="/inscription"')
hm = re.sub(r'<section class="sec" id="commander">[\s\S]*?</section>', """<section class="sec" id="commander">
    <div class="order">
      <div>
        <p class="eyebrow">Commander</p>
        <h2 style="max-width:14ch">Prêt à lancer votre site ?</h2>
        <p class="lede">La demande prend 3 minutes, elle est sans engagement et sans paiement. Réunissez ces éléments, ils suffisent pour lancer la création.</p>
        <p style="margin-top:24px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="/inscription">Faire ma demande""" + icon("arrow") + """</a><a class="btn ghost" href="/offre">Voir l’abonnement</a></p>
      </div>
      <ul class="need">
        <li>Votre activité et le nom du commerce</li>
        <li>Adresse et téléphone</li>
        <li>Horaires d’ouverture</li>
        <li>Tarifs et durées des prestations</li>
        <li>Quelques photos de votre commerce</li>
        <li>Vos couleurs, si vous en avez</li>
        <li>Le nom de domaine souhaité</li>
      </ul>
    </div>
  </section>""", hm, count=1)
hm = hm.replace("Le prix ne change pas pendant l’engagement.</p>",
                'Le prix ne change pas pendant l’engagement.</p>\n        <p style="margin-top:12px"><a href="/offre" style="color:inherit">Voir le détail de l’abonnement →</a></p>', 1)
hm = hm.replace("<h2>Ce qu’on nous demande souvent</h2>",
                '<h2>Ce qu’on nous demande souvent</h2>\n    <p class="lede">Les réponses rapides. Les autres sont dans la <a href="/faq">FAQ complète</a>.</p>', 1)
home_body = hm.replace("</main>", "")
home_body = re.sub(r"^\s*<span id=\"haut\"></span>", "", home_body)
page("index", "Accueil", "Votre commerce mérite d’être vu, même en ligne. Un joli site vitrine fait sur mesure : nom de domaine, hébergement, espace client et guide pub inclus. Dès 60 € HT par mois, avec réservation en ligne en formule Pro.",
     home_body, cur="home", page_js='<script src="/assets/demo.js?v=%s" defer></script>\n' % VER,
     full_title="%s | Site vitrine pour commerçants" % SITE_NAME)

# ------------------------------------------------------------------ offre
offre_body = phead("Offre et prix", "Deux formules, tout compris",
                   "Essentiel à 60 € HT par mois, Pro à 100 € HT par mois avec réservation en ligne et agenda. 12 mois d’engagement. Domaine, hébergement, espace client et guide pub compris.",
                   '<div class="meta"><span>Mis à jour le <time datetime="%s">%s</time></span></div>' % (UPDATED_ISO, UPDATED_HUMAN)) + """
<div class="wrap">
<section class="sec" id="simulateur" style="padding-top:8px;padding-bottom:20px">
  <p class="eyebrow">Simulateur</p>
  <h2>Combien ça coûte, au total ?</h2>
  <div class="calc">
    <div>
      <fieldset class="fsel"><legend>Formule</legend>
        <label><input type="radio" name="fm" value="essentiel" checked><span>Essentiel · 60 €</span></label>
        <label><input type="radio" name="fm" value="pro"><span>Pro · 100 €</span></label>
      </fieldset>
      <label for="mails" class="lab" style="display:block;margin-top:18px;font:500 11.5px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--muted)">Adresses mail professionnelles</label>
      <p style="font:700 1.6rem var(--display);margin:8px 0 6px"><span id="c-n">0</span> <span id="c-n2" style="font-weight:600;color:var(--muted);font-size:1rem">adresse mail pro</span></p>
      <input type="range" id="mails" min="0" max="10" step="1" value="0" aria-describedby="c-help">
      <p id="c-help" class="sub">De 0 à 10 adresses. Chaque adresse coûte 4 € HT par mois ; la première est incluse dans la formule Pro.</p>
    </div>
    <div class="out" aria-live="polite">
      <div class="big-n"><span id="c-m">60</span> €<small>HT par mois</small></div>
      <div class="row2"><span id="c-basel">Formule Essentiel</span><b id="c-base">60 €</b></div>
      <div class="row2"><span id="c-maill">Options mail</span><b id="c-mail">0 €</b></div>
    </div>
  </div>
  <p class="sub" style="margin-top:12px">Montants hors taxes. La TVA, si elle s’applique, est ajoutée sur la facture.</p>
</section>

<section class="sec" id="contenu-offre" style="padding-top:40px;padding-bottom:20px">
  <p class="eyebrow">Ce que comprend l’abonnement</p>
  <h2>Inclus, en option, non inclus</h2>
  <div class="cmp">
    <div class="card"><span class="tag">Inclus</span><h3>Essentiel · 60 € HT</h3><ul>
      <li>Site vitrine sur mesure</li><li>Adapté au téléphone, tablette et ordinateur</li><li>Nom de domaine réservé et renouvelé chaque année</li><li>Hébergement et certificat HTTPS</li><li>Espace client de suivi</li><li>1 modification par mois, réalisée par nous sur demande</li><li>Relecture avant mise en ligne</li><li>Guide pub, 8 chapitres</li></ul></div>
    <div class="card pro"><span class="tag">En plus, avec le Pro</span><h3>Pro · 100 € HT</h3><ul>
      <li>Tout l’Essentiel</li><li>Éditeur en libre-service : textes, prix, horaires, photos</li><li>3 modifications par mois réalisées par nous</li><li>Outil de réservation en ligne : prestation, jour, créneau</li><li>Agenda dans l’espace client</li><li>1 adresse mail pro incluse</li><li>Prestations, durées et horaires paramétrés par nous</li></ul></div>
    <div class="card no"><span class="tag">Non inclus</span><h3>À prévoir à part</h3><ul>
      <li>Publicité faite pour vous</li><li>Référencement payant</li><li>Boutique en ligne et paiement en ligne (peut-être bientôt)</li><li>Rappels par SMS</li><li>Refonte complète du design</li><li>Séance photo</li></ul><p class="sub" style="margin-top:12px">Mail pro supplémentaire : 4 € HT par mois et par adresse.</p></div>
  </div>
</section>

<section class="sec" id="vie" style="padding-top:40px;padding-bottom:20px">
  <p class="eyebrow">La vie de votre abonnement</p>
  <h2>De la commande à la fin des 12 mois</h2>
  <ol class="tline">
    <li><span class="when">Jour 0</span><div><b>Vous faites votre demande</b><span class="d">Sans engagement ni paiement. Nous vous répondons pour valider les détails.</span></div></li>
    <li><span class="when">Validation</span><div><b>Vous acceptez les conditions et réglez le premier mois</b><span class="d">Le contrat est formé à ce moment-là.</span></div></li>
    <li><span class="when">+ 5 jours ouvrés</span><div><b>Votre aperçu est prêt</b><span class="d">Le délai commence quand tous vos contenus sont reçus. Vous demandez vos ajustements, puis vous validez.</span></div></li>
    <li><span class="when">Mise en ligne</span><div><b>Votre site est en ligne</b><span class="d">Nous branchons votre nom de domaine. Les 12 mois d’engagement démarrent. Vous recevez le guide pub.</span></div></li>
    <li><span class="when">Chaque mois</span><div><b>Vous modifiez ce que vous voulez</b><span class="d">Un texte, une photo ou un bloc, depuis votre espace client, avec retour en arrière possible.</span></div></li>
    <li><span class="when">Mois 10</span><div><b>Vous recevez un rappel</b><span class="d">60 jours avant l’échéance, pour décider : continuer, ou résilier avec 30 jours de préavis.</span></div></li>
    <li><span class="when">Mois 12</span><div><b>Reconduction ou fin</b><span class="d">Sans résiliation, l’abonnement continue pour 12 mois au même prix. Sinon le site est mis hors ligne et vous pouvez récupérer vos contenus et votre nom de domaine.</span></div></li>
  </ol>
</section>

<section class="sec" id="conditions" style="padding-top:40px;padding-bottom:20px">
  <p class="eyebrow">Conditions en bref</p>
  <h2>Ce qu’il faut savoir avant de signer</h2>
  <div class="prose" style="margin-top:20px">
    <ul>
      <li><strong>Engagement :</strong> 12 mois, puis reconduction tacite par périodes de 12 mois. Résiliation par écrit, 30 jours avant l’échéance.</li>
      <li><strong>Paiement :</strong> mensuel et d’avance, par carte ou prélèvement SEPA. Prix fixe pendant l’engagement.</li>
      <li><strong>Changer de formule :</strong> de l’Essentiel au Pro à tout moment (effet au mois suivant, nouvelle période de 12 mois) ; du Pro à l’Essentiel à l’échéance.</li>
      <li><strong>Modifications :</strong> 1 par mois, non cumulable. Nouvelle page ou refonte : sur devis.</li>
      <li><strong>Nom de domaine :</strong> géré et renouvelé par nous pendant l’engagement, transférable à la fin si tout est réglé.</li>
      <li><strong>Résultats :</strong> aucun nombre de visites, classement ou chiffre d’affaires n’est promis.</li>
    </ul>
    <p>Le texte complet fait foi : <a href="/cgv">conditions générales de vente</a>. Une question ? <a href="/faq">La FAQ</a> répond à la plupart.</p>
  </div>
</section>

<div class="cta-band">
  <h2>Prêt à lancer votre site ?</h2>
  <p>La demande prend 3 minutes. Elle est sans engagement et sans paiement.</p>
  <a class="btn" href="/inscription">Faire ma demande""" + icon("arrow") + """</a>
</div>
<div style="height:72px"></div>
</div>
"""
page("offre", "Offre et prix", "Les formules Essentiel (60 € HT par mois) et Pro (100 € HT par mois, avec réservation en ligne) en détail, 12 mois d’engagement, avec simulateur de prix.",
     offre_body, cur="offre")

# ------------------------------------------------------------------ FAQ
qhtml = []
for cat, qid, q, a in FAQ:
    label = dict(CATS)[cat]
    qhtml.append('<details class="q" id="q-%s" data-cat="%s"><summary>%s</summary><div class="a"><span class="cat">%s</span>%s</div></details>'
                 % (qid, cat, html.escape(q), label, a))
chips = '<button type="button" class="chip" data-cat="all" aria-pressed="true">Toutes</button>' + "".join(
    '<button type="button" class="chip" data-cat="%s" aria-pressed="false">%s</button>' % (c, l) for c, l in CATS)
faq_body = phead("FAQ", "Questions fréquentes", "Prix, délais, modifications, nom de domaine, résiliation, données : les réponses, classées par thème.") + """
<div class="wrap">
  <div class="faqtools">
    <div class="fsearch">""" + icon("search") + """<input type="search" id="qfilter" placeholder="Filtrer les questions : domaine, prix, résiliation…" aria-label="Filtrer les questions" autocomplete="off"></div>
    <div class="cats" role="group" aria-label="Catégories">""" + chips + """</div>
    <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap"><button type="button" class="cbtn" id="qtoggle">""" + icon("up") + """<span class="lbl">Tout déplier</span></button><span class="qcount" id="qcount" aria-live="polite"></span></div>
  </div>
  <div class="qlist" id="qlist">
""" + "\n".join(qhtml) + """
    <p class="qempty" id="qempty">Aucune question ne correspond. Essayez un autre mot, ou <a href="/inscription">posez-nous la question</a>.</p>
  </div>
  <div class="cta-band">
    <h2>Une autre question ?</h2>
    <p>Écrivez-nous via la demande en ligne : elle est sans engagement, nous vous répondons.</p>
    <a class="btn" href="/inscription">Poser ma question""" + icon("arrow") + """</a>
  </div>
  <div style="height:72px"></div>
</div>
"""
ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": BeautifulSoup(a, "html.parser").get_text(" ", strip=True)}}
    for _, _, q, a in FAQ]}
ldjs = '<script type="application/ld+json">%s</script>\n' % json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
page("faq", "FAQ", "Les réponses aux questions fréquentes : prix, délais, modifications, nom de domaine, résiliation, données personnelles.", faq_body, cur="faq", head_extra=ldjs)

# ------------------------------------------------------------------ commander
def field(name, label, kind="text", req=False, auto="", hint="", extra="", ph=""):
    r = ' data-req aria-required="true"' if req else ""
    opt = "" if req else ' <span class="opt">(facultatif)</span>'
    h = '<small class="h" id="%s-h">%s</small>' % (name, hint) if hint else ""
    ac = ' autocomplete="%s"' % auto if auto else ""
    d = ' aria-describedby="%s-e%s"' % (name, (" %s-h" % name) if hint else "")
    pl = ' placeholder="%s"' % ph if ph else ""
    return ('<div class="field"><label for="f-%s">%s%s</label><input id="f-%s" name="%s" type="%s"%s%s%s%s%s>%s<p class="errmsg" id="%s-e" role="alert"></p></div>'
            % (name, label, opt, name, name, kind, ac, r, d, pl, extra, h, name))


cmd_body = phead("Demande", "Demandez votre site", "Quelques informations suffisent pour commencer. La demande est sans engagement et sans paiement.") + """
<div class="wrap" style="padding-bottom:72px">
<div class="formcard">
<form id="demande" class="form" novalidate>
  <div class="alert bad" id="d-bad" role="alert" tabindex="-1">""" + icon("x") + """<span></span></div>
  <div class="fgrid two">
    """ + field("nom", "Votre nom", req=True, auto="name", extra=' minlength="2" maxlength="80"') + """
    """ + field("email", "Votre e-mail", "email", req=True, auto="email", extra=' maxlength="120"') + """
  </div>
  <div class="fgrid two">
    """ + field("tel", "Téléphone", "tel", auto="tel", extra=' maxlength="20"') + """
    """ + field("commerce", "Nom de votre commerce", req=True, auto="organization", extra=' minlength="2" maxlength="80"') + """
  </div>
  <div class="fgrid two">
    <div class="field"><label for="f-activite">Votre activité</label>
      <select id="f-activite" name="activite" data-req aria-required="true" aria-describedby="activite-e">
        <option value="">Choisir…</option><option value="coiffeur">Coiffeur</option><option value="restaurant">Restaurant</option><option value="artisan">Artisan du bâtiment</option><option value="therapeute">Thérapeute, bien-être</option><option value="coach">Coach sportif</option><option value="boutique">Boutique de quartier</option><option value="autre">Autre</option>
      </select><p class="errmsg" id="activite-e" role="alert"></p></div>
    """ + field("ville", "Ville", req=True, auto="address-level2", extra=' minlength="2" maxlength="60"') + """
  </div>
  <div class="field"><label for="f-formule">Formule</label>
    <select id="f-formule" name="formule" data-req aria-required="true" aria-describedby="formule-e"><option value="essentiel">Essentiel · 60 € HT par mois</option><option value="pro">Pro · 100 € HT par mois (réservation en ligne)</option></select><p class="errmsg" id="formule-e" role="alert"></p></div>
  <div class="fgrid two">
    """ + field("domaine", "Nom de domaine souhaité", hint="Par exemple : maisonolive ou maisonolive.fr. Nous vérifions la disponibilité.", extra=' maxlength="70" autocapitalize="none" spellcheck="false"') + """
    <div class="field"><label for="f-mails">Adresses mail pro <span class="opt">(4 € HT par mois chacune, la 1ʳᵉ incluse en Pro)</span></label>
      <select id="f-mails" name="mails" aria-describedby="mails-e"><option value="0">Aucune</option><option value="1">1 adresse</option><option value="2">2 adresses</option><option value="3">3 adresses</option><option value="4">4 adresses</option><option value="5">5 adresses</option></select><p class="errmsg" id="mails-e" role="alert"></p></div>
  </div>
  <div class="field"><label for="f-message">Un mot sur votre projet <span class="opt">(facultatif)</span></label>
    <textarea id="f-message" name="message" maxlength="1000" aria-describedby="message-e message-h" placeholder="Votre activité, ce que vous attendez du site, vos échéances…"></textarea>
    <small class="h" id="message-h">Merci de ne pas saisir d’informations sensibles (santé, banque).</small><p class="errmsg" id="message-e" role="alert"></p></div>
  <div class="hp" aria-hidden="true"><label>Ne pas remplir<input type="text" name="site_web_url" tabindex="-1" autocomplete="off"></label></div>
  <div class="field"><label class="check" for="f-cgv"><input type="checkbox" id="f-cgv" name="cgv" data-req aria-required="true" aria-describedby="cgv-e"><span>J’agis pour mon activité professionnelle et j’ai lu les <a href="/cgv" target="_blank" rel="noopener">conditions générales de vente</a> et la <a href="/confidentialite" target="_blank" rel="noopener">politique de confidentialité</a>.</span></label><p class="errmsg" id="cgv-e" role="alert"></p></div>
  <p class="sub">Vos informations servent uniquement à répondre à votre demande. Aucun paiement n’est demandé à cette étape.</p>
  <div><button class="btn" id="d-send" type="submit"><span class="lbl">Envoyer ma demande</span>""" + icon("loader", "ic spin") + """</button></div>
</form>
<div class="done" id="d-done" aria-live="polite">
  <p class="eyebrow">Demande envoyée</p>
  <h2 style="margin:0;max-width:18ch">Merci, c’est bien reçu.</h2>
  <p>Votre numéro de demande :</p>
  <p><span class="ref" id="d-ref">—</span> <button type="button" class="cbtn" id="d-ref-btn" data-copy="">""" + icon("copy") + """<span class="lbl">Copier</span></button></p>
  <p>Gardez-le pour toute question. Nous vous répondons sous 2 jours ouvrés pour valider les détails. <strong>Aucun paiement n’a été demandé.</strong></p>
  <p style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="/espace">Mon espace</a><a class="btn ghost" href="/offre">Voir l’abonnement</a></p>
</div>
</div>
</div>
<dialog class="dlg" id="confirm" aria-labelledby="cf-t">
  <h2 id="cf-t">Envoyer votre demande ?</h2>
  <p>Vérifiez ces informations. La demande est sans engagement et sans paiement.</p>
  <dl><div><dt>Nom</dt><dd id="cf-nom"></dd></div><div><dt>E-mail</dt><dd id="cf-mail"></dd></div><div><dt>Commerce</dt><dd id="cf-com"></dd></div><div><dt>Activité</dt><dd id="cf-act"></dd></div><div><dt>Formule</dt><dd id="cf-formule"></dd></div><div><dt>Mail pro</dt><dd id="cf-mails"></dd></div></dl>
  <div class="row"><button type="button" class="btn ghost" id="cf-cancel">Modifier</button><button type="button" class="btn" id="cf-ok">Oui, envoyer</button></div>
</dialog>
"""
page("commander", "Demander mon site", "Faites votre demande de site vitrine en 3 minutes : sans engagement et sans paiement.", cmd_body)

# ------------------------------------------------------------------ inscription et connexion
def pwfield(name, label, auto):
    return ('<div class="field"><label for="f-%s">%s</label><div class="pwrap"><input id="f-%s" name="%s" type="password" autocomplete="%s" data-req aria-required="true" aria-describedby="%s-e" minlength="8" maxlength="100">'
            '<button type="button" class="eye" aria-label="Afficher le mot de passe" aria-pressed="false">' % (name, label, name, name, auto, name)
            + icon("eye", "ic on") + icon("eyeoff", "ic off") + '</button></div><p class="errmsg" id="%s-e" role="alert"></p></div>' % name)

HP = '<div class="hp" aria-hidden="true"><label>Ne pas remplir<input type="text" name="site_web_url" tabindex="-1" autocomplete="off"></label></div>'

signup_body = phead("Inscription", "Créez votre compte", "Un compte est nécessaire pour faire une demande de site. Il vous donne aussi accès au suivi de votre commande.") + """
<div class="wrap ctr" style="padding-bottom:72px">
<div class="formcard" style="max-width:560px">
<form id="signup" class="form" novalidate>
  <div class="alert bad" id="s-bad" role="alert" tabindex="-1">""" + icon("x") + """<span></span></div>
  """ + field("nom", "Votre nom", req=True, auto="name", extra=' minlength="2" maxlength="80"') + """
  """ + field("email", "Votre e-mail", "email", req=True, auto="email", extra=' maxlength="120"') + """
  """ + pwfield("password", "Votre mot de passe (8 caractères minimum)", "new-password") + """
  """ + pwfield("password2", "Confirmez votre mot de passe", "new-password") + """
  """ + HP + """
  <div class="field"><label class="check" for="f-cgv"><input type="checkbox" id="f-cgv" name="cgv" data-req aria-required="true" aria-describedby="cgv-e"><span>J’agis pour mon activité professionnelle et j’ai lu les <a href="/cgv" target="_blank" rel="noopener">conditions générales de vente</a> et la <a href="/confidentialite" target="_blank" rel="noopener">politique de confidentialité</a>.</span></label><p class="errmsg" id="cgv-e" role="alert"></p></div>
  <div><button class="btn" type="submit"><span class="lbl">Créer mon compte</span></button></div>
  <p class="sub">Déjà un compte ? <a href="/connexion">Se connecter</a>. Créer un compte est gratuit et sans engagement.</p>
</form>
</div>
</div>
"""
page("inscription", "Créer mon compte", "Créez votre compte pour faire votre demande de site vitrine.", signup_body)

login_body = phead("Connexion", "Connexion", "Suivez votre demande et accédez à votre espace client.") + """
<div class="wrap ctr" style="padding-bottom:72px">
<div class="formcard" style="max-width:520px">
<form id="login" class="form" novalidate>
  <div class="alert bad" id="l-bad" role="alert" tabindex="-1">""" + icon("x") + """<span></span></div>
  """ + field("email", "Votre e-mail", "email", req=True, auto="email", extra=' maxlength="120"') + """
  """ + pwfield("password", "Mot de passe", "current-password") + """
  <div><button class="btn" type="submit"><span class="lbl">Se connecter</span></button></div>
  <p class="sub"><a href="/mot-de-passe-oublie">Mot de passe oublié ?</a></p>
  <p class="sub">Pas encore de compte ? <a href="/inscription">Créer mon compte</a>.</p>
</form>
<div id="l-ok" hidden></div>
</div>
</div>
"""
page("connexion", "Connexion", "Espace client : suivi de commande et éditeur de modifications.", login_body)

forgot_body = phead("Mot de passe", "Mot de passe oublié", "Indiquez votre e-mail : nous vous envoyons un lien pour choisir un nouveau mot de passe.") + """
<div class="wrap ctr" style="padding-bottom:72px">
<div class="formcard" style="max-width:520px">
<form id="forgot" class="form" novalidate>
  <div class="alert bad" id="f-bad" role="alert" tabindex="-1">""" + icon("x") + """<span></span></div>
  """ + field("email", "Votre e-mail", "email", req=True, auto="email", extra=' maxlength="120"') + """
  """ + HP + """
  <div><button class="btn" type="submit"><span class="lbl">Envoyer le lien</span></button></div>
  <p class="sub"><a href="/connexion">Retour à la connexion</a></p>
</form>
<div class="done" id="f-done" aria-live="polite"><h2 style="margin:0">Vérifiez votre boîte mail.</h2><p>Si un compte existe avec cette adresse, un lien de réinitialisation vient de lui être envoyé. Il est valable 1 heure. Pensez à regarder dans les courriers indésirables.</p><p><a class="btn ghost" href="/connexion">Retour à la connexion</a></p></div>
</div>
</div>
"""
page("mot-de-passe-oublie", "Mot de passe oublié", "Recevez un lien pour choisir un nouveau mot de passe.", forgot_body)

reset_body = phead("Mot de passe", "Nouveau mot de passe", "Choisissez un nouveau mot de passe pour votre compte.") + """
<div class="wrap ctr" style="padding-bottom:72px">
<div class="formcard" style="max-width:520px">
<form id="reset" class="form" novalidate>
  <div class="alert bad" id="r-bad" role="alert" tabindex="-1">""" + icon("x") + """<span></span></div>
  """ + pwfield("password", "Nouveau mot de passe (8 caractères minimum)", "new-password") + """
  """ + pwfield("password2", "Confirmez le mot de passe", "new-password") + """
  <div><button class="btn" type="submit"><span class="lbl">Changer mon mot de passe</span></button></div>
</form>
</div>
</div>
"""
page("reinitialiser", "Nouveau mot de passe", "Choisissez un nouveau mot de passe.", reset_body)


# ------------------------------------------------------------------ administration (page indépendante : ni menu, ni pied de page du site)
def _ic(d): return '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="%s"/></svg>' % d
ADMIN_HTML = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Administration | Devanture Web</title>
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="robots" content="noindex, nofollow">
<meta name="color-scheme" content="light dark">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/admin.css?v=%(v)s">
</head>
<body>
<div class="gate card" id="gate" role="status" style="max-width:420px;margin:14vh auto"><p>Vérification de l’accès…</p></div>
<div class="shell" id="app" hidden>
<aside class="side">
<div class="brand"><i><svg width="22" height="22" viewBox="0 0 64 64" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M8 20 12 8h40l4 12"/><path d="M8 20a6 6 0 0 0 12 0 6 6 0 0 0 12 0 6 6 0 0 0 12 0 6 6 0 0 0 12 0"/><path d="M12 33v23h40V33"/><path d="M26 56V42h12v14"/><path d="M41 38l11 4.5-4.6 1.8-1.8 4.7z" fill="#17C26E" stroke="#17C26E" stroke-width="1.5"/></svg></i><div><b>Devanture Web</b><small>Espace administrateur</small></div></div>
<nav class="nav" aria-label="Administration">
<button type="button" id="n-stats" aria-current="page">""" + _ic("M3 3v18h18M7 15l4-4 3 3 5-6") + """Tableau de bord</button>
<button type="button" id="n-clients">""" + _ic("M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8") + """Clients</button>
<button type="button" id="n-rev">""" + _ic("M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6") + """Revenus</button>
<button type="button" id="n-com">""" + _ic("M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zM22 6l-10 7L2 6") + """Communication</button>
<button type="button" id="n-mdp">""" + _ic("M21 2l-2 2m-7.6 7.6a5.5 5.5 0 1 1-7.8 7.8 5.5 5.5 0 0 1 7.8-7.8zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4") + """Mot de passe</button>
</nav>
<div class="sp"></div>
<nav class="nav"><a href="/" target="_blank" rel="noopener">""" + _ic("M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3") + """Voir le site</a>
<button type="button" id="n-out">""" + _ic("M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9") + """Se déconnecter</button></nav>
</aside>
<main class="main" id="main"></main>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="/assets/admin.js?v=%(v)s" defer></script>
</body>
</html>
""" % dict(v=VER)
wr("admin.html", ADMIN_HTML)

ESPACE_HTML = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Mon espace | Devanture Web</title>
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="robots" content="noindex, nofollow">
<meta name="color-scheme" content="light dark">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/admin.css?v=%(v)s">
<link rel="stylesheet" href="/assets/espace.css?v=%(v)s">
</head>
<body>
<div class="gate card" id="gate" role="status" style="max-width:420px;margin:14vh auto"><p>Chargement de votre espace…</p></div>
<div class="shell" id="app" hidden>
<aside class="side">
<div class="brand"><i>""" + _ic("M3 11l9-8 9 8v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z") + """</i><div><b>Devanture Web</b><small>Mon espace</small></div></div>
<nav class="nav" id="nav" aria-label="Mon espace"></nav>
<div class="sp"></div>
<nav class="nav"><a href="/" target="_blank" rel="noopener">""" + _ic("M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3") + """Le site Devanture Web</a>
<button type="button" id="n-out">""" + _ic("M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9") + """Se déconnecter</button></nav>
</aside>
<main class="main" id="main"></main>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="/assets/espace.js?v=%(v)s" defer></script>
</body>
</html>
""" % dict(v=VER)
wr("espace.html", ESPACE_HTML)

# ------------------------------------------------------------------ pages légales
LEGAL = legal_pages(EDITOR)
LEG_TITLES = {"mentions-legales": "Mentions légales", "cgv": "CGV", "confidentialite": "Confidentialité", "cookies": "Cookies"}
for slug, p in LEGAL.items():
    soup = BeautifulSoup(p["body"], "html.parser")
    toc = []
    for h in soup.find_all("h2"):
        toc.append('<li><a href="#%s">%s</a></li>' % (h["id"], h.get_text()))
    note = '<p class="callout" style="margin-top:20px">%s</p>' % p["notice"] if p.get("notice") else ""
    extra = ('<div class="meta"><span>Dernière mise à jour : <time datetime="%s">%s</time></span>'
             '<button type="button" class="cbtn" data-print>%s<span class="lbl">Imprimer</span></button>'
             '<button type="button" class="cbtn" data-copy-url="page">%s<span class="lbl">Copier le lien</span></button></div>'
             % (UPDATED_ISO, UPDATED_HUMAN, icon("print"), icon("link"))) + note
    body = phead(p["title"], p["title"], p["lede"], extra)
    body += ('<div class="wrap"><div class="doc has-toc"><nav class="toc" aria-label="Sommaire"><b>Sommaire</b><ol>%s</ol></nav>'
             '<article class="prose"><p class="printonly">%s, %s. Mise à jour du %s. Page imprimée depuis %s%s.</p>%s</article></div></div>'
             % ("".join(toc), SITE_NAME, p["title"], UPDATED_HUMAN, BASE_URL, "/" + slug, p["body"]))
    page(slug, p["title"], p["desc"], body)

# ------------------------------------------------------------------ 404
nf = """<div class="wrap"><div class="notfound"><p class="crumb">Erreur 404</p><p class="n" aria-hidden="true">404</p>
<h1 style="font:800 clamp(1.8rem,5vw,2.8rem)/1.1 var(--display);letter-spacing:-.03em;margin:8px 0 12px">Cette page n’existe pas (ou plus).</h1>
<p class="lede">Le lien est peut-être erroné. Essayez la recherche, ou repartez de l’accueil.</p>
<p style="margin-top:24px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="/">Retour à l’accueil</a><button type="button" class="btn ghost" data-search>""" + icon("search") + """Rechercher</button></p></div></div>"""
page("404", "Page introuvable", "Cette page n’existe pas.", nf)

# ------------------------------------------------------------------ démo réservation
SERVICES = [("coupe-femme", "Coupe femme", "1 h", "38 €"), ("coupe-homme", "Coupe homme", "30 min", "24 €"),
            ("couleur", "Couleur", "1 h 30", "70 €"), ("brushing", "Brushing", "30 min", "20 €")]
svc_html = "".join('<label class="svc"><input type="radio" name="svc" value="%s"%s><span><b>%s</b><small>%s · %s</small></span></label>'
                   % (k, " checked" if i == 0 else "", n, d, p) for i, (k, n, d, p) in enumerate(SERVICES))
resa_body = phead("Démo", "Réservation en ligne", "Voici ce que vos clients voient avec la formule Pro. Essayez : choisissez une prestation, un jour, un créneau. Le créneau pris n’est plus proposé aux suivants.") + """
<div class="wrap" style="padding-bottom:72px">
<div class="alert warn on" style="display:flex;margin-bottom:18px" role="note">""" + icon("help") + """<span><b>Démonstration.</b> Ne saisissez pas de vraies données : un prénom fictif suffit. Les réservations de test sont supprimées au bout de 24 heures. Le salon « Atelier Capucine » est imaginaire.</span></div>
<div class="tabs2" role="tablist" aria-label="Vue">
  <button type="button" role="tab" id="t-client" aria-selected="true" aria-controls="p-client">Vue de votre client</button>
  <button type="button" role="tab" id="t-agenda" aria-selected="false" aria-controls="p-agenda" tabindex="-1">Votre agenda (exemple)</button>
</div>
<div id="p-client" role="tabpanel" aria-labelledby="t-client" class="resa">
  <form id="resa" novalidate>
    <fieldset class="rstep"><legend><span class="n">1</span> Prestation</legend><div class="svcs">""" + svc_html + """</div></fieldset>
    <fieldset class="rstep"><legend><span class="n">2</span> Jour</legend><div class="days" id="r-days" role="group" aria-label="Jours disponibles"></div></fieldset>
    <fieldset class="rstep"><legend><span class="n">3</span> Créneau</legend><p class="sub" id="r-slot-help">Choisissez d’abord un jour.</p><div class="slots" id="r-slots" role="group" aria-label="Créneaux disponibles"></div></fieldset>
    <fieldset class="rstep"><legend><span class="n">4</span> Vos coordonnées</legend>
      <div class="fgrid two">
        <div class="field"><label for="r-nom">Prénom</label><input id="r-nom" name="nom" type="text" maxlength="40" autocomplete="given-name" aria-describedby="r-nom-e"><p class="errmsg" id="r-nom-e" role="alert"></p></div>
        <div class="field"><label for="r-tel">Téléphone <span class="opt">(facultatif)</span></label><input id="r-tel" name="tel" type="tel" maxlength="20" autocomplete="tel" aria-describedby="r-tel-e"><p class="errmsg" id="r-tel-e" role="alert"></p></div>
      </div>
      <div class="hp" aria-hidden="true"><label>Ne pas remplir<input type="text" name="site_web_url" tabindex="-1" autocomplete="off"></label></div>
    </fieldset>
    <div class="alert bad" id="r-bad" role="alert" tabindex="-1">""" + icon("x") + """<span></span></div>
    <p class="rsum" id="r-sum" aria-live="polite"></p>
    <button class="btn" id="r-send" type="submit"><span class="lbl">Réserver ce créneau</span>""" + icon("loader", "ic spin") + """</button>
  </form>
  <div class="done" id="r-done" aria-live="polite">
    <p class="eyebrow">Réservation enregistrée</p>
    <h2 style="margin:0;max-width:20ch" id="r-done-t">C’est réservé.</h2>
    <p id="r-done-p"></p>
    <p>Numéro : <span class="ref" id="r-ref">—</span></p>
    <p style="display:flex;gap:12px;flex-wrap:wrap"><button type="button" class="btn" id="r-again">Réserver un autre créneau</button><button type="button" class="btn ghost" id="r-see">Voir dans l’agenda</button></p>
  </div>
</div>
<div id="p-agenda" role="tabpanel" aria-labelledby="t-agenda" class="resa" hidden>
  <p class="sub">Exemple de ce que vous voyez dans votre espace client : les rendez-vous du jour, triés par heure. Les lignes en gris sont fictives ; votre réservation de test s’ajoute en haut quand vous en faites une.</p>
  <ol class="agenda" id="ag-list"></ol>
</div>
<div class="cta-band">
  <h2>La réservation fait gagner du temps</h2>
  <p>Fini les appels manqués : vos clients réservent seuls, à toute heure. Disponible avec la formule Pro, à 100 € HT par mois.</p>
  <a class="btn" href="/inscription?formule=pro">Choisir le Pro""" + icon("arrow") + """</a>
</div>
</div>
"""
page("reservation-demo", "Démo de réservation", "Essayez la réservation en ligne de la formule Pro : choix de la prestation, du jour et du créneau.", resa_body, cur="offre",
     page_js='<script src="/assets/booking.js?v=%s" defer></script>\n' % VER)

# ------------------------------------------------------------------ index de recherche
PAGES = [("index", "Accueil"), ("offre", "Offre et prix"), ("faq", "FAQ"), ("commander", "Commander"), ("inscription", "Inscription"), ("connexion", "Connexion"),
         ("mentions-legales", "Mentions légales"), ("cgv", "CGV"), ("confidentialite", "Confidentialité"), ("cookies", "Cookies"), ("reservation-demo", "Démo réservation")]
entries = []
for slug, label in PAGES:
    soup = BeautifulSoup(rd(os.path.join(OUT, slug + ".html")), "html.parser")
    main = soup.find("main")
    url0 = "/" if slug == "index" else "/" + slug
    if slug in ("commander", "connexion", "inscription"):
        h1 = main.find("h1")
        entries.append(dict(t=h1.get_text(" ", strip=True), p=label, u=url0, x=main.find(class_="lede").get_text(" ", strip=True)))
        continue
    if slug == "faq":
        for d in main.find_all("details", class_="q"):
            entries.append(dict(t=d.find("summary").get_text(" ", strip=True), p=label, u=url0 + "#" + d["id"],
                                x=d.find(class_="a").get_text(" ", strip=True).replace(" #", "").replace("#", "")[:400]))
        continue
    for h in main.find_all("h2"):
        if "cta-band" in (h.parent.get("class") or []):
            continue
        hid = h.get("id")
        if not hid:
            sec = h.find_parent(attrs={"id": True})
            hid = sec["id"] if sec else ""
            if hid == "contenu":
                hid = ""
        txt = []
        for sib in h.next_siblings:
            if getattr(sib, "name", None) in ("h2", "h3"):
                break
            if hasattr(sib, "get_text"):
                txt.append(sib.get_text(" ", strip=True))
            if sum(len(t) for t in txt) > 360:
                break
        t = h.get_text(" ", strip=True).replace("#", "").strip()
        if not t or t.startswith("Article") and False:
            continue
        entries.append(dict(t=t, p=label, u=url0 + ("#" + hid if hid else ""), x=" ".join(txt)[:400]))
wr("assets/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#fff"/><g transform="translate(5 5) scale(.84)" fill="none" stroke="#0B0B0C" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M8 20 12 8h40l4 12"/><path d="M8 20a6 6 0 0 0 12 0 6 6 0 0 0 12 0 6 6 0 0 0 12 0 6 6 0 0 0 12 0"/><path d="M12 33v23h40V33"/><path d="M26 56V42h12v14"/><path d="M41 38l11 4.5-4.6 1.8-1.8 4.7z" fill="#17C26E" stroke="#17C26E" stroke-width="1.5"/></g></svg>')
wr("assets/search-index.json", json.dumps(entries, ensure_ascii=False, separators=(",", ":")))

# ------------------------------------------------------------------ fichiers statiques
wr("assets/site.css", css)
wr("assets/site.js", js_common)
wr("assets/demo.js", demo_js)
wr("assets/booking.js", rd(os.path.join(SRC, "booking.js")))
wr("assets/admin.js", rd(os.path.join(SRC, "admin.js")))
wr("assets/admin.css", rd(os.path.join(SRC, "admin.css")))
wr("assets/espace.js", rd(os.path.join(SRC, "espace.js")))
wr("assets/espace.css", rd(os.path.join(SRC, "espace.css")))
wr("robots.txt", "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % BASE_URL if INDEXABLE else "User-agent: *\nDisallow: /\n")
if INDEXABLE:
    urls = "".join("<url><loc>%s%s</loc><lastmod>%s</lastmod></url>" % (BASE_URL, "" if s == "index" else "/" + s, UPDATED_ISO) for s, _ in PAGES if s != "connexion")
    wr("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>' % urls)
print("OK  version=%s  pages=%d  recherche=%d entrées  css=%dko" % (VER, len(PAGES) + 1, len(entries), len(css) // 1024))
