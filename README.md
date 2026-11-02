# Devanture Web

Site public, généré par `python3 tools/build.py` (sources dans `tools/`), servi depuis `site/` par un Worker Cloudflare (`worker/worker.js`).

- Modifier un texte : éditer `tools/content_*.py` ou `tools/build.py`, relancer le build, pousser sur `main` : le site se met à jour en ~1 minute.
- Identité de l'éditeur (mentions légales) : dictionnaire `EDITOR` dans `tools/build.py`.
- Ce dépôt ne contient aucun secret.
