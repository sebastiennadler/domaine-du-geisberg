#!/usr/bin/env python3
"""Génère le site statique : templates Jinja2 + contenu par langue (tools/content/*.json).

Usage : python3 tools/build.py
Sortie : pages FR à la racine, autres langues dans /en, /de, /es, /pt, /nl, /zh.

Les photos sont décrites dans tools/content/images.json (produit par tools/photos.py) ; les
gabarits les affichent avec la fonction `pic()` définie plus bas, qui écrit un <img> complet
(srcset, dimensions, chargement différé).
"""

import hashlib
import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "tools" / "templates"
CONTENT = ROOT / "tools" / "content"
SITE_URL = "https://www.domainedugeisberg.fr"

LANGS = [  # ordre demandé : FR, EN, DE, ES, PT, NL, ZH
    ("fr", "Français", "🇫🇷", ""),
    ("en", "English", "🇬🇧", "en/"),
    ("de", "Deutsch", "🇩🇪", "de/"),
    ("es", "Español", "🇪🇸", "es/"),
    ("pt", "Português", "🇵🇹", "pt/"),
    ("nl", "Nederlands", "🇳🇱", "nl/"),
    ("zh", "中文", "🇨🇳", "zh/"),
]
PAGES = [
    "index",
    "le-domaine",
    "gites",
    "videos",
    "autour",
    "avis",
    "visite",
    "reservation",
    "diaporama",
    "mentions-legales",
]
# anciennes adresses conservées : chacune renvoie vers la page qui la remplace
REDIRECTS = {"gite-1": "gites.html#gite-1", "gite-2": "gites.html#gite-2"}

env = Environment(
    loader=FileSystemLoader(str(TPL)),
    autoescape=select_autoescape(["html"]),
    trim_blocks=True,
    lstrip_blocks=True,
)

shared = json.loads((CONTENT / "shared.json").read_text(encoding="utf-8"))
images = json.loads((CONTENT / "images.json").read_text(encoding="utf-8"))
busy = (
    json.loads((CONTENT / "busy.json").read_text(encoding="utf-8"))
    if (CONTENT / "busy.json").exists()
    else {}
)
shared["busy1"] = ",".join(f"{a}/{b}" for a, b in busy.get("gite1", []))
shared["busy2"] = ",".join(f"{a}/{b}" for a, b in busy.get("gite2", []))
shared["busy_updated"] = busy.get("updated", "")
contents = {}
for code, *_ in LANGS:
    p = CONTENT / f"{code}.json"
    if p.exists():
        contents[code] = json.loads(p.read_text(encoding="utf-8"))

fr = contents["fr"]
cred = (
    json.loads((CONTENT.parent / "credits.json").read_text(encoding="utf-8"))
    if (CONTENT.parent / "credits.json").exists()
    else {}
)
shared["audio_credit"] = cred.get("audio")
shared["credits"] = [
    [v["file"].replace("File:", ""), v["author"], v["license"], v["source"]] for k, v in cred.items()
]


# empreinte des fichiers CSS/JS : change à chaque modification, ce qui force les navigateurs à recharger
def digest(path):
    return hashlib.sha1((ROOT / path).read_bytes()).hexdigest()[:8]


assets = {"css": digest("css/style.css"), "js": digest("js/site.js")}


def deep_merge(base, over):
    out = dict(base)
    for k, v in over.items():
        out[k] = deep_merge(base[k], v) if isinstance(v, dict) and isinstance(base.get(k), dict) else v
    return out


def image_helpers(rel):
    """Fonctions mises à disposition des gabarits pour une langue donnée (rel = chemin vers la racine)."""

    def src(ident, width=None):
        """URL d'une photo : la plus grande par défaut, ou la version la plus proche de la largeur demandée."""
        files = images[ident]["files"]  # [[largeur, chemin dans img/], …] du plus grand au plus petit
        if width:
            files = sorted(files, key=lambda f: abs(f[0] - width))
        return f"{rel}img/{files[0][1]}"

    def url(ident, width=None):
        """Adresse absolue d'une photo (balises Open Graph, données structurées)."""
        return f"{SITE_URL}/img/{src(ident, width)[len(rel) + 4:]}"

    def pic(ident, alt, sizes="100vw", eager=False, cls="", data=None):
        """Balise <img> complète : srcset pour que le navigateur choisisse la taille, width/height
        pour réserver la place avant le chargement, chargement différé sauf si eager=True.
        `data` : attributs data-* supplémentaires ({'cap': 'Légende'} → data-cap="Légende")."""
        info = images[ident]
        attrs = [f'src="{src(ident)}"']
        if len(info["files"]) > 1:
            srcset = ", ".join(f"{rel}img/{path} {w}w" for w, path in info["files"])
            attrs += [f'srcset="{srcset}"', f'sizes="{sizes}"']
        attrs += [
            f'width="{info["w"]}"',
            f'height="{info["h"]}"',
            f'alt="{escape(alt)}"',
            'fetchpriority="high" decoding="sync"' if eager else 'loading="lazy" decoding="async"',
        ]
        if cls:
            attrs.append(f'class="{escape(cls)}"')
        if info.get("pos"):
            attrs.append(f'style="object-position:{escape(info["pos"])}"')
        for k, v in (data or {}).items():
            attrs.append(f'data-{k}="{escape(v)}"')
        return Markup("<img " + " ".join(attrs) + ">")

    return {"src": src, "url": url, "pic": pic}


def write(path, html):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


built = 0
for code, name, flag, prefix in LANGS:
    c = deep_merge(fr, contents.get(code, {}))  # repli sur le français si une clé manque
    outdir = ROOT / prefix if prefix else ROOT
    rel = "../" if prefix else ""  # chemin vers la racine (img, css, js)
    common = dict(
        lang=code,
        t=c,
        s=shared,
        rel=rel,
        prefix=prefix,
        langs=LANGS,
        assets=assets,
        site_url=SITE_URL,
        images=images,
        **image_helpers(rel),
    )
    for page in PAGES:
        tpl = env.get_template(f"{page}.html")
        html = tpl.render(
            page=page,
            canonical=f"{SITE_URL}/{prefix}{'' if page=='index' else page+'.html'}",
            fallback=(code != "fr" and code not in contents),
            **common,
        )
        write(outdir / f"{page}.html", html)
        built += 1
    for old, target in REDIRECTS.items():
        html = env.get_template("_redirect.html").render(target=target, **common)
        write(outdir / f"{old}.html", html)

# sitemap + robots
urls = []
for code, name, flag, prefix in LANGS:
    for page in PAGES:
        if page == "mentions-legales":
            continue
        urls.append(f"{SITE_URL}/{prefix}{'' if page=='index' else page+'.html'}")
sm = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]
sm += [f"  <url><loc>{u}</loc></url>" for u in urls]
sm.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
(ROOT / "robots.txt").write_text(
    f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8"
)
print(f"{built} pages générées ({len(contents)} langues traduites, repli FR pour les autres)")
