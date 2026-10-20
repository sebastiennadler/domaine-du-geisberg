# TODO — ce qu'il reste à faire

Mis à jour le 20/10/2026. Cocher au fur et à mesure ; une ligne terminée reste cochée (historique).
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
- [ ] Resynchroniser le dossier du Mac avec GitHub (autorisation de suppression : 1re confirmation reçue le 20/10, 2e à obtenir).

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

## 3. Référencement (étape 3) — seulement ce qui se fait de notre côté, pour préparer le terrain

- [ ] Titres et descriptions par page et par langue, un `<h1>` par page, `alt` sur toutes les photos.
- [ ] JSON-LD enrichi (`priceRange`, offres, équipements, `aggregateRating` sourcé), fil d'Ariane,
      `VideoObject`, `FAQPage`.
- [ ] Page « Questions fréquentes » ; pages de fond : gîte accessible PMR Moselle, lac de Creutzwald,
      entre Saint-Avold et Sarrebruck (textes à faire valider par Marc).
- [ ] Page 404.
- [ ] **Plus tard** (pas dans l'étape 3 — Sébastien, 20/10) : redirections 301 des adresses de l'ancien
      site (liste dans `ancien-site/`), `.htaccess` définitif.
- [ ] Après bascule : Search Console + sitemap, Bing, fiche Google Business (Marc), lien vers le site
      depuis Gîtes de France, Clévacances, Airbnb, Abritel.

## 4. À demander à Marc (questions ouvertes — Sébastien lui transmet quand il le décide)

Chaque ligne commence par `{clé}` : la clé désigne l'endroit du site où la question s'affiche en mode
« Notes pour Marc » (accueil : hero, h1, facts, gites, fiche, equip, review, hosts, todo · réservation : dispo,
prices, included, widget, access · domaine : domaine_txt, domaine_gal, around, around_gal, leisure, links ·
médias : diapo, videos, visite · avis : ratings, reviews, labels, platforms, guestbook · mentions : legal).
Sans clé, la ligne va dans la vue d'ensemble de l'accueil.

- [ ] {hero} Le bandeau commence par votre photo (4 s), puis la maison depuis la prairie, les chevaux au soir, le coucher de soleil. Cet ordre vous convient-il ? Avez-vous une photo récente de la façade en été ?
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
- [ ] {labels} Labels affichés : Gîtes de France, Clévacances, Tourisme & Handicap — toujours valables ?
- [ ] {guestbook} Livre d'or Nuitrésa : vide tant que les questionnaires de satisfaction ne sont pas revenus (3 à envoyer). Le cacher en attendant ?
- [ ] {legal} Qui a créé le logo (Synchro, 2014 ?) pour le créditer dans les mentions légales ? SIRET et forme juridique à vérifier.
- [ ] Photos : une photo du séjour et une de la façade en été seraient bienvenues.

## 5. À faire par Marc dans Nuitrésa

- [ ] Capacité mini = 1 sur les deux fiches (aujourd'hui 4 : une personne seule ou un couple ne peut pas réserver). Capacité maxi 5 (4 + appoint).
- [ ] Nuits minimum = 2, et la grille par durée : 2 nuits 300 €, 3 nuits 350 €, 4 nuits 300 €, 5 à 7 nuits 420 € (arrivée le vendredi pour les week-ends ; 4 nuits minimum en semaine).
- [ ] Bébés : combien en plus des 5 personnes ; régler « Bébés acceptés » et « Gestion de la capacité ».
- [ ] Caution : 300 € (0 € aujourd'hui) ; TVA 10 % à vérifier avec le comptable.
- [ ] Photos et descriptif des fiches (le descriptif dit « 4/5 personnes » et « vitrocéramique »).
- [ ] Relier Stripe ou PayPal si le paiement en ligne est souhaité ; puis une seule demande test à votre nom, à refuser ensuite.
- [ ] Retirer le mot de passe du document Word envoyé par e-mail et le changer dans Nuitrésa.
- [ ] Nuitrésa doit être le planning de référence avant la bascule ; l'adresse du site sera changée dans les fiches à ce moment-là.

## 6. Avant la mise en ligne définitive (étape 4)

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
