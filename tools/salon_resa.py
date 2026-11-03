# -*- coding: utf-8 -*-
"""Réservation du site d'exemple « Maison Olive » (salon de coiffure) :
 - prise de rendez-vous EXTERNE, intégrée au site du salon (toutes les prestations, jour, heure, coordonnées)
 - espace réservation INTERNE (site/exemples/salon-reservation-interne.html) : agenda par coiffeur
Les deux partagent les mêmes données, mémorisées dans le navigateur : un rendez-vous pris sur le site
apparaît tout de suite dans l'agenda interne. Tout est fictif."""
import json

# ---------- données communes (JavaScript) ----------
CORE = r"""
var KEY='salon-demo-rdv-v1';
var STY=[{n:'Thomas',c:'#7a4a2c'},{n:'Élodie',c:'#b0822f'},{n:'Lucas',c:'#a8553a'},{n:'Sophie',c:'#4f6b6b'}];
var CATS=['Coupes','Couleurs','Soins'];
var PREST=[
{id:'c1',cat:0,n:'Coupe femme',d:'Shampoing, coupe, coiffage',min:45,p:38,who:[1,2,3]},
{id:'c2',cat:0,n:'Coupe homme',d:'Shampoing, coupe',min:30,p:24,who:[0,2]},
{id:'c3',cat:0,n:'Coupe enfant',d:'Moins de 12 ans',min:30,p:16,who:[0,2]},
{id:'c4',cat:0,n:'Brushing',d:'Sur cheveux mi-longs',min:30,p:26,who:[1,3]},
{id:'k1',cat:1,n:'Racines',d:'Coloration + soin',min:75,p:55,who:[1,2]},
{id:'k2',cat:1,n:'Couleur complète',d:'Longueur et pointes',min:105,p:68,who:[1,2]},
{id:'k3',cat:1,n:'Balayage',d:'Technique à la main',min:150,p:90,from:1,who:[1,2]},
{id:'k4',cat:1,n:'Patine / gloss',d:'Brillance et reflets',min:30,p:28,who:[1,2]},
{id:'s1',cat:2,n:'Soin profond',d:'Masque + massage crânien',min:30,p:24,who:[3,1]},
{id:'s2',cat:2,n:'Lissage kératine',d:'Effet 3 mois',min:150,p:120,from:1,who:[3,1]},
{id:'s3',cat:2,n:'Chignon / mariée',d:'Essai inclus',min:60,p:70,from:1,who:[3,1]},
{id:'s4',cat:2,n:'Barbe',d:'Taille et contours',min:20,p:14,who:[0]}];
var MOIS=['janv.','févr.','mars','avr.','mai','juin','juil.','août','sept.','oct.','nov.','déc.'];
var JOURS=['dim.','lun.','mar.','mer.','jeu.','ven.','sam.'];
function pad(n){return n<10?'0'+n:''+n}
function iso(d){return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate())}
function parse(s){var p=s.split('-');return new Date(+p[0],+p[1]-1,+p[2],12)}
function hash(s){var h=0;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return Math.abs(h)}
function cap1(s){return s.charAt(0).toUpperCase()+s.slice(1)}
function label(s){var d=parse(s);return cap1(JOURS[d.getDay()])+' '+d.getDate()+' '+MOIS[d.getMonth()]+' '+d.getFullYear()}
function hm(m){var h=Math.floor(m/60),r=m%60;return h+' h'+(r?' '+pad(r):'')}
function hhmm(m){return pad(Math.floor(m/60))+':'+pad(m%60)}
function dur(m){var h=Math.floor(m/60),r=m%60;return h?(h+' h'+(r?' '+pad(r):'')):(r+' min')}
function eur(p,from){return (from?'dès ':'')+p+' €'}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function byId(id){for(var i=0;i<PREST.length;i++)if(PREST[i].id===id)return PREST[i]}
var TODAY=iso(new Date());
function hours(s){var w=parse(s).getDay();if(w===0||w===1)return[];if(w===6)return[[540,1020]];return[[540,720],[840,1080]]}
function startTimes(s,min){var out=[];hours(s).forEach(function(h){for(var t=h[0];t+min<=h[1];t+=30)out.push(t)});return out}
var NOMS=['Mme Bernard','M. Roche','Mme Fabre','Mme Colin','M. Lemaire','Mme Vidal','Mme Morel','M. Simon','Mme Aubert','Mme Chevalier','M. Gauthier','Mme Marchand','Mme Lopez','M. Perrin'];
function overlap(a,b){return a[0]<b[1]&&b[0]<a[1]}
function seeded(s){
  var out=[],h=hours(s);if(!h.length)return out;
  var hh=hash(s),n=(parse(s).getDay()===6?9:6)+hh%4,i,busy=[[],[],[],[]];
  for(i=0;i<n*3&&out.length<n;i++){
    var g=hash(s+'#'+i),p=PREST[g%PREST.length],w=p.who[(g>>3)%p.who.length],st=startTimes(s,p.min);if(!st.length)continue;
    var t=st[(g>>6)%st.length],seg=[t,t+p.min],ok=true;
    busy[w].forEach(function(b){if(overlap(b,seg))ok=false});
    if(!ok)continue;busy[w].push(seg);
    out.push({id:'g'+s+i,iso:s,t:t,dur:p.min,p:p.id,who:w,nom:NOMS[(g>>9)%NOMS.length],web:0});
  }
  return out;
}
function store(){try{var o=JSON.parse(localStorage.getItem(KEY));if(o&&o.res)return o}catch(e){}return{res:[],del:[]}}
function save(o){try{localStorage.setItem(KEY,JSON.stringify(o))}catch(e){}}
function all(s){var st=store();return seeded(s).concat(st.res.filter(function(r){return r.iso===s})).filter(function(r){return st.del.indexOf(r.id)<0}).sort(function(a,b){return a.t-b.t})}
function isOpenDay(s){return hours(s).length>0}
function freeStylist(s,t,p,list){
  var seg=[t,t+p.min];
  for(var k=0;k<p.who.length;k++){var w=p.who[k],ok=true;
    list.forEach(function(r){if(r.who===w&&overlap([r.t,r.t+r.dur],seg))ok=false});
    if(ok)return w}
  return -1;
}
function slotsFor(s,p){
  var list=all(s),now=new Date(),lim=(s===TODAY)?now.getHours()*60+now.getMinutes()+60:-1;
  return startTimes(s,p.min).map(function(t){return{t:t,w:(s<TODAY||t<=lim)?-1:freeStylist(s,t,p,list)}});
}
"""

