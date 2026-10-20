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
- Le dossier du site sur le Mac (`~/Desktop/SiteDomaineDuGeisberg`) est la **source de vérité du dépôt** :
  on commite sur le Mac, on pousse vers GitHub via un bundle depuis le cloud (git ne peut pas effacer ses
  fichiers de verrou sur le Mac — ne pas s'en inquiéter, les renommer). Messages de commit en français.
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
- Le **mot de passe** Nuitrésa ne doit apparaître nulle part (notes, dépôt, docs, messages). Se déconnecter
  de Nuitrésa en fin de session. (Marc doit le retirer du document Word envoyé et le changer.)

### Qualité, avant toute mise en ligne (GitHub ou DECLIC)
- `python3 tools/build.py` puis `python3 tools/check.py` : **0 erreur**.
- Tests Playwright (`tests/test_site.py`) tous verts, balayage des débordements (`tests/sweep.py`)
  de 320 à 1366 px sans débordement, vérification visuelle dans le navigateur (ordinateur et mobile).
- Rien ne part en ligne sans ces contrôles.

### Communication
- Messages rédigés pour Sébastien à son père : tutoiement, « Papa », signature **« Biz »** (jamais
  « Je t'embrasse »). Mails à des tiers : vouvoiement, sauf indication.
- Tout ce qui est dit à Marc par mail à propos du site doit **aussi** figurer dans les notes du site.
- Ne pas envoyer de mail à la place de Sébastien : préparer le texte, il envoie.

## 3. Notes pour Marc (mode « Notes »)

- Bouton « Notes pour Marc » en bas à droite de chaque page, **en français seulement**, inactif par défaut.
  Pastilles numérotées sur les éléments concernés + panneau récapitulatif en bas.
- Les notes sont **exhaustives sur toutes les pages**, mises à jour à chaque changement, et signalent
  aussi les **problèmes** (réglages Nuitrésa, contradictions entre le site et Nuitrésa, sécurité).
- L'accueil porte une note « Vue d'ensemble » qui résume tout ce qu'il reste à faire côté Marc.
- Les textes sont dans `tools/content/fr.json` → `notes`, accrochés par `data-note` dans les gabarits.

## 4. Décisions de contenu validées (par Marc, sauf mention)

### Identité
- **Logo officiel** fourni le 20/10 (maison dessinée, bordeaux et verts, « Domaine du Geisberg — Gîtes
  ruraux Varsberg ») : **à utiliser**, « sans abuser, mais à mettre en avant » — en-tête, favicon, pied de
  page, image de partage. Source : `photos-sources/logo/logo-geisberg.png`.
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
  (« doit rester exceptionnel ») : une mention discrète dans la fiche, jamais dans les chiffres clés.
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
- Texte « gîtes jumeaux » (variante courte de Marc, 19/10) : « Deux gîtes identiques. Réservez l'un des
  deux, ou les deux pour un groupe. » **[À CONFIRMER]** vs sa première variante « Deux gîtes jumeaux, même
  vue — Mêmes prestations de part et d'autre. Réservez l'un des deux, ou les deux pour une tribu. »
- Horaires : arrivée à partir de 16 h, départ avant 10 h (comme dans Nuitrésa).

### Tarifs (Marc, 20/10) — par gîte
| Séjour | Conditions | Prix |
|---|---|---|
| Week-end, 2 nuits | arrivée vendredi (vendredi + samedi) | 300 € |
| Week-end, 3 nuits | arrivée vendredi (vendredi + samedi + dimanche) | 350 € |
| Semaine, 4 nuits | arrivée dimanche, lundi, mardi, mercredi ou jeudi ; **minimum 4 nuits hors week-end** | 300 € |
| 5, 6 ou 7 nuits | — | 420 € |

- Acompte : 25 % (Nuitrésa). Taxe de séjour en sus. CB, Visa, MasterCard, chèques-vacances ANCV.
- Caution : 300 € sur le site, 0 € dans Nuitrésa — **à trancher par Marc** (chèque à l'arrivée ou
  empreinte bancaire via Nuitrésa).
- Le site affiche cette grille ; c'est Marc qui la reporte dans Nuitrésa (prix selon la durée).

### Pages et structure
- **Menu à 5 entrées** : accepté « à voir une fois monté ».
- **Accueil** : d'abord la photo d'Agnès, Marc et Urielle (environ 4 secondes, « à voir »), puis les photos
  de la maison, puis les **photos et la description des gîtes sur la même page** ; les équipements peuvent
  y rester. → Interprétation retenue **[À CONFIRMER]** : l'accueil devient la page de présentation
  (hôtes → maison → gîtes → fiche → tiroir « Tout l'équipement » → bouton Réserver) et il n'y a plus de
  page « Les gîtes » séparée.
- **Disponibilités** : « une page disponibilité avec les deux gîtes » → les deux calendriers (un par
  gîte) sur la page **Réservation**, au-dessus du formulaire unique **[À CONFIRMER]**.
- **Page Avis : ne rien changer** (Marc l'aime bien).
- **Visite 360°** (hdmedia, 2015) : conservée, onglet nommé « Visite du gîte ».
- Photos : **retirer la photo de nuit de la maison sous la neige** (mur sali) partout — bandeau d'accueil,
  diaporama, partage. Ne pas insister sur le lit du salon dans les photos. Marc a envoyé des photos
  récentes (à abonder).
- Distances validées : lac de Creutzwald 6 km, piscine de Creutzwald 7 km, gare de Saint-Avold 15 km,
  cimetière américain 15 km, Völklingen 28 km, musée des mineurs 31 km, Centre Pompidou-Metz 40 km,
  Bliesbruck 61 km. Restent à confirmer : zoo d'Amnéville, Sainte-Croix, boucle de la Sarre.
- Chaque information n'existe **qu'à un seul endroit** du site (son « chez-soi ») ; ailleurs, un lien.
  Simple en surface, complet en profondeur : l'essentiel en trois écrans, le détail dans des tiroirs.

### Réservation et Nuitrésa (côté site)
- Nuitrésa remplace Bed Booking. Le site intègre : le **formulaire v2** (un seul pour les deux gîtes,
  option « estimation globale des disponibilités »), les **calendriers publics** par gîte (ids 1100 et
  1101) et le **livre d'or**. Clé et identifiants dans `tools/content/shared.json`.
- Le site reste **100 % statique** : aucune donnée client, aucun paiement ne transite par lui.
- Réglages Nuitrésa à faire par Marc (listés dans les notes) : capacité mini 1 ; nuits minimum 2 (règle
  week-end / 4 nuits en semaine par la grille tarifaire) ; bébés ; caution ; TVA (avec le comptable) ;
  photos et descriptif des fiches ; adresse du site à la bascule.

### Référencement
- **Carte blanche** à Claude ; plusieurs pages si utile au référencement.
- Langues : FR (référence), EN, DE, ES, PT, NL, ZH, avec repli FR pour les textes non traduits.

### Code et licence
- Code publié en **licence libre (MIT)** ; photos, vidéos, textes, logo et nom : **tous droits réservés**
  (Marc et Agnès Nadler). **[À CONFIRMER]**

## 5. Questions ouvertes

Voir `TODO.md`, section « À confirmer ». Les principales : interprétation « accueil = page de
présentation », calendriers sur la page Réservation, variante du texte « gîtes jumeaux », caution,
affichage du couchage d'appoint, licence, couleurs du site alignées sur le logo ou non.
