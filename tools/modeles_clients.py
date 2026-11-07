# -*- coding: utf-8 -*-
"""Modèles de pages légales pour les SITES DES CLIENTS (commerçants), à générer à chaque création de site.

Usage :
    from modeles_clients import pages
    p = pages(dict(nom="Maison Olive SARL", ...), paiement=True, rdv=True)
    # p["mentions-legales"], p["confidentialite"], p["conditions"] : HTML prêt à insérer

Tout champ manquant s'affiche « [À compléter : …] » : le site ne doit pas être mis en ligne tant qu'il en reste.
Le commerçant relit et valide ces textes : il en est responsable (CGV de Devanture Web, articles 6 et 12).

Points à vérifier avec le commerçant avant la mise en ligne :
- activité réglementée (santé, droit, etc.) : ordre, titre, règles professionnelles, pas de données de santé (CGV art. 11) ;
- médiateur de la consommation : OBLIGATOIRE dès qu'il vend à des particuliers (art. L612-1 Code conso) ;
- droit de rétractation de ses clients : voir la clause « retractation » ci-dessous (dépend de l'activité) ;
- ATTENTION : si le droit de rétractation s'applique (cas général des prestations hors restauration/loisirs à date
  déterminée), un client qui annule avant sa prestation doit être remboursé intégralement, même tardivement :
  pas de frais d'annulation tardive ni d'acompte conservé dans ce cas (à faire confirmer par un juriste) ;
- dans le module de réservation avec paiement : case à cocher « J'accepte les conditions » + lien, et, si le
  rendez-vous tombe dans les 14 jours, demande expresse d'exécution avant la fin du délai de rétractation.
"""

CLOUDFLARE = "Cloudflare, Inc., 101 Townsend Street, San Francisco, CA 94107, États-Unis, téléphone : +1 888 993 5273"
STRIPE = "Stripe Payments Europe, Ltd., 1 Grand Canal Street Lower, Grand Canal Dock, Dublin, D02 H210, Irlande"


