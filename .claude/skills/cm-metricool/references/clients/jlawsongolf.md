# J Lawson Golf — fiche client

## ✍️ Voix éditoriale — LA VOIX DE JOHN (règle client, 03/08/2026)
Le client a fourni son texte de référence (post AIG Women's Open du 03/08) et demandé que **tous les posts** adoptent ce style. Les 33 brouillons feed (10/08 → 23/10) ont été réécrits en conséquence. Codification :
- **Première personne du fitteur** : « je », « ce que je retiens », « je mesure », « j'y serai ». Plus de « on » d'agence ni de « le studio vous… » désincarné.
- **Vouvoiement du lecteur** (« pour vous », « votre swing ») — le tutoiement des anciennes légendes est abandonné.
- **Phrases courtes, paragraphes d'une à deux lignes.** Constat technique d'abord, enseignement ensuite.
- **Clôture en maxime sobre** (« Il faut trouver l'objet qui fonctionne pour vous », « Ça ne se devine pas. Ça se mesure ») — plus de CTA criard « 👉 lien en bio ».
- **Émojis quasi absents** : 🏆 toléré sur les posts résultat, rien d'autre.
- **Hashtags conservés, 4 par post.**
- Détails techniques précis bienvenus (bounce, torque, tr/min) — c'est sa crédibilité. Jamais de chiffre inventé : reprendre ceux validés ou rester qualitatif.
- ⚠️ Les 2 posts déjà validés par Maxime (05 et 07/08, draft:false) sont restés dans l'ancien style — ne pas les toucher.
- Post de référence : « Ce que je retiens de cette saison de majors féminins : 3 victoires avec des putters "lames" (Nelly Korda x 2 et Shiho Kuwaki) et 2 avec un maillet : Haeran Ryu. Il faut trouver l'objet qui fonctionne pour vous. »

## J Lawson Golf (source : jlawsongolf.com/rendezvous.html, vérifié juillet 2026)
- Fitting Driver/bois : 160 € (~1h)
- Fitting Fers/wedges : 160 € (~1h)
- Fitting putter : 160 € (~1h)
- Analyse technique Gears full corps : 260 € (~1h30)
- Panier moyen retenu : 160 € / séance (jusqu'à 260 €)
- Formule ROI : nb de fittings pour rembourser = prestation CM mensuelle ÷ 160
  - Ex. prestation 500 €/mois → ~3 fittings/mois · 800 €/mois → 5 fittings/mois
- Typologie : vente unitaire à forte valeur, clientèle qui revient à chaque changement de matériel (LTV : re-fitting tous les 2-3 ans + bouche-à-oreille club)

## Banque photos réelle — 107 fichiers (recomptés le 30/07/2026)
- Le dossier `medias/jlawson-golf/` contient **107 photos** (69 paysage, 38 verticales), pas 42 : la note ci-dessous date d'un comptage partiel. Statut `en-reserve` dans `recaps/medias-index.json` → vivier où la tâche du lundi puise pour remplacer progressivement les visuels IA (max 4/semaine).
- Les 38 verticales comblent le « trou » signalé plus bas (verticales 9:16 pour stories) : les stories IA du compte peuvent passer en vraies photos.

## jlawsongolf (banque validée juillet 2026 — 42 photos)
- Shooting pro HOMESANFAUTE (mai 2026) : portraits fitteur (bio/coulisses), sessions fitting client (P1/P5), détails clubs/shafts (P1/P2), ambiance studio+écrans (P3/P4)
- Photos terrain IMG_14xx-16xx : atelier gripping/loft-lie (P3 reels bruts), mur de shafts (P1/P2), clubs finis (P5), écrans de mesure/data (P1/P5)
- Trous à combler : verticales 9:16 pour stories, avant/après client, photos extérieur parcours
- Élément IA Higgsfield : "JLawson-Studio" (id 12942370-e8c1-465c-9ea0-2583a9384e0c) — DA moderne tech premium, métal noir mat, LED accent chaud, bleu marine + vert, AUCUN bois

## Visuels IA (Higgsfield) + branchement
- ⚠️ **INCOHÉRENCE DA À TRANCHER** : la description de l'élément de référence JLawson-Studio dit « lumière ambrée type atelier, ambiance premium artisanale », alors que la note ci-dessus dit « tech moderne, métal noir mat, AUCUN bois ». La banque IA générée (22/07/2026) suit l'élément de référence (atelier + bois) → à valider ou régénérer en version « tech moderne sans bois » si le client préfère.
- Banque IA locale (9 visuels) `medias/jlawson-golf/ia/` : fer-fitting, mur-shafts, balles, grip, driver, wedges, launch-monitor, studio, parcours. Bleu marine + vert respectés ; contiennent du bois (établi/mur).
- Attachement : **Instagram + Facebook**, 18h (posts « résultat tournoi » du dimanche à 12h). ⚠️ Metricool refuse les dates passées → un post daté d'hier ne peut pas être branché.
- **STATUT BRANCHEMENT : ✅ (22/07/2026)** — 38/39 posts avec média (le seul sans média = 21/07, déjà passé donc non branchable). ~31 posts branchés en rotation + 6 qui avaient déjà de vraies photos (shooting HOMESANFAUTE, non touchés). Mapping : fer→fers/lie/dispersion ; mur-shafts→shaft/Ryan Fox/Toussaint ; balles→balle ; grip→regripping/rentrée sac/checklist ; driver→driver/distance ; wedges→wedges ; launch-monitor→Gears/technologie/FedEx/bilan ; studio→journée studio/index/indoor/prépa/Open France ; parcours→tournois (circuit euro, Solheim, BMW PGA, Albatros).

## Post résultat AIG Women's Open — complété le 02/08/2026
- Post du **03/08 12:00** (ancien id 352532618 → nouveau **357057266**, via `bulk_replace_posts`). Brouillon vérifié, IG+FB, heure Paris exacte.
- Résultat réel : **Shiho Kuwaki** bat Esther Henseleit en playoff (mort subite sur le 18, victoire au 2ᵉ passage) à Royal Lytham, les deux à -5 après 72 trous. Premier majeur et première victoire LPGA Tour.
- ⚠️ **Le WITB a été abandonné, volontairement.** Le calendrier prévoyait un post « dans son sac ». Aucune source fiable ne donne son sac club par club : seul un agrégateur (golfreviewsguide) liste putter Odyssey White Hot OG 2-Ball + balle Bridgestone Tour B X, page inaccessible en vérification directe et compilée *pendant* le tournoi. Règle « jamais de matériel inventé » → post recentré sur le playoff et la leçon de fitting (régularité du club sous pression). **Ne pas réintroduire de WITB sans source constructeur ou média équipement.**
- **Visuel : carte résultat typographique** (choix de Maxime, 02/08). Aucune photo de Kuwaki n'est utilisable : toutes les images de l'épreuve sont des photos d'agence (Getty — Luke Walker, Warren Little), « editorial use only », et il n'existe aucune photo d'elle sous licence libre sur Wikimedia Commons. La règle « jamais de photo d'agence sur un compte commercial » s'applique.
- Carte régénérable à l'identique :
  ```
  python3 scripts/carte-resultat.py carte.jpg \
    --surtitre "AIG WOMEN'S OPEN 2026 · ROYAL LYTHAM & ST ANNES" \
    --nom "SHIHO KUWAKI" --score "-5" --mention "VICTOIRE EN PLAYOFF" \
    --detail "Bat Esther Henseleit au 2e trou de mort subite, après 72 trous à égalité" \
    --note "PREMIER MAJEUR"
  ```
- ⚠️ **La carte a dû être attachée à la main.** L'environnement de la session n'a pas d'accès sortant vers les hôtes d'hébergement (Higgsfield, CloudFront, static.metricool) → impossible de produire l'URL publique qu'exige `media_url`. Le brouillon porte en attendant un visuel IA de links. Depuis une machine avec accès réseau normal, le pipeline `media_upload → PUT → media_confirm → bulk_replace_posts` fonctionne comme d'habitude.
- Modèle réutilisable pour tout post « résultat de tournoi » : `scripts/carte-resultat.py` (4:5, DA marine/vert/ambre).

## Stories — rotation 2 semaines, vidéo + fond sonore (03/08/2026) ✅ ACTIF
- **Règle Maxime (03/08) : aucune story identique sur 2 semaines consécutives.** Rotation de **14 cartes distinctes** en cycle A/B (A = semaines des 03, 17, 31/08 ; B = 10, 24/08). Vérifié par calcul : toute fenêtre glissante de 14 jours contient 14 stories différentes.
- **28 stories VIDÉO planifiées ✅ 04→31/08 à 10:00** (ids 357218610→357219269), IG+FB, brouillon vérifié par `get_post_raw`. L'ancienne rotation hebdo de 7 visuels IA (28 brouillons) a été supprimée. La story du 03/08 (ancienne, visuel IA fixe) a été laissée en place.
- **Format : cartes typographiques ANIMÉES 7,5 s avec fond musical** — cartes PIL pures (zéro IA, zéro photo, DA marine/vert/ambre, conforme au précédent Pierre Huiban), musique en **synthèse procédurale** (`scripts/fond-sonore-stories.py` : pulse électronique premium ~100 BPM — aucun sample tiers, aucun modèle génératif, zéro droits). Assemblage ffmpeg image+audio.
- Source de vérité de la rotation : `assets/stories/manifest-stories-2sem.json` (14 slots : titre, sous-titre, note). Cartes : `assets/stories/jlawson-golf/`. Régénération : `carte-story-typo.py` + `fond-sonore-stories.py` + ffmpeg.
- Reconduction de septembre : replanifier les mêmes 14 vidéos (URLs cloudfront dans le manifest des payloads, réutilisables telles quelles) en respectant le cycle A/B.
- 📌 Ces cartes typo sont l'intérim conforme à la règle « zéro IA dans les stories » : quand `medias/` sera rapatrié, les 38 photos verticales réelles pourront remplacer progressivement les cartes via la tâche du lundi (i2v identité verrouillée + contrôle dernière frame).

## Stories VRAIES PHOTOS (03/08/2026, décision Maxime : « photos transformées en vidéo ») — EN COURS
- **Fait — slot « Analyse Gears » (jeudi B)** : photo réelle 11 (studio, homme au stick d'alignement, `…mtr_11226288403794074990.jpg`) → crop 9:16 → i2v kling3_0_turbo identité verrouillée (job 413f6f72) → **dernière frame contrôlée visuellement : identique** → 1080×1920 + calque texte « ANALYSE GEARS / TON SWING CAPTURÉ EN 3D » + jl.wav → `https://d2ol7oe51mr4n9.cloudfront.net/user_2zae6klRfE97hlBWhyQP6j7d9cR/91db08d2-78fc-4e1d-b50c-833f14b7a54f.mp4`. Planifiée **13/08 + 27/08 10:00** (ids **357397907, 357397912**, brouillon IG+FB vérifié) ; anciennes cartes 357218703/357219041 supprimées.
- **Prêt à générer (bloqué par le plafond quotidien Higgsfield `grace_daily_limit_reached` du 03/08)** — crops 9:16 hébergés et confirmés, presignés 24 h :
  | Photo | media_id crop | Slot cible | Cartes à supprimer |
  |---|---|---|---|
  | 03 mur de shafts (John choisit un shaft) | `8160dba4-c7b2-47af-b296-e710a306b634` | mardi (A) — LE SHAFT / « Flex, poids, torque : le moteur de ton club » | 357218610 (04/08), 357218963 (18/08) |
  | 06 swing sur simulateur, data à l'écran | `4fb51fe1-f79b-40e0-b502-f459b5e3d1af` | samedi (A) — LA DATA PARLE / « Chaque club validé au launch monitor » | 357218645 (08/08), 357219000 (22/08) |
  | 09 John en conseil client, mur Titleist | `eeeb1120-549b-45af-ad84-884089f1501d` | samedi (B) — CÔTÉ ATELIER / « Montage, gripping, loft-lie : fait ici » | 357218722 (15/08), 357219244 (29/08) |
- Photo 01 exclue (visuel promo The Open/Royal Birkdale : texte incrusté + droits R&A). Bilan : 4 slots/14 en vraies photos ; les 10 autres gardent leur carte typo en attendant de nouvelles photos.
- ⚠️ Si les dates 04/08 ou 08/08 sont passées à la reprise, ne remplacer que l'occurrence future du slot.

## Stories quotidiennes août 2026 (28/07/2026 — REMPLACÉE le 03/08)
- Banque 7 stories 9:16 `medias/jlawson-golf/ia/stories/` (lun nouvelle-semaine, mar shaft, mer fers, jeu driver, ven résa, sam data, dim parcours). Visuels IA, rotation hebdo — abandonnée au profit de la rotation 2 semaines ci-dessus.
