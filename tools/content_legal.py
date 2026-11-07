# -*- coding: utf-8 -*-
"""Textes légaux. Les informations d'identité de l'éditeur viennent de EDITOR (build.py).
Un champ vide s'affiche en jaune « À compléter » pour ne jamais passer inaperçu.
Les jetons [[NOM]], [[SIRET]]… sont remplacés à la fin de mk()."""

STRIPE = "Stripe Payments Europe, Ltd., 1 Grand Canal Street Lower, Grand Canal Dock, Dublin, D02 H210, Irlande"
CLOUDFLARE = "Cloudflare, Inc., 101 Townsend Street, San Francisco, CA 94107, États-Unis, téléphone : +1 888 993 5273"


def mk(E):
    def v(key, label):
        val = E.get(key, "").strip()
        return val if val else '<mark class="todo">[À compléter : %s]</mark>' % label

    T = dict(
        NAME=E["site_name"],
        NOM=v("nom", "nom et prénom, suivis de « EI » (entrepreneur individuel), ou raison sociale"),
        STATUT=v("statut", "statut juridique, par exemple entrepreneur individuel (micro-entreprise)"),
        SIRET=v("siret", "numéro SIRET"),
        IMMAT=v("immat", "immatriculation : « RNE » ou « RCS de [ville] » suivi du numéro SIREN"),
        ADRESSE=v("adresse", "adresse postale"),
        TEL=v("tel", "téléphone"),
        MAIL=v("email", "adresse e-mail de contact"),
        DIR=v("directeur", "directeur de la publication (en principe vous-même)"),
        TVA=v("tva", "mention de TVA : numéro de TVA intracommunautaire, ou « TVA non applicable, article 293 B du CGI »"),
        TRIB=v("tribunal", "ville du tribunal compétent (siège de l’éditeur)"),
        STRIPE=STRIPE, CLOUDFLARE=CLOUDFLARE,
        CONTACT='la page <a href="/contact">Nous contacter</a>' + ((" ou l’adresse " + E["email"]) if E.get("email") else ""),
    )

    def fill(s):
        for k, val in T.items():
            s = s.replace("[[%s]]" % k, val)
        assert "[[" not in s, s[s.index("[["):s.index("[[") + 40]
        return s

    pages = {}

    # ------------------------------------------------------------------ mentions légales
    pages["mentions-legales"] = dict(
        title="Mentions légales",
        desc="Mentions légales du site [[NAME]] : éditeur, hébergeur, paiements, propriété intellectuelle, avis.",
        lede="Qui édite ce site, qui l’héberge, qui traite les paiements, et les règles qui s’y appliquent.",
        body="""
<h2 id="editeur">1. Éditeur du site</h2>
<p>Le site <strong>[[NAME]]</strong> est édité par :</p>
<ul>
<li>Nom ou raison sociale : [[NOM]]</li>
<li>Statut : [[STATUT]]</li>
<li>SIRET : [[SIRET]]</li>
<li>Immatriculation : [[IMMAT]]</li>
<li>Adresse : [[ADRESSE]]</li>
<li>Téléphone : [[TEL]]</li>
<li>E-mail : [[MAIL]]</li>
<li>TVA : [[TVA]]</li>
</ul>
<p>Directeur de la publication : [[DIR]].</p>

<h2 id="hebergeur">2. Hébergeur</h2>
<p>Le site, sa base de données et ses fichiers sont hébergés par <strong>[[CLOUDFLARE]]</strong> (<a href="https://www.cloudflare.com" rel="noopener" target="_blank">www.cloudflare.com</a>).</p>
<p>Le code source du site est conservé sur la plateforme GitHub (GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis). Il ne contient aucune donnée de client.</p>

<h2 id="paiements">3. Paiements en ligne</h2>
<p>Lorsque les sites que nous réalisons proposent le paiement en ligne (formule Pro), les paiements sont traités par <strong>[[STRIPE]]</strong>, prestataire de services de paiement. Le commerçant encaisse directement sur son propre compte Stripe : [[NAME]] ne reçoit, ne détient et ne transfère jamais ces fonds, et ne prélève aucune commission. Les numéros de carte sont saisis chez Stripe et ne passent jamais par nos serveurs. Le détail figure à l’<a href="/cgv#art-12">article 12 des conditions générales de vente</a>.</p>

<h2 id="activite">4. Activité</h2>
<p>[[NAME]] propose, sous forme d’abonnement, la création et l’hébergement de sites vitrines pour les commerces, les indépendants et les associations. L’offre est réservée aux professionnels et aux non-professionnels (associations, par exemple) : elle ne s’adresse pas aux consommateurs. Les conditions figurent dans les <a href="/cgv">conditions générales de vente</a>.</p>

<h2 id="propriete">5. Propriété intellectuelle</h2>
<p>Les textes, images, graphismes, logos et le code du site [[NAME]] sont protégés par le droit d’auteur et, le cas échéant, par le droit des marques. Toute reproduction, représentation ou adaptation, totale ou partielle, sans autorisation écrite préalable, est interdite.</p>
<p>Les polices de caractères sont publiées sous licence libre SIL Open Font License 1.1 et hébergées sur notre propre site (<a href="/assets/fonts/LICENCES.txt">licences</a>).</p>
<p>Les sites d’exemple présentés (salon de coiffure, restaurant, cabinet, garage, etc.) sont des démonstrations. Les noms, adresses, numéros de téléphone, tarifs, rendez-vous, statistiques et paiements qui y figurent sont fictifs ; aucun paiement réel n’y est possible.</p>

<h2 id="avis">6. Avis de nos clients</h2>
<p>Les avis affichés sur ce site proviennent uniquement de nos clients dont le site est en ligne. Ils sont déposés depuis l’espace client, sans contrepartie, et publiés avec l’accord de leur auteur. Chaque avis est relu avant publication pour écarter les contenus injurieux, illicites ou sans rapport avec notre service ; les avis négatifs sont publiés comme les positifs. La date de publication est indiquée. L’auteur d’un avis refusé est informé du motif. La note moyenne est calculée sur l’ensemble des avis publiés. Pour signaler un avis qui vous paraît douteux, utilisez [[CONTACT]].</p>

<h2 id="responsabilite">7. Responsabilité</h2>
<p>Nous nous efforçons de fournir des informations exactes et à jour, sans pouvoir garantir l’absence d’erreur ou d’omission. Le site peut être interrompu pour maintenance. Les liens vers des sites tiers sont fournis à titre d’information : nous ne contrôlons pas leur contenu.</p>

<h2 id="donnees">8. Données personnelles et cookies</h2>
<p>Le traitement de vos données est décrit dans la <a href="/confidentialite">politique de confidentialité</a>. Ce que le site enregistre dans votre navigateur est décrit dans la <a href="/cookies">page cookies</a>.</p>

<h2 id="droit">9. Droit applicable</h2>
<p>Le présent site est soumis au droit français.</p>

<h2 id="contact">10. Contact</h2>
<p>Pour toute question ou réclamation, utilisez [[CONTACT]].</p>
""")

    # ------------------------------------------------------------------ CGV
    pages["cgv"] = dict(
        title="Conditions générales de vente",
        desc="Conditions générales de vente de l’abonnement [[NAME]] : prix, durée, paiement en ligne Stripe, données, résiliation.",
        lede="Les règles de l’abonnement, en clair : prix, durée de 12 mois, paiement en ligne, données, résiliation.",
        notice="L’offre est réservée aux professionnels et aux non-professionnels (associations, par exemple). Elle ne s’adresse pas aux consommateurs.",
        body="""
<div class="callout"><strong>En résumé.</strong> Un site vitrine, un nom de domaine, un hébergement, un espace client et un guide pub, avec un engagement de <strong>12 mois</strong>, en deux formules : <strong>Essentiel à 60 € HT (72 € TTC) par mois</strong> et <strong>Pro à 100 € HT (120 € TTC) par mois</strong>. Le Pro ajoute la réservation en ligne, le paiement en ligne de vos clients par Stripe (sans aucune commission de notre part), l’éditeur en libre-service et une adresse mail pro. Ce résumé n’a pas de valeur contractuelle : seuls les articles ci-dessous s’appliquent.</div>

<h2 id="art-1">Article 1. Objet, parties et champ d’application</h2>
<p>Les présentes conditions générales de vente (« CGV ») régissent la vente de l’abonnement « [[NAME]] » proposé par [[NOM]] ([[STATUT]], SIRET [[SIRET]], [[IMMAT]], [[ADRESSE]]), ci-après « l’Éditeur », au « Client ».</p>
<p>Le Client est une personne agissant pour les besoins de son activité commerciale, industrielle, artisanale, libérale ou agricole (professionnel), ou une personne morale n’agissant pas à des fins professionnelles, comme une association (non-professionnel). <strong>L’Éditeur ne contracte pas avec des consommateurs</strong> : la personne qui commande déclare agir dans l’un de ces deux cadres.</p>
<p>Toute commande suppose l’acceptation sans réserve des CGV en vigueur au jour de la commande, qui prévalent sur tout autre document du Client, sauf accord écrit contraire.</p>

<h2 id="art-2">Article 2. Description de l’offre</h2>
<p>L’abonnement comprend, dans les deux formules :</p>
<ul>
<li>la conception d’un site vitrine adapté au téléphone, à partir des informations et contenus fournis par le Client ;</li>
<li>la réservation et le renouvellement annuel d’un nom de domaine pendant la durée de l’abonnement (article 9) ;</li>
<li>l’hébergement du site, avec certificat HTTPS (article 13) ;</li>
<li>un espace client de suivi, des modifications réalisées par l’Éditeur (article 8) ;</li>
<li>un logo simple créé par l’Éditeur si le Client n’en a pas (article 7) ;</li>
<li>un guide pub : document d’aide pour faire connaître son activité ;</li>
<li>des modèles de mentions légales et de politique de confidentialité pour le site du Client (article 6).</li>
</ul>
<p>La <strong>formule Pro</strong> comprend en plus : un éditeur en libre-service, trois modifications par mois au lieu d’une, la réservation en ligne (article 11), le paiement en ligne par Stripe si le Client le souhaite (article 12) et une adresse mail professionnelle (article 10). <strong>Option</strong> dans les deux formules : adresses mail supplémentaires (article 10).</p>
<p><strong>Ne sont pas compris :</strong> la publicité réalisée pour le compte du Client, le référencement payant, une boutique en ligne complète (vente de produits avec panier et livraison), un logo élaboré, une charte graphique, la refonte complète du design, la rédaction de contenus volumineux, la production de photographies, les rappels par SMS et la synchronisation avec un agenda externe. Ces prestations peuvent faire l’objet d’un devis séparé.</p>

<h2 id="art-3">Article 3. Commande et formation du contrat</h2>
<p>Le Client remplit la demande en ligne, qui est gratuite et sans engagement. L’Éditeur vérifie la faisabilité et confirme les éléments de la commande (formule, activité, nom de domaine souhaité, options). Il peut refuser une commande pour motif légitime (contenu ou activité illicite, nom de domaine portant atteinte aux droits d’un tiers, impayé antérieur, commande passée par un consommateur).</p>
<p>Le contrat est formé lorsque le Client a accepté les présentes CGV (case à cocher) <strong>et</strong> que le premier paiement mensuel a été reçu par l’Éditeur, sous réserve de l’article 17 en cas de contrat conclu hors établissement. Les CGV acceptées restent consultables, imprimables et enregistrables à tout moment sur cette page ; l’Éditeur en conserve la version datée applicable à chaque commande et la communique sur simple demande.</p>

<h2 id="art-4">Article 4. Prix, facturation et paiement</h2>
<ul>
<li>Formule Essentiel : <strong>60 € HT (72 € TTC) par mois</strong>.</li>
<li>Formule Pro : <strong>100 € HT (120 € TTC) par mois</strong>.</li>
<li>Adresse mail professionnelle : <strong>4 € HT (4,80 € TTC) par mois et par adresse</strong> (la première est incluse dans la formule Pro).</li>
</ul>
<p>Les prix sont en euros, hors taxes (HT) et toutes taxes comprises (TTC, TVA à 20 %). [[TVA]] Le prix de l’abonnement ne change pas pendant la période d’engagement en cours. Aucuns frais de création ne s’ajoutent.</p>
<p>L’abonnement est payable <strong>mensuellement et d’avance</strong>, au début de chaque mois d’abonnement, par carte bancaire ou prélèvement SEPA, par l’intermédiaire d’un prestataire de paiement agréé. L’Éditeur ne reçoit ni ne conserve les données de carte bancaire. Une facture est mise à disposition dans l’espace client à chaque échéance ; elle est émise sous forme électronique, selon les règles de facturation électronique en vigueur. Aucun escompte n’est accordé pour paiement anticipé.</p>
<p>En cas de retard de paiement, des pénalités sont dues de plein droit, sans mise en demeure préalable, au taux de trois fois le taux d’intérêt légal, à compter du lendemain de la date d’échéance, ainsi qu’une indemnité forfaitaire pour frais de recouvrement de 40 € (articles L441-10 et D441-5 du Code de commerce). Après une mise en demeure restée sans effet pendant 8 jours, l’Éditeur peut suspendre le site et l’espace client jusqu’au paiement, sans que cette suspension n’interrompe l’abonnement.</p>

<h2 id="art-5">Article 5. Durée, reconduction et changement de formule</h2>
<p>L’abonnement est conclu pour une durée initiale de <strong>12 mois</strong> à compter de la mise en ligne du site. Il est ensuite reconduit tacitement par périodes de 12 mois, sauf résiliation dans les conditions de l’article 16.</p>
<p>L’Éditeur adresse au Client un rappel écrit au plus tôt trois mois et au plus tard un mois avant la date limite de résiliation de chaque période, en lui rappelant la possibilité de ne pas reconduire l’abonnement (article L215-1 du Code de la consommation, applicable aux non-professionnels).</p>
<p>Le Client peut passer de l’Essentiel au Pro à tout moment, avec effet au début du mois suivant ; une nouvelle période de 12 mois commence alors. Le passage du Pro à l’Essentiel n’est possible qu’à l’échéance de la période en cours ; le paiement en ligne (article 12) est alors désactivé.</p>

<h2 id="art-6">Article 6. Création, livraison et contenus</h2>
<p>L’Éditeur livre un aperçu du site dans un <strong>délai indicatif de 5 jours ouvrés</strong> à compter de la réception de l’ensemble des contenus nécessaires (textes, photos, horaires, tarifs, coordonnées, choix du nom de domaine). Tout retard du Client à fournir ou valider ces éléments décale d’autant la livraison. Le Client demande ses ajustements sur l’aperçu ; le site est mis en ligne après sa validation. À défaut de réponse dans les 15 jours suivant l’envoi de l’aperçu et une relance, l’abonnement et sa facturation débutent à la date de cette relance.</p>
<p>L’Éditeur met en forme les contenus et corrige les fautes de langue évidentes. Il relit le site avant mise en ligne (textes, photos, liens, affichage sur téléphone). Il fournit des <strong>modèles</strong> de mentions légales, de politique de confidentialité et, si le paiement en ligne est activé, de conditions de vente et de réservation, que le Client complète avec ses propres informations. Le Client reste seul responsable de l’exactitude de ces informations, de ses prix (affichés TTC à l’égard de ses propres clients consommateurs), de ses conditions de vente et du respect des règles propres à son activité.</p>

<h2 id="art-7">Article 7. Obligations du Client et logo</h2>
<p>Le Client s’engage à : fournir des informations exactes et complètes ; disposer des droits sur les textes, photos, logos et marques qu’il transmet (droit d’auteur, droit à l’image) ; ne publier aucun contenu illicite, trompeur, diffamatoire, contrefaisant ou contraire à l’ordre public ; garder confidentiels ses identifiants ; signaler sans délai toute erreur ou tout usage frauduleux. Il demeure seul responsable du contenu de son site et de la légalité de son activité.</p>
<p><strong>Logo.</strong> Si le Client n’a pas de logo, l’Éditeur en crée un simple (nom du commerce en typographie soignée, avec au besoin un petit symbole), avec une proposition et une série de retouches. Un logo élaboré, une charte graphique ou des déclinaisons font l’objet d’un devis.</p>

<h2 id="art-8">Article 8. Modifications comprises</h2>
<p>Le Client peut demander à l’Éditeur, depuis son espace client, <strong>une modification par mois</strong> (<strong>trois</strong> dans la formule Pro) : remplacement d’un texte ou d’une photo, ajout ou suppression d’un bloc de contenu. Les modifications non utilisées ne se cumulent pas. Un historique est conservé et une modification peut être annulée.</p>
<p>Dans la formule Pro, l’<strong>éditeur en libre-service</strong> permet au Client de modifier lui-même, sans limite, les textes, prix, horaires et photos, sans changer la mise en page. Le Client est seul responsable des contenus qu’il publie ainsi. L’Éditeur peut annuler ou corriger une modification contraire à la loi ou aux CGV. Une nouvelle page, une refonte ou une fonctionnalité supplémentaire font l’objet d’un devis.</p>

<h2 id="art-9">Article 9. Nom de domaine</h2>
<p>L’Éditeur réserve, gère et renouvelle chaque année le nom de domaine choisi pendant la durée de l’abonnement ; ce coût est compris. La disponibilité d’un nom n’est pas garantie : des variantes sont proposées si besoin. Le Client garantit que le nom choisi ne porte pas atteinte aux droits de tiers.</p>
<p>À la fin de l’abonnement, et sous réserve du paiement des sommes dues, le Client peut demander le transfert de son nom de domaine ; l’Éditeur lui remet le code de transfert dans un délai raisonnable. Un nom de domaine que le Client possédait déjà reste chez son prestataire d’origine, à sa charge.</p>

<h2 id="art-10">Article 10. Adresse mail professionnelle</h2>
<p>Chaque adresse est facturée 4 € HT (4,80 € TTC) par mois, sauf la première adresse de la formule Pro, qui est incluse, et suit la durée de l’abonnement. Un guide d’installation est fourni. La boîte est de taille limitée, pour un usage professionnel normal ; l’envoi de messages en masse ou non sollicités est interdit. À la fin de l’abonnement, les adresses sont fermées 30 jours après la date de fin, pour permettre au Client de récupérer ses messages.</p>

<h2 id="art-11">Article 11. Formule Pro : réservation en ligne</h2>
<p>La formule Pro comprend un module de réservation intégré au site du Client : le visiteur choisit une prestation, un jour et un créneau disponible, et laisse ses coordonnées ; un créneau réservé n’est plus proposé. Les réservations et leurs statistiques sont consultables dans l’espace de réservation du Client.</p>
<ul>
<li>L’Éditeur paramètre, à partir des informations du Client, les prestations, leurs durées, leurs prix et les horaires. Les changements ultérieurs comptent comme des modifications au sens de l’article 8, sauf s’ils sont faits par le Client avec l’éditeur en libre-service.</li>
<li>Le Client reste responsable de l’honneur des rendez-vous, de ses conditions d’annulation et de l’information de ses propres clients.</li>
<li><strong>Données de santé.</strong> L’hébergement de l’Éditeur n’est pas certifié « hébergeur de données de santé » (HDS). Le module de réservation ne doit donc pas servir à recueillir des données de santé (symptômes, pathologies, motif médical, antécédents). Pour les professions de santé et assimilées, le formulaire est limité à l’identité, aux coordonnées, au type de rendez-vous et au créneau, et le Client s’engage à ne pas demander d’informations de santé par ce moyen.</li>
</ul>

<h2 id="art-12">Article 12. Formule Pro : paiement en ligne par Stripe</h2>
<p><strong>12.1 Principe.</strong> Si le Client le souhaite, ses propres clients peuvent payer en ligne, par carte, la prestation qu’ils réservent sur son site. Le paiement est assuré par <strong>[[STRIPE]]</strong> (« Stripe »), prestataire de services de paiement. Cette fonction est facultative et peut être activée ou désactivée par le Client depuis son espace.</p>
<p><strong>12.2 Compte Stripe du Client.</strong> Le Client ouvre ou connecte <strong>son propre compte Stripe</strong> depuis son espace, en suivant le parcours d’inscription de Stripe. Il conclut directement avec Stripe le contrat de services Stripe et le contrat de compte connecté (<a href="https://stripe.com/fr/legal/ssa" rel="noopener" target="_blank">stripe.com/fr/legal/ssa</a>, <a href="https://stripe.com/fr/legal/connect-account" rel="noopener" target="_blank">stripe.com/fr/legal/connect-account</a>). Stripe vérifie seul son identité et celle de son entreprise, et peut refuser, limiter ou fermer son compte selon ses propres règles ; l’Éditeur n’intervient pas dans ces décisions et n’en est pas responsable.</p>
<p><strong>12.3 Fonds.</strong> Les sommes payées par les clients du Client sont encaissées <strong>directement sur le compte Stripe du Client</strong>, puis virées par Stripe sur son compte bancaire. L’Éditeur ne reçoit, ne détient et ne transfère jamais ces fonds.</p>
<p><strong>12.4 Aucune commission.</strong> <strong>L’Éditeur ne prélève aucune commission</strong> ni aucun frais sur les paiements reçus par le Client : le Client paie seulement son abonnement. Les frais de Stripe (par exemple, pour une carte européenne standard, un pourcentage du montant plus un montant fixe par paiement) sont fixés et prélevés directement par Stripe sur chaque paiement, selon les tarifs publiés par Stripe (<a href="https://stripe.com/fr/pricing" rel="noopener" target="_blank">stripe.com/fr/pricing</a>) ou convenus entre le Client et Stripe. Les frais estimés affichés dans l’espace du Client sont indicatifs ; seuls les relevés Stripe font foi.</p>
<p><strong>12.5 Rôle de l’Éditeur.</strong> L’Éditeur fournit la liaison technique entre le site et le compte Stripe du Client (plateforme Stripe Connect) : il crée les paiements correspondant aux réservations, reçoit de Stripe les informations nécessaires (référence, montant, statut, date du paiement ou du remboursement) pour les afficher dans l’espace du Client, et déclenche les remboursements demandés par le Client. Il n’a jamais accès aux numéros de carte, qui sont saisis sur une page ou un module sécurisé de Stripe.</p>
<p><strong>12.6 Obligations du Client vendeur.</strong> Le Client est le seul vendeur des prestations payées en ligne. Il lui appartient notamment :</p>
<ul>
<li>d’afficher des prix exacts, TTC, et ses conditions de vente, d’annulation et de remboursement, à partir du modèle fourni par l’Éditeur qu’il complète et valide ;</li>
<li>de respecter le droit de la consommation à l’égard de ses clients (information précontractuelle, droit de rétractation lorsqu’il s’applique, médiation de la consommation) ;</li>
<li>de délivrer à ses clients les factures ou justificatifs exigés et de déclarer et payer la TVA et les impôts sur ses ventes ;</li>
<li>de traiter les annulations, remboursements, réclamations et contestations de paiement (« litiges ») et d’en supporter le coût, y compris les frais de litige facturés par Stripe ;</li>
<li>de respecter les conditions et la liste des activités interdites de Stripe.</li>
</ul>
<p><strong>12.7 Responsabilité.</strong> L’Éditeur n’est pas partie aux ventes conclues entre le Client et ses clients, ni au contrat entre le Client et Stripe. Il n’est pas responsable d’une indisponibilité de Stripe, d’un refus de paiement, d’un blocage ou d’un délai de virement décidé par Stripe, ni d’un litige entre le Client et ses clients. Il reste tenu du bon fonctionnement de la liaison technique qu’il fournit, dans les limites de l’article 14.</p>
<p><strong>12.8 Fin.</strong> À la fin de l’abonnement Pro, la liaison est coupée et le paiement en ligne retiré du site. Le compte Stripe reste la propriété du Client, avec son historique, chez Stripe. Les remboursements de paiements antérieurs restent à la charge du Client, depuis son compte Stripe.</p>

<h2 id="art-13">Article 13. Hébergement, disponibilité et sécurité</h2>
<p>Le site est hébergé sur l’infrastructure de Cloudflare. L’Éditeur est tenu d’une obligation de moyens quant à la disponibilité du site, de l’espace client et du module de réservation et de paiement. Des interruptions peuvent survenir pour maintenance ou du fait de tiers (hébergeur, réseau, Stripe, registres de noms de domaine). Aucun niveau de disponibilité n’est garanti. L’Éditeur met en œuvre des mesures de sécurité adaptées (chiffrement HTTPS, accès restreints, mots de passe chiffrés de façon irréversible, clés secrètes stockées hors du code, sauvegardes).</p>

<h2 id="art-14">Article 14. Responsabilité</h2>
<p>L’Éditeur ne garantit aucun résultat : nombre de visites, position dans les moteurs de recherche, nombre de réservations, chiffre d’affaires. Le guide pub est une aide, pas une promesse de résultat.</p>
<p>La responsabilité de l’Éditeur ne peut être engagée qu’en cas de faute prouvée et se limite aux dommages directs. Elle est plafonnée, toutes causes confondues, aux sommes effectivement payées par le Client au titre de l’abonnement au cours des 12 mois précédant le fait générateur. L’Éditeur n’est pas responsable des dommages indirects (perte de chiffre d’affaires, de clientèle, d’image). Ces limites ne s’appliquent pas en cas de faute lourde ou dolosive, de dommage corporel, ni lorsque la loi l’interdit.</p>
<p>Aucune partie n’est responsable d’un manquement dû à un cas de force majeure au sens de l’article 1218 du Code civil.</p>

<h2 id="art-15">Article 15. Propriété intellectuelle</h2>
<p><strong>Contenus du Client.</strong> Le Client conserve la propriété de ses textes, photos, logos et marques. Il concède à l’Éditeur le droit de les reproduire et de les diffuser sur son site pendant la durée de l’abonnement, pour les besoins de la prestation.</p>
<p><strong>Création de l’Éditeur.</strong> Le code, les modèles, la structure et les éléments graphiques conçus par l’Éditeur restent sa propriété. Pendant l’abonnement, l’Éditeur concède au Client un droit d’utilisation non exclusif et non cessible pour exploiter son site. À la fin de l’abonnement, le Client récupère ses contenus (textes et photos) sur simple demande.</p>
<p><strong>Logo créé pour le Client.</strong> Il lui est cédé, pour tous usages, dès que les sommes dues sont réglées ; l’Éditeur lui en remet les fichiers sur demande. L’Éditeur ne garantit pas sa disponibilité comme marque : il appartient au Client de le vérifier, au besoin, auprès de l’INPI.</p>
<p>L’Éditeur peut citer le site réalisé comme référence, sauf opposition écrite du Client.</p>

<h2 id="art-16">Article 16. Résiliation</h2>
<p><strong>Par le Client.</strong> Le Client peut résilier à l’échéance de chaque période de 12 mois, avec un préavis d’au moins 30 jours avant cette échéance, par écrit (e-mail ou courrier) ou avec le bouton « Demander la résiliation » de son espace client (rubrique « Abonnement »), qui lui délivre un accusé de réception. Pendant la période d’engagement en cours, les mensualités restantes demeurent dues et ne sont pas remboursées.</p>
<p><strong>Pour manquement.</strong> Chaque partie peut résilier le contrat en cas de manquement grave de l’autre partie non réparé 15 jours après une mise en demeure écrite. Si le manquement est le fait de l’Éditeur, les sommes versées pour la période non consommée sont remboursées au prorata.</p>
<p><strong>Effets.</strong> À la fin du contrat, le site est mis hors ligne, les accès sont fermés, la liaison Stripe est coupée, et les articles 9 (transfert du domaine), 10 (fermeture du mail), 12.8 (Stripe), 15 (récupération des contenus) et 18 (sort des données) s’appliquent.</p>

<h2 id="art-17">Article 17. Droit de rétractation</h2>
<p><strong>Commande passée en ligne ou à distance.</strong> Entre professionnels, le droit de rétractation prévu par le Code de la consommation ne s’applique pas aux contrats conclus à distance. Avant le premier paiement, la demande reste de toute façon sans engagement.</p>
<p><strong>Contrat signé hors établissement.</strong> Lorsque le contrat est conclu hors de l’établissement de l’Éditeur, en présence physique des parties (par exemple dans le commerce du Client), avec un professionnel qui emploie <strong>cinq salariés au plus</strong> et pour qui la création d’un site internet n’entre pas dans le champ de son activité principale, ce professionnel bénéficie des règles prévues à l’article L221-3 du Code de la consommation :</p>
<ul>
<li>il dispose d’un <strong>délai de rétractation de 14 jours</strong> à compter de la conclusion du contrat, sans avoir à se justifier ni à payer de pénalité ;</li>
<li>il peut se rétracter avec le formulaire ci-dessous ou par toute déclaration dénuée d’ambiguïté, envoyée par e-mail ou par courrier à l’Éditeur ([[ADRESSE]]) ; un exemplaire du formulaire lui est remis lors de la signature ;</li>
<li>l’Éditeur ne demande ni ne reçoit aucun paiement avant l’expiration d’un délai de sept jours à compter de la conclusion du contrat ;</li>
<li>la création du site ne commence pendant le délai de rétractation que si le Client le demande expressément ; s’il se rétracte ensuite, il paie seulement un montant proportionnel au travail réalisé jusqu’à la communication de sa décision ;</li>
<li>en cas de rétractation, l’Éditeur rembourse les sommes éventuellement versées dans les 14 jours, par le même moyen de paiement.</li>
</ul>
<div class="callout"><strong>Formulaire de rétractation</strong> (à compléter et renvoyer uniquement si vous souhaitez vous rétracter d’un contrat conclu hors établissement)<br>
À l’attention de [[NOM]], [[ADRESSE]], [[MAIL]] :<br>
Je vous notifie par la présente ma rétractation du contrat portant sur la prestation de services ci-dessous :<br>
— Abonnement [[NAME]], formule : …………<br>
— Conclu le : …………<br>
— Nom du client et de son entreprise : …………<br>
— Adresse : …………<br>
— Signature (si le formulaire est envoyé sur papier) : …………<br>
— Date : …………</div>

<h2 id="art-18">Article 18. Données personnelles et accord de sous-traitance</h2>
<p><strong>18.1 Données du Client.</strong> L’Éditeur traite les données du Client en qualité de responsable de traitement, conformément à sa <a href="/confidentialite">politique de confidentialité</a>.</p>
<p><strong>18.2 Données des clients du Client.</strong> Pour les données personnelles des visiteurs et clients du site du Client (formulaire de contact, réservations, paiements, statistiques), le Client est <strong>responsable de traitement</strong> et l’Éditeur son <strong>sous-traitant</strong> au sens de l’article 28 du RGPD. Le présent article vaut accord de sous-traitance :</p>
<ul>
<li><strong>Objet et durée :</strong> hébergement du site, réception des messages, gestion des réservations, affichage des paiements et des statistiques, pendant la durée de l’abonnement.</li>
<li><strong>Données et personnes concernées :</strong> clients et prospects du Client : nom, prénom, téléphone, e-mail, message, prestation et créneau réservés, statut de la réservation, référence, montant et statut du paiement (jamais les numéros de carte), données techniques de connexion. Aucune donnée de santé (article 11).</li>
<li><strong>Instructions :</strong> l’Éditeur ne traite ces données que sur instruction documentée du Client (les présentes CGV et les réglages de son espace), et l’informe si une instruction lui paraît contraire à la réglementation.</li>
<li><strong>Confidentialité et sécurité :</strong> seules les personnes habilitées par l’Éditeur, tenues à la confidentialité, y accèdent ; l’Éditeur met en œuvre les mesures de l’article 13.</li>
<li><strong>Sous-traitants ultérieurs :</strong> le Client autorise l’Éditeur à recourir à Cloudflare, Inc. (hébergement et base de données) et à Resend, Inc. (envoi des e-mails de confirmation). L’Éditeur informe le Client de tout ajout ou remplacement, qui peut s’y opposer pour motif légitime. Il impose à ses sous-traitants les mêmes obligations. Stripe n’est pas un sous-traitant de l’Éditeur : il traite les données de paiement en vertu de son propre contrat avec le Client.</li>
<li><strong>Transferts hors Union européenne :</strong> ils s’appuient sur le cadre de protection des données UE–États-Unis ou sur les clauses contractuelles types de la Commission européenne.</li>
<li><strong>Assistance :</strong> l’Éditeur aide le Client à répondre aux demandes d’exercice de droits des personnes, à assurer la sécurité et, le cas échéant, à réaliser une analyse d’impact.</li>
<li><strong>Violation de données :</strong> l’Éditeur notifie au Client toute violation de données dans les meilleurs délais et au plus tard 48 heures après en avoir pris connaissance, avec les informations utiles.</li>
<li><strong>Fin du contrat :</strong> l’Éditeur remet au Client, à sa demande, l’export de ses réservations, puis supprime ces données au plus tard 30 jours après la fin de l’abonnement, sauf obligation légale de conservation.</li>
<li><strong>Contrôle :</strong> l’Éditeur met à la disposition du Client les informations nécessaires pour démontrer le respect de ces obligations et permet des audits raisonnables, à la charge du Client, avec un préavis de 30 jours.</li>
</ul>
<p>Le Client informe ses propres clients du traitement de leurs données (politique de confidentialité de son site, à partir du modèle fourni).</p>

<h2 id="art-19">Article 19. Parrainage</h2>
<p>Chaque Client reçoit un code de parrainage. Lorsqu’un nouveau client saisit ce code lors de son inscription, ou dans son espace avant le démarrage de son abonnement, et que son abonnement démarre, le parrain et le filleul reçoivent chacun <strong>un mois d’abonnement offert</strong>, déduit d’une prochaine facture. Un parrainage non transformé en abonnement dans les 90 jours expire. Chaque mois offert est valable 12 mois, n’est ni remboursable ni convertible en argent, et ne réduit pas la durée d’engagement. Le code n’est valable que pour de nouveaux clients ; un Client ne peut pas se parrainer lui-même. L’Éditeur peut annuler un mois offert obtenu de façon frauduleuse.</p>

<h2 id="art-20">Article 20. Réclamations et litiges</h2>
<p>Toute réclamation peut être adressée à l’Éditeur via [[CONTACT]], ou par courrier à [[ADRESSE]]. L’Éditeur en accuse réception et recherche une solution amiable. L’offre n’étant pas proposée aux consommateurs, le dispositif de médiation de la consommation ne s’applique pas.</p>
<p>Les CGV sont soumises au droit français. En cas de litige entre professionnels, et à défaut d’accord amiable, le tribunal compétent est celui de [[TRIB]]. Pour un Client non-professionnel, les règles légales de compétence s’appliquent.</p>

<h2 id="art-21">Article 21. Modification des CGV</h2>
<p>Les CGV applicables sont celles en vigueur à la date de la commande. L’Éditeur peut les modifier pour l’avenir ; les contrats en cours se poursuivent aux conditions initiales jusqu’à leur échéance, sauf évolution légale impérative ou modification favorable au Client. Toute modification défavorable est notifiée au moins 30 jours avant son application et permet au Client de ne pas reconduire l’abonnement.</p>
""")

    # ------------------------------------------------------------------ confidentialité
    pages["confidentialite"] = dict(
        title="Politique de confidentialité",
        desc="Comment [[NAME]] utilise vos données personnelles : finalités, durées, destinataires, paiements, vos droits.",
        lede="Quelles données nous collectons, pourquoi, combien de temps, avec qui, et comment exercer vos droits.",
        body="""
<div class="callout"><strong>En résumé.</strong> Nous collectons le minimum nécessaire. Nous ne vendons aucune donnée et ne faisons pas de publicité ciblée. Les numéros de carte bancaire ne passent jamais par nos serveurs. Vous pouvez accéder à vos données, les corriger ou les faire supprimer à tout moment.</div>

<h2 id="responsable">1. Responsable du traitement</h2>
<p>Le responsable du traitement est [[NOM]] ([[STATUT]], SIRET [[SIRET]]), [[ADRESSE]]. Contact : [[MAIL]], ou [[CONTACT]].</p>
<p>Cette politique concerne <strong>ce site</strong> et nos clients. Les données des visiteurs et des clients <strong>du site d’un commerçant</strong> que nous avons réalisé (réservations, messages, paiements) sont traitées pour le compte de ce commerçant, qui en est responsable : sa propre politique de confidentialité s’applique, et nous agissons comme son sous-traitant (<a href="/cgv#art-18">article 18 des CGV</a>).</p>

<h2 id="donnees">2. Données collectées et finalités</h2>
<div class="tw"><table>
<thead><tr><th>Situation</th><th>Données</th><th>Finalité</th><th>Base légale</th></tr></thead>
<tbody>
<tr><td>Compte client</td><td>Nom, e-mail, mot de passe (enregistré uniquement sous forme chiffrée irréversible), date de création, dernière connexion, abonnement, journal des actions sur le compte, empreinte irréversible de l’adresse IP</td><td>Vous permettre de faire une demande et de suivre votre commande ; gérer l’abonnement et le service client (l’éditeur peut consulter votre compte pour vous aider, chaque consultation est enregistrée) ; limiter les abus</td><td>Mesures précontractuelles et exécution du contrat ; intérêt légitime (sécurité)</td></tr>
<tr><td>Demande de site</td><td>Nom, e-mail, téléphone (facultatif), nom du commerce, activité, ville, nom de domaine souhaité, options, message, code de parrainage éventuel</td><td>Répondre à votre demande, préparer votre site</td><td>Mesures précontractuelles prises à votre demande</td></tr>
<tr><td>Abonnement et facturation</td><td>Identité, coordonnées, numéro SIREN, formule, factures, paiements de l’abonnement (montant, date, statut), historique des modifications</td><td>Exécuter le contrat, facturer, assurer le support, tenir la comptabilité</td><td>Exécution du contrat ; obligation légale (comptabilité, facturation)</td></tr>
<tr><td>Paiement en ligne de vos clients (formule Pro)</td><td>Identifiant de votre compte Stripe connecté et son statut d’activation ; pour chaque paiement reçu sur votre site : référence, montant, date, statut, remboursement éventuel</td><td>Relier votre site à votre compte Stripe, afficher vos paiements et vos statistiques, déclencher les remboursements que vous demandez</td><td>Exécution du contrat</td></tr>
<tr><td>Dossier de création de votre site</td><td>Informations sur votre commerce (présentation, horaires, adresse, téléphone, tarifs), logo, photos et documents que vous déposez</td><td>Créer et mettre à jour votre site</td><td>Exécution du contrat</td></tr>
<tr><td>Messages et e-mails de service</td><td>Adresse e-mail, contenu des e-mails transactionnels (code de connexion, suivi de commande, rappels)</td><td>Vous envoyer les messages liés à votre compte et à votre abonnement</td><td>Exécution du contrat</td></tr>
<tr><td>Actualités par e-mail</td><td>Nom, adresse e-mail, choix de désinscription</td><td>Informer nos clients et les personnes ayant fait une demande de nos nouveautés et offres liées à leur activité</td><td>Intérêt légitime ; désinscription possible à tout moment, en un clic dans chaque e-mail ou depuis l’espace client</td></tr>
<tr><td>Avis</td><td>Note, commentaire, prénom, initiale du nom, nom du commerce, date</td><td>Recueillir votre retour ; le publier sur ce site, seulement si vous l’acceptez</td><td>Consentement (case à cocher, retirable à tout moment)</td></tr>
<tr><td>Parrainage</td><td>Code, lien entre parrain et filleul, mois offerts</td><td>Gérer le parrainage et appliquer les mois offerts</td><td>Exécution du contrat</td></tr>
<tr><td>Demande de résiliation</td><td>Motif, message, date d’effet</td><td>Traiter votre demande</td><td>Exécution du contrat</td></tr>
<tr><td>Navigation sur ce site</td><td>Adresse IP, type de navigateur, pages demandées (journaux techniques de l’hébergeur)</td><td>Sécurité, prévention des abus, bon fonctionnement</td><td>Intérêt légitime</td></tr>
<tr><td>Mesure de fréquentation</td><td>Date, page visitée, nombre de visites. Aucun cookie, aucune adresse IP, aucun identifiant ; l’option « Ne pas me suivre » est respectée</td><td>Savoir quelles pages sont consultées</td><td>Intérêt légitime (mesure anonyme)</td></tr>
<tr><td>Anti-abus des formulaires</td><td>Empreinte irréversible de l’adresse IP</td><td>Limiter les envois automatisés</td><td>Intérêt légitime</td></tr>
<tr><td>Démonstration de réservation</td><td>Prénom (fictif conseillé), téléphone (facultatif), créneau, empreinte irréversible de l’adresse IP</td><td>Montrer le fonctionnement de la réservation, éviter les abus</td><td>Intérêt légitime</td></tr>
<tr><td>Suivi de campagne (si accepté)</td><td>Paramètres UTM de l’adresse visitée, site d’origine, page d’arrivée</td><td>Savoir quelle annonce ou quel lien a amené la demande</td><td>Consentement</td></tr>
</tbody></table></div>
<p>Les sites d’exemple (salon, cabinet, restaurant…) ne transmettent rien : les réservations et paiements simulés restent dans votre navigateur. Aucune donnée sensible n’est demandée ; merci de ne pas en saisir dans les champs libres.</p>

<h2 id="durees">3. Durées de conservation</h2>
<ul>
<li>Demande non suivie d’une commande : 3 ans après le dernier contact.</li>
<li>Compte et données liées à l’abonnement : pendant le contrat, puis 5 ans (prescription).</li>
<li>Factures et pièces comptables : 10 ans (obligation légale).</li>
<li>Dossier de création et données des réservations : pendant le contrat, puis supprimés au plus tard 30 jours après la fin de l’abonnement, sauf demande de récupération.</li>
<li>Informations sur les paiements reçus via Stripe : pendant le contrat, puis 30 jours ; l’historique complet reste dans votre compte Stripe.</li>
<li>Avis publiés : jusqu’au retrait de votre consentement.</li>
<li>Envoi d’actualités : jusqu’à votre désinscription, et au plus 3 ans après notre dernier échange si vous n’êtes pas client.</li>
<li>Journaux techniques : selon la politique de l’hébergeur, en principe quelques semaines.</li>
<li>Compteurs de visites : 13 mois au plus. Paramètres UTM : 30 jours dans votre navigateur.</li>
<li>Réservations de la page de démonstration : supprimées au bout de 24 heures.</li>
</ul>

<h2 id="destinataires">4. Destinataires et prestataires</h2>
<p>Vos données sont accessibles à l’Éditeur seul. Elles sont traitées par les prestataires suivants, uniquement pour fournir le service :</p>
<ul>
<li><strong>Cloudflare, Inc.</strong> (États-Unis) : hébergement du site, base de données, réseau de diffusion ;</li>
<li><strong>Resend, Inc.</strong> (États-Unis) : envoi des e-mails de service ;</li>
<li><strong>GitHub, Inc.</strong> (États-Unis) : conservation du code source (sans données de clients) ;</li>
<li><strong>Stripe Payments Europe, Ltd.</strong> (Irlande) : paiements. Stripe agit comme responsable de traitement indépendant pour l’ouverture des comptes, la vérification d’identité, la lutte contre la fraude et les paiements (<a href="https://stripe.com/fr/privacy" rel="noopener" target="_blank">politique de confidentialité de Stripe</a>).</li>
</ul>
<p>Les polices de caractères sont hébergées sur notre propre site : aucun appel n’est fait à Google Fonts. Nous ne vendons ni ne louons aucune donnée. Les données peuvent être communiquées aux autorités qui en font la demande légale.</p>

<h2 id="transferts">5. Transferts hors Union européenne</h2>
<p>Cloudflare, Resend et GitHub sont établis aux États-Unis. Ces transferts s’appuient sur le cadre de protection des données UE–États-Unis (Data Privacy Framework) ou sur les clauses contractuelles types de la Commission européenne, selon les prestataires.</p>

<h2 id="droits">6. Vos droits</h2>
<p>Vous disposez d’un droit d’accès, de rectification, d’effacement, de limitation, d’opposition et de portabilité, du droit de retirer votre consentement à tout moment et de définir des directives sur le sort de vos données après votre décès. Pour les exercer, utilisez [[CONTACT]] ; nous répondons dans un délai d’un mois. Si vous êtes client d’un commerçant équipé par nos soins, adressez-vous d’abord à ce commerçant ; nous l’aiderons à vous répondre.</p>
<p>Vous pouvez introduire une réclamation auprès de la CNIL : <a href="https://www.cnil.fr/fr/plaintes" rel="noopener" target="_blank">www.cnil.fr/fr/plaintes</a>.</p>

<h2 id="securite">7. Sécurité</h2>
<p>Les échanges sont chiffrés (HTTPS). Les mots de passe sont enregistrés sous forme chiffrée irréversible. L’accès aux données est limité à l’Éditeur et chaque consultation d’un compte client est enregistrée. Les clés secrètes (paiement, e-mail) sont stockées hors du code. Les numéros de carte sont saisis chez Stripe et ne transitent jamais par nos serveurs. En cas de violation de données présentant un risque pour vous, nous prévenons la CNIL dans les 72 heures et vous informons dans les meilleurs délais.</p>

<h2 id="cookies">8. Cookies</h2>
<p>Le détail figure sur la page <a href="/cookies">cookies</a>. Vous pouvez modifier vos choix à tout moment avec le lien « Gérer les cookies » en bas de page.</p>

<h2 id="mineurs">9. Mineurs</h2>
<p>Ce service s’adresse à des professionnels et associations, représentés par des personnes majeures. Nous ne collectons pas sciemment de données de mineurs.</p>

<h2 id="evolutions">10. Évolution de cette politique</h2>
<p>Nous pouvons mettre à jour cette politique, par exemple à l’ouverture de nouveaux services. La date de dernière mise à jour figure en haut de la page ; en cas de changement important, nos clients sont prévenus par e-mail.</p>
""")

    # ------------------------------------------------------------------ cookies
    pages["cookies"] = dict(
        title="Cookies et stockage local",
        desc="Ce que ce site enregistre dans votre navigateur et comment gérer vos choix.",
        lede="Ce que le site enregistre dans votre navigateur, ce qui demande votre accord, et comment changer d’avis.",
        body="""
<div class="callout"><strong>En résumé.</strong> Ce site n’utilise ni publicité, ni outil de mesure d’audience tiers, ni police chargée chez Google. La fréquentation est comptée par nos soins, sans cookie ni identifiant. Seul le suivi des campagnes (UTM) est optionnel et ne démarre qu’avec votre accord.</div>
<p><button type="button" class="btn sm" data-cookies>Gérer mes choix maintenant</button></p>

<h2 id="quoi">1. Ce que nous enregistrons</h2>
<div class="tw"><table>
<thead><tr><th>Nom</th><th>Type</th><th>Rôle</th><th>Durée</th><th>Accord requis ?</th></tr></thead>
<tbody>
<tr><td><code>sv_session</code></td><td>Cookie</td><td>Vous garde connecté à votre compte</td><td>30 jours au plus</td><td>Non (nécessaire)</td></tr>
<tr><td><code>sv_consent</code></td><td>Stockage local</td><td>Mémorise vos choix sur les cookies</td><td>13 mois au plus</td><td>Non (nécessaire)</td></tr>
<tr><td><code>sv_theme</code></td><td>Stockage local</td><td>Mémorise le thème clair ou sombre que vous avez choisi</td><td>Jusqu’à effacement</td><td>Non (préférence demandée par vous)</td></tr>
<tr><td>Données des sites d’exemple</td><td>Stockage local</td><td>Gardent les réservations et paiements simulés que vous faites dans les démonstrations, pour les afficher dans l’espace d’exemple</td><td>Jusqu’à effacement</td><td>Non (fonction demandée par vous)</td></tr>
<tr><td><code>sv_utm</code></td><td>Stockage local</td><td>Garde l’origine de votre visite (paramètres UTM) pour la joindre à votre demande</td><td>30 jours</td><td><strong>Oui</strong></td></tr>
</tbody></table></div>
<p>Ces informations restent dans votre navigateur et ne sont envoyées à aucun tiers. Le cookie de session n’est envoyé qu’à notre site, en connexion chiffrée.</p>

<h2 id="utm">2. Le suivi UTM, c’est quoi ?</h2>
<p>Quand vous cliquez sur une annonce ou un lien partagé, l’adresse peut contenir des repères comme <code>utm_source=facebook</code>. Si vous acceptez, nous les gardons 30 jours pour savoir d’où vient votre demande. Si vous refusez, rien n’est enregistré et ces repères sont ignorés.</p>

<h2 id="tiers">3. Contenus de tiers</h2>
<p>Aucun. Les polices de caractères et tous les fichiers du site sont servis depuis notre propre domaine. Sur le site d’un commerçant qui propose le paiement en ligne, la page de paiement de Stripe peut déposer ses propres cookies, nécessaires à la sécurité du paiement et à la lutte contre la fraude ; ils sont décrits par Stripe et par le commerçant.</p>

<h2 id="gerer">4. Changer d’avis</h2>
<p>Vous pouvez modifier vos choix à tout moment avec le lien « Gérer les cookies » en bas de chaque page, ou effacer les données du site dans les réglages de votre navigateur. Nous vous redemandons votre choix au plus tard au bout de 13 mois.</p>

<h2 id="plus">5. En savoir plus</h2>
<p>Voir la <a href="/confidentialite">politique de confidentialité</a>. Informations de la CNIL sur les cookies : <a href="https://www.cnil.fr/fr/cookies-et-autres-traceurs" rel="noopener" target="_blank">cnil.fr</a>.</p>
""")

    for p in pages.values():
        for k in ("title", "desc", "lede", "body", "notice"):
            if k in p:
                p[k] = fill(p[k])
    return pages
