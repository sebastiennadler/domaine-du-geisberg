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

# Garde-fous avant livraison : rien du site de travail ne doit partir chez l'hébergeur.
problems = []
for f in DIST.rglob("*.html"):
    h = f.read_text(encoding="utf-8")
    redirect = 'http-equiv="refresh"' in h  # pages de renvoi des anciennes adresses : noindex voulu
    for bad in ("data-note=", 'id="nbtn"', "Notes pour Marc", "github.io") + (() if redirect or f.name == "404.html" else ("noindex",)):
        if bad in h:
            problems.append(f"{f.relative_to(DIST)} : contient « {bad} »")
    if "Content-Security-Policy" not in h:
        problems.append(f"{f.relative_to(DIST)} : pas de politique de sécurité (CSP)")
    if "<script>" in h or "<script " in h.replace('<script src=', '').replace('<script type="application/ld+json"', '').replace('<script type="application/json"', '').replace('<script async src=', ''):
        problems.append(f"{f.relative_to(DIST)} : script en ligne (interdit par la CSP)")
for must in (".htaccess", "404.html", "sitemap.xml", "robots.txt", "fonts"):
    if not (DIST / must).exists():
        problems.append(f"{must} manquant dans dist/")
if problems:
    sys.exit("Livraison refusée :\n  - " + "\n  - ".join(problems))
OUT.mkdir(exist_ok=True)
stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
base = OUT / f"domainedugeisberg-{stamp}"
archive = shutil.make_archive(str(base), "zip", root_dir=DIST)
size = Path(archive).stat().st_size // 1024 // 1024
print(f"Livraison prête : {Path(archive).relative_to(ROOT)} ({size} Mo)")
print("Rappel : dist/ contient maintenant la version SANS notes ; relancer tools/build.py pour le site de travail.")
