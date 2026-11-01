# -*- coding: utf-8 -*-
"""Textes légaux. Les informations d'identité de l'éditeur viennent de EDITOR (build.py).
Un champ vide s'affiche en jaune « À compléter » pour ne jamais passer inaperçu."""


def mk(E):
    def v(key, label):
        val = E.get(key, "").strip()
        return val if val else '<mark class="todo">[À compléter : %s]</mark>' % label

    NOM = v("nom", "nom ou raison sociale")
    STATUT = v("statut", "statut juridique, par exemple entrepreneur individuel")
    SIRET = v("siret", "numéro SIRET")
    ADRESSE = v("adresse", "adresse postale")
    TEL = v("tel", "téléphone")
    MAIL = v("email", "adresse e-mail de contact")
    DIR = v("directeur", "directeur de la publication")
    TVA = v("tva", "mention de TVA : numéro de TVA ou « TVA non applicable, article 293 B du CGI »")
    TRIB = v("tribunal", "ville du tribunal compétent (siège de l’éditeur)")
    NAME = E["site_name"]

    pages = {}

    # ------------------------------------------------------------------ mentions légales
    pages["mentions-legales"] = dict(
        title="Mentions légales",
        desc="Mentions légales du site %s : éditeur, hébergeur, propriété intellectuelle." % NAME,
        lede="Les informations légales sur l’éditeur et l’hébergeur du site.",
        body="""
<h2 id="editeur">1. Éditeur du site</h2>
<p>Le site <strong>%(NAME)s</strong> est édité par :</p>
<ul>
<li>Nom ou raison sociale : %(NOM)s</li>
<li>Statut : %(STATUT)s</li>
<li>SIRET : %(SIRET)s</li>
<li>Adresse : %(ADRESSE)s</li>
<li>Téléphone : %(TEL)s</li>
<li>E-mail : %(MAIL)s</li>
<li>%(TVA)s</li>
</ul>
<p>Directeur de la publication : %(DIR)s.</p>

<h2 id="hebergeur">2. Hébergeur</h2>
<p>Le site est hébergé par <strong>Cloudflare, Inc.</strong>, 101 Townsend Street, San Francisco, CA 94107, États-Unis. Site : <a href="https://www.cloudflare.com" rel="noopener" target="_blank">www.cloudflare.com</a>.</p>
<p>Le code source du site est conservé sur la plateforme GitHub (GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis).</p>

<h2 id="activite">3. Activité</h2>
<p>%(NAME)s propose la création et l’hébergement de sites vitrines clé en main pour les commerces et les indépendants, sous forme d’abonnement. Les conditions de l’offre figurent dans les <a href="/cgv">conditions générales de vente</a>.</p>

<h2 id="propriete">4. Propriété intellectuelle</h2>
<p>Les textes, images, graphismes, logos et le code du site %(NAME)s sont protégés par le droit d’auteur et par le droit des marques. Toute reproduction, représentation ou adaptation, totale ou partielle, sans autorisation écrite préalable, est interdite.</p>
<p>Les sites d’exemples montrés sur cette page (salon de coiffure, restaurant, etc.) sont des maquettes de démonstration. Les noms, adresses, numéros de téléphone et tarifs qui y figurent sont fictifs.</p>

<h2 id="responsabilite">5. Responsabilité</h2>
<p>Nous nous efforçons de fournir des informations exactes et à jour, mais nous ne pouvons pas garantir qu’elles soient exemptes d’erreur ou d’omission. Le site peut être interrompu pour maintenance. Les liens vers des sites tiers sont fournis à titre d’information : nous ne contrôlons pas leur contenu.</p>

<h2 id="donnees">6. Données personnelles et cookies</h2>
<p>Le traitement de vos données est décrit dans la <a href="/confidentialite">politique de confidentialité</a>. L’usage des cookies et des stockages locaux est décrit dans la <a href="/cookies">page cookies</a>.</p>

<h2 id="droit">7. Droit applicable</h2>
<p>Le présent site est soumis au droit français. En cas de litige, et à défaut de résolution amiable, les tribunaux français sont compétents.</p>

<h2 id="contact">8. Contact</h2>
<p>Pour toute question, utilisez la <a href="/commander">demande en ligne</a>%(MAILSENT)s.</p>
""" % dict(NAME=NAME, NOM=NOM, STATUT=STATUT, SIRET=SIRET, ADRESSE=ADRESSE, TEL=TEL, MAIL=MAIL, DIR=DIR, TVA=TVA,
           MAILSENT=(" ou écrivez à " + E["email"]) if E.get("email") else ""))

    # ------------------------------------------------------------------ CGV
    pages["cgv"] = dict(
        title="Conditions générales de vente",
        desc="Conditions générales de vente de l’abonnement %s : prix, durée, résiliation, modifications, nom de domaine." % NAME,
        lede="Les règles de l’abonnement, en clair : prix, durée de 12 mois, modifications, nom de domaine, résiliation.",
        notice="Ces conditions s’appliquent aux commandes passées par des professionnels. Elles seront complétées à l’ouverture du paiement en ligne.",
        body="""
<div class="callout"><strong>En résumé.</strong> Un site vitrine, un nom de domaine, un hébergement, un espace client et un guide pub avec un engagement de <strong>12 mois</strong>, en deux formules : <strong>Essentiel à 60 € HT par mois</strong> et <strong>Pro à 100 € HT par mois</strong> (réservation en ligne et une adresse mail pro incluses). Une modification par mois est comprise. Chaque adresse mail pro supplémentaire coûte 4 € HT par mois. Ce résumé n’a pas de valeur contractuelle : seuls les articles ci-dessous s’appliquent.</div>

<h2 id="art-1">Article 1. Objet et champ d’application</h2>
<p>Les présentes conditions générales de vente (« CGV ») régissent la vente de l’abonnement « %(NAME)s » proposé par %(NOM)s (%(STATUT)s, SIRET %(SIRET)s, %(ADRESSE)s), ci-après « l’Éditeur », à toute personne agissant pour les besoins de son activité professionnelle, ci-après « le Client ».</p>
<p>Le Client déclare agir à des fins professionnelles. Toute commande suppose l’acceptation sans réserve des CGV en vigueur au jour de la commande.</p>

<h2 id="art-2">Article 2. Description de l’offre</h2>
<p>L’abonnement comprend :</p>
<ul>
<li>la conception d’un site vitrine, adapté au téléphone, à partir des informations et contenus fournis par le Client ;</li>
<li>la réservation et le renouvellement annuel d’un nom de domaine pendant la durée de l’engagement ;</li>
<li>l’hébergement du site, avec certificat HTTPS ;</li>
<li>un espace client de suivi et un éditeur de modifications (article 9) ;</li>
<li>un guide pub : document d’aide pour faire connaître son activité.</li>
</ul>
<p><strong>Formules :</strong> l’abonnement existe en formule « Essentiel » et en formule « Pro ». La formule Pro comprend en plus la réservation en ligne et une adresse mail professionnelle (article 11 bis). <strong>Option :</strong> adresse mail professionnelle supplémentaire (article 11).</p>
<p><strong>Ne sont pas compris :</strong> la publicité réalisée pour le compte du Client, le référencement payant, une boutique en ligne, un système de réservation en ligne (sauf dans la formule Pro), les pages au-delà de cinq, la refonte complète du design, la rédaction de contenus volumineux et la production de photographies. Ces prestations peuvent faire l’objet d’un devis séparé.</p>

<h2 id="art-3">Article 3. Commande et formation du contrat</h2>
<p>Le Client remplit la demande en ligne, qui est sans engagement. L’Éditeur vérifie la faisabilité, confirme les éléments de la commande (activité, nom de domaine souhaité, option mail) et transmet au Client un récapitulatif.</p>
<p>Le contrat est formé lorsque le Client a accepté les présentes CGV <strong>et</strong> que le premier paiement mensuel a été reçu par l’Éditeur. L’Éditeur peut refuser une commande pour motif légitime (contenu illicite, nom de domaine contrevenant à des droits de tiers, impayé antérieur).</p>

<h2 id="art-4">Article 4. Prix et paiement</h2>
<ul>
<li>Formule Essentiel : <strong>60 € HT par mois</strong>.</li>
<li>Formule Pro : <strong>100 € HT par mois</strong>.</li>
<li>Adresse mail professionnelle : <strong>4 € HT par mois et par adresse</strong> (la première est incluse dans la formule Pro).</li>
</ul>
<p>Les prix sont exprimés en euros, hors taxes. %(TVA)s La TVA applicable, le cas échéant, figure sur chaque facture. Le prix de l’abonnement ne change pas pendant la durée de l’engagement en cours.</p>
<p>Le paiement est mensuel et d’avance, par carte bancaire ou prélèvement SEPA, par l’intermédiaire d’un prestataire de paiement sécurisé. L’Éditeur ne conserve pas les données de carte bancaire. Une facture est mise à disposition dans l’espace client.</p>
<p>En cas de retard de paiement, des pénalités de retard sont dues de plein droit, au taux de trois fois le taux d’intérêt légal, à compter de la date d’échéance et sans mise en demeure préalable, ainsi qu’une indemnité forfaitaire pour frais de recouvrement de 40 € (articles L441-10 et D441-5 du Code de commerce). L’Éditeur peut en outre suspendre le site après mise en demeure restée sans effet pendant 8 jours.</p>

<h2 id="art-5">Article 5. Durée et reconduction</h2>
<p>L’abonnement est conclu pour une durée initiale de <strong>12 mois</strong> à compter de la mise en ligne du site. Il est ensuite reconduit tacitement par périodes successives de 12 mois, sauf résiliation par le Client dans les conditions de l’article 17.</p>
<p>L’Éditeur adresse au Client un rappel écrit au plus tard 60 jours avant chaque échéance. Si le Client est une personne non professionnelle au sens de l’article L215-1 du Code de la consommation, ce rappel est envoyé entre trois mois et un mois avant la fin de la période de non-reconduction, et mentionne la possibilité de ne pas reconduire.</p>

<h2 id="art-6">Article 6. Délai de livraison et mise en ligne</h2>
<p>Le site est livré sous <strong>5 jours ouvrés à compter de la réception de tous les contenus nécessaires</strong> (textes, photos, horaires, tarifs, coordonnées, choix du nom de domaine). Ce délai est indicatif et se décompte à partir d’un dossier complet : tout retard du Client à fournir ou valider les éléments suspend le délai d’autant.</p>
<p>Un aperçu est mis à disposition du Client, qui formule ses demandes d’ajustement avant de valider. Le site est mis en ligne après la validation du Client. À défaut de réponse du Client dans un délai de 15 jours après l’envoi de l’aperçu et d’une relance, la période d’abonnement et la facturation débutent à la date de cette relance.</p>

<h2 id="art-7">Article 7. Obligations du Client</h2>
<p>Le Client s’engage à : fournir des informations exactes et complètes ; disposer des droits sur les textes, photos, logos et marques qu’il transmet ; ne publier aucun contenu illicite, diffamatoire, contrefaisant ou contraire à l’ordre public ; garder confidentiels ses identifiants d’accès ; et signaler sans délai toute erreur ou usage frauduleux.</p>
<p>Le Client demeure seul responsable du contenu de son site et de la légalité de son activité.</p>

<h2 id="art-8">Article 8. Contenus et relecture</h2>
<p>L’Éditeur met en forme les contenus fournis et corrige les fautes de langue évidentes. Il relit le site avant mise en ligne : textes, photos, liens, affichage sur téléphone. Le Client reste responsable de l’exactitude des informations (horaires, prix, adresse) et des mentions légales propres à son activité.</p>

<h2 id="art-9">Article 9. Modifications comprises dans l’abonnement</h2>
<p>Le Client dispose d’<strong>une modification par mois</strong> (<strong>trois</strong> dans la formule Pro), qu’il réalise lui-même depuis l’éditeur de son espace client. Une modification consiste en : le remplacement d’un texte, le remplacement d’une photo, l’ajout d’un bloc de contenu ou la suppression d’un bloc de contenu.</p>
<ul>
<li>Les modifications non utilisées ne se cumulent pas d’un mois sur l’autre.</li>
<li>Le Client peut annuler une modification ; un historique est conservé.</li>
<li>L’éditeur ne permet pas de changer la mise en page, ce qui garantit la stabilité du site.</li>
<li>Une nouvelle page, une refonte du design ou une fonctionnalité supplémentaire ne sont pas comprises et font l’objet d’un devis.</li>
<li>L’Éditeur peut annuler ou corriger une modification contraire à la loi ou aux présentes CGV.</li>
</ul>

<h2 id="art-10">Article 10. Nom de domaine</h2>
<p>L’Éditeur réserve, gère et renouvelle chaque année le nom de domaine choisi pendant la durée de l’engagement ; ce coût est compris dans l’abonnement. La disponibilité d’un nom n’est pas garantie : l’Éditeur propose des variantes si le nom souhaité est pris. Le Client garantit que le nom choisi ne porte pas atteinte aux droits de tiers.</p>
<p>À la fin de l’abonnement, et sous réserve du paiement de toutes les sommes dues, le Client peut demander le transfert de son nom de domaine ; l’Éditeur lui remet le code de transfert dans un délai raisonnable. Si le Client utilise un nom de domaine qu’il possédait déjà, ce nom reste chez son prestataire d’origine et son renouvellement reste à sa charge.</p>

<h2 id="art-11">Article 11. Adresse mail professionnelle (option)</h2>
<p>Chaque adresse est facturée 4 € HT par mois, sauf la première adresse de la formule Pro qui est incluse, et suit la durée de l’abonnement. La boîte est de taille limitée, pour un usage professionnel normal ; l’envoi de messages en masse ou non sollicités est interdit. En cas de fin d’abonnement, les adresses sont fermées 30 jours après la date de fin, pour permettre au Client de récupérer ses messages.</p>

<h2 id="art-11b">Article 11 bis. Formule Pro : réservation en ligne</h2>
<p>La formule Pro comprend un module de réservation en ligne intégré au site du Client : le visiteur choisit une prestation, un jour et un créneau disponible, et laisse ses coordonnées. Un créneau réservé n’est plus proposé. Les réservations sont consultables dans l’agenda de l’espace client.</p>
<ul>
<li>L’Éditeur paramètre, à partir des informations fournies par le Client, les prestations, leurs durées et les horaires d’ouverture ; l’activation de la réservation intervient dans les 2 jours ouvrés suivant la validation du site. Les modifications ultérieures des prestations et horaires comptent comme une modification au sens de l’article 9.</li>
<li>Ne sont pas compris : le paiement ou l’acompte en ligne, les rappels par SMS, la synchronisation avec un agenda externe et toute fonctionnalité non décrite ci-dessus, qui peuvent faire l’objet d’un devis.</li>
<li>Le Client reste responsable de l’honneur des rendez-vous, de ses conditions d’annulation et de l’information de ses propres clients. Pour les données personnelles de ces clients (nom, téléphone), le Client est responsable de traitement et l’Éditeur son sous-traitant, comme prévu à l’article 14.</li>
<li>Le Client peut passer de la formule Essentiel à la formule Pro à tout moment, avec effet au début du mois suivant ; une nouvelle période d’engagement de 12 mois court alors à compter de ce changement. Le passage du Pro à l’Essentiel n’est possible qu’à l’échéance de la période en cours.</li>
</ul>

<h2 id="art-12">Article 12. Hébergement, disponibilité et sauvegardes</h2>
<p>Le site est hébergé sur l’infrastructure de Cloudflare. L’Éditeur est tenu d’une obligation de moyens quant à la disponibilité du site et de l’espace client. Des interruptions peuvent survenir pour maintenance, mise à jour ou du fait de tiers (hébergeur, réseau, fournisseurs de noms de domaine). Aucun niveau de disponibilité n’est garanti.</p>

<h2 id="art-13">Article 13. Propriété intellectuelle</h2>
<p><strong>Contenus du Client.</strong> Le Client conserve la propriété de ses textes, photos, logos et marques. Il concède à l’Éditeur le droit de les reproduire et de les diffuser sur son site pendant la durée de l’abonnement, pour les besoins de la prestation.</p>
<p><strong>Création de l’Éditeur.</strong> Le code, les modèles, la structure et les éléments graphiques conçus par l’Éditeur restent sa propriété. Pendant l’abonnement, l’Éditeur concède au Client un droit d’utilisation non exclusif, non cessible, pour exploiter son site. À la fin de l’abonnement, le Client peut récupérer ses contenus (textes et photos) sur simple demande.</p>
<p>L’Éditeur peut citer le site réalisé comme référence, sauf opposition écrite du Client.</p>

<h2 id="art-14">Article 14. Données personnelles</h2>
<p>L’Éditeur traite les données du Client conformément à sa <a href="/confidentialite">politique de confidentialité</a>. Pour les données personnelles des visiteurs du site du Client (par exemple via un formulaire de contact), le Client est responsable de traitement et l’Éditeur agit en qualité de sous-traitant ; l’Éditeur ne traite ces données que sur instruction du Client, assure leur sécurité et aide le Client à répondre aux demandes d’exercice de droits. Un accord de sous-traitance peut être fourni sur demande.</p>

<h2 id="art-15">Article 15. Responsabilité</h2>
<p>L’Éditeur ne garantit aucun résultat : nombre de visites, position dans les moteurs de recherche, chiffre d’affaires ou nombre de clients. Le guide pub est une aide et ne constitue pas une promesse de résultat.</p>
<p>La responsabilité de l’Éditeur ne peut être engagée qu’en cas de faute prouvée, et se limite aux dommages directs. Elle est plafonnée, toutes causes confondues, au montant des sommes effectivement payées par le Client au cours des 12 derniers mois précédant le fait générateur. L’Éditeur n’est pas responsable des dommages indirects (perte de chiffre d’affaires, de clientèle, d’image, de données). Ces limites ne s’appliquent pas en cas de faute lourde ou dolosive, ni dans les cas où la loi l’interdit.</p>

<h2 id="art-16">Article 16. Force majeure</h2>
<p>Aucune partie ne peut être tenue responsable d’un manquement dû à un cas de force majeure au sens de l’article 1218 du Code civil, notamment une panne générale de réseau ou d’un hébergeur, une cyberattaque d’envergure ou une décision d’autorité publique.</p>

<h2 id="art-17">Article 17. Résiliation</h2>
<p><strong>Par le Client.</strong> Le Client peut résilier à l’échéance de chaque période de 12 mois, par écrit (e-mail ou courrier) avec un préavis d’au moins 30 jours avant cette échéance. Un bouton de résiliation sera proposé dans l’espace client. Pendant la période d’engagement en cours, les mensualités restantes demeurent dues et ne donnent lieu à aucun remboursement.</p>
<p><strong>Pour manquement.</strong> Chaque partie peut résilier le contrat en cas de manquement grave de l’autre partie non réparé 15 jours après une mise en demeure par écrit. Si le manquement est le fait de l’Éditeur, les sommes versées pour la période non consommée sont remboursées au prorata.</p>
<p><strong>Effets.</strong> À la fin du contrat, le site est mis hors ligne, les accès sont fermés, et les articles 10 (transfert du domaine), 11 (fermeture du mail) et 13 (récupération des contenus) s’appliquent.</p>

<h2 id="art-18">Article 18. Droit de rétractation</h2>
<p>L’offre s’adresse aux professionnels : le droit de rétractation prévu par le Code de la consommation ne s’applique pas. Avant le premier paiement, la demande du Client reste sans engagement.</p>

<h2 id="art-19">Article 19. Réclamations</h2>
<p>Toute réclamation peut être adressée à l’Éditeur par la <a href="/commander">demande en ligne</a>%(MAILSENT)s. L’Éditeur s’engage à accuser réception et à rechercher une solution amiable. Si le Client est une personne non professionnelle, il peut recourir gratuitement à un médiateur de la consommation dont les coordonnées sont communiquées sur demande.</p>

<h2 id="art-20">Article 20. Modification des CGV</h2>
<p>Les CGV applicables sont celles en vigueur à la date de la commande. L’Éditeur peut les modifier pour l’avenir ; les contrats en cours se poursuivent aux conditions initiales jusqu’à leur échéance, sauf évolution légale impérative ou modification favorable au Client. Toute modification défavorable pour le Client est notifiée au moins 30 jours avant son application et lui permet de ne pas reconduire l’abonnement.</p>

<h2 id="art-21">Article 21. Droit applicable et litiges</h2>
<p>Les CGV sont soumises au droit français. En cas de litige entre professionnels, et à défaut d’accord amiable, le tribunal compétent est celui de %(TRIB)s. Si le Client n’agit pas pour ses besoins professionnels, les règles légales de compétence s’appliquent.</p>
""" % dict(NAME=NAME, NOM=NOM, STATUT=STATUT, SIRET=SIRET, ADRESSE=ADRESSE, TVA=TVA, TRIB=TRIB,
           MAILSENT=(" ou à " + E["email"]) if E.get("email") else ""))

    # ------------------------------------------------------------------ confidentialité
    pages["confidentialite"] = dict(
        title="Politique de confidentialité",
        desc="Comment %s utilise vos données personnelles : finalités, durées, vos droits." % NAME,
        lede="Quelles données nous collectons, pourquoi, combien de temps, et comment exercer vos droits.",
        body="""
<div class="callout"><strong>En résumé.</strong> Nous collectons le minimum : les informations que vous saisissez dans la demande de site. Nous ne les vendons pas. Vous pouvez demander leur consultation, correction ou suppression à tout moment.</div>

<h2 id="responsable">1. Responsable du traitement</h2>
<p>Le responsable du traitement est %(NOM)s (%(STATUT)s, SIRET %(SIRET)s), %(ADRESSE)s. Contact : %(MAIL)s.</p>

<h2 id="donnees">2. Données collectées et finalités</h2>
<div class="tw"><table>
<thead><tr><th>Situation</th><th>Données</th><th>Finalité</th><th>Base légale</th></tr></thead>
<tbody>
<tr><td>Compte client</td><td>Nom, e-mail, mot de passe (conservé uniquement sous forme chiffrée irréversible), date de création, dernière connexion, abonnement, plaintes éventuelles, journal des actions sur le compte, empreinte irréversible de l’adresse IP</td><td>Vous permettre de faire une demande et de suivre votre commande ; gérer l’abonnement et le service client (l’éditeur peut consulter votre compte pour vous aider, chaque consultation est enregistrée) ; limiter les abus</td><td>Exécution de mesures précontractuelles ; intérêt légitime</td></tr>
<tr><td>Demande de site</td><td>Nom, e-mail, téléphone (facultatif), nom du commerce, activité, ville, nom de domaine souhaité, nombre d’adresses mail, message, date de la demande</td><td>Répondre à votre demande, préparer votre devis et votre site</td><td>Mesures précontractuelles prises à votre demande</td></tr>
<tr><td>Abonnement</td><td>Identité, coordonnées, contenus du site, factures, historique des modifications</td><td>Exécuter le contrat, facturer, assurer le support</td><td>Exécution du contrat ; obligation légale (comptabilité)</td></tr>
<tr><td>Navigation sur ce site</td><td>Adresse IP, type de navigateur, pages demandées (journaux techniques de l’hébergeur)</td><td>Sécurité, prévention des abus, bon fonctionnement</td><td>Intérêt légitime</td></tr>
<tr><td>Démonstration de réservation</td><td>Prénom (fictif conseillé), téléphone (facultatif), créneau choisi, empreinte irréversible de l’adresse IP</td><td>Montrer le fonctionnement de la réservation et éviter les abus</td><td>Intérêt légitime</td></tr>
<tr><td>Anti-abus du formulaire</td><td>Empreinte irréversible de l’adresse IP</td><td>Limiter les envois automatisés</td><td>Intérêt légitime</td></tr>
<tr><td>Suivi de campagne (si accepté)</td><td>Paramètres UTM de l’adresse visitée, site d’origine, page d’arrivée</td><td>Savoir quelle annonce ou quel lien a amené la demande</td><td>Consentement</td></tr>
</tbody></table></div>
<p>Aucune donnée sensible n’est demandée. Merci de ne pas en saisir dans le champ « message ».</p>

<h2 id="durees">3. Durées de conservation</h2>
<ul>
<li>Demande non suivie d’une commande : 3 ans après le dernier contact, puis suppression.</li>
<li>Données liées à un abonnement : pendant la durée du contrat, puis 5 ans (prescription civile).</li>
<li>Factures et pièces comptables : 10 ans (obligation légale).</li>
<li>Journaux techniques : selon la politique de l’hébergeur, en principe quelques semaines.</li>
<li>Paramètres UTM : 30 jours dans votre navigateur.</li>
<li>Réservations de la page de démonstration : supprimées automatiquement au bout de 24 heures.</li>
</ul>

<h2 id="destinataires">4. Destinataires et sous-traitants</h2>
<p>Vos données sont accessibles à l’Éditeur. Elles sont traitées par des prestataires techniques, uniquement pour fournir le service :</p>
<ul>
<li><strong>Cloudflare, Inc.</strong> : hébergement du site, base de données des demandes, réseau de diffusion ;</li>
<li><strong>GitHub, Inc.</strong> : conservation du code source du site (sans données de clients) ;</li>
<li><strong>Google Fonts (Google LLC)</strong> : affichage des polices de caractères ; votre navigateur contacte les serveurs de Google, qui reçoivent votre adresse IP ;</li>
<li>à l’ouverture du paiement en ligne : un prestataire de paiement et un service d’envoi d’e-mails. Cette liste sera mise à jour avant leur mise en service.</li>
</ul>

<h2 id="transferts">5. Transferts hors Union européenne</h2>
<p>Cloudflare, GitHub et Google sont établis aux États-Unis. Ces transferts s’appuient sur le cadre de protection des données UE–États-Unis (Data Privacy Framework) et sur les clauses contractuelles types de la Commission européenne, selon les prestataires.</p>

<h2 id="droits">6. Vos droits</h2>
<p>Vous disposez d’un droit d’accès, de rectification, d’effacement, de limitation, d’opposition et de portabilité de vos données, ainsi que du droit de retirer votre consentement à tout moment et de définir des directives sur le sort de vos données après votre décès. Pour les exercer, écrivez-nous via la <a href="/commander">demande en ligne</a>%(MAILSENT)s en précisant votre demande ; nous répondons dans un délai d’un mois.</p>
<p>Vous pouvez aussi introduire une réclamation auprès de la CNIL : <a href="https://www.cnil.fr/fr/plaintes" rel="noopener" target="_blank">www.cnil.fr/fr/plaintes</a>.</p>

<h2 id="securite">7. Sécurité</h2>
<p>Les échanges sont chiffrés (HTTPS). L’accès aux données est limité à l’Éditeur. Les numéros de carte bancaire ne transitent pas par nos serveurs. Aucun système n’est infaillible : en cas de violation de données présentant un risque pour vous, nous vous en informerons et préviendrons la CNIL dans les délais légaux.</p>

<h2 id="cookies">8. Cookies</h2>
<p>Le détail figure sur la page <a href="/cookies">cookies</a>. Vous pouvez modifier vos choix à tout moment avec le lien « Gérer les cookies » en bas de page.</p>

<h2 id="mineurs">9. Mineurs</h2>
<p>Ce service s’adresse à des professionnels majeurs. Nous ne collectons pas sciemment de données de mineurs.</p>

<h2 id="evolutions">10. Évolution de cette politique</h2>
<p>Nous pouvons mettre à jour cette politique, par exemple à l’ouverture de nouveaux services. La date de dernière mise à jour figure en haut de la page.</p>
""" % dict(NOM=NOM, STATUT=STATUT, SIRET=SIRET, ADRESSE=ADRESSE, MAIL=MAIL,
           MAILSENT=(" ou écrivez à " + E["email"]) if E.get("email") else ""))

    # ------------------------------------------------------------------ cookies
    pages["cookies"] = dict(
        title="Cookies et stockage local",
        desc="Ce que ce site enregistre dans votre navigateur et comment gérer vos choix.",
        lede="Ce que le site enregistre dans votre navigateur, ce qui demande votre accord, et comment changer d’avis.",
        body="""
<div class="callout"><strong>En résumé.</strong> Ce site n’utilise ni publicité ni outil de mesure d’audience tiers. Seul le suivi des campagnes (UTM) est optionnel et ne démarre qu’avec votre accord.</div>
<p><button type="button" class="btn sm" data-cookies>Gérer mes choix maintenant</button></p>

<h2 id="quoi">1. Ce que nous enregistrons</h2>
<div class="tw"><table>
<thead><tr><th>Nom</th><th>Rôle</th><th>Durée</th><th>Accord requis ?</th></tr></thead>
<tbody>
<tr><td><code>sv_consent</code></td><td>Mémorise vos choix sur les cookies</td><td>Navigateur, jusqu’à effacement</td><td>Non (nécessaire)</td></tr>
<tr><td><code>sv_session</code></td><td>Vous garde connecté à votre compte</td><td>Cookie, 30 jours au plus</td><td>Non (nécessaire)</td></tr>
<tr><td><code>sv_theme</code></td><td>Mémorise le thème clair ou sombre que vous avez choisi</td><td>Navigateur, jusqu’à effacement</td><td>Non (préférence demandée par vous)</td></tr>
<tr><td><code>sv_utm</code></td><td>Garde l’origine de votre visite (paramètres UTM) pour la joindre à votre demande</td><td>30 jours</td><td><strong>Oui</strong></td></tr>
</tbody></table></div>
<p>Ces informations sont enregistrées dans le stockage local de votre navigateur (« localStorage »), et non envoyées à des tiers.</p>

<h2 id="utm">2. Le suivi UTM, c’est quoi ?</h2>
<p>Quand vous cliquez sur une annonce ou un lien partagé, l’adresse peut contenir des repères comme <code>utm_source=facebook</code>. Si vous acceptez, nous les gardons 30 jours pour savoir d’où vient votre demande. Si vous refusez, rien n’est enregistré et ces repères sont ignorés.</p>

<h2 id="tiers">3. Contenus de tiers</h2>
<p>Les polices de caractères sont chargées depuis Google Fonts. Votre navigateur se connecte alors aux serveurs de Google, qui reçoivent votre adresse IP et des informations techniques. Nous prévoyons de les héberger directement sur le site pour supprimer ce transfert.</p>

<h2 id="gerer">4. Changer d’avis</h2>
<p>Vous pouvez modifier vos choix à tout moment avec le lien « Gérer les cookies » en bas de chaque page. Vous pouvez aussi effacer les données du site dans les réglages de votre navigateur.</p>
<p>Votre choix est conservé jusqu’à effacement du stockage de votre navigateur. Nous vous le redemandons au plus tard au bout de 13 mois.</p>

<h2 id="plus">5. En savoir plus</h2>
<p>Voir la <a href="/confidentialite">politique de confidentialité</a>. Informations de la CNIL sur les cookies : <a href="https://www.cnil.fr/fr/cookies-et-autres-traceurs" rel="noopener" target="_blank">cnil.fr</a>.</p>
""")

    return pages