# ---------- prise de rendez-vous externe (intégrée au site du salon) ----------
WIDGET_CSS = r"""
.rdvw{display:grid;gap:22px;grid-template-columns:minmax(0,1fr)}.rdvw>*{min-width:0}
.rdvw .st{display:flex;gap:12px;align-items:center;margin-bottom:12px}.rdvw .st i{flex:none;display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--sage);color:#fff;font:700 14px 'Jost',sans-serif;font-style:normal}
.rdvw .st b{font:600 1.3rem 'Cormorant Garamond',serif}
.pcat{font:800 11.5px 'Jost',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--clay);margin:14px 0 8px}
.pgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.pc{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;text-align:left;font:inherit;color:inherit;background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:12px 14px;cursor:pointer;transition:border-color .15s,box-shadow .15s}
.pc:hover{border-color:var(--sage)}.pc span b{display:block;font-weight:700;font-size:15px}.pc span small{color:var(--mut);font-size:12.5px;display:block;line-height:1.35;margin-top:2px}
.pc em{font-style:normal;font-weight:800;color:var(--sage);white-space:nowrap;font-size:15px;text-align:right}.pc em small{display:block;font-weight:500;color:var(--mut);font-size:12px}
.pc.on{background:#eef3ef;border-color:var(--sage);box-shadow:0 0 0 2px var(--sage) inset}
.dchips{display:flex;gap:8px;overflow-x:auto;padding-bottom:6px;-webkit-overflow-scrolling:touch}
.dc,.tc2{font:inherit;font-weight:700;color:inherit;background:#fff;border:1.5px solid var(--line);border-radius:12px;cursor:pointer}
.dc{flex:none;min-width:64px;padding:9px 8px;display:grid;line-height:1.15;text-align:center;font-size:13px}.dc small{font-weight:500;color:var(--mut)}
.tgrid{display:flex;gap:8px;flex-wrap:wrap}.tc2{padding:10px 14px;font-size:14.5px}
.dc.on,.tc2.on{background:var(--sage);border-color:var(--sage);color:#fff}.dc.on small{color:#d6e2da}
.tc2:disabled{text-decoration:line-through;color:#aaa;border-style:dashed;background:transparent;cursor:not-allowed}
.hintx{color:var(--mut);font-size:14px;margin:2px 0}
.rf{display:grid;grid-template-columns:1fr 1fr;gap:10px}.rf label{display:grid;gap:5px;font:700 12px 'Jost',sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
.rf input,.rf textarea{font:500 15px 'Jost',sans-serif;padding:12px 14px;border-radius:12px;border:1.5px solid var(--line);background:#fff;color:var(--ink);text-transform:none;letter-spacing:0;width:100%}
.rf .w2{grid-column:1/-1}.rf textarea{min-height:70px}
.recap2{background:#eef3ef;border-radius:14px;padding:12px 16px;font-weight:600;display:flex;gap:6px 18px;flex-wrap:wrap}
.rgo{border:0;cursor:pointer;font:700 15.5px 'Jost',sans-serif;background:var(--sage);color:#fff;padding:16px 24px;border-radius:99px;width:100%}.rgo:disabled{opacity:.45;cursor:not-allowed}
.rerr{color:#b3261e;font-size:13.5px;min-height:18px}
.rok{display:none;text-align:center;padding:14px 6px}.rok .big{width:64px;height:64px;border-radius:50%;background:var(--sage);color:#fff;display:grid;place-items:center;margin:0 auto 12px;font-size:30px}
.rok h3{font:600 1.6rem 'Cormorant Garamond',serif}.rok .ref{display:inline-block;margin:10px 0;font:700 1.05rem monospace;background:#eef3ef;padding:7px 14px;border-radius:10px;letter-spacing:.06em}
.rok p{color:var(--mut);max-width:440px;margin:6px auto}.rok a.l{display:inline-block;margin-top:12px;font-weight:700;color:var(--sage);text-decoration:underline}
.rdvw.done>.rst{display:none}.rdvw.done .rok{display:block}
.resa-demo{position:sticky;top:0;z-index:60;display:flex;gap:10px;align-items:center;justify-content:center;flex-wrap:wrap;background:var(--gold2);color:#241c15;font:700 14px/1.3 'Jost',system-ui,sans-serif;padding:9px 14px;min-height:46px}
.resa-demo a{background:#241c15;color:#fff;padding:8px 16px;border-radius:99px;font-size:13.5px}.resa-demo a:hover{background:#000}
@media(max-width:700px){.pgrid,.rf{grid-template-columns:minmax(0,1fr)}}
"""

