# Pierre Huiban — fiche d'onboarding

## Identité
- blogId Metricool : 6572293
- Réseaux connectés : Instagram (@pierrehuiban89)
- Secteur / typologie : athlète sponsorisé — compétiteur Hyrox (double vie commercial Europe / athlète), campagne Road to Stockholm (Mondiaux Hyrox 2026)
- Ville / zone de chalandise : n/a (personal branding, pas de zone de chalandise)
- Site web / source officielle : n/a — vérifier si un site/linktree existe

## Ligne éditoriale — RÉÉCRITE LE 20/08/2026
⛔ **L'ancienne ligne est morte.** Elle disait « tutoiement, énergie brute, LFG
comme signature, rage silencieuse ». Pierre l'a rejetée le 19/08 (« ça ne me
ressemble pas ») en envoyant une capture de sa propre story. Détail du diagnostic
plus bas ; ce qui suit est la ligne en vigueur.

- **Langue : anglais.** C'est la langue dans laquelle il écrit lui-même.
- **Ton : première personne, récit du quotidien, chaleureux et généreux.** Il
  remercie, il met les autres en valeur, il admet ce qu'il a mal fait.
- **Émojis assumés** : 🔊 ❤️ 🙏 — pas de décoration, ils portent l'intention.
- **Interdits absolus** : « LFG », « Pas d'excuses », « Balance-moi », l'impératif
  sec, le registre coach-motivation. Aucun de ces mots ne doit revenir.
- **Fin de post** : une invitation ouverte et un remerciement, jamais un ordre.
  Modèle : « Tell me which one changed the most for you. I read everything 🙏 ».
- Cible : communauté Hyrox (France et au-delà), marques cherchant un athlète
  sponsorisé authentique.
- Piliers : dépassement de soi, double vie (commercial + athlète + papa),
  coulisses d'entraînement, Road to Hong Kong.
- Direction artistique : **inchangée** (Pitch Black #0A0A0A + Rouge Sang #DC2626,
  capitales). Il n'a jamais reproché la DA. Ne pas la refaire sans lui demander.
- Direction artistique (si supports visuels type carrousels/covers) : Pitch Black #0A0A0A + Rouge Sang #DC2626, typo display Anton (UPPERCASE), corps Inter, stats en JetBrains Mono
- Interdits : jamais de sponsoring déguisé non assumé, jamais de prix/partenariat inventé

