# Devanture Web

Site public, généré par `python3 tools/build.py` (sources dans `tools/`), servi depuis `site/` par un Worker Cloudflare (`worker/worker.js`).

- Modifier un texte : éditer `tools/content_*.py` ou `tools/build.py`, relancer le build, pousser sur `main` : le site se met à jour en ~1 minute.
- Identité de l'éditeur (mentions légales) : dictionnaire `EDITOR` dans `tools/build.py`.
- Ce dépôt ne contient aucun secret.

## Commande, paiement de l'abonnement et factures

Parcours client (espace, onglet « Abonnement ») : récapitulatif → informations de facturation (SIREN) → case « J'accepte les CGV » (version `CGV_VERSION` dans `worker/worker.js`) → e-mail de confirmation avec les CGV jointes → paiement du 1er mois par Stripe Checkout (carte ou SEPA) → facture émise. À la mise en ligne, l'admin passe l'abonnement en « actif » : l'abonnement mensuel Stripe est créé automatiquement (1er prélèvement un mois après la mise en ligne).

Pour l'activer :
1. Remplir `EMETTEUR` (et `TVA_FRANCHISE` si franchise de TVA) en haut de la section « Commande, paiement » de `worker/worker.js`, et `EDITOR` dans `tools/build.py`.
2. Secrets Cloudflare du Worker : `STRIPE_SECRET_KEY` (clé secrète Stripe, idéalement une clé restreinte) et `STRIPE_WEBHOOK_SECRET`.
3. Dans Stripe > Développeurs > Webhooks : point de terminaison `https://<domaine>/api/stripe/webhook`, événements `checkout.session.completed`, `checkout.session.async_payment_succeeded`, `checkout.session.async_payment_failed`, `invoice.created`, `invoice.paid`, `invoice.payment_failed`.
4. Tester d'abord en mode test de Stripe (clés `sk_test_…`).

Factures : numérotation continue (`F2026-000001`…), non modifiables ni supprimables (déclencheurs SQL), mentions de la facturation électronique (SIREN client, nature de l'opération). Chaque facture est téléchargeable au format UBL (EN 16931) pour import dans la plateforme agréée de facturation électronique choisie. À chaque mise à jour des CGV : changer `CGV_VERSION` et `UPDATED_*` dans `tools/build.py`.
