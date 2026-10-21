# Pierre Huiban — fiche d'onboarding

## ⚙️ PUBLICATION AUTOMATIQUE · 21/10/2026 (décision Maxime)

« On va faire l'automatisation des postes avec Pierre parce qu'il ne les valide pas […]
on va les publier. » Pierre ne reçoit plus de tableau hebdo (`actif: false` dans
`reviews/config.json`) ; la relève (`validation_auto: true`) passe en publication les
brouillons des 14 jours à venir, avec les garde-fous de la review (média présent, pas
de placeholder ni de tiret cadratin, image de feed entre 4:5 et 1.91:1). Les **reels**
sortent en **mode notification** : Metricool notifie Maxime à l'heure prévue, il pose la
musique dans Instagram et publie (le compte n'est pas relié à une page Facebook, le son
Instagram ne peut pas être posé par Metricool : 403 le 21/10). On continue de tout
créer en brouillon.

## ✅ RELANCE « ROAD TO HONG KONG » — 05/10/2026 (décision Maxime)

Maxime relance l'accompagnement à fond : Pierre est qualifié pour les Mondiaux
HYROX de Hong Kong (juin 2027). Deux consignes explicites : **« on oublie le LFG »**
et **« une DA adaptée au texte que je t'ai envoyé »** (son persona, ci-dessous).

### Persona (transmis par Maxime le 03/10/2026)
- Père de famille, marié, un petit garçon.
- Dirigeant commercial : équipe sur la France, l'Espagne et l'Italie. **L'employeur
  n'est pas nommé dans les posts** tant que Pierre ne l'a pas validé.
- Athlète HYROX en **Pro Doubles Men avec Antoine Bouhana**. Stockholm : premiers
  Français de la catégorie 35-39, 16es mondiaux. Nouvelle victoire de catégorie et
  nouvelle qualification à Rome.
- Partenaire signé : **Fitness Park**. Recherche un petit nombre de partenaires,
  « pas simplement un logo sur une tenue ».
- Budget de saison : **jamais publié** (décision de Maxime du 05/10).

### DA « trois vies » (remplace Pitch Black / Rouge Sang)
- Papier `#F2EEE6`, encre `#14171C`, un seul accent « aube » `#E8622C`.
- Titres Fraunces SemiBold en casse normale, texte Inter, chiffres JetBrains Mono.
- Registre en tête de chaque visuel : `ATHLETE · FATHER · EXECUTIVE`, avec la
  facette du jour en couleur. Pied : `ROAD TO HONG KONG · JUNE 2027`.
- Générateurs : `scripts/pierre-carousel-v2.py` (carrousels 1080×1350) et
  `scripts/pierre-story-photo-v2.py` (stories 1080×1920 sur vraie photo).
  Aucune image générée, aucune retouche du visage.
- **Stories : toujours une VRAIE photo d'entraînement de Pierre en fond**
  (décision de Maxime du 05/10 : les cartes typographiques sur fond uni sont
  « nulles, fades »). Photo de la banque recadrée 9:16, dégradé sombre en haut
  et en bas, une seule phrase. `scripts/pierre-story-cards-v2.py` est périmé.

### Données de course (source HYRESULT, vérifiées)
- `assets/hyrox/hyrox_pierre-huiban_rome_2026.{json,csv,srt}` : Rome 26/09/2026,
  **53:34**, 1er des 35-39, 12e sur 292 en Pro Doubles Men.
- `assets/hyrox/pierre-huiban_saison-2026_avec-antoine.json` : Paris 54:42,
  Lyon 54:59, Stockholm 55:29, Rome 53:34.
- `assets/hyrox/rushes_rome_2026.json` : 34 rushes FX3 recalés sur le chrono.
  Les vidéos 7302 à 7344 et 7347 manquent dans le Drive (seuls les XML y sont).
- **Stats d'entraînement : aucune source.** Le Strava connecté est celui de
  Maxime. Demander à Pierre des exports Garmin ou Strava, ou des captures.

### Ce qui est dans Metricool (brouillons, vérifiés le 05/10)
- 4 carrousels, mercredi 18:00 : 07/10 Rome station par station, 14/10 quatre
  courses avec Antoine, 21/10 trois vies, 28/10 Road to Hong Kong (Fitness Park,
  appel aux partenaires). Specs dans `projets/pierre-huiban/carrousels-v2/2026-10-*.json`.
- 12 reels **sans vidéo** (06/10 au 01/11), légendes prêtes. Le montage revient à
  Maxime à partir des rushes de Rome ; plan clip par clip dans
  `plans/pierre-huiban/2026-10-reels.json`. À l'ajout de la vidéo, vérifier
  que le post passe bien en type Reel.