def pages(c, paiement=False, rdv=True, editeur="Devanture Web", editeur_contact="[À compléter : coordonnées de Devanture Web]"):
    def v(k, label):
        x = (c.get(k) or "").strip()
        return x if x else "<mark>[À compléter : %s]</mark>" % label

    nom = v("nom", "nom et prénom suivis de « EI », ou raison sociale et forme (SARL, SAS…)")
    capital = ("<li>Capital social : %s</li>" % c["capital"]) if c.get("capital") else ""
    immat = v("immat", "immatriculation : « RNE » ou « RCS de [ville] », et numéro SIREN")
    siret = v("siret", "SIRET")
    adr = v("adresse", "adresse de l’établissement")
    tel = v("tel", "téléphone")
    mail = v("email", "e-mail")
    tva = v("tva", "numéro de TVA intracommunautaire, ou « TVA non applicable, art. 293 B du CGI »")
    dirp = v("directeur", "directeur de la publication")
    regl = ("<li>Profession réglementée : %s</li>" % c["reglementee"]) if c.get("reglementee") else ""
    med = v("mediateur", "nom, adresse et site du médiateur de la consommation (obligatoire)")
    annul = v("annulation_h", "délai d’annulation gratuite, en heures (par exemple 24)")
    commerce = v("commerce", "nom commercial")

    P = {}
    P["mentions-legales"] = f"""
<h2>Éditeur du site</h2>
<ul><li>{nom}</li>{capital}<li>Immatriculation : {immat}</li><li>SIRET : {siret}</li><li>Adresse : {adr}</li>
<li>Téléphone : {tel}</li><li>E-mail : {mail}</li><li>TVA : {tva}</li>{regl}</ul>
<p>Directeur de la publication : {dirp}.</p>
<h2>Réalisation et hébergement</h2>
<p>Site réalisé et maintenu par {editeur} ({editeur_contact}). Hébergeur : {CLOUDFLARE}.</p>
{"<h2>Paiement en ligne</h2><p>Les paiements sont traités par " + STRIPE + ". Les numéros de carte sont saisis chez Stripe et ne sont jamais transmis à " + commerce + " ni à " + editeur + ".</p>" if paiement else ""}
<h2>Propriété intellectuelle</h2>
<p>Les textes, photos et logos de ce site appartiennent à {commerce} ou à leurs auteurs. Toute reproduction sans autorisation est interdite.</p>
<h2>Données personnelles</h2>
<p>Voir la politique de confidentialité.</p>
"""

    lignes = ["<tr><td>Formulaire de contact</td><td>Nom, e-mail ou téléphone, message</td><td>Vous répondre</td><td>Mesures précontractuelles / intérêt légitime</td><td>3 ans après le dernier contact</td></tr>"]
    if rdv:
        lignes.append("<tr><td>Réservation</td><td>Nom, prénom, téléphone, e-mail, prestation, date et heure, message éventuel</td><td>Gérer votre rendez-vous, vous envoyer la confirmation</td><td>Exécution du contrat</td><td>3 ans après le dernier rendez-vous</td></tr>")
    if paiement:
        lignes.append("<tr><td>Paiement en ligne</td><td>Référence, montant, date et statut du paiement (jamais le numéro de carte)</td><td>Encaisser, rembourser, tenir la comptabilité</td><td>Exécution du contrat ; obligation légale</td><td>10 ans (pièces comptables)</td></tr>")
    P["confidentialite"] = f"""
<h2>Responsable du traitement</h2>
<p>{nom}, {adr}, {mail}.</p>
<h2>Données, finalités et durées</h2>
<table><thead><tr><th>Situation</th><th>Données</th><th>Finalité</th><th>Base légale</th><th>Durée</th></tr></thead><tbody>{"".join(lignes)}</tbody></table>
<p>Merci de ne communiquer aucune information sur votre santé dans les formulaires.</p>
<h2>Destinataires</h2>
<p>{commerce} ; {editeur}, qui réalise et héberge le site pour notre compte (sous-traitant) ; ses prestataires Cloudflare, Inc. (hébergement) et Resend, Inc. (e-mails de confirmation), établis aux États-Unis, avec des garanties adaptées (cadre UE–États-Unis ou clauses contractuelles types).
{"Stripe Payments Europe, Ltd. traite les paiements en tant que responsable de traitement indépendant (<a href=\"https://stripe.com/fr/privacy\">politique de Stripe</a>)." if paiement else ""}</p>
<h2>Vos droits</h2>
<p>Accès, rectification, effacement, limitation, opposition, portabilité : écrivez à {mail}. Réponse sous un mois. Réclamation possible auprès de la CNIL (cnil.fr).</p>
<h2>Cookies</h2>
<p>Ce site ne dépose aucun cookie publicitaire ni de mesure d’audience. {"La page de paiement de Stripe utilise des cookies nécessaires à la sécurité du paiement et à la lutte contre la fraude." if paiement else ""}</p>
"""

    if paiement or rdv:
        retract = c.get("retractation_exclue")  # True pour restauration / loisirs à date déterminée (art. L221-28 12°)
        if retract:
            rt = ("<p>Conformément à l’article L221-28 12° du Code de la consommation, le droit de rétractation ne s’applique pas aux prestations de "
                  + v("type_prestation", "restauration ou loisirs") + " fournies à une date déterminée. Les conditions d’annulation ci-dessus s’appliquent.</p>")
        else:
            rt = ("<p>Pour une réservation faite à distance, vous disposez d’un délai de rétractation de 14 jours à compter de la réservation. "
                  "Si votre rendez-vous a lieu avant la fin de ce délai, vous demandez expressément, en cochant la case prévue lors de la réservation, que la prestation soit réalisée avant la fin du délai. "
                  "Vous pouvez vous rétracter jusqu’au rendez-vous en nous l’indiquant (e-mail, téléphone ou formulaire ci-dessous) : vous êtes alors remboursé intégralement sous 14 jours, par le même moyen de paiement. "
                  "Une fois la prestation entièrement réalisée, la rétractation n’est plus possible (article L221-28 1°).</p>"
                  "<p><strong>Formulaire de rétractation</strong> — À l’attention de " + nom + ", " + adr + ", " + mail + " : je vous notifie ma rétractation du contrat portant sur la prestation suivante : … ; réservée le : … ; nom : … ; adresse : … ; date : … ; signature (sur papier).</p>")
        P["conditions"] = f"""
<h2>Vendeur</h2>
<p>{nom}, {adr}, {tel}, {mail}, SIRET {siret}.</p>
<h2>Prestations et prix</h2>
<p>Les prestations, leur durée et leur prix sont indiqués sur le site. Les prix sont en euros, toutes taxes comprises (TTC).</p>
<h2>Réservation</h2>
<p>Vous choisissez une prestation et un créneau, puis vous confirmez{" et payez en ligne" if paiement else ""}. Un e-mail de confirmation récapitule votre rendez-vous{", le prix payé et la référence du paiement" if paiement else ""}.</p>
{"<h2>Paiement</h2><p>Le prix de la prestation est payé en ligne au moment de la réservation, par carte bancaire, via notre prestataire de paiement sécurisé Stripe. Vos données bancaires sont saisies chez Stripe et ne nous sont jamais communiquées. Un justificatif vous est remis ; une facture vous est délivrée sur demande.</p>" if paiement else ""}
<h2>Annulation et modification</h2>
<p>Vous pouvez annuler ou déplacer gratuitement votre rendez-vous jusqu’à {annul} heures avant l’heure prévue, depuis le lien de votre e-mail de confirmation ou par téléphone{" ; vous êtes alors remboursé intégralement, sous 5 à 10 jours" if paiement else ""}. {(v("regle_tardive", "règle en cas d’annulation tardive ou d’absence (par exemple : le montant reste acquis, sauf cas de force majeure justifié)") + ".") if c.get("retractation_exclue") else "Ces conditions s’appliquent sans préjudice de votre droit de rétractation ci-dessous."} Si nous devons annuler, vous êtes prévenu au plus vite et {"remboursé intégralement" if paiement else "un autre créneau vous est proposé"}.</p>
<h2>Droit de rétractation</h2>
{rt}
<h2>Réclamations et médiation</h2>
<p>Pour toute réclamation, contactez-nous : {mail}, {tel}. En cas de litige non résolu, vous pouvez recourir gratuitement au médiateur de la consommation : {med}.</p>
<h2>Droit applicable</h2>
<p>Droit français.</p>
"""
    return P
