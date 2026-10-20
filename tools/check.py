#!/usr/bin/env python3
"""Vérifie le site généré dans dist/ : liens et images cassés, fichiers d'images inutilisés, attributs
manquants sur les images (alt, width/height), poids des pages. À lancer après tools/build.py.

Usage : python3 tools/check.py
Code de retour 1 s'il y a au moins une erreur (pratique dans un workflow GitHub).
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent / "dist"  # on vérifie ce qui sera publié
LANG_DIRS = ["", "en", "de", "es", "pt", "nl", "zh"]
IMG_EXT = {".webp", ".jpg", ".jpeg", ".png", ".svg"}


class Collector(HTMLParser):
    """Relève les URL locales (href, src, srcset, poster, background-image) et les <img> incomplets."""

    def __init__(self):
        super().__init__()
        self.urls, self.img_issues, self.ids = [], [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for key in ("href", "src", "poster"):
            if a.get(key):
                self.urls.append((key, a[key]))
        for key in ("srcset", "imagesrcset"):
            if a.get(key):
                for part in a[key].split(","):
                    self.urls.append((key, part.strip().split(" ")[0]))
        if a.get("style") and "url(" in a["style"]:
            for m in re.finditer(r"url\(['\"]?([^'\")]+)", a["style"]):
                self.urls.append(("style", m.group(1)))
        if tag == "img":
            missing = [k for k in ("alt", "width", "height") if k not in a]
            if missing:
                self.img_issues.append((a.get("src", "?"), missing))


BASE_PATHS = ("/domaine-du-geisberg/", "/")  # racines absolues possibles (site de travail GitHub Pages, hébergeur)


def local(url):
    """Chemin relatif local, ou None si l'URL est externe / mailto / tel / ancre.
    Un chemin absolu (page 404) est ramené à la racine de dist/."""
    u = urlsplit(url)
    if u.scheme or url.startswith(("#", "mailto:", "tel:", "data:")):
        return None
    path = unquote(u.path)
    for base in BASE_PATHS:
        if path.startswith(base):
            return str(ROOT / path[len(base):]), u.fragment
    return path, u.fragment


errors, warnings = [], []
used_files = set()
pages = []
if not ROOT.exists():
    sys.exit("dist/ absent : lancer d'abord python3 tools/build.py")
for d in LANG_DIRS:
    pages += sorted((ROOT / d).glob("*.html")) if d else sorted(ROOT.glob("*.html"))

for page in pages:
    c = Collector()
    c.feed(page.read_text(encoding="utf-8"))
    for key, url in c.urls:
        loc = local(url)
        if not loc:
            continue
        path, frag = loc
        target = (page.parent / path).resolve() if path else page
        if path and not target.exists():
            errors.append(f"{page.relative_to(ROOT)} : {key} introuvable → {url}")
        elif target.is_file():
            used_files.add(target)
    for src, missing in c.img_issues:
        warnings.append(f"{page.relative_to(ROOT)} : <img src=\"{src}\"> sans {', '.join(missing)}")

# ancres (#dispo, #demande…) : la cible doit exister dans la page visée
for page in pages:
    c = Collector()
    c.feed(page.read_text(encoding="utf-8"))
    for key, url in c.urls:
        loc = local(url)
        if loc and loc[1] and loc[0]:
            target = (page.parent / loc[0]).resolve()
            if target.suffix == ".html" and target.exists():
                tc = Collector()
                tc.feed(target.read_text(encoding="utf-8"))
                if loc[1] not in tc.ids:
                    errors.append(f"{page.relative_to(ROOT)} : ancre #{loc[1]} absente de {target.relative_to(ROOT)}")

# images présentes mais jamais utilisées
for f in sorted((ROOT / "img").rglob("*")):
    if f.is_file() and f.suffix.lower() in IMG_EXT and f.resolve() not in used_files:
        warnings.append(f"image inutilisée : {f.relative_to(ROOT)} ({f.stat().st_size // 1024} Ko)")

# poids des pages d'accueil : HTML + CSS + JS + première photo du bandeau (ce que le visiteur charge d'abord)
index = ROOT / "index.html"
first = re.search(r'<link rel="preload" as="image" imagesrcset="([^" ]+)', index.read_text(encoding="utf-8"))
weight = index.stat().st_size + (ROOT / "css/style.css").stat().st_size + (ROOT / "js/site.js").stat().st_size
if first:
    weight += (ROOT / first.group(1)).stat().st_size

print(f"{len(pages)} pages vérifiées")
for e in errors:
    print("ERREUR", e)
for w in warnings:
    print("avertissement", w)
print(f"Accueil : {weight // 1024} Ko avant les photos chargées à la demande (HTML + CSS + JS + 1re photo)")
print(f"{len(errors)} erreur(s), {len(warnings)} avertissement(s)")
sys.exit(1 if errors else 0)
