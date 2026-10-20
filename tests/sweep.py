"""Balayage des débordements : pour chaque page et chaque largeur, repère
- un défilement horizontal de la page (contenu plus large que l'écran) ;
- un élément de texte dont le contenu dépasse sa boîte (scrollWidth > clientWidth) ;
- un enfant de grille / flex qui déborde de son parent (chevauchement du voisin)."""
import asyncio, re, json, sys
from playwright.async_api import async_playwright

BASE = 'http://127.0.0.1:8111'  # serveur local sur dist/ (voir tests/run.sh)
PAGES = ['index', 'reservation', 'le-domaine', 'medias', 'avis', 'mentions-legales']
DIRS = ['', 'en/', 'de/', 'es/', 'pt/', 'nl/', 'zh/']
WIDTHS = [320, 360, 390, 430, 600, 768, 834, 1024, 1140, 1366]

JS = r"""
(() => {
  const out = [];
  const vw = document.documentElement.clientWidth;
  if (document.documentElement.scrollWidth > vw + 1) out.push(['page', 'défilement horizontal', document.documentElement.scrollWidth - vw]);
  const skip = (el) => el.closest('.nav, .lb, .npanel, .ntip, .langdd .langs, .brand-txt, .visually-hidden, .diapo-overlay[hidden], details:not([open]) > :not(summary)');
  const sel = 'a, span, b, small, p, li, h1, h2, h3, cite, label, button, summary, dt, dd, figcaption, blockquote';
  for (const el of document.querySelectorAll(sel)) {
    if (skip(el)) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.position === 'fixed') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const txt = (el.innerText || '').trim().slice(0, 50);
    if (!txt) continue;
    // 1. texte plus large que sa boîte (hors boîtes qui défilent volontairement)
    if (cs.overflowX === 'visible' && el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 0) {
      out.push(['déborde de sa boîte', txt, el.scrollWidth - el.clientWidth, el.tagName + '.' + el.className]);
    }
    // 2. dépasse l'écran
    if (r.right > vw + 1) out.push(['dépasse l\'écran', txt, Math.round(r.right - vw), el.tagName + '.' + el.className]);
    // 3. enfant direct d'une grille/flex qui dépasse son parent (chevauchement)
    const p = el.parentElement;
    if (p) {
      const pcs = getComputedStyle(p);
      if ((pcs.display === 'grid' || pcs.display === 'flex') && pcs.overflowX === 'visible') {
        const pr = p.getBoundingClientRect();
        if (r.right > pr.right + 2) out.push(['dépasse sa colonne', txt, Math.round(r.right - pr.right), el.tagName + '.' + el.className]);
      }
    }
  }
  return out;
})()
"""

async def main():
    issues = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in WIDTHS:
            ctx = await b.new_context(viewport={'width': w, 'height': 900})
            page = await ctx.new_page()
            page.set_default_timeout(15000)
            async def block(route): await route.abort()
            await page.route(re.compile(r'^(?!http://127\.0\.0\.1).*'), block)
            for d in DIRS:
                for pg in PAGES:
                    await page.goto(f'{BASE}/{d}{pg}.html', wait_until='domcontentloaded')
                    await page.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
                    if w < 1040:  # ouvrir le tiroir mobile pour vérifier aussi son contenu
                        pass
                    found = await page.evaluate(JS)
                    for f in found:
                        key = (f[0], f[1], f[3] if len(f) > 3 else '')
                        issues.setdefault(key, []).append(f'{d}{pg}@{w}')
            await ctx.close()
        await b.close()
    if not issues:
        print('Aucun débordement détecté.')
    for (kind, txt, where), pages in sorted(issues.items(), key=lambda x: -len(x[1])):
        print(f'{kind:22} | {txt[:45]:45} | {where[:40]:40} | {len(pages)} cas, ex. {pages[0]}, {pages[-1]}')
    return len(issues)

sys.exit(1 if asyncio.run(main()) else 0)
