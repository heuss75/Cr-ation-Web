from common import *
JS = """() => { const o=[]; const q=s=>[...document.querySelectorAll(s)];
 if(!document.documentElement.lang) o.push('html sans lang');
 if(!document.title) o.push('sans title');
 if(q('h1').length!==1) o.push('h1 x'+q('h1').length);
 q('img').filter(i=>!i.hasAttribute('alt')).forEach(i=>o.push('img sans alt '+i.src.slice(-30)));
 q('input:not([type=hidden]),select,textarea').filter(e=>e.offsetParent).forEach(e=>{const l=e.labels&&e.labels.length||e.getAttribute('aria-label')||e.getAttribute('aria-labelledby')||e.title; if(!l) o.push('champ sans label '+(e.name||e.id||e.type));});
 q('button,a[href]').filter(e=>e.offsetParent && !(e.textContent.trim()||e.getAttribute('aria-label')||e.title||e.querySelector('img[alt]'))).forEach(e=>o.push('bouton/lien sans nom '+(e.id||e.className)));
 const ids={}; q('[id]').forEach(e=>{ids[e.id]=(ids[e.id]||0)+1}); Object.entries(ids).filter(([k,v])=>v>1).forEach(([k])=>o.push('id dupliqué '+k));
 if(!q('main,[role=main]').length) o.push('pas de <main>');
 if(document.documentElement.scrollWidth>innerWidth+1) o.push('débordement horizontal');
 return o }"""
pages = ["/", "/offre", "/faq", "/commander", "/connexion", "/inscription", "/mot-de-passe-oublie", "/cgv", "/confidentialite", "/cookies", "/mentions-legales", "/guide-messagerie", "/admin", "/espace", "/page-inconnue"]
with sync_playwright() as p:
    for w in (1280, 390):
        br, ctx = launch(p, w, 900, mobile=(w < 500)); pg = ctx.new_page()
        for path in pages:
            pg.goto(B + path); pg.wait_for_timeout(700); r = pg.evaluate(JS); print(w, path, "OK" if not r else r)
        br.close()
