# -*- coding: utf-8 -*-
"""
Réservation du site d'exemple « Cabinet Lemaire » (ostéopathe) :
 - prise de rendez-vous EXTERNE, détaillée (type de patient, motif, praticien, jour, heure, coordonnées, consentement)
 - espace INTERNE (site/exemples/osteo-reservation-interne.html) : tableau de bord et statistiques, agenda, liste des rendez-vous, réglages
Les deux partagent les mêmes données, mémorisées dans le navigateur : un rendez-vous pris sur le site apparaît tout de suite
dans l'espace interne. Tout est fictif."""
import stripe_demo

CORE = r"""
var KEY='osteo-demo-rdv-v1';
var PRA=[{n:'Léa Lemaire',c:'#0a3d3b',r:'Ostéopathe D.O.',days:[1,2,3,4,5,6]},{n:'Hugo Perrin',c:'#b99c64',r:'Ostéopathe D.O. · sport',days:[2,4,6]}];
var TYPES=[
{id:'ad',n:'Adulte',d:'Consultation d’une heure',min:60,p:60,age:'dès 13 ans',w:60},
{id:'sp',n:'Suivi sportif',d:'Bilan, prévention, reprise',min:60,p:60,age:'tous niveaux',w:12},
{id:'en',n:'Enfant',d:'Techniques adaptées',min:45,p:45,age:'2 à 12 ans',w:10},
{id:'ge',n:'Femme enceinte',d:'Table réglable, positions adaptées',min:60,p:55,age:'toute la grossesse',w:10},
{id:'nr',n:'Nourrisson',d:'Très douce, parents présents',min:45,p:50,age:'moins de 2 ans',w:8}];
var MOTIFS=['Tête / mâchoire','Nuque / cervicales','Épaule','Haut du dos','Bas du dos / lombaires','Coude / poignet','Hanche / bassin','Genou / jambe','Bébé : digestion, sommeil','Grossesse / post-partum','Prévention / contrôle','Autre'];
var MOIS=['janv.','févr.','mars','avr.','mai','juin','juil.','août','sept.','oct.','nov.','déc.'];
var JOURS=['dim.','lun.','mar.','mer.','jeu.','ven.','sam.'];
var JF=['dimanche','lundi','mardi','mercredi','jeudi','vendredi','samedi'];
function pad(n){return n<10?'0'+n:''+n}
function iso(d){return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate())}
function parse(s){var p=s.split('-');return new Date(+p[0],+p[1]-1,+p[2],12)}
function hash(s){var h=0;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return Math.abs(h)}
function cap1(s){return s.charAt(0).toUpperCase()+s.slice(1)}
function label(s){var d=parse(s);return cap1(JOURS[d.getDay()])+' '+d.getDate()+' '+MOIS[d.getMonth()]+' '+d.getFullYear()}
function hm(m){var h=Math.floor(m/60),r=m%60;return h+' h'+(r?' '+pad(r):'')}
function hhmm(m){return pad(Math.floor(m/60))+':'+pad(m%60)}
function dur(m){var h=Math.floor(m/60),r=m%60;return h?(h+' h'+(r?' '+pad(r):'')):(r+' min')}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function byT(id){for(var i=0;i<TYPES.length;i++)if(TYPES[i].id===id)return TYPES[i]}
function dep(t){return t.p}
function stripeOn(){try{return localStorage.getItem('osteo-set-stripe')!=='0'}catch(e){return true}}
function payOf(r){if(r.pay)return r.pay.a;if(r.chan==='web')return dep(byT(r.type));return 0}
var TODAY=iso(new Date());
function daysBetween(a,b){return Math.round((parse(b)-parse(a))/864e5)}
function addDays(s,n){var d=parse(s);d.setDate(d.getDate()+n);return iso(d)}
function hours(s){var w=parse(s).getDay();if(w===0)return[];if(w===6)return[[540,780]];if(w===5)return[[540,720],[840,1020]];if(w===3)return[[540,720],[840,1080]];return[[540,720],[840,1140]]}
function isOpenDay(s){return hours(s).length>0}
function works(w,s){return PRA[w].days.indexOf(parse(s).getDay())>-1}
function startTimes(s,min){var out=[];hours(s).forEach(function(h){for(var t=h[0];t+min<=h[1];t+=30)out.push(t)});return out}
function capacity(s,w){if(!works(w,s))return 0;var c=0;hours(s).forEach(function(h){c+=h[1]-h[0]});return c}
var NOMS=['Claire Bonnet','Thomas Roche','Julie Fabre','Maxime Colin','Sarah Vidal','Nicolas Morel','Emma Simon','Antoine Aubert','Camille Chevalier','Lucas Gauthier','Inès Marchand','Hugo Lopez','Léa Perrin','Karim Benali','Marion Garnier','Paul Renard','Alice Blanc','Mathieu Faure','Sophie Meyer','Yanis Bouzid','Chloé Dupuis','Louis Navarro','Manon Leroy','Adrien Petit'];
function pickType(g){var t=g%100,c=0;for(var i=0;i<TYPES.length;i++){c+=TYPES[i].w;if(t<c)return TYPES[i]}return TYPES[0]}
function overlap(a,b){return a[0]<b[1]&&b[0]<a[1]}
var cache={};
function seeded(s){
  if(cache[s])return cache[s];
  var out=[],h=hours(s);cache[s]=out;if(!h.length)return out;
  var dw=parse(s).getDay(),diff=daysBetween(TODAY,s),busy=[[],[]],nowm=new Date().getHours()*60+new Date().getMinutes();
  for(var w=0;w<2;w++){
    if(!works(w,s))continue;
    var target=(w===0?6+hash(s+'a')%3:4+hash(s+'b')%3)+(dw===6?-1:0);
    if(diff>0)target=Math.max(1,Math.round(target*Math.max(.2,1-diff/26)));
    for(var i=0,n=0;i<target*5&&n<target;i++){
      var g=hash(s+w+'#'+i),ty=pickType(g),st=startTimes(s,ty.min);if(!st.length)continue;
      var t=st[(g>>5)%st.length],seg=[t,t+ty.min],ok=true;
      busy[w].forEach(function(b){if(overlap(b,seg))ok=false});
      if(!ok)continue;busy[w].push(seg);n++;
      var r=(g>>9)%100,statut;
      if(diff<0||(diff===0&&t+ty.min<=nowm))statut=r<5?'absent':(r<11?'annulé':'fait');else statut=(diff>0&&r<7)?'annulé':'confirmé';
      var chan=(g>>3)%100<52?'web':((g>>4)%100<75?'tel':'place');
      out.push({id:'g'+s+w+i,iso:s,t:t,dur:ty.min,type:ty.id,motif:MOTIFS[(g>>11)%(ty.id==='nr'?9:(ty.id==='ge'?10:8))%MOTIFS.length],who:w,nom:NOMS[(g>>13)%NOMS.length],nouveau:(g>>2)%100<27,statut:statut,chan:chan,lead:1+(g>>15)%12,web:chan==='web'?1:0,seed:1});
    }
  }
  return out;
}
function store(){try{var o=JSON.parse(localStorage.getItem(KEY));if(o&&o.res)return o}catch(e){}return{res:[],del:[],st:{},ref:[]}}
function save(o){try{localStorage.setItem(KEY,JSON.stringify(o))}catch(e){}}
function all(s){var st=store(),L=seeded(s).concat(st.res.filter(function(r){return r.iso===s}));
  return L.filter(function(r){return st.del.indexOf(r.id)<0}).map(function(r){var o=st.st&&st.st[r.id];if(o){r=JSON.parse(JSON.stringify(r));r.statut=o}return r}).sort(function(a,b){return a.t-b.t})}
function busyList(s){return all(s).filter(function(r){return r.statut!=='annulé'})}
function freePra(s,t,min,list,pref){
  var seg=[t,t+min],order=pref>=0?[pref]:[0,1];
  for(var k=0;k<order.length;k++){var w=order[k];if(!works(w,s))continue;var ok=true;
    list.forEach(function(r){if(r.who===w&&overlap([r.t,r.t+r.dur],seg))ok=false});
    if(ok)return w}
  return -1;
}
function slotsFor(s,ty,pref){
  var list=busyList(s),now=new Date(),lim=(s===TODAY)?now.getHours()*60+now.getMinutes()+90:-1;
  return startTimes(s,ty.min).map(function(t){return{t:t,w:(s<TODAY||t<=lim)?-1:freePra(s,t,ty.min,list,pref)}});
}
function eur(p){return p+' €'}
"""

