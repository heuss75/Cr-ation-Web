"""Effet « le burger se compose » pour le site exemple de la brasserie : de vraies photos (pain, steak, fromage, oignons, tomates, salade, pain)
qui tombent et s'empilent. Images détourées dans site/assets/ex/burger-*.webp."""

# (id, libellé, délai de chute en secondes), dans l'ordre où elles tombent
ETAPES = [("pb", "Pain brioché toasté", 0.0), ("st", "Steak haché de bœuf, cuit minute", 0.55), ("fr", "Cheddar fondu", 1.1),
          ("oi", "Oignons rouges marinés", 1.65), ("to", "Tomates du marché", 2.2), ("sa", "Salade croquante", 2.75), ("ph", "Pain aux graines de sésame", 3.3)]
D = {k: d for k, _, d in ETAPES}
# position finale de chaque couche, en % de la zone (gauche, haut, largeur)
GEO = {"ph": {"l": 9.193, "t": 4.473, "w": 80.621}, "sa": {"l": 2.981, "t": 21.725, "w": 94.037}, "to": {"l": 10.435, "t": 37.806, "w": 75.652}, "oi": {"l": 8.447, "t": 48.136, "w": 78.137}, "fr": {"l": 9.441, "t": 56.23, "w": 78.509}, "st": {"l": 10.683, "t": 59.851, "w": 77.516}, "pb": {"l": 7.702, "t": 75.612, "w": 79.876}}
RATIO = 0.8573   # largeur / hauteur de la zone

CSS = """
.burger-sec{background:radial-gradient(60% 80% at 75% 50%,#2a1d0b 0,#0d0f0c 70%);overflow:hidden}
.bsec{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}
.bsec .copy p{color:var(--mut);margin-top:14px;max-width:46ch}
.bsec ul{margin:22px 0;display:grid;gap:10px}
.bsec li{display:flex;gap:12px;align-items:center;font-size:15.5px}
.bsec li i{flex:none;width:22px;height:22px;border-radius:50%;background:var(--gold);color:#1a1205;display:grid;place-items:center;font:700 12px/1 'DM Sans',sans-serif;font-style:normal}
.bsec .px{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-top:6px}
.bsec .px b{font:italic 600 2rem 'Playfair Display',serif;color:var(--gold)}
.bsec .rj{background:transparent;border:1.5px solid #5a4217;color:var(--ink);padding:10px 18px;border-radius:99px;font:600 13.5px 'DM Sans',sans-serif;cursor:pointer}
.bsec .rj:hover{border-color:var(--gold)}
.burger{position:relative;width:min(100%,400px);margin-inline:auto;aspect-ratio:0.8573}
.burger .stk{position:absolute;inset:0}
.burger .l{position:absolute;display:block;height:auto;transform-origin:center;pointer-events:none;user-select:none}
.burger .gl{position:absolute;inset:-8% -14%;background:radial-gradient(closest-side,rgba(255,200,110,.55),transparent);opacity:0;pointer-events:none}
.burger .sh{position:absolute;left:6%;right:6%;bottom:-1.5%;height:5%;background:radial-gradient(closest-side,rgba(0,0,0,.7),transparent);filter:blur(4px)}
@media(max-width:900px){.bsec{grid-template-columns:1fr;gap:20px}.bsec .copy{order:2}.burger{width:min(100%,320px)}}
@media(prefers-reduced-motion:no-preference){
  .burger.arm .l,.bsec.arm li{opacity:0}
  .burger.go .l{animation:bdrop .95s both;animation-delay:var(--d)}
  .burger.go .stk{animation:bsettle .6s ease-out 3.95s both;transform-origin:50% 100%}
  .burger.go .sh{animation:bshadow 4.6s ease-out both}
  .burger.go .gl{animation:bglow 1.6s ease-out 4.05s both}
  .bsec.go li{animation:bli .45s ease-out both;animation-delay:calc(var(--d) + .55s)}
  @keyframes bdrop{
    0%{transform:translateY(-480px) rotate(var(--r,0deg));opacity:0;animation-timing-function:cubic-bezier(.5,0,1,.55)}
    6%{opacity:1}
    58%{transform:translateY(0) rotate(0);opacity:1;animation-timing-function:cubic-bezier(.2,.7,.3,1)}
    74%{transform:translateY(-16px);animation-timing-function:cubic-bezier(.5,0,1,.55)}
    87%{transform:translateY(0);animation-timing-function:cubic-bezier(.2,.7,.3,1)}
    94%{transform:translateY(-4px);animation-timing-function:cubic-bezier(.5,0,1,.55)}
    100%{transform:translateY(0);opacity:1}}
  @keyframes bsettle{0%{transform:scale(1,1)}35%{transform:scale(1.03,.96)}70%{transform:scale(.992,1.012)}100%{transform:scale(1,1)}}
  @keyframes bshadow{0%{opacity:.25;transform:scaleX(.7)}100%{opacity:.8;transform:scaleX(1)}}
  @keyframes bglow{0%{opacity:0}30%{opacity:.9}100%{opacity:0}}
  @keyframes bli{from{opacity:0;transform:translateX(-12px)}to{opacity:1;transform:none}}
}
"""

ROT = {"to": "-9deg", "oi": "6deg", "sa": "-4deg", "ph": "3deg", "st": "-3deg", "fr": "5deg", "pb": "0deg"}

def _layers():
    out = []
    for k, _, d in ETAPES:
        g = GEO[k]
        out.append(f'<img class="l" src="/assets/ex/burger-{k}.webp" alt="" loading="lazy" decoding="async" '
                   f'style="left:{g["l"]}%;top:{g["t"]}%;width:{g["w"]}%;--d:{d}s;--r:{ROT[k]}">')
    return "".join(out)

def html():
    lis = "".join(f'<li style="--d:{d}s"><i>✓</i>{t}</li>' for _, t, d in ETAPES)
    return ('<section class="burger-sec" id="burger"><div class="w bsec" id="bsec"><div class="copy"><p class="eb">Notre signature</p><h2>Le Burger du Marché</h2>'
            '<p>Un burger monté minute, avec des produits des producteurs voisins. Regardez-le se composer, couche après couche.</p>'
            f'<ul>{lis}</ul><div class="px"><b>16 €</b><a class="btn" href="/exemples/bistro-reservation-client">Réserver une table</a>'
            '<button type="button" class="rj" id="rejouer">Rejouer ↻</button></div></div>'
            '<div class="burger" id="burger-fx" role="img" aria-label="Un burger composé de pain, steak, fromage, oignons, tomates, salade et pain aux graines de sésame">'
            f'<div class="gl"></div><div class="sh"></div><div class="stk">{_layers()}</div></div></div></section>\n')

JS = """<script>(function(){var b=document.getElementById('burger-fx'),s=document.getElementById('bsec');if(!b||!s)return;
var calm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;if(calm||!('IntersectionObserver' in window))return;
function play(){b.classList.remove('go');s.classList.remove('go');void b.offsetWidth;b.classList.add('go');s.classList.add('go')}
b.classList.add('arm');s.classList.add('arm');
new IntersectionObserver(function(es,o){es.forEach(function(e){if(e.isIntersecting){o.disconnect();var go=false,once=function(){if(!go){go=true;play()}};var im=[].slice.call(b.querySelectorAll('img'));Promise.all(im.map(function(i){return i.decode?i.decode().catch(function(){}):0})).then(once);setTimeout(once,1500)}})},{threshold:.45}).observe(b);
var r=document.getElementById('rejouer');if(r)r.addEventListener('click',play)})()</script>"""
