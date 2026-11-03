"""Régénère les gros fichiers de test (non versionnés) : python3 make.py"""
import os, numpy as np
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__)); rng = np.random.default_rng(1)
def jpg(name, w, h, q):
    Image.fromarray(rng.integers(0, 255, (h, w, 3), dtype=np.uint8)).save(os.path.join(here, name), quality=q)
jpg("photo-reelle.jpg", 3000, 2000, 75); jpg("grosse-photo.jpg", 4000, 3000, 90)
open(os.path.join(here, "gros.pdf"), "wb").write(b"%PDF-1.4\n" + b"0" * 1500000 + b"\n%%EOF")