- 57 stories 06:00 (05/10 au 30/11) sur vraies photos d'entraînement, 21
  visuels en rotation, libellés en anglais. Specs et calendrier appliqué :
  `projets/pierre-huiban/carrousels-v2/stories-photos-v2.json`. 8 visuels prévus n'ont pas
  pu être hébergés (mercredi, vendredi, samedi tournent sur 2 photos) : à
  ajouter quand l'upload repasse.
- Validation par Pierre : une feuille par semaine dans son dossier Drive
  `1VGThaVWofkwv3sUqZQo-R0_sST5nvytB` (semaines du 05-10 et du 12-10 créées le
  05/10, deux semaines d'avance). Colonne Format corrigée à la main (Story /
  Reel / Carrousel) en attendant le correctif de `review.py`.
- Supprimés : les 8 posts feed en français d'octobre (LFG, « rage silencieuse »,
  « ma saison se joue plus tard » devenu faux après Rome). Textes archivés dans
  `archives/pierre-huiban/metricool-brouillons-2026-10-05.json`.
- ⚠️ **Restent 8 posts feed en français en novembre** (04, 07, 11, 14, 18, 21,
  25, 28/11), ancienne ligne, dont 3 avec « LFG ». À réécrire ou remplacer dans
  la nouvelle DA quand le plan de novembre sera fait.
- ⚠️ Les cartes de story **LFG en français** étaient revenues sur octobre et
  novembre alors qu'elles avaient été remplacées le 20/08 : nouvelle occurrence
  du processus inconnu qui réécrit les calendriers.

### Décisions de Maxime du 05/10/2026 (font foi)
- **Langue : anglais.** Un peu de français de temps en temps, jamais en majorité.
- **Employeur : jamais cité.** Ni nom, ni logo, ni indice permettant de le
  retrouver. On peut parler du métier (équipe commerciale France, Espagne, Italie).
- **Budget de saison : jamais public.** Il reste un argument de discussion en
  privé avec les marques, jamais dans un post, une story ou une légende.
- **Partenaires actuels : LE PREWORKOUT et Fitness Park.**
  « LE PREWORKOUT » est le nom de la marque, donné tel quel par Maxime le 05/10.
  Son compte Instagram n'est pas encore connu : citer la marque par son nom,
  sans @ inventé. **Kairyn ne fait plus partie des partenaires** : ne plus la
  citer ni la taguer. GX Society et Split Nutrition, non cités par Maxime, sont
  considérés inactifs jusqu'à confirmation.
- **Antoine Bouhana : @antoine_bhna** (donné par Maxime le 05/10). Tagué une
  fois par légende, à la première mention ; les mentions suivantes restent
  « Antoine ». Déjà fait sur les 5 brouillons qui le citent (07/10, 14/10,
  reels du 06/10, 18/10 et 22/10).

### Encore ouvert
Compte Instagram de LE PREWORKOUT ; statut de GX Society et Split Nutrition ; tournage d'entraînement en novembre ; stats
d'entraînement (export Garmin ou Strava).

### Reels monologue (13/10/2026)
Référence donnée par Maxime : @rundadlift, reel DeHgY1RxPfB (monologue intérieur
d'un père qui court, noir et blanc, sous-titres jaunes à empattements centrés,
valse au piano). Cinq specs dans `projets/pierre-huiban/reels-monologue/` :
M3-R6 (27/10, REEL 401840603), M1-R7 (20/10, 388250104, non branché), D1-R8 (22/10,
388353604), M2-R11 (29/10, 388250135), M4-R12 (01/11, 388250148). Moteur :
gabarit `monologue` de `scripts/pierre-reel-ralenti.py`, mode d'emploi dans
`projets/pierre-huiban/reels-dialogue/README.md`. Sorties muettes, aucune voix
synthétisée, aucun plan d'Antoine sous un « I ». Au 13/10, aucun reel n'est
rendu (Drive en « Quota exceeded ») et les légendes des brouillons sont encore
les anciennes : les remplacer par la `legende` de chaque spec au branchement.

## Identité
- blogId Metricool : 6572293
- Réseaux connectés : Instagram (@pierrehuiban89)
- Secteur / typologie : athlète sponsorisé — compétiteur Hyrox (double vie commercial Europe / athlète), campagne Road to Hong Kong (Mondiaux Hyrox 2027)
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
- Direction artistique : ⛔ **remplacée le 05/10/2026** par la DA « trois vies »
  (voir la section en tête). Pitch Black / Rouge Sang / Anton ne sert plus.
