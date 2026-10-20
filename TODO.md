# TODO — ce qu'il reste à faire

Mis à jour le 20/10/2026. Cocher au fur et à mesure ; une ligne terminée reste cochée (historique).
Règles et décisions : `CLAUDE.md`. Plan complet : `docs/PLAN-DU-SITE.md`.

## 0. À confirmer par Sébastien (avant de commencer la v2)

- [ ] **Accueil = page de présentation** (hôtes → maison → gîtes → fiche → tiroir équipement → Réserver) et
      plus de page « Les gîtes » séparée. Alternative : garder « Les gîtes » et un accueil court.
- [x] Calendriers des deux gîtes sur la page Réservation, au-dessus du formulaire (20/10).
- [x] Texte « gîtes jumeaux » : « Deux gîtes identiques. Réservez l'un des deux, ou les deux pour un groupe. » (20/10).
- [x] Couchage d'appoint : une ligne discrète dans la fiche (20/10).
- [x] Caution : 300 € (ancien site) ; règle générale : ce qui n'est pas dans les directives de Marc vient de l'ancien site (20/10).
- [x] Couleurs : accent aligné sur le bordeaux du logo (20/10).
- [x] Licence : aucune — tout « tous droits réservés » (20/10).
- [ ] Menu : « Le domaine & alentours » et « Photos & vidéos » comme noms d'entrées.

## 1. Sauvegarde et structure (étape 1)

- [x] Sauvegarde du site v1 avant toute modification (20/10) : archive `SiteDomaineDuGeisberg-v1-2026-10-20.tar.gz`
      sur le Bureau (104 Mo, sans .git ni vidéos sources), tag git local `v1-2026-10-20` et branche GitHub
      `sauvegarde-v1-2026-10-20` (commit 9b48899).
- [ ] Nouvelle structure (`src/`, `assets/`, `tools/`, `tests/`, `dist/`) — voir plan, partie 4.
- [ ] `build.py` : sortie dans `dist/`, option `--prod` (sans notes, `SITE_URL` définitif), `.htaccess`, 404.
- [ ] `pages.yml` : construire puis déployer `dist/` ; lancer `check.py` et les tests avant de déployer.
- [ ] `tools/package.py` : zip de livraison pour DECLIC.
- [ ] Tests rapatriés dans `tests/` et documentés dans le README.

## 2. Contenu et pages (étape 2 — v2)

- [ ] Logo intégré : en-tête, favicon, pied de page, image de partage (Open Graph), JSON-LD `logo`.
- [ ] Retirer la photo de nuit de la maison sous la neige partout (bandeau, diaporama, OG, JSON-LD).
- [ ] Bandeau d'accueil : photo d'Agnès, Marc et Urielle en premier (≈ 4 s), puis la maison.
- [ ] Accueil restructuré selon la décision 0.1 ; une seule fiche ; tiroir « Tout l'équipement » ;
      « Inclus / non fourni » ; un seul avis ; aperçus des autres pages.
- [ ] Supprimer les doublons : tarifs (Réservation seulement), bloc hôtes (Accueil seulement), services
      inclus (un seul endroit), logos des labels (Avis + pied de page), surfaces par pièce (supprimées).
- [ ] Capacité : « de 1 à 4 personnes » ; appoint discret selon 0.4 ; induction ; Wi-Fi fibre ; plus
      d'équitation (chevaux à la retraite) ; texte « gîtes identiques ».
- [ ] Tarifs : nouvelle grille (300 / 350 / 300 / 420) + conditions d'arrivée + inclus / non fourni.
- [ ] Page Réservation : calendriers + tarifs + formulaire + accès ; page Avis inchangée.
- [ ] Page « Photos & vidéos » à trois onglets (diaporama, vidéos, visite 360°) ; redirections des
      anciennes pages (gites, diaporama, videos, visite, autour, gite-1, gite-2).
- [ ] « Le domaine & alentours » : fusion, texte du domaine à relire (garder / raccourcir), distances.
- [ ] Nouvelles photos envoyées par Marc : trier, intégrer (gîtes, maison en été, séjour).
- [ ] Traductions des nouveaux textes dans les 6 autres langues.
- [ ] Notes pour Marc refaites page par page (toujours exhaustives, vue d'ensemble sur l'accueil).
- [ ] Tests mis à jour ; balayage ; vérification visuelle ; mise en ligne sur GitHub.
      **Pas de mail à Marc pour l'instant** (on le laisse tranquille — Sébastien, 20/10) : Sébastien lui
      montrera la v2 quand il le décidera.

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

## 4. Côté Marc (à lui rappeler, aussi dans les notes du site)

- [ ] Nuitrésa : capacité mini 1 (réservable pour une personne seule), nuits minimum 2 + grille par durée,
      bébés, caution, TVA (comptable), photos et descriptif des fiches.
- [ ] Nuitrésa : relier Stripe/PayPal si paiement en ligne souhaité ; une demande test à son nom, puis la refuser.
- [ ] Retirer le mot de passe Nuitrésa du document Word et le changer.
- [ ] Choisir l'avis mis en avant sur l'accueil ; valider les titres des vidéos ; tarifs par saison ?
- [ ] Consigne d'arrivée (clés, stationnement) ; confirmer zoo, Sainte-Croix, boucle de la Sarre.
- [ ] Demander à DECLIC : type d'hébergement, Apache / HTTPS, accès FTP pour Sébastien, ne rien couper
      avant le feu vert.
- [ ] Nuitrésa doit être le planning de référence avant la bascule.

## 5. Avant la mise en ligne définitive (étape 4)

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
