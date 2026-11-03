# Tests (banc local)

Banc d'essai hors ligne : un serveur Node émule D1 en mémoire et exécute `worker/worker.js`.
Jamais lancé contre le site en ligne. Prérequis : Node 22, Python 3 + Playwright, Chrome.

1. `bash tests/bench/sync.sh` (copie le Worker dans le banc) puis `bash tests/bench/restart.sh`
2. `NOPOP=1 python3 tests/bench/e2e1.py r.json` etc. (e2e2 → e2e6 s'enchaînent sans redémarrer ; api_tests, api_v2, e2e7, e2e8, e2e9 : redémarrer avant chacun).

Chemins à adapter dans `restart.sh`/`sync.sh` si le dépôt n'est pas dans /home/claude.
