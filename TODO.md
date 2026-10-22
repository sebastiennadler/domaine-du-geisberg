# TODO — ce qu'il reste à faire

Mis à jour le 20/10/2026 (soir). Cocher au fur et à mesure ; une ligne terminée reste cochée (historique).
Règles et décisions : `CLAUDE.md`. Plan complet : `docs/PLAN-DU-SITE.md`.

## 0. À confirmer par Sébastien (avant de commencer la v2)

- [x] Accueil = page de présentation, plus de page « Les gîtes » séparée (20/10).
- [x] Calendriers des deux gîtes sur la page Réservation, au-dessus du formulaire (20/10).
- [x] Texte « gîtes jumeaux » : « Deux gîtes identiques. Réservez l'un des deux, ou les deux pour un groupe. » (20/10).
- [x] Couchage d'appoint : une ligne discrète dans la fiche (20/10).
- [x] Caution : 300 € (ancien site) ; règle générale : ce qui n'est pas dans les directives de Marc vient de l'ancien site (20/10).
- [x] Couleurs : accent aligné sur le bordeaux du logo (20/10).
- [x] Licence : aucune — tout « tous droits réservés » (20/10).
- [x] Menu : « Le domaine & alentours » et « En images » (20/10 ; à revoir sur la maquette si besoin).
- [x] Bandeau d'accueil : inclinaison 3D à la souris, à l'essai, avec interrupteur pour revenir en arrière (20/10).

## 1. Sauvegarde et structure (étape 1)

- [x] Sauvegarde du site v1 avant toute modification (20/10) : archive `SiteDomaineDuGeisberg-v1-2026-10-20.tar.gz`
      sur le Bureau (104 Mo, sans .git ni vidéos sources), tag git local `v1-2026-10-20` et branche GitHub
      `sauvegarde-v1-2026-10-20` (commit 9b48899).
- [x] Nouvelle structure (`src/`, `assets/`, `tools/`, `tests/`, `dist/`) — pages générées identiques à la v1 (20/10).
- [x] `build.py` : sortie dans `dist/`, option `--prod` (sans notes) (20/10). `.htaccess` et 404 : étape 3 / plus tard.
- [x] `pages.yml` : construit, vérifie (`check.py`), teste (`tests/run.sh`) puis déploie `dist/` (20/10).
- [x] `tools/package.py` : zip de livraison pour DECLIC dans `livraison/` (20/10).
- [x] Tests dans `tests/` (`run.sh`, codes de retour) et documentés dans le README (20/10).
- [x] Resynchroniser le dossier du Mac avec GitHub (autorisation de suppression accordée le 20/10 pour ce dossier).

## 2. Contenu et pages (étape 2 — v2) — fait le 20/10, en ligne sur le site de travail

- [x] Logo intégré (recadré, version pour le mode sombre, favicon, icône Apple, JSON-LD `logo`).
- [x] Photo de nuit retirée partout ; chambre à deux lits ajoutée ; photo des hôtes en tête du bandeau.
- [x] Bandeau : 4 s fixes sur les hôtes puis zoom + déplacement (départ de loin), durée par photo,
      inclinaison à la souris et parallaxe avec interrupteurs `hero_tilt` / `hero_parallax` (`shared.json`).
- [x] Calendriers Nuitrésa uniquement sur Réservation ; bouton « Diaporama » sur le bandeau qui ouvre le
      diaporama complet en superposition (même composant que la page En images).
- [x] Notes pour Marc alimentées par `TODO.md` (clés de page), textes `notes` retirés de `fr.json`.
- [x] Accueil = page de présentation : chiffres clés, galerie 8 photos, fiche unique, tiroir équipement,
      un avis, hôtes et coordonnées, aperçus. Doublons supprimés (tarifs, hôtes, inclus, labels, surfaces).
- [x] Capacité « de 1 à 4 personnes », appoint discret, induction, Wi-Fi fibre, chevaux à la retraite,
      « Deux gîtes identiques ».
