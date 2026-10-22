# CLAUDE.md — Directives du projet (source de vérité)

Ce fichier est lu automatiquement par Claude Code au début de chaque session de travail sur ce dépôt.
C'est la **référence unique** des règles et des décisions du projet : en cas de conflit avec un autre
document, c'est ce fichier qui fait foi, et c'est ici qu'on met à jour une décision.

- `README.md` : documentation technique (comment modifier, régénérer, publier).
- `docs/PLAN-DU-SITE.md` : plan complet du site, instructions pour le recréer de zéro, registre daté des directives.
- `TODO.md` : tout ce qu'il reste à faire, par priorité.

**Règle n° 1 — en cas de contradiction ou de doute, demander avant de corriger.** Si une nouvelle demande
contredit une directive ci-dessous, le signaler explicitement (« ceci contredit la directive X du … »),
demander confirmation à Sébastien, puis mettre ce fichier à jour. Les points marqués **[À CONFIRMER]**
sont des interprétations en attente de validation.

---

## 1. Le projet

- Refonte du site des gîtes des parents de Sébastien, **Marc et Agnès Nadler** : *Domaine du Geisberg*,
  6 rue du Geisberg, 57880 Varsberg (Moselle). Deux gîtes identiques de 60 m², 4 personnes, accessibles PMR.
- Ancien site : `http://www.domainedugeisberg.fr`, réalisé et hébergé par **DECLIC** (société d'un ami de Marc).
  Hébergement déjà facturé jusqu'au **30/11/2027**.
- Rôles : **Sébastien** = développeur, décideur technique, seul interlocuteur de Claude ;
  **Marc** = propriétaire, valide les contenus, règle Nuitrésa ; **Claude** = exécute, documente, alerte.
- **Site de travail** : GitHub Pages — `https://sebastiennadler.github.io/domaine-du-geisberg/`
  (dépôt `sebastiennadler/domaine-du-geisberg`). C'est là que Marc relit et valide.
- **Mentions légales** : l'hébergeur affiché est **DECLIC** (jamais GitHub, qui n'est que le site de travail) ;
  ses coordonnées exactes et sa mention éventuelle pour le déploiement sont à lui demander (`TODO.md` § 6).
  Sébastien souhaite aussi lui proposer ses services (missions ponctuelles) — à mentionner dans le mail.
- **Mise en ligne définitive** : l'hébergeur actuel (DECLIC) est conservé. Sébastien lui **fournit le site**
  (dossier de fichiers statiques) et DECLIC le met en ligne sur `domainedugeisberg.fr`. **Pas de transfert
  de nom de domaine** ni de changement d'hébergeur pour l'instant (« plus tard on verra »).
- Objectif de bascule : **entre fin novembre et fin décembre 2026**. Nuitrésa devient le planning de
  référence de Marc au plus tard à la bascule (début 2027 sinon).

## 2. Règles de travail (demandées par Sébastien)

### Sur son ordinateur et sur le dépôt
- **Expliquer avant d'agir** sur son Mac et obtenir sa permission ; le tenir régulièrement informé de
  l'avancement ; le prévenir quand une tâche est interrompue.
- **Ne jamais supprimer** un fichier ou un dossier sur son Mac sans **double confirmation explicite**.
  À défaut : déplacer (sur le Bureau, ou dans `_to_delete/`).
