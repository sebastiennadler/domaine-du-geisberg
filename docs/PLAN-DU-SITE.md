# Plan du site — Domaine du Geisberg

Ce document décrit le site **en entier**, assez précisément pour le **recréer de zéro** : identité,
contenus, pages, structure du code, génération, référencement, tests, livraison. Les règles et décisions
qui priment sont dans `CLAUDE.md` ; ce qu'il reste à faire est dans `TODO.md`. La partie 9 est le
**registre daté des directives** reçues depuis le début du projet.

Versions : v1 (site actuel, octobre 2026) → **v2** (structure cible décrite ici, à construire).

---

## 1. Identité

| Élément | Valeur |
|---|---|
| Nom | Domaine du Geisberg — Gîtes ruraux, Varsberg |
| Propriétaires / hôtes | Agnès et Marc Nadler, hôtes depuis 2007 ; Urielle, leur malinoise ; chevaux à la retraite |
| Adresse | 6 rue du Geisberg, 57880 Varsberg (Moselle, Grand Est) — GPS 49.1712729, 6.6259474 |
| Contact | Marc 07 89 56 74 91 · Agnès 06 73 42 05 89 · gitevarsberg@hotmail.com |
| Site | `https://www.domainedugeisberg.fr` (DECLIC) ; site de travail `https://sebastiennadler.github.io/domaine-du-geisberg/` |
| Labels | Gîtes de France, Clévacances, Tourisme & Handicap |
| Plateformes | Gîtes de France, Clévacances, Airbnb (gîte 1 et 2), Abritel / Expedia (gîte 1 et 2) ; Superhôte Airbnb |
| Réservation | Nuitrésa (clé publique `e8dc8870f783d664870e89ac71801620`, gîtes 1100 et 1101) |
| Logo | `assets/photos-sources/logo/logo-geisberg.png` — maison dessinée, bordeaux `#7a1f2b` env., vert olive `#5b6b2f` env., vert clair `#a8c45a` env. |
| Accroche | « Au cœur de la nature, deux gîtes d'exception à proximité immédiate de la forêt » |
| Mentions légales | SIRET 478 447 790 00013 · TVA FR44 478447790 · éditeur Marc Nadler · hébergeur DECLIC (GitHub Pages pour le site de travail) |

**Direction artistique (v1, à conserver sauf décision)** : naturel, calme, chaleureux. Fond crème
`#f5f2ea`, vert profond `#2b5240` (accent), cuivre `#a2652f` (accent secondaire), thème sombre
automatique. Titres *Playfair Display* (600/700), texte *Nunito Sans* (400/700/800). Coins arrondis
14 px, ombres douces, animations discrètes (désactivées si `prefers-reduced-motion`).
**Décidé le 20/10** : l'accent cuivre est remplacé par le bordeaux du logo (le logo doit s'intégrer).

## 2. Contenus (source : `src/content/`)

- `shared.json` : données communes à toutes les langues (nom, adresse, téléphones, e-mail, GPS, tarifs,
  capacité, SIRET, listes de photos par section, labels, plateformes et notes, avis, distances, liens,
  crédits, Nuitrésa, visite virtuelle, vidéos).
- `fr.json` : tous les textes en français (référence) + les notes pour Marc. `en/de/es/pt/nl/zh.json` :
  traductions, mêmes clés ; toute clé absente **retombe sur le français** (`deep_merge`).
- `images.json` : généré par `tools/photos.py` (tailles, fichiers, point focal).

### 2.1 Textes de référence validés
- Accroche (ci-dessus). Phrase hôtes : « Depuis 2007, année d'ouverture de nos gîtes, nous avons aimé
  partager avec nos hôtes de toutes nationalités, notre façon de vivre et de découvrir la leur. C'est un
  moyen pour nous de découvrir d'autres pays et cultures et de faire découvrir à d'autres les richesses de
  notre région et pays. L'usage régulier des langues allemandes et anglaises est un exercice plaisant et
  dépaysant. »
