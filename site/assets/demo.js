
(function(){
  var DAYS=['dimanche','lundi','mardi','mercredi','jeudi','vendredi','samedi'];
  function S(map){var a=[null,null,null,null,null,null,null];map.forEach(function(m){m[0].forEach(function(d){a[d]=m[1]})});return a}
  var M={
    coiffeur:{label:'Coiffeur',def:'Maison Olive',
      sched:S([[[2,3,4,5],[[9,19]]],[[6],[[9,17]]]]),
      rows:[['Mardi au vendredi','9 h – 19 h'],['Samedi','9 h – 17 h'],['Dimanche, lundi','Fermé']],
      addr:'14 rue des Tanneurs, 69003 Lyon · 04 78 00 12 34',
      items:[['Coupe femme','45 min','38 €'],['Coupe homme','30 min','24 €'],['Brushing','30 min','26 €'],['Couleur racines','1 h 15','55 €'],['Balayage','2 h 30','dès 90 €']]},
    restaurant:{label:'Restaurant',def:'La Table d’Alix',
      sched:S([[[2,3,4,5,6],[[12,14.5],[19,22]]],[[0],[[12,15]]]]),
      rows:[['Mardi au samedi','12 h – 14 h 30 · 19 h – 22 h'],['Dimanche','12 h – 15 h'],['Lundi','Fermé']],
      addr:'3 place du Marché, 69001 Lyon · 04 78 00 45 67',
      items:[['Entrée','Velouté de potimarron, éclats de noisette','8 €'],['Plat','Joue de bœuf braisée, purée maison','19 €'],['Plat du jour','Demandez l’ardoise','14 €'],['Dessert','Tarte fine aux pommes tièdes','7 €']]},
    artisan:{label:'Artisan du bâtiment',def:'Durand Plomberie',
      sched:S([[[1,2,3,4,5],[[8,18]]],[[6],[[8,12]]]]),
      rows:[['Lundi au vendredi','8 h – 18 h'],['Samedi','8 h – 12 h'],['Urgences','24 h / 24']],
      addr:'Zone des Chênes, 69120 Vaulx-en-Velin · 06 00 00 12 34',
      stats:[['48 h','devis gratuit'],['2 h','dépannage urgent'],['10 ans','garantie décennale']],
      items:[['Déplacement dépannage','49 €'],['Remplacement mitigeur','dès 120 €'],['Débouchage canalisation','dès 89 €'],['Salle de bains complète','sur devis']]},
    therapeute:{label:'Thérapeute · bien-être',def:'Espace Aurore',
      sched:S([[[1,2,3,4],[[9,19]]],[[5],[[9,13]]]]),
      rows:[['Lundi au jeudi','9 h – 19 h'],['Vendredi','9 h – 13 h'],['Week-end','Fermé']],
      addr:'8 rue des Lilas, 69006 Lyon · 04 78 00 78 90',
      items:[['Première séance','45 min','50 €'],['Séance individuelle','1 h','60 €'],['Séance de couple','1 h 30','80 €']]},
    coach:{label:'Coach sportif',def:'Atelier Rythme',
      sched:S([[[1,2,3,4,5],[[7,20]]],[[6],[[9,13]]]]),
      rows:[['Lundi au vendredi','7 h – 20 h'],['Samedi','9 h – 13 h'],['Dimanche','Fermé']],
      addr:'22 quai Saint-Vincent, 69001 Lyon · 06 00 00 56 78',
      items:[['Séance solo','1 h','45 €'],['Cours collectif','1 h','12 €'],['Carte 10 séances','solo','400 €'],['Bilan de départ','45 min','offert']]},
    boutique:{label:'Boutique de quartier',def:'Lucie & Cie',
      sched:S([[[2,3,4,5,6],[[10,12.5],[14,19]]]]),
      rows:[['Mardi au samedi','10 h – 12 h 30 · 14 h – 19 h'],['Dimanche, lundi','Fermé']],
      addr:'5 rue Mercière, 69002 Lyon · 04 78 00 90 12',
      items:[['Carnet en lin','14 €','#E5C3D3'],['Bougie cire de colza','22 €','#D9B8C9'],['Tote bag brodé','18 €','#EBD3DD'],['Set de 3 crayons','9 €','#CFA9BE']]}
  };
  var KEYS=['coiffeur','restaurant','artisan','therapeute','coach','boutique'];

  function esc(s){return String(s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
  function fh(h){var hh=Math.floor(h),m=Math.round((h-hh)*60);return hh+' h'+(m?' '+(m<10?'0':'')+m:'')}
  function status(k){
    var s=M[k].sched,n=new Date(),d=n.getDay(),t=n.getHours()+n.getMinutes()/60,i,j,r,dd,lab;
    var today=s[d]||[];
    for(j=0;j<today.length;j++){r=today[j];if(t>=r[0]&&t<r[1])return {open:true,text:'Ouvert maintenant · jusqu’à '+fh(r[1])}}
    for(i=0;i<8;i++){
      dd=(d+i)%7;var list=s[dd]||[];
      for(j=0;j<list.length;j++){r=list[j];if(i===0&&r[0]<=t)continue;
        lab=i===0?'aujourd’hui':(i===1?'demain':DAYS[dd]);
        return {open:false,text:'Fermé · ouvre '+lab+' à '+fh(r[0])}}
    }
    return {open:false,text:'Fermé'};
  }
  function open(k){var s=status(k);return '<span class="t-open'+(s.open?' on':'')+'"><i></i>'+s.text+'</span>'}
  function hours(k){return '<dl class="t-hours">'+M[k].rows.map(function(r){return '<div><dt>'+r[0]+'</dt><dd>'+r[1]+'</dd></div>'}).join('')+'</dl>'}
  function acts(a,b){return '<div class="t-actions"><button type="button">'+a+'</button><button type="button" class="alt">'+b+'</button></div>'}

  var R={
    coiffeur:function(n,k){return '<div class="tpl tpl-coiffeur"><div class="t-hero">'+open(k)+'<p class="k">Salon de coiffure</p><h3>'+n+'</h3><p class="t-lead">Coupes, couleurs et soins. Avec ou sans rendez-vous.</p>'+acts('Appeler','Itinéraire')+'</div><div class="t-cols"><section class="t-sec"><h4>Tarifs</h4><ul class="t-menu">'+
      M[k].items.map(function(i){return '<li><span>'+i[0]+'<small>'+i[1]+'</small></span><i class="lead"></i><b>'+i[2]+'</b></li>'}).join('')+'</ul></section><section class="t-sec"><h4>Horaires</h4>'+hours(k)+'<p class="t-addr">'+M[k].addr+'</p></section></div></div>'},
    restaurant:function(n,k){return '<div class="tpl tpl-restaurant"><div class="gingham"></div><div class="t-hero">'+open(k)+'<h3>'+n+'</h3><p class="t-lead">Cuisine de saison, produits de producteurs voisins.</p>'+acts('Réserver par téléphone','Itinéraire')+'<br><span class="formule">Formule midi 17 €</span></div><div class="t-cols"><section class="t-sec"><h4>La carte</h4><ul class="t-cards">'+
      M[k].items.map(function(i){return '<li class="t-card"><em>'+i[0]+'</em><span class="dish">'+i[1]+'</span><b>'+i[2]+'</b></li>'}).join('')+'</ul></section><section class="t-sec"><h4>Horaires</h4>'+hours(k)+'<p class="t-addr">'+M[k].addr+'</p></section></div></div>'},
    artisan:function(n,k){return '<div class="tpl tpl-artisan"><div class="stripe"></div><div class="t-hero">'+open(k)+'<h3>'+n+'</h3><p class="t-lead">Plomberie, chauffage, salle de bains.</p><div class="t-stats">'+
      M[k].stats.map(function(s){return '<div><b>'+s[0]+'</b><span>'+s[1]+'</span></div>'}).join('')+'</div>'+acts('Demander un devis','Appeler')+'</div><div class="t-cols"><section class="t-sec"><h4>Tarifs indicatifs</h4><ul class="t-rows">'+
      M[k].items.map(function(i){return '<li><span>'+i[0]+'</span><b>'+i[1]+'</b></li>'}).join('')+'</ul><p class="urgent"><b>URGENCE</b> · intervention 24 h / 24, 7 j / 7</p></section><section class="t-sec"><h4>Horaires</h4>'+hours(k)+'<p class="t-addr">'+M[k].addr+'</p></section></div></div>'},
    therapeute:function(n,k){return '<div class="tpl tpl-therapeute"><div class="t-hero"><div class="arch"></div>'+open(k)+'<h3 style="margin-top:14px">'+n+'</h3><p class="t-lead">Accompagnement individuel et de couple, dans un cabinet calme.</p>'+acts('Prendre rendez-vous','Itinéraire')+'</div><div class="t-cols"><section class="t-sec"><h4>Séances</h4><ul class="t-menu">'+
      M[k].items.map(function(i){return '<li><span>'+i[0]+'<small>'+i[1]+'</small></span><b>'+i[2]+'</b></li>'}).join('')+'</ul></section><section class="t-sec"><h4>Horaires</h4>'+hours(k)+'<p class="t-addr">'+M[k].addr+'</p></section></div></div>'},
    coach:function(n,k){return '<div class="tpl tpl-coach"><div class="t-hero">'+open(k)+'<h3>'+n+'</h3><p class="t-lead">Séances en solo ou en petit groupe. On commence par un bilan.</p>'+acts('Réserver une séance','Appeler')+'</div><div class="t-cols"><section class="t-sec"><h4>Formules</h4><ul class="t-grid">'+
      M[k].items.map(function(i){return '<li>'+i[0]+'<small>'+i[1]+'</small><b>'+i[2]+'</b></li>'}).join('')+'</ul></section><section class="t-sec"><h4>Horaires</h4>'+hours(k)+'<p class="t-addr">'+M[k].addr+'</p></section></div></div>'},
    boutique:function(n,k){return '<div class="tpl tpl-boutique"><div class="t-hero">'+open(k)+'<h3 style="margin-top:14px">'+n+'</h3><p class="t-lead">Papeterie, déco et idées de cadeaux, choisies une à une.</p>'+acts('Appeler','Itinéraire')+'</div><div class="t-cols"><section class="t-sec"><h4>Nouveautés</h4><ul class="t-prod">'+
      M[k].items.map(function(i){return '<li><div class="ph" style="--c:'+i[2]+'"></div><b>'+i[0]+'</b><span>'+i[1]+'</span></li>'}).join('')+'</ul></section><section class="t-sec"><h4>Horaires</h4>'+hours(k)+'<p class="t-addr">'+M[k].addr+'</p></section></div></div>'}
  };

  function mount(el,k,name,keep){
    var st=keep?el.scrollTop:0;
    el.innerHTML=R[k](esc((name||'').trim()||M[k].def),k);
    el.scrollTop=st;
  }
  function slug(s){return (s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9]+/g,'').slice(0,28)}

  /* appareils : les sites sont dessinés à leur vraie taille puis réduits pour tenir dans le cadre */
  function fit(){
    var list=document.querySelectorAll('.vp');
    Array.prototype.forEach.call(list,function(vp){
      var w=+vp.getAttribute('data-w'),h=+vp.getAttribute('data-h'),s=vp.clientWidth/w,inner=vp.firstElementChild;
      if(!w||!vp.clientWidth)return;
      inner.style.width=w+'px';inner.style.height=h+'px';
      inner.style.transform='scale('+s+')';
      vp.style.height=(h*s)+'px';
    });
  }
  window.addEventListener('resize',fit);
  window.addEventListener('load',fit);

  /* aperçu personnalisé */
  fit();
  if(document.fonts&&document.fonts.ready){document.fonts.ready.then(fit)}

  /* mot qui change dans le bandeau */
  (function(){
    var r=document.querySelector('.rot');
    if(!r||!window.matchMedia||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
    var w=r.children,i=0;
    setInterval(function(){
      var cur=w[i];i=(i+1)%w.length;
      cur.className='out';
      var nx=w[i];nx.className='';
      void nx.offsetWidth;nx.className='on';
      setTimeout(function(){if(cur!==w[i])cur.className=''},500);
    },2400);
  })();

  /* chiffres qui défilent */
  (function(){
    var els=document.querySelectorAll('[data-count]');
    if(!els.length||!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
    function run(el){
      var to=+el.getAttribute('data-count'),t0=null,d=1300;
      function f(ts){
        if(t0===null)t0=ts;
        var p=Math.min(1,(ts-t0)/d),e=1-Math.pow(1-p,3);
        el.textContent=Math.round(to*e);
        if(p<1)requestAnimationFrame(f);
      }
      el.textContent='0';requestAnimationFrame(f);
    }
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){if(e.isIntersecting){io.unobserve(e.target);run(e.target)}});
    },{threshold:.6});
    Array.prototype.forEach.call(els,function(el){io.observe(el)});
  })();
})();

