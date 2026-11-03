# -*- coding: utf-8 -*-
"""Système de réservation du site d'exemple « Le Bistro du Marché » :
 - espace réservation CLIENT  (site/exemples/bistro-reservation-client.html)
 - espace réservation INTERNE (site/exemples/bistro-reservation-interne.html)
Les deux pages partagent les mêmes données (réservations déjà prises + celles faites pendant la visite,
mémorisées dans le navigateur) : une réservation faite côté client apparaît tout de suite côté interne."""

FONTS = "family=DM+Sans:wght@400;500;700&family=Playfair+Display:wght@600;700"

# ---------- icônes (traits) ----------
ICONS = {
    "cal": "M7 3v3M17 3v3M4 8h16M5 5h14a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1z",
    "users": "M16 20v-1.5a3.5 3.5 0 0 0-3.5-3.5h-5A3.5 3.5 0 0 0 4 18.5V20M10 12a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zM20 20v-1.5a3.5 3.5 0 0 0-2.5-3.3M15.5 5.2a3.5 3.5 0 0 1 0 6.6",
    "user": "M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM5 21v-1a5 5 0 0 1 5-5h4a5 5 0 0 1 5 5v1",
    "table": "M4 10h16M6 10v9M18 10v9M5 10V6.5C5 5.7 5.7 5 6.5 5h11c.8 0 1.5.7 1.5 1.5V10",
    "euro": "M17 7.5A6 6 0 1 0 17 16.5M5 10.5h8M5 13.5h8",
    "home": "M3 11l9-8 9 8M5 10v10h5v-6h4v6h5V10",
    "fork": "M7 3v7a2 2 0 0 0 2 2v9M7 3v5M11 3v5M9 3v9M17 3c-2 2-2.500 5-2.500 8h2.500v10",
    "book": "M12 6c-2-1.500-5-2-8-2v14c3 0 6 .5 8 2 2-1.500 5-2 8-2V4c-3 0-6 .5-8 2zM12 6v14",
    "chart": "M5 20V10M12 20V4M19 20v-7",
    "gear": "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM19.400 15a1.700 1.700 0 0 0 .3 1.800l.1.1a2 2 0 1 1-2.800 2.800l-.1-.1a1.700 1.700 0 0 0-1.800-.3 1.700 1.700 0 0 0-1 1.500V21a2 2 0 1 1-4 0v-.1a1.700 1.700 0 0 0-1.100-1.500 1.700 1.700 0 0 0-1.800.3l-.1.1a2 2 0 1 1-2.800-2.800l.1-.1a1.700 1.700 0 0 0 .3-1.800 1.700 1.700 0 0 0-1.500-1H3a2 2 0 1 1 0-4h.1a1.700 1.700 0 0 0 1.500-1.100 1.700 1.700 0 0 0-.3-1.800l-.1-.1a2 2 0 1 1 2.800-2.800l.1.1a1.700 1.700 0 0 0 1.800.3H9a1.700 1.700 0 0 0 1-1.500V3a2 2 0 1 1 4 0v.1a1.700 1.700 0 0 0 1 1.500 1.700 1.700 0 0 0 1.800-.3l.1-.1a2 2 0 1 1 2.800 2.800l-.1.1a1.700 1.700 0 0 0-.3 1.800V9a1.700 1.700 0 0 0 1.500 1H21a2 2 0 1 1 0 4h-.1a1.700 1.700 0 0 0-1.500 1z",
    "cake": "M4 20h16v-7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2zM4 16c2 1.500 3 1.500 4 0s2-1.500 4 0 3 1.500 4 0 2-1.500 4 0M12 11V7M12 7c-1 0-1.500-1-1.500-1.800S12 3 12 3s1.500 1.400 1.500 2.200S13 7 12 7z",
    "bell": "M6 16V11a6 6 0 1 1 12 0v5l1.500 2h-15zM10 21h4",
    "dl": "M12 4v11M7.500 11 12 15.500 16.500 11M5 20h14",
    "list": "M8 6h12M8 12h12M8 18h12M4 6h.01M4 12h.01M4 18h.01",
    "plus": "M12 5v14M5 12h14",
    "left": "M15 5l-7 7 7 7",
    "right": "M9 5l7 7-7 7",
    "down": "M6 9l6 6 6-6",
    "check": "M5 12.500l4.500 4.500L19 7.500",
    "sun": "M12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM12 2v2M12 20v2M4.900 4.900l1.400 1.400M17.700 17.700l1.400 1.400M2 12h2M20 12h2M4.900 19.100l1.400-1.400M17.700 6.300l1.400-1.400",
    "moon": "M20 14.500A8 8 0 1 1 9.500 4a6.500 6.500 0 0 0 10.500 10.500z",
    "chef": "M7 14.500A4 4 0 1 1 9 7a4 4 0 0 1 6 0 4 4 0 1 1 2 7.500V19H7zM7 17h10",
    "group": "M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM15.500 11a2.500 2.500 0 1 0 0-5M3 20v-1a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v1M17 15a4 4 0 0 1 4 4v1",
    "mail": "M4 6h16v12H4zM4 7l8 6 8-6",
    "phone": "M5 4h4l2 5-2.500 1.500a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z",
    "x": "M6 6l12 12M18 6 6 18",
}


def ic(name, size=20, sw=1.8):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{ICONS[name]}"/></svg>')


