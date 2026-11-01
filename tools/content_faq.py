# -*- coding: utf-8 -*-
"""Questions fréquentes (catégorie, identifiant, question, réponse en HTML)."""

CATS = [
    ("offre", "Offre et prix"),
    ("commande", "Commande et délais"),
    ("modif", "Modifications"),
    ("domaine", "Domaine et mail"),
    ("technique", "Technique"),
    ("contrat", "Contrat et résiliation"),
    ("donnees", "Données et sécurité"),
]

FAQ = [
    # ---------- Offre et prix ----------
    ("offre", "prix", "Quel est le prix exact ?",
     "<p>Deux formules, avec un engagement de 12 mois. <strong>Essentiel : 60 € HT par mois</strong> (720 € HT sur l’année). <strong>Pro : 100 € HT par mois</strong> (1 200 € HT sur l’année), avec la réservation en ligne et une adresse mail pro incluse. Il n’y a pas de frais de création à part : le site, le nom de domaine, l’hébergement, l’espace client et le guide pub sont compris dans les deux.</p>"
     "<p>Chaque adresse mail professionnelle supplémentaire coûte <strong>4 € HT par mois</strong>. Vous pouvez simuler votre total sur la page <a href=\"/offre\">Offre et prix</a>.</p>"),
    ("offre", "essentiel-pro", "Quelle différence entre Essentiel et Pro ?",
     "<p>L’<strong>Essentiel</strong> est le site vitrine complet : site de 5 pages, nom de domaine, hébergement, espace client, 1 modification par semaine et guide pub.</p>"
     "<p>Le <strong>Pro</strong> ajoute la <strong>réservation en ligne</strong> avec un agenda, et inclut <strong>1 adresse mail professionnelle</strong>. Il convient aux activités qui prennent des rendez-vous : coiffeur, esthétique, bien-être, coach, garage, restaurant.</p>"
     "<p>Vous pouvez tester la réservation sur la <a href=\"/reservation-demo\">page de démonstration</a>.</p>"),
    ("offre", "reservation", "Comment fonctionne la réservation en ligne ?",
     "<p>Sur votre site, un client choisit une prestation, un jour et un créneau libre, puis laisse son nom et son téléphone. Le créneau n’est alors plus proposé aux autres : pas de double réservation. Les réservations apparaissent dans l’agenda de votre espace client.</p>"
     "<p>Nous paramétrons pour vous vos prestations, leurs durées et vos horaires d’ouverture. Ne sont pas compris : le paiement ou l’acompte en ligne, les rappels par SMS et la synchronisation avec un autre agenda. Nous pouvons en parler sur devis.</p>"),
    ("offre", "changer-formule", "Puis-je passer de l’Essentiel au Pro ?",
     "<p>Oui, à tout moment : le Pro s’applique au début du mois suivant, et une nouvelle période de 12 mois commence à ce moment-là. Le passage du Pro à l’Essentiel se fait à l’échéance de la période en cours.</p>"),
    ("offre", "inclus", "Qu’est-ce qui est inclus dans l’abonnement ?",
     "<ul><li>Un site vitrine sur mesure, jusqu’à 5 pages, adapté au téléphone</li><li>Le nom de domaine, réservé et renouvelé chaque année pendant l’engagement</li><li>L’hébergement, avec certificat HTTPS</li><li>Un espace client pour suivre votre commande et modifier votre site</li><li>1 modification par semaine, que vous faites vous-même</li><li>Le guide pub, pas à pas, pour vous faire connaître</li></ul>"),
    ("offre", "non-inclus", "Qu’est-ce qui n’est pas inclus ?",
     "<p>Ne sont pas compris : la publicité faite pour vous, le référencement payant, une boutique en ligne, un système de réservation en ligne (compris dans la formule Pro), les pages au-delà de 5, une refonte complète du design, et les séances photo. Si vous avez besoin d’un de ces points, nous en parlons et nous faisons un devis séparé.</p>"),
    ("offre", "engagement-12", "Pourquoi un engagement de 12 mois ?",
     "<p>Le nom de domaine se renouvelle à l’année, et la création du site demande du temps de notre côté. L’engagement de 12 mois permet de garder un prix mensuel bas et fixe. Le prix ne change pas pendant l’engagement.</p>"),
    ("offre", "ht-ttc", "Les prix sont-ils hors taxes ou toutes taxes comprises ?",
     "<p>Les prix sont indiqués <strong>hors taxes (HT)</strong>. La TVA, si elle s’applique, est ajoutée et détaillée sur chaque facture.</p>"),
    ("offre", "paiement", "Comment se règle l’abonnement ?",
     "<p>Le paiement est mensuel et d’avance, par carte bancaire ou prélèvement SEPA, via un prestataire de paiement sécurisé. Nous ne conservons jamais vos coordonnées bancaires. Le premier mois est réglé à la validation de votre commande. Les modalités exactes vous sont confirmées avant tout paiement.</p>"),

    # ---------- Commande et délais ----------
    ("commande", "commander", "Comment commander ?",
     "<p>Remplissez la <a href=\"/commander\">demande en ligne</a>. Elle est sans engagement et sans paiement. Nous vous répondons pour valider les détails, puis vous acceptez les conditions et réglez le premier mois. Les 8 étapes sont décrites <a href=\"/#etapes\">sur la page d’accueil</a>.</p>"),
    ("commande", "delai", "En combien de temps mon site est-il en ligne ?",
     "<p>La livraison se fait sous <strong>5 jours ouvrés après réception de tous vos contenus</strong> : textes, photos, horaires, tarifs, adresse. Le délai commence quand le dossier est complet. La date prévue est affichée dans votre espace client.</p>"),
    ("commande", "besoin", "De quoi ai-je besoin pour commencer ?",
     "<ul><li>Votre activité et le nom du commerce</li><li>Adresse et téléphone</li><li>Horaires d’ouverture</li><li>Tarifs et durées des prestations</li><li>Quelques photos de votre commerce</li><li>Vos couleurs, si vous en avez</li><li>Le nom de domaine souhaité</li></ul>"),
    ("commande", "sans-photos", "Je n’ai ni photos ni textes prêts, que faire ?",
     "<p>Envoyez vos informations en vrac, même en brouillon : nous les mettons en forme et nous corrigeons les fautes. Des photos prises avec votre téléphone suffisent si elles sont nettes et bien éclairées.</p>"),
    ("commande", "apercu", "Puis-je voir mon site avant sa mise en ligne ?",
     "<p>Oui. Vous recevez un aperçu et vous demandez vos ajustements avant de valider. Le site n’est mis en ligne qu’après votre accord.</p>"),
    ("commande", "pages", "Combien de pages comprend mon site ?",
     "<p>Jusqu’à 5 pages (par exemple : accueil, services ou carte, à propos, tarifs, contact). Une page supplémentaire fait l’objet d’un devis.</p>"),

    # ---------- Modifications ----------
    ("modif", "modifier", "Comment je modifie mon site ?",
     "<p>Depuis votre espace client, avec l’éditeur : vous remplacez un texte ou une photo, vous ajoutez ou supprimez un bloc. Vous ne changez pas la mise en page, ce qui évite de casser le site. Vous pouvez tester le principe sur la <a href=\"/#modifier\">démonstration de l’accueil</a>.</p>"),
    ("modif", "une-par-semaine", "Que veut dire « 1 modification par semaine » ?",
     "<p>Chaque semaine, vous pouvez faire une modification : remplacer un texte, remplacer une photo, ajouter un bloc ou en supprimer un. Le compteur est visible dans votre espace client. Une modification non utilisée ne se cumule pas avec la semaine suivante.</p>"),
    ("modif", "annuler", "Puis-je annuler une modification ?",
     "<p>Oui. L’éditeur garde un historique de vos changements et vous permet de revenir en arrière.</p>"),
    ("modif", "plus", "Et si j’ai besoin de faire plus de changements ?",
     "<p>Une nouvelle page, un nouveau design ou une fonction en plus ne font pas partie de l’abonnement. Écrivez-nous : nous vous proposons un devis clair avant de commencer.</p>"),

    # ---------- Domaine et mail ----------
    ("domaine", "domaine-a-moi", "Le nom de domaine est-il à moi ?",
     "<p>Nous réservons, gérons et renouvelons le nom de domaine pendant l’engagement. À la fin, vous pouvez partir avec votre nom grâce au code de transfert, à condition que les sommes dues soient réglées.</p>"),
    ("domaine", "domaine-pris", "Et si le nom que je veux est déjà pris ?",
     "<p>Nous vous proposons des variantes proches (autre terminaison comme .fr ou .com, ajout de la ville ou du métier). Vous choisissez avant toute réservation.</p>"),
    ("domaine", "renouvellement", "Quand le domaine est-il renouvelé ?",
     "<p>Chaque année, pendant l’engagement. Le renouvellement est compris dans l’abonnement, vous n’avez rien à payer en plus ni à y penser.</p>"),
    ("domaine", "domaine-existant", "J’ai déjà un nom de domaine, puis-je le garder ?",
     "<p>En général oui : nous relions votre domaine existant à votre nouveau site. Dans ce cas, il reste chez votre hébergeur actuel et son renouvellement reste à votre charge. Précisez-le dans la demande.</p>"),
    ("domaine", "mail-pro", "Comment fonctionne l’adresse mail professionnelle ?",
     "<p>Elle coûte 4 € HT par mois et par adresse (la première est incluse dans la formule Pro), et suit la durée de votre abonnement (par exemple prenom@votresite.fr). La boîte est de taille limitée, pour un usage professionnel normal, sans envoi de masse. Un guide vous explique comment la configurer sur votre téléphone. Si vous résiliez, les adresses sont fermées après 30 jours pour vous laisser récupérer vos mails.</p>"),

    # ---------- Technique ----------
    ("technique", "mobile", "Mon site sera-t-il lisible sur téléphone ?",
     "<p>Oui, il est conçu d’abord pour le téléphone, puis adapté aux tablettes et aux ordinateurs. Nous le vérifions sur téléphone avant chaque mise en ligne.</p>"),
    ("technique", "hebergement", "Où est hébergé mon site ?",
     "<p>Chez Cloudflare, sur un réseau mondial de serveurs qui rapproche le site de vos visiteurs. Le certificat HTTPS (le petit cadenas) est inclus.</p>"),
    ("technique", "google", "Mon site apparaîtra-t-il sur Google ?",
     "<p>Nous préparons les bases (titres, descriptions, adresse, horaires). Mais nous ne pouvons pas promettre une position dans Google ni un nombre de visites : cela dépend de votre activité et de la concurrence. Le guide pub vous explique les gestes qui aident, comme la fiche Google Business et les avis clients.</p>"),
    ("technique", "disponibilite", "Mon site sera-t-il toujours disponible ?",
     "<p>Nous mettons tout en œuvre pour qu’il le soit, avec un hébergement fiable et des sauvegardes. Il s’agit d’une obligation de moyens : aucune disponibilité de 100 % n’est garantie.</p>"),
    ("technique", "relecture", "Qui relit mon site avant la mise en ligne ?",
     "<p>Une personne. Textes corrigés, photos vérifiées, liens testés, affichage contrôlé sur téléphone. Rien n’est publié sans cette relecture.</p>"),

    # ---------- Contrat et résiliation ----------
    ("contrat", "duree", "Combien de temps dure l’engagement ?",
     "<p>12 mois à partir de la mise en ligne de l’abonnement. Le prix reste le même pendant cette durée. Un rappel vous est envoyé 60 jours avant la fin.</p>"),
    ("contrat", "reconduction", "Que se passe-t-il à la fin des 12 mois ?",
     "<p>L’abonnement est reconduit pour 12 mois, sauf si vous nous prévenez par écrit au moins 30 jours avant la date d’échéance. Vous recevez un rappel 60 jours avant. Le détail figure dans les <a href=\"/cgv\">conditions générales de vente</a>.</p>"),
    ("contrat", "resilier", "Comment résilier ?",
     "<p>Par écrit (e-mail ou courrier), avec un préavis de 30 jours avant l’échéance des 12 mois. Un bouton de résiliation sera aussi proposé dans votre espace client.</p>"),
    ("contrat", "avant-terme", "Puis-je arrêter avant la fin des 12 mois ?",
     "<p>L’abonnement est un engagement de 12 mois : les mensualités restantes restent dues, sauf manquement grave de notre part. C’est le prix de la mensualité basse.</p>"),
    ("contrat", "fin-site", "Que devient mon site après la résiliation ?",
     "<p>Il est mis hors ligne à la date de fin. Vous pouvez demander la récupération de vos textes et photos, et le transfert de votre nom de domaine. Les adresses mail sont fermées 30 jours plus tard.</p>"),
    ("contrat", "retractation", "Ai-je un droit de rétractation ?",
     "<p>L’offre s’adresse aux professionnels. Le droit de rétractation prévu pour les consommateurs ne s’applique donc pas. Avant tout paiement, votre demande reste sans engagement : vous pouvez y renoncer librement.</p>"),

    # ---------- Données et sécurité ----------
    ("donnees", "donnees", "Que faites-vous de mes données ?",
     "<p>Nous utilisons vos informations uniquement pour répondre à votre demande, créer votre site et gérer votre abonnement. Nous ne les vendons pas. Tout est expliqué dans la <a href=\"/confidentialite\">politique de confidentialité</a>.</p>"),
    ("donnees", "formulaire-site", "Et les messages envoyés par les visiteurs de mon site ?",
     "<p>Les messages du formulaire de contact de votre site vous sont destinés. Pour ces données, c’est vous qui êtes responsable du traitement. Nous préremplissons les mentions utiles sur votre site.</p>"),
    ("donnees", "carte", "Mes coordonnées bancaires sont-elles en sécurité ?",
     "<p>Le paiement est géré par un prestataire spécialisé. Vos numéros de carte ne passent pas par nos serveurs et ne sont jamais enregistrés par nous.</p>"),
    ("donnees", "cookies", "Utilisez-vous des cookies ?",
     "<p>Peu. Votre choix de thème et vos préférences sont mémorisés dans votre navigateur. Le suivi des campagnes (UTM) n’est activé qu’avec votre accord. Vous pouvez changer d’avis à tout moment via « Gérer les cookies » en bas de page, ou lire la <a href=\"/cookies\">page cookies</a>.</p>"),
]
