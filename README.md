# Domaine du Geisberg — site des gîtes

> **Où est quoi ?** `CLAUDE.md` = les règles et décisions du projet (source de vérité, lu par Claude Code à
> chaque session) · `docs/PLAN-DU-SITE.md` = le plan complet du site et de quoi le recréer de zéro ·
> `TODO.md` = ce qu'il reste à faire · ce `README.md` = la documentation technique : comment modifier un
> texte ou une photo, régénérer, vérifier, publier.

Site des deux gîtes du Domaine du Geisberg (Marc et Agnès Nadler), 6 rue du Geisberg, 57880 Varsberg (Moselle).

- Site en ligne (maquette) : https://sebastiennadler.github.io/domaine-du-geisberg/
- Adresse définitive prévue : https://www.domainedugeisberg.fr/
- Développement : Sébastien Nadler

Le site est **entièrement statique** : pas de base de données, pas de serveur à maintenir. Les pages HTML sont
générées par un petit script Python à partir de textes (JSON) et de modèles (templates), puis publiées par
GitHub Pages. Les disponibilités et la réservation en ligne sont assurées par le widget Nuitrésa (le
prestataire de Marc), intégré dans la page Réservation.

## Organisation du dépôt

```
.
├── CLAUDE.md                     règles et décisions du projet (source de vérité)
├── TODO.md                       ce qu'il reste à faire, dont les points à demander à Marc
├── README.md                     ce document
├── docs/                         PLAN-DU-SITE.md (plan complet), guide PDF, étude des plateformes, rapport des liens
├── src/                          TOUT ce que l'on modifie à la main
│   ├── content/
│   │   ├── shared.json           données communes à toutes les langues : adresse, téléphones, tarifs,
│   │   │                         listes de photos (identifiants du catalogue), sites à visiter, avis, Nuitrésa…
│   │   ├── fr.json … zh.json     tous les TEXTES, une langue par fichier (le français sert de repli)
│   │   └── images.json           dimensions et tailles de chaque photo (écrit par photos.py, ne pas éditer)
│   ├── templates/
│   │   ├── base.html             squelette commun (head, en-tête, pied de page, notes, scripts)
│   │   ├── pages/                un gabarit Jinja2 par page (index, reservation, le-domaine, medias, avis, mentions-legales,
│   │   │                         questions = FAQ, landing.html = les trois pages de fond, 404.html)
│   │   └── partials/             morceaux réutilisés (_macros.html : notes ; _diapo.html : diaporama ; _redirect.html)
│   ├── catalog/                  photos.json, videos.json (catalogues), credits.json, liens-candidats.txt
│   ├── css/style.css             la feuille de styles (polices locales, couleurs, mise en page, mobile, thème sombre)
│   ├── js/site.js                les scripts (menu, thème, bandeau, galerie, onglets, notes, calendriers, effets)
│   ├── js/theme.js               minuscule, chargé en premier : applique le thème mémorisé avant l'affichage
│   └── htaccess                  réglages Apache livrés à l'hébergeur (HTTPS forcé, en-têtes de sécurité, cache, 404)
├── assets/
│   ├── photos-sources/           photos d'origine (JPEG/PNG) : c'est ici qu'on dépose une nouvelle photo ; logo/
│   ├── img/                      photos WebP GÉNÉRÉES par tools/photos.py (suivies par git)
│   ├── fonts/                    polices Playfair Display et Nunito Sans (WOFF2, licence OFL) servies par le site
│   ├── videos-sources/           vidéos d'origine (.MOV, non versionnées : trop lourdes)
│   ├── videos/                   vidéos MP4 GÉNÉRÉES par tools/videos.py
│   └── audio/                    fond sonore du diaporama (libre de droits, voir crédits)
├── tools/
│   ├── build.py                  génère le site dans dist/  →  python3 tools/build.py  (ou --prod)
│   ├── check.py                  vérifie dist/ (liens, images, attributs, poids)
│   ├── package.py                livraison pour l'hébergeur : build --prod + check + zip dans livraison/
│   ├── photos.py / videos.py     photos → WebP en plusieurs tailles ; vidéos → MP4 légers + affiches
│   └── fetch_commons.py, fetch_audio.py   médias libres (Wikimedia Commons)
├── tests/                        test_site.py (fonctionnel), sweep.py (débordements), run.sh (les deux)
├── dist/                         le site GÉNÉRÉ (non suivi par git) : ce qui est publié et livré
├── livraison/                    archives zip pour l'hébergeur (non suivi)
├── ancien-site/                  copie de l'ancien site (textes, photos) pour référence
└── .github/workflows/            pages.yml (construit, teste, publie dist/), liens.yml (liens externes, le lundi),
                                  photos-commons.yml, audio-commons.yml
```