WIDGET_HTML = """<div class="bk"><div class="rdvw" id="rdvw">
<div class="rst" style="display:grid;gap:22px;grid-template-columns:minmax(0,1fr)">
<div><div class="st"><i>1</i><b>Choisissez votre prestation</b></div><div id="pl"></div></div>
<div><div class="st"><i>2</i><b>Le jour</b></div><div class="dchips" id="dl"></div></div>
<div><div class="st"><i>3</i><b>L’heure</b></div><div class="tgrid" id="tl"></div><p class="hintx" id="th"></p></div>
<div><div class="st"><i>4</i><b>Vos coordonnées</b></div>
<div class="rf"><label>Prénom<input id="rp" autocomplete="given-name" placeholder="Claire"></label><label>Nom<input id="rn" autocomplete="family-name" placeholder="Martin"></label>
<label>Téléphone<input id="rt" type="tel" autocomplete="tel" placeholder="06 12 34 56 78"></label><label>E-mail <span style="text-transform:none;letter-spacing:0;font-weight:500">(confirmation)</span><input id="rm" type="email" autocomplete="email" placeholder="claire@exemple.fr"></label>
<label class="w2">Un message pour le salon ? <span style="text-transform:none;letter-spacing:0;font-weight:500">(facultatif)</span><textarea id="rg" placeholder="Longueur actuelle, allergie, première visite…"></textarea></label></div></div>
<div class="recap2" id="rc" hidden></div>
<div class="rerr" id="re" role="alert"></div>
<button type="button" class="rgo" id="rb">Confirmer mon rendez-vous</button>
</div>
<div class="rok" id="rk"><div class="big">✓</div><h3>Rendez-vous confirmé</h3><div class="ref" id="rr"></div><p id="rs"></p><p>Un e-mail de confirmation vous est envoyé, avec un rappel la veille. Vous pouvez modifier ou annuler jusqu’à 24 h avant.</p><a class="l" id="rl" href="/exemples/salon-reservation-interne" target="_blank" rel="noopener">Voir ce rendez-vous dans l’agenda du salon (espace interne) →</a><br><a class="l" href="#rdv" id="ra">Prendre un autre rendez-vous</a></div>
</div></div>"""