# ---------------------------------------------------------------- widget externe
WIDGET_CSS = stripe_demo.CSS + r"""
.rz{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:34px;margin-top:40px;align-items:start}.rz>*{min-width:0}
.rz .step{background:#fff;border-radius:22px;padding:28px 30px;box-shadow:0 8px 30px #032a2a0d;margin-bottom:18px}
.rz .sh{display:flex;gap:14px;align-items:center;margin-bottom:16px}.rz .sh i{flex:none;display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--g);color:#fff;font:500 15px 'Inter',sans-serif;font-style:normal}.rz .sh b{font:500 1.45rem/1.15 'Newsreader',Georgia,serif;color:var(--g)}.rz .sh small{margin-left:auto;color:var(--mut);font-size:13px}
.rz .tg{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.rz .tc{display:flex;flex-direction:column;gap:2px;text-align:left;font:inherit;color:inherit;background:var(--bg);border:1.5px solid var(--ln);border-radius:16px;padding:16px 18px;cursor:pointer;transition:.2s}.rz .tc:hover{border-color:var(--gold)}.rz .tc b{font:500 1.15rem 'Newsreader',Georgia,serif;color:var(--g);display:flex;justify-content:space-between;gap:10px}.rz .tc b em{font:600 1rem 'Inter',sans-serif;font-style:normal;color:var(--gold)}.rz .tc small{color:var(--mut);font-size:13.5px}.rz .tc.on{background:#fff;border-color:var(--g);box-shadow:0 0 0 1.5px var(--g) inset}
.rz .chips{display:flex;gap:9px;flex-wrap:wrap}.rz .chip{font:500 14.5px 'Inter',sans-serif;border:1.5px solid var(--ln);background:var(--bg);color:var(--g);padding:10px 16px;border-radius:99px;cursor:pointer;transition:.2s}.rz .chip:hover{border-color:var(--gold)}.rz .chip.on{background:var(--g);border-color:var(--g);color:#fff}
.rz .pg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.rz .pc{text-align:left;font:inherit;color:inherit;background:var(--bg);border:1.5px solid var(--ln);border-radius:16px;padding:14px 16px;cursor:pointer;display:grid;gap:3px;transition:.2s}.rz .pc i{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;color:#fff;font:500 14px 'Newsreader',Georgia,serif;font-style:normal;margin-bottom:6px}.rz .pc b{font:500 1.05rem 'Newsreader',Georgia,serif;color:var(--g)}.rz .pc small{color:var(--mut);font-size:12.5px}.rz .pc:hover{border-color:var(--gold)}.rz .pc.on{background:#fff;border-color:var(--g);box-shadow:0 0 0 1.5px var(--g) inset}
.rz .dl{display:flex;gap:8px;overflow-x:auto;padding:2px 2px 8px;scrollbar-width:thin}.rz .dc{flex:none;min-width:68px;background:var(--bg);border:1.5px solid var(--ln);border-radius:14px;padding:10px 6px;text-align:center;cursor:pointer;font:500 12.5px/1.25 'Inter',sans-serif;color:var(--g);transition:.2s}.rz .dc b{display:block;font:500 1.7rem/1.1 'Newsreader',Georgia,serif}.rz .dc:hover{border-color:var(--gold)}.rz .dc.on{background:var(--g);color:#fff;border-color:var(--g)}.rz .dc.full{opacity:.4;pointer-events:none}.rz .dc small{display:block;font-size:11px;color:var(--gold);margin-top:2px}.rz .dc.on small{color:#e8dcc2}
.rz .tl h4{font:500 12px 'Inter',sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin:14px 0 8px}.rz .tgrid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px}.rz .ts{font:500 15px 'Inter',sans-serif;border:1.5px solid var(--ln);background:var(--bg);color:var(--g);padding:11px 0;border-radius:12px;cursor:pointer;transition:.2s}.rz .ts:hover:not(:disabled){border-color:var(--gold)}.rz .ts.on{background:var(--gold);border-color:var(--gold);color:var(--g)}.rz .ts:disabled{opacity:.35;text-decoration:line-through;cursor:not-allowed}
.rz .hint{color:var(--mut);font-size:14px;margin-top:10px}
.rz .rf{display:grid;grid-template-columns:1fr 1fr;gap:14px}.rz .rf label{display:grid;gap:6px;font:500 13px 'Inter',sans-serif;color:var(--mut)}.rz .rf label.w2{grid-column:1/-1}.rz .rf input,.rz .rf textarea{font:400 16px 'Inter',sans-serif;padding:13px 15px;border:1.5px solid var(--ln);border-radius:12px;background:var(--bg);color:var(--ink);width:100%}.rz .rf input:focus,.rz .rf textarea:focus{outline:0;border-color:var(--gold);background:#fff}.rz .rf textarea{min-height:80px}
.rz .ck{display:flex;gap:12px;align-items:flex-start;font-size:14.5px;color:var(--ink);margin-top:14px;cursor:pointer}.rz .ck input{margin-top:4px;width:18px;height:18px;accent-color:var(--g)}.rz .ck span{color:var(--mut)}
.rz .side{position:sticky;top:112px}.rz .rc{background:var(--g);color:#fff;border-radius:24px;padding:30px 28px;box-shadow:0 24px 50px #032a2a30}.rz .rc h3{color:#fff;font:500 1.5rem 'Newsreader',Georgia,serif;margin-bottom:16px}.rz .rc ul{display:grid;gap:12px;margin-bottom:18px}.rz .rc li{display:grid;grid-template-columns:90px 1fr;gap:10px;font-size:15px;color:#e5eeeb;border-bottom:1px solid #ffffff1c;padding-bottom:12px}.rz .rc li:last-child{border:0}.rz .rc li span{color:#9fb8b3;font-size:13px}.rz .rc li b{font-weight:500;color:#fff}.rz .rc .tot{display:flex;justify-content:space-between;align-items:baseline;border-top:1px solid #ffffff33;padding-top:16px;font:500 1.1rem 'Inter',sans-serif}.rz .rc .tot b{font:500 2.2rem/1 'Newsreader',Georgia,serif;color:var(--gold)}
.rz .rc .rgo{width:100%;margin-top:20px;background:var(--gold);color:var(--g);border:0;border-radius:12px;padding:18px;font:600 16px 'Inter',sans-serif;cursor:pointer;transition:.2s}.rz .rc .rgo:hover:not(:disabled){background:#fff}.rz .rc .rgo:disabled{opacity:.45;cursor:not-allowed}
.rz .rerr{color:#ffb4a8;font-size:14px;min-height:20px;margin-top:10px}.rz .rc .fine{font-size:12.5px;color:#9fb8b3;margin-top:12px;line-height:1.5}
.rz .rok{display:none;grid-column:1/-1;background:#fff;border-radius:26px;padding:46px 34px;text-align:center;box-shadow:0 8px 30px #032a2a0d}.rz.done>.rl,.rz.done>.side{display:none}.rz.done .rok{display:block}
.rz .rok .big{width:72px;height:72px;border-radius:50%;background:var(--g);color:var(--gold);display:grid;place-items:center;margin:0 auto 16px;font-size:34px}.rz .rok h3{font:500 2.2rem/1.1 'Newsreader',Georgia,serif;color:var(--g)}.rz .rok .ref{display:inline-block;margin:14px 0;font:600 1.05rem ui-monospace,monospace;background:var(--bg);padding:8px 16px;border-radius:10px;letter-spacing:.08em;color:var(--g)}.rz .rok .sm{color:var(--ink);font-size:1.12rem;margin:6px 0}.rz .rok p{color:var(--mut);max-width:520px;margin:8px auto}.rz .rok .act{display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-top:24px}.rz .rok .act a,.rz .rok .act button{display:inline-flex;align-items:center;gap:8px;padding:14px 22px;border-radius:10px;font:500 15px 'Inter',sans-serif;cursor:pointer;border:1.5px solid var(--g);background:transparent;color:var(--g)}.rz .rok .act .pr{background:var(--g);color:#fff}.rz .rok .act .dg{border-color:#b3261e;color:#b3261e}.rz .rok .act a:hover,.rz .rok .act button:hover{background:var(--g);color:#fff}.rz .rok .act .dg:hover{background:#b3261e;color:#fff}.rz .rok .tip{margin:26px auto 0;background:var(--bg);border-radius:16px;padding:18px 22px;max-width:560px;text-align:left;font-size:14.5px;color:var(--mut)}.rz .rok .tip b{color:var(--g)}
.rz [hidden]{display:none!important}
.rz{--pay-ln:var(--ln);--pay-mut:var(--mut)}.rz .lnk{background:none;border:0;color:#b3261e;font:500 15px Inter,sans-serif;text-decoration:underline;cursor:pointer;padding:14px 10px}.resa-demo{background:var(--gold2);color:var(--g);font:500 14px/1.3 'Inter',sans-serif;padding:11px 14px;text-align:center}.resa-demo a{display:inline-block;margin-left:12px;background:var(--g);color:#fff;padding:8px 16px;border-radius:99px;font-size:13.5px}
@media(max-width:980px){.rz{grid-template-columns:1fr}.rz .side{position:static}.rz .tgrid{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media(max-width:600px){.rz .tg,.rz .pg,.rz .rf{grid-template-columns:minmax(0,1fr)}.rz .step{padding:22px 18px}.rz .tgrid{grid-template-columns:repeat(3,minmax(0,1fr))}.rz .rok{padding:34px 18px}}
"""