- **Dépôt** : la branche `main` sur GitHub est la référence ; Claude travaille dans son clone cloud, commite
  et pousse (messages de commit en français). Le dossier du Mac (`~/Desktop/SiteDomaineDuGeisberg`) est une
  copie de travail à resynchroniser (`git pull`) — ce qui exige l'autorisation de supprimer des fichiers dans
  ce dossier (git l'exige pour ses verrous et pour remplacer des fichiers) : à demander avec la double
  confirmation. Tant qu'elle n'est pas accordée, les fichiers sont recopiés dans le dossier sans git.
- Un changement important se fait sur une **branche** (`etape-N-…`), fusionnée dans `main` seulement quand
  `check.py` et les tests sont verts : le site de travail n'est jamais cassé.
- Les fichiers sans rapport avec le site ne restent pas dans le dossier du site (déplacés sur le Bureau).
- Outils ponctuels (scripts de migration) : dans `archives/outils-ponctuels/` (non suivi par git).
- **Sauvegarde avant toute série de modifications importantes** : archive `.tar.gz` du dossier sur le
  Bureau + branche `sauvegarde-<version>-<date>` sur GitHub (les tags ne passent pas par le proxy).
  Sauvegarde v1 faite le 20/10 : `SiteDomaineDuGeisberg-v1-2026-10-20.tar.gz`, branche `sauvegarde-v1-2026-10-20`.

### Nuitrésa (compte de Marc — identifiants transmis par Sébastien)
- **Ne JAMAIS envoyer de demande de réservation**, test ou non, par le formulaire Nuitrésa. La seule
  demande test sera faite par Marc, à son nom, une seule fois, puis refusée par lui.
- **Ne RIEN modifier dans le compte Nuitrésa** sans accord explicite de Sébastien. Seule modification
  autorisée et faite (18/10) : « réservation tardive » = le jour J jusqu'à 21 h, pour les deux gîtes.
  Tout le reste (capacité, nuits minimum, tarifs, caution, TVA, photos…) est **à faire par Marc** ; le site
  se contente de le signaler dans les notes.
- Laisser le lien vers **l'ancien site** dans les fiches Nuitrésa jusqu'à la bascule.
- Le **mot de passe** Nuitrésa ne doit apparaître nulle part (notes, dépôt, docs, messages, **tests**) — pas
  même un fragment : un test en contenait un du 18 au 20/10 (dépôt public, historique conservé), d'où le
  changement de mot de passe rendu obligatoire pour Marc (`TODO.md` § 5). Se déconnecter de Nuitrésa en fin
  de session.
- Le formulaire Nuitrésa est un cadre d'un autre domaine : le site ne peut pas filtrer ses champs (personnes,
  bébés). Les plafonds viennent des fiches de Marc (`capacity_min/max`, `babies_max`) : **1 à 5 personnes,
  3 bébés** par gîte, à régler par Marc (Sébastien, 20/10).

### Sécurité (audit du 20/10, règles permanentes)
- **Aucun secret dans le dépôt** (public) : ni mot de passe, ni fragment, ni jeton ; les seules valeurs
  présentes sont publiques par nature (clé Nuitrésa, coordonnées des gîtes, adresse de Sébastien — qu'il a
  choisi de laisser en clair dans le pied de page, 20/10).
- **Aucun script en ligne** dans les gabarits : tout script est un fichier de `src/js/` (ou le chargeur
  Nuitrésa) ; les données passent par des blocs `application/json`. La **CSP** générée par `build.py`
  (balise `<meta>`) n'autorise que le site, `public.nuit-resa.com` et `hdmedia.fr` ; tout nouveau service
  externe doit y être ajouté (et justifié). `tools/package.py` refuse de livrer sinon.
- **Polices auto-hébergées** (`assets/fonts`, OFL) : jamais de Google Fonts ni d'autre ressource tierce qui
  transmettrait l'adresse des visiteurs (RGPD) ; pas de statistiques (Analytics) sans décision explicite et
  bandeau de consentement.
- `src/htaccess` (livré dans `dist/.htaccess` par `--prod`) porte HTTPS forcé, HSTS, `frame-ancestors`, etc. ;
  les redirections de l'ancien site y seront ajoutées plus tard (bloc « À COMPLÉTER »).