WIDGET_JS = r"""
var $=function(s){return document.querySelector(s)};
var S={p:null,day:null,t:null,days:[]};
(function(){var d=new Date();d.setHours(12,0,0,0);while(S.days.length<14){var s=iso(d);if(isOpenDay(s)&&(s>TODAY||slotsFor(s,PREST[3]).some(function(x){return x.w>=0})))S.days.push(s);d.setDate(d.getDate()+1)}})();
function drawP(){var h='';CATS.forEach(function(c,ci){h+='<div class="pcat">'+c+'</div><div class="pgrid">';
  PREST.forEach(function(p){if(p.cat!==ci)return;h+='<button type="button" class="pc'+(S.p===p.id?' on':'')+'" data-id="'+p.id+'"><span><b>'+p.n+'</b><small>'+p.d+'</small></span><em>'+eur(p.p,p.from)+'<small>'+dur(p.min)+'</small></em></button>'});
  h+='</div>'});$('#pl').innerHTML=h}
function drawD(){var h='';S.days.forEach(function(s){var d=parse(s);h+='<button type="button" class="dc'+(S.day===s?' on':'')+'" data-d="'+s+'">'+JOURS[d.getDay()]+'<small>'+d.getDate()+' '+MOIS[d.getMonth()]+'</small></button>'});$('#dl').innerHTML=h}
function drawT(){var el=$('#tl'),p=S.p?byId(S.p):null,hint=$('#th');
  if(!p||!S.day){el.innerHTML='';hint.textContent=!p?'Choisissez d’abord une prestation.':'Choisissez un jour.';return}
  var sl=slotsFor(S.day,p),h='',any=false;
  sl.forEach(function(x){if(x.w>=0)any=true;h+='<button type="button" class="tc2'+(S.t===x.t&&x.w>=0?' on':'')+'" data-t="'+x.t+'"'+(x.w<0?' disabled':'')+'>'+hhmm(x.t)+'</button>'});
  el.innerHTML=h;if(S.t!==null&&!sl.some(function(x){return x.t===S.t&&x.w>=0}))S.t=null;
  hint.textContent=any?'Les horaires barrés sont déjà pris. Durée prévue : '+dur(p.min)+'.':'Plus de créneau ce jour-là pour cette prestation : essayez un autre jour.';}
function drawR(){var r=$('#rc'),p=S.p?byId(S.p):null;if(p&&S.day&&S.t!==null){r.hidden=false;r.innerHTML='<span>✂ '+esc(p.n)+'</span><span>📅 '+label(S.day)+' à '+hm(S.t)+'</span><span>⏱ '+dur(p.min)+'</span><span>💶 '+eur(p.p,p.from)+'</span>'}else r.hidden=true}
function all3(){drawP();drawD();drawT();drawR();$('#re').textContent=''}
$('#pl').onclick=function(e){var b=e.target.closest('.pc');if(!b)return;S.p=b.dataset.id;S.t=null;all3();if(!S.day)$('#dl').scrollIntoView({block:'nearest',behavior:'smooth'})};
$('#dl').onclick=function(e){var b=e.target.closest('.dc');if(!b)return;S.day=b.dataset.d;S.t=null;all3()};
$('#tl').onclick=function(e){var b=e.target.closest('.tc2');if(!b||b.disabled)return;S.t=+b.dataset.t;all3()};
$('#rb').onclick=function(){
  var p=S.p?byId(S.p):null,pr=$('#rp').value.trim(),nm=$('#rn').value.trim(),tel=$('#rt').value.trim(),mail=$('#rm').value.trim(),e=$('#re');
  if(!p){e.textContent='Choisissez une prestation.';return}
  if(!S.day||S.t===null){e.textContent='Choisissez un jour et une heure.';return}
  if(pr.length<2||nm.length<2){e.textContent='Indiquez votre prénom et votre nom.';return}
  if(tel.replace(/\D/g,'').length<8){e.textContent='Indiquez un numéro de téléphone valide.';return}
  if(mail&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail)){e.textContent='Cette adresse e-mail ne semble pas valide.';return}
  var w=freeStylist(S.day,S.t,p,all(S.day));if(w<0||S.day<TODAY){e.textContent='Ce créneau vient d’être pris. Choisissez-en un autre.';drawT();return}
  var st=store(),id='u'+Date.now(),ref='RDV-'+Math.random().toString(36).slice(2,8).toUpperCase();
  st.res.push({id:id,iso:S.day,t:S.t,dur:p.min,p:p.id,who:w,nom:pr+' '+nm,tel:tel,mail:mail,msg:$('#rg').value.trim(),web:1,ref:ref});save(st);
  $('#rr').textContent=ref;$('#rs').innerHTML='<b>'+esc(label(S.day))+' à '+hm(S.t)+'</b><br>'+esc(p.n)+' · '+dur(p.min)+' · '+eur(p.p,p.from)+' · avec '+STY[w].n+'<br>Merci '+esc(pr)+', votre rendez-vous est réservé.';
  $('#rl').href='/exemples/salon-reservation-interne?d='+S.day+'&n='+id;
  $('#rdvw').classList.add('done');$('#rdvw').scrollIntoView({block:'start',behavior:'smooth'})};
$('#ra').onclick=function(ev){ev.preventDefault();S.p=null;S.day=null;S.t=null;['#rp','#rn','#rt','#rm','#rg'].forEach(function(s){$(s).value=''});$('#rdvw').classList.remove('done');all3()};
all3();
"""