WIDGET_HTML = """<div class="rz" id="rz"><div class="rl">
<div class="step"><div class="sh"><i>1</i><b>Pour qui est la consultation ?</b></div><div class="tg" id="tg"></div></div>
<div class="step"><div class="sh"><i>2</i><b>Votre situation</b></div><div class="chips" id="sit"><button type="button" class="chip on" data-v="n">Première consultation</button><button type="button" class="chip" data-v="s">Je suis déjà suivi(e) au cabinet</button></div><p class="hint" id="sith"></p></div>
<div class="step"><div class="sh"><i>3</i><b>Le motif principal</b><small>facultatif</small></div><div class="chips" id="mo"></div></div>
<div class="step"><div class="sh"><i>4</i><b>Avec qui ?</b></div><div class="pg" id="pg"></div></div>
<div class="step"><div class="sh"><i>5</i><b>Jour et heure</b></div><div class="dl" id="dl"></div><div class="tl" id="tl"></div><p class="hint" id="th"></p></div>
<div class="step"><div class="sh"><i>6</i><b>Vos coordonnées</b></div>
<div class="rf"><label>Prénom<input id="rp" autocomplete="given-name" placeholder="Claire"></label><label>Nom<input id="rn" autocomplete="family-name" placeholder="Martin"></label>
<label>Téléphone<input id="rt" type="tel" autocomplete="tel" placeholder="06 12 34 56 78"></label><label>E-mail (confirmation)<input id="rm" type="email" autocomplete="email" placeholder="claire@exemple.fr"></label>
<label id="nl">Date de naissance du patient<input id="rb" type="date"></label><label class="w2">Un message pour Léa ? (facultatif)<textarea id="rg" placeholder="Depuis quand, ce qui soulage ou aggrave, radios récentes…"></textarea></label></div>
<label class="ck"><input type="checkbox" id="c1" checked><span>Je souhaite recevoir un SMS de rappel la veille du rendez-vous.</span></label>
<label class="ck"><input type="checkbox" id="c2"><span>J’accepte que mes informations (y compris de santé) soient utilisées par le cabinet pour gérer ce rendez-vous. Elles ne sont ni revendues ni partagées.</span></label></div>
<div class="step" id="paystep"><div class="sh"><i>7</i><b>Paiement en ligne</b></div>@@PAY@@</div>
</div>
<aside class="side"><div class="rc"><h3>Votre rendez-vous</h3><ul id="ru"></ul><div class="tot"><span>Tarif de la séance</span><b id="rp2">—</b></div><button type="button" class="rgo" id="rg2">Confirmer mon rendez-vous</button><div class="rerr" id="re" role="alert"></div><p class="fine">Annulation gratuite jusqu’à 24 h avant. Un rendez-vous manqué sans prévenir est facturé 30 €. Paiement sur place : carte, espèces ou chèque.</p></div></aside>
<div class="rok" id="rk"><div class="big">✓</div><h3>Rendez-vous confirmé</h3><div class="ref" id="rr"></div><p class="sm" id="rs"></p><p>Un e-mail de confirmation vous est envoyé, avec un rappel par SMS la veille.</p>
<div id="rcp"></div><div class="act"><a id="ics" class="pr" download="rendez-vous-cabinet-lemaire.ics" href="#">Ajouter à mon agenda</a><button type="button" id="rcn" class="dg">Annuler ce rendez-vous</button><button type="button" id="rna">Prendre un autre rendez-vous</button><a id="rli" href="/exemples/osteo-reservation-interne" target="_blank" rel="noopener">Voir côté cabinet</a></div>
<div class="tip" id="rtip"></div></div></div>"""

WIDGET_JS = r"""
var $=function(s){return document.querySelector(s)};
var S={ty:'ad',sit:'n',mo:null,pra:-1,day:null,t:null,days:[],last:null};
(function(){var d=new Date();d.setHours(12,0,0,0);d.setDate(d.getDate());while(S.days.length<14){var s=iso(d);if(isOpenDay(s))S.days.push(s);d.setDate(d.getDate()+1)}})();
function ty(){return byT(S.ty)}
function drawTy(){$('#tg').innerHTML=TYPES.map(function(t){return'<button type="button" class="tc'+(S.ty===t.id?' on':'')+'" data-id="'+t.id+'"><b>'+t.n+'<em>'+eur(t.p)+'</em></b><small>'+t.age+' · '+dur(t.min)+'</small><small>'+t.d+'</small></button>'}).join('')}
function drawMo(){$('#mo').innerHTML=MOTIFS.map(function(m){return'<button type="button" class="chip'+(S.mo===m?' on':'')+'" data-m="'+esc(m)+'">'+m+'</button>'}).join('')}
function drawPra(){var h='<button type="button" class="pc'+(S.pra<0?' on':'')+'" data-w="-1"><i style="background:#5f6b69">?</i><b>Le plus tôt possible</b><small>Premier créneau libre</small></button>';
  PRA.forEach(function(p,i){h+='<button type="button" class="pc'+(S.pra===i?' on':'')+'" data-w="'+i+'"><i style="background:'+p.c+'">'+p.n.charAt(0)+'</i><b>'+p.n+'</b><small>'+p.r+'</small></button>'});$('#pg').innerHTML=h}
function dayFree(s){return slotsFor(s,ty(),S.pra).filter(function(x){return x.w>=0}).length}
function drawDay(){$('#dl').innerHTML=S.days.map(function(s){var d=parse(s),n=dayFree(s);return'<button type="button" class="dc'+(S.day===s?' on':'')+(n?'':' full')+'" data-d="'+s+'">'+JOURS[d.getDay()]+'<b>'+d.getDate()+'</b>'+MOIS[d.getMonth()]+'<small>'+(n?n+(n>1?' créneaux':' créneau'):'complet')+'</small></button>'}).join('')}
function drawTime(){var el=$('#tl'),h=$('#th');
  if(!S.day){el.innerHTML='';h.textContent='Choisissez un jour pour voir les horaires.';return}
  var sl=slotsFor(S.day,ty(),S.pra),am=sl.filter(function(x){return x.t<780}),pm=sl.filter(function(x){return x.t>=780}),any=sl.some(function(x){return x.w>=0});
  function g(L){return L.length?'<div class="tgrid">'+L.map(function(x){return'<button type="button" class="ts'+(S.t===x.t&&x.w>=0?' on':'')+'" data-t="'+x.t+'"'+(x.w<0?' disabled':'')+'>'+hhmm(x.t)+'</button>'}).join('')+'</div>':''}
  el.innerHTML=(am.length?'<h4>Matin</h4>'+g(am):'')+(pm.length?'<h4>Après-midi</h4>'+g(pm):'');
  if(S.t!==null&&!sl.some(function(x){return x.t===S.t&&x.w>=0}))S.t=null;
  h.textContent=any?'Les horaires barrés sont déjà pris. Durée prévue : '+dur(ty().min)+'.':'Plus de créneau ce jour-là : essayez un autre jour ou un autre praticien.'}
function who(){if(S.day&&S.t!==null){var w=freePra(S.day,S.t,ty().min,busyList(S.day),S.pra);return w}return S.pra}
function drawRec(){var t=ty(),w=S.day&&S.t!==null?who():S.pra;
  var L=[['Patient',t.n+' · '+t.age],['Situation',S.sit==='n'?'Première consultation':'Déjà suivi(e)'],['Motif',S.mo||'À préciser sur place'],['Avec',w>=0?PRA[w].n:'Premier praticien libre'],['Quand',S.day&&S.t!==null?label(S.day)+' à '+hm(S.t):'À choisir'],['Durée',dur(t.min)]].concat(stripeOn()?[['Paiement',money(dep(t))+' · réglé en ligne']]:[]);
  $('#ru').innerHTML=L.map(function(x){return'<li><span>'+x[0]+'</span><b>'+esc(x[1])+'</b></li>'}).join('');$('#rp2').textContent=eur(t.p);$('#paystep').hidden=!stripeOn();$('#rg2').textContent=stripeOn()?'Payer '+money(dep(t))+' et confirmer':'Confirmer mon rendez-vous';
  $('#nl').style.display=(S.ty==='en'||S.ty==='nr')?'':'none';
  $('#sith').textContent=S.sit==='n'?'Apportez vos radios, IRM et comptes rendus récents : ils m’aident à adapter le soin.':'Je retrouve votre dossier : inutile de tout raconter à nouveau.'}
function all5(){drawTy();drawMo();drawPra();drawDay();drawTime();drawRec();$('#re').textContent=''}
$('#tg').onclick=function(e){var b=e.target.closest('.tc');if(!b)return;S.ty=b.dataset.id;S.t=null;all5()};
$('#sit').onclick=function(e){var b=e.target.closest('.chip');if(!b)return;S.sit=b.dataset.v;[].forEach.call($('#sit').children,function(x){x.classList.toggle('on',x===b)});drawRec()};
$('#mo').onclick=function(e){var b=e.target.closest('.chip');if(!b)return;S.mo=S.mo===b.dataset.m?null:b.dataset.m;drawMo();drawRec()};
$('#pg').onclick=function(e){var b=e.target.closest('.pc');if(!b)return;S.pra=+b.dataset.w;S.t=null;all5()};
$('#dl').onclick=function(e){var b=e.target.closest('.dc');if(!b)return;S.day=b.dataset.d;S.t=null;all5()};
$('#tl').onclick=function(e){var b=e.target.closest('.ts');if(!b||b.disabled)return;S.t=+b.dataset.t;drawTime();drawRec()};
function ics(r){var d=r.iso.replace(/-/g,''),a=pad(Math.floor(r.t/60))+pad(r.t%60)+'00',e2=r.t+r.dur,b=pad(Math.floor(e2/60))+pad(e2%60)+'00';
  return 'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Cabinet Lemaire//FR\r\nBEGIN:VEVENT\r\nUID:'+r.ref+'@cabinet-lemaire\r\nDTSTART:'+d+'T'+a+'\r\nDTEND:'+d+'T'+b+'\r\nSUMMARY:Ostéopathe · Cabinet Lemaire\r\nLOCATION:27 cours Saint-Louis\\, 33300 Bordeaux\r\nDESCRIPTION:Rendez-vous '+r.ref+'. Annulation gratuite jusqu’à 24 h avant.\r\nEND:VEVENT\r\nEND:VCALENDAR'}
$('#rg2').onclick=function(){
  var t=ty(),pr=$('#rp').value.trim(),nm=$('#rn').value.trim(),tel=$('#rt').value.trim(),mail=$('#rm').value.trim(),e=$('#re'),btn=$('#rg2');
  if(!S.day||S.t===null){e.textContent='Choisissez un jour et une heure.';return}
  if(pr.length<2||nm.length<2){e.textContent='Indiquez votre prénom et votre nom.';return}
  if(tel.replace(/\D/g,'').length<8){e.textContent='Indiquez un numéro de téléphone valide.';return}
  if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail)){e.textContent='Indiquez une adresse e-mail valide pour recevoir la confirmation.';return}
  if(!$('#c2').checked){e.textContent='Merci de cocher l’autorisation d’utilisation de vos informations.';return}
  var w=freePra(S.day,S.t,t.min,busyList(S.day),S.pra);if(w<0||S.day<TODAY){e.textContent='Ce créneau vient d’être pris. Choisissez-en un autre.';all5();return}
  function book(pay){var st=store(),id='u'+Date.now(),ref='RDV-'+Math.random().toString(36).slice(2,8).toUpperCase();
    var r={id:id,iso:S.day,t:S.t,dur:t.min,type:t.id,motif:S.mo||'Autre',who:w,nom:pr+' '+nm,tel:tel,mail:mail,msg:$('#rg').value.trim(),nouveau:S.sit==='n',statut:'confirmé',chan:'web',lead:Math.max(0,daysBetween(TODAY,S.day)),web:1,ref:ref,sms:$('#c1').checked?1:0,created:Date.now()};
    if(pay)r.pay=pay;st.res.push(r);save(st);S.last=r;
    $('#rr').textContent=ref;
    $('#rs').innerHTML='<b>'+esc(label(S.day))+' à '+hm(S.t)+'</b><br>'+esc(t.n)+' · '+dur(t.min)+' · '+eur(t.p)+' · avec '+esc(PRA[w].n)+'<br>Merci '+esc(pr)+', votre rendez-vous est réservé.';
    $('#rcp').innerHTML=pay?'<span class="recpt">🔒 Paiement de '+money(pay.a)+' réglé par '+pay.brand+' •••• '+pay.last4+' · reçu '+pay.id+'</span><p style="margin-top:8px;color:var(--mut)">Rien à régler sur place.</p>':'';
    $('#ics').href='data:text/calendar;charset=utf-8,'+encodeURIComponent(ics(r));
    $('#rli').href='/exemples/osteo-reservation-interne?d='+S.day+'&n='+id;
    $('#rtip').innerHTML='<b>Avant le rendez-vous</b><br>'+(S.sit==='n'?'Venez avec vos radios, IRM et comptes rendus récents, et une tenue confortable. ':'')+'Arrivez 5 minutes en avance. Cabinet de plain-pied, tram C arrêt Chartrons.';
    btn.disabled=false;$('#rz').classList.add('done');$('#rz').scrollIntoView({block:'start',behavior:'smooth'})}
  if(stripeOn()){btn.disabled=true;e.textContent='';stripePay(dep(t)).then(function(pay){book(pay)},function(m){btn.disabled=false;e.textContent=m})}else book(null)};
$('#rcn').onclick=function(){if(!S.last)return;var st=store();st.del.push(S.last.id);if(S.last.pay){st.ref=st.ref||[];st.ref.push({id:S.last.id,a:S.last.pay.a})}save(st);$('#rs').innerHTML='<b>Rendez-vous annulé.</b><br>Le créneau est de nouveau libre. Vous recevez un e-mail de confirmation d’annulation.';$('#rcp').innerHTML=S.last.pay?'<span class="recpt">Paiement de '+money(S.last.pay.a)+' remboursé sur votre carte •••• '+S.last.pay.last4+' (5 à 10 jours)</span>':'';$('#rcn').style.display='none';$('#ics').style.display='none'};
$('#rna').onclick=function(){S.day=null;S.t=null;S.last=null;['#rp','#rn','#rt','#rm','#rg','#rb'].forEach(function(s){$(s).value=''});$('#c2').checked=false;['#spc','#spe','#spv'].forEach(function(x){$(x).value=''});$('#rcn').style.display='';$('#ics').style.display='';$('#rz').classList.remove('done');all5()};
spInit();document.addEventListener('osteo-motif',function(e){S.mo=e.detail;drawMo();drawRec()});
all5();
for(var k=0;k<S.days.length;k++){if(dayFree(S.days[k])){S.day=S.days[k];break}}all5();
"""


