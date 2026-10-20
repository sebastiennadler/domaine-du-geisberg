#!/usr/bin/env python3
"""Prépare les vidéos du site : lit les originaux (.MOV) dans assets/videos-sources/, écrit des MP4
légers dans assets/videos/ et une image d'affiche (poster) dans assets/photos-sources/, que tools/photos.py
transforme ensuite en WebP.

Usage : python3 tools/videos.py            (ne refait que ce qui a changé)
        python3 tools/videos.py --force    (refait tout)

Le catalogue est src/catalog/videos.json : identifiant, fichier source, hauteur maximale et instant
de l'affiche. Nécessite ffmpeg (brew install ffmpeg).

Réglages choisis pour un site statique sans serveur vidéo :
- H.264 (profil high), AAC 96 kb/s : lu partout, y compris sur iPhone et vieux navigateurs ;
- CRF 26 : bonne qualité pour un poids réduit (≈ 1 Mo pour 10 s en 720p) ;
- `faststart` : les métadonnées sont en tête du fichier, la lecture démarre sans tout télécharger.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "videos-sources"
OUT = ROOT / "assets" / "videos"
POSTERS = ROOT / "assets" / "photos-sources"
CATALOG = ROOT / "src" / "catalog" / "videos.json"


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def newer(out, src):
    return out.exists() and out.stat().st_mtime >= src.stat().st_mtime


def main():
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg est introuvable : brew install ffmpeg")
    force = "--force" in sys.argv
    OUT.mkdir(exist_ok=True)
    for v in json.loads(CATALOG.read_text(encoding="utf-8")):
        src = SRC / v["src"]
        if not src.exists():
            print(f"  ! source manquante : {src.relative_to(ROOT)}", file=sys.stderr)
            continue
        mp4 = OUT / f"{v['id']}.mp4"
        poster = POSTERS / f"video-{v['id']}.jpg"
        height = v.get("height", 720)
        if force or not newer(mp4, src):
            # -2 : largeur paire calculée automatiquement ; on ne grossit jamais une vidéo
            scale = f"scale=-2:'min({height},ih)'"
            maxrate = v.get("maxrate_kbps", 2500)  # plafond de débit : évite les fichiers énormes sur les plans agités
            audio = v.get("audio_kbps", 96)
            run([
                "ffmpeg", "-y", "-i", str(src),
                "-vf", scale,
                "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", str(v.get("crf", 26)),
                "-maxrate", f"{maxrate}k", "-bufsize", f"{2 * maxrate}k",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                "-c:a", "aac", "-b:a", f"{audio}k", "-ac", "2" if audio >= 64 else "1",
                str(mp4),
            ])
            print(f"  videos/{mp4.name}  ←  {v['src']}  ({mp4.stat().st_size // 1024} Ko)")
        if force or not newer(poster, src):
            run(["ffmpeg", "-y", "-ss", str(v.get("poster_at", 1)), "-i", str(src), "-frames:v", "1", "-q:v", "2", str(poster)])
            print(f"  affiche : photos-sources/{poster.name}")
    print("vidéos prêtes → lancez ensuite python3 tools/photos.py pour les affiches")


if __name__ == "__main__":
    main()
