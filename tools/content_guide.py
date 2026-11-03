# -*- coding: utf-8 -*-
"""Guide d'installation de la messagerie professionnelle (page publique, même gabarit que les pages légales)."""


def mk(E):
    NAME = E["site_name"]
    pages = {}
    pages["guide-messagerie"] = dict(
        title="Guide messagerie",
        desc="Installer son adresse mail professionnelle sur iPhone, Android, Thunderbird ou Outlook, ou la lire depuis un navigateur : réglages et étapes.",
        lede="Installer votre adresse mail professionnelle sur votre téléphone ou votre ordinateur, pas à pas. Comptez cinq minutes.",
        notice="Ce guide est fourni avec la formule Pro. Avec la formule Essentiel, il est fourni à l’achat d’une adresse mail pro.",
        body="""
<h2 id="avant">1. Avant de commencer</h2>
<nav class="gm-dev" aria-label="Choisir votre appareil"><span>Je suis sur :</span><a href="#iphone">iPhone / iPad</a><a href="#android">Android</a><a href="#thunderbird">Thunderbird</a><a href="#outlook">Outlook</a><a href="#webmail">Webmail</a></nav>
<figure class="gm-fig"><svg viewBox="0 0 560 190" role="img" aria-label="Votre boîte mail est stockée sur un serveur et synchronisée avec le téléphone, l’ordinateur et le webmail" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,sans-serif">
<rect x="1" y="1" width="558" height="188" rx="16" fill="var(--surface)" stroke="var(--line)"/>
<rect x="215" y="52" width="130" height="86" rx="14" fill="var(--ink)"/><rect x="233" y="70" width="94" height="10" rx="5" fill="#17C26E"/><rect x="233" y="90" width="94" height="10" rx="5" fill="var(--muted)" opacity=".6"/><rect x="233" y="110" width="94" height="10" rx="5" fill="var(--muted)" opacity=".6"/><text x="280" y="158" font-size="12" font-weight="700" fill="var(--ink)" text-anchor="middle">Votre boîte mail</text><text x="280" y="174" font-size="11" fill="var(--muted)" text-anchor="middle">sur le serveur (IMAP)</text>
<g stroke="#17C26E" stroke-width="2.5" fill="none" stroke-linecap="round"><path d="M215 80H152"/><path d="M215 95H152"/><path d="M345 80h63"/><path d="M345 95h63"/><path d="M280 52V30"/></g>
<rect x="104" y="46" width="48" height="84" rx="9" fill="var(--surface)" stroke="var(--ink)" stroke-width="3"/><rect x="112" y="58" width="32" height="5" rx="2.5" fill="var(--muted)"/><rect x="112" y="70" width="32" height="5" rx="2.5" fill="var(--muted)"/><circle cx="128" cy="118" r="4" fill="var(--ink)"/><text x="128" y="150" font-size="12" font-weight="700" fill="var(--ink)" text-anchor="middle">Téléphone</text>
<rect x="408" y="52" width="86" height="58" rx="7" fill="var(--surface)" stroke="var(--ink)" stroke-width="3"/><path d="M398 118h106l-8 9h-90z" fill="var(--ink)"/><rect x="418" y="64" width="50" height="5" rx="2.5" fill="var(--muted)"/><rect x="418" y="76" width="66" height="5" rx="2.5" fill="var(--muted)"/><text x="451" y="150" font-size="12" font-weight="700" fill="var(--ink)" text-anchor="middle">Ordinateur</text>
<rect x="250" y="8" width="60" height="22" rx="11" fill="var(--soft)"/><text x="280" y="23" font-size="11" font-weight="700" fill="var(--ink)" text-anchor="middle">Webmail</text></svg>
<figcaption>Vos messages restent sur le serveur : ce que vous lisez, envoyez ou supprimez sur un appareil apparaît sur les autres.</figcaption></figure>
<div class="gm-cards"><div><b>1</b><span>Votre adresse<small>ex. contact@votrecommerce.fr</small></span></div><div><b>2</b><span>Votre mot de passe<small>provisoire, à changer ensuite</small></span></div><div><b>3</b><span>Le webmail<small>l’adresse de connexion web</small></span></div></div>
<p>Nous vous avons envoyé trois choses : votre <strong>adresse mail professionnelle</strong> (par exemple <em>contact@votrecommerce.fr</em>), un <strong>mot de passe provisoire</strong> et l’adresse du <strong>webmail</strong>. Gardez-les sous la main. Si un des trois vous manque, écrivez-nous depuis votre espace client.</p>
<p>Quel que soit l’appareil, ce sont toujours les mêmes réglages. Voici le tableau à garder :</p>
<table>
<caption>Réglages de votre adresse mail pro</caption>
<thead><tr><th scope="col">Quoi</th><th scope="col">Réglage</th></tr></thead>
<tbody>
<tr><th scope="row">Nom d’utilisateur</th><td>Votre <strong>adresse complète</strong> (pas seulement le début)</td></tr>
<tr><th scope="row">Mot de passe</th><td>Celui que nous vous avons envoyé</td></tr>
<tr><th scope="row">Type de compte</th><td><strong>IMAP</strong> (et non POP)</td></tr>
<tr><th scope="row">Serveur de réception (IMAP)</th><td><code>imap.mail.ovh.net</code> <button type="button" class="gm-copy" data-copy="imap.mail.ovh.net" aria-label="Copier imap.mail.ovh.net">Copier</button>, port <strong>993</strong>, sécurité <strong>SSL/TLS</strong></td></tr>
<tr><th scope="row">Serveur d’envoi (SMTP)</th><td><code>smtp.mail.ovh.net</code> <button type="button" class="gm-copy" data-copy="smtp.mail.ovh.net" aria-label="Copier smtp.mail.ovh.net">Copier</button>, port <strong>465</strong>, sécurité <strong>SSL/TLS</strong></td></tr>
<tr><th scope="row">Identification du serveur d’envoi</th><td>Oui, avec la même adresse et le même mot de passe</td></tr>
</tbody>
</table>
<p class="callout"><strong>Pourquoi IMAP ?</strong> Vos mails restent sur le serveur : vous retrouvez les mêmes messages sur votre téléphone, votre ordinateur et le webmail. Un mail lu ou supprimé sur un appareil l’est partout.</p>

<h2 id="iphone">2. iPhone et iPad (application Mail)</h2>
<p>Rien à télécharger : l’application Mail est déjà installée.</p>
<ol class="gm">
<li>Ouvrez <strong>Réglages</strong>, puis <strong>Mail</strong> (sur les versions récentes : <strong>Apps</strong>, puis <strong>Mail</strong>), puis <strong>Comptes de messagerie</strong>.</li>
<li>Touchez <strong>Ajouter un compte</strong>, puis <strong>Autre</strong>, puis <strong>Ajouter un compte Mail</strong>.</li>
<li>Saisissez votre nom, votre adresse mail pro, votre mot de passe et une description (par exemple « Pro »). Touchez <strong>Suivant</strong>.</li>
<li>Choisissez <strong>IMAP</strong> en haut de l’écran.</li>
<li>Serveur de réception : nom d’hôte <code>imap.mail.ovh.net</code>, nom d’utilisateur = votre adresse complète, mot de passe.</li>
<li>Serveur d’envoi : nom d’hôte <code>smtp.mail.ovh.net</code>, nom d’utilisateur = votre adresse complète, mot de passe.</li>
<li>Touchez <strong>Suivant</strong>, puis <strong>Enregistrer</strong>. Si le téléphone demande des ports, indiquez 993 pour la réception et 465 pour l’envoi, avec SSL.</li>
</ol>
<p>Pour envoyer vos mails depuis cette adresse par défaut : <strong>Réglages</strong>, <strong>Mail</strong>, <strong>Compte par défaut</strong>.</p>

<h2 id="android">3. Android (application Gmail)</h2>
<p>L’application Gmail, déjà installée sur la plupart des téléphones Android, accepte les adresses d’autres fournisseurs. Vous n’avez pas besoin d’un compte Gmail personnel pour y ajouter votre adresse pro.</p>
<ol class="gm">
<li>Ouvrez <strong>Gmail</strong>, touchez votre photo ou votre initiale en haut à droite, puis <strong>Ajouter un autre compte</strong>.</li>
<li>Choisissez <strong>Autre</strong>, saisissez votre adresse mail pro et touchez <strong>Suivant</strong>.</li>
<li>Choisissez <strong>Personnel (IMAP)</strong>, puis saisissez votre mot de passe.</li>
<li>Serveur de réception : <code>imap.mail.ovh.net</code>, sécurité SSL/TLS, port 993. Nom d’utilisateur : votre adresse complète.</li>
<li>Serveur d’envoi : <code>smtp.mail.ovh.net</code>, sécurité SSL/TLS, port 465. Cochez « Connexion requise », avec votre adresse complète et votre mot de passe.</li>
<li>Terminez avec <strong>Suivant</strong>. Réglez la fréquence de synchronisation sur « Toujours » pour recevoir vos mails tout de suite.</li>
</ol>
<p>Les noms des menus peuvent varier un peu d’un téléphone à l’autre. Les réglages, eux, restent ceux du tableau.</p>

<h2 id="thunderbird">4. Ordinateur : Thunderbird (gratuit)</h2>
<p><a href="https://www.thunderbird.net/fr/" target="_blank" rel="noopener">Thunderbird</a> est un logiciel de messagerie gratuit, pour Windows, Mac et Linux. Nous le recommandons pour son côté simple et sans publicité.</p>
<ol class="gm">
<li>Installez Thunderbird, puis ouvrez-le. Au premier lancement, il propose de configurer un compte. Sinon : menu (trois barres), <strong>Nouveau</strong>, puis <strong>Compte courrier</strong>.</li>
<li>Saisissez votre nom, votre adresse mail pro et votre mot de passe, puis cliquez sur <strong>Continuer</strong>.</li>
<li>Si Thunderbird trouve seul les réglages, vérifiez qu’il indique <strong>IMAP</strong>. Sinon, cliquez sur <strong>Configurer manuellement</strong> et remplissez avec le tableau du début.</li>
<li>Pour la réception et l’envoi, choisissez <strong>SSL/TLS</strong> et l’authentification <strong>Mot de passe normal</strong>. Le nom d’utilisateur est votre adresse complète.</li>
<li>Cliquez sur <strong>Terminé</strong>.</li>
</ol>

<h2 id="outlook">5. Ordinateur : Outlook</h2>
<p>Outlook sait aussi lire une adresse d’un autre fournisseur.</p>
<ol class="gm">
<li>Dans Outlook, ouvrez <strong>Fichier</strong>, puis <strong>Ajouter un compte</strong> (dans le nouvel Outlook : <strong>Paramètres</strong>, <strong>Comptes</strong>, <strong>Ajouter un compte</strong>).</li>
<li>Saisissez votre adresse mail pro, puis cliquez sur <strong>Options avancées</strong> et cochez <strong>Je veux configurer manuellement mon compte</strong>.</li>
<li>Choisissez <strong>IMAP</strong>.</li>
<li>Saisissez les réglages du tableau : serveur et port pour la réception, serveur et port pour l’envoi, SSL/TLS, puis votre mot de passe.</li>
<li>Cliquez sur <strong>Connecter</strong>.</li>
</ol>

<h2 id="webmail">6. Sans rien installer : le webmail</h2>
<p>Vous pouvez lire et envoyer vos mails depuis n’importe quel navigateur, sur un ordinateur de passage par exemple. Ouvrez l’adresse du webmail que nous vous avons envoyée et connectez-vous avec votre adresse complète et votre mot de passe.</p>

<h2 id="bonnes-pratiques">7. Bonnes pratiques</h2>
<div class="gm-tips">
<div><b>Changez le mot de passe provisoire</b><p>Dès la première connexion, choisissez un mot de passe long et unique, que vous n’utilisez nulle part ailleurs. Mettez ensuite à jour les appareils.</p></div>
<div><b>Une signature professionnelle</b><p>Nom, activité, téléphone, adresse du site. Elle rassure et vous fait gagner du temps.</p></div>
<div><b>Gardez l’adresse sur tous vos supports</b><p>Site, cartes de visite, devis, factures, fiche Google : la même adresse partout.</p></div>
<div><b>Méfiez-vous des faux messages</b><p>Nous ne vous demandons jamais votre mot de passe par mail. Ne cliquez pas sur un lien qui vous presse de « confirmer votre compte ».</p></div>
</div>
<h2 id="probleme">8. Ça ne marche pas ?</h2>
<ul>
<li><strong>« Mot de passe incorrect ».</strong> Vérifiez que le nom d’utilisateur est l’adresse <strong>complète</strong> et recopiez le mot de passe sans espace en fin. Essayez-le d’abord dans le webmail : s’il y fonctionne, le problème vient du réglage de l’application.</li>
<li><strong>Je reçois mais je n’envoie pas.</strong> Le serveur d’envoi doit être <code>smtp.mail.ovh.net</code>, avec le port 465, SSL/TLS et l’identification activée. Ne gardez pas le serveur d’envoi de votre fournisseur d’accès à internet.</li>
<li><strong>Mon message est arrivé chez le destinataire dans les courriers indésirables.</strong> C’est fréquent au début avec une nouvelle adresse. Demandez à votre correspondant de la marquer comme « fiable » ; ça s’améliore ensuite.</li>
<li><strong>Je vois mes mails sur le téléphone mais pas sur l’ordinateur.</strong> Vérifiez que les deux appareils sont en <strong>IMAP</strong>. En POP, un mail téléchargé quelque part disparaît du serveur.</li>
<li><strong>J’ai oublié mon mot de passe.</strong> Écrivez-nous depuis votre espace client : nous le réinitialisons et nous vous en envoyons un nouveau.</li>
</ul>
<p>Si rien de cela ne règle votre problème, contactez-nous depuis votre espace client en précisant votre appareil (iPhone, Android, ordinateur) et ce que vous voyez à l’écran.</p>
""",
    )
    return pages
