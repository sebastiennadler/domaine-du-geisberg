#!/usr/bin/env python3
"""Cherche sur Wikimedia Commons une photo libre (CC BY / CC BY-SA / domaine public) pour chaque sujet
listé dans SUJETS, la télécharge en 1600 px dans img/autour/ et note l'attribution dans tools/credits.json."""
import json, sys, urllib.request, urllib.parse, io
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
SUJETS = {
  "creutzwald-lac": ["Étang de Creutzwald", "Creutzwald lac", "Creutzwald plan d'eau", "Creutzwald"],
}
UA = "domaine-du-geisberg-site/1.0 (sebastien.nadler@gmail.com)"
OK_LIC = ("cc-by", "cc by", "cc0", "public domain", "pd-", "cc-zero")
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=40).read()
def api(**params):
    params.update(format="json"); return json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)))
credits = json.loads((ROOT / "tools/credits.json").read_text()) if (ROOT / "tools/credits.json").exists() else {}
for key, terms in SUJETS.items():
    found = None
    for term in terms:
        r = api(action="query", generator="search", gsrsearch=f"{term} filetype:bitmap", gsrnamespace=6, gsrlimit=20,
                prop="imageinfo", iiprop="url|extmetadata|size", iiurlwidth=1600)
        for p in (r.get("query", {}).get("pages", {}) or {}).values():
            ii = p.get("imageinfo", [{}])[0]; md = ii.get("extmetadata", {})
            lic = (md.get("LicenseShortName", {}).get("value", "") + " " + md.get("License", {}).get("value", "")).lower()
            if ii.get("width", 0) < 1000 or not any(k in lic for k in OK_LIC): continue
            found = (p["title"], ii.get("thumburl") or ii["url"], md.get("Artist", {}).get("value", ""), md.get("LicenseShortName", {}).get("value", ""), ii.get("descriptionurl", ""))
            break
        if found: break
    if not found:
        print(f"{key}: rien trouvé", file=sys.stderr); continue
    title, url, artist, lic, page = found
    im = Image.open(io.BytesIO(get(url))).convert("RGB")
    if im.width > 1600: im = im.resize((1600, int(im.height * 1600 / im.width)))
    out = ROOT / "img/autour" / f"{key}.webp"; im.save(out, "WEBP", quality=80, method=6)
    import re
    credits[key] = {"file": title, "author": re.sub(r"<[^>]+>", "", artist), "license": lic, "source": page}
    print(f"{key}: {title} ({lic})")
(ROOT / "tools/credits.json").write_text(json.dumps(credits, ensure_ascii=False, indent=1) + "\n")
