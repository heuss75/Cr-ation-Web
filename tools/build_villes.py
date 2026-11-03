"""Génère site/assets/villes.json : toutes les communes de France (dont arrondissements de Paris, Lyon, Marseille)
à partir des fichiers ouverts d'Etalab « decoupage-administratif » (licence MIT) : sources/communes.csv + sources/codes-postaux.json.
Usage : python3 tools/build_villes.py /chemin/vers/decoupage-administratif"""
import csv, json, sys, os
src = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/etalab/decoupage-administratif'
cp = {}
for x in json.load(open(os.path.join(src, 'sources/codes-postaux.json'))):
    cp.setdefault(x['codeCommune'], [])
    if x['codePostal'] not in cp[x['codeCommune']]: cp[x['codeCommune']].append(x['codePostal'])
out, seen = [], set()
for r in csv.DictReader(open(os.path.join(src, 'sources/communes.csv'), encoding='utf-8')):
    if r['TYPECOM'] not in ('COM', 'ARM'): continue
    nom = r['LIBELLE'].strip(); codes = cp.get(r['COM'], [])
    if r['COM'] in ('75056', '69123', '13055'): codes = [{'75056': '75000', '69123': '69000', '13055': '13000'}[r['COM']]]
    c = codes[0] if codes else r['DEP'].ljust(5, '0')
    k = nom + '|' + c
    if k in seen: continue
    seen.add(k); out.append(nom + '|' + c)
out.sort()
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site', 'assets', 'villes.json')
json.dump(out, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(out), 'communes ->', dst, os.path.getsize(dst) // 1024, 'Ko')
