#!/usr/bin/env python3
"""Prépare les photos du site : lit les originaux dans photos-sources/, écrit des WebP
redimensionnés dans img/ et note leurs dimensions dans tools/content/images.json.

Usage : python3 tools/photos.py            (ne refait que ce qui a changé)
        python3 tools/photos.py --force    (refait tout)

Le catalogue est tools/photos.json : pour chaque photo, un identifiant (qui devient le
chemin dans img/), le fichier source, les largeurs à produire et, au besoin, "pos" : le point de
la photo à garder visible quand elle est recadrée (bandeau d'accueil), ex. "40% 70%". Les gabarits (templates)
affichent ensuite chaque photo avec `pic()` (voir tools/build.py), qui écrit un <img> avec
srcset et dimensions : le navigateur choisit la taille adaptée à l'écran et réserve la place
avant le chargement. Les métadonnées (EXIF, position GPS…) ne sont pas recopiées dans les WebP.

Les images à taille unique des dossiers STATIC_DIRS (photos libres récupérées par
tools/fetch_commons.py, logos) sont simplement mesurées et ajoutées au même catalogue.
"""

import json
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "photos-sources"
OUT = ROOT / "img"
CATALOG = ROOT / "tools" / "photos.json"
MANIFEST = ROOT / "tools" / "content" / "images.json"
STATIC_DIRS = ["autour", "logos"]

DEFAULT_WIDTHS = [1600, 800]
QUALITY = 80


def convert(entry, force):
    """Produit les WebP d'une entrée du catalogue ; renvoie sa fiche pour images.json."""
    src = SRC / entry["src"]
    if not src.exists():
        print(f"  ! source manquante : {src.relative_to(ROOT)}", file=sys.stderr)
        return None
    widths = entry.get("widths", DEFAULT_WIDTHS)
    target_dir = OUT / Path(entry["id"]).parent
    target_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(entry["id"]).name
    outputs = [target_dir / f"{stem}-{w}.webp" for w in widths]
    up_to_date = all(o.exists() and o.stat().st_mtime >= src.stat().st_mtime for o in outputs)

    if force or not up_to_date:
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        crop = entry.get("crop")  # [gauche, haut, droite, bas] en fraction de l'image
        if crop:
            w, h = im.size
            im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
        for w, out in zip(widths, outputs):
            scaled = im.copy()
            if scaled.width > w:
                scaled.thumbnail((w, w * 10), Image.LANCZOS)
            scaled.save(out, "WEBP", quality=entry.get("quality", QUALITY), method=6)
        print(f"  {entry['id']}  ←  {entry['src']}  ({', '.join(str(w) for w in widths)})")

    files = []
    for out in outputs:
        with Image.open(out) as im:
            files.append([im.width, str(out.relative_to(OUT))])
    info = {"w": files[0][0], "h": _height(outputs[0]), "files": files}
    if entry.get("pos"):  # point d'intérêt pour les cadrages serrés (object-position), ex. "40% 70%"
        info["pos"] = entry["pos"]
    return info


def _height(path):
    with Image.open(path) as im:
        return im.height


def static_entries():
    """Images à taille unique (une seule largeur, le fichier tel quel)."""
    out = {}
    for d in STATIC_DIRS:
        for f in sorted((OUT / d).glob("*.webp")):
            with Image.open(f) as im:
                out[f"{d}/{f.stem}"] = {"w": im.width, "h": im.height, "files": [[im.width, str(f.relative_to(OUT))]]}
    return out


def main():
    force = "--force" in sys.argv
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    manifest = {}
    for entry in catalog:
        info = convert(entry, force)
        if info:
            manifest[entry["id"]] = info
    manifest.update(static_entries())
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"{len(manifest)} images cataloguées → {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
