# Domaine du Geisberg — site des gîtes

Site des deux gîtes du Domaine du Geisberg (Marc et Agnès Nadler), 6 rue du Geisberg, 57880 Varsberg (Moselle).

- Site en ligne (maquette) : https://sebastiennadler.github.io/domaine-du-geisberg/
- Adresse définitive prévue : https://www.domainedugeisberg.fr/
- Développement : Sébastien Nadler

Le site est **entièrement statique** : pas de base de données, pas de serveur à maintenir. Les pages HTML sont
générées par un petit script Python à partir de textes (JSON) et de modèles (templates), puis publiées par
GitHub Pages. Le calendrier des disponibilités se met à jour tout seul, toutes les heures.

## Organisation du dépôt

```
.
├── index.html, gites.html, …    pages françaises GÉNÉRÉES (ne pas modifier à la main)
├── en/ de/ es/ pt/ nl/ zh/       mêmes pages dans les six autres langues (générées)
├── gite-1.html, gite-2.html      anciennes adresses : renvoient vers gites.html (générées aussi)
├── sitemap.xml, robots.txt       générés aussi
├── css/style.css                 la feuille de styles (couleurs, mise en page, mobile, thème sombre)
├── js/site.js                    les scripts (menu, thème, bandeau, galerie, calendrier, formulaire, notes)
├── img/                          photos WebP GÉNÉRÉES par tools/photos.py : hero/, domaine/, gites/, videos/
│                                 (affiches), plus autour/ et logos/ (taille unique)
├── videos/                       vidéos MP4 GÉNÉRÉES par tools/videos.py
├── photos-sources/               photos d'origine (JPEG/PNG) : c'est ici qu'on dépose une nouvelle photo
├── videos-sources/               vidéos d'origine (.MOV, non versionnées : trop lourdes)
├── audio/chants-oiseaux.mp3      fond sonore du diaporama (libre de droits, voir crédits)
├── tools/
│   ├── build.py                  génère toutes les pages  →  python3 tools/build.py
│   ├── photos.py / photos.json   catalogue des photos → WebP en plusieurs tailles + images.json
│   ├── videos.py / videos.json   catalogue des vidéos → MP4 légers + affiches
│   ├── check.py                  vérifie le site généré (liens, images, attributs, poids)
│   ├── templates/                modèles Jinja2 (un par page + base.html commun)
│   ├── content/
│   │   ├── shared.json           données communes à toutes les langues : adresse, téléphones, tarifs,
│   │   │                         listes de photos (identifiants du catalogue), sites à visiter, avis…
│   │   ├── images.json           dimensions et tailles de chaque photo (écrit par photos.py, ne pas éditer)
│   │   ├── fr.json … zh.json     tous les TEXTES, une langue par fichier (le français sert de repli)
│   │   └── busy.json             périodes réservées (écrit automatiquement, ne pas éditer)
│   ├── credits.json              attributions des photos et de l'audio récupérés sur Wikimedia Commons
│   ├── fetch_ical.py             lit les calendriers iCal (Bed Booking…) → busy.json
│   ├── fetch_commons.py          cherche des photos libres (lac, village, forêt…) sur Wikimedia Commons
│   ├── fetch_audio.py            cherche un enregistrement libre de chants d'oiseaux
│   └── liens-candidats.txt       liens supplémentaires à tester par le vérificateur de liens
├── docs/                         documents pour Marc : guide PDF, étude des plateformes, rapport des liens
├── ancien-site/                  archive de l'ancien site (images d'origine, scripts de récupération)
└── .github/workflows/            automatisations GitHub Actions (voir plus bas)
```

## Modifier le site

### 1. Changer un texte

Les textes sont dans `tools/content/<langue>.json`. Chaque fichier a la même structure :

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
| `reservation` | page Réservation et formulaire de contact                               |
| `visite`      | page Visite 3D                                                          |
| `diapo`       | page Diaporama                                                          |
| `legal`       | mentions légales et crédits                                             |
| `notes`       | (français seulement) les « Notes pour Marc » du mode annotation         |

Une clé absente dans une langue reprend automatiquement la valeur française.

Ce qui est commun à toutes les langues (téléphones, e-mail, tarifs, surface, capacité, listes de photos,
sites à visiter avec leurs liens, avis, notes des plateformes) est dans `tools/content/shared.json`.

### 2. Ajouter ou remplacer des photos

1. Déposer la photo d'origine (JPEG ou PNG, telle que sortie de l'appareil) dans `photos-sources/`, avec un
   nom parlant : `terrasse-ete.jpeg`.
