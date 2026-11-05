"""Effet « le burger se compose » pour le site exemple de la brasserie (pain, steak, fromage, salade, tomates... qui tombent et s'empilent)."""

# (id, libellé, délai de chute en secondes)
ETAPES = [("pb", "Pain brioché toasté", 0.0), ("st", "Steak haché de bœuf, cuit minute", 0.55), ("fr", "Cheddar fondu", 1.1),
          ("sa", "Salade croquante", 1.65), ("to", "Tomates du marché", 2.2), ("oi", "Oignons rouges marinés", 2.85), ("ph", "Pain aux graines de sésame", 3.3)]
D = {k: d for k, _, d in ETAPES}

CSS = '''
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
.burger{position:relative;max-width:440px;margin-inline:auto;width:100%}
.burger svg{display:block;width:100%;height:auto;overflow:visible}
.burger .l{transform-box:fill-box;transform-origin:center}
@media(max-width:900px){.bsec{grid-template-columns:1fr;gap:20px}.bsec .copy{order:2}.burger{max-width:340px}}
@media(prefers-reduced-motion:no-preference){
  .burger.arm .l,.bsec.arm li{opacity:0}
  .burger.go .l{animation:bdrop .95s both;animation-delay:var(--d)}
  .burger.go .stk{animation:bsettle .6s ease-out 3.95s both}
  .burger.go .sh{animation:bshadow 4.6s ease-out both}
  .burger.go .sd{animation:bpop .35s cubic-bezier(.3,1.6,.5,1) both;animation-delay:var(--d)}
  .burger.go .gl{animation:bglow 1.4s ease-out 4.1s both}
  .bsec.go li{animation:bli .45s ease-out both;animation-delay:calc(var(--d) + .55s)}
  @keyframes bdrop{
    0%{transform:translateY(-330px) rotate(var(--r,0deg));opacity:0;animation-timing-function:cubic-bezier(.5,0,1,.55)}
    6%{opacity:1}
    58%{transform:translateY(0) rotate(0);opacity:1;animation-timing-function:cubic-bezier(.2,.7,.3,1)}
    74%{transform:translateY(-15px);animation-timing-function:cubic-bezier(.5,0,1,.55)}
    87%{transform:translateY(0);animation-timing-function:cubic-bezier(.2,.7,.3,1)}
    94%{transform:translateY(-4px);animation-timing-function:cubic-bezier(.5,0,1,.55)}
    100%{transform:translateY(0);opacity:1}}
  @keyframes bsettle{0%{transform:scale(1,1)}35%{transform:scale(1.035,.955)}70%{transform:scale(.99,1.015)}100%{transform:scale(1,1)}}
  @keyframes bshadow{0%{opacity:.25;transform:scaleX(.7)}100%{opacity:.55;transform:scaleX(1)}}
  @keyframes bpop{0%{transform:scale(0);opacity:0}100%{transform:scale(1);opacity:1}}
  @keyframes bglow{0%{opacity:0}30%{opacity:.9}100%{opacity:0}}
  @keyframes bli{from{opacity:0;transform:translateX(-12px)}to{opacity:1;transform:none}}
}
'''

