#!/usr/bin/env python3
"""Génère le site statique dans dist/ : gabarits Jinja2 (src/templates) + contenu par langue
(src/content/*.json) + fichiers statiques (src/css, src/js, assets/img, assets/videos, assets/audio).

Usage : python3 tools/build.py            site de travail (avec le mode « Notes pour Marc »)
        python3 tools/build.py --prod     version à livrer (sans les notes)

Sortie : dist/ — pages FR à la racine, autres langues dans /en, /de, /es, /pt, /nl, /zh, plus
sitemap.xml, robots.txt et .nojekyll. Le dossier dist/ est recréé à chaque exécution et n'est pas suivi
par git : c'est ce que GitHub Pages publie et ce que tools/package.py livre à l'hébergeur.

Les photos sont décrites dans src/content/images.json (produit par tools/photos.py) ; les gabarits les
affichent avec la fonction `pic()` définie plus bas, qui écrit un <img> complet (srcset, dimensions,
chargement différé).
"""

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from markupsafe import Markup, escape

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
TPL = SRC / "templates"
CONTENT = SRC / "content"
CATALOG = SRC / "catalog"
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"
SITE_URL = "https://www.domainedugeisberg.fr"

# dossiers copiés tels quels dans dist/ : (source, nom dans dist/)
STATIC = [(SRC / "css", "css"), (SRC / "js", "js"), (ASSETS / "img", "img"),
          (ASSETS / "videos", "videos"), (ASSETS / "audio", "audio")]

LANGS = [  # ordre demandé : FR, EN, DE, ES, PT, NL, ZH
    ("fr", "Français", "🇫🇷", ""),
    ("en", "English", "🇬🇧", "en/"),
    ("de", "Deutsch", "🇩🇪", "de/"),
    ("es", "Español", "🇪🇸", "es/"),
    ("pt", "Português", "🇵🇹", "pt/"),
    ("nl", "Nederlands", "🇳🇱", "nl/"),
    ("zh", "中文", "🇨🇳", "zh/"),
]
PAGES = ["index", "reservation", "le-domaine", "medias", "avis", "mentions-legales"]
# anciennes adresses conservées : chacune renvoie vers la page (et l'ancre) qui la remplace, avec le libellé du menu
REDIRECTS = {
    "gites": ("index.html#gites", "gites"),
    "gite-1": ("index.html#gites", "gites"),
    "gite-2": ("index.html#gites", "gites"),
    "autour": ("le-domaine.html#alentours", "alentours"),
    "diaporama": ("medias.html#diaporama", "diaporama"),
    "videos": ("medias.html#videos", "videos"),
    "visite": ("medias.html#visite", "visite"),
}
TODO = ROOT / "TODO.md"


def marc_notes_from_todo():
    """Lit TODO.md et renvoie {clé: texte} pour le mode « Notes pour Marc ».

    Dans les sections « À demander à Marc » et « À faire par Marc dans Nuitrésa », une ligne
    `- [ ] {clé} texte` accroche la question à l'élément de page portant note('clé') dans les gabarits
    (ex. {facts} = chiffres clés de l'accueil, {widget} = formulaire). Une ligne sans clé va dans la
    vue d'ensemble de l'accueil ({todo}). Plusieurs lignes pour une même clé sont numérotées."""
    import re

    if not TODO.exists():
        return {}
    notes, section = {}, None
    for line in TODO.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:]
            continue
        if not section or not (section.startswith("4.") or section.startswith("5.")):
            continue
        m = re.match(r"^- \[ \] (?:\{(\w+)\} )?(.+)$", line.strip())
        if not m:
            continue
        key = m.group(1) or ("widget" if section.startswith("5.") else "todo")
        notes.setdefault(key, []).append(m.group(2).strip())
    out = {}
    for key, items in notes.items():
        head = "Nuitrésa — à faire par Marc :" if key == "widget" else ("Vue d'ensemble — ce qu'il reste à faire :" if key == "todo" else None)
        body = "\n".join(f"{i}. {x}" for i, x in enumerate(items, 1)) if len(items) > 1 else items[0]
        out[key] = (head + "\n" + body) if head else body
    return out


def main():
    args = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    args.add_argument("--prod", action="store_true", help="version à livrer : sans le mode « Notes pour Marc »")
    opts = args.parse_args()

    env = Environment(
        loader=FileSystemLoader(str(TPL)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined,  # une clé absente des textes = erreur, pas un trou dans la page
    )

    shared = json.loads((CONTENT / "shared.json").read_text(encoding="utf-8"))
    images = json.loads((CONTENT / "images.json").read_text(encoding="utf-8"))
    contents = {}
    for code, *_ in LANGS:
        p = CONTENT / f"{code}.json"
        if p.exists():
            contents[code] = json.loads(p.read_text(encoding="utf-8"))
    fr = contents["fr"]
    marc_notes = marc_notes_from_todo() if not opts.prod else {}

    cred_file = CATALOG / "credits.json"
    cred = json.loads(cred_file.read_text(encoding="utf-8")) if cred_file.exists() else {}
    shared["audio_credit"] = cred.get("audio")
    shared["credits"] = [
        [v["file"].replace("File:", ""), v["author"], v["license"], v["source"]] for k, v in cred.items()
    ]

    # dist/ repart de zéro, puis reçoit les fichiers statiques
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    for source, name in STATIC:
        if source.exists():
            shutil.copytree(source, DIST / name)
    (DIST / ".nojekyll").write_text("", encoding="utf-8")

    # empreinte des fichiers CSS/JS : change à chaque modification, ce qui force les navigateurs à recharger
    def digest(path):
        return hashlib.sha1(path.read_bytes()).hexdigest()[:8]

    assets = {"css": digest(SRC / "css" / "style.css"), "js": digest(SRC / "js" / "site.js")}

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
        outdir = DIST / prefix if prefix else DIST
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
            notes=(code == "fr" and not opts.prod),  # mode « Notes pour Marc » : FR, site de travail seulement
            marc_notes=marc_notes,
            nr_lang={"fr": "FR", "en": "EN", "de": "DE", "es": "ES"}.get(code, "EN"),  # langues des cadres Nuitrésa
            **image_helpers(rel),
        )
        for page in PAGES:
            tpl = env.get_template(f"pages/{page}.html")
            html = tpl.render(
                page=page,
                canonical=f"{SITE_URL}/{prefix}{'' if page=='index' else page+'.html'}",
                fallback=(code != "fr" and code not in contents),
                **common,
            )
            write(outdir / f"{page}.html", html)
            built += 1
        for old, (target, label_key) in REDIRECTS.items():
            html = env.get_template("partials/_redirect.html").render(target=target, label=c["nav"][label_key], **common)
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
    (DIST / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8"
    )
    mode = "version à livrer (sans notes)" if opts.prod else "site de travail (avec notes)"
    print(f"{built} pages générées dans dist/ — {mode} ({len(contents)} langues traduites, repli FR pour les autres)")


if __name__ == "__main__":
    main()
