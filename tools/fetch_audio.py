#!/usr/bin/env python3
"""Cherche sur Wikimedia Commons un enregistrement libre (CC0 / domaine public / CC BY) de chants d'oiseaux,
le convertit en MP3 (audio/chants-oiseaux.mp3, 1 à 6 minutes) et note l'attribution dans tools/credits.json."""
import json, re, subprocess, sys, urllib.request, urllib.parse, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
UA = "domaine-du-geisberg-site/1.0 (sebastien.nadler@gmail.com)"
OK_LIC = ("cc0", "public domain", "pd-", "cc-zero", "cc by 4", "cc by 3", "cc by 2", "cc-by-4", "cc-by-3", "cc-by-sa")
QUERIES = ["dawn chorus birdsong", "Vogelgesang Morgen", "birdsong forest spring", "chant d'oiseaux forêt", "blackbird song", "Amsel Gesang", "nightingale song", "Vogelstimmen Wald"]
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
def api(**p):
    p.update(format="json"); return json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)))
credits = json.loads((ROOT / "tools/credits.json").read_text())
if "audio" in credits: print("déjà présent"); sys.exit(0)
seen = set()
for q in QUERIES:
    r = api(action="query", generator="search", gsrsearch=f"{q} filetype:audio", gsrnamespace=6, gsrlimit=30, prop="imageinfo", iiprop="url|extmetadata|size|mime")
    for p in (r.get("query", {}).get("pages", {}) or {}).values():
        t = p["title"]
        if t in seen: continue
        seen.add(t)
        ii = p.get("imageinfo", [{}])[0]; md = ii.get("extmetadata", {})
        lic = (md.get("LicenseShortName", {}).get("value", "") + " " + md.get("License", {}).get("value", "")).lower()
        if not any(k in lic for k in OK_LIC): continue
        if ii.get("size", 0) > 60_000_000 or ii.get("size", 0) < 300_000: continue
        try:
            with tempfile.TemporaryDirectory() as d:
                src = Path(d) / ("in" + Path(t).suffix.lower()); src.write_bytes(get(ii["url"]))
                dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)]).decode().strip())
                if not (55 <= dur <= 400): print(f"{t}: durée {dur:.0f}s, écartée"); continue
                out = ROOT / "audio" / "chants-oiseaux.mp3"; out.parent.mkdir(exist_ok=True)
                subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-t", "300", "-af", "afade=t=in:d=2,afade=t=out:st=298:d=2,loudnorm=I=-20", "-codec:a", "libmp3lame", "-b:a", "96k", "-ac", "2", str(out)])
        except Exception as e:
            print(f"{t}: {e.__class__.__name__}", file=sys.stderr); continue
        credits["audio"] = {"file": t, "author": re.sub(r"<[^>]+>", "", md.get("Artist", {}).get("value", "")), "license": md.get("LicenseShortName", {}).get("value", ""), "source": ii.get("descriptionurl", ""), "seconds": round(min(dur, 300))}
        (ROOT / "tools/credits.json").write_text(json.dumps(credits, ensure_ascii=False, indent=1) + "\n")
        print(f"OK {t} ({lic}, {dur:.0f}s)"); sys.exit(0)
print("rien trouvé", file=sys.stderr); sys.exit(1)