def widget():
    return WIDGET_HTML, WIDGET_CSS, "<script>(function(){" + CORE + WIDGET_JS + "})();</script>"


# ---------- espace interne ----------
FONTS = "family=Jost:wght@400;500;600;700&family=Cormorant+Garamond:wght@500;600;700"

INT_CSS = r"""
*{box-sizing:border-box}body{margin:0;font:400 15px/1.5 'Jost',system-ui,sans-serif;color:#241c15;background:#fbf6ef}
h1,h2,h3,p,ul{margin:0;padding:0}ul{list-style:none}button{font:inherit;color:inherit;cursor:pointer}a{color:inherit;text-decoration:none}
.swbar{position:sticky;top:0;z-index:60;display:flex;gap:10px;align-items:center;justify-content:center;flex-wrap:wrap;background:#2b2118;color:#fff;font:500 13px/1.3 system-ui,sans-serif;padding:9px 14px}
.swbar a{padding:7px 14px;border-radius:99px;box-shadow:inset 0 0 0 1.5px #ffffff66;font-weight:700}
.demo-bar{margin-top:30px;background:#111;color:#fff;font:500 12.5px/1.3 system-ui,sans-serif;padding:9px 14px;display:flex;gap:12px;justify-content:space-between;flex-wrap:wrap}
.wrap{max-width:1240px;margin:0 auto;padding:22px 18px 10px}
.top{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:16px}.top h1{font:600 clamp(1.7rem,4vw,2.3rem)/1.1 'Cormorant Garamond',serif}.top p{color:#6f6459}.sp{flex:1}
.btn{border:0;border-radius:99px;background:#b0822f;color:#fff;font-weight:700;padding:11px 20px}.btn.o{background:#fff;color:#b0822f;box-shadow:inset 0 0 0 1.5px #b0822f}.btn.d{background:#b3261e}
.nav{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.nav button.i{width:42px;height:42px;border-radius:50%;border:1.5px solid #eadfce;background:#fff;font-size:18px}
.nav .dt{font:600 1.3rem 'Cormorant Garamond',serif;min-width:210px;text-align:center}
.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:16px}.kpi{background:#fff;border:1px solid #eadfce;border-radius:18px;padding:16px}
.kpi small{color:#6f6459;display:block;font-size:13px}.kpi b{font:600 1.8rem/1.2 'Cormorant Garamond',serif;color:#b0822f}.kpi i{font-style:normal;font-size:12.5px;color:#6f6459}
.grid{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:16px;align-items:start}
.card{background:#fff;border:1px solid #eadfce;border-radius:20px;padding:16px}.card h2{font:600 1.2rem 'Cormorant Garamond',serif;margin-bottom:10px}
.pl{display:grid;grid-template-columns:48px repeat(4,minmax(0,1fr));gap:0;position:relative;overflow-x:auto}
.pl .hd{position:sticky;top:0;background:#fff;z-index:3;padding:8px 6px;text-align:center;font-weight:800;border-bottom:1px solid #eadfce;font-size:14px}.pl .hd span{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
.pl .tm{position:relative;border-right:1px solid #f1e8d8}.pl .tm small{position:absolute;right:6px;transform:translateY(-50%);color:#6f6459;font-size:11.5px}
.pl .col{position:relative;border-right:1px dashed #f1e8d8;min-width:120px}
.hr{position:absolute;left:0;right:0;border-top:1px solid #f0e9dd}
.lunch{position:absolute;left:0;right:0;background:repeating-linear-gradient(45deg,#f1ebdf 0 6px,#f8f3ea 6px 12px);display:grid;place-items:center;color:#9b9486;font-size:12px}
.ev{position:absolute;left:3px;right:3px;border-radius:10px;padding:5px 8px;color:#fff;font-size:12.5px;line-height:1.25;overflow:hidden;border:0;text-align:left;box-shadow:0 2px 6px #0002}
.ev b{display:block;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.ev.web:after{content:"en ligne";position:absolute;right:6px;top:5px;background:#fff;color:#b0822f;font-weight:800;font-size:10px;border-radius:99px;padding:1px 6px}
.ev.hl{outline:3px solid #f2c94c;outline-offset:1px}
.closed{padding:50px 10px;text-align:center;color:#6f6459}
.ls li{display:flex;gap:10px;align-items:center;padding:10px 0;border-top:1px solid #f1e8d8;font-size:14px}.ls li:first-child{border:0}.ls .tm2{font-weight:800;min-width:54px}.ls small{display:block;color:#6f6459}
.ls button{margin-left:auto;border:1.5px solid #eadfce;background:#fff;border-radius:10px;padding:5px 10px;font-size:13px}
.bars div{display:grid;grid-template-columns:90px 1fr 34px;gap:8px;align-items:center;font-size:13.5px;margin:7px 0}.bars i{display:block;height:10px;border-radius:99px;background:#b0822f}
.mdl{position:fixed;inset:0;background:#0007;z-index:80;display:grid;place-items:center;padding:16px}.mdl[hidden]{display:none}
.mdl .box{background:#fff;border-radius:22px;padding:22px;max-width:440px;width:100%;box-shadow:0 30px 80px #0006}.mdl h3{font:600 1.4rem 'Cormorant Garamond',serif;margin-bottom:10px}
.mdl dl{display:grid;grid-template-columns:110px 1fr;gap:6px 10px;margin:10px 0}.mdl dt{color:#6f6459}.mdl dd{margin:0;font-weight:600}.mdl .acts{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
.f{display:grid;gap:10px}.f label{display:grid;gap:4px;font-weight:700;font-size:12.5px;color:#6f6459}.f input,.f select{font:500 15px 'Jost',sans-serif;padding:10px 12px;border:1.5px solid #eadfce;border-radius:12px;background:#fff;color:#241c15}
.toast{position:fixed;left:50%;bottom:64px;transform:translateX(-50%);background:#241c15;color:#fff;padding:12px 18px;border-radius:12px;font-size:14px;z-index:90;opacity:0;pointer-events:none;transition:opacity .2s;max-width:90vw}.toast.on{opacity:1}
@media(max-width:980px){.grid{grid-template-columns:1fr}.kpis{grid-template-columns:repeat(2,1fr)}}
"""

