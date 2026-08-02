# J Lawson Golf — fiche client

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

## Stories quotidiennes août 2026 (28/07/2026)
- Banque 7 stories 9:16 `medias/jlawson-golf/ia/stories/` (lun nouvelle-semaine, mar shaft, mer fers, jeu driver, ven résa, sam data, dim parcours). Vérifiées.
- **31 stories planifiées ✅** 01→31/08 à 10:00, IG+FB, brouillon, via `bulk_schedule_stories`.