def _svg():
    g = lambda k, extra="", body="": f'<g class="l" style="--d:{D[k]}s{extra}">{body}</g>'
    seeds = "".join(f'<ellipse class="sd" style="--d:{3.95 + i * 0.07:.2f}s" cx="{x}" cy="{y}" rx="5.5" ry="3" transform="rotate({r} {x} {y})" fill="#f6e3b4" stroke="#b9823a" stroke-width=".6"/>'
                    for i, (x, y, r) in enumerate([(150, 156, -25), (190, 146, 10), (232, 150, 30), (268, 166, 55), (120, 178, -50), (206, 172, -15), (250, 188, 40), (166, 190, 20)]))
    return f'''<svg viewBox="0 0 400 380" role="img" aria-label="Un burger composé de pain, steak, fromage, salade, tomates, oignons et pain aux graines de sésame">
<defs>
<linearGradient id="bgp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8a553"/><stop offset="1" stop-color="#b9702b"/></linearGradient>
<linearGradient id="bgs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a2e17"/><stop offset="1" stop-color="#341a0c"/></linearGradient>
<radialGradient id="bgt" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#ef6a4b"/><stop offset="1" stop-color="#c9321f"/></radialGradient>
<radialGradient id="bgg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffd98a" stop-opacity=".9"/><stop offset="1" stop-color="#ffd98a" stop-opacity="0"/></radialGradient>
</defs>
<ellipse class="gl" cx="200" cy="230" rx="190" ry="140" fill="url(#bgg)" opacity="0"/>
<ellipse class="sh" cx="200" cy="352" rx="150" ry="16" fill="#000" opacity=".55" style="transform-box:fill-box;transform-origin:center"/>
<ellipse cx="200" cy="338" rx="165" ry="20" fill="#2a2113"/><ellipse cx="200" cy="334" rx="165" ry="19" fill="#3b2e1b"/>
<g class="stk" style="transform-box:fill-box;transform-origin:50% 100%">
{g("pb", body='<path d="M70 292h260q0 40-42 40H112q-42 0-42-40z" fill="url(#bgp)"/><path d="M92 300q108 14 216 0" stroke="#f3c07a" stroke-width="3" fill="none" opacity=".5" stroke-linecap="round"/>')}
{g("st", body='<rect x="60" y="262" width="280" height="34" rx="17" fill="url(#bgs)"/><path d="M86 272q30-6 60 0M178 278q34-6 66 0M266 272q24-5 48 0" stroke="#7a4325" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/>')}
{g("fr", body='<path d="M62 254H338L322 264 308 290 292 264H212L196 296 178 264H112L98 282 80 264Z" fill="#f4b73c" stroke="#d9951a" stroke-width="2" stroke-linejoin="round"/>')}
{g("sa", body='<path d="M54 252q16-24 32 0q16-24 32 0q16-24 32 0q16-24 32 0q16-24 32 0q16-24 32 0q16-24 32 0q16-24 32 0v12H54z" fill="#62b236"/><path d="M60 252q14-14 26 0q14-14 26 0q14-14 26 0q14-14 26 0q14-14 26 0q14-14 26 0q14-14 26 0" stroke="#8dd35a" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/>')}
{g("to", ';--r:-14deg', '<ellipse cx="124" cy="232" rx="50" ry="12" fill="url(#bgt)"/><ellipse cx="124" cy="232" rx="36" ry="7" fill="#f58a6d" opacity=".55"/>')}
{g("to", ';--r:8deg;transform:none', '<ellipse cx="204" cy="228" rx="52" ry="12.5" fill="url(#bgt)"/><ellipse cx="204" cy="228" rx="38" ry="7.5" fill="#f58a6d" opacity=".55"/>').replace(f"--d:{D['to']}s", f"--d:{D['to'] + .12:.2f}s")}
{g("to", ';--r:20deg', '<ellipse cx="282" cy="232" rx="50" ry="12" fill="url(#bgt)"/><ellipse cx="282" cy="232" rx="36" ry="7" fill="#f58a6d" opacity=".55"/>').replace(f"--d:{D['to']}s", f"--d:{D['to'] + .24:.2f}s")}
{g("oi", body='<g fill="none" stroke="#b64a8c" stroke-width="3" stroke-linecap="round"><ellipse cx="150" cy="216" rx="30" ry="6"/><ellipse cx="232" cy="215" rx="34" ry="6.5"/><ellipse cx="288" cy="219" rx="22" ry="5"/></g>')}
{g("ph", body='<path d="M64 214q0-84 136-84t136 84q0 14-16 14H80q-16 0-16-14z" fill="url(#bgp)"/><path d="M96 168q40-32 110-30" stroke="#f6cf92" stroke-width="6" fill="none" stroke-linecap="round" opacity=".5"/>')}
{seeds}
</g>
</svg>'''

def html():
    lis = "".join(f'<li style="--d:{d}s"><i>✓</i>{t}</li>' for _, t, d in ETAPES)
    return f'''<section class="burger-sec" id="burger"><div class="w bsec" id="bsec"><div class="copy"><p class="eb">Notre signature</p><h2>Le Burger du Marché</h2><p>Un burger monté minute, avec des produits des producteurs voisins. Regardez-le se composer, couche après couche.</p><ul>{lis}</ul><div class="px"><b>16 €</b><a class="btn" href="/exemples/bistro-reservation-client">Réserver une table</a><button type="button" class="rj" id="rejouer">Rejouer ↻</button></div></div><div class="burger" id="burger-fx">{_svg()}</div></div></section>
'''

JS = '''<script>(function(){var b=document.getElementById('burger-fx'),s=document.getElementById('bsec');if(!b||!s)return;
var calm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;if(calm||!('IntersectionObserver' in window))return;
function play(){b.classList.remove('go');s.classList.remove('go');void b.offsetWidth;b.classList.add('go');s.classList.add('go')}
b.classList.add('arm');s.classList.add('arm');
new IntersectionObserver(function(es,o){es.forEach(function(e){if(e.isIntersecting){o.disconnect();play()}})},{threshold:.45}).observe(b);
var r=document.getElementById('rejouer');if(r)r.addEventListener('click',play)})()</script>'''