INT_BODY = """<div class="swbar"><b>Site d’exemple · Maison Olive</b><a href="/exemples/salon">← Site du salon</a></div>
<div class="wrap">
<div class="top"><div><h1>Agenda du salon</h1><p>Maison Olive · espace réservation interne</p></div><div class="sp"></div>
<div class="nav"><button class="i" id="pv" aria-label="Jour précédent">‹</button><span class="dt" id="dt"></span><button class="i" id="nx" aria-label="Jour suivant">›</button><button class="btn o" id="td">Aujourd’hui</button><button class="btn" id="nw">+ Nouveau rendez-vous</button></div></div>
<div class="kpis" id="kp"></div>
<div class="grid"><div class="card"><h2>Planning par coiffeur</h2><div id="pl"></div></div>
<div style="display:grid;gap:16px"><div class="card"><h2>Liste du jour</h2><ul class="ls" id="ls"></ul></div><div class="card"><h2>Par type de prestation</h2><div class="bars" id="br"></div></div></div></div>
</div>
<div class="mdl" id="md" hidden><div class="box" id="mb"></div></div>
<div class="demo-bar"><span>Exemple réalisé par Devanture Web · noms et rendez-vous fictifs · les rendez-vous pris ici restent dans votre navigateur · sur un vrai site, cet espace est protégé par un mot de passe et réservé au salon</span><a href="/#avant" target="_top">← Retour à l’offre</a></div><div class="toast" id="toast" role="status"></div>"""