def widget():
    return WIDGET_HTML.replace("@@PAY@@", stripe_demo.HTML), WIDGET_CSS, "(function(){" + CORE + stripe_demo.JS + WIDGET_JS + "})();"


# ---------------------------------------------------------------- espace interne
FONTS = "family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=Inter:wght@400;500;600"

INT_CSS = r"""
.pm{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:12px 0}.pm div{background:#f4f1e8;border-radius:14px;padding:14px 16px}.pm small{display:block;color:var(--mut);font-size:12.5px}.pm b{display:block;font:500 1.8rem/1.2 'Newsreader',serif;color:var(--g)}
.sconn{display:flex;gap:14px;align-items:center;justify-content:space-between;flex-wrap:wrap;border:1.5px solid #e4ddc9;border-radius:14px;padding:14px 16px}.sconn small{display:block;color:var(--mut)}.tgw{display:flex;gap:10px;align-items:center}.pill.x{background:#e8f0ee;color:var(--g)}
.tgl{position:relative;width:46px;height:26px;border-radius:99px;background:#cfd6d3;border:0;transition:.2s;flex:none;cursor:pointer}.tgl:after{content:"";position:absolute;left:3px;top:3px;width:20px;height:20px;border-radius:50%;background:#fff;transition:.2s}.tgl.on{background:var(--g)}.tgl.on:after{left:23px}
@media(max-width:700px){.pm{grid-template-columns:1fr 1fr}}
*{box-sizing:border-box}:root{--g:#032a2a;--g2:#0a3d3b;--gold:#b99c64;--gold2:#e8dcc2;--bg:#f6f4ef;--card:#fff;--ink:#0f2a29;--mut:#5f6b69;--ln:#e4ded2}
body{margin:0;font:400 15px/1.5 'Inter',system-ui,sans-serif;color:var(--ink);background:var(--bg)}
h1,h2,h3,p,ul,dl,dd{margin:0;padding:0}ul{list-style:none}button{font:inherit;color:inherit;cursor:pointer}a{color:inherit;text-decoration:none}
h1,h2,h3,.serif{font-family:'Newsreader',Georgia,serif;font-weight:500;color:var(--g)}
.swbar{position:sticky;top:0;z-index:70;display:flex;gap:12px;align-items:center;justify-content:center;flex-wrap:wrap;background:var(--g);color:#fff;font:500 13px/1.3 'Inter',sans-serif;padding:9px 14px}.swbar a{padding:7px 14px;border-radius:99px;box-shadow:inset 0 0 0 1.5px #ffffff66;font-weight:600}.swbar a:hover{background:#fff;color:var(--g)}
.app{display:grid;grid-template-columns:240px 1fr;min-height:calc(100vh - 44px)}
.sb{background:#fff;border-right:1px solid var(--ln);padding:24px 16px;position:sticky;top:44px;height:calc(100vh - 44px);align-self:start;display:flex;flex-direction:column;gap:6px}
.sb .lg{display:flex;gap:10px;align-items:center;padding:0 8px 18px}.sb .lg i{width:40px;height:40px;border-radius:12px;background:var(--g);color:var(--gold);display:grid;place-items:center;font:500 1.4rem 'Newsreader',serif;font-style:normal}.sb .lg b{display:block;font:500 1.15rem/1.1 'Newsreader',serif;color:var(--g)}.sb .lg small{color:var(--mut);font-size:11.5px;letter-spacing:.08em}
.sb button.t{display:flex;gap:12px;align-items:center;text-align:left;border:0;background:none;padding:12px 14px;border-radius:12px;font-weight:500;color:var(--ink);transition:.2s}.sb button.t:hover{background:var(--bg)}.sb button.t.on{background:var(--g);color:#fff}.sb button.t svg{width:20px;height:20px;flex:none}
.sb .me{margin-top:auto;border-top:1px solid var(--ln);padding:14px 8px 0;display:flex;gap:10px;align-items:center;font-size:13.5px}.sb .me i{width:36px;height:36px;border-radius:50%;background:var(--gold2);display:grid;place-items:center;font:500 1rem 'Newsreader',serif;font-style:normal;color:var(--g)}.sb .me small{display:block;color:var(--mut)}
.main{padding:28px 32px 40px;min-width:0}
.head{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:22px}.head h1{font-size:2.1rem;line-height:1.1}.head p{color:var(--mut)}.sp{flex:1}
.btn{border:0;border-radius:10px;background:var(--g);color:#fff;font-weight:500;padding:11px 18px;transition:.2s}.btn:hover{background:var(--g2)}.btn.o{background:#fff;color:var(--g);box-shadow:inset 0 0 0 1.5px var(--g)}.btn.o:hover{background:var(--g);color:#fff}.btn.g{background:var(--gold);color:var(--g)}.btn.d{background:#b3261e}.btn.sm{padding:7px 12px;font-size:13px}
.seg{display:inline-flex;background:#fff;border:1px solid var(--ln);border-radius:12px;padding:4px}.seg button{border:0;background:none;padding:8px 16px;border-radius:9px;font-weight:500;color:var(--mut)}.seg button.on{background:var(--g);color:#fff}
.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-bottom:18px}.kpi{background:var(--card);border-radius:18px;padding:20px 22px;box-shadow:0 6px 24px #032a2a0b}.kpi small{display:block;color:var(--mut);font-size:13px}.kpi b{display:block;font:500 2.4rem/1.15 'Newsreader',serif;color:var(--g);margin:4px 0 2px}.kpi i{font-style:normal;font-size:13px;color:var(--mut)}.kpi i.up{color:#1f7a4d}.kpi i.dn{color:#b3261e}
.cards{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:16px}.card{background:var(--card);border-radius:20px;padding:22px 24px;box-shadow:0 6px 24px #032a2a0b;min-width:0}.card h2{font-size:1.25rem;margin-bottom:4px}.card .sub{color:var(--mut);font-size:13.5px;margin-bottom:16px}.c4{grid-column:span 4}.c5{grid-column:span 5}.c6{grid-column:span 6}.c7{grid-column:span 7}.c8{grid-column:span 8}.c12{grid-column:span 12}
.bars{display:flex;align-items:flex-end;gap:10px;height:190px;padding-top:10px}.bars>div{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:6px;height:100%;min-width:0}.bars i{display:block;width:100%;max-width:46px;border-radius:8px 8px 3px 3px;background:var(--g);min-height:3px;transition:height .6s}.bars i.web{background:var(--gold)}.bars b{font:500 .95rem 'Inter',sans-serif;color:var(--g)}.bars small{color:var(--mut);font-size:11.5px;white-space:nowrap}
.hz{display:grid;gap:9px}.hz div{display:grid;grid-template-columns:130px 1fr 40px;gap:12px;align-items:center;font-size:14px}.hz i{display:block;height:10px;border-radius:99px;background:var(--gold)}.hz span.tr{display:block;background:#f0ebe0;border-radius:99px}.hz b{text-align:right;font-weight:500}
.heat{display:grid;grid-template-columns:44px repeat(7,1fr);gap:4px;font-size:12px;color:var(--mut)}.heat div{min-width:0}.heat .c{height:26px;border-radius:6px;display:grid;place-items:center;font-size:11.5px;color:#fff}.heat .h{text-align:right;padding-right:6px;align-self:center}.heat .d{text-align:center;font-weight:500}
.don{display:flex;gap:22px;align-items:center;flex-wrap:wrap}.don .ring{width:150px;height:150px;border-radius:50%;flex:none;position:relative}.don .ring:after{content:"";position:absolute;inset:30px;border-radius:50%;background:#fff}.don ul{display:grid;gap:8px;font-size:14px;flex:1;min-width:150px}.don li{display:flex;gap:10px;align-items:center}.don li i{width:12px;height:12px;border-radius:4px;flex:none}.don li b{margin-left:auto;font-weight:500}
.pl{display:grid;grid-template-columns:54px repeat(2,minmax(0,1fr));overflow-x:auto}.pl .hd{position:sticky;top:0;background:#fff;z-index:3;padding:10px 6px;text-align:center;font-weight:500;border-bottom:1px solid var(--ln)}.pl .hd span{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:7px}
.pl .tm{position:relative;border-right:1px solid #f1ecdf}.pl .tm small{position:absolute;right:8px;transform:translateY(-50%);color:var(--mut);font-size:11.5px}.pl .col{position:relative;border-right:1px dashed #efe9db;min-width:170px}.hr{position:absolute;left:0;right:0;border-top:1px solid #f1ecdf}
.lunch{position:absolute;left:0;right:0;background:repeating-linear-gradient(45deg,#f3efe5 0 6px,#f9f6ef 6px 12px);display:grid;place-items:center;color:#9b9486;font-size:12px}
.ev{position:absolute;left:4px;right:4px;border-radius:10px;padding:6px 10px;color:#fff;font-size:12.5px;line-height:1.25;overflow:hidden;border:0;text-align:left;box-shadow:0 2px 6px #0002}.ev b{display:block;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-weight:500}.ev.web:after{content:"en ligne";position:absolute;right:6px;top:6px;background:#fff;color:var(--g);font-weight:600;font-size:10px;border-radius:99px;padding:1px 7px}.ev.hl{outline:3px solid #f2c94c;outline-offset:1px}.ev.ab{opacity:.45;text-decoration:line-through}
.closed{padding:60px 10px;text-align:center;color:var(--mut)}
.tbl{width:100%;border-collapse:collapse;font-size:14px}.tbl th{text-align:left;font:500 12px 'Inter',sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);padding:10px 12px;border-bottom:1px solid var(--ln)}.tbl td{padding:13px 12px;border-bottom:1px solid #f1ecdf;vertical-align:middle}.tbl tr:hover td{background:#faf8f3}.tbl small{display:block;color:var(--mut)}
.pill{display:inline-block;border-radius:99px;padding:3px 11px;font-size:12px;font-weight:500;background:#eef4ef;color:#1f7a4d}.pill.w{background:#fbf3df;color:#8a6d1f}.pill.x{background:#fbe9e7;color:#b3261e}.pill.g{background:#eceae3;color:var(--mut)}
.tools{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}.tools input,.tools select{font:inherit;padding:10px 14px;border:1.5px solid var(--ln);border-radius:10px;background:#fff;color:var(--ink)}.tools input{flex:1;min-width:200px}
.set{display:grid;gap:14px}.set .row{display:flex;gap:16px;align-items:center;justify-content:space-between;padding:14px 0;border-bottom:1px solid #f1ecdf}.set .row:last-child{border:0}.set .row small{display:block;color:var(--mut)}
.tg{position:relative;width:46px;height:26px;border-radius:99px;background:#d7d2c4;border:0;flex:none;transition:.2s}.tg:after{content:"";position:absolute;left:3px;top:3px;width:20px;height:20px;border-radius:50%;background:#fff;transition:.2s;box-shadow:0 1px 3px #0004}.tg.on{background:var(--g)}.tg.on:after{left:23px}
.mdl{position:fixed;inset:0;background:#032a2a99;z-index:90;display:grid;place-items:center;padding:16px}.mdl[hidden]{display:none}.mdl .box{background:#fff;border-radius:24px;padding:28px;max-width:480px;width:100%;box-shadow:0 30px 80px #0006}.mdl h3{font-size:1.6rem;margin-bottom:10px}.mdl dl{display:grid;grid-template-columns:110px 1fr;gap:8px 12px;margin:12px 0}.mdl dt{color:var(--mut)}.mdl dd{margin:0;font-weight:500}.mdl .acts{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}
.f{display:grid;gap:12px}.f label{display:grid;gap:5px;font-weight:500;font-size:13px;color:var(--mut)}.f input,.f select{font:inherit;padding:11px 13px;border:1.5px solid var(--ln);border-radius:10px;background:#fff;color:var(--ink)}
.toast{position:fixed;left:50%;bottom:64px;transform:translateX(-50%);background:var(--g);color:#fff;padding:13px 20px;border-radius:12px;font-size:14px;z-index:95;opacity:0;pointer-events:none;transition:opacity .2s;max-width:90vw}.toast.on{opacity:1}
.view{display:none}.view.on{display:block;animation:vin .45s cubic-bezier(.2,.8,.2,1)}@keyframes vin{from{opacity:0;transform:translateY(10px)}}
.demo-bar{background:#111;color:#fff;font:500 12.5px/1.3 system-ui,sans-serif;padding:10px 16px;display:flex;gap:12px;justify-content:space-between;flex-wrap:wrap}
.bur{display:none}
@media(max-width:1100px){.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.c4,.c5,.c6,.c7,.c8{grid-column:span 12}}
@media(max-width:860px){.app{grid-template-columns:1fr}.sb{position:static;height:auto;flex-direction:row;flex-wrap:wrap;padding:12px;gap:4px;border-right:0;border-bottom:1px solid var(--ln)}.sb .lg{padding:0 8px 0 4px}.sb .me{display:none}.sb button.t{padding:9px 12px}.main{padding:20px 16px 30px}.pl{grid-template-columns:44px repeat(2,minmax(150px,1fr))}.tbl .hide{display:none}}
@media(max-width:520px){.kpis{grid-template-columns:1fr 1fr;gap:10px}.kpi{padding:14px}.kpi b{font-size:1.9rem}.sb button.t span{display:none}.hz div{grid-template-columns:100px 1fr 34px}}
"""