- Gîtes jumeaux : « Deux gîtes identiques. Réservez l'un des deux, ou les deux pour un groupe. » (validé)
- Capacité : « de 1 à 4 personnes » (+ couchage d'appoint discret : chauffeuse 90 cm dans le salon).

### 2.2 Fiche d'un gîte (une seule, les deux sont identiques)
Séjour avec cuisine intégrée · 2 chambres, 2 lits de 90 × 190 chacune · salle d'eau accessible PMR
(douche à l'italienne, WC) · 60 m² · terrasse privée, salon de jardin, barbecue · parking privé ·
Wi-Fi fibre · chauffage au sol par géothermie · plaque à induction, four, micro-ondes, lave-vaisselle,
lave-linge, congélateur · téléviseur écran plat · équipement bébé sur demande (lit, baignoire, chaise
haute) · VTT à disposition · animaux acceptés (2 max, sans supplément) · non fumeur · arrivée 16 h,
départ 10 h · boulangerie 300 m, restaurant 1 km, supérette 3 km.
**Inclus** : lits faits à l'arrivée, draps, toutes charges (électricité, eau, chauffage), ménage de
finition offert (logement rendu propre, vaisselle lavée et rangée). **Non fourni** : serviettes de bain.

### 2.3 Tarifs (par gîte)
Week-end 2 nuits (arrivée vendredi) 300 € · week-end 3 nuits (arrivée vendredi) 350 € · semaine 4 nuits
(arrivée dimanche à jeudi, minimum 4 nuits hors week-end) 300 € · 5 à 7 nuits 420 €. Acompte 25 %.
Taxe de séjour en sus. CB, chèques-vacances ANCV. Caution : 300 € (moyen à choisir par Marc : chèque ou empreinte).

### 2.4 Autour
Distances validées : lac de Creutzwald 6 km (base nautique, pêche, tennis), piscine de Creutzwald 7 km,
gare de Saint-Avold 15 km, cimetière américain 15 km, golf 15 km, Völklingen 28 km, musée des mineurs
31 km, Calypso 35 km, Centre Pompidou-Metz 40 km, Bliesbruck 61 km. À confirmer : zoo d'Amnéville,
Sainte-Croix, boucle de la Sarre. Sur place : randonnée, forêts, commerces à proximité (plus d'équitation).

### 2.5 Photos
- `photos-sources/` (originaux, suivis par git) → `tools/photos.py` → `img/<section>/<nom>-<largeur>.webp`
  (800 / 1280 / 1920 px) + `images.json`. Chaque photo a un identifiant `section/nom` utilisé dans `shared.json`.
- Sections : `hero` (bandeau d'accueil), `domaine`, `gites` (communes aux deux gîtes), `autour`, `logos`,
  `videos` (vignettes). **Retirée** : `hero/maison-neige-soir` (mur sali). Photo des hôtes : `domaine/agnes-marc`.
- Légendes dans `fr.json` (`captions`), dans l'ordre des listes de `shared.json`.
- Vidéos : `videos-sources/` (non suivi) → `tools/videos.py` → `videos/*.mp4` + vignettes. Trois clips :
  chant des oiseaux, balade avec les chevaux et Urielle, chevreuil. Audio du diaporama : `audio/chants-oiseaux.mp3` (Wikimedia Commons).

## 3. Pages et navigation (v2 cible)

Notes pour Marc : elles viennent de `TODO.md` (`- [ ] {clé} texte` dans les sections 4 et 5) ; `build.py` les injecte via la macro `note('clé')` des gabarits (`partials/_macros.html`), en FR et hors `--prod`.

Principe : **simple en surface, complet en profondeur**. Chaque information n'a qu'un seul « chez-soi » ;
les autres pages y renvoient. L'essentiel (quoi, combien, réserver) tient en trois écrans ; le détail
est dans des tiroirs (`<details>`) ou des pages de fond.

Menu (5 entrées + bouton « Réserver » toujours visible + langues + thème) :

| # | Page | Fichier | Contenu, dans l'ordre |
|---|---|---|---|
| 1 | **Accueil** (présentation) | `index.html` | Bandeau : photo d'Agnès, Marc et Urielle ≈ 4 s, puis photos de la maison (fondu). Accroche + 2 boutons (Voir les gîtes / Réserver). Chiffres clés : 2 gîtes identiques · 60 m² · de 1 à 4 personnes · accessible PMR · animaux. Galerie des gîtes (7 photos communes) + 2 phrases. Fiche unique (9 lignes, dont tarifs « à partir de ») + tiroir « Tout l'équipement » (5 groupes). Un seul avis (`featured_review` dans shared.json) + lien Avis. Hôtes « depuis 2007 » + coordonnées. Aperçus (photo + 2 lignes + lien) : Le domaine & alentours, En images. Bouton « Diaporama » sur le bandeau (superposition). **Fait le 20/10.** |
| 2 | **Réservation** | `reservation.html` | Disponibilités : 2 calendriers Nuitrésa (Gîte 1, Gîte 2). Tarifs (grille 2.3) + inclus / non fourni. Formulaire Nuitrésa unique (option estimation globale). Accès (itinéraire, train, carte, coordonnées). **Fait le 20/10.** |
| 3 | **Le domaine & alentours** | `le-domaine.html` | Texte « Le domaine » (à raccourcir ?), galerie du domaine (6 photos), les 6 sites incontournables avec distances et photos, loisirs (puces avec km), liens utiles. |
| 4 | **En images** | `medias.html` | Trois onglets : Diaporama (plein écran, 5 s, pause, audio), Vidéos (3 clips), Visite du gîte (360° hdmedia). Le même diaporama s'ouvre en superposition depuis le bouton du bandeau d'accueil. |
| 5 | **Avis** | `avis.html` | **Inchangée** : notes des plateformes, 6 avis, labels, « où réserver », livre d'or Nuitrésa. |
| — | Mentions légales | `mentions-legales.html` | Éditeur, hébergeur, propriété intellectuelle, données, crédits. Lien en pied de page seulement. |
| — | Redirections | `gites.html`, `diaporama.html`, `videos.html`, `visite.html`, `autour.html`, `gite-1.html`, `gite-2.html` | Pages de redirection (meta refresh + lien) vers leur nouveau « chez-soi », pour ne casser aucun lien existant. |
| — | Questions fréquentes | `questions.html` | 12 questions / réponses en tiroirs (`t.faq.items`), données structurées `FAQPage`, 7 langues. Lien en pied de page. **Fait le 20/10.** |
| — | Pages de fond (référencement) | `gite-accessible-pmr-moselle.html`, `gite-lac-de-creutzwald.html`, `gites-saint-avold-sarrebruck.html` | Un gabarit (`pages/landing.html`), contenu `t.landing[page]` : titre, accroche, photo de bandeau, 3 sections, photo secondaire, faits (dl), boutons. **FR, EN, DE seulement** (`PAGE_LANGS` dans `build.py`). Liens en pied de page. **Fait le 20/10.** |
| — | Page 404 | `404.html` (racine) | Français, liens absolus (racine du site de travail ou « / » en `--prod`) vers l'accueil de chaque langue, `noindex`, sans canonical. GitHub Pages la sert automatiquement, Apache via `ErrorDocument` (`.htaccess`). **Fait le 20/10.** |

Pied de page (toutes pages) : logo, adresse, téléphones, e-mail, labels (petits), langues, mentions
légales, « Notes pour Marc » (FR).

Pied de page : lien « Questions fréquentes » dans toutes les langues ; liens vers les trois pages de fond
en FR, EN et DE.

## 4. Structure du code (v2 cible, claire et réutilisable)

```
CLAUDE.md                 directives (source de vérité)       README.md   doc technique
TODO.md                   reste à faire                        docs/       plan, rapports, guide PDF
src/
  content/                shared.json, fr.json, en.json, … (textes et données)
  templates/
    base.html             squelette commun (head SEO, en-tête, pied, notes, scripts)
    partials/             _hero.html, _fiche.html, _calendriers.html, _widget.html, _reviews.html, _redirect.html
    pages/                index.html, reservation.html, le-domaine.html, medias.html, avis.html, mentions-legales.html
  css/style.css           une feuille, sections commentées (variables → composants → pages → notes → effets)
  js/site.js              un script, sections commentées (thème, menu, bandeau, galerie, notes, calendriers, effets)
assets/
  photos-sources/         originaux (dont logo/)              img/   dérivés webp générés (suivis par git)
  videos-sources/         originaux (non suivis)              videos/ audio/
tools/
  build.py                génère dist/ : 7 langues × pages, sitemap.xml, robots.txt, redirections, .htaccess
  check.py                vérifie dist/ : liens, images, dimensions, poids, canonical/hreflang, JSON-LD
  photos.py  videos.py    dérivés d'images / de vidéos          fetch_commons.py, fetch_audio.py : médias libres
  package.py              crée la livraison pour DECLIC : zip de dist/ horodaté
tests/
  run.sh                  serveur local sur dist/ + les deux scripts (code de retour non nul en cas d'échec)
  test_site.py            tests fonctionnels Playwright (≈ 500, réseau coupé)
  sweep.py                balayage des débordements, toutes pages, 320 → 1366 px
dist/                     généré, NON suivi par git ; c'est ce qui est publié (GitHub Pages) et livré (DECLIC)
.github/workflows/        pages.yml (build + tests + déploiement de dist/), liens.yml (lundi : liens externes),
                          photos-commons.yml, audio-commons.yml
```

Règles : contenu ≠ gabarit ≠ style ≠ script (jamais de texte en dur dans un gabarit) ; une page = un
gabarit ; un composant réutilisé = un partial ; toute donnée = `shared.json` ; tout texte = `<langue>.json`.
Le HTML généré ne se modifie jamais à la main. Python 3 + Jinja2 + Pillow ; Node uniquement pour Playwright.

Migration v1 → v2 : **faite le 20/10** (étape 1) — pages générées identiques à la v1 octet pour octet.

## 5. Génération (`tools/build.py`)

Pour chaque langue (FR à la racine, autres dans `/en/`, `/de/`… ) et chaque page : rendu Jinja2 de
`base.html` + gabarit de page avec `t` (textes de la langue, repli FR), `s` (données), `images`, helpers
`pic()` (balise `<picture>` responsive avec `srcset`, dimensions, `loading="lazy"` sauf le bandeau),
`src()`/`url()`, `nr_lang` (langue des cadres Nuitrésa : FR, EN, DE, ES, sinon EN), `csp` (politique de
sécurité, partie 8 bis), `prod`. Empreinte des fichiers CSS/JS dans l'URL (`?v=<hash>`) pour le cache. Puis
`sitemap.xml` (toutes langues, `xhtml:link` hreflang par page, sans mentions légales), `robots.txt`
(`Disallow: /` sur le site de travail, `Allow` en `--prod`), pages de redirection, `404.html`, et en `--prod`
`.htaccess` (copie de `src/htaccess`). `PAGES`, `PAGE_LANGS` (pages limitées à certaines langues),
`PAGE_TEMPLATE` (gabarit partagé) et `NO_SITEMAP` pilotent la liste des pages.

Le `head` de chaque page : `<title>` et `meta description` par page et par langue (`meta` dans
`<langue>.json`), `canonical`, `hreflang` × 7 + `x-default`, Open Graph (titre, description, image = logo
ou photo de la maison, locale), cartes Twitter, icônes, préchargement de la première photo du bandeau,
`referrer` strict, **CSP**, **JSON-LD** `LodgingBusiness` (nom, adresse, GPS, téléphone, e-mail, horaires,
équipements, images, fondateurs, logo, offres 300 / 350 / 300 / 420) + `BreadcrumbList` (hors accueil) ;
bloc `jsonld` par page (`FAQPage` sur la FAQ). Aucun script en ligne : `js/theme.js` (bloquant, minuscule)
puis la feuille de style ; les textes de l'interface vont dans `<script type="application/json" id="ui-strings">`.

## 6. Référencement (plan — carte blanche) — points 1 à 3 faits côté site le 20/10 (sauf redirections 301)

1. **Technique** : un `<title>` unique par page (« Gîtes ruraux à Varsberg, Moselle — Domaine du
   Geisberg »), descriptions de 150 caractères, un seul `<h1>` par page, hiérarchie h2/h3, `alt`
   descriptifs sur toutes les photos, canonical + hreflang, sitemap, robots, pages rapides (déjà :
   webp responsive, ≈ 350 Ko avant photos), HTTPS, 404 propre, redirections 301 des anciennes adresses.
2. **Données structurées** : `LodgingBusiness` enrichi (`priceRange`, `amenityFeature` complets,
   `aggregateRating` à partir des plateformes si on cite la source, `makesOffer` pour les tarifs) ;
   `BreadcrumbList` ; `VideoObject` pour les vidéos ; `FAQPage` sur une page questions fréquentes.
3. **Contenu** : mots-clés naturels dans les titres et premiers paragraphes — gîte Varsberg, gîte Moselle,
   gîte accessible handicap / PMR, gîte près de Saint-Avold, Creutzwald, Sarrebruck, lac de Creutzwald,
   forêt du Warndt, Gîtes de France Moselle. Pages de fond dédiées (partie 3). Page « Questions
   fréquentes » (animaux, bébés, arrivée, caution, accessibilité, week-end). Textes en 7 langues avec
   `hreflang` : visibilité en Allemagne, Luxembourg, Belgique, Pays-Bas.
4. **Local** : fiche Google Business Profile à jour et reliée au site (Marc), même nom / adresse /
   téléphone partout (site, Google, Gîtes de France, Clévacances, Airbnb, Abritel), lien vers le site
   depuis chaque fiche de plateforme et depuis la mairie / l'office de tourisme si possible.
5. **Suivi** : Google Search Console (propriété `domainedugeisberg.fr`, envoi du sitemap) et Bing
   Webmaster, après la bascule ; vérification trimestrielle des liens (déjà automatisée).

## 7. Hébergement, livraison et bascule

- **Site de travail** : GitHub Pages, déployé à chaque push sur `main` (`pages.yml`). Marc relit là.
- **Livraison à DECLIC** : `tools/package.py` produit `livraison/domainedugeisberg-<date>.zip` = contenu
  de `dist/` (HTML des 7 langues, css, js, img, videos, audio, sitemap, robots, `.htaccess`, 404).
  Avant de livrer : `SITE_URL` = `https://www.domainedugeisberg.fr`, retirer le bouton « Notes pour Marc »
  (option `--prod` du build), contrôles de la partie 8.
- **`.htaccess`** (`src/htaccess`, livré en `--prod` ; si DECLIC est sous Apache — à leur demander) :
  redirection HTTP → HTTPS et `domainedugeisberg.fr` → `www`, en-têtes de sécurité (HSTS, `frame-ancestors`,
  `X-Frame-Options`, `nosniff`, `Referrer-Policy`, `Permissions-Policy`, versions masquées), fichiers cachés
  interdits, page 404, cache long pour `img/css/js/fonts` (empreintes dans les URL), compression ; les
  redirections 301 des anciennes adresses du site 2014 y seront ajoutées plus tard (bloc « À COMPLÉTER »).
- **À demander à DECLIC** : type d'hébergement (statique suffit), Apache ou autre, HTTPS (Let's Encrypt),
  un accès FTP/SFTP pour Sébastien (sinon livraison par zip à chaque mise à jour), ne rien couper avant
  le feu vert.
- **Checklist de bascule** : (1) tout `TODO.md` « avant mise en ligne » coché ; (2) Nuitrésa = planning
  de référence, réglages faits, une demande test par Marc ; (3) livraison à DECLIC et mise en ligne ;
  (4) vérifier en ligne : HTTPS, 7 langues, formulaire, calendriers, redirections ; (5) Search Console +
  sitemap ; (6) mettre l'adresse du nouveau site dans Nuitrésa et sur les plateformes ; (7) retirer
  GitHub Pages de l'index (`robots` noindex sur le site de travail) ou le laisser en préproduction.

## 8. Tests et contrôles

- `tools/check.py` : liens internes, fichiers référencés, dimensions des images, poids de l'accueil,
  pages générées seulement. 0 erreur exigé.
- `tests/test_site.py` (Playwright, Chromium, réseau externe coupé, serveur local `python3 -m http.server`
  servant `dist/` sous `/domaine-du-geisberg/`) : contenu et traductions, pages des 7 langues (menu, hreflang,
  CSP, aucun script ni police externe, longueurs titre/description), polices locales, menu et tiroir mobile,
  bandeau, galerie / visionneuse, diaporama, vidéos, cadres Nuitrésa par langue, livre d'or, boutons Réserver,
  notes pour Marc (présence, panneau, absence de secrets), langues, contrastes clair/sombre, FAQ, pages de fond,
  sitemap, 404, redirections, audit d'accessibilité axe-core (WCAG 2.1 A/AA, deux thèmes, FR et DE, zéro
  violation). ≈ 1 040 tests, tous verts.
- `tests/sweep.py` : aucune largeur de 320 à 1366 px ne provoque de défilement horizontal.
- Vérification visuelle dans le navigateur (ordinateur + mobile) après chaque mise en ligne.
- Automatique : liens externes chaque lundi (`liens.yml`, rapport `docs/liens-rapport.md`).

## 8 bis. Sécurité (audit du 20/10)

Règles : aucun secret dans le dépôt public (ni fragment : un test en contenait un du 18 au 20/10 → mot de
passe Nuitrésa à changer par Marc) ; aucun script en ligne ; CSP générée par `build.py` (`default-src 'self'` ;
scripts et cadres : site + `public.nuit-resa.com` + `www.hdmedia.fr` ; styles en ligne tolérés pour les attributs
`style` et la feuille injectée par le widget Nuitrésa ; `object-src 'none'`, `base-uri`, `form-action`,
`upgrade-insecure-requests`) ; polices auto-hébergées (`assets/fonts`, OFL, sous-ensembles latin + latin-ext,
`@font-face` dans `style.css`) ; `.htaccess` (partie 7) ; `tools/package.py` refuse de livrer si une page
manque de CSP, contient un script en ligne, une note, `noindex` ou `github.io`, ou s'il manque `.htaccess`,
`404.html`, `sitemap.xml` ou `fonts/`. Le formulaire Nuitrésa (cadre externe) ne peut pas être filtré par le
site : ses plafonds (1 à 5 personnes, 3 bébés) se règlent dans les fiches de Marc. Ancien site : WordPress 5.3 /
PHP 7.4, extensions à failles connues, pas de HTTPS forcé, Analytics sans consentement → à faire retirer de la ligne par
DECLIC après la bascule, avec une sauvegarde hors ligne (note pour Marc dans `TODO.md` § 4).

## 9. Registre des directives (chronologique)

**Sébastien — règles permanentes** : expliquer avant d'agir sur son Mac ; jamais de suppression sans
double confirmation ; le tenir informé ; messages à son père signés « Biz » ; demander confirmation en
cas de doute ou de contradiction et tenir `CLAUDE.md` à jour.

| Date | Source | Directive |
|---|---|---|
| 18/10 | Marc | Accroche « Au cœur de la nature… » ; 60 m², 4 personnes (2 par chambre) ; distances lac 6, gare 15, piscine 7 ; texte hôtes « Depuis 2007… » ; photos envoyées ; pas de nom pour les gîtes (permutés parfois) ; Bed Booking remplacé par Nuitrésa ; onglet « Visite du gîte » ; incontournables : lac 6, cimetière américain 15, musée des mineurs 31, Völklingen 28, Bliesbruck 61, Pompidou 40 km. |
| 18/10 | Sébastien | Réservation tardive 21 h sur les deux gîtes (seule modification Nuitrésa autorisée) ; ne rien toucher d'autre dans Nuitrésa ; week-ends acceptés ; notes pour Marc exhaustives, y compris les problèmes et la sécurité ; garder le lien vers l'ancien site dans Nuitrésa ; fichiers hors site déplacés sur le Bureau ; aucune demande de réservation test. |
| 18/10 | Sébastien | Le chien s'appelle Urielle. Mails préparés, jamais envoyés par Claude. |
| 19/10 | Marc | Photos des gîtes : ne pas insister sur le lit du salon (exceptionnel) ; 4 personnes ; il corrigera Nuitrésa ; plaque à induction ; pas de surfaces par pièce ; Wi-Fi fibre ; textes « gîtes jumeaux » (2 variantes) ; une page disponibilité avec les deux gîtes ; « Agnès et Marc vous accueillent » en accueil, puis photos de la maison et des gîtes ; Nuitrésa référence début 2027 ou à la bascule. |
| 19/10 | Sébastien | Hébergement : analyse GitHub ; code ouvert envisagé (contenus protégés) ; surfaces par pièce retirées ; visite 360° conservée ; mails à Marc et au prestataire préparés (devenus caducs le 20/10 pour le domaine). |
| 20/10 | Marc | Accueil : photo Agnès-Marc-Urielle ≈ 4 s puis maison, puis photos + description des gîtes sur la même page, équipements possibles sur la même page ; induction ; OK 5 entrées (à voir monté) ; 4 personnes + 1 appoint 90 cm (chauffeuse) ; plus d'équitation, chevaux à la retraite ; grille tarifaire (300/350/300/420) ; page Avis inchangée ; rester chez DECLIC (facturé jusqu'au 30/11/2027), bascule faite par DECLIC ; inclus : lits faits, charges, ménage de finition (logement rendu propre), serviettes non fournies ; référencement : carte blanche, plusieurs pages si utile ; utiliser le logo. |
| 20/10 | Sébastien (soir) | Calendriers uniquement sur Réservation ; notes pour Marc alimentées par `TODO.md` (référence unique, « au bon endroit ») ; vérifier toutes les langues et la qualité des traductions ; vérifier modes sombre et clair ; bandeau : partir de loin puis zoomer, zoom + déplacement, 4 s fixes sur la photo des hôtes, parallaxe légère (3D) ; pas de licence ; caution 300 € (repli ancien site) ; accent bordeaux ; pas de mail à Marc pour l'instant ; référencement côté site seulement ; redirections et mail DECLIC plus tard. |
| 20/10 | Sébastien | Retirer la photo de nuit de la maison (mur sali) ; on garde l'hébergeur, on fournit le site, DECLIC le met en ligne ; GitHub reste le site de travail ; un gîte doit être réservable pour une personne seule ; `CLAUDE.md` = source de vérité, `TODO.md`, plan complet, structure de code claire et réutilisable ; demander confirmation avant de corriger une directive contredite. |
| 20/10 | Sébastien (nuit) | Les 60 personnes / 12 bébés du formulaire viennent de Nuitrésa : limiter à 5 personnes et 3 bébés par gîte (réglage des fiches par Marc) ; audit complet de la sécurité du site ; mettre en avant les failles de l'ancien site dans les notes pour Marc si elles sont plus critiques (pour accélérer la bascule) ; l'adresse e-mail de Sébastien reste en clair dans le pied de page ; mentions légales : l'hébergeur affiché est DECLIC, jamais GitHub ; questions à poser à DECLIC (hébergeur, mention, collaboration). |
