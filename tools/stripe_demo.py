# -*- coding: utf-8 -*-
"""Paiement « Stripe » pour les sites d'exemple (démonstration).
Aucune carte réelle n'est débitée : le parcours reproduit ce que fait la vraie intégration (Stripe Checkout / Connect) :
saisie de carte, refus possible, reçu, remboursement à l'annulation. Sur un vrai site, la carte est saisie dans les champs
sécurisés de Stripe : elle ne passe jamais par nos serveurs."""

CSS = r"""
.pay{border:1.5px solid var(--pay-ln,#e4ded2);border-radius:16px;padding:18px 20px;background:#fff;display:grid;gap:12px}
.pay-h{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}.pay-h b{font-weight:700}
.pay .stripe{font:800 1.05rem/1 system-ui,sans-serif;letter-spacing:-.02em;color:#635bff;background:#635bff14;padding:6px 10px;border-radius:8px}
.pay-demo{background:#fff8e6;border:1px solid #f0dfae;color:#6e5a1a;border-radius:10px;padding:9px 12px;font-size:13px;line-height:1.4}
.pay label{display:grid;gap:5px;font:600 12px/1.2 system-ui,sans-serif;letter-spacing:.05em;text-transform:uppercase;color:var(--pay-mut,#666)}
.pay input{font:500 16px system-ui,sans-serif;padding:12px 14px;border-radius:10px;border:1.5px solid var(--pay-ln,#e4ded2);background:#fff;color:#111;width:100%;letter-spacing:0;text-transform:none}
.pay input:focus{outline:0;border-color:#635bff;box-shadow:0 0 0 3px #635bff22}.pay-r{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.pay-n{font-size:12.5px;color:var(--pay-mut,#666);margin:0}
.pay-load{display:none;align-items:center;gap:10px;font-size:14px;color:var(--pay-mut,#666)}.pay.busy .pay-load{display:flex}.pay.busy label,.pay.busy .pay-r{opacity:.5;pointer-events:none}
.pay-load i{width:18px;height:18px;border-radius:50%;border:2.5px solid #635bff44;border-top-color:#635bff;animation:payspin .8s linear infinite}@keyframes payspin{to{transform:rotate(360deg)}}
.pay[hidden]{display:none!important}
.recpt{display:inline-flex;gap:8px;align-items:center;background:#f1f0ff;color:#4b43d6;border-radius:10px;padding:8px 14px;font-size:13.5px;font-weight:600;margin-top:6px}
"""

HTML = """<div class="pay" id="pay"><div class="pay-h"><b>Paiement sécurisé</b><span class="stripe">stripe</span></div>
<div class="pay-demo">Mode démonstration : aucune carte réelle n’est débitée. Utilisez 4242 4242 4242 4242, une date future et un code à 3 chiffres. (4000 0000 0000 0002 simule une carte refusée.)</div>
<label>Numéro de carte<input id="spc" inputmode="numeric" autocomplete="cc-number" placeholder="1234 1234 1234 1234" maxlength="23"></label>
<div class="pay-r"><label>Expiration<input id="spe" inputmode="numeric" autocomplete="cc-exp" placeholder="MM / AA" maxlength="7"></label><label>Code (CVC)<input id="spv" inputmode="numeric" autocomplete="cc-csc" placeholder="123" maxlength="4"></label></div>
<div class="pay-load"><i></i><span>Paiement en cours auprès de Stripe…</span></div>
<p class="pay-n">🔒 Vos données bancaires sont saisies et conservées par Stripe, jamais par l’établissement ni par Devanture Web.</p>
<p class="pay-n">En payant, vous acceptez les conditions de vente et d’annulation de l’établissement, et vous demandez que la prestation ait lieu à la date choisie. Vous pouvez annuler avant le rendez-vous et être remboursé selon ces conditions.</p></div>"""

JS = r"""
function luhn(n){var s=0,d=false;for(var i=n.length-1;i>=0;i--){var x=+n.charAt(i);if(d){x*=2;if(x>9)x-=9}s+=x;d=!d}return n.length>=13&&s%10===0}
function spInit(){var c=document.getElementById('spc'),e=document.getElementById('spe');if(!c)return;
 c.addEventListener('input',function(){var v=c.value.replace(/\D/g,'').slice(0,19);c.value=v.replace(/(.{4})/g,'$1 ').trim()});
 e.addEventListener('input',function(){var v=e.value.replace(/\D/g,'').slice(0,4);e.value=v.length>2?v.slice(0,2)+' / '+v.slice(2):v})}
function stripePay(amount){
  return new Promise(function(ok,ko){
    var n=document.getElementById('spc').value.replace(/\D/g,''),ex=document.getElementById('spe').value.replace(/\D/g,''),cv=document.getElementById('spv').value.replace(/\D/g,''),box=document.getElementById('pay');
    if(!luhn(n)){ko('Numéro de carte invalide.');return}
    var mm=+ex.slice(0,2),yy=2000+(+ex.slice(2,4)),now=new Date();
    if(ex.length<4||mm<1||mm>12||yy<now.getFullYear()||(yy===now.getFullYear()&&mm<now.getMonth()+1)){ko('Date d’expiration invalide ou dépassée.');return}
    if(cv.length<3){ko('Code de sécurité invalide.');return}
    box.classList.add('busy');
    setTimeout(function(){box.classList.remove('busy');
      if(n==='4000000000000002'){ko('Votre carte a été refusée. Essayez une autre carte.');return}
      if(n==='4000000000009995'){ko('Fonds insuffisants. Essayez une autre carte.');return}
      ok({id:'pi_3'+Math.random().toString(36).slice(2,12).toUpperCase(),last4:n.slice(-4),brand:n.charAt(0)==='4'?'Visa':(n.charAt(0)==='5'?'Mastercard':(n.charAt(0)==='3'?'American Express':'Carte')),a:amount,t:Date.now()})},1500)})}
function feeOf(a){return Math.round((a*0.015+0.25)*100)/100}
function money(n){return (Math.round(n*100)/100).toLocaleString('fr-FR',{minimumFractionDigits:(n%1?2:0),maximumFractionDigits:2})+' €'}
"""