- Ancien site (WordPress 5.3 / PHP 7.4, extensions à failles connues, pas de HTTPS forcé, Analytics sans
  consentement) : constats consignés dans `TODO.md` § 4 (note pour Marc) ; à faire **retirer de la ligne** par
  DECLIC après la bascule, **en gardant une sauvegarde** hors ligne (Sébastien, 20/10).

### Qualité, avant toute mise en ligne (GitHub ou DECLIC)
- `python3 tools/build.py` puis `python3 tools/check.py` : **0 erreur**.
- `bash tests/run.sh` : tests Playwright (`tests/test_site.py`) tous verts, balayage des débordements
  (`tests/sweep.py`) de 320 à 1366 px sans débordement ; vérification visuelle dans le navigateur
  (ordinateur et mobile). Le workflow GitHub refait ces contrôles et ne publie que s'ils passent.
- **Toutes les langues** : chaque page vérifiée dans les 7 langues ; les 6 traductions relues pour être
  irréprochables (naturelles, idiomatiques, cohérentes avec le français validé) ; un test signale toute clé
  qui retombe sur le français par oubli (Sébastien, 20/10).
- **Mode sombre et mode clair** : vérifiés page par page (captures dans les deux modes, contrastes du texte,
  des boutons, des cadres Nuitrésa et du logo) (Sébastien, 20/10).
- **Accessibilité** : audit axe-core (WCAG 2.1 A/AA) intégré aux tests, zéro violation exigée ; `alt` sur
  toutes les images, structure sémantique, clavier, contrastes ≥ 4,5:1 dans les deux thèmes (Sébastien, 20/10).
- Rien ne part en ligne sans ces contrôles.

