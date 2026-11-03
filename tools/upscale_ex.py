# -*- coding: utf-8 -*-
"""Améliore la netteté des photos d'exemple (agrandissement Lanczos x2 + léger renforcement, JPEG qualité 88).
Chaque fichier n'est traité qu'une fois (liste dans tools/ex_upscaled.txt). Pour de vraies photos HD, remplacer les fichiers de site/assets/ex/."""
import os, glob
from PIL import Image, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "site", "assets", "ex"); L = os.path.join(ROOT, "tools", "ex_upscaled.txt")
done = set(open(L).read().split()) if os.path.exists(L) else set()
for f in sorted(glob.glob(D + "/*.jpg")):
    n = os.path.basename(f)
    if n in done: continue
    im = Image.open(f).convert("RGB"); w, h = im.size
    im = im.resize((w * 2, h * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.4, percent=70, threshold=2))
    im.save(f, "JPEG", quality=88, optimize=True, progressive=True); done.add(n); print(n, (w, h), "->", im.size, os.path.getsize(f) // 1024, "ko")
open(L, "w").write("\n".join(sorted(done)) + "\n")
