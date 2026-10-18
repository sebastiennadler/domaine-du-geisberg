#!/usr/bin/env python3
"""Lit les calendriers iCal (Airbnb, Bed Booking, Gîtes de France…) et écrit tools/content/busy.json.

Les adresses des flux sont lues dans les variables d'environnement ICAL_GITE1 et ICAL_GITE2
(plusieurs adresses possibles, séparées par des virgules). Elles ne sont jamais écrites dans le dépôt.
Seules les plages de dates occupées sont conservées : aucun nom, aucun lien, aucune plateforme.
"""
import json, os, re, sys, urllib.request, datetime as dt
from pathlib import Path

OUT = Path(__file__).resolve().parent / "content" / "busy.json"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "domaine-du-geisberg-calendar/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

def parse(ics):
    """Retourne une liste de (début, fin exclusive) au format AAAA-MM-JJ."""
    ranges = []
    for ev in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", ics.replace("\r\n ", "").replace("\r\n", "\n").replace("\n ", ""), re.S):
        ds = re.search(r"DTSTART[^:]*:(\d{8})", ev); de = re.search(r"DTEND[^:]*:(\d{8})", ev)
        if not ds: continue
        start = dt.date(int(ds.group(1)[:4]), int(ds.group(1)[4:6]), int(ds.group(1)[6:]))
        end = dt.date(int(de.group(1)[:4]), int(de.group(1)[4:6]), int(de.group(1)[6:])) if de else start + dt.timedelta(days=1)
        if end <= start: end = start + dt.timedelta(days=1)
        ranges.append((start, end))
    return ranges

def merge(ranges):
    ranges = sorted(ranges); out = []
    for s, e in ranges:
        if out and s <= out[-1][1]: out[-1] = (out[-1][0], max(out[-1][1], e))
        else: out.append((s, e))
    return out

def main():
    today = dt.date.today(); horizon = today + dt.timedelta(days=540)
    result = {"updated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")}
    ok = False
    for key in ("gite1", "gite2"):
        urls = [u.strip() for u in os.environ.get("ICAL_" + key.upper(), "").split(",") if u.strip()]
        ranges = []
        for u in urls:
            try:
                ranges += parse(fetch(u)); ok = True
            except Exception as e:
                print(f"{key}: flux illisible ({e.__class__.__name__})", file=sys.stderr)
        ranges = [(max(s, today - dt.timedelta(days=31)), min(e, horizon)) for s, e in ranges if e > today - dt.timedelta(days=31) and s < horizon]
        result[key] = [[s.isoformat(), e.isoformat()] for s, e in merge(ranges)]
    if not ok:
        print("Aucun flux lu : busy.json inchangé.", file=sys.stderr); return 0
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"gîte 1 : {len(result['gite1'])} périodes · gîte 2 : {len(result['gite2'])} périodes")

if __name__ == "__main__":
    sys.exit(main() or 0)