Règle d'or : on ne modifie que `src/`, `assets/photos-sources/`, `tools/` et les documents ; `dist/` est
régénéré à chaque fois et n'est jamais retouché à la main.

## Modifier le site

### 1. Changer un texte

Les textes sont dans `src/content/<langue>.json`. Chaque fichier a la même structure :

| Clé           | Contenu                                                                 |
|---------------|-------------------------------------------------------------------------|
| `meta`        | titre et description de chaque page (référencement Google)              |
| `nav`, `ui`   | libellés du menu, boutons, pied de page                                 |
| `home`        | page d'accueil (accroche, légendes du bandeau, bloc « Agnès et Marc vous accueillent ») |
| `domaine`     | page Le domaine (textes et légendes des photos)                         |
| `gites`       | page Les gîtes (équipements, chambres, légendes des photos)             |
| `videos`      | page Vidéos (titres et descriptions des vidéos)                         |
| `autour`      | page Aux alentours                                                      |
| `extra`       | avis, infos pratiques, labels                                           |
| `reservation` | page Réservation (tarifs, textes autour du widget Nuitrésa, accès)      |
| `visite`      | page Visite 3D                                                          |
| `diapo`       | page Diaporama                                                          |
| `legal`       | mentions légales et crédits                                             |
| `notes`       | (français seulement) les « Notes pour Marc » du mode annotation         |

Une clé absente dans une langue reprend automatiquement la valeur française.

Ce qui est commun à toutes les langues (téléphones, e-mail, tarifs, surface, capacité, listes de photos,
sites à visiter avec leurs liens, avis, notes des plateformes) est dans `src/content/shared.json`.

### 2. Ajouter ou remplacer des photos

1. Déposer la photo d'origine (JPEG ou PNG, telle que sortie de l'appareil) dans `assets/photos-sources/`, avec un
   nom parlant : `terrasse-ete.jpeg`.