# ---------- noyau de données partagé (JavaScript) ----------
CORE = r"""
var CAP=48,TABLES=12,KEY='bistro-demo-resa-v1';
var MOIS=['janv.','févr.','mars','avr.','mai','juin','juil.','août','sept.','oct.','nov.','déc.'];
var JOURS=['dim.','lun.','mar.','mer.','jeu.','ven.','sam.'];
function pad(n){return n<10?'0'+n:''+n}
function iso(d){return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate())}
function parse(s){var p=s.split('-');return new Date(+p[0],+p[1]-1,+p[2],12)}
function hash(s){var h=0;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return Math.abs(h)}
function mins(t){var p=t.split(':');return (+p[0])*60+(+p[1])}
function hm(t){return t.replace(':',' h ').replace(' h 00',' h')}
function cap1(s){return s.charAt(0).toUpperCase()+s.slice(1)}
function label(s){var d=parse(s);return cap1(JOURS[d.getDay()])+' '+d.getDate()+' '+MOIS[d.getMonth()]+' '+d.getFullYear()}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
var TODAY=iso(new Date());
var SHOW=(function(){if('2026-11-07'>=TODAY)return '2026-11-07';var d=new Date();d.setHours(12);while(d.getDay()!==6)d.setDate(d.getDate()+1);return iso(d)})();
function openDay(s){return parse(s).getDay()!==1}
var MIDI=['12:00','12:30','13:00','13:30','14:00'],SOIR=['19:00','19:30','20:00','20:30','21:00'];
function service(t){return mins(t)<16*60?'midi':'soir'}
/* Jour de démonstration : exactement les réservations de la capture (19 résas, 76 couverts) */
var SHOWDATA=[
['12:00',4,'M. Laurent','table'],['12:00',2,'Mme Garcia','table'],['12:30',2,'Mme Martin','table'],['12:30',2,'M. Roux','table'],
['13:00',6,'Groupe Dubois','group'],['13:30',8,'Anniversaire','event'],
['19:00',2,'M. Petit','table'],['19:00',2,'Mme Lopez','table'],['19:00',2,'M. Girard','table'],
['19:30',4,'Mme Leroy','table'],['19:30',4,'Famille Noël','table'],
['20:00',6,'M. Moreau','group'],['20:00',2,'M. Faure','table'],['20:00',4,'Mme Blanc','table'],
['20:30',10,'Repas d’équipe','event'],['20:30',2,'Mme Henry','table'],
['21:00',4,'M. Perrin','table'],['21:00',6,'Mme Dupuis','group'],['21:30',4,'Mme Bernard','table']];
var NOMS=['M. Bernard','Mme Roche','M. Fabre','Mme Colin','M. Lemaire','Mme Vidal','M. Morel','Mme Simon','M. Aubert','Mme Chevalier','M. Gauthier','Mme Marchand'];
var TAILLES=[2,2,2,3,4,4,5,6];
function seeded(s){
  var out=[],i;
  if(s===SHOW){SHOWDATA.forEach(function(r,k){out.push({id:'s'+k,iso:s,t:r[0],n:r[1],nom:r[2],kind:r[3]})});return out}
  if(!openDay(s))return out;
  var h=hash(s),svc=[['midi',MIDI,3+h%4]];
  if(parse(s).getDay()!==0)svc.push(['soir',SOIR.concat(['21:30']),5+(h>>3)%6]);
  svc.forEach(function(v){for(i=0;i<v[2];i++){var g=hash(s+v[0]+i);out.push({id:'g'+s+v[0]+i,iso:s,t:v[1][g%v[1].length],n:TAILLES[(g>>4)%TAILLES.length],nom:NOMS[(g>>7)%NOMS.length],kind:'table'})}});
  return out;
}
function store(){try{var o=JSON.parse(localStorage.getItem(KEY));if(o&&o.res)return o}catch(e){}return{res:[],del:[]}}
function save(o){try{localStorage.setItem(KEY,JSON.stringify(o))}catch(e){}}
function all(s){var st=store();return seeded(s).concat(st.res.filter(function(r){return r.iso===s})).filter(function(r){return st.del.indexOf(r.id)<0}).sort(function(a,b){return mins(a.t)-mins(b.t)})}
function around(list,t){var c=0;list.forEach(function(r){if(Math.abs(mins(r.t)-mins(t))<60)c+=r.n});return c}
function isOpen(s,t,n){
  if(!openDay(s)||s<TODAY)return false;
  if(parse(s).getDay()===0&&service(t)==='soir')return false;
  if(s===SHOW&&(t==='13:00'||t==='13:30'))return false;
  if(s!==SHOW&&hash(s+t)%6===0)return false;
  return around(all(s),t)+n<=CAP;
}
"""

# ---------- gabarit commun ----------
BASE_CSS = r"""
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font:400 15px/1.5 'DM Sans',system-ui,sans-serif;color:#2a1519;background:#f8f1ee}
h1,h2,h3,p,ul{margin:0;padding:0}ul{list-style:none}button{font:inherit;color:inherit;cursor:pointer}a{color:inherit;text-decoration:none}
.serif{font-family:'Playfair Display',Georgia,serif}
.swbar{position:sticky;top:0;z-index:60;display:flex;gap:10px;align-items:center;justify-content:center;flex-wrap:wrap;background:#1c0d10;color:#fff;font:500 13px/1.3 system-ui,sans-serif;padding:9px 14px}
.swbar b{font-weight:700}.swbar a{padding:7px 14px;border-radius:99px;box-shadow:inset 0 0 0 1.5px #ffffff55;font-weight:700}.swbar a.on{background:#fff;color:#4a1219;box-shadow:none}.swbar a.bk{box-shadow:none;opacity:.8}
.demo-bar{position:sticky;bottom:0;z-index:50;margin-top:30px;background:#111;color:#fff;font:500 12.5px/1.3 system-ui,sans-serif;padding:9px 14px;display:flex;gap:12px;justify-content:space-between;flex-wrap:wrap}
.toast{position:fixed;left:50%;bottom:64px;transform:translateX(-50%);background:#1c0d10;color:#fff;padding:12px 18px;border-radius:12px;font-size:14px;z-index:90;box-shadow:0 10px 30px #0005;opacity:0;pointer-events:none;transition:opacity .2s;max-width:90vw}.toast.on{opacity:1}
"""

BAR = """<div class="swbar"><b>Démonstration · Le Bistro du Marché</b><a href="/exemples/bistro-reservation-client" class="%(c)s">Espace réservation client</a><a href="/exemples/bistro-reservation-interne" class="%(i)s">Espace réservation interne</a><a href="/exemples/bistro" class="bk">← Site du restaurant</a></div>"""
FOOT = """<div class="demo-bar"><span>Exemple réalisé par Devanture Web · noms, chiffres et réservations fictifs · les réservations faites ici restent dans votre navigateur</span><a href="/#avant" target="_top">← Retour à l’offre</a></div><div class="toast" id="toast" role="status"></div>"""


