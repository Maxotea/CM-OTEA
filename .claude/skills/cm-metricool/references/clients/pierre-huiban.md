# Pierre Huiban — fiche d'onboarding

## Identité
- blogId Metricool : 6572293
- Réseaux connectés : Instagram (@pierrehuiban89)
- Secteur / typologie : athlète sponsorisé — compétiteur Hyrox (double vie commercial Europe / athlète), campagne Road to Stockholm (Mondiaux Hyrox 2026)
- Ville / zone de chalandise : n/a (personal branding, pas de zone de chalandise)
- Site web / source officielle : n/a — vérifier si un site/linktree existe

## Ligne éditoriale
- Ton : tutoiement, énergie brute, "LFG" comme signature récurrente, pas de mise en scène, pas de bullshit
- Cible : communauté Hyrox France, marques cherchant un athlète sponsorisé authentique
- Différenciateur n°1 : la rage silencieuse — intensité brute plutôt que discours marketing ; la donnée (chronos, compteurs J-XX, volumes) comme preuve plutôt que promesse
- Piliers de contenu : dépassement de soi, double vie (commercial + athlète + papa), coulisses d'entraînement, LFG comme fil rouge non expliqué
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

## Carrousel hebdo (créneau du mercredi, 18h, Instagram)
- **Typologie** : personal branding athlète → la preuve est la donnée et la constance, jamais la promesse. **Cible** : communauté Hyrox France (pratiquants amateurs qui bossent à plein temps) et marques cherchant un athlète authentique. Jargon Hyrox assumé, tutoiement, aucune mise en scène.
- **Archétypes prioritaires** : A7 (coulisses), A2 (erreurs), A1 (méthode), A5 (guide de choix). A6 (décryptage chiffré) dès que Pierre fournit ses vrais chronos et volumes — **ne jamais fabriquer un chiffre**.
- **DA carrousel** (`scripts/themes.json` → `pierre-huiban`) : Pitch Black #0A0A0A, texte blanc, accent Rouge Sang #DC2626, capitales, stats en mono. Cartes typographiques uniquement — conforme à la règle « vraies photos only » pour le photographique, on ne fabrique aucune image de lui.
- **Planifiés (spec dans `carrousels/pierre-huiban/`)** : 12/08 A7 « Une semaine de prépa, vraiment » · 19/08 A2 « 5 erreurs qui te coûtent des minutes » · 26/08 A1 « Sled push : la station qui casse ta course » · 02/09 A5 « Quelle station bosser en priorité ».
- **Ce que ça résout** : la fiche signalait que les posts « Swipez → » n'avaient qu'une photo de couverture, sans slides. Le format carrousel est désormais outillé — les anciens posts « Swipez » peuvent être repris avec ce moteur.
- **Vigilance** : **tout le contenu technique doit être relu par Pierre avant publication** — c'est son expertise, pas la nôtre. Aucun chrono, aucune charge en kilos, aucune date de Mondiaux cités sans vérification. Aucun sponsor mentionné dans ces quatre carrousels : un carrousel sponsorisé exige les handles exacts, les règles de tag contractuelles et de vraies photos produit, tout cela encore manquant.