(function(){var r=document.getElementById('exls');if(!r)return;var w=r.parentNode,P=w.querySelector('.prev'),N=w.querySelector('.next'),D=document.getElementById('exdots'),c=[].slice.call(r.children),n=c.length,pos=0,tgt=0,drag=null,raf=0,vel=0,moved=0;
for(var i=0;i<n;i++){D.appendChild(document.createElement('i'))}
function size(){var W=r.clientWidth,cw=Math.min(380,Math.max(250,W*(W<700?.72:.34)));r.style.setProperty('--cw',cw+'px');r.style.height=(cw*0.625+175)+'px';return{W:W,cw:cw}}
function draw(){var z=size(),Rx=z.W<700?z.W*.34:z.W*.36,Rz=z.W<700?110:190,best=0,bd=9;
c.forEach(function(el,i){var d=i-pos;d=((d%n)+n+n/2)%n-n/2;var t=d*2*Math.PI/n,x=Math.sin(t)*Rx,zz=(Math.cos(t)-1)*Rz,sc=.62+.38*(Math.cos(t)+1)/2,ad=Math.abs(d);
 el.style.transform='translate3d(calc(-50% + '+x.toFixed(1)+'px),0,'+zz.toFixed(1)+'px) rotateY('+(-t*28/ (Math.PI/3)).toFixed(1)+'deg) scale('+sc.toFixed(3)+')';
 el.style.zIndex=Math.round(100-ad*10);el.style.opacity=Math.max(.25,1-ad*.28).toFixed(2);el.style.filter=ad<.5?'none':'saturate('+(1-Math.min(ad,2)*.2)+')';
 el.classList.toggle('front',ad<.5);el.style.pointerEvents=ad<.5?'auto':'auto';if(ad<bd){bd=ad;best=i}});
 for(var k=0;k<n;k++)D.children[k].className=k===best?'on':''}
function loop(){raf=0;if(!drag){var d=tgt-pos;if(Math.abs(d)<.002){pos=tgt;draw();return}pos+=d*.14}draw();raf=requestAnimationFrame(loop)}
function kick(){if(!raf)raf=requestAnimationFrame(loop)}
function snap(){tgt=Math.round(pos+vel*6);vel=0;kick()}
function go(d){tgt=Math.round(tgt)+d;kick()}
r.addEventListener('pointerdown',function(e){if(e.button>0)return;drag={x:e.clientX,p:pos,lx:e.clientX};moved=0;vel=0;r.classList.add('grab');kick()});
window.addEventListener('pointermove',function(e){if(!drag)return;var dx=e.clientX-drag.x;moved=Math.max(moved,Math.abs(dx));var step=r.clientWidth/(n*.75);var np=drag.p-dx/step;vel=(np-pos)*.6;pos=np;tgt=pos;drag.lx=e.clientX;if(moved>6&&!r.hasPointerCapture&&e.pointerType!=='mouse'){}});
window.addEventListener('pointerup',function(){if(!drag)return;drag=null;r.classList.remove('grab');snap()});
r.addEventListener('click',function(e){if(moved>6){e.preventDefault();e.stopPropagation();return}var card=e.target.closest('.exl');if(card&&!card.classList.contains('front')){e.preventDefault();var i=c.indexOf(card),d=i-Math.round(pos);d=((d%n)+n+n/2)%n-n/2;go(d)}},true);
r.addEventListener('wheel',function(e){if(Math.abs(e.deltaX)>Math.abs(e.deltaY)&&Math.abs(e.deltaX)>8){e.preventDefault();go(e.deltaX>0?1:-1)}},{passive:false});
r.tabIndex=0;r.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){go(1)}else if(e.key==='ArrowLeft'){go(-1)}});
P.onclick=function(){go(-1)};N.onclick=function(){go(1)};
window.addEventListener('resize',draw);draw()})()
