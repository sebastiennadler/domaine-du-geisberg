#!/usr/bin/env python3
"""Prépare la livraison du site à l'hébergeur (DECLIC) : génère la version à livrer (sans le mode
« Notes pour Marc »), vérifie, puis archive dist/ dans livraison/domainedugeisberg-<date>.zip.

Usage : python3 tools/package.py
Le dossier livraison/ n'est pas suivi par git. L'archive contient la racine du site telle qu'elle doit être
déposée sur l'hébergeur (index.html, dossiers des langues, css, js, img, videos, audio, sitemap, robots).
"""

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
OUT = ROOT / "livraison"


def run(*cmd):
    print("$", " ".join(cmd))
    r = subprocess.run([sys.executable, *cmd], cwd=ROOT)
    if r.returncode:
        sys.exit(f"échec : {' '.join(cmd)}")


run("tools/build.py", "--prod")
run("tools/check.py")
OUT.mkdir(exist_ok=True)
stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
base = OUT / f"domainedugeisberg-{stamp}"
archive = shutil.make_archive(str(base), "zip", root_dir=DIST)
size = Path(archive).stat().st_size // 1024 // 1024
print(f"Livraison prête : {Path(archive).relative_to(ROOT)} ({size} Mo)")
print("Rappel : dist/ contient maintenant la version SANS notes ; relancer tools/build.py pour le site de travail.")
