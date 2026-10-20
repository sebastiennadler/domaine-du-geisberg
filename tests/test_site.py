"""Tests fonctionnels du site généré (copie locale servie sur 127.0.0.1:8111)."""
import asyncio, json, re
from playwright.async_api import async_playwright

BASE = 'http://127.0.0.1:8111'  # serveur local sur dist/ (voir tests/run.sh)
PAGES = ['index', 'le-domaine', 'gites', 'videos', 'diaporama', 'visite', 'autour', 'avis', 'reservation', 'mentions-legales']
DIRS = ['', 'en/', 'de/', 'es/', 'pt/', 'nl/', 'zh/']
results = []


def ok(name, cond, detail=''):
    results.append((name, bool(cond), detail)); print(("ok " if cond else "KO ") + name, flush=True)


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 1280, 'height': 800})
        page = await ctx.new_page()
        page.set_default_timeout(15000)
        # pas de réseau externe ici (polices, iframe hdmedia) : on coupe tout ce qui n'est pas local
        async def block(route):
            await route.abort()
        await page.route(re.compile(r'^(?!http://127\.0\.0\.1).*'), block)
        js_errors = []
        page.on('pageerror', lambda e: js_errors.append(str(e)))
        page.on('console', lambda m: js_errors.append(m.text) if m.type == 'error' and 'Failed to load' not in m.text else None)

        # 1. toutes les pages de toutes les langues : chargement, H1, menu complet, sans erreur JS
        for d in DIRS:
            for pg in PAGES:
                r = await page.goto(f'{BASE}/{d}{pg}.html', wait_until='domcontentloaded')
                ok(f'{d}{pg}: HTTP 200', r.status == 200)
                h1 = await page.locator('h1').count()
                ok(f'{d}{pg}: un H1', h1 == 1, f'{h1} h1')
                nav = await page.locator('nav.nav > a').count()
                ok(f'{d}{pg}: menu 9 entrées + Réserver', nav == 10, f'{nav}')
                if pg != 'mentions-legales':  # pas dans le menu
                    cur = await page.locator('nav.nav > a[aria-current="page"]').count()
                    ok(f'{d}{pg}: entrée de menu active', cur == 1, f'{cur}')
                lang = await page.get_attribute('html', 'lang')
                ok(f'{d}{pg}: attribut lang', lang == (d.strip('/') or 'fr'), lang)
        ok('aucune erreur JavaScript sur les 70 pages', not js_errors, '; '.join(js_errors[:3]))

        # 2. renvois gite-1 / gite-2
        await page.goto(f'{BASE}/gite-1.html', wait_until='domcontentloaded')
        await page.wait_for_timeout(500)
        ok('gite-1.html renvoie vers gites.html', page.url.endswith('/gites.html'), page.url)
        await page.goto(f'{BASE}/de/gite-2.html', wait_until='domcontentloaded')
        await page.wait_for_timeout(500)
        ok('de/gite-2.html renvoie vers de/gites.html', page.url.endswith('/de/gites.html'), page.url)

        # 3. accueil : bandeau, points, thème, visionneuse, menu mobile
        await page.goto(f'{BASE}/index.html', wait_until='domcontentloaded')
        ok('bandeau : 3 diapositives', await page.locator('.hero .slide').count() == 3)
        ok('bandeau : première diapositive visible', 'on' in (await page.get_attribute('.hero .slide:nth-child(1)', 'class')))
        await page.click('.hero .dots button:nth-child(2)')
        ok('bandeau : clic sur un point change la diapositive', 'on' in (await page.get_attribute('.hero .slide:nth-child(2)', 'class')))
        await page.click('#theme')
        ok('bouton thème → sombre', await page.get_attribute('html', 'data-theme') == 'dark')
        await page.click('#theme')
        ok('bouton thème → clair', await page.get_attribute('html', 'data-theme') == 'light')
        await page.click('.mosaic a:first-child')
        await page.wait_for_timeout(300)
        ok('visionneuse : s\'ouvre au clic sur la mosaïque', await page.is_visible('.lb.open'))
        src1 = await page.get_attribute('.lb img', 'src')
        await page.keyboard.press('ArrowRight')
        src2 = await page.get_attribute('.lb img', 'src')
        ok('visionneuse : flèche droite = photo suivante', src1 != src2)
        await page.keyboard.press('Escape')
        ok('visionneuse : Échap ferme', not await page.is_visible('.lb.open'))
        ok('bouton remonter présent', await page.locator('.totop').count() == 1)
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

        # 4. gîtes : galerie, calendriers Nuitrésa (un par gîte, langue du cadre), bandeau → réservation
        KEY = 'e8dc8870f783d664870e89ac71801620'
        NRL = [('', 'FR'), ('en/', 'EN'), ('de/', 'DE'), ('es/', 'ES'), ('pt/', 'EN'), ('nl/', 'EN'), ('zh/', 'EN')]
        for d, nrl in NRL:
            await page.goto(f'{BASE}/{d}gites.html', wait_until='domcontentloaded')
            srcs = await page.evaluate("[...document.querySelectorAll('#dispo iframe.nr-cal')].map(f=>f.getAttribute('src'))")
            ok(f'{d}gîtes : 2 calendriers Nuitrésa (gîte 1100 et 1101)', len(srcs) == 2 and '/calendrier-multiple-1100-' + KEY in srcs[0] and '/calendrier-multiple-1101-' + KEY in srcs[1], json.dumps(srcs))
            ok(f'{d}gîtes : calendriers en {nrl}, 2 mois, id transmis', all(f'?l={nrl}&nb_mois=2&id=nr-cal-' in x for x in srcs), json.dumps(srcs))
            ok(f'{d}gîtes : calendriers chargés à la demande, avec titre', await page.evaluate("[...document.querySelectorAll('iframe.nr-cal')].every(f=>f.loading==='lazy' && f.title && f.id===new URL(f.src).searchParams.get('id'))"))
        await page.goto(f'{BASE}/gites.html', wait_until='domcontentloaded')
        ok('gîtes : plus aucun calendrier maison', await page.locator('.cal').count() == 0)
        ok('gîtes : galerie de 7 photos', await page.locator('.gallery a').count() == 7)
        ok('gîtes : bandeau #dispo', await page.locator('#dispo').count() == 1)
        ok('gîtes : bouton du bandeau → reservation.html#demande', await page.get_attribute('#dispo .band a.btn', 'href') == 'reservation.html#demande')
        leads = await page.evaluate("[...document.querySelectorAll('p.lead, .list li')].map(e=>[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('')).join(' ')")
        ok('gîtes : 4 personnes (jamais 5) dans les textes', '4 personnes' in leads and '5 personnes' not in leads)
        await page.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
        await page.wait_for_timeout(900)
        ok('gîtes : calendriers côte à côte sur ordinateur', await page.evaluate("(()=>{const b=[...document.querySelectorAll('.cal-box')].map(e=>e.getBoundingClientRect());return b.length===2 && Math.abs(b[0].top-b[1].top)<2 && b[1].left>b[0].right})()"))
        await page.set_viewport_size({'width': 390, 'height': 844})
        ok('gîtes : calendriers empilés sur mobile, sans débordement', await page.evaluate("(()=>{const b=[...document.querySelectorAll('.cal-box')].map(e=>e.getBoundingClientRect());return b.length===2 && b[1].top>b[0].bottom-1 && b[1].right<=391 && document.documentElement.scrollWidth<=390})()"))
        await page.set_viewport_size({'width': 1280, 'height': 800})
        # hauteur ajustée par message (simulation du message que le cadre Nuitrésa envoie) ; message d'une autre origine ignoré
        h0 = await page.evaluate("document.getElementById('nr-cal-1100').getBoundingClientRect().height")
        await page.evaluate("window.postMessage({frameId:'nr-cal-1100', height:900}, '*')")
        await page.wait_for_timeout(200)
        h1 = await page.evaluate("document.getElementById('nr-cal-1100').getBoundingClientRect().height")
        ok('gîtes : un message de hauteur venant d\'ailleurs que Nuitrésa est ignoré', h0 == h1 == 430, f'{h0} → {h1}')

        # 5. diaporama : les photos défilent, une seule visible, audio
        await page.goto(f'{BASE}/diaporama.html', wait_until='domcontentloaded')
        await page.wait_for_timeout(800)
        async def visible_imgs():
            return await page.evaluate("[...document.querySelectorAll('#diapo img')].filter(i=>getComputedStyle(i).opacity==='1').map(i=>i.getAttribute('data-cap'))")
        v0 = await visible_imgs()
        ok('diaporama : exactement une photo visible', len(v0) == 1, json.dumps(v0, ensure_ascii=False))
        cap0 = await page.text_content('#diapo-cap')
        ok('diaporama : légende = photo visible', v0 and v0[0] == cap0, f'{v0} / {cap0}')
        await page.click('#d-next')
        await page.wait_for_timeout(1500)
        v1 = await visible_imgs()
        ok('diaporama : bouton suivant change la photo', len(v1) == 1 and v1 != v0, json.dumps(v1, ensure_ascii=False))
        await page.wait_for_timeout(5500)
        v2 = await visible_imgs()
        ok('diaporama : défilement automatique (5 s)', len(v2) == 1 and v2 != v1, json.dumps(v2, ensure_ascii=False))
        await page.click('#d-play')
        ok('diaporama : pause', await page.get_attribute('#d-play', 'aria-pressed') == 'false')
        au = await page.evaluate("(async()=>{document.getElementById('d-audio').click();await new Promise(r=>setTimeout(r,1500));var a=document.getElementById('d-bird');return {paused:a.paused,err:a.error&&a.error.code,rs:a.readyState}})()")
        ok('diaporama : chants d\'oiseaux se lancent', not au['paused'] and not au['err'], json.dumps(au))
        ok('diaporama : 15 photos (3 bandeau + 6 domaine + 7 gîtes) — 16 attendu ?', await page.locator('#diapo img').count() in (15, 16), str(await page.locator('#diapo img').count()))

        # 6. vidéos
        await page.goto(f'{BASE}/videos.html', wait_until='domcontentloaded')
        ok('vidéos : 3 lecteurs', await page.locator('video').count() == 3)
        ok('vidéos : preload=none (rien téléchargé avant lecture)', await page.evaluate("[...document.querySelectorAll('video')].every(v=>v.preload==='none')"))
        # (la lecture H.264 est testée dans le vrai navigateur sur le site en ligne : Chromium de test n'a pas le codec)
        srcs = await page.evaluate("[...document.querySelectorAll('video source')].map(s=>s.getAttribute('src'))")
        ok('vidéos : 3 sources MP4 distinctes', len(set(srcs)) == 3 and all(x.endswith('.mp4') for x in srcs), json.dumps(srcs))
        ok('vidéos : affiche (poster) sur chaque lecteur', await page.evaluate("[...document.querySelectorAll('video')].every(v=>v.poster)"))

        # 7. visite 360° : iframe https
        await page.goto(f'{BASE}/visite.html', wait_until='domcontentloaded')
        src = await page.get_attribute('.visite iframe', 'src')
        ok('visite : iframe en https', src and src.startswith('https://'), src)

        # 8. réservation : widget Nuitrésa (un seul), langue du widget, repli e-mail
        for d, nrl in [('', 'FR'), ('en/', 'EN'), ('de/', 'DE'), ('es/', 'ES'), ('pt/', 'EN'), ('nl/', 'EN'), ('zh/', 'EN')]:
            await page.goto(f'{BASE}/{d}reservation.html', wait_until='domcontentloaded')
            ok(f'{d}réservation : un seul widget Nuitrésa', await page.locator('.nuit-resa-widget').count() == 1)
            ok(f'{d}réservation : clé publique et version v2', await page.get_attribute('.nuit-resa-widget', 'data-nr-key') == 'e8dc8870f783d664870e89ac71801620' and await page.get_attribute('.nuit-resa-widget', 'data-nr-version') == 'v2')
            ok(f'{d}réservation : langue du widget = {nrl}', await page.get_attribute('.nuit-resa-widget', 'data-nr-lang') == nrl)
            ok(f'{d}réservation : script Nuitrésa chargé en async', await page.evaluate("!!document.querySelector('script[async][src^=\"https://public.nuit-resa.com/js/nuit-resa-widget-v2.js\"]')"))
            ok(f'{d}réservation : plus de formulaire maison ni de calendrier', await page.locator('#resa, .cal').count() == 0)
            ok(f'{d}réservation : option « disponibilités globales » du formulaire', await page.get_attribute('.nuit-resa-widget', 'data-nr-aggregate-availability') == '1' and await page.get_attribute('.nuit-resa-widget', 'data-nr-params') == 'ad=1')
            ok(f'{d}réservation : repli e-mail sous le widget', await page.locator('#demande a[href=\"mailto:gitevarsberg@hotmail.com\"]').count() == 1)
        await page.goto(f'{BASE}/reservation.html', wait_until='domcontentloaded')
        ok('réservation : ancre #demande (cible des boutons Réserver)', await page.locator('#demande').count() == 1)
        ok('réservation : ancre #acces (photo Agnès et Marc)', await page.locator('#acces .hosts img').count() == 1)
        ok('réservation : aucune trace d\'identifiant/mot de passe', 'Uriellea' not in (await page.content()))
        # 8b. tous les boutons « Réserver » du site pointent vers reservation.html#demande
        for d in DIRS:
            await page.goto(f'{BASE}/{d}index.html', wait_until='domcontentloaded')
            hrefs = await page.evaluate("[...document.querySelectorAll('a.book, .mobile-cta a.btn-p')].map(a=>a.getAttribute('href'))")
            ok(f'{d}accueil : boutons Réserver → reservation.html#demande', hrefs and all(h == 'reservation.html#demande' for h in hrefs), json.dumps(hrefs))

        # 8c. avis : livre d'or Nuitrésa
        for d in DIRS:
            await page.goto(f'{BASE}/{d}avis.html', wait_until='domcontentloaded')
            src = await page.get_attribute('#livre-d-or iframe.nr-guestbook', 'src')
            ok(f'{d}avis : livre d\'or Nuitrésa (chargé à la demande)', src == 'https://public.nuit-resa.com/avis-' + KEY + '.html' and await page.get_attribute('#livre-d-or iframe', 'loading') == 'lazy', str(src))
            ok(f'{d}avis : 6 avis + titre du livre d\'or', await page.locator('.reviews blockquote').count() == 6 and (await page.text_content('#livre-d-or h2')).strip() != '')

        # 9. notes pour Marc (FR seulement)
        await page.goto(f'{BASE}/index.html', wait_until='domcontentloaded')
        await page.click('#nbtn')
        ok('notes : mode activé', 'notes' in (await page.get_attribute('html', 'class')))
        n = await page.locator('.nbub').count()
        ok('notes : pastilles présentes sur l\'accueil', n >= 3, str(n))
        await page.goto(f'{BASE}/en/index.html', wait_until='domcontentloaded')
        ok('notes : absentes en anglais', await page.locator('#nbtn').count() == 0)
        await page.goto(f'{BASE}/gites.html', wait_until='domcontentloaded')
        await page.click('#nbtn')
        nn = await page.evaluate("[...document.querySelectorAll('[data-note]')].map(e=>e.getAttribute('data-note'))")
        ok('notes gîtes : note « réglages Nuitrésa » avec ses 8 points', any(n.startswith('Réglages Nuitrésa') and n.count('\n') >= 8 for n in nn), str(len(nn)))
        ok('notes gîtes : retours à la ligne conservés à l\'affichage', await page.evaluate("getComputedStyle(document.querySelector('.ntip')).whiteSpace === 'pre-line'"))
        ok('notes : aucune note ne contient le mot de passe lui-même', not any('Uriellea' in n for n in nn))
        ok('notes gîtes : point sécurité (mot de passe à retirer du document et à changer)', any('Sécurité : le mot de passe' in n for n in nn))
        # chaque page FR a des notes et son panneau les liste toutes ; aucune n'est vide
        for pg in PAGES:
            await page.goto(f'{BASE}/{pg}.html', wait_until='domcontentloaded')
            n_attr = await page.locator('[data-note]').count()
            n_list = await page.locator('#nlist li').count()
            empty = await page.evaluate("[...document.querySelectorAll('[data-note]')].some(e=>e.getAttribute('data-note').trim().length < 20)")
            ok(f'notes {pg} : {n_attr} note(s), toutes listées dans le panneau, aucune vide', n_attr >= 1 and n_list == n_attr and not empty, f'{n_attr} / {n_list}')
        await page.goto(f'{BASE}/index.html', wait_until='domcontentloaded')
        todo = await page.evaluate("[...document.querySelectorAll('[data-note]')].map(e=>e.getAttribute('data-note')).find(n=>n.startsWith(\"VUE D'ENSEMBLE\"))")
        ok('notes accueil : vue d\'ensemble (Nuitrésa urgent, à confirmer, à envoyer, mise en ligne)', bool(todo) and all(k in todo for k in ['URGENT', '4 à 5 personnes', 'canapé-lit', 'OVH', 'Sécurité']))
        await page.goto(f'{BASE}/reservation.html', wait_until='domcontentloaded')
        wn = await page.evaluate("document.querySelector('#demande').getAttribute('data-note')")
        ok('notes réservation : capacité mini 4 et 4 nuits signalées sur le formulaire', wn.startswith('URGENT') and 'Capacité mini = 4' in wn and 'nuits minimum = 4' in wn and 'une seule demande test' in wn)
        await page.goto(f'{BASE}/index.html', wait_until='domcontentloaded')
        ok('notes : le mot « Urielle » remplace « le chien » dans les légendes', 'Urielle' in (await page.evaluate("document.querySelector('.hosts img').alt")))

        # 10. langues : chaque drapeau mène à la même page dans l'autre langue
        await page.goto(f'{BASE}/gites.html', wait_until='domcontentloaded')
        hrefs = await page.evaluate("[...document.querySelectorAll('.langs a')].map(a=>a.getAttribute('href'))")
        ok('langues : 7 liens (×2 : rangée mobile + menu ordinateur), vers gites.html', len(hrefs) == 14 and all(h.endswith('gites.html') for h in hrefs), json.dumps(hrefs))
        await page.click('.langdd summary')
        ok('langues : le menu déroulant s\'ouvre', await page.get_attribute('.langdd', 'open') is not None)
        await page.click('h1')
        ok('langues : clic ailleurs referme le menu', await page.get_attribute('.langdd', 'open') is None)

        await b.close()

    bad = [r for r in results if not r[1]]
    for name, good, detail in results:
        print(('OK   ' if good else 'ÉCHEC') + ' ' + name + (f'  [{detail}]' if detail and not good else ''))
    print(f'\n{len(results) - len(bad)} tests réussis, {len(bad)} échec(s)')
    return len(bad)

sys.exit(1 if asyncio.run(main()) else 0)