## Partenariats / sponsors actuels (mise à jour 17/07/2026)
- **KAIRYN** (site : kairyn.fr — attention à l'orthographe, pas "Kayrin") — marque française de compléments sport, slogan "Refuse The Average", fondée par un pratiquant Hyrox. Produit phare : pré-workout **IGNITE**. Intégré au post "7 incontournables" (angle pré-workout/compléments).
- **GX SOCIETY** (SAS, Anglet, dirigeant Alexandre Gouaux) — PAS une marque de vêtements : matériel de **récupération / pressothérapie** ("La révolution de la récupération"). Intégré au post "7 incontournables" (angle outils de récup). Le post "setup d'entraînement" (chaussures/vêtements/accessoires) a été repassé en version sans mention sponsor — aucun des 3 partenaires ne correspond à cette catégorie.
- **SPLIT NUTRITION** — repas sains livrés à domicile (pas des compléments). Mentionné pour l'instant uniquement dans l'annonce partenariat groupée du 21/07 — pas encore de post dédié qui lui correspond vraiment (aucun post actuel ne parle de repas/alimentation quotidienne). À créer quand plus d'infos/assets seront dispo.

⚠️ Handles Instagram exacts et règles de tag contractuelles (hashtag obligatoire, @ légende vs commentaire, logo) **toujours à confirmer** — Instagram bloque le fetch direct, donc handles non vérifiables pour l'instant. Mentions actuelles faites par nom de marque uniquement (pas de @handle inventé), avec disclosure `#partenariat` par transparence publicitaire.

## Rythme & horaires
- Cadence actuelle observée : reels/posts lifestyle Hyrox, horaires 00h30/06h00 (à confirmer si voulu, ces horaires semblent atypiques pour du lifestyle sport — à vérifier avec l'utilisateur)

## Saisonnalité & temps forts
- Road to Stockholm : Mondiaux Hyrox 2026 (vérifier dates exactes par recherche web le moment venu)
- Contenus déjà en brouillon : famille/double vie, setup d'entraînement, mindset, coach (Quentin), objectifs fin 2026

## Tarifs vérifiés — pour le module ROI
- Non applicable : accompagnement à part (pas un client facturé au même titre que les 6 comptes CM classiques). Pas de calcul ROI à produire pour ce compte.

## Banque photos
- Emplacement / état : catalogue dans `references/clients/banque-photos-pierre-huiban.md`, classé générique / par sponsor (Kairyn, GX Society, Split Nutrition). 81 vraies photos dans `medias/pierre-huiban/` (fichiers `Sans titre-NN.jpg`).
- Preset IA (Higgsfield) : aucun — on utilise les VRAIES photos (personal branding, du vrai obligatoire).

## Branchement des visuels
- **STATUT : ✅ (23/07/2026)** — 11/11 posts feed avec vraie photo, 0 sans média, **Instagram uniquement**, horaires d'origine conservés (00:30 / 06:00). Vérifié.
- Méthode : vraies photos locales redimensionnées 1440px → hébergées via [[hebergement-photos-reelles-metricool]] (media_upload → PUT → media_confirm → URL cloudfront) → `schedule_post` `media01`=URL, `instagram:true`, `facebook:false`, `linkedin:false`. Bug +7h corrigé via `bulk_update_post_times`.
- Mapping photo↔post : 25/07 compétition→85 ; 29/07 setup→51 (b-roll chaussures) ; 01/08 7 incontournables→47 (b-roll corde, neutre) ; 05/08 mental→76 (néon SE DÉPASSER) ; 08/08 5 phrases→62 (rameur) ; 12/08 coach→75 (Pierre+Quentin) ; 15/08 3 raisons coach→53 ; 19/08 rentrée→13 ; 22/08 objectifs→73 (console stats) ; 26/08 communauté→68 ; 29/08 automne→16 (box jump).
- ⚠️ **À AMÉLIORER** : (1) les posts « Swipez → » sont des **carrousels** — je n'ai attaché qu'**UNE photo de couverture** ; à compléter avec les slides quand elles seront designées. (2) Le post « 7 incontournables » mentionne **Kairyn + GX Society** mais **aucune photo sponsor n'existe** → j'ai mis une photo neutre (corde, sans logo) ; demander à Pierre de vraies photos des produits Kairyn (IGNITE) et du matériel GX Society pour un vrai post sponsorisé.

## Stories quotidiennes août 2026 (28/07/2026)
- Banque 7 cartes typographiques 9:16 `medias/pierre-huiban/ia-stories/` — DA fiche (Pitch Black #0A0A0A + Rouge #DC2626, uppercase condensé) : lun LUNDI-ON-REPART-LFG, mar PAS-D'EXCUSES, mer LA-DONNÉE-PARLE, jeu ÇA-BRÛLE, ven ENCORE-UNE-SÉANCE, sam SAMEDI-VOLUME, dim RÉCUP. Cartes design (pas de fausses photos) — conforme à la règle « vraies photos only » pour le photographique.
- **31 stories planifiées ✅** 01→31/08 à **06:00** (son créneau), Instagram uniquement, brouillon, via `bulk_schedule_stories`.

## 🔴 RETOUR CLIENT 19/08/2026 — fautes + « ça ne me ressemble pas »

### 1. Les fautes — carrousel « Cinq erreurs… » du 19/08 (id 363944373)
⚠️ **Déjà publié** : instagram.com/p/DcOk-T3im0Y — les slides sont hébergées sur
i.ibb.co, on ne peut pas les corriger a posteriori dans un post en ligne.

| Slide | Texte publié | Problème |
|---|---|---|
| 1 | « Aucune n'a à voir avec ta condition physique. » | Il manque le *rien* : « n'a **rien** à voir avec ». |
| 3 | « Le sled ne se pousse pas, il s'appuie. » | **Contresens technique.** Le sled push *est* une poussée. Un pratiquant Hyrox voit tout de suite que ce n'est pas écrit par quelqu'un qui pratique. |
| 4 | « Faire du wall ball frais, tout le monde sait. » | Phrase incomplète : « tout le monde **sait le faire** ». |

### 2. Le vrai problème : la ligne éditoriale est fausse depuis l'onboarding
Pierre a envoyé une capture de sa propre story comme référence. Sa voix réelle :
- **il écrit en anglais** ;
- première personne, récit du quotidien (« Today, I went for a track session ») ;
- **chaleureux et généreux** — il remercie, il met les autres en valeur
  (« You kids are absolute magic. Thank you for the energy ») ;
- émojis assumés (🔊 ❤️ 🙏) ;
- propos rassembleur : le sport qui fait tomber les barrières sociales.

Ce que la fiche a codé et ce qu'on publie pour lui :
- **en français** ;
- « rage silencieuse », « LFG » en signature, impératif, « Pas d'excuses »,
  « Dis-moi en commentaire » ;
- registre coach-motivation agressif.

**Ce n'est pas un défaut d'exécution, c'est la ligne qui est fausse.** Elle a été
déduite à l'onboarding, jamais validée avec lui. Tant qu'elle n'est pas refaite
avec Pierre, tout ce qu'on produit continuera de « ne pas lui ressembler ».

⛔ **Ne pas relancer de production sur ce compte** avant d'avoir tranché avec lui :
langue (anglais / français / les deux), registre, et place du « LFG ».

### Leçon
Une ligne éditoriale de personal branding ne se déduit pas d'un secteur. Elle se
construit à partir des textes que la personne a **déjà écrits elle-même**, et se
fait valider avant la première production.

## ✅ LIGNE REFAITE EN ANGLAIS — 20/08/2026 (décision Maxime)
Maxime a tranché : **anglais, son ton réel**. Tout le compte a été repris sur la
capture qu'il a envoyée — anglais, première personne, récit, gratitude, émojis
assumés. **« LFG », « Pas d'excuses », « Balance-moi », « Dis-moi en
commentaire » ont disparu du compte.**

### 🚨 Ce qu'il faut regarder en premier : 4 stories étaient en publication auto
`363944431` (20/08), `363944089` (21/08), `363943901` (22/08), `363943845`
(23/08) étaient en **`draft:false` + `autoPublish:true`**. Elles allaient partir
toutes seules, avec les cartes « PAS D'EXCUSES » que Pierre venait de rejeter.

- Les 3 à venir ont été repassées en brouillon immédiatement.
- **`363944431` (20/08 06:00) était déjà passée** — impossible de la rattraper,
  Metricool refuse d'éditer une date écoulée.
- ⚠️ Règle 1 du CLAUDE.md : *tout contenu reste en brouillon*. Un contrôle
  `draft`/`autoPublish` doit être fait **sur chaque compte**, pas seulement sur
  celui qu'on est en train de traiter.

### Les 5 posts feed, réécrits
| Date | Sujet | Ce qui change |
|---|---|---|
| 22/08 | Three goals for the end of 2026 | anglais ; « Swipez → » retiré (le post n'a **qu'une seule image**, la promesse de swipe était fausse) |
| 26/08 | The sled that ends most races | anglais ; « Dis-moi lequel… LFG » → « If it helps you, tell me. I'd love to know 🙏 » |
| 29/08 | What's coming this autumn | anglais ; « Swipez → » retiré (une seule image) |
| 02/09 | September — four profiles | anglais ; « Balance-moi ton point faible. LFG » → « Tell me what your weak station is — I read everything 🙏 » |
| 09/09 | Road to Hong Kong | anglais ; « LFG. » final → « Thank you for the energy ❤️🙏 » |

### Les 24 slides de carrousel, régénérées
Les slides étaient en **français** avec l'ancien registre. Les 3 carrousels
(26/08, 02/09, 09/09) ont été refaits, 8 slides chacun, en anglais.

**Le gabarit visuel n'a pas été touché** — c'est délibéré. Pierre n'a jamais
reproché la DA, il a reproché les textes. Redessiner la DA sans la lui faire
valider serait refaire exactement l'erreur d'origine. Le gabarit a donc été
relevé au pixel sur les slides existantes et reproduit à l'identique :
fond `#0A0A0A`, accent `#DC2626`, corps `#9A9A9A`, surtitre rouge interlettré,
titre capitales blanc puis rouge, pied « n/8 » + « SWIPE → », dernière slide
inversée en rouge. Générateur versionné : `scripts/pierre-carousel.py`.

### Les 7 cartes de story, régénérées en anglais
Le texte des cartes est **incrusté dans l'image** : réécrire la légende ne
suffisait pas. Les 7 cartes ont été refaites, même DA, textes chaleureux :

| Jour | Avant (FR) | Après (EN) |
|---|---|---|
| lundi | Lundi. On repart. LFG | A NEW WEEK — *One session at a time.* |
| mardi | Pas d'excuses | SHOW UP ANYWAY — *Some days the session is average. It still counts.* |
| mercredi | La donnée parle | THE DATA DOESN'T LIE |
| jeudi | Ça brûle ? | IT BURNS A LITTLE |
| vendredi | Encore une séance | ONE MORE SESSION |
| samedi | Samedi = volume | VOLUME DAY |
| dimanche | Récup | REST IS TRAINING TOO — *Thank you for this week.* |

Les 11 stories du 21 au 31/08 pointent dessus, rotation par jour de semaine.

### Vérifié après coup
`17 posts sur 20/08 → 30/09 · 5 feed · 12 stories · noMedia:0 · aucun doublon ·
draft:true partout sauf 363944431 (déjà publiée, hors de portée).`

### Ce qui reste ouvert
- Faire **valider la nouvelle ligne par Pierre lui-même** avant de reprendre la
  production. On a corrigé sur la base de sa capture, pas sur une validation.
- Les **fautes du carrousel du 19/08 déjà publié** (`instagram.com/p/DcOk-T3im0Y`)
  restent en ligne : slides hébergées sur i.ibb.co, non corrigeables a posteriori.
  Seule option : supprimer et republier — décision de Maxime.
- Les **handles Instagram exacts** des sponsors, toujours non vérifiés.

### ⚠️ Une 5e story a échappé au verrouillage — publiée le 20/08 à 06:00
Le passage du 19/08 avait neutralisé 4 stories en `autoPublish:true`. Une
cinquième (`363944431`) est passée entre les mailles : elle est partie seule ce
matin à 06:00, avec un visuel du **28/07** — donc de l'ancienne ligne, celle que
Pierre a rejetée. `instagram.com/stories/pierrehuiban89/3967631015874705336`

Une story expire en 24 h, donc l'exposition est limitée et il n'y a rien à
défaire. Ce qu'il faut en retenir : **le contrôle `autoPublish` doit porter sur
tout le calendrier du compte, pas sur les seules publications qu'on est en train
de retoucher.** Le compte est vérifié depuis : `16 publications · draft:true
partout · autoPublish:false partout · noMedia 0`.
