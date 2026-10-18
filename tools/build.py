#!/usr/bin/env python3
"""Génère le site statique : templates Jinja2 + contenu par langue (tools/content/*.json).

Usage : python3 tools/build.py
Sortie : pages FR à la racine, autres langues dans /en, /de, /es, /pt, /nl, /zh.
"""
import json, os, shutil, sys, hashlib
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

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
PAGES = ["index", "le-domaine", "gites", "gite-1", "gite-2", "autour", "avis", "visite", "reservation", "diaporama", "mentions-legales"]

env = Environment(loader=FileSystemLoader(str(TPL)), autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)

shared = json.loads((CONTENT / "shared.json").read_text(encoding="utf-8"))
busy = json.loads((CONTENT / "busy.json").read_text(encoding="utf-8")) if (CONTENT / "busy.json").exists() else {}
shared["busy1"] = ",".join(f"{a}/{b}" for a, b in busy.get("gite1", []))
shared["busy2"] = ",".join(f"{a}/{b}" for a, b in busy.get("gite2", []))
shared["busy_updated"] = busy.get("updated", "")
contents = {}
for code, *_ in LANGS:
    p = CONTENT / f"{code}.json"
    if p.exists():
        contents[code] = json.loads(p.read_text(encoding="utf-8"))

fr = contents["fr"]
# empreinte des fichiers CSS/JS : change à chaque modification, ce qui force les navigateurs à recharger
def digest(path):
    return hashlib.sha1((ROOT / path).read_bytes()).hexdigest()[:8]
assets = {"css": digest("css/style.css"), "js": digest("js/site.js")}

def deep_merge(base, over):
    out = dict(base)
    for k, v in over.items():
        out[k] = deep_merge(base[k], v) if isinstance(v, dict) and isinstance(base.get(k), dict) else v
    return out

built = 0
for code, name, flag, prefix in LANGS:
    c = deep_merge(fr, contents.get(code, {}))  # repli sur le français si une clé manque
    outdir = ROOT / prefix if prefix else ROOT
    outdir.mkdir(parents=True, exist_ok=True)
    rel = "../" if prefix else ""  # chemin vers la racine (img, css, js)
    for page in PAGES:
        tpl = env.get_template(f"{page}.html")
        html = tpl.render(
            lang=code, t=c, s=shared, page=page, rel=rel, prefix=prefix, langs=LANGS,
            assets=assets, site_url=SITE_URL, canonical=f"{SITE_URL}/{prefix}{'' if page=='index' else page+'.html'}",
            fallback=(code != "fr" and code not in contents),
        )
        (outdir / f"{page}.html").write_text(html, encoding="utf-8")
        built += 1

# sitemap + robots
urls = []
for code, name, flag, prefix in LANGS:
    for page in PAGES:
        if page == "mentions-legales":
            continue
        urls.append(f"{SITE_URL}/{prefix}{'' if page=='index' else page+'.html'}")
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += [f"  <url><loc>{u}</loc></url>" for u in urls]
sm.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
print(f"{built} pages générées ({len(contents)} langues traduites, repli FR pour les autres)")