2. L'inscrire au catalogue `tools/photos.json` : un identifiant (`"gites/terrasse-ete"` → le dossier et le
   nom dans `img/`), le fichier source, et éventuellement les largeurs à produire (par défaut 1600 et 800 px ;
   1920 / 1280 / 800 pour le bandeau d'accueil) ou `"pos"`, le point de la photo à garder visible quand elle
   est recadrée (`"42% 72%"`).
3. `python3 tools/photos.py` : écrit les WebP dans `img/` (sans les métadonnées de l'appareil) et note
   leurs dimensions dans `images.json`.
4. Ajouter l'identifiant dans la liste voulue de `shared.json` (`hero`, `domaine`, `gites`, `gites_home`,
   `around_gallery`, `site_imgs`, `hosts_photo`) et sa légende, au même rang, dans chaque `<langue>.json`
   (`home.hero_alts`, `domaine.captions`, `gites.captions`, `autour.gallery_caps`).
5. Régénérer (étape 4).

Dans les gabarits, une photo s'affiche avec `{{ pic('gites/terrasse-ete', légende, tailles) }}`, qui écrit
la balise `<img>` complète (plusieurs tailles au choix du navigateur, dimensions réservées, chargement
différé) ; `src(id)` donne l'adresse de la plus grande version (visionneuse, fond de bandeau).

### 3. Ajouter une vidéo

1. Déposer le fichier d'origine dans `videos-sources/` (dossier non versionné : garder une copie ailleurs).
2. L'inscrire dans `tools/videos.json` : identifiant, fichier, hauteur maximale (720 par défaut), instant de
   l'affiche en secondes.
3. `python3 tools/videos.py` (nécessite ffmpeg : `brew install ffmpeg`) : écrit un MP4 léger dans `videos/`
   et son affiche dans `photos-sources/` ; puis `python3 tools/photos.py` pour l'affiche en WebP.
4. Ajouter la vidéo dans `shared.json` (`videos`) et son titre + sa description dans `videos.clips` de chaque
   `<langue>.json`, au même rang.

### 4. Régénérer et vérifier les pages

```sh
pip install jinja2 pillow   # une seule fois
python3 tools/build.py      # écrit les 70 pages (+ 14 renvois), le sitemap et robots.txt
python3 tools/check.py      # liens et images cassés, images inutilisées, attributs manquants, poids
```

Ouvrir ensuite `index.html` dans un navigateur pour vérifier. Les pages HTML du dépôt sont des fichiers générés :
toute modification faite directement dedans sera écrasée au prochain `build.py`.

### 5. Publier

```sh
git add -A
git commit -m "Description du changement"
git push
```

L'action « Publier sur GitHub Pages » se lance toute seule et le site est à jour en une à deux minutes.
Les fichiers CSS et JS portent une empreinte (`style.css?v=…`) calculée à chaque génération, donc les
navigateurs rechargent toujours la dernière version.

## Automatisations (GitHub Actions)

| Workflow               | Déclenchement          | Rôle                                                                      |
|------------------------|------------------------|---------------------------------------------------------------------------|
| `pages.yml`            | à chaque `push`        | publie le dépôt sur GitHub Pages                                          |
| `calendrier.yml`       | toutes les heures      | lit les flux iCal, réécrit `busy.json`, régénère et republie si changement |
| `liens.yml`            | chaque lundi           | teste tous les liens externes → `docs/liens-rapport.md`                   |
| `photos-commons.yml`   | à la demande           | récupère des photos libres sur Wikimedia Commons (`tools/fetch_commons.py`) |
| `audio-commons.yml`    | à la demande           | récupère un enregistrement libre de chants d'oiseaux (`tools/fetch_audio.py`) |

### Calendrier des disponibilités

Les adresses des flux iCal (Airbnb, Bed Booking, Gîtes de France…) sont des **secrets** du dépôt
(`Settings → Secrets and variables → Actions`) : `ICAL_GITE1` et `ICAL_GITE2`, plusieurs adresses possibles
séparées par des virgules. Elles n'apparaissent jamais dans le code. Seules les plages de dates occupées sont
conservées dans `busy.json` : aucun nom de client, aucun lien.

Pour forcer une mise à jour immédiate : onglet *Actions* → « Mettre à jour le calendrier » → *Run workflow*.

### Formulaire de contact

Le formulaire de la page Réservation envoie les messages à l'adresse des gîtes via le service FormSubmit
(sans serveur). À la première utilisation, FormSubmit envoie un e-mail de confirmation à activer une seule fois.
Si l'envoi échoue, le site ouvre le logiciel de messagerie du visiteur avec le message pré-rempli.

## Mode « Notes pour Marc »

Sur les pages françaises, un petit bouton en bas à droite affiche des bulles numérotées : ce qu'il reste à
fournir ou à décider (photos récentes, tarifs, accès OVH…). Les textes sont dans la clé `notes` de `fr.json`.
Ce mode est invisible tant que l'on n'appuie pas sur le bouton ; il sera retiré à la mise en ligne définitive.

## Mise en ligne définitive (liste de contrôle)

1. Dans `tools/templates/base.html`, retirer la balise `<meta name="robots" content="noindex, nofollow">`
   et la balise `Cache-Control` (toutes deux marquées « maquette »).
2. Retirer le bouton et le script du mode notes (`base.html`, bloc `{% if lang == 'fr' %}` en bas de page).
3. Faire pointer le domaine `domainedugeisberg.fr` vers GitHub Pages (fichier `CNAME` + réglage DNS chez
   l'hébergeur du domaine), puis activer *Enforce HTTPS* dans `Settings → Pages`.
4. Régénérer, publier, puis déclarer le sitemap dans Google Search Console.

Le détail, écrit pour Marc, est dans `docs/Guide-site-Domaine-du-Geisberg.pdf`.

## Choix techniques (robustesse et vitesse)

- Site statique, sans base de données ni dépendance JavaScript externe : rien à mettre à jour, rien qui casse.
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
  `tools/credits.json` et sur la page Mentions légales.
- Polices : Playfair Display et Nunito Sans (Google Fonts).