### Communication
- Messages rédigés pour Sébastien à son père : tutoiement, « Papa », signature **« Biz »** (jamais
  « Je t'embrasse »). Mails à des tiers : vouvoiement, sauf indication.
- Tout ce qui est dit à Marc par mail à propos du site doit **aussi** figurer dans les notes du site.
- Ne pas envoyer de mail à la place de Sébastien : préparer le texte, il envoie.
- Quand Marc doit écrire à un tiers (DECLIC…), **ne jamais lui dicter le texte** : lui donner les points à
  aborder et le laisser rédiger à sa façon (Sébastien, 20/10).
- **Pas de nouveau mail à Marc pour l'instant** (20/10) : on le laisse tranquille jusqu'à ce que Sébastien
  décide de lui montrer la v2. Les notes du site continuent d'être tenues à jour. Exception décidée par
  Sébastien le 20/10 (soir) : un court mail à Marc contenant le texte à faire suivre à DECLIC (Sébastien n'a
  pas l'adresse de l'entreprise).
- Étape référencement : seulement ce qui se fait côté site maintenant (préparer le terrain) ; les
  redirections de l'ancien site et le mail de livraison à DECLIC sont pour plus tard (20/10). Fait le 20/10 :
  titres/descriptions, JSON-LD (offres, fil d'Ariane, FAQ), page Questions fréquentes (7 langues), trois pages
  de fond (FR/EN/DE), 404, sitemap multilingue.
- Mettre en avant les failles de l'ancien site dans les notes pour Marc, si elles sont plus critiques que
  celles du nouveau — pour accélérer la bascule (Sébastien, 20/10).

## 3. Notes pour Marc (mode « Notes ») et TODO.md

- **`TODO.md` est la référence unique** de ce qu'il reste à faire (décidé le 20/10), avec deux sections
  dédiées à Marc : « À demander à Marc » (questions ouvertes) et « À faire par Marc dans Nuitrésa ».
- Le mode « Notes pour Marc » du site (bouton en bas à droite, **en français seulement**, inactif par
  défaut, pastilles numérotées sur les éléments concernés + panneau récapitulatif) **affiche les points du
  TODO, au bon endroit de la page** : à partir de l'étape 2, chaque point de la section « À demander à
  Marc » porte une étiquette de page/élément et `build.py` les injecte dans les gabarits — plus de textes
  de notes en double dans `fr.json`. Jusque-là, les notes existantes (`src/content/fr.json` → `notes`)
  restent telles quelles.
- La version à livrer (`build.py --prod`) ne contient pas ce mode.

## 4. Décisions de contenu validées (par Marc, sauf mention)

### Identité
- **Logo officiel** fourni le 20/10 (maison dessinée, bordeaux et verts, « Domaine du Geisberg — Gîtes
  ruraux Varsberg ») : **à utiliser**, « sans abuser, mais à mettre en avant » — en-tête, favicon, pied de
  page, image de partage. Source : `assets/photos-sources/logo/logo-geisberg.png` (recadré et version pour
  le mode sombre à côté). **Crédit du créateur du logo** : inconnu (l'ancien site ne crédite que Synchro,
  2014, pour l'hébergement) — question posée à Marc dans `TODO.md`, à publier dans les mentions légales
  dès qu'on le sait (Sébastien, 20/10).
- Accroche : **« Au cœur de la nature, deux gîtes d'exception à proximité immédiate de la forêt »**.
- Texte des hôtes « Depuis 2007, année d'ouverture de nos gîtes… » (texte de Marc, 18/10), avec la photo
  d'Agnès, Marc et **Urielle** (la chienne, une malinoise). Les chevaux sont **à la retraite** : il n'y a
  **plus d'équitation** sur place.
- **Pas de nom pour les gîtes** (Marc les permute parfois) : « Gîte 1 » et « Gîte 2 », comme dans
  Nuitrésa. Les photos sont communes et ne doivent pas différencier les gîtes.

### Les gîtes
- 60 m², 2 chambres (2 lits de 90 × 190 chacune), salle d'eau accessible (douche à l'italienne, WC),
  séjour avec cuisine intégrée, terrasse privée. **Capacité affichée : 4 personnes.**
- Couchage d'appoint : 1 chauffeuse convertible (90 cm) dans le salon, **à ne pas mettre en avant**
  (« doit rester exceptionnel ») : **une seule ligne discrète dans la fiche** (validé 20/10), jamais dans
  les chiffres clés.
- **Un gîte doit pouvoir être réservé même pour une personne seule** (Sébastien, 20/10) : la capacité
  affichée (4) est un maximum, pas un minimum. Le site le dit (« de 1 à 4 personnes ») et Nuitrésa sera
  réglé ensuite par Marc : réservable de **1 à 5 personnes** (bébés en plus, à discuter).
- Équipements : **plaque à induction** (pas vitrocéramique), four, micro-ondes, lave-vaisselle, lave-linge,
  congélateur, téléviseur écran plat, **Wi-Fi fibre**, chauffage au sol par géothermie, salon de jardin,
  barbecue, équipement bébé (lit, baignoire, chaise haute sur demande), VTT à disposition, parking privé,
  animaux acceptés (2 maximum, sans supplément), gîte non fumeur.
- **Pas de surfaces par pièce** (« n'apporte rien ») : supprimées, pas même dans un tiroir.
- Les équipements **peuvent rester sur la même page** que les photos et la description.
- Inclus dans le prix : **lits faits à l'arrivée**, draps fournis, **toutes charges incluses** (électricité,
  eau, chauffage au sol), **ménage de finition offert** (le logement est rendu propre : vaisselle lavée et
  rangée), **serviettes de bain NON fournies**.
- Texte « gîtes jumeaux » (validé par Sébastien le 20/10) : **« Deux gîtes identiques. Réservez l'un des
  deux, ou les deux pour un groupe. »**
- Horaires : arrivée à partir de 16 h, départ avant 10 h (comme dans Nuitrésa).

### Tarifs (Marc, 20/10) — par gîte
| Séjour | Conditions | Prix |
|---|---|---|
| Week-end, 2 nuits | arrivée vendredi (vendredi + samedi) | 300 € |
| Week-end, 3 nuits | arrivée vendredi (vendredi + samedi + dimanche) | 350 € |
| Semaine, 4 nuits | arrivée dimanche, lundi, mardi, mercredi ou jeudi ; **minimum 4 nuits hors week-end** | 300 € |
| 5, 6 ou 7 nuits | — | 420 € |

- Acompte : 25 % (Nuitrésa). Taxe de séjour en sus. CB, Visa, MasterCard, chèques-vacances ANCV.
- Caution : **300 €** (information de l'ancien site, retenue le 20/10 faute de directive de Marc) ;
  Nuitrésa est à 0 € — Marc choisit le moyen (chèque à l'arrivée ou empreinte bancaire via Nuitrésa).
- Le site affiche cette grille ; c'est Marc qui la reporte dans Nuitrésa (prix selon la durée).

### Pages et structure
- **Menu à 5 entrées** : Accueil · Réservation · Le domaine & alentours · **En images** · Avis, plus le
  bouton Réserver. « En images » (décidé 20/10) remplace « Photos & vidéos » pour inclure la visite 360°.
- **Accueil** : d'abord la photo d'Agnès, Marc et Urielle (environ 4 secondes, « à voir »), puis les photos
  de la maison, puis les **photos et la description des gîtes sur la même page** ; les équipements peuvent
  y rester. → **Validé par Sébastien le 20/10** : l'accueil devient la page de présentation
  (hôtes → maison → gîtes → fiche → tiroir « Tout l'équipement » → bouton Réserver) et il n'y a plus de
  page « Les gîtes » séparée (`gites.html` redirige vers l'accueil).
- **Disponibilités** : les deux calendriers (un par gîte) sur la page **Réservation**, au-dessus du
  formulaire unique (validé 20/10) — **et nulle part ailleurs** : ni sur l'accueil ni sur une page Gîtes
  (Sébastien, 20/10).
- **Diaporama** : « les deux, sans doublon » (20/10) — le bandeau de l'accueil est le diaporama d'ambiance ;
  un bouton « Diaporama » sur le bandeau ouvre le diaporama complet (lecture/pause, précédent/suivant,
  chants d'oiseaux, plein écran, clavier, gestes) en superposition, photos chargées au clic ; la page
  « En images » le propose aussi en premier onglet. Un seul composant (`partials/_diapo.html` + `site.js`).
- **Page Avis : ne rien changer** (Marc l'aime bien) — sauf les liens, retirés le 22/10 (voir « Liens »).
- **Liens** (Marc, 22/10) : **aucun lien vers les plateformes de réservation ni vers les sites des labels**
  (Gîtes de France, Clévacances, Airbnb, Abritel…) — logos et notes affichés sans lien. Les liens utiles au
  visiteur (sites touristiques, mairie, carte, visite 360°) restent, et **tout lien s'ouvre dans la même
  fenêtre** (pas de `target="_blank"`), pour pouvoir revenir en arrière. Les liens sortants n'apportent
  rien au référencement (seuls les liens entrants comptent). Question ouverte à Marc : retirer aussi les
  liens touristiques ? (`TODO.md` § 4 `{labels}`).
- **Visite 360°** (hdmedia, 2015) : conservée, onglet nommé « Visite du gîte ».
- Photos : **retirer la photo de nuit de la maison sous la neige** (mur sali) partout — bandeau d'accueil,
  diaporama, partage. Ne pas insister sur le lit du salon dans les photos. Marc a envoyé des photos
  récentes (à abonder).
- **Bandeau d'accueil** (Sébastien, 20/10) : d'abord **4 secondes fixes** sur la photo d'Agnès, Marc et
  Urielle, puis les autres photos avec **zoom + déplacement** (effet Ken Burns) : chaque photo **part de
  loin** (échelle 1, photo entière) puis zoome lentement en glissant vers son point focal, quitte à zoomer
  plus qu'aujourd'hui — jamais l'inverse. Durée réglable par photo. Effet 3D : **parallaxe légère** du
  bandeau (plans photo / voile / titre à vitesses différentes) retenue ; **inclinaison à la souris
  acceptée à l'essai** (20/10) — Sébastien teste, donc **retour arrière facile** : un interrupteur
  `hero_tilt` (et `hero_parallax`) dans `shared.json`, une ligne à passer à `false` ; vraie 3D par carte de
  profondeur écartée.
- **Texte du bandeau selon la photo** (Marc, 22/10) : sur la photo d'Agnès, Marc et Urielle, « Agnès et
  Marc vous accueillent » + une ligne ; sur les autres photos, l'accroche des gîtes. Le `<h1>` reste
  l'accroche (unique, toujours dans la page) ; le texte des hôtes est un paragraphe stylé. Diapositive
  marquée `copy: "hosts"` dans `shared.json` ; sans JavaScript, l'accroche s'affiche.
- Distances validées : lac de Creutzwald 6 km, piscine de Creutzwald 7 km, gare de Saint-Avold 15 km,
  cimetière américain 15 km, Völklingen 28 km, musée des mineurs 31 km, Centre Pompidou-Metz 40 km,
  Bliesbruck 61 km. Restent à confirmer : zoo d'Amnéville, Sainte-Croix, boucle de la Sarre.
- Chaque information n'existe **qu'à un seul endroit** du site (son « chez-soi ») ; ailleurs, un lien.
  Simple en surface, complet en profondeur : l'essentiel en trois écrans, le détail dans des tiroirs.

### Réservation et Nuitrésa (côté site)
- Nuitrésa remplace Bed Booking. Le site intègre : le **formulaire v2** (un seul pour les deux gîtes,
  option « estimation globale des disponibilités »), les **calendriers publics** par gîte (ids 1100 et
  1101) et le **livre d'or**. Clé et identifiants dans `src/content/shared.json`.
- Le site reste **100 % statique** : aucune donnée client, aucun paiement ne transite par lui.
- Réglages Nuitrésa à faire par Marc (listés dans les notes) : capacité mini 1 ; nuits minimum 2 (règle
  week-end / 4 nuits en semaine par la grille tarifaire) ; bébés ; caution ; TVA (avec le comptable) ;
  photos et descriptif des fiches ; adresse du site à la bascule.

### Référencement
- **Carte blanche** à Claude ; plusieurs pages si utile au référencement.
- Langues : FR (référence), EN, DE, ES, PT, NL, ZH, avec repli FR pour les textes non traduits.
- Pages de fond (`landing`) : FR, EN et DE seulement (marchés visés) ; FAQ et 404 : toutes les langues.
  Titres ≤ 70 caractères, descriptions ≤ 160 (test automatique). `mentions-legales` hors sitemap.

### Code et licence
- **Pas de licence** (validé 20/10) : le dépôt est public (site de travail) mais **tout est « tous droits
  réservés »** — code, photos, vidéos, textes, logo et nom. Ne pas ajouter de fichier `LICENSE` ; une
  mention « © Agnès et Marc Nadler — tous droits réservés » dans le README et les mentions légales.

### Règle de repli pour les contenus
- **Si une information n'est pas dans les directives de Marc, prendre celle de l'ancien site**
  (`ancien-site/`), et la signaler dans les notes pour qu'il la valide (Sébastien, 20/10).

### Couleurs
- **Aligner l'accent du site sur le bordeaux du logo** (validé 20/10) : le cuivre `#a2652f` est remplacé
  par le bordeaux du logo ; les verts du site restent (ils sont proches de ceux du logo).

## 5. Questions ouvertes

Voir `TODO.md`. Aucune décision structurante en attente côté Sébastien ; restent les questions à Marc
(section 4 du TODO) et le verdict sur l'inclinaison 3D du bandeau après essai sur un vrai écran.