INT_JS = r"""
var $=function(s){return document.querySelector(s)},PX=1.15,T0=540,T1=1080;
var q=new URLSearchParams(location.search),HL=q.get('n');
var cur=q.get('d')&&isOpenDay(q.get('d'))?q.get('d'):(function(){var d=new Date();d.setHours(12);while(!isOpenDay(iso(d)))d.setDate(d.getDate()+1);return iso(d)})();
var tt;function toast(m){var t=$('#toast');t.textContent=m;t.classList.add('on');clearTimeout(tt);tt=setTimeout(function(){t.classList.remove('on')},2400)}
function shift(n){var d=parse(cur);do{d.setDate(d.getDate()+n)}while(!isOpenDay(iso(d)));cur=iso(d);draw()}
function draw(){
  $('#dt').textContent=label(cur);var L=all(cur),h=hours(cur);
  var tot=0,ca=0,web=0,bycat=[0,0,0];L.forEach(function(r){var p=byId(r.p);tot+=r.dur;ca+=p.p;if(r.web)web++;bycat[p.cat]++});
  $('#kp').innerHTML='<div class="kpi"><small>Rendez-vous</small><b>'+L.length+'</b><i>dont '+web+' pris en ligne</i></div><div class="kpi"><small>Temps réservé</small><b>'+dur(tot)+'</b><i>sur '+STY.length+' coiffeurs</i></div><div class="kpi"><small>Chiffre d’affaires prévu</small><b>'+ca+' €</b><i>prix indicatifs</i></div><div class="kpi"><small>Prochain rendez-vous</small><b>'+(L[0]?hm(L[0].t):'—')+'</b><i>'+(L[0]?esc(L[0].nom):'aucun')+'</i></div>';
  var g='<div class="pl"><div class="hd"></div>'+STY.map(function(s){return'<div class="hd"><span style="background:'+s.c+'"></span>'+s.n+'</div>'}).join('');
  var H=(T1-T0)*PX,tm='<div class="tm" style="height:'+H+'px">';for(var m=T0;m<=T1;m+=60)tm+='<small style="top:'+((m-T0)*PX)+'px">'+(m/60)+' h</small>';tm+='</div>';g+=tm;
  for(var w=0;w<4;w++){var c='<div class="col" style="height:'+H+'px">';
    for(var m2=T0;m2<T1;m2+=60)c+='<div class="hr" style="top:'+((m2-T0)*PX)+'px"></div>';
    if(h.length===2)c+='<div class="lunch" style="top:'+((720-T0)*PX)+'px;height:'+(120*PX)+'px">pause</div>';
    if(h.length===1&&h[0][1]<T1)c+='<div class="lunch" style="top:'+((h[0][1]-T0)*PX)+'px;height:'+((T1-h[0][1])*PX)+'px">fermé</div>';
    L.filter(function(r){return r.who===w}).forEach(function(r){var p=byId(r.p);c+='<button class="ev'+(r.web?' web':'')+(r.id===HL?' hl':'')+'" data-id="'+r.id+'" style="top:'+((r.t-T0)*PX)+'px;height:'+(r.dur*PX-2)+'px;background:'+STY[w].c+'"><b>'+hhmm(r.t)+' · '+esc(r.nom)+'</b>'+esc(p.n)+'</button>'});
    g+=c+'</div>'}
  $('#pl').innerHTML=g+'</div>';
  $('#ls').innerHTML=L.length?L.map(function(r){var p=byId(r.p);return'<li><span class="tm2">'+hm(r.t)+'</span><span><b>'+esc(r.nom)+'</b><small>'+esc(p.n)+' · '+STY[r.who].n+(r.web?' · en ligne':'')+'</small></span><button data-id="'+r.id+'">Voir</button></li>'}).join(''):'<li>Aucun rendez-vous ce jour-là.</li>';
  $('#br').innerHTML=CATS.map(function(c,i){return'<div><span>'+c+'</span><span><i style="width:'+(L.length?Math.round(bycat[i]/L.length*100):0)+'%"></i></span><b>'+bycat[i]+'</b></div>'}).join('');
}
function find(id){return all(cur).filter(function(r){return r.id===id})[0]}
function modal(h){$('#mb').innerHTML=h;$('#md').hidden=false}
function close(){$('#md').hidden=true}
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-id]');
  if(b&&(b.classList.contains('ev')||b.closest('.ls'))){var r=find(b.dataset.id);if(!r)return;var p=byId(r.p);
    modal('<h3>'+esc(r.nom)+'</h3><dl><dt>Prestation</dt><dd>'+esc(p.n)+' · '+dur(r.dur)+'</dd><dt>Quand</dt><dd>'+label(cur)+' à '+hm(r.t)+'</dd><dt>Avec</dt><dd>'+STY[r.who].n+'</dd><dt>Prix</dt><dd>'+eur(p.p,p.from)+'</dd>'+(r.tel?'<dt>Téléphone</dt><dd>'+esc(r.tel)+'</dd>':'')+(r.mail?'<dt>E-mail</dt><dd>'+esc(r.mail)+'</dd>':'')+(r.msg?'<dt>Message</dt><dd>'+esc(r.msg)+'</dd>':'')+'<dt>Origine</dt><dd>'+(r.web?'Site internet'+(r.ref?' · '+r.ref:''):'Téléphone / sur place')+'</dd></dl><div class="acts"><button class="btn d" data-del="'+r.id+'">Annuler ce rendez-vous</button><button class="btn o" data-x="1">Fermer</button></div>');return}
  if(e.target.closest('[data-x]')||e.target===$('#md')){close();return}
  var d=e.target.closest('[data-del]');if(d){var st=store();st.del.push(d.dataset.del);save(st);close();draw();toast('Rendez-vous annulé : le créneau est de nouveau libre.');return}
});
$('#pv').onclick=function(){shift(-1)};$('#nx').onclick=function(){shift(1)};
$('#td').onclick=function(){var d=new Date();d.setHours(12);while(!isOpenDay(iso(d)))d.setDate(d.getDate()+1);cur=iso(d);draw()};
$('#nw').onclick=function(){
  modal('<h3>Nouveau rendez-vous</h3><div class="f"><label>Prestation<select id="np">'+PREST.map(function(p){return'<option value="'+p.id+'">'+p.n+' · '+dur(p.min)+' · '+eur(p.p,p.from)+'</option>'}).join('')+'</select></label><label>Heure<select id="nt"></select></label><label>Nom du client<input id="nn" placeholder="Ex. : Mme Dupont"></label><label>Téléphone (facultatif)<input id="ntl" type="tel"></label></div><div class="rerr" id="ne" style="color:#b3261e;font-size:13.5px;min-height:18px"></div><div class="acts"><button class="btn" id="ng">Ajouter à l’agenda</button><button class="btn o" data-x="1">Fermer</button></div>');
  function fill(){var p=byId($('#np').value),sl=slotsFor(cur,p).filter(function(x){return x.w>=0});$('#nt').innerHTML=sl.length?sl.map(function(x){return'<option value="'+x.t+'">'+hm(x.t)+' · '+STY[x.w].n+'</option>'}).join(''):'<option value="">Aucun créneau libre</option>'}
  $('#np').onchange=fill;fill();
  $('#ng').onclick=function(){var p=byId($('#np').value),t=+$('#nt').value,n=$('#nn').value.trim();if(!t){$('#ne').textContent='Aucun créneau libre pour cette prestation ce jour-là.';return}if(n.length<2){$('#ne').textContent='Indiquez le nom du client.';return}
    var w=freeStylist(cur,t,p,all(cur));if(w<0){$('#ne').textContent='Ce créneau vient d’être pris.';return}
    var st=store();st.res.push({id:'m'+Date.now(),iso:cur,t:t,dur:p.min,p:p.id,who:w,nom:n,tel:$('#ntl').value.trim(),web:0});save(st);close();draw();toast('Rendez-vous ajouté à l’agenda.')}};
draw();
"""


def interne():
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Agenda · Espace salon · Maison Olive</title><meta name="description" content="Démonstration de l’agenda interne du salon Maison Olive (exemple fictif)."><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS}&display=swap">
<style>{INT_CSS}</style></head><body>
{INT_BODY}
<script>(function(){{{CORE}
{INT_JS}
}})();</script></body></html>"""


def write_all(out):
    open(out + "/salon-reservation-interne.html", "w").write(interne())