- [x] Réservation : calendriers, grille 300 / 350 / 300 / 420, inclus / non fourni, formulaire, accès.
- [x] « En images » à trois onglets ; « Le domaine & alentours » fusionnée ; 7 redirections.
- [x] Traductions des 6 langues faites et relues ; test « aucune clé ne retombe sur le français ».
- [x] Modes clair et sombre vérifiés page par page (test de contraste ≥ 4,5:1).
- [x] 543 tests verts, balayage sans débordement, mise en ligne sur GitHub. Pas de mail à Marc.
- [ ] Photos envoyées par Marc (séjour, façade en été) : à intégrer quand elles arrivent.
- [ ] Vérifier les effets du bandeau (zoom, inclinaison, parallaxe) sur un vrai écran ; garder ou non
      l'inclinaison (`hero_tilt` dans `shared.json`, une ligne).

## 3. Référencement (étape 3) — seulement ce qui se fait de notre côté, pour préparer le terrain — fait le 20/10

- [x] Titres (≤ 70 caractères) et descriptions (≤ 160) par page et par langue, un `<h1>` par page, `alt`
      sur toutes les photos ; cartes Twitter ; test automatique des longueurs.
- [x] JSON-LD enrichi : `LodgingBusiness` (logo, offres 300 / 350 / 300 / 420, équipements), fil d'Ariane
      (`BreadcrumbList`), `FAQPage`. `aggregateRating` et `VideoObject` : non ajoutés (les notes des
      plateformes doivent d'abord être rafraîchies et sourcées — § 4 `{ratings}`).
- [x] Page « Questions fréquentes » (12 questions, 7 langues) ; pages de fond en FR, EN, DE : gîte accessible
      PMR Moselle, lac de Creutzwald, entre Saint-Avold et Sarrebruck (textes à faire valider par Marc,
      § 4 `{landing}` et `{faq}`) ; liens en pied de page.
- [x] Page 404 (liens absolus, non indexée) ; sitemap avec les versions linguistiques (`xhtml:link`) ;
      `robots.txt` : interdit sur le site de travail, ouvert dans la version livrée.
- [ ] **Plus tard** (pas dans l'étape 3 — Sébastien, 20/10) : redirections 301 des adresses de l'ancien
      site (liste dans `ancien-site/`) — l'emplacement est prêt dans `src/htaccess` (bloc « À COMPLÉTER »).
- [ ] Après bascule : Search Console + sitemap, Bing, fiche Google Business (Marc), lien vers le site
      depuis Gîtes de France, Clévacances, Airbnb, Abritel.

## 3 bis. Sécurité (audit du 20/10, demandé par Sébastien) — corrections faites le 20/10

- [x] Fragment du mot de passe Nuitrésa retiré du test `tests/test_site.py` (il y figurait depuis le 18/10,
      donc dans l'historique git public — d'où le changement de mot de passe obligatoire, § 5).
- [x] Polices auto-hébergées (`assets/fonts`, licence OFL) : plus aucun appel à Google Fonts (RGPD, vitesse).
- [x] Politique de sécurité de contenu (CSP) en `<meta>` sur chaque page, aucun script en ligne
      (`theme.js`, bloc JSON pour les textes de l'interface, onglets dans `site.js`) ; `referrer` strict.
- [x] `src/htaccess` livré dans le zip : HTTPS forcé + www, HSTS, `frame-ancestors`, `X-Frame-Options`,
      `nosniff`, `Referrer-Policy`, `Permissions-Policy`, versions masquées, fichiers cachés interdits,
      page 404, compression, cache.
- [x] Garde-fous de `tools/package.py` : refus de livrer si notes, `noindex`, `github.io`, script en ligne,
      page sans CSP, ou `.htaccess` / 404 / sitemap / polices manquants.
- [x] Tests : CSP sur chaque page, aucun script ni police externe (hors Nuitrésa), polices servies par le site.
- [ ] Décision Sébastien : réécrire l'historique git pour effacer le fragment de mot de passe (force-push ;
      casse les clones existants) — ou s'en tenir au changement de mot de passe.
- [ ] Optionnel : épingler les actions GitHub sur un SHA ; `sandbox` sur les cadres des calendriers Nuitrésa.
- [ ] Après la bascule : vérifier en ligne les en-têtes (securityheaders.com, observatory.mozilla.org) et
      le HTTPS (ssllabs.com) ; demander à DECLIC de **retirer l'ancien WordPress de la ligne** (fichiers,
      base, extensions) en **gardant une sauvegarde** (archive hors ligne — Sébastien, 20/10) : le laisser en
      ligne, même sans lien, reste une porte d'entrée.

## 4. À demander à Marc (questions ouvertes — Sébastien lui transmet quand il le décide)

Chaque ligne commence par `{clé}` : la clé désigne l'endroit du site où la question s'affiche en mode
« Notes pour Marc » (accueil : hero, h1, facts, gites, fiche, equip, review, hosts, todo · réservation : dispo,
prices, included, widget, access · domaine : domaine_txt, domaine_gal, around, around_gal, leisure, links ·
médias : diapo, videos, visite · avis : ratings, reviews, labels, platforms, guestbook · mentions : legal).
Sans clé, la ligne va dans la vue d'ensemble de l'accueil.

- [ ] {hero} Le bandeau commence par votre photo (7 s) avec « Agnès et Marc vous accueillent » (fait le 22/10), puis la maison depuis la prairie, les chevaux au soir, le coucher de soleil avec l'accroche des gîtes. Cet ordre vous convient-il ? Avez-vous une photo récente de la façade en été ?
- [ ] {facts} Le site affiche « de 1 à 4 personnes » (couchage d'appoint mentionné discrètement dans la fiche). D'accord ?
- [ ] {gites} 8 photos communes aux deux gîtes, dont la chambre à deux lits. Manque une photo récente du séjour ; les photos envoyées le 18/10 sont-elles toutes intégrées ?
- [ ] {fiche} Fiche de l'essentiel : vérifiez chaque ligne (induction, Wi-Fi fibre, horaires 16 h / 10 h, 2 animaux maximum, boulangerie 300 m, restaurant 1 km, supérette 3 km).
- [ ] {review} Quel avis mettre en avant sur l'accueil (parmi les six de la page Avis) ? Celui de Nicolas est affiché en attendant.
- [ ] {hosts} Votre texte « Depuis 2007 » est en place avec la photo d'Agnès, Marc et Urielle. Coordonnées affichées : Marc 07 89 56 74 91, Agnès 06 73 42 05 89, gitevarsberg@hotmail.com — à vérifier.
- [ ] {prices} Tarifs : 300 € (week-end 2 nuits), 350 € (3 nuits), 300 € (4 nuits en semaine), 420 € (5 à 7 nuits), d'après vos réponses du 20/10. Y a-t-il des tarifs par saison (Noël, été) ? Montant de la taxe de séjour ? Caution : chèque à l'arrivée ou empreinte bancaire via Nuitrésa ?
- [ ] {included} Inclus / non fourni : lits faits, charges, ménage de finition offert (gîte rendu propre), serviettes de bain non fournies. Exact ?
- [ ] {access} Itinéraire correct ? Une consigne d'arrivée (clés, stationnement) à ajouter ?
- [ ] {domaine_txt} Texte « Le domaine » repris de l'ancien site, dernier paragraphe adapté (plus d'équitation, chevaux à la retraite). Garder, raccourcir, réécrire ?
- [ ] {around} Distances : zoo d'Amnéville 55 km, Sainte-Croix 60 km, boucle de la Sarre 80 km restent à confirmer. Vos 4 incontournables ?
- [ ] {links} Liens utiles repris de l'ancien site : lesquels garder ? Ajouter la mairie de Varsberg et l'office de tourisme ?
- [ ] {videos} Titres des trois vidéos à valider. D'autres vidéos (drone, saisons, intérieur) ?
- [ ] {visite} La visite virtuelle date de 2015 : on la garde, comme convenu. Prévoir de nouvelles photos à 360° un jour ?
- [ ] {ratings} Notes des plateformes relevées le 18/10 (à rafraîchir avant la mise en ligne). La mention Airbnb doit-elle être retirée ?
- [ ] {labels} Labels affichés : Gîtes de France, Clévacances, Tourisme & Handicap — toujours valables ? Comme demandé (22/10), plus aucun lien vers ces sites ni vers Airbnb / Abritel : les logos et les notes restent, sans lien. Faut-il aussi retirer les liens vers les sites touristiques (page Le domaine & alentours : lac, Völklingen, offices de tourisme…) ? Pour l'instant ils restent, ouverts dans la même fenêtre.
- [ ] {guestbook} Livre d'or Nuitrésa : vide tant que les questionnaires de satisfaction ne sont pas revenus (3 à envoyer). Le cacher en attendant ?
- [ ] {legal} Qui a créé le logo (Synchro, 2014 ?) pour le créditer dans les mentions légales ? SIRET et forme juridique à vérifier. L'hébergeur affiché est DECLIC : ses coordonnées exactes sont à obtenir (voir section 6).
- [ ] {faq} Page « Questions fréquentes » : 12 réponses écrites d'après vos directives et l'ancien site (animaux, bébés, horaires, caution 300 €, acompte 25 %, Wi-Fi, commerces). À relire et corriger.
- [ ] {landing} Trois pages de fond pour Google (gîte accessible PMR, lac de Creutzwald, entre Saint-Avold et Sarrebruck), en français, anglais et allemand : à relire ; signalez toute inexactitude (distances, activités, labels).
- [ ] Photos : une photo du séjour et une de la façade en été seraient bienvenues.
- [ ] DECLIC : Sébastien n'a pas leur adresse ; il vous a envoyé la liste des points à voir avec votre ami (coordonnées pour les mentions légales, type d'hébergement, accès pour les mises à jour, sauvegarde puis retrait de l'ancien site à la bascule, collaboration possible). À vous de lui écrire à votre façon, avec Sébastien en destinataire direct pour les réponses techniques.
- [ ] Sécurité de l'ancien site (constaté le 20/10, en lecture seule) : WordPress 5.3 de 2019 avec PHP 7.4 (plus aucun correctif de sécurité depuis novembre 2022), extensions anciennes à failles connues (Slider Revolution 5.4, Contact Form 7 5.1, Photo Gallery 1.5), pas de HTTPS forcé, aucun en-tête de sécurité, Google Analytics sans bandeau de consentement (RGPD). C'est le type de site le plus visé par les piratages automatiques : une raison de plus pour basculer vite, puis de faire retirer l'ancien site de la ligne par DECLIC (en gardant une sauvegarde). Le nouveau site, statique, n'a aucune de ces faiblesses.

## 5. À faire par Marc dans Nuitrésa

- [ ] Capacité de chaque gîte : **mini 1, maxi 5** (aujourd'hui mini 4 : une personne seule ou un couple ne peut pas réserver). Le formulaire lit ces valeurs dans vos fiches : au-delà de 5 personnes il refusera lui-même (« Capacité acceptée : de 1 à 5 »). Rien à régler côté site (Sébastien, 20/10).
- [ ] Bébés : **3 maximum par gîte**, en plus des 5 personnes (« Bébés acceptés » = 3, « hors capacité ») — le champ bébés du formulaire se limitera alors à 3 (Sébastien, 20/10).
- [ ] Nuits minimum = 2, et la grille par durée : 2 nuits 300 €, 3 nuits 350 €, 4 nuits 300 €, 5 à 7 nuits 420 € (arrivée le vendredi pour les week-ends ; 4 nuits minimum en semaine).
- [ ] Caution : 300 € (0 € aujourd'hui) ; TVA 10 % à vérifier avec le comptable.
- [ ] Photos et descriptif des fiches (le descriptif dit « 4/5 personnes » et « vitrocéramique »).
- [ ] Relier Stripe ou PayPal si le paiement en ligne est souhaité ; puis une seule demande test à votre nom, à refuser ensuite.
- [ ] **Changer le mot de passe Nuitrésa** (Configuration → Mon compte) et le retirer du document Word envoyé par e-mail : obligatoire, il a circulé par mail et un fragment s'est retrouvé dans le dépôt public du site (retiré le 20/10, mais l'historique le garde). Ne jamais transmettre un mot de passe par mail ou dans un document.
- [ ] Nuitrésa doit être le planning de référence avant la bascule ; l'adresse du site sera changée dans les fiches à ce moment-là.

## 6. À demander à DECLIC (l'entreprise de l'ami de Marc, qui hébergera le site)

- [ ] Quelle société et quel hébergeur exactement (raison sociale, adresse, téléphone) pour les mentions légales
      « Hébergement » — le site dit « DECLIC (coordonnées à compléter) » en attendant.
- [ ] Souhaitent-ils être mentionnés pour la mise en ligne / le déploiement du site (pied de page ou mentions légales) ?
- [ ] Type d'hébergement (statique suffit), Apache ou autre, HTTPS, accès FTP/SFTP pour Sébastien ; ne rien
      couper avant le feu vert.
- [ ] Le `.htaccess` livré (HTTPS forcé, en-têtes de sécurité, cache, 404) est-il pris en compte
      (`AllowOverride`, modules `rewrite`, `headers`, `expires`, `deflate`) ? Le certificat HTTPS couvre-t-il
      `domainedugeisberg.fr` et `www.` ? (HSTS n'est à activer qu'à cette condition.)
- [ ] À la bascule : retirer l'ancien WordPress de la ligne (fichiers, base de données, PHP) en en gardant une
      sauvegarde hors ligne (archive) — voir § 3 bis.
- [ ] Sébastien n'a pas l'adresse de DECLIC : le mail de questions passe par Marc, qui le fait suivre à son ami
      (points envoyés à Marc le 20/10 ; il rédige lui-même).
- [ ] Bouteille à la mer : Sébastien aimerait proposer ses services (développement, sites, automatisation)
      pour des missions ponctuelles — à glisser dans le mail de livraison ou dans un mail séparé.

## 7. Avant la mise en ligne définitive (étape 4)

- [ ] `build.py --prod` ; `check.py` 0 erreur ; tests verts ; balayage ; relecture des 7 langues.
- [ ] `tools/package.py` → zip ; livraison à DECLIC ; mise en ligne par DECLIC ; vérification en ligne
      (HTTPS, langues, formulaire, calendriers, redirections, 404).
- [ ] **Plus tard** : le mail à DECLIC pour la livraison (Sébastien, 20/10) — pas avant que le site soit prêt.
- [ ] Adresse du nouveau site dans Nuitrésa (fiches des gîtes) et sur les plateformes.
- [ ] Site de travail GitHub : `noindex` ou conservation en préproduction (décider).
- [ ] Mettre à jour `docs/PLAN-DU-SITE.md` (registre) et archiver la v2 (tag `v2-<date>`).

## Fait

- [x] 18/10 — Nuitrésa intégré (calendriers par gîte, formulaire avec estimation globale, livre d'or) ;
      réservation tardive 21 h ; notes pour Marc exhaustives ; 495 tests ; Urielle dans les légendes.
- [x] 19/10 — Mails préparés (notes, nom de domaine — caduc, plan de simplification) ; SMS calendriers.
- [x] 20/10 — Réponses de Marc intégrées dans `CLAUDE.md` et `docs/PLAN-DU-SITE.md` ; `TODO.md` créé.
- [x] 20/10 — Étape 1 (structure) et étape 2 (v2 du contenu) en ligne sur le site de travail.
- [x] 20/10 — Étape 3 (référencement côté site : titres, descriptions, JSON-LD, FAQ, 3 pages de fond, 404,
      sitemap) et audit de sécurité (CSP, polices locales, `.htaccess`, garde-fous de livraison).