IC = {
 'dash': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>',
 'cal': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3.500" y="5" width="17" height="15" rx="2"/><path d="M3.500 10h17M8 3v4M16 3v4"/></svg>',
 'list': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M8 6h13M8 12h13M8 18h13M3.500 6h.01M3.500 12h.01M3.500 18h.01"/></svg>',
 'set': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.400 15a1.700 1.700 0 0 0 .3 1.800l.1.1a2 2 0 1 1-2.800 2.800l-.1-.1a1.700 1.700 0 0 0-1.800-.3 1.700 1.700 0 0 0-1 1.500V21a2 2 0 1 1-4 0v-.1a1.700 1.700 0 0 0-1.100-1.500 1.700 1.700 0 0 0-1.800.3l-.1.1a2 2 0 1 1-2.800-2.800l.1-.1a1.700 1.700 0 0 0 .3-1.800 1.700 1.700 0 0 0-1.500-1H3a2 2 0 1 1 0-4h.1a1.700 1.700 0 0 0 1.500-1.100 1.700 1.700 0 0 0-.3-1.800l-.1-.1a2 2 0 1 1 2.800-2.800l.1.1a1.700 1.700 0 0 0 1.800.3H9a1.700 1.700 0 0 0 1-1.500V3a2 2 0 1 1 4 0v.1a1.700 1.700 0 0 0 1 1.500 1.700 1.700 0 0 0 1.800-.3l.1-.1a2 2 0 1 1 2.800 2.800l-.1.1a1.700 1.700 0 0 0-.3 1.800V9a1.700 1.700 0 0 0 1.500 1H21a2 2 0 1 1 0 4h-.1a1.700 1.700 0 0 0-1.500 1z"/></svg>'}

INT_BODY = """<div class="swbar"><b>Site d’exemple · Cabinet Lemaire</b><a href="/exemples/osteo">← Site du cabinet</a></div>
<div class="app"><aside class="sb"><div class="lg"><i>L</i><span><b>Cabinet Lemaire</b><small>ESPACE PROFESSIONNEL</small></span></div>
<button class="t on" data-v="dash">@@I1@@<span>Tableau de bord</span></button><button class="t" data-v="agenda">@@I2@@<span>Agenda</span></button><button class="t" data-v="liste">@@I3@@<span>Rendez-vous</span></button><button class="t" data-v="regl">@@I4@@<span>Réglages</span></button>
<div class="me"><i>LL</i><span>Léa Lemaire<small>Ostéopathe D.O.</small></span></div></aside>
<main class="main">

<section class="view on" id="v-dash"><div class="head"><div><h1>Tableau de bord</h1><p>Vos réservations en un coup d’œil</p></div><div class="sp"></div><div class="seg" id="per"><button data-p="7">7 jours</button><button data-p="30" class="on">30 jours</button><button data-p="90">90 jours</button></div></div>
<div class="kpis" id="kp"></div>
<div class="card" style="margin-bottom:18px"><h2>Paiements en ligne (Stripe)</h2><p class="sub">Encaissés directement sur votre compte, sans commission de notre part</p><div class="pm" id="pm"></div></div>
<div class="cards"><div class="card c8"><h2>Rendez-vous par semaine</h2><p class="sub">Les 8 dernières semaines, la semaine en cours et la suivante · en doré, les rendez-vous pris en ligne</p><div class="bars" id="wk"></div></div>
<div class="card c4"><h2>Prochain rendez-vous</h2><p class="sub" id="nxs"></p><div id="nx"></div></div>
<div class="card c6"><h2>Motifs de consultation</h2><p class="sub">Ce qui amène vos patients</p><div class="hz" id="mt"></div></div>
<div class="card c6"><h2>Types de patients</h2><p class="sub">Répartition sur la période</p><div class="don" id="ty"></div></div>
<div class="card c7"><h2>Jours et heures les plus demandés</h2><p class="sub">Plus la case est foncée, plus le créneau est réservé</p><div class="heat" id="ht"></div></div>
<div class="card c5"><h2>Comment ils réservent</h2><p class="sub">Canal de prise de rendez-vous</p><div class="hz" id="ch"></div><h2 style="margin-top:22px">Par praticien</h2><p class="sub">Taux de remplissage de l’agenda</p><div class="hz" id="pr"></div></div></div></section>

<section class="view" id="v-agenda"><div class="head"><div><h1>Agenda</h1><p id="dt2">—</p></div><div class="sp"></div><button class="btn o" id="pv" aria-label="Jour précédent">‹</button><button class="btn o" id="td">Aujourd’hui</button><button class="btn o" id="nxd" aria-label="Jour suivant">›</button><button class="btn g" id="nw">+ Nouveau rendez-vous</button></div>
<div class="card"><div id="pl"></div></div></section>

<section class="view" id="v-liste"><div class="head"><div><h1>Rendez-vous</h1><p>Tous les rendez-vous, à venir et passés</p></div></div>
<div class="tools"><input id="q" placeholder="Rechercher un patient ou un motif"><select id="fs"><option value="">Tous les statuts</option><option value="confirmé">Confirmés</option><option value="fait">Réalisés</option><option value="absent">Absents</option><option value="annulé">Annulés</option></select><select id="fp"><option value="">Tous les praticiens</option><option value="0">Léa Lemaire</option><option value="1">Hugo Perrin</option></select><select id="fw"><option value="">Passés et à venir</option><option value="f">À venir</option><option value="p">Passés</option></select></div>
<div class="card" style="overflow-x:auto"><table class="tbl"><thead><tr><th>Date</th><th>Patient</th><th class="hide">Motif</th><th class="hide">Praticien</th><th>Statut</th><th></th></tr></thead><tbody id="rows"></tbody></table><p class="sub" id="cnt" style="margin:14px 0 0"></p></div></section>

<section class="view" id="v-regl"><div class="head"><div><h1>Réglages</h1><p>Comment fonctionne la réservation en ligne</p></div></div>
<div class="cards"><div class="card c6"><h2>Réservation en ligne</h2><p class="sub">Ce que vos patients voient sur le site</p><div class="set" id="st1"></div></div>
<div class="card c6"><h2>Horaires d’ouverture</h2><p class="sub">Les créneaux proposés suivent ces horaires</p><ul class="hz" style="gap:0" id="hh"></ul></div>
<div class="card c12"><h2>Paiement en ligne · Stripe</h2><p class="sub">Le client règle sa prestation en ligne, au moment de réserver. Aucune commission : seuls les frais de Stripe s’appliquent.</p><div class="sconn"><span><b id="sct">Compte Stripe connecté</b><small id="scs"></small></span><span class="tgw"><small>Paiement en ligne</small><button class="tgl on" id="tgs" aria-label="Activer le paiement en ligne"></button></span></div></div>
<div class="card c12"><h2>Durées et tarifs</h2><p class="sub">Les types de consultation proposés à la réservation</p><table class="tbl"><thead><tr><th>Type</th><th>Durée</th><th>Tarif</th><th>Patients</th></tr></thead><tbody id="tt"></tbody></table></div></div></section>

</main></div>
<div class="mdl" id="md" hidden><div class="box" id="mb"></div></div>
<div class="demo-bar"><span>Exemple réalisé par Devanture Web · noms et rendez-vous fictifs · les rendez-vous pris sur le site restent dans votre navigateur · sur un vrai site, cet espace est protégé par un mot de passe et réservé au cabinet</span><a href="/#avant" target="_top">← Retour à l’offre</a></div><div class="toast" id="toast"></div>"""

INT_JS = r"""
var $=function(s){return document.querySelector(s)},PX=1.1,T0=540,T1=1140;
var q=new URLSearchParams(location.search),HL=q.get('n'),per=30;
var cur=q.get('d')&&isOpenDay(q.get('d'))?q.get('d'):(function(){var d=new Date();d.setHours(12);while(!isOpenDay(iso(d)))d.setDate(d.getDate()+1);return iso(d)})();
var tt;function toast(m){var t=$('#toast');t.textContent=m;t.classList.add('on');clearTimeout(tt);tt=setTimeout(function(){t.classList.remove('on')},2600)}
function range(a,b){var o=[],d=a;while(d<=b){o.push(d);d=addDays(d,1)}return o}
function pct(a,b){return b?Math.round(a/b*100):0}
function eurs(n){return n.toLocaleString('fr-FR')+' €'}
/* ---------- tableau de bord ---------- */
function stats(days){
  var L=[];days.forEach(function(s){L=L.concat(all(s))});
  var done=L.filter(function(r){return r.statut==='fait'||r.statut==='confirmé'&&r.iso<=TODAY}),act=L.filter(function(r){return r.statut!=='annulé'});
  var booked=0,cap=0;days.forEach(function(s){PRA.forEach(function(p,w){cap+=capacity(s,w)})});act.forEach(function(r){booked+=r.dur});
  return{L:L,act:act,done:done,booked:booked,cap:cap,ca:act.filter(function(r){return r.statut!=='absent'}).reduce(function(s,r){return s+byT(r.type).p},0),nouv:act.filter(function(r){return r.nouveau}).length,abs:L.filter(function(r){return r.statut==='absent'}).length,can:L.filter(function(r){return r.statut==='annulé'}).length,web:act.filter(function(r){return r.chan==='web'}).length,lead:act.length?act.reduce(function(s,r){return s+r.lead},0)/act.length:0}
}
function drawDash(){
  var end=addDays(TODAY,0),cmp=addDays(TODAY,-per),days=range(addDays(TODAY,-per+1),end),prev=range(addDays(TODAY,-2*per+1),addDays(TODAY,-per));
  var S=stats(days),P=stats(prev);function tr(a,b,pl){var d=b?Math.round((a-b)/b*100):0;return'<i class="'+(d>=0?'up':'dn')+'">'+(d>=0?'▲ +':'▼ ')+d+' % '+pl+'</i>'}
  var real=S.act.filter(function(r){return r.iso<=TODAY}).length;
  $('#kp').innerHTML='<div class="kpi"><small>Rendez-vous</small><b>'+S.act.length+'</b>'+tr(S.act.length,P.act.length,'vs période précédente')+'</div>'
   +'<div class="kpi"><small>Taux de remplissage</small><b>'+pct(S.booked,S.cap)+' %</b><i>'+Math.round(S.booked/60)+' h réservées sur '+Math.round(S.cap/60)+' h</i></div>'
   +'<div class="kpi"><small>Chiffre d’affaires</small><b>'+eurs(S.ca)+'</b>'+tr(S.ca,P.ca,'vs période précédente')+'</div>'
   +'<div class="kpi"><small>Nouveaux patients</small><b>'+S.nouv+'</b><i>'+pct(S.nouv,S.act.length)+' % des rendez-vous</i></div>'
   +'<div class="kpi"><small>Pris en ligne</small><b>'+pct(S.web,S.act.length)+' %</b><i>'+S.web+' réservations en ligne</i></div>'
   +'<div class="kpi"><small>Taux d’absence</small><b>'+pct(S.abs,S.L.length-S.can||1)+' %</b><i>'+S.abs+' absents · '+S.can+' annulés</i></div>'
   +'<div class="kpi"><small>Délai moyen de réservation</small><b>'+S.lead.toFixed(1).replace('.',',')+' j</b><i>entre la prise et le rendez-vous</i></div>'
   +'<div class="kpi"><small>Prochain créneau libre</small><b id="nfree">—</b><i>pour une consultation adulte</i></div>';
  /* semaines */
  var wk=[],mon=addDays(TODAY,-((parse(TODAY).getDay()+6)%7));
  for(var i=-8;i<=1;i++){var a=addDays(mon,i*7),n=0,w=0;for(var j=0;j<7;j++){all(addDays(a,j)).forEach(function(r){if(r.statut!=='annulé'){n++;if(r.chan==='web')w++}})}wk.push({a:a,n:n,w:w,cur:i===0})}
  var mx=Math.max.apply(null,wk.map(function(x){return x.n}))||1;
  $('#wk').innerHTML=wk.map(function(x){var d=parse(x.a);return'<div><b>'+x.n+'</b><i style="height:'+Math.round((x.n-x.w)/mx*120)+'px;border-radius:0 0 3px 3px;background:var(--g)"></i><i class="web" style="height:'+Math.round(x.w/mx*120)+'px;border-radius:8px 8px 0 0" title="'+x.w+' en ligne"></i><small>'+d.getDate()+' '+MOIS[d.getMonth()]+'</small></div>'}).join('');
  /* motifs */
  var mo={};S.act.forEach(function(r){mo[r.motif]=(mo[r.motif]||0)+1});var ml=Object.keys(mo).sort(function(a,b){return mo[b]-mo[a]}).slice(0,6),m0=mo[ml[0]]||1;
  $('#mt').innerHTML=ml.map(function(k){return'<div><span>'+esc(k)+'</span><span class="tr"><i style="width:'+Math.round(mo[k]/m0*100)+'%"></i></span><b>'+mo[k]+'</b></div>'}).join('');
  /* types */
  var cols=['#032a2a','#b99c64','#5f8f8b','#d9c79f','#8aa09b'],ty={};S.act.forEach(function(r){ty[r.type]=(ty[r.type]||0)+1});var acc=0,seg=[];
  TYPES.forEach(function(t,i){var v=ty[t.id]||0,p=pct(v,S.act.length);seg.push(cols[i]+' '+acc+'% '+(acc+p)+'%');acc+=p});
  $('#ty').innerHTML='<div class="ring" style="background:conic-gradient('+seg.join(',')+')"></div><ul>'+TYPES.map(function(t,i){return'<li><i style="background:'+cols[i]+'"></i>'+t.n+'<b>'+(ty[t.id]||0)+'</b></li>'}).join('')+'</ul>';
  /* heatmap */
  var hm2={},hmx=1;S.act.forEach(function(r){var k=parse(r.iso).getDay()+'-'+Math.floor(r.t/60);hm2[k]=(hm2[k]||0)+1;if(hm2[k]>hmx)hmx=hm2[k]});
  var hh='<div></div>'+[1,2,3,4,5,6,0].map(function(d){return'<div class="d">'+JOURS[d].replace('.','')+'</div>'}).join('');
  for(var h=9;h<=18;h++){hh+='<div class="h">'+h+' h</div>';[1,2,3,4,5,6,0].forEach(function(d){var v=hm2[d+'-'+h]||0,a=v/hmx;hh+='<div class="c" style="background:'+(v?'rgba(3,42,42,'+(.15+a*.85).toFixed(2)+')':'#f3efe5')+';color:'+(a>.35?'#fff':'#5f6b69')+'">'+(v||'')+'</div>'})}
  $('#ht').innerHTML=hh;
  /* canaux */
  var cn={web:0,tel:0,place:0};S.act.forEach(function(r){cn[r.chan]++});var cl={web:'Site internet',tel:'Téléphone',place:'Sur place'},cm=Math.max(cn.web,cn.tel,cn.place)||1;
  $('#ch').innerHTML=['web','tel','place'].map(function(k){return'<div><span>'+cl[k]+'</span><span class="tr"><i style="width:'+Math.round(cn[k]/cm*100)+'%"></i></span><b>'+pct(cn[k],S.act.length)+' %</b></div>'}).join('');
  $('#pr').innerHTML=PRA.map(function(p,w){var b=0,c=0;days.forEach(function(s){c+=capacity(s,w)});S.act.forEach(function(r){if(r.who===w)b+=r.dur});return'<div><span>'+p.n+'</span><span class="tr"><i style="width:'+pct(b,c)+'%;background:'+p.c+'"></i></span><b>'+pct(b,c)+' %</b></div>'}).join('');
  /* prochain rdv */
  var now=new Date(),nm=now.getHours()*60+now.getMinutes(),nxr=null;
  for(var k=0;k<30&&!nxr;k++){var s=addDays(TODAY,k);all(s).forEach(function(r){if(!nxr&&r.statut==='confirmé'&&(k>0||r.t>nm))nxr=r})}
  $('#nxs').textContent=nxr?label(nxr.iso)+' à '+hm(nxr.t):'Aucun rendez-vous à venir';
  $('#nx').innerHTML=nxr?'<div class="serif" style="font-size:1.5rem">'+esc(nxr.nom)+'</div><p style="color:var(--mut);margin:4px 0 12px">'+byT(nxr.type).n+' · '+esc(nxr.motif)+'<br>avec '+PRA[nxr.who].n+'</p><button class="btn o sm" data-id="'+nxr.id+'" data-d="'+nxr.iso+'">Voir la fiche</button>':'';
  for(var f=0;f<20;f++){var s2=addDays(TODAY,f);if(!isOpenDay(s2))continue;var sl=slotsFor(s2,byT('ad'),-1).filter(function(x){return x.w>=0});if(sl.length){$('#nfree').textContent=(f===0?'Aujourd’hui':f===1?'Demain':cap1(JOURS[parse(s2).getDay()])+' '+parse(s2).getDate())+' · '+hhmm(sl[0].t);break}}
}
/* ---------- agenda ---------- */
function drawAg(){
  $('#dt2').textContent=label(cur);var L=all(cur),h=hours(cur);
  if(!h.length){$('#pl').innerHTML='<div class="closed">Cabinet fermé ce jour-là.</div>';return}
  var H=(T1-T0)*PX,g='<div class="pl"><div class="hd"></div>'+PRA.map(function(s){return'<div class="hd"><span style="background:'+s.c+'"></span>'+s.n+'</div>'}).join('');
  var tm='<div class="tm" style="height:'+H+'px">';for(var m=T0;m<=T1;m+=60)tm+='<small style="top:'+((m-T0)*PX)+'px">'+(m/60)+' h</small>';g+=tm+'</div>';
  for(var w=0;w<2;w++){var c='<div class="col" style="height:'+H+'px">';for(var m2=T0;m2<T1;m2+=60)c+='<div class="hr" style="top:'+((m2-T0)*PX)+'px"></div>';
    if(!works(w,cur))c+='<div class="lunch" style="top:0;height:'+H+'px">ne consulte pas ce jour</div>';
    else{if(h.length===2)c+='<div class="lunch" style="top:'+((h[0][1]-T0)*PX)+'px;height:'+((h[1][0]-h[0][1])*PX)+'px">pause</div>';var last=h[h.length-1][1];if(last<T1)c+='<div class="lunch" style="top:'+((last-T0)*PX)+'px;height:'+((T1-last)*PX)+'px">fermé</div>';if(h[0][0]>T0)c+='<div class="lunch" style="top:0;height:'+((h[0][0]-T0)*PX)+'px"></div>'}
    L.filter(function(r){return r.who===w&&r.statut!=='annulé'}).forEach(function(r){c+='<button class="ev'+(r.chan==='web'?' web':'')+(r.statut==='absent'?' ab':'')+(r.id===HL?' hl':'')+'" data-id="'+r.id+'" data-d="'+cur+'" style="top:'+((r.t-T0)*PX)+'px;height:'+(r.dur*PX-2)+'px;background:'+PRA[w].c+'"><b>'+hhmm(r.t)+' · '+esc(r.nom)+'</b>'+byT(r.type).n+' · '+esc(r.motif)+'</button>'});
    g+=c+'</div>'}
  $('#pl').innerHTML=g+'</div>';
}
/* ---------- liste ---------- */
function pill(s){return'<span class="pill '+(s==='confirmé'?'w':s==='fait'?'':s==='absent'?'g':'x')+'">'+(s==='confirmé'?'Confirmé':s==='fait'?'Réalisé':s==='absent'?'Absent':'Annulé')+'</span>'}
function drawList(){
  var L=[];range(addDays(TODAY,-45),addDays(TODAY,21)).forEach(function(s){L=L.concat(all(s))});
  var t=$('#q').value.trim().toLowerCase(),fs=$('#fs').value,fp=$('#fp').value,fw=$('#fw').value;
  L=L.filter(function(r){return(!t||(r.nom+' '+r.motif).toLowerCase().indexOf(t)>-1)&&(!fs||r.statut===fs)&&(fp===''||r.who===+fp)&&(!fw||(fw==='f'?r.iso>=TODAY:r.iso<TODAY))}).sort(function(a,b){return fw==='p'||(!fw&&false)?0:0});
  L.sort(function(a,b){return a.iso===b.iso?a.t-b.t:(a.iso<b.iso?1:-1)});
  var nbf=L.length;L=L.slice(0,60);
  $('#rows').innerHTML=L.map(function(r){return'<tr><td><b>'+label(r.iso).replace(/ \d{4}$/,'')+'</b><small>'+hm(r.t)+' · '+dur(r.dur)+'</small></td><td><b>'+esc(r.nom)+'</b><small>'+byT(r.type).n+(r.nouveau?' · nouveau patient':'')+(r.chan==='web'?' · en ligne':'')+'</small></td><td class="hide">'+esc(r.motif)+'</td><td class="hide">'+PRA[r.who].n+'</td><td>'+pill(r.statut)+'</td><td><button class="btn o sm" data-id="'+r.id+'" data-d="'+r.iso+'">Voir</button></td></tr>'}).join('')||'<tr><td colspan="6" style="color:var(--mut);padding:30px">Aucun rendez-vous ne correspond.</td></tr>';
  $('#cnt').textContent=nbf+' rendez-vous'+(nbf>60?' · les 60 plus récents sont affichés':'');
}
['#q','#fs','#fp','#fw'].forEach(function(s){$(s).oninput=drawList;$(s).onchange=drawList});
/* ---------- réglages ---------- */
function togg(k,d){var st=localStorage.getItem('osteo-set-'+k);return st===null?d:st==='1'}
function drawSet(){
  var R=[['online','Réservation en ligne activée','Les patients prennent rendez-vous 24 h/24 depuis le site',true],['sms','Rappel SMS la veille','Réduit les absences en moyenne de moitié',true],['mail','E-mail de confirmation immédiat','Avec le lien pour ajouter au calendrier',true],['auto','Confirmation automatique','Sinon, vous validez chaque demande à la main',true],['new','Accepter les nouveaux patients','Désactivez si votre agenda est complet',true]];
  $('#st1').innerHTML=R.map(function(r){return'<div class="row"><span><b>'+r[1]+'</b><small>'+r[2]+'</small></span><button class="tg'+(togg(r[0],r[3])?' on':'')+'" data-k="'+r[0]+'" aria-label="'+r[1]+'"></button></div>'}).join('');
  $('#hh').innerHTML=[1,2,3,4,5,6,0].map(function(d){var s=addDays(TODAY,(d-parse(TODAY).getDay()+7)%7),h=hours(s);return'<div style="grid-template-columns:110px 1fr;padding:9px 0;border-bottom:1px solid #f1ecdf"><span>'+cap1(JF[d])+'</span><b style="font-weight:500">'+(h.length?h.map(function(x){return hm(x[0])+' – '+hm(x[1])}).join(' · '):'Fermé')+'</b></div>'}).join('');
  $('#tt').innerHTML=TYPES.map(function(t){return'<tr><td><b>'+t.n+'</b><small>'+t.d+'</small></td><td>'+dur(t.min)+'</td><td>'+eur(t.p)+'</td><td>'+t.age+'</td></tr>'}).join('');
}
$('#st1').onclick=function(e){var b=e.target.closest('.tg');if(!b)return;b.classList.toggle('on');try{localStorage.setItem('osteo-set-'+b.dataset.k,b.classList.contains('on')?'1':'0')}catch(x){}toast('Réglage enregistré (exemple).')};
/* ---------- fiche + actions ---------- */
function find(id,d){return all(d).filter(function(r){return r.id===id})[0]}
function modal(h){$('#mb').innerHTML=h;$('#md').hidden=false}
function close(){$('#md').hidden=true}
function setStatut(id,s){var st=store();st.st=st.st||{};st.st[id]=s;save(st)}
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-id]');
  if(b&&!b.closest('#md')&&b.dataset.d){var r=find(b.dataset.id,b.dataset.d);if(!r)return;var ty=byT(r.type),fut=r.iso>=TODAY;
    modal('<h3>'+esc(r.nom)+'</h3><p>'+pill(r.statut)+(r.nouveau?' <span class="pill w">Nouveau patient</span>':'')+'</p><dl><dt>Quand</dt><dd>'+label(r.iso)+' à '+hm(r.t)+'</dd><dt>Consultation</dt><dd>'+ty.n+' · '+dur(r.dur)+' · '+eur(ty.p)+'</dd><dt>Motif</dt><dd>'+esc(r.motif)+'</dd><dt>Praticien</dt><dd>'+PRA[r.who].n+'</dd><dt>Réservé via</dt><dd>'+({web:'le site internet',tel:'le téléphone',place:'sur place'})[r.chan]+'</dd>'+(r.tel?'<dt>Téléphone</dt><dd>'+esc(r.tel)+'</dd>':'')+(r.mail?'<dt>E-mail</dt><dd>'+esc(r.mail)+'</dd>':'')+(r.msg?'<dt>Message</dt><dd>'+esc(r.msg)+'</dd>':'')+(r.ref?'<dt>Référence</dt><dd>'+esc(r.ref)+'</dd>':'')+(payOf(r)?'<dt>Paiement</dt><dd>'+money(payOf(r))+' payé en ligne (Stripe) · '+(r.statut==='annulé'?'remboursé':(r.statut==='absent'?'conservé':'réglé intégralement'))+'</dd>':'')+'</dl><div class="acts">'+(r.statut==='confirmé'&&!fut?'<button class="btn" data-act="fait" data-id="'+r.id+'" data-d="'+r.iso+'">Marquer présent</button><button class="btn o" data-act="absent" data-id="'+r.id+'" data-d="'+r.iso+'">Absent</button>':'')+(r.statut==='confirmé'&&fut?'<button class="btn d" data-act="annulé" data-id="'+r.id+'" data-d="'+r.iso+'">Annuler le rendez-vous</button>':'')+'<button class="btn o" data-x>Fermer</button></div>');return}
  var a=e.target.closest('[data-act]');if(a){var id=a.dataset.id;if(id.charAt(0)==='u'||id.charAt(0)==='m'){var st=store();st.st=st.st||{};}setStatut(id,a.dataset.act);close();refresh();toast(a.dataset.act==='annulé'?'Rendez-vous annulé : le créneau est libre.':'Statut mis à jour.');return}
  if(e.target.closest('[data-x]')||e.target===$('#md')){close();return}
});
/* ---------- nouveau rendez-vous ---------- */
$('#nw').onclick=function(){
  modal('<h3>Nouveau rendez-vous</h3><div class="f"><label>Type de consultation<select id="np">'+TYPES.map(function(t){return'<option value="'+t.id+'">'+t.n+' · '+dur(t.min)+' · '+eur(t.p)+'</option>'}).join('')+'</select></label><label>Créneau<select id="nt"></select></label><label>Nom du patient<input id="nn" placeholder="Ex. : Marie Durand"></label><label>Téléphone<input id="ntl" type="tel" placeholder="06 00 00 00 00"></label></div><p class="sub" id="ne" style="color:#b3261e;margin-top:8px"></p><div class="acts"><button class="btn g" id="ng">Ajouter à l’agenda</button><button class="btn o" data-x>Annuler</button></div>');
  function fill(){var t=byT($('#np').value),sl=slotsFor(cur,t,-1).filter(function(x){return x.w>=0});$('#nt').innerHTML=sl.length?sl.map(function(x){return'<option value="'+x.t+'">'+hm(x.t)+' · '+PRA[x.w].n+'</option>'}).join(''):'<option value="">Aucun créneau libre</option>'}
  $('#np').onchange=fill;fill();
  $('#ng').onclick=function(){var t=byT($('#np').value),m=+$('#nt').value,n=$('#nn').value.trim();if(!m){$('#ne').textContent='Aucun créneau libre ce jour-là pour cette consultation.';return}if(n.length<2){$('#ne').textContent='Indiquez le nom du patient.';return}
    var w=freePra(cur,m,t.min,busyList(cur),-1);if(w<0){$('#ne').textContent='Ce créneau vient d’être pris.';return}
    var st=store();st.res.push({id:'m'+Date.now(),iso:cur,t:m,dur:t.min,type:t.id,motif:'Autre',who:w,nom:n,tel:$('#ntl').value.trim(),nouveau:false,statut:'confirmé',chan:'place',lead:0,web:0});save(st);close();refresh();toast('Rendez-vous ajouté à l’agenda.')}};
/* ---------- navigation ---------- */
function drawPay(){
  var on=stripeOn(),i,st=store(),inn=0,fut=0,fees=0,refs=0,keep=0,dd=0;
  all(cur).forEach(function(r){if(r.statut!=='annulé')dd+=payOf(r)});
  $('#kp').insertAdjacentHTML('beforeend','<div class="kpi"><small>Paiements du jour</small><b>'+money(dd)+'</b><i>payés en ligne via Stripe</i></div>');
  for(i=-30;i<=14;i++){var d=parse(TODAY);d.setDate(d.getDate()+i);var s=iso(d);all(s).forEach(function(r){var a=payOf(r);if(!a||r.statut==='annulé')return;if(i<=0){inn+=a;fees+=feeOf(a);if(r.statut==='absent')keep+=a}else fut+=a})}
  (st.ref||[]).forEach(function(x){refs+=x.a});
  $('#pm').innerHTML='<div><small>Paiements encaissés (30 jours)</small><b>'+money(inn)+'</b></div><div><small>Paiements à venir (14 jours)</small><b>'+money(fut)+'</b></div><div><small>Non remboursés (absents)</small><b>'+money(keep)+'</b></div><div><small>Frais Stripe estimés · remboursés '+money(refs)+'</small><b>'+money(fees)+'</b></div>';
  $('#tgs').classList.toggle('on',on);$('#sct').textContent=on?'Compte Stripe connecté':'Paiement désactivé';$('#scs').textContent=on?'Virements automatiques vers votre compte bancaire · IBAN FR76 •••• •••• 4821':'Vos patients réservent sans payer. Réactivez le paiement en ligne.'}
$('#tgs').onclick=function(){try{localStorage.setItem('osteo-set-stripe',stripeOn()?'0':'1')}catch(e){}refresh();toast(stripeOn()?'Paiement en ligne activé.':'Paiement désactivé sur le site.')};
function refresh(){drawDash();drawPay();drawAg();drawList()}
function shift(n){var d=cur;do{d=addDays(d,n)}while(!isOpenDay(d));cur=d;drawAg()}
$('#pv').onclick=function(){shift(-1)};$('#nxd').onclick=function(){shift(1)};
$('#td').onclick=function(){var d=TODAY;while(!isOpenDay(d))d=addDays(d,1);cur=d;drawAg()};
$('#per').onclick=function(e){var b=e.target.closest('button');if(!b)return;per=+b.dataset.p;[].forEach.call($('#per').children,function(x){x.classList.toggle('on',x===b)});drawDash();drawPay()};
var tabs=[].slice.call(document.querySelectorAll('.sb button.t'));
function go(v){tabs.forEach(function(t){t.classList.toggle('on',t.dataset.v===v)});[].forEach.call(document.querySelectorAll('.view'),function(x){x.classList.toggle('on',x.id==='v-'+v)});try{history.replaceState(null,'','#'+v)}catch(e){}window.scrollTo(0,0)}
tabs.forEach(function(t){t.onclick=function(){go(t.dataset.v)}});
refresh();drawSet();
var h0=(location.hash||'').slice(1);if(['dash','agenda','liste','regl'].indexOf(h0)>-1)go(h0);else if(q.get('n')||q.get('d'))go('agenda');
"""


def interne():
    body = INT_BODY.replace("@@I1@@", IC['dash']).replace("@@I2@@", IC['cal']).replace("@@I3@@", IC['list']).replace("@@I4@@", IC['set'])
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Espace cabinet · Statistiques de réservation · Cabinet Lemaire</title><meta name="description" content="Démonstration de l’espace de réservation interne du Cabinet Lemaire (exemple fictif)."><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS}&display=swap">
<style>{INT_CSS}</style></head><body>
{body}
<script>(function(){{{CORE}
{stripe_demo.JS}
{INT_JS}
}})();</script></body></html>"""


def write_all(out):
    open(out + "/osteo-reservation-interne.html", "w").write(interne())
