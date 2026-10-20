"""Tests fonctionnels du site généré dans dist/ (servi sur 127.0.0.1:8111, voir tests/run.sh).
Réseau externe coupé : les cadres Nuitrésa, les polices et la visite 360° ne sont pas chargés."""
import asyncio, json, re, sys
from pathlib import Path
from playwright.async_api import async_playwright

BASE = 'http://127.0.0.1:8111/domaine-du-geisberg'  # serveur local sur dist/, sous le même préfixe que GitHub Pages (voir tests/run.sh)
ROOT = Path(__file__).resolve().parent.parent
PAGES = ['index', 'reservation', 'le-domaine', 'medias', 'avis', 'mentions-legales', 'questions']
LANDING = ['gite-accessible-pmr-moselle', 'gite-lac-de-creutzwald', 'gites-saint-avold-sarrebruck']  # fr, en, de seulement
LANDING_DIRS = ['', 'en/', 'de/']
MENU = ['index', 'reservation', 'le-domaine', 'medias', 'avis']
DIRS = ['', 'en/', 'de/', 'es/', 'pt/', 'nl/', 'zh/']
NRL = {'': 'FR', 'en/': 'EN', 'de/': 'DE', 'es/': 'ES', 'pt/': 'EN', 'nl/': 'EN', 'zh/': 'EN'}
KEY = 'e8dc8870f783d664870e89ac71801620'
REDIRECTS = {'gites': 'index.html#gites', 'gite-1': 'index.html#gites', 'gite-2': 'index.html#gites', 'autour': 'le-domaine.html#alentours',
             'diaporama': 'medias.html#diaporama', 'videos': 'medias.html#videos', 'visite': 'medias.html#visite'}
results = []


def ok(name, cond, detail=''):
    results.append((name, bool(cond), detail)); print(("ok " if cond else "KO ") + name, flush=True)


def walk(o, p=''):
    """Toutes les feuilles (clé → valeur texte) d'un JSON de contenu."""
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, f'{p}/{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f'{p}[{i}]')
    elif isinstance(o, str):
        yield p, o


# --- contrôles sur les fichiers de contenu (sans navigateur) ---
def content_checks():
    fr = json.loads((ROOT / 'src/content/fr.json').read_text(encoding='utf-8'))
    fr_leaves = dict(walk(fr))
    for code in ['en', 'de', 'es', 'pt', 'nl', 'zh']:
        d = json.loads((ROOT / f'src/content/{code}.json').read_text(encoding='utf-8'))
        leaves = dict(walk(d))
        # les pages de fond (landing + leur meta) n'existent qu'en fr/en/de ; les identifiants de photos ne se traduisent pas
        missing = [k for k in fr_leaves if k not in leaves and (code in ('en', 'de') or not (k.startswith('/landing/') or k.startswith('/meta/gite')))]
        ok(f'{code} : aucune clé manquante (sinon repli sur le français)', not missing, ', '.join(missing[:5]))
        # une valeur identique au français est suspecte, sauf noms propres, chiffres, adresses, codes
        same = [k for k, v in leaves.items() if k in fr_leaves and v == fr_leaves[k] and len(v) > 14
                and not re.match(r'^[\d\s€%×,.:–\-h]+$', v) and not any(w in v for w in ['Varsberg', 'Geisberg', 'Nuitr', 'Gîtes de France', 'Clévacances', 'Tourisme & Handicap', 'Urielle', 'Agnès', 'Marc', 'Vogelsgesang', 'Airbnb', 'Abritel', 'http', '@', 'SIRET', 'TVA', 'Saint-Avold', 'Creutzwald', 'Nadler', 'Saarschleife', 'Playfair'])]
        same = [k for k in same if not k.startswith('/legal') and not k.startswith('/domaine/sites') and '/links' not in k and not k.endswith(('/photo', '/photo2'))]
        ok(f'{code} : pas de texte resté en français', len(same) <= 2, ', '.join(same[:6]))
    todo = (ROOT / 'TODO.md').read_text(encoding='utf-8')
    ok('TODO.md : section « À demander à Marc » avec des clés de page', '## 4. À demander à Marc' in todo and len(re.findall(r'^- \[ \] \{\w+\} ', todo, re.M)) >= 10)
    for code in ['fr', 'en', 'de', 'es', 'pt', 'nl', 'zh']:
        txt = (ROOT / f'src/content/{code}.json').read_text(encoding='utf-8')
        ok(f'{code} : ni surfaces par pièce, ni vitrocéramique, ni équitation sur place', 'm² ·' not in txt and 'itrocéram' not in txt and 'Vitrokeram' not in txt and '"equitation"' not in txt)