2. L'inscrire au catalogue `src/catalog/photos.json` : un identifiant (`"gites/terrasse-ete"` → le dossier et le
   nom dans `assets/img/`), le fichier source, et éventuellement les largeurs à produire (par défaut 1600 et 800 px ;
   1920 / 1280 / 800 pour le bandeau d'accueil) ou `"pos"`, le point de la photo à garder visible quand elle
   est recadrée (`"42% 72%"`).
3. `python3 tools/photos.py` : écrit les WebP dans `assets/img/` (sans les métadonnées de l'appareil) et note
   leurs dimensions dans `images.json`.
4. Ajouter l'identifiant dans la liste voulue de `shared.json` (`hero`, `domaine`, `gites`, `gites_home`,
   `around_gallery`, `site_imgs`, `hosts_photo`) et sa légende, au même rang, dans chaque `<langue>.json`
   (`home.hero_alts`, `domaine.captions`, `gites.captions`, `autour.gallery_caps`).
5. Régénérer (étape 4).

Dans les gabarits, une photo s'affiche avec `{{ pic('gites/terrasse-ete', légende, tailles) }}`, qui écrit
la balise `<img>` complète (plusieurs tailles au choix du navigateur, dimensions réservées, chargement
différé) ; `src(id)` donne l'adresse de la plus grande version (visionneuse, fond de bandeau).

### 3. Ajouter une vidéo

1. Déposer le fichier d'origine dans `assets/videos-sources/` (dossier non versionné : garder une copie ailleurs).
2. L'inscrire dans `src/catalog/videos.json` : identifiant, fichier, hauteur maximale (720 par défaut), instant de
   l'affiche en secondes.
3. `python3 tools/videos.py` (nécessite ffmpeg : `brew install ffmpeg`) : écrit un MP4 léger dans `assets/videos/`
   et son affiche dans `assets/photos-sources/` ; puis `python3 tools/photos.py` pour l'affiche en WebP.
4. Ajouter la vidéo dans `shared.json` (`videos`) et son titre + sa description dans `videos.clips` de chaque
   `<langue>.json`, au même rang.

### 4. Régénérer et vérifier les pages

```sh
pip install jinja2 pillow playwright && playwright install chromium   # une seule fois
python3 tools/build.py      # écrit dist/ : 58 pages (+ 49 renvois), 404, css, js, polices, img, vidéos, sitemap, robots
python3 tools/check.py      # liens et images cassés, images inutilisées, attributs manquants, poids
bash tests/run.sh           # tests fonctionnels (≈ 1 000) + balayage des débordements, contre dist/
```

Pour regarder le résultat : `python3 -m http.server 8111 --directory dist` puis ouvrir `http://127.0.0.1:8111/`
(seule la page 404, aux liens absolus, suppose le préfixe `/domaine-du-geisberg/` du site de travail).
`dist/` est entièrement régénéré à chaque `build.py` : toute modification faite dedans est perdue.
`python3 tools/build.py --prod` produit la version à livrer : sans le mode « Notes pour Marc », `robots.txt`
ouvert, liens de la 404 à la racine, et `.htaccess` (copie de `src/htaccess`).

### 5. Publier

```sh
git add -A
git commit -m "Description du changement"
git push
```

L'action « Construire, tester et publier » se lance toute seule : elle génère `dist/`, lance `check.py` et les
tests, et ne publie que si tout est vert. Le site de travail est à jour en trois à cinq minutes.
Pour l'hébergeur définitif (DECLIC) : `python3 tools/package.py` crée `livraison/domainedugeisberg-<date>.zip`,
à lui transmettre ; il dépose son contenu à la racine du site. Le script refuse de livrer s'il reste une trace
du site de travail (notes, `noindex`, `github.io`), un script en ligne, une page sans CSP, ou s'il manque
`.htaccess`, `404.html`, `sitemap.xml` ou les polices.
Les fichiers CSS et JS portent une empreinte (`style.css?v=…`) calculée à chaque génération, donc les
navigateurs rechargent toujours la dernière version.

## Automatisations (GitHub Actions)

| Workflow               | Déclenchement          | Rôle                                                                      |
|------------------------|------------------------|---------------------------------------------------------------------------|
| `pages.yml`            | à chaque `push`        | publie le dépôt sur GitHub Pages                                          |
| `liens.yml`            | chaque lundi           | teste tous les liens externes → `docs/liens-rapport.md`                   |
| `photos-commons.yml`   | à la demande           | récupère des photos libres sur Wikimedia Commons (`tools/fetch_commons.py`) |
| `audio-commons.yml`    | à la demande           | récupère un enregistrement libre de chants d'oiseaux (`tools/fetch_audio.py`) |

### Tests automatiques (`tests/`)

- `bash tests/run.sh` lance un serveur local qui sert `dist/` sous `/domaine-du-geisberg/` (comme GitHub
  Pages) puis les deux scripts ; `bash tests/run.sh tests` ou `bash tests/run.sh sweep` pour l'un seulement.
  Les deux renvoient un code d'erreur en cas d'échec (c'est ce qui bloque la publication dans le workflow GitHub).
- `tests/test_site.py` : tests fonctionnels Playwright (Chromium), réseau externe coupé (≈ 1 000 tests) :
  contenu et traductions, chaque page dans chaque langue (menu, hreflang, CSP, aucun script ni police externe,
  longueur des titres et descriptions), accueil, réservation, En images, avis, notes, langues, contrastes
  clair/sombre, FAQ (données structurées), pages de fond, sitemap, 404.
- `tests/sweep.py` : balayage de toutes les pages de 320 à 1366 px ; ne doit signaler aucun débordement.
- Prérequis : `pip install playwright && playwright install chromium`.

### Disponibilités et réservation (Nuitrésa)

Tout vient de l'espace Nuitrésa de Marc (Outils → Formulaires pour site web → Codes à intégrer) ; les valeurs
sont dans `src/content/shared.json` : `nuitresa_key` (clé publique), `nuitresa_script`, `nuitresa_public`
(adresse des cadres) et `nuitresa_rooms` (identifiant Nuitrésa et nom de chaque gîte : 1100 et 1101).

- **Page Les gîtes, section « Disponibilités »** : un calendrier public par gîte (cadre
  `calendrier-multiple-<id>-<clé>.html`, 2 mois, flèches pour avancer), vert = libre, rouge = occupé. Il reflète
  le planning Nuitrésa, réservations des plateformes comprises. Le cadre envoie sa hauteur par `postMessage`
  et `src/js/site.js` l'ajuste (uniquement depuis l'origine `public.nuit-resa.com`). Chargement différé.
- **Page Réservation** : le formulaire Nuitrésa (`data-nr-version="v2"`), avec l'option « estimation globale des
  disponibilités » (`data-nr-aggregate-availability="1"`) qui colore en rouge, dans son calendrier, les dates où
  les deux gîtes sont pris. Choix du gîte, coordonnées et confirmation sont gérés côté Nuitrésa ; le site
  n'héberge aucune donnée client. Capacité, nuits minimum, acompte et dates fermées sont les réglages des fiches
  Nuitrésa (menu Hébergements), pas du site.
- **Page Avis** : le livre d'or public (`avis-<clé>.html`), alimenté par le questionnaire de satisfaction que
  Nuitrésa envoie après chaque séjour.

La langue des cadres et du formulaire suit celle de la page (FR, EN, DE, ES ; anglais pour les autres). Pour
changer de clé, d'identifiants de gîtes ou de version du script, modifier `shared.json` et régénérer.

### Contact

Les coordonnées (téléphones, e-mail, adresse) sont dans `shared.json` et apparaissent sur l'accueil, la page
Réservation et le pied de page. Il n'y a plus de formulaire maison : une question passe par e-mail ou téléphone,
une réservation par le widget.

## Mode « Notes pour Marc »

Sur les pages françaises, un petit bouton en bas à droite affiche des bulles numérotées : ce qu'il reste à
fournir ou à décider. Les textes viennent de `TODO.md` (sections « À demander à Marc » et « À faire par Marc
dans Nuitrésa ») : une ligne `- [ ] {clé} texte` s'affiche à l'endroit de la page qui porte `note('clé')`.
Ce mode est invisible tant que l'on n'appuie pas sur le bouton ; la version à livrer (`--prod`) ne le contient pas.

## Mise en ligne définitive (liste de contrôle)

1. `TODO.md`, section « Avant la mise en ligne définitive » : tout coché.
2. `python3 tools/package.py` : version sans notes, vérifiée, archivée dans `livraison/`.
3. Transmettre l'archive à DECLIC (hébergeur conservé), qui la dépose sur `domainedugeisberg.fr`.
4. Vérifier en ligne (HTTPS, 7 langues, formulaire, calendriers), puis déclarer le sitemap dans Google
   Search Console et mettre l'adresse du site dans Nuitrésa et sur les plateformes.

Le détail, écrit pour Marc, est dans `docs/Guide-site-Domaine-du-Geisberg.pdf`.

## Sécurité

- Site statique : aucun formulaire ni donnée personnelle traités ici (la réservation est un cadre Nuitrésa,
  sur leur domaine) ; aucun secret dans le dépôt (la clé Nuitrésa est publique par nature).
- Chaque page porte une **politique de sécurité de contenu** (`<meta http-equiv="Content-Security-Policy">`,
  générée par `build.py`) : scripts et cadres limités au site, à `public.nuit-resa.com` et à `www.hdmedia.fr` ;
  aucun script en ligne (les textes passés aux scripts sont dans un bloc `application/json`). Pour ajouter un
  service externe, il faut l'inscrire dans la CSP (`build.py`) et le justifier.
- Polices servies par le site (`assets/fonts`, WOFF2, licence OFL) : aucune requête vers Google.
- `src/htaccess` (dans le zip de livraison) : HTTPS forcé et `www` canonique, HSTS, `frame-ancestors` /
  `X-Frame-Options`, `nosniff`, `Referrer-Policy`, `Permissions-Policy`, versions masquées, fichiers cachés
  interdits, page 404, compression et cache. GitHub Pages ne permet pas ces en-têtes : le site de travail n'a
  que la CSP en `<meta>`.
- Scripts : `site.js` n'écoute les messages (`postMessage`) que de l'origine Nuitrésa et ne redimensionne que
  les cadres des calendriers ; les liens externes portent `rel="noopener"`.
- Après la mise en ligne : vérifier les en-têtes sur securityheaders.com / observatory.mozilla.org et le
  certificat sur ssllabs.com ; faire supprimer l'ancien WordPress par l'hébergeur.

## Choix techniques (robustesse et vitesse)

- Site statique, sans base de données ni dépendance JavaScript externe (hormis les cadres Nuitrésa : calendriers
  sur Les gîtes, formulaire sur Réservation, livre d'or sur Avis — chargés à la demande) : rien à mettre à jour,
  rien qui casse.
- Chaque photo existe en plusieurs tailles (`srcset`) et porte ses dimensions : un téléphone ne télécharge
  pas la version 1920 px, et la page ne « saute » pas pendant le chargement. La première photo du bandeau
  est préchargée ; toutes les autres se chargent à la demande.
- Vidéos en H.264 + AAC (lisibles partout), débit plafonné, `preload="none"` : une vidéo ne pèse sur la page
  que si on la lance.
- Effets (fondu entre les photos du bandeau avec zoom lent, apparition des sections au défilement) en CSS,
  désactivés si le visiteur a choisi « réduire les animations » ; sans JavaScript, tout reste visible.
- `tools/check.py` détecte avant publication un lien ou une image cassés.

## Crédits

- Photos et vidéos du domaine et des gîtes : Marc et Agnès Nadler (et photos publiées sur Gîtes de France,
  Clévacances).
- Photos d'illustration des environs et fond sonore : Wikimedia Commons, auteurs et licences listés dans
  `src/catalog/credits.json` et sur la page Mentions légales.
- Polices : Playfair Display et Nunito Sans (SIL Open Font License, servies par le site — `assets/fonts/LICENCE-POLICES.txt`).