def shell(title, css, body, js, c="", i=""):
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="Démonstration du système de réservation du Bistro du Marché (exemple fictif)."><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS}&display=swap">
<style>{BASE_CSS}{css}</style></head><body>
{BAR % dict(c=c, i=i)}
{body}
{FOOT}
<script>(function(){{{CORE}
var tt;function toast(m){{var t=document.getElementById('toast');t.textContent=m;t.classList.add('on');clearTimeout(tt);tt=setTimeout(function(){{t.classList.remove('on')}},2600)}}
{js}
}})();</script></body></html>"""


# =====================================================================
#  ESPACE RÉSERVATION CLIENT
# =====================================================================
CLIENT_CSS = r"""
body{background:radial-gradient(1200px 500px at 50% -10%,#f1dcd6,transparent),#f8f1ee}
.wrap{max-width:660px;margin:26px auto 0;padding:0 14px}
.card{background:#fff;border-radius:26px;box-shadow:0 24px 60px #4a121933,0 2px 0 #fff inset;overflow:hidden}
.hd{position:relative;height:170px;background:#4a1219;color:#fff;display:flex;align-items:center;gap:22px;padding:0 34px}
.hd svg.bg{position:absolute;inset:0;width:100%;height:100%;opacity:.55;object-fit:cover}.hd:before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#4a1219f2 15%,#4a121966 100%);z-index:1}
.hd>*{position:relative;z-index:2}.hd .chef{color:#fff;flex:none}.hd h1{font:700 clamp(1.5rem,5vw,2.1rem)/1.1 'Playfair Display',serif}.hd p{opacity:.9;margin-top:6px}
.body{padding:22px 26px 28px;margin-top:-16px;background:#fff;border-radius:26px 26px 0 0;position:relative;z-index:3}
.steps{display:flex;align-items:center;gap:6px;padding-bottom:18px;border-bottom:1px solid #f1e4e0;margin-bottom:20px;overflow-x:auto}
.st{display:flex;align-items:center;gap:8px;white-space:nowrap;font-weight:600;font-size:14px;color:#2a1519}.st i{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;border:1.5px solid #e4c9c5;font:600 15px 'DM Sans',system-ui,sans-serif;font-style:normal;color:#6b1f2b;background:#fff;flex:none}
.st.on i,.st.done i{background:#6b1f2b;color:#fff;border-color:#6b1f2b}.st:not(.on):not(.done){font-weight:500;color:#4d3a3c}.st.sep{flex:1;min-width:14px;height:1px;background:#e8d5d1}
h2.q{font:700 1.7rem 'Playfair Display',serif;margin:6px 0 14px}
.types{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
.ty{position:relative;border:1.5px solid #eadbd7;background:#fff;border-radius:16px;padding:18px 10px;text-align:center;display:grid;gap:8px;justify-items:center;align-content:center;min-height:128px;box-shadow:0 2px 8px #4a121912}
.ty b{font:600 1.05rem/1.2 'Playfair Display',serif}.ty small{font-size:13px;color:#5a4648}.ty svg{color:#2a1519}
.ty .ck svg{color:#fff}.ty.on{background:#f8ecec;border-color:#8a3340}.ty.on svg{color:#6b1f2b}.ty .ck{display:none;position:absolute;top:10px;right:10px;width:28px;height:28px;border-radius:50%;background:#6b1f2b;color:#fff;place-items:center}.ty.on .ck{display:grid}
.row2{display:grid;grid-template-columns:1fr 1.15fr;gap:14px;margin-top:16px}
.box{border:1px solid #f1e4e0;border-radius:16px;padding:14px 16px;background:#fffdfc}.box h3{font:700 1.15rem 'Playfair Display',serif;margin-bottom:8px}
.stepper{display:flex;align-items:center;gap:8px;border:1px solid #eadbd7;border-radius:14px;padding:6px 8px;background:#fff;box-shadow:0 2px 8px #4a121910}
.stepper>svg{color:#2a1519;margin:0 6px 0 4px}.stepper b{flex:1;text-align:center;font-size:1.35rem;font-weight:600}
.stepper button{width:40px;height:40px;border-radius:50%;border:1px solid #e4c9c5;background:#fff;font-size:20px;line-height:1}.stepper button:disabled{opacity:.35;cursor:not-allowed}
.sel{position:relative}.sel select{appearance:none;width:100%;border:1px solid #eadbd7;border-radius:14px;padding:13px 40px 13px 46px;font:600 15px 'DM Sans',system-ui,sans-serif;background:#fff;color:#2a1519;box-shadow:0 2px 8px #4a121910;height:54px}
.sel>svg{position:absolute;left:14px;top:50%;transform:translateY(-50%);pointer-events:none}.sel>svg.r{left:auto;right:14px}
.seg{display:grid;grid-template-columns:1fr 1fr;background:#f1ecec;border-radius:99px;padding:3px;margin:10px 0 14px}.seg button{border:0;background:transparent;border-radius:99px;padding:11px;font-weight:700;color:#3a2a2c}.seg button.on{background:#6b1f2b;color:#fff}.seg button:disabled{opacity:.4;cursor:not-allowed}
.times{display:grid;grid-template-columns:repeat(5,1fr);gap:9px}.times button{border:1px solid #eadbd7;background:#fff;border-radius:13px;padding:13px 0;font-weight:700;font-size:15px;box-shadow:0 2px 8px #4a121910}
.times button.on{background:#6b1f2b;color:#fff;border-color:#6b1f2b}.times button:disabled{text-decoration:line-through;color:#a99a9b;border-style:dashed;box-shadow:none;background:#faf6f5;cursor:not-allowed}
.hint{font-size:13px;color:#6a5557;margin-top:10px;display:flex;gap:6px;align-items:center}.hint s{color:#a99a9b}
.go{display:flex;align-items:center;justify-content:center;gap:10px;width:100%;margin-top:20px;border:0;border-radius:99px;background:#5b1823;color:#fff;font:700 1.15rem 'DM Sans',system-ui,sans-serif;padding:18px;box-shadow:0 10px 24px #4a121955}.go:disabled{opacity:.45;cursor:not-allowed}
.link{background:none;border:0;color:#6b1f2b;font-weight:700;padding:10px;margin-top:6px;width:100%}
.f{display:grid;gap:12px}.f label{font-weight:700;font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:#6a5557;display:grid;gap:6px}
.f input,.f textarea{font:500 16px 'DM Sans',system-ui,sans-serif;border:1px solid #e4d2ce;border-radius:13px;padding:13px 14px;background:#fff;color:#2a1519;width:100%;text-transform:none;letter-spacing:0}.f textarea{min-height:84px}
.err{color:#b3261e;font-size:13.5px;min-height:18px;margin-top:6px}
.recap{background:#f8ecec;border-radius:16px;padding:14px 16px;margin-bottom:14px;display:flex;gap:10px 22px;flex-wrap:wrap;font-weight:600}.recap span{display:flex;gap:7px;align-items:center}
.okk{text-align:center;padding:10px 0 4px}.okk .big{width:74px;height:74px;border-radius:50%;background:#6b1f2b;color:#fff;display:grid;place-items:center;margin:4px auto 14px}
.okk h2{font:700 1.8rem 'Playfair Display',serif}.okk .ref{display:inline-block;margin:12px 0;font:700 1.15rem monospace;background:#f8ecec;padding:8px 14px;border-radius:10px;letter-spacing:.06em}
.okk p{color:#4d3a3c;max-width:440px;margin:6px auto}.okk .acts{display:grid;gap:10px;margin-top:18px}
.okk .acts a{display:block;border-radius:99px;padding:15px;font-weight:700}.okk .acts a.p{background:#5b1823;color:#fff}.okk .acts a.s{box-shadow:inset 0 0 0 1.5px #c9a5a5;color:#6b1f2b}
.note{margin:16px auto 0;max-width:620px;font-size:13.5px;color:#6a5557;text-align:center;padding:0 14px}
@media(max-width:560px){.types{grid-template-columns:1fr}.ty{min-height:0;grid-template-columns:auto 1fr;justify-items:start;text-align:left;padding:14px 16px}.row2{grid-template-columns:1fr}.times{grid-template-columns:repeat(3,1fr)}.body{padding:18px 16px 24px}.hd{padding:0 20px}.st span{display:none}.st.on span{display:inline}}
"""

CLIENT_BODY = """
<div class="wrap"><div class="card">
<div class="hd">%(bg)s<span class="chef">%(chef)s</span><div><h1>Le Bistro du Marché</h1><p>Restaurant · Cuisine de saison</p></div></div>
<div class="body">
<div class="steps" id="steps"></div>

<section id="s1">
<h2 class="q">Type de réservation</h2>
<div class="types" id="types">
 <button type="button" class="ty on" data-k="table">%(fork)s<b>Table au restaurant</b><span class="ck">%(check)s</span></button>
 <button type="button" class="ty" data-k="group">%(group)s<b>Groupe / Événement</b><small>(8 à 40 pers.)</small><span class="ck">%(check)s</span></button>
 <button type="button" class="ty" data-k="event">%(cake)s<b>Événement privé</b><small>(anniversaire, repas pro…)</small><span class="ck">%(check)s</span></button>
</div>
<div class="row2">
 <div class="box"><h3>Nombre de convives</h3><div class="stepper">%(user)s<button type="button" id="minus" aria-label="Moins de convives">−</button><b id="nb" aria-live="polite">4</b><button type="button" id="plus" aria-label="Plus de convives">+</button></div></div>
 <div class="box"><h3>Date</h3><div class="sel">%(cal)s<select id="date" aria-label="Date"></select>%(down)s</div></div>
</div>
<h2 class="q" style="margin-top:22px;font-size:1.4rem">Choisissez un horaire</h2>
<div class="seg" role="tablist"><button type="button" id="b-midi">Midi</button><button type="button" id="b-soir" class="on">Soir</button></div>
<div class="times" id="times"></div>
<p class="hint">%(info)s <span id="hint">Les horaires barrés sont déjà complets.</span></p>
<button type="button" class="go" id="next">Continuer %(arrow)s</button>
<div class="err" id="err1" role="alert"></div>
</section>

<section id="s3" hidden>
<h2 class="q">Vos coordonnées</h2>
<div class="recap" id="recap"></div>
<div class="f">
 <label>Nom et prénom<input id="nom" autocomplete="name" placeholder="Ex. : Claire Martin"></label>
 <label>Téléphone<input id="tel" type="tel" autocomplete="tel" placeholder="06 12 34 56 78"></label>
 <label>E-mail <small style="text-transform:none;letter-spacing:0;font-weight:500">(pour la confirmation)</small><input id="mail" type="email" autocomplete="email" placeholder="claire@exemple.fr"></label>
 <label>Une demande particulière ?<textarea id="msg" placeholder="Allergies, poussette, anniversaire, gâteau…"></textarea></label>
</div>
<div class="err" id="err3" role="alert"></div>
<button type="button" class="go" id="confirm">Confirmer ma réservation %(arrow)s</button>
<button type="button" class="link" id="back">← Modifier ma réservation</button>
</section>

<section id="s4" hidden class="okk">
<div class="big">%(check2)s</div>
<h2>Réservation confirmée</h2>
<div class="ref" id="ref"></div>
<p id="sum"></p>
<p>Un e-mail de confirmation vous est envoyé, avec un rappel la veille. Vous pouvez modifier ou annuler jusqu’à 2 h avant.</p>
<div class="acts"><a class="p" id="toInt" href="/exemples/bistro-reservation-interne">Voir cette réservation côté restaurant (espace interne) →</a><a class="s" href="/exemples/bistro-reservation-client" id="again">Faire une autre réservation</a></div>
</section>
</div></div>
<p class="note">Démonstration : les créneaux déjà pris sont ceux de l’agenda du restaurant. Votre réservation apparaîtra dans l’espace interne, et le créneau se remplit.</p>
</div>
"""

CLIENT_JS = r"""
var $=function(s){return document.querySelector(s)};
var S={k:'table',n:4,date:SHOW,svc:'soir',t:'20:00'};
var LIM={table:[1,8],group:[8,40],event:[6,40]};
var NAMES={table:'Table au restaurant',group:'Groupe / Événement',event:'Événement privé'};
function steps(a){var L=['Réservation','Date & convives','Vos infos','Confirmation'],h='';L.forEach(function(l,i){var c=i+1===a?' on':(i+1<a?' done':'');h+=(i?'<span class="st sep"></span>':'')+'<span class="st'+c+'"><i>'+(i+1)+'</i><span>'+l+'</span></span>'});$('#steps').innerHTML=h}
function fillDates(){var h='',d=new Date();d.setHours(12);for(var i=0;i<60;i++){var s=iso(d);if(openDay(s))h+='<option value="'+s+'"'+(s===S.date?' selected':'')+'>'+label(s)+'</option>';d.setDate(d.getDate()+1)}$('#date').innerHTML=h}
function draw(){
  $('#nb').textContent=S.n;var lim=LIM[S.k];$('#minus').disabled=S.n<=lim[0];$('#plus').disabled=S.n>=lim[1];
  Array.prototype.forEach.call(document.querySelectorAll('.ty'),function(b){b.classList.toggle('on',b.dataset.k===S.k)});
  var sun=parse(S.date).getDay()===0;if(sun&&S.svc==='soir')S.svc='midi';
  $('#b-soir').disabled=sun;$('#b-midi').classList.toggle('on',S.svc==='midi');$('#b-soir').classList.toggle('on',S.svc==='soir');
  var list=S.svc==='midi'?MIDI:SOIR,h='',any=false;
  list.forEach(function(t){var o=isOpen(S.date,t,S.n);if(o)any=true;h+='<button type="button" data-t="'+t+'"'+(o?'':' disabled')+(S.t===t&&o?' class="on"':'')+'>'+t+'</button>'});
  $('#times').innerHTML=h;
  if(S.t&&!isOpen(S.date,S.t,S.n)||list.indexOf(S.t)<0)S.t=null;
  if(S.t)Array.prototype.forEach.call(document.querySelectorAll('#times button'),function(b){b.classList.toggle('on',b.dataset.t===S.t)});
  $('#hint').textContent=any?'Les horaires barrés sont déjà complets.':'Plus de table à ce service : essayez l’autre service ou un autre jour.';
  $('#err1').textContent='';
}
$('#types').onclick=function(e){var b=e.target.closest('.ty');if(!b)return;S.k=b.dataset.k;var l=LIM[S.k];S.n=Math.min(Math.max(S.n,l[0]),l[1]);if(S.k!=='table'&&S.n<l[0])S.n=l[0];draw()};
$('#minus').onclick=function(){S.n--;draw()};$('#plus').onclick=function(){S.n++;draw()};
$('#date').onchange=function(){S.date=this.value;draw()};
$('#b-midi').onclick=function(){S.svc='midi';S.t=null;draw()};$('#b-soir').onclick=function(){S.svc='soir';S.t=null;draw()};
$('#times').onclick=function(e){var b=e.target.closest('button');if(!b||b.disabled)return;S.t=b.dataset.t;draw()};
$('#next').onclick=function(){if(!S.t){$('#err1').textContent='Choisissez un horaire disponible.';return}
  $('#recap').innerHTML='<span>'+'📅 '+label(S.date)+'</span><span>🕗 '+hm(S.t)+'</span><span>👥 '+S.n+' convive'+(S.n>1?'s':'')+'</span><span>🍽 '+NAMES[S.k]+'</span>';
  $('#s1').hidden=true;$('#s3').hidden=false;steps(3);window.scrollTo({top:0,behavior:'smooth'})};
$('#back').onclick=function(){$('#s3').hidden=true;$('#s1').hidden=false;steps(1)};
$('#confirm').onclick=function(){
  var nom=$('#nom').value.trim(),tel=$('#tel').value.trim(),mail=$('#mail').value.trim(),e=$('#err3');
  if(nom.length<2){e.textContent='Indiquez votre nom.';return}
  if(tel.replace(/\D/g,'').length<8){e.textContent='Indiquez un numéro de téléphone valide.';return}
  if(mail&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail)){e.textContent='Cette adresse e-mail ne semble pas valide.';return}
  if(!isOpen(S.date,S.t,S.n)){e.textContent='Ce créneau vient d’être pris. Choisissez-en un autre.';return}
  var ref='RDV-'+Math.random().toString(36).slice(2,8).toUpperCase(),st=store(),id='u'+Date.now();
  st.res.push({id:id,iso:S.date,t:S.t,n:S.n,nom:nom,tel:tel,mail:mail,msg:$('#msg').value.trim(),kind:S.k,ref:ref,web:1});save(st);
  $('#ref').textContent=ref;$('#sum').innerHTML='<b>'+esc(label(S.date))+' à '+hm(S.t)+'</b> · '+S.n+' convive'+(S.n>1?'s':'')+' · '+NAMES[S.k]+'<br>Merci '+esc(nom)+', votre table est réservée.';
  $('#toInt').href='/exemples/bistro-reservation-interne?d='+S.date+'&n='+id;
  $('#s3').hidden=true;$('#s4').hidden=false;steps(4);window.scrollTo({top:0,behavior:'smooth'});e.textContent=''};
fillDates();steps(1);draw();
"""


def client():
    body = CLIENT_BODY % dict(
        bg=open("tools/src/bistro-scene.svg").read().replace("<svg ", '<svg class="bg" ', 1),
        chef=ic("chef", 76, 1.6), fork=ic("fork", 42, 2), group=ic("group", 40, 1.8), cake=ic("cake", 40, 1.8),
        check=ic("check", 16, 3), check2=ic("check", 38, 3), user=ic("user", 22), cal=ic("cal", 22), down=ic("down", 20),
        info=ic("bell", 16), arrow=ic("right", 22, 2.4))
    return shell("Réserver une table · Le Bistro du Marché", CLIENT_CSS, body, CLIENT_JS, c="on")


# =====================================================================
#  ESPACE RÉSERVATION INTERNE
# =====================================================================
INT_CSS = r"""
body{background:#f7f1ee}
.app{display:grid;grid-template-columns:268px minmax(0,1fr);min-height:calc(100vh - 40px)}
aside{background:linear-gradient(180deg,#6a1c2a,#4e1220 70%,#431019);color:#fff;padding:24px 14px;display:flex;flex-direction:column;gap:6px;position:sticky;top:38px;height:calc(100vh - 38px);align-self:start}
.brand{display:flex;gap:14px;align-items:center;padding:0 8px 22px}.brand b{font:700 1.35rem/1.15 'Playfair Display',serif;display:block}.brand small{opacity:.8;font-size:14px}
.nv{display:flex;gap:16px;align-items:center;padding:14px 18px;border-radius:12px;border:0;background:transparent;color:#fff;text-align:left;font-size:16px;width:100%;opacity:.95}.nv:hover{background:#ffffff14}.nv.on{background:#8a3340;font-weight:700}
.cap{margin-top:auto;border:1px solid #ffffff33;border-radius:16px;padding:16px;display:grid;gap:9px;font-size:15px}.cap b{font-size:15px}.cap span{display:flex;gap:12px;align-items:center}
main{padding:22px 26px 10px;min-width:0}
.top{display:flex;gap:16px;align-items:center;margin-bottom:18px;flex-wrap:wrap}.top .ic{color:#4e1220}.top h1{font:700 2.3rem/1.1 'Playfair Display',serif;color:#2a1519}.top p{color:#4d3a3c;margin-top:2px}.top .sp{flex:1}
.pill{display:flex;align-items:center;gap:8px;border:1px solid #eadbd7;background:#fff;border-radius:99px;padding:11px 18px;font-weight:600;box-shadow:0 2px 8px #4a121912}
.bell{position:relative;width:52px;height:52px;border-radius:50%;border:1px solid #eadbd7;background:#fff;display:grid;place-items:center}.bell i{position:absolute;top:-4px;right:-4px;background:#c4222e;color:#fff;border-radius:99px;font:700 11px/1 'DM Sans',system-ui,sans-serif;font-style:normal;padding:4px 6px}
.me{width:56px;height:56px;border-radius:50%;border:1px solid #eadbd7;background:#fff;display:grid;place-items:center}
.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.kpi{background:#fff;border-radius:18px;padding:18px;display:flex;gap:14px;align-items:center;box-shadow:0 4px 18px #4a12190d}
.kpi .ico{width:62px;height:62px;border-radius:50%;background:#f4e2e1;color:#6a1c2a;display:grid;place-items:center;flex:none}
.kpi small{color:#4d3a3c;font-size:14px;display:block}.kpi b{font-size:1.4rem;font-weight:700;display:block;line-height:1.25}.kpi .d{display:inline-flex;gap:5px;align-items:center;background:#dcf5e3;color:#1c7c3a;font-weight:700;font-size:13px;border-radius:8px;padding:3px 9px;margin-top:4px}
.bar{height:9px;background:#efe4e2;border-radius:99px;margin-top:8px;width:150px;display:inline-block;vertical-align:middle}.bar i{display:block;height:100%;background:#7a1f2e;border-radius:99px}
.panel{background:#fff;border-radius:20px;padding:16px;box-shadow:0 4px 18px #4a12190d;margin-top:16px}
.tb{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:14px}
.tabs{display:flex;background:#fff;border:1px solid #eadbd7;border-radius:14px;padding:3px;box-shadow:0 2px 8px #4a121912}.tabs button{border:0;background:transparent;border-radius:11px;padding:11px 18px;font-weight:600;display:flex;gap:9px;align-items:center}.tabs button.on{background:#5b1823;color:#fff}
.dnav{display:flex;gap:10px;align-items:center;margin-left:auto}.dnav button.arrow{width:48px;height:48px;border-radius:14px;border:1px solid #eadbd7;background:#fff;display:grid;place-items:center}
.dnav .pill{border-radius:14px;font-weight:700;min-width:190px;justify-content:center}
.new{border:0;background:#5b1823;color:#fff;border-radius:16px;padding:16px 24px;font-weight:700;display:flex;gap:10px;align-items:center;box-shadow:0 8px 20px #4a121944}
.cols{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:16px}
.svc{display:flex;align-items:center;gap:10px;background:#faf0ec;border-radius:12px;padding:11px 16px;font-weight:700;margin-bottom:6px}.svc svg{color:#d58a1a}.svc.s2 svg{color:#4e1220}.svc small{font-weight:500;color:#4d3a3c}
.grid{position:relative;margin:6px 0 16px;border-left:0}
.hr{position:absolute;left:0;right:0;height:34px;border-top:1px solid #f0e6e3;font-size:14.500px;color:#2a1519}.hr span{position:absolute;left:0;top:-11px;background:#fff;padding-right:8px}
.blk{position:absolute;height:31px;border-radius:7px;padding:5px 10px;font-size:14px;font-weight:600;display:flex;gap:7px;align-items:flex-start;overflow:hidden;cursor:pointer;border-left:4px solid;box-shadow:0 3px 8px #4a121918;white-space:nowrap;text-overflow:ellipsis}
.blk svg{flex:none;margin-top:2px}.blk .ck{margin-left:auto;flex:none}.blk.new{outline:3px solid #7a1f2e}
.c0{background:#dff3e0;border-color:#4caf50}.c1{background:#dbeefb;border-color:#42a5f5}.c2{background:#fde2e1;border-color:#ef6f6c}.c3{background:#ece0fa;border-color:#8e5bd8}
.list h3{display:flex;gap:10px;align-items:center;font:700 1.15rem 'DM Sans',system-ui,sans-serif;margin:6px 4px 10px}.list h3 span.cnt{background:#5b1823;color:#fff;border-radius:99px;font-size:12px;padding:3px 9px}
.rows{max-height:372px;overflow:auto;padding-right:4px}.lr{display:grid;grid-template-columns:50px 80px 1fr auto 22px;gap:8px;align-items:center;padding:10px 6px;border-top:1px solid #f4ecea;font-size:14.500px;width:100%;background:none;border-left:0;border-right:0;border-bottom:0;text-align:left}
.lr.sep{border-top:2px solid #e7d6d2;margin-top:8px}.lr.new{background:#fbeeee}
.ok{background:#dcf5e3;color:#1c7c3a;font-weight:700;font-size:13px;border-radius:99px;padding:4px 14px;text-align:center}.ok.web{background:#ffe9c7;color:#8a5a00}
.stats3{display:grid;grid-template-columns:repeat(3,1fr);margin-top:16px;text-align:center}.stats3>div{padding:8px;border-left:1px solid #f0e6e3}.stats3>div:first-child{border:0}.stats3 svg{color:#6a1c2a}.stats3 b{display:block;font:600 2rem 'Playfair Display',serif}.stats3 small{color:#4d3a3c}
table{width:100%;border-collapse:collapse}th{text-align:left;font-size:12.5px;text-transform:uppercase;letter-spacing:.06em;color:#6a5557;padding:8px}td{padding:11px 8px;border-top:1px solid #f4ecea}
.bars{display:grid;gap:8px}.bars div{display:grid;grid-template-columns:60px 1fr 60px;gap:10px;align-items:center;font-size:14px}.bars i{display:block;height:18px;border-radius:6px;background:linear-gradient(90deg,#8a3340,#5b1823)}
.pop{position:absolute;right:0;top:60px;width:340px;background:#fff;border-radius:16px;box-shadow:0 18px 50px #4a121955;padding:12px;z-index:30;display:none}.pop.on{display:block}.pop li{padding:10px;border-top:1px solid #f4ecea;font-size:14px}.pop li:first-child{border:0}.pop b{display:block}
.ov{position:fixed;inset:0;background:#1c0d1099;z-index:80;display:none;align-items:center;justify-content:center;padding:16px}.ov.on{display:flex}
.md{background:#fff;border-radius:20px;padding:24px;width:min(460px,100%);max-height:92vh;overflow:auto}.md h2{font:700 1.5rem 'Playfair Display',serif;margin-bottom:12px}
.md .f{display:grid;gap:10px}.md label{font-weight:700;font-size:13px;color:#6a5557;display:grid;gap:5px}.md input,.md select{font:500 16px 'DM Sans',system-ui,sans-serif;border:1px solid #e4d2ce;border-radius:11px;padding:11px 12px;width:100%}
.md .ac{display:flex;gap:10px;margin-top:16px;flex-wrap:wrap}.md .ac button{border-radius:12px;padding:12px 18px;font-weight:700;border:1.5px solid #c9a5a5;background:#fff}.md .ac button.p{background:#5b1823;color:#fff;border-color:#5b1823}.md .ac button.d{color:#b3261e;border-color:#e3b3b0}
.md dl{display:grid;grid-template-columns:110px 1fr;gap:6px 10px;margin:0}.md dt{color:#6a5557}.md dd{margin:0;font-weight:600}
@media(max-width:1250px){.kpis{grid-template-columns:1fr 1fr}.cols{grid-template-columns:1fr}}
@media(max-width:900px){.tabs{max-width:100%}.tabs button{padding:10px 11px;gap:6px;font-size:14px}.tabs button svg{display:none}.dnav{width:100%;justify-content:space-between}.dnav .pill{min-width:0;flex:1}.blk span{overflow:hidden;text-overflow:ellipsis}.app{grid-template-columns:1fr}aside{position:static;height:auto;flex-direction:row;flex-wrap:wrap;padding:12px}.brand{padding:0 8px 0 4px}.nv{width:auto;padding:9px 12px;font-size:14px}.nv svg{display:none}.cap{display:none}main{padding:16px 12px}.top h1{font-size:1.8rem}.dnav{margin-left:0}.new{width:100%;justify-content:center}.kpis{grid-template-columns:1fr}.lr{grid-template-columns:46px 70px 1fr auto}.lr>svg{display:none}}
"""

INT_BODY = """
<div class="app">
<aside>
 <div class="brand"><span style="color:#fff">%(chef)s</span><div><b>Le Bistrot<br>du Marché</b><small>Espace restaurant</small></div></div>
 <button class="nv" data-x="Tableau de bord">%(home)s Tableau de bord</button>
 <button class="nv on">%(cal)s Réservations</button>
 <button class="nv" data-v="agenda">%(cal)s Agenda</button>
 <button class="nv" data-x="Clients">%(users)s Clients</button>
 <button class="nv" data-x="Services">%(fork)s Services</button>
 <button class="nv" data-x="Menus">%(book)s Menus</button>
 <button class="nv" data-v="stats">%(chart)s Statistiques</button>
 <button class="nv" data-x="Paramètres">%(gear)s Paramètres</button>
 <div class="cap"><b>Capacité du restaurant</b><span>%(table)s <span id="capc">48 couverts</span></span><span>%(table)s <span>12 tables</span></span></div>
</aside>
<main>
 <div class="top" style="position:relative"><span class="ic">%(cal)s</span><div><h1>Réservations</h1><p>Gérez vos réservations et votre planning en toute simplicité</p></div><span class="sp"></span>
  <button class="pill" id="exp">%(dl)s Exporter</button><button class="bell" id="bell" aria-label="Notifications">%(bell)s<i id="bn">3</i></button><span class="me">%(user)s</span>
  <div class="pop" id="pop"><ul id="notifs"></ul></div></div>
 <div class="kpis" id="kpis"></div>
 <div class="panel">
  <div class="tb"><div class="tabs" id="tabs"><button data-v="agenda" class="on">%(cal)s Agenda</button><button data-v="liste">%(list)s Liste</button><button data-v="stats">%(chart)s Statistiques</button></div>
   <div class="dnav"><button class="arrow" id="prev" aria-label="Jour précédent">%(left)s</button><span class="pill" id="dlab">%(cal)s <span></span></span><button class="arrow" id="next" aria-label="Jour suivant">%(right)s</button></div>
   <button class="new" id="add">%(plus)s Nouvelle réservation</button></div>
  <div class="cols"><div id="left"></div><div><div class="list" id="list"></div><div class="stats3" id="s3"></div></div></div>
 </div>
</main></div>
<div class="ov" id="ov"><div class="md" id="md" role="dialog" aria-modal="true"></div></div>
"""

INT_JS = r"""
var $=function(s){return document.querySelector(s)};
var IC=%(icons)s;
function ic(n,s){return '<svg width="'+(s||20)+'" height="'+(s||20)+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="'+IC[n]+'"/></svg>'}
var q=new URLSearchParams(location.search),V={day:/^\d{4}-\d\d-\d\d$/.test(q.get('d')||'')?q.get('d'):SHOW,view:'agenda',hl:q.get('n')};
function nextOpen(s,dir){var d=parse(s);do{d.setDate(d.getDate()+dir)}while(!openDay(iso(d)));return iso(d)}
function sum(l){return l.reduce(function(a,r){return a+r.n},0)}
function stats(l){var cov=sum(l),tb=Math.min(TABLES,Math.round(l.length*0.53));return{res:l.length,cov:cov,tb:tb,ca:Math.round(cov*25.26/10)*10,pct:Math.round(tb/TABLES*100)}}
function kindIc(k,s){return k==='event'?ic('cake',s||20):''}
function pers(r){return r.n+' pers.'}
function rowName(r){return esc(r.nom)}
function kpis(l){var s=stats(l),h=hash(V.day),sh=V.day===SHOW,d=sh?[12,18,14]:[5+h%12,6+(h>>3)%12,4+(h>>5)%12];
  function card(i,lab,val,extra){return '<div class="kpi"><span class="ico">'+ic(i,30)+'</span><div><small>'+lab+'</small><b>'+val+'</b>'+extra+'</div></div>'}
  function dl(x,up){return '<span class="d">'+(up?'<span>↑</span>':ic('check',13))+' +'+x+' %%</span>'}
  $('#kpis').innerHTML=card('cal',V.day===TODAY||V.day===SHOW?'Aujourd’hui':'Ce jour-là',s.res+' réservations',dl(d[0],1))+
   card('users','Couverts '+(V.day===TODAY||V.day===SHOW?'aujourd’hui':'ce jour-là'),s.cov+' personnes',dl(d[1]))+
   card('table','Tables occupées',s.tb+' / '+TABLES,'<div><span class="bar"><i style="width:'+s.pct+'%%"></i></span> <small style="display:inline">'+s.pct+' %%</small></div>')+
   card('euro','CA estimé (réservations)',s.ca.toLocaleString('fr-FR')+' €',dl(d[2]));
}
function agenda(l){
  var h='';[['midi','sun',['12:00','12:30','13:00','13:30','14:00'],'Service du midi'],['soir','moon',['19:00','19:30','20:00','20:30','21:00','21:30','22:00'],'Service du soir']].forEach(function(S,si){
    var items=l.filter(function(r){return service(r.t)===S[0]});
    if(S[0]==='soir'&&parse(V.day).getDay()===0)return;
    h+='<div class="svc s'+(si+1)+'">'+ic(S[1],22)+S[3]+' <small>('+items.length+' réservation'+(items.length>1?'s':'')+' – '+sum(items)+' pers.)</small></div>';
    var RH=34,rows=S[2];
    h+='<div class="grid" style="height:'+(rows.length*RH+8)+'px">';
    rows.forEach(function(t,i){h+='<div class="hr" style="top:'+(i*RH+8)+'px"><span>'+t+'</span></div>'});
    var by={};items.forEach(function(r){(by[r.t]=by[r.t]||[]).push(r)});
    Object.keys(by).forEach(function(t){var g=by[t],i=rows.indexOf(t);if(i<0)i=Math.max(0,Math.min(rows.length-1,Math.round((mins(t)-mins(rows[0]))/30)));
      var off=(i%3)*0.17,space=1-off,w=g.length===1?Math.min(space,0.56):space/g.length-0.01;
      g.forEach(function(r,k){h+='<div class="blk c'+((i+k)%4)+(r.id===V.hl?' new':'')+'" data-id="'+r.id+'" style="top:'+(i*RH+9)+'px;left:calc(54px + (100% - 54px)*'+(off+k*(g.length===1?0:space/g.length)).toFixed(3)+');width:calc((100% - 54px)*'+w.toFixed(3)+')" title="'+esc(r.nom)+'">'+ic('users',15)+'<span>'+pers(r)+' – '+rowName(r)+'</span>'+(r.kind==='event'?'<span class="ck">'+ic('cake',18)+'</span>':'')+'</div>'})});
    h+='</div>';
  });
  return h;
}
function listRows(l){var h='',prev=null;l.forEach(function(r){var s=service(r.t);h+='<button class="lr'+(prev&&prev!==s?' sep':'')+(r.id===V.hl?' new':'')+'" data-id="'+r.id+'"><b>'+r.t+'</b><span>'+ic('users',16)+' '+pers(r)+'</span><span>'+rowName(r)+'</span><span class="ok'+(r.web?' web':'')+'">'+(r.web?'En ligne':'Confirmée')+'</span>'+ic('right',16)+'</button>';prev=s});return h||'<p style="padding:18px;color:#6a5557">Aucune réservation ce jour-là (restaurant fermé le lundi).</p>'}
function tableView(l){var h='<table><tr><th>Heure</th><th>Nom</th><th>Pers.</th><th>Type</th><th>Origine</th><th>Statut</th></tr>';l.forEach(function(r){h+='<tr data-id="'+r.id+'" style="cursor:pointer"><td><b>'+r.t+'</b></td><td>'+rowName(r)+'</td><td>'+r.n+'</td><td>'+({table:'Table',group:'Groupe',event:'Événement'}[r.kind]||'Table')+'</td><td>'+(r.web?'Site web':(r.tel?'Téléphone':'Réservation'))+'</td><td><span class="ok">Confirmée</span></td></tr>'});return h+'</table>'}
function statView(l){var slots=['12:00','12:30','13:00','13:30','14:00','19:00','19:30','20:00','20:30','21:00','21:30'],mx=1,h='<h3 class="serif" style="font-size:1.3rem;margin-bottom:10px">Couverts par créneau</h3><div class="bars">';
  var vals=slots.map(function(t){var c=0;l.forEach(function(r){if(r.t===t)c+=r.n});mx=Math.max(mx,c);return c});
  slots.forEach(function(t,i){h+='<div><span>'+t+'</span><i style="width:'+Math.max(2,vals[i]/mx*100)+'%%"></i><b>'+vals[i]+'</b></div>'});h+='</div><h3 class="serif" style="font-size:1.3rem;margin:22px 0 10px">Les 7 prochains jours ouverts</h3><div class="bars">';
  var d=V.day,rows=[];for(var i=0;i<7;i++){var L=all(d);rows.push([d,sum(L)]);d=nextOpen(d,1)}var m2=Math.max.apply(null,rows.map(function(r){return r[1]}))||1;
  rows.forEach(function(r){h+='<div><span style="font-size:12.5px">'+label(r[0]).slice(0,-5)+'</span><i style="width:'+Math.max(2,r[1]/m2*100)+'%%"></i><b>'+r[1]+'</b></div>'});return h+'</div>'}
function render(){
  var l=all(V.day),s=stats(l);
  kpis(l);$('#dlab span').textContent=label(V.day);
  $('#left').innerHTML=V.view==='agenda'?agenda(l):V.view==='liste'?tableView(l):statView(l);
  $('#list').innerHTML='<h3>'+ic('cal',22)+'Réservations du jour <span class="cnt">'+s.res+'</span></h3><div class="rows">'+listRows(l)+'</div>';
  $('#s3').innerHTML='<div>'+ic('table',40)+'<b>'+TABLES+'</b><small>Tables totales</small></div><div>'+ic('group',40)+'<b>'+s.cov+'</b><small>Personnes</small></div><div>'+ic('chart',40)+'<b>'+s.pct+' %%</b><small>Taux d’occupation</small></div>';
  Array.prototype.forEach.call(document.querySelectorAll('#tabs button'),function(b){b.classList.toggle('on',b.dataset.v===V.view)});
  var n=store().res.filter(function(r){return r.web}).length;$('#bn').textContent=3+n;
  var nf='';store().res.filter(function(r){return r.web}).slice(-3).reverse().forEach(function(r){nf+='<li><b>Nouvelle réservation en ligne</b>'+esc(r.nom)+' · '+r.n+' pers. · '+label(r.iso)+' '+r.t+'</li>'});
  nf+='<li><b>Mme Leroy a confirmé</b>Samedi, 19 h 30 · 4 personnes</li><li><b>Rappel envoyé</b>12 clients prévenus pour demain</li><li><b>Annulation</b>M. Henry · mardi 12 h 30 (table libérée)</li>';$('#notifs').innerHTML=nf;
}
function modal(h){$('#md').innerHTML=h;$('#ov').classList.add('on')}function close(){$('#ov').classList.remove('on')}
$('#ov').onclick=function(e){if(e.target===this)close()};document.addEventListener('keydown',function(e){if(e.key==='Escape')close()});
function detail(id){var r=all(V.day).filter(function(x){return x.id===id})[0];if(!r)return;
  modal('<h2>'+esc(r.nom)+'</h2><dl><dt>Date</dt><dd>'+label(r.iso)+'</dd><dt>Heure</dt><dd>'+hm(r.t)+'</dd><dt>Convives</dt><dd>'+r.n+'</dd><dt>Type</dt><dd>'+({table:'Table au restaurant',group:'Groupe / Événement',event:'Événement privé'}[r.kind]||'Table')+'</dd>'+(r.tel?'<dt>Téléphone</dt><dd>'+esc(r.tel)+'</dd>':'')+(r.mail?'<dt>E-mail</dt><dd>'+esc(r.mail)+'</dd>':'')+(r.ref?'<dt>Référence</dt><dd>'+esc(r.ref)+'</dd>':'')+(r.msg?'<dt>Demande</dt><dd>'+esc(r.msg)+'</dd>':'')+'<dt>Statut</dt><dd>Confirmée'+(r.web?' (réservée en ligne)':'')+'</dd></dl><div class="ac"><button class="p" id="mc">Fermer</button><button id="mr">Envoyer un rappel</button><button class="d" id="mx">Annuler la réservation</button></div>');
  $('#mc').onclick=close;$('#mr').onclick=function(){close();toast('Rappel envoyé à '+r.nom+' (démonstration)')};
  $('#mx').onclick=function(){var st=store();st.del.push(r.id);save(st);close();render();toast('Réservation annulée : la table est de nouveau disponible.')}}
$('#left').onclick=function(e){var b=e.target.closest('[data-id]');if(b)detail(b.dataset.id)};$('#list').onclick=function(e){var b=e.target.closest('[data-id]');if(b)detail(b.dataset.id)};
$('#prev').onclick=function(){V.day=nextOpen(V.day,-1);V.hl=null;render()};$('#next').onclick=function(){V.day=nextOpen(V.day,1);V.hl=null;render()};
$('#tabs').onclick=function(e){var b=e.target.closest('button');if(b){V.view=b.dataset.v;render()}};
document.querySelector('aside').onclick=function(e){var b=e.target.closest('.nv');if(!b)return;if(b.dataset.v){V.view=b.dataset.v;render()}else if(b.dataset.x)toast(b.dataset.x+' : disponible dans votre espace (démonstration).')};
$('#bell').onclick=function(e){e.stopPropagation();$('#pop').classList.toggle('on')};document.addEventListener('click',function(){$('#pop').classList.remove('on')});
$('#exp').onclick=function(){var l=all(V.day),c='Heure;Nom;Personnes;Type\n';l.forEach(function(r){c+=r.t+';'+String(r.nom).replace(/[;\n]/g,' ').replace(/^[=+\-@]/,"'$&")+';'+r.n+';'+r.kind+'\n'});
  var a=document.createElement('a');a.href=URL.createObjectURL(new Blob(['﻿'+c],{type:'text/csv'}));a.download='reservations-'+V.day+'.csv';document.body.appendChild(a);a.click();a.remove();toast('Export téléchargé (démonstration).')};
$('#add').onclick=function(){var opts='';MIDI.concat(['14:30'],SOIR,['21:30']).forEach(function(t){opts+='<option>'+t+'</option>'});
  modal('<h2>Nouvelle réservation</h2><p style="margin-bottom:10px;color:#6a5557">'+label(V.day)+'</p><div class="f"><label>Nom<input id="fn" placeholder="Ex. : M. Durand"></label><label>Téléphone<input id="ft" type="tel" placeholder="06 …"></label><label>Heure<select id="fh">'+opts+'</select></label><label>Convives<input id="fp" type="number" min="1" max="40" value="2"></label><label>Type<select id="fk"><option value="table">Table</option><option value="group">Groupe</option><option value="event">Événement privé</option></select></label></div><p id="fe" style="color:#b3261e;min-height:20px;margin-top:8px"></p><div class="ac"><button class="p" id="fs">Enregistrer</button><button id="fc">Annuler</button></div>');
  $('#fc').onclick=close;$('#fs').onclick=function(){var nom=$('#fn').value.trim(),n=Math.max(1,Math.min(40,+$('#fp').value||0));if(nom.length<2){$('#fe').textContent='Indiquez un nom.';return}
   var st=store(),id='u'+Date.now();st.res.push({id:id,iso:V.day,t:$('#fh').value,n:n,nom:nom,tel:$('#ft').value.trim(),kind:$('#fk').value});save(st);V.hl=id;close();render();toast('Réservation ajoutée à l’agenda.')}};
render();
if(V.hl)setTimeout(function(){var b=document.querySelector('.blk.new');if(b)b.scrollIntoView({block:'center',behavior:'smooth'})},300);
"""


def interne():
    import json
    body = INT_BODY % dict(chef=ic("chef", 52, 1.7), home=ic("home", 24), cal=ic("cal", 24), users=ic("users", 24), fork=ic("fork", 24),
                           book=ic("book", 24), chart=ic("chart", 24), gear=ic("gear", 24), table=ic("table", 24), dl=ic("dl", 20),
                           bell=ic("bell", 24), user=ic("user", 26), list=ic("list", 20), left=ic("left", 22), right=ic("right", 22), plus=ic("plus", 22, 2.4))
    body = body.replace("%%", "%")
    js = INT_JS.replace("%(icons)s", json.dumps(ICONS)).replace("%%", "%")
    return shell("Espace restaurant · Réservations · Le Bistro du Marché", INT_CSS, body, js, i="on")


def write_all(out):
    open(out + "/bistro-reservation-client.html", "w").write(client())
    open(out + "/bistro-reservation-interne.html", "w").write(interne())


if __name__ == "__main__":
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "site", "exemples")
    os.chdir(root)
    open(os.path.join(out, "bistro-reservation-client.html"), "w").write(client())
    open(os.path.join(out, "bistro-reservation-interne.html"), "w").write(interne())
    print("réservation bistro OK")