async def main():
    content_checks()
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 1280, 'height': 800})
        page = await ctx.new_page()
        page.set_default_timeout(15000)
        async def block(route):
            await route.abort()
        await page.route(re.compile(r'^(?!http://127\.0\.0\.1).*'), block)
        js_errors = []
        page.on('pageerror', lambda e: js_errors.append(str(e)))
        page.on('console', lambda m: js_errors.append(m.text) if m.type == 'error' and 'Failed to load' not in m.text else None)

        # 1. toutes les pages de toutes les langues : chargement, H1, menu à 5 entrées, logo, sans erreur JS
        for d in DIRS:
            for pg in PAGES + (LANDING if d in LANDING_DIRS else []):
                r = await page.goto(f'{BASE}/{d}{pg}.html', wait_until='domcontentloaded')
                ok(f'{d}{pg}: HTTP 200', r.status == 200)
                h1 = await page.locator('h1').count()
                ok(f'{d}{pg}: un H1', h1 == 1, f'{h1} h1')
                nav = await page.evaluate("[...document.querySelectorAll('nav.nav > a:not(.book)')].map(a=>a.getAttribute('href'))")
                ok(f'{d}{pg}: menu 5 entrées', nav == [m + '.html' for m in MENU], json.dumps(nav))
                ok(f'{d}{pg}: bouton Réserver du menu', await page.get_attribute('nav.nav > a.book', 'href') == 'reservation.html#demande')
                if pg in MENU:
                    cur = await page.locator('nav.nav > a[aria-current="page"]').count()
                    ok(f'{d}{pg}: entrée de menu active', cur == 1, f'{cur}')
                lang = await page.get_attribute('html', 'lang')
                ok(f'{d}{pg}: attribut lang', lang == (d.strip('/') or 'fr'), lang)
                logos = await page.evaluate("[...document.querySelectorAll('.brand img.logo')].map(i=>getComputedStyle(i).display)")
                ok(f'{d}{pg}: logo clair affiché, sombre masqué', logos == ['block', 'none'], json.dumps(logos))
                ok(f'{d}{pg}: favicon et icône Apple', await page.locator('link[rel="icon"][href$="favicon.png"]').count() == 1 and await page.locator('link[rel="apple-touch-icon"]').count() == 1)
                nalt = 4 if pg in LANDING else 8
                ok(f'{d}{pg}: canonical + hreflang ({nalt - 1} langues + x-default)', await page.locator('link[rel="canonical"]').count() == 1 and await page.locator('link[rel="alternate"][hreflang]').count() == nalt)
                # sécurité : politique CSP, aucun script en ligne, polices et scripts locaux seulement
                csp = await page.get_attribute('meta[http-equiv="Content-Security-Policy"]', 'content')
                ok(f'{d}{pg}: politique CSP', csp is not None and "script-src 'self' https://public.nuit-resa.com" in csp and "object-src 'none'" in csp)
                inline = await page.evaluate("[...document.scripts].filter(s=>!s.src && !['application/ld+json','application/json'].includes(s.type)).length")
                ok(f'{d}{pg}: aucun script en ligne', inline == 0, str(inline))
                ext = await page.evaluate("[...document.querySelectorAll('script[src], link[rel=stylesheet][href], link[rel=preconnect]')].map(e=>e.src||e.href).filter(u=>!u.startsWith(location.origin) && !u.startsWith('https://public.nuit-resa.com'))")
                ok(f'{d}{pg}: ni police ni script externe (hors Nuitrésa)', not ext, json.dumps(ext))
                ok(f'{d}{pg}: theme.js chargé avant la feuille de style', await page.locator('head script[src*="js/theme.js"] + link[rel=stylesheet]').count() == 1)
                # référencement : titre et description de longueur raisonnable
                title = await page.title()
                desc = await page.get_attribute('meta[name=description]', 'content')
                ok(f'{d}{pg}: titre ≤ 70 et description ≤ 160 caractères', len(title) <= 70 and len(desc) <= 160, f'{len(title)} / {len(desc)}')
        ok('aucune erreur JavaScript sur toutes les pages', not js_errors, '; '.join(js_errors[:3]))

        # 1b. polices auto-hébergées : chargées depuis le site (réseau externe coupé, elles doivent quand même être disponibles)
        await page.goto(f'{BASE}/index.html', wait_until='load')
        await page.evaluate('document.fonts.ready')
        fonts = await page.evaluate("[document.fonts.check(\"700 20px 'Playfair Display'\"), document.fonts.check(\"400 16px 'Nunito Sans'\"), document.fonts.check(\"800 16px 'Nunito Sans'\")]")
        ok('polices Playfair Display et Nunito Sans servies par le site', all(fonts), json.dumps(fonts))
        h1font = await page.evaluate("getComputedStyle(document.querySelector('h1')).fontFamily")
        ok('H1 en Playfair Display', 'Playfair' in h1font, h1font)

        # 2. renvois des anciennes adresses, dans deux langues
        for d in ['', 'de/']:
            for old, target in REDIRECTS.items():
                await page.goto(f'{BASE}/{d}{old}.html', wait_until='domcontentloaded')
                await page.wait_for_timeout(400)
                ok(f'{d}{old}.html renvoie vers {target}', page.url.endswith(f'/{d}{target}'), page.url)

        # 3. accueil : bandeau (durées, mouvement), points, thème, logo sombre, galerie, tiroir, avis unique, aperçus
        await page.goto(f'{BASE}/index.html', wait_until='load')
        ok('bandeau : 4 diapositives', await page.locator('.hero .slide').count() == 4)
        ok('bandeau : la photo des hôtes en premier, fixe, 4 s', await page.evaluate("(()=>{const s=document.querySelector('.hero .slide');return s.classList.contains('on')&&s.getAttribute('data-dur')==='4000'&&s.getAttribute('data-move')==='none'&&s.querySelector('img').alt.includes('Urielle')})()"))
        ok('bandeau : première photo sans animation', await page.evaluate("getComputedStyle(document.querySelector('.hero .slide.on img')).animationName") == 'none')
        ok('bandeau : interrupteurs inclinaison / parallaxe présents', await page.get_attribute('#hero', 'data-tilt') in ('on', 'off') and await page.get_attribute('#hero', 'data-parallax') in ('on', 'off'))
        await page.click('.hero .dots button:nth-child(2)')
        await page.wait_for_timeout(200)
        ok('bandeau : clic sur un point change la diapositive', 'on' in (await page.get_attribute('.hero .slide:nth-child(2)', 'class')))
        ok('bandeau : les photos suivantes partent de loin et zooment (animation)', (await page.evaluate("getComputedStyle(document.querySelector('.hero .slide.on img')).animationName")).startswith('kb-'))
        ok('bandeau : plus de photo de nuit (mur sali)', await page.evaluate("[...document.querySelectorAll('.hero img')].every(i=>!i.src.includes('neige'))"))
        await page.mouse.move(300, 300)
        await page.wait_for_timeout(400)
        tr = await page.evaluate("document.querySelector('.hero .layer').style.transform")
        fine = await page.evaluate("matchMedia('(hover: hover) and (pointer: fine)').matches")
        ok('bandeau : inclinaison à la souris (quand hero_tilt est activé et qu\'il y a une souris)', ('rotate' in tr) == (fine and await page.get_attribute('#hero', 'data-tilt') == 'on'), f'{tr[:60]} pointeur fin={fine}')
        await page.click('#theme')
        ok('bouton thème → sombre', await page.get_attribute('html', 'data-theme') == 'dark')
        logos = await page.evaluate("[...document.querySelectorAll('.brand img.logo')].map(i=>getComputedStyle(i).display)")
        ok('thème sombre : logo sombre affiché, clair masqué', logos == ['none', 'block'], json.dumps(logos))
        await page.click('#theme')
        ok('bouton thème → clair', await page.get_attribute('html', 'data-theme') == 'light')
        facts = await page.evaluate("[...document.querySelectorAll('.chips.facts li')].map(l=>l.textContent)")
        ok('chiffres clés : de 1 à 4 personnes, jamais 5', any('1 à 4' in f for f in facts) and not any('5' in f for f in facts), json.dumps(facts))
        ok('galerie des gîtes : 8 photos, dont la chambre à deux lits', await page.locator('#gites .gallery a').count() == 8 and await page.locator('#gites .gallery img[src*="deux-lits"]').count() == 1)
        await page.click('#gites .gallery a:first-child')
        await page.wait_for_timeout(300)
        ok('visionneuse : s\'ouvre au clic sur la galerie', await page.is_visible('.lb.open'))
        src1 = await page.get_attribute('.lb img', 'src')
        await page.keyboard.press('ArrowRight')
        src2 = await page.get_attribute('.lb img', 'src')
        ok('visionneuse : flèche droite = photo suivante', src1 != src2)
        await page.keyboard.press('Escape')
        ok('visionneuse : Échap ferme', not await page.is_visible('.lb.open'))
        fiche = await page.evaluate("[...document.querySelectorAll('.fiche dt')].map(d=>d.textContent)")
        ok('fiche : 9 lignes, sans surfaces par pièce', len(fiche) == 9 and not any('Pièce' in f for f in fiche), json.dumps(fiche))
        ok('fiche : induction, Wi-Fi fibre, couchage d\'appoint discret', await page.evaluate("(()=>{const t=document.querySelector('.fiche').textContent;return t.includes('induction')&&t.includes('Wi-Fi fibre')&&t.includes('appoint')})()"))
        ok('tiroir équipement fermé par défaut', not await page.evaluate("document.querySelector('.drawer').open"))
        await page.click('.drawer summary')
        ok('tiroir équipement : s\'ouvre, 5 groupes', await page.evaluate("document.querySelector('.drawer').open") and await page.locator('.drawer-in h4').count() == 5)
        ok('un seul avis sur l\'accueil + lien vers tous les avis', await page.locator('#avis blockquote').count() == 1 and await page.get_attribute('#avis a.more', 'href') == 'avis.html')
        ok('pas de calendrier Nuitrésa sur l\'accueil', await page.locator('iframe.nr-cal').count() == 0)
        ok('pas de tableau des tarifs sur l\'accueil (un seul chez-soi : Réservation)', await page.locator('.prices').count() == 0)
        ok('aperçus : domaine & alentours, En images', await page.evaluate("[...document.querySelectorAll('.teaser')].map(a=>a.getAttribute('href'))") == ['le-domaine.html', 'medias.html'])
        ok('bouton remonter présent', await page.locator('.totop').count() == 1)
        # diaporama en superposition
        ok('diaporama : photos non chargées avant le clic', await page.evaluate("[...document.querySelectorAll('#home-diapo img')].every(i=>!i.getAttribute('src'))"))
        await page.click('#open-diapo')
        await page.wait_for_timeout(500)
        ok('diaporama : s\'ouvre en superposition, photos chargées', await page.evaluate("!document.getElementById('home-diapo').hidden && [...document.querySelectorAll('#home-diapo img')].every(i=>i.src)"))
        ok('diaporama : légende et compteur', await page.evaluate("document.querySelector('#home-diapo [data-idx]').textContent") == '1 / 17')
        ok('diaporama : la zone des photos occupe l\'écran (pas réduite à zéro)', await page.evaluate("document.querySelector('#home-diapo .diapo').getBoundingClientRect().height") > 500)
        ok('diaporama : photo de nuit absente', await page.evaluate("[...document.querySelectorAll('#home-diapo img')].every(i=>!i.src.includes('neige'))"))
        await page.keyboard.press('ArrowRight')
        await page.wait_for_timeout(100)
        ok('diaporama : flèche droite = photo suivante', await page.evaluate("document.querySelector('#home-diapo [data-idx]').textContent") == '2 / 17')
        await page.click('#home-diapo [data-play]')
        ok('diaporama : bouton pause', await page.get_attribute('#home-diapo [data-play]', 'aria-pressed') == 'false')
        await page.keyboard.press('Escape')
        await page.wait_for_timeout(200)
        ok('diaporama : Échap ferme la superposition', await page.evaluate("document.getElementById('home-diapo').hidden && document.body.style.overflow===''"))
        # menu mobile
        await page.set_viewport_size({'width': 390, 'height': 844})
        await page.click('#menu')
        await page.wait_for_timeout(400)
        ok('menu mobile : s\'ouvre', 'open' in (await page.get_attribute('#nav', 'class')))
        await page.click('#menu-close')
        await page.wait_for_timeout(400)
        ok('menu mobile : se ferme', 'open' not in (await page.get_attribute('#nav', 'class')))
        ok('barre Réserver / Appeler visible sur mobile', await page.is_visible('.mobile-cta'))
        await page.set_viewport_size({'width': 1280, 'height': 800})

        # 4. réservation : deux calendriers (langue du cadre), tarifs, inclus / non fourni, widget unique, accès
        for d in DIRS:
            await page.goto(f'{BASE}/{d}reservation.html', wait_until='domcontentloaded')
            srcs = await page.evaluate("[...document.querySelectorAll('#dispo iframe.nr-cal')].map(f=>f.getAttribute('src'))")
            ok(f'{d}réservation : 2 calendriers Nuitrésa (gîtes 1100 et 1101) en {NRL[d]}', len(srcs) == 2 and '/calendrier-multiple-1100-' + KEY in srcs[0] and '/calendrier-multiple-1101-' + KEY in srcs[1] and all(f'?l={NRL[d]}&nb_mois=2&id=nr-cal-' in x for x in srcs), json.dumps(srcs))
            w = await page.locator('.nuit-resa-widget').count()
            ok(f'{d}réservation : un seul formulaire Nuitrésa, langue {NRL[d]}, estimation globale', w == 1 and await page.get_attribute('.nuit-resa-widget', 'data-nr-lang') == NRL[d] and await page.get_attribute('.nuit-resa-widget', 'data-nr-aggregate-availability') == '1')
            prices = await page.evaluate("[...document.querySelectorAll('#tarifs .prices b')].map(b=>b.textContent)")
            ok(f'{d}réservation : grille 300 / 350 / 300 / 420 €', prices == ['300 €', '350 €', '300 €', '420 €'], json.dumps(prices))
            ok(f'{d}réservation : inclus (4) et non fourni (2)', await page.locator('.incl .list:not(.minus) li').count() == 4 and await page.locator('.incl .list.minus li').count() == 2)
            ok(f'{d}réservation : ordre des sections', await page.evaluate("[...document.querySelectorAll('main section[id]')].map(s=>s.id)") == ['dispo', 'tarifs', 'demande', 'acces'])
        await page.goto(f'{BASE}/reservation.html', wait_until='domcontentloaded')
        ok('réservation : calendriers côte à côte sur ordinateur', await page.evaluate("(()=>{const b=[...document.querySelectorAll('.cal-box')].map(e=>e.getBoundingClientRect());return b.length===2 && Math.abs(b[0].top-b[1].top)<2 && b[1].left>b[0].right})()"))
        await page.evaluate("window.postMessage({frameId:'nr-cal-1100', height:900}, '*')")
        await page.wait_for_timeout(300)
        ok('réservation : un message de hauteur venant d\'ailleurs que Nuitrésa est ignoré', await page.evaluate("document.getElementById('nr-cal-1100').style.height") == '')
        ok('réservation : repli e-mail sous le formulaire', await page.locator('#demande a[href^="mailto:"]').count() == 1)
        ok('réservation : plus de bloc hôtes (un seul chez-soi : accueil)', await page.locator('.hosts').count() == 0)

        # 5. tous les boutons « Réserver » du site pointent vers reservation.html#demande
        for pg in ['index', 'le-domaine', 'medias', 'avis']:
            await page.goto(f'{BASE}/{pg}.html', wait_until='domcontentloaded')
            bad = await page.evaluate("[...document.querySelectorAll('a.btn-p, a.book')].filter(a=>!a.getAttribute('href').startsWith('reservation.html#demande')).map(a=>a.getAttribute('href'))")
            ok(f'{pg} : boutons Réserver → reservation.html#demande', not bad, json.dumps(bad))

        # 6. domaine & alentours : texte adapté (plus d'équitation), galeries, sites, loisirs, liens
        await page.goto(f'{BASE}/le-domaine.html', wait_until='domcontentloaded')
        txt = await page.evaluate("document.querySelector('#domaine').textContent")
        ok('domaine : chevaux à la retraite, plus d\'équitation', 'retraite' in txt and 'cavaliers confirmés' not in txt)
        ok('domaine : galerie 6 photos (Urielle)', await page.locator('#domaine ~ section .gallery a').count() >= 6 and 'Urielle' in (await page.evaluate("document.querySelector('[data-cap*=Urielle]')?.getAttribute('data-cap') || ''")))
        ok('alentours : ancre #alentours, 9 sites, loisirs sans équitation', await page.locator('#alentours').count() == 1 and await page.locator('.grid3 .tile').count() == 9 and not await page.evaluate("[...document.querySelectorAll('.chips li')].some(l=>/[ée]quitation|riding|Reiten|equitación|equitação|paardrijden|骑马/i.test(l.textContent))"))
        ok('alentours : liens utiles', await page.locator('.chips li a[target=_blank]').count() >= 5)

        # 7. En images : onglets, diaporama partagé, vidéos, visite 360° chargée à l'ouverture
        await page.goto(f'{BASE}/medias.html', wait_until='load')
        ok('en images : 3 onglets, diaporama ouvert par défaut', await page.locator('.tabs [role=tab]').count() == 3 and await page.evaluate("[...document.querySelectorAll('.panel')].map(p=>p.hidden)") == [False, True, True])
        ok('diaporama : 17 photos, une seule visible, sans photo de nuit', await page.locator('.diapo img').count() == 17 and await page.locator('.diapo img.on').count() == 1 and await page.evaluate("[...document.querySelectorAll('.diapo img')].every(i=>!i.src.includes('neige'))"))
        ok('diaporama : légende « Le domaine »', await page.evaluate("document.querySelector('.diapo b[data-group]').textContent") == 'Le domaine')
        await page.click('.diapo-ctl [data-next]')
        ok('diaporama : bouton suivant', await page.evaluate("document.querySelector('.diapo [data-idx]').textContent") == '2 / 17')
        ok('diaporama : audio en pause par défaut', await page.evaluate("document.querySelector('.diapo-app audio').paused"))
        await page.click('#tab-videos')
        ok('onglet vidéos : 3 vidéos avec affiche et sous-titre', await page.evaluate("[...document.querySelectorAll('.panel')].map(p=>p.hidden)") == [True, False, True] and await page.locator('#videos video[poster]').count() == 3 and await page.locator('#videos figcaption b').count() == 3)
        ok('onglet vidéos : diaporama mis en pause', await page.get_attribute('.diapo-ctl [data-play]', 'aria-pressed') == 'false')
        ok('visite 360° : cadre non chargé tant que l\'onglet est fermé', await page.evaluate("!document.querySelector('#visite iframe').src"))
        await page.click('#tab-visite')
        ok('visite 360° : cadre https chargé à l\'ouverture de l\'onglet, lien de repli', await page.evaluate("document.querySelector('#visite iframe').src.startsWith('https://www.hdmedia.fr/')") and await page.locator('#visite a[target=_blank]').count() == 1)
        await page.goto(f'{BASE}/medias.html#visite', wait_until='load')
        ok('en images : l\'ancre #visite ouvre le bon onglet', await page.evaluate("[...document.querySelectorAll('.panel')].map(p=>p.hidden)") == [True, True, False])

        # 8. avis : inchangée (notes, 6 avis, labels, plateformes, livre d'or)
        for d in DIRS:
            await page.goto(f'{BASE}/{d}avis.html', wait_until='domcontentloaded')
            src = await page.get_attribute('#livre-d-or iframe.nr-guestbook', 'src')
            ok(f'{d}avis : 4 notes, 6 avis, 3 labels, 6 plateformes, livre d\'or', await page.locator('.rating').count() == 4 and await page.locator('.reviews blockquote').count() == 6 and await page.locator('.logos a').count() >= 3 and await page.locator('.prices div').count() == 6 and src == 'https://public.nuit-resa.com/avis-' + KEY + '.html')

        # 9. notes pour Marc (FR seulement) : venues de TODO.md, au bon endroit, sans mot de passe
        await page.goto(f'{BASE}/index.html', wait_until='domcontentloaded')
        ok('notes : bouton présent en français', await page.locator('#nbtn').count() == 1)
        ok('notes : invisibles tant que le bouton n\'est pas pressé', not await page.is_visible('.nbub'))
        await page.click('#nbtn')
        ok('notes : pastilles et panneau après le clic', await page.is_visible('.nbub') and await page.is_visible('.npanel'))
        nn = await page.evaluate("[...document.querySelectorAll('[data-note]')].map(e=>e.getAttribute('data-note'))")
        ok('notes accueil : vue d\'ensemble (sans clé dans le TODO) + notes sur la fiche, l\'avis, les hôtes', any(n.startswith("Vue d'ensemble") for n in nn) and len(nn) >= 5, str(len(nn)))
        # Sécurité : aucun identifiant ni mot de passe dans les notes (on cherche les formes « mot de passe : xxx »,
        # « login : xxx » — jamais la valeur elle-même, qui ne doit exister nulle part dans le dépôt).
        ok('notes : aucune ne contient un identifiant ou un mot de passe', not any(re.search(r'(mot de passe|password|login|identifiant)\s*[:=]\s*\S', n, re.I) for n in nn))
        for pg, must in [('reservation', 'Nuitrésa — à faire par Marc'), ('mentions-legales', 'logo'), ('medias', 'vidéos'), ('le-domaine', 'retraite'), ('avis', 'Airbnb')]:
            await page.goto(f'{BASE}/{pg}.html', wait_until='domcontentloaded')
            nn = await page.evaluate("[...document.querySelectorAll('[data-note]')].map(e=>e.getAttribute('data-note'))")
            ok(f'notes {pg} : présentes et au bon endroit ({must})', any(must in n for n in nn), str(len(nn)))
        await page.goto(f'{BASE}/en/index.html', wait_until='domcontentloaded')
        ok('notes : absentes en anglais', await page.locator('#nbtn, [data-note]').count() == 0)

        # 10. langues : chaque drapeau mène à la même page dans l'autre langue
        await page.goto(f'{BASE}/medias.html', wait_until='domcontentloaded')
        hrefs = await page.evaluate("[...document.querySelectorAll('.langs a')].map(a=>a.getAttribute('href'))")
        ok('langues : 7 liens (×2), vers medias.html', len(hrefs) == 14 and all(h.endswith('medias.html') for h in hrefs), json.dumps(hrefs))
        await page.click('.langdd summary')
        ok('langues : le menu déroulant s\'ouvre', await page.get_attribute('.langdd', 'open') is not None)
        await page.click('h1')
        ok('langues : clic ailleurs referme le menu', await page.get_attribute('.langdd', 'open') is None)

        # 12. référencement : FAQ (données structurées), pages de fond en fr/en/de seulement, pied de page, sitemap, 404
        await page.goto(f'{BASE}/questions.html', wait_until='domcontentloaded')
        faq = await page.evaluate("JSON.parse([...document.querySelectorAll('script[type=\"application/ld+json\"]')].map(s=>s.textContent).find(t=>t.includes('FAQPage')))")
        ok('FAQ : données structurées FAQPage avec 12 questions', faq['@type'] == 'FAQPage' and len(faq['mainEntity']) == 12 and all(q['acceptedAnswer']['text'] for q in faq['mainEntity']))
        ok('FAQ : 12 tiroirs, le premier ouvert', await page.locator('.faq details').count() == 12 and await page.get_attribute('.faq details', 'open') is not None)
        bc = await page.evaluate("[...document.querySelectorAll('script[type=\"application/ld+json\"]')].some(s=>s.textContent.includes('BreadcrumbList'))")
        ok('FAQ : fil d\'Ariane (BreadcrumbList)', bc)
        foot = await page.evaluate("[...document.querySelectorAll('.foot-links a')].map(a=>a.getAttribute('href'))")
        ok('pied de page FR : FAQ + 3 pages de fond + mentions légales', foot[:4] == ['questions.html'] + [l + '.html' for l in LANDING] and 'mentions-legales.html' in foot, json.dumps(foot))
        await page.goto(f'{BASE}/es/questions.html', wait_until='domcontentloaded')
        foot = await page.evaluate("[...document.querySelectorAll('.foot-links a')].map(a=>a.getAttribute('href'))")
        ok('pied de page ES : FAQ sans pages de fond', foot[0] == 'questions.html' and not any(l in h for h in foot for l in LANDING), json.dumps(foot))
        r = await page.goto(f'{BASE}/es/gite-lac-de-creutzwald.html', wait_until='domcontentloaded')
        ok('pages de fond : absentes en espagnol (404)', r.status == 404)
        await page.goto(f'{BASE}/de/gite-accessible-pmr-moselle.html', wait_until='domcontentloaded')
        ok('page de fond DE : H1, photo d\'illustration, faits, bouton Réserver', await page.locator('h1').count() == 1 and await page.locator('.page-hero img').count() >= 1 and await page.locator('dl.fiche div').count() >= 4 and await page.locator('a.btn[href="reservation.html#demande"]').count() >= 1)
        sm = (ROOT / 'dist/sitemap.xml').read_text(encoding='utf-8')
        ok('sitemap : versions linguistiques (xhtml:link) et pages de fond, sans mentions légales', 'xhtml:link rel="alternate" hreflang="de"' in sm and 'gite-lac-de-creutzwald.html' in sm and 'mentions-legales' not in sm and sm.count('<url>') >= 7 * 7 - 7 + 9)
        rb = (ROOT / 'dist/robots.txt').read_text(encoding='utf-8')
        ok('robots.txt : site de travail interdit aux moteurs (la version livrée les autorise)', 'Disallow: /' in rb)
        r = await page.goto(f'{BASE}/404.html', wait_until='domcontentloaded')
        ok('404 : page présente, non indexée, titre, liens absolus vers l\'accueil de chaque langue', r.status == 200 and await page.locator('meta[name=robots]').count() == 1 and 'introuvable' in (await page.title()).lower() and await page.locator('main a[href="/domaine-du-geisberg/index.html"]').count() >= 1 and await page.locator('main a[href="/domaine-du-geisberg/zh/index.html"]').count() == 1)
        ok('404 : feuille de style et logo en chemin absolu', await page.locator('link[rel=stylesheet][href^="/domaine-du-geisberg/css/"]').count() == 1)
        ok('404 : pas de canonical ni de hreflang', await page.locator('link[rel=canonical], link[rel=alternate][hreflang]').count() == 0)

        # 13. accessibilité : audit axe-core (WCAG 2.1 A/AA + bonnes pratiques) sur chaque page, deux thèmes, deux langues.
        # Contexte à part : l'injection du script d'audit est un script en ligne, interdit par la CSP du site.
        actx = await b.new_context(viewport={'width': 1280, 'height': 800}, bypass_csp=True)
        apage = await actx.new_page()
        await apage.route(re.compile(r'^(?!http://127\.0\.0\.1).*'), block)
        axe = str(ROOT / 'tests/vendor/axe.min.js')
        for theme in ['light', 'dark']:
            for d in ['', 'de/']:
                for pg in PAGES + LANDING + (['404'] if d == '' else []):
                    await apage.goto(f'{BASE}/{d}{pg}.html', wait_until='load')
                    # animations figées : axe mesure des couleurs stables, pas un fondu en cours
                    await apage.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important} .reveal{opacity:1!important;transform:none!important}')
                    await apage.evaluate(f"document.documentElement.setAttribute('data-theme','{theme}'); document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
                    await apage.add_script_tag(path=axe)
                    res = await apage.evaluate("axe.run(document, {runOnly:{type:'tag', values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}})")
                    viol = [f"{v['id']} ({v['impact']}) : {v['nodes'][0]['html'][:60]}" for v in res['violations']]
                    ok(f'accessibilité {theme} {d}{pg} : aucune violation axe-core', not viol, ' | '.join(viol[:3]))
        await actx.close()

        # 11. modes clair et sombre : contraste du texte courant, des boutons et des liens sur chaque page
        JS_CONTRAST = """(() => {
          const parse = c => { const m = c.match(/-?\\d+(\\.\\d+)?/g).map(Number); return c.startsWith('color(srgb') ? m.slice(0,3).map(v => v*255) : m.slice(0,3) };
          const lum = c => { const [r,g,b] = parse(c).map(v => { v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4)}); return 0.2126*r+0.7152*g+0.0722*b };
          const alpha = c => { const m = c.match(/\\/\\s*([\\d.]+)\\)$|,\\s*([\\d.]+)\\)$/); return m ? parseFloat(m[1] || m[2]) : 1 };
          const bgOf = el => { let e = el; while (e) { const c = getComputedStyle(e).backgroundColor; if (c && c !== 'transparent' && alpha(c) > 0.5) return c; e = e.parentElement } return getComputedStyle(document.body).backgroundColor };
          const bad = [];
          for (const el of document.querySelectorAll('main p, main li, main dd, main dt, main h2, main h3, .btn, .site-footer a, nav.nav > a')) {
            if (!el.offsetParent || el.closest('.hero, .page-hero, .teaser, .diapo, .diapo-overlay')) continue;
            const cs = getComputedStyle(el); const fg = lum(cs.color), bg = lum(bgOf(el));
            const ratio = (Math.max(fg,bg)+0.05)/(Math.min(fg,bg)+0.05);
            if (ratio < 4.5) bad.push(el.tagName + (el.className ? '.' + String(el.className).split(' ')[0] : '') + ' ' + ratio.toFixed(1));
          }
          return bad;
        })()"""
        for theme in ['light', 'dark']:
            for pg in PAGES + LANDING + ['404']:
                await page.goto(f'{BASE}/{pg}.html', wait_until='domcontentloaded')
                await page.evaluate(f"document.documentElement.setAttribute('data-theme','{theme}'); document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
                await page.wait_for_timeout(100)
                bad = await page.evaluate(JS_CONTRAST)
                ok(f'contraste {theme} {pg} : texte, boutons et liens ≥ 4,5:1', not bad, ', '.join(bad[:4]))
                bgc = await page.evaluate("getComputedStyle(document.body).backgroundColor")
                ok(f'fond {theme} {pg} appliqué', (bgc == 'rgb(21, 21, 22)') == (theme == 'dark'), bgc)

        await b.close()

    bad = [r for r in results if not r[1]]
    for name, good, detail in results:
        print(('OK   ' if good else 'ÉCHEC') + ' ' + name + (f'  [{detail}]' if detail and not good else ''))
    print(f'\n{len(results) - len(bad)} tests réussis, {len(bad)} échec(s)')
    return len(bad)

sys.exit(1 if asyncio.run(main()) else 0)