- Interdits : jamais de sponsoring déguisé non assumé, jamais de prix/partenariat inventé

## Partenariats / sponsors (historique du 17/07/2026, ⛔ périmé : voir les décisions du 05/10 en tête)
- **KAIRYN** (site : kairyn.fr — attention à l'orthographe, pas "Kayrin") — marque française de compléments sport, slogan "Refuse The Average", fondée par un pratiquant Hyrox. Produit phare : pré-workout **IGNITE**. Intégré au post "7 incontournables" (angle pré-workout/compléments).
- **GX SOCIETY** (SAS, Anglet, dirigeant Alexandre Gouaux) — PAS une marque de vêtements : matériel de **récupération / pressothérapie** ("La révolution de la récupération"). Intégré au post "7 incontournables" (angle outils de récup). Le post "setup d'entraînement" (chaussures/vêtements/accessoires) a été repassé en version sans mention sponsor — aucun des 3 partenaires ne correspond à cette catégorie.
- **SPLIT NUTRITION** — repas sains livrés à domicile (pas des compléments). Mentionné pour l'instant uniquement dans l'annonce partenariat groupée du 21/07 — pas encore de post dédié qui lui correspond vraiment (aucun post actuel ne parle de repas/alimentation quotidienne). À créer quand plus d'infos/assets seront dispo.

⚠️ Handles Instagram exacts et règles de tag contractuelles (hashtag obligatoire, @ légende vs commentaire, logo) **toujours à confirmer** — Instagram bloque le fetch direct, donc handles non vérifiables pour l'instant. Mentions actuelles faites par nom de marque uniquement (pas de @handle inventé), avec disclosure `#partenariat` par transparence publicitaire.

## Rythme & horaires
- Cadence actuelle observée : reels/posts lifestyle Hyrox, horaires 00h30/06h00 (à confirmer si voulu, ces horaires semblent atypiques pour du lifestyle sport — à vérifier avec l'utilisateur)

## Saisonnalité & temps forts
- **Road to Hong Kong** : Mondiaux Hyrox 2027, AsiaWorld-Expo, 10-13 juin 2027 (vérifié par recherche web le 06/08/2026 — annoncé pendant les Mondiaux de Stockholm).
- ⚠️ **Stockholm, c'est fini** : les Mondiaux 2026 ont eu lieu du 18 au 21 juin 2026. Le hashtag `#roadtostockholm` est périmé depuis. Une campagne datée se revérifie à chaque trimestre — celle-ci est restée dans la fiche deux mois de trop et s'est retrouvée dans quatre carrousels avant qu'un correctif manuel dans Metricool ne la rattrape.
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

## Carrousel hebdo (créneau du mercredi, 18h, Instagram)
- **Typologie** : personal branding athlète → la preuve est la donnée et la constance, jamais la promesse. **Cible** : communauté Hyrox France (pratiquants amateurs qui bossent à plein temps) et marques cherchant un athlète authentique. Jargon Hyrox assumé, tutoiement, aucune mise en scène.
- **Archétypes prioritaires** : A7 (coulisses), A2 (erreurs), A1 (méthode), A5 (guide de choix). A6 (décryptage chiffré) dès que Pierre fournit ses vrais chronos et volumes — **ne jamais fabriquer un chiffre**.
- **DA carrousel** (`scripts/themes.json` → `pierre-huiban`) : Pitch Black #0A0A0A, texte blanc, accent Rouge Sang #DC2626, capitales, stats en mono. Cartes typographiques uniquement — conforme à la règle « vraies photos only » pour le photographique, on ne fabrique aucune image de lui.
- **Planifiés (spec dans `carrousels/pierre-huiban/`)** : 12/08 A7 « Une semaine de prépa, vraiment » · 19/08 A2 « 5 erreurs qui te coûtent des minutes » · 26/08 A1 « Sled push : la station qui casse ta course » · 02/09 A5 « Quelle station bosser en priorité ».
- **Ce que ça résout** : la fiche signalait que les posts « Swipez → » n'avaient qu'une photo de couverture, sans slides. Le format carrousel est désormais outillé — les anciens posts « Swipez » peuvent être repris avec ce moteur.
- **Vigilance** : **tout le contenu technique doit être relu par Pierre avant publication** — c'est son expertise, pas la nôtre. Aucun chrono, aucune charge en kilos, aucune date de Mondiaux cités sans vérification. Aucun sponsor mentionné dans ces quatre carrousels : un carrousel sponsorisé exige les handles exacts, les règles de tag contractuelles et de vraies photos produit, tout cela encore manquant.

## Relance du 13/10/2026

Journaux complets : scratchpad de la session, `relance/` (état, exécution, décembre, clôture). Aucune question Q1 à
Q16 du cadrage ne concerne Pierre. Les reels (chantier monologue) relèvent d'un autre chantier.

- **DA** : « trois vies » inchangée. Stories sur vraies photos ; jamais d'IA sur son visage
  (`recaps/clients-config.json`), donc des stories vidéo tirées de vrais ralentis, et l'i2v seulement sur des photos
  sans visage (47, 50, 51), si Maxime le confirme. La section « Carrousel hebdo » plus bas (Pitch Black, Rouge Sang)
  est périmée.
- **Feed** : les 8 posts de novembre en français (ancienne ligne, LFG) réécrits en anglais le 13/10 : 394698312
  (04/11), 394698681 (07/11, « ask me anything »), 394698708, 394698738, 394698771, 394698790, 394698816, 394698840.
  Décembre posé en brouillon : 7 posts, 394831234 (C1, 02/12), 394832053 (C2 partenaires), 394832080 (J-180, 12/12),
  394832122 (C3 en version repli), 394832144 (C4), 394832169 (C5 bilan), 394832189 (31/12). Les 3 reels et les 31
  stories de décembre ne sont pas créés : aucune vidéo de fond.
- **Validation** : rien de nos brouillons n'est parti depuis le 05/10. Le tableau du 19-10 est en lecture seule, les
  liens n'ont pas été envoyés, le courriel perso de Pierre manque.
- **Reels monologue branchés le 21/10** (type REEL, vidéo de livraison vérifiée au md5 sur le CDN et dans la copie Metricool, puis passés en **mode notification** le même jour, musique à poser dans Instagram) : D1 « Rome, split by split » **402181744** (jeu. 22/10 12:30, couverture 1,5 s), M1 « After the line » **402226693** (sam. 24/10 12:30, couverture 2,4 s, publié sur décision de Maxime sans attendre Pierre), M3 « Two engines » **402224390** (mar. 27/10 12:30, couverture 6,67 s), M2 « Keep showing up » **402224788** (jeu. 29/10 12:30, couverture 1,7 s), M4 « 221 days » **402224853** (dim. 01/11 18:00, couverture 2,0 s). Ids des brouillons d'avant : 402004284, 401840603, 402005051, 402005104. R5 « Sled pull » (388250088) et R10 « The hidden station » (388250126), sans vidéo, sont supprimés sur décision de Maxime du 15/10 (mêmes rushes et mêmes idées que M3 et D1).
- **Corrigé le 13/10** (décision de Maxime : « je ne sais pas, corrige ») : « won several Pro Doubles races together », non documenté, devient « won our age group in Rome and qualified for the World Championships twice », sans la phrase de chute « Rome was one more » qui laissait croire à une troisième qualification. « this season » devient « this year » dans la légende, et le sur-titre de la slide 02 « THE SEASON » devient « 2026 » : Pierre compte Rome comme la course n° 1 d'une nouvelle saison (30/09), et HYROX classe Paris (23 au 26/04/2026) et Lyon (20 au 24/05/2026) en saison 25/26. Les quatre courses sont toutes en 2026. Carrousel du 14/10 : **395138284** (slides 02 et 06 re-rendues, spec `projets/pierre-huiban/carrousels-v2/2026-10-14-quatre-courses-avec-antoine.json`) ; reel du 18/10 : **395043919** (`instagramData.type` encore POST, à passer en REEL au branchement de la vidéo). Tableau du 12-10 mis à jour (_tech B10, B16, E10, E16 ; G6, G12 ; lien F6 vers une planche des 7 slides), `legende_modifiee` reste faux.
- **Chiffres (13/09 au 12/10)** : 4 718 abonnés au 12/10, 97 gagnés et 321 perdus (perte qui ralentit : 458, 424,
  321) ; ses carrousels font 1 423 de portée moyenne contre 840 pour ses reels ; tout ce qui a marché, il l'a publié
  lui-même.
- **Reste** : brief de tournage prêt (envoi par Maxime, tournage les 19 à 21/10 ou les 24 et 25/10) ; photos
  Lightroom et rushes Rome 7302 à 7344 ; médias des posts de novembre (2:3 et doublons de stories, avant le 23/10) ;
  11 stories qui répètent un visuel à moins de 28 jours ; calendrier de courses 2026-2027 ; compte Instagram de LE
  PREWORKOUT. Son coach apparaît sous @leqiou_fit dans ses publications (la fiche dit « Quentin ») : à confirmer.
