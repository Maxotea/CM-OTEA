# Gossip Beauty Center by Sarah (Argenteuil) — fiche client

> ## ⛔ COMPTE DÉSACTIVÉ — 25/08/2026
>
> Maxime a demandé la désactivation du compte le 25/08/2026. **Ne plus produire
> de contenu, ne plus programmer, ne plus brancher de média, ne plus générer de
> compte rendu client.** Le compte est sorti du récap du lundi et de la
> détection de nouveaux médias (`recaps/clients-config.json`, `actif: false`).
>
> **Ce qui restait dans Metricool au moment de la désactivation :** 39 contenus
> du 25/08 au 23/10, dont 32 posts feed et 7 stories. **Tous en brouillon, aucun
> en publication automatique** : rien ne partira tout seul, il n'y avait donc
> pas d'urgence à purger. Quatre posts sans média et quatre carrousels encore
> à la maquette (`[CARROUSEL - contenu à mettre en page]`) faisaient partie du
> lot. **Ces brouillons n'ont pas été supprimés** : la suppression est
> irréversible et Maxime ne l'a pas demandée. À trancher avec lui.
>
> La fiche ci-dessous est conservée telle quelle : elle sert si le compte
> revient, et elle contient des règles qui ont demandé du travail (calendrier
> hégirien, salon exclusivement féminin, ton).

## Gossip Beauty Center by Sarah (Argenteuil) — profil éditorial validé juillet 2026
- Prestations : coiffure, spa, bien-être, hammam, massage. Tarifs : NON vérifiés — à demander (lien Planity ou liste) avant tout calcul ROI.
- Ton : classe à prix abordable — vouvoiement élégant, chaleureux, jamais de promo inventée.
- SPÉCIFICITÉS CLÉS : salon EXCLUSIVEMENT FÉMININ (argument majeur : intimité totale, femmes voilées libres — à rappeler ~1x/mois) + communauté musulmane active dans la clientèle.
- Calendrier hégirien à intégrer CHAQUE trimestre (dates à revérifier par recherche web, elles reculent ~11 jours/an) : Ramadan (~fév-mars 2027 : adapter les horaires de contenu, contenus douceur/patience, JAMAIS de récupération commerciale), Aïd el-Fitr (~mars 2027 : vœux + mise en beauté de fête), Aïd al-Adha (~mai 2027 : vœux sobres), Mawlid (26 août 2026 ±1j : vœux sobres sans CTA).
- Règle religieuse : posts de vœux sobres, inclusifs (« à toutes celles qui le célèbrent »), sans CTA commercial. Le hammam se raconte comme tradition/transmission (Maghreb, entre femmes).

## Visuels IA (Higgsfield)
- **Élément de référence : `Gossip-Studio`** (id `9c0e5746-c1ab-4d0c-8b1e-3e5a3763992f`). DA : institut féminin chaleureux/lumineux — rose poudré, beige, crème, laiton doré, fleurs roses (pivoine, rose, orchidée), marbre crème, touches orientales pour le hammam (seau laiton, savon noir, zellige). **Jamais de visage.** Réutiliser `<<<9c0e5746-c1ab-4d0c-8b1e-3e5a3763992f>>>`.
- Banque IA locale COMPLÈTE (8 visuels) `medias/gossip-beauty-center/ia/` : hammam, massage, coiffure (salon), produits-cheveux, soin-visage, cocooning, accueil, octobre-rose.
- Attachement : **Instagram + Facebook**, 18h. `schedule_post` + `media01`=URL, `draft:true`, `autoPublish:false` → corriger heure (`bulk_update_post_times` à 18:00, change les IDs) → supprimer l'ancien. ⚠️ Rate limit Zapier après ~6 créations : procéder par vagues de 6 avec pause ~90s ; ~1 création/vague échoue avec `followUpQuestion` (résolveur de compte) → refaire avec instruction compte explicite ; les suppressions échouent parfois « Code execution error » mais suppriment quand même (vérifier via list). ⚠️ Le champ `hasMedia` de list_scheduled_posts est trompeur (indiquait true alors que media vide) → vérifier via `get_post_raw`.
- **STATUT BRANCHEMENT : ✅ TERMINÉ (22/07/2026)** — 64 posts feed branchés en rotation, vérif finale = 0 post sans média.

## Stories quotidiennes (créées 27/07/2026)
- **Banque de 7 stories 9:16** dans `medias/gossip-beauty-center/ia/stories/` — DA Gossip-Studio, texte info incrusté sur le visuel (vérifié sans coquille) : lundi `story-lundi-semaine` (BELLE SEMAINE + liste services), mardi `story-hammam` (LE RITUEL HAMMAM), mercredi `story-coiffure` (CÔTÉ COIFFURE — Coupe·Couleur·Soin), jeudi `story-massage` (INSTANT MASSAGE), vendredi `story-weekend-resa` (PENSEZ AU WEEK-END), samedi `story-feminin` (UN LIEU 100% FÉMININ), dimanche `story-dimanche` (DOUCEUR DU DIMANCHE).
- **Planifiées ✅ (27/07)** : 35 stories en brouillon du 28/07 au 31/08 à **10:00**, IG+FB, rotation hebdo jour↔visuel (27/07/2026 = un lundi ; 1re planif était décalée d'un jour → supprimée et recréée). Créées via la code action **`bulk_schedule_stories`** (écrite sur mesure : posts JSON [{date_time, text, media_url}] + blog_id + networks → STORY draft avec média, timezone Paris correcte = PAS de bug +7h, ~12 posts/appel en ~15s). Rester ≤12 posts/batch (timeout sandbox).
## 🎥 Stories VIDÉO — vraies photos de l'institut (31/07/2026)
- **7 vraies photos du lieu déposées par Maxime** dans `medias/gossip-beauty-center/` (hammam travertin + laiton, cabines de repos rideaux, vasque marbre). Elles remplacent les visuels IA génériques sur 6 des 7 slots — c'est le vrai lieu, argument bien plus fort.
- **Cartes recomposées en DA Gossip** (`stories-video/carte-*.jpg`) : photo plein cadre + bandeau crème opaque en haut + titre Didot bronze `#5A3A21` interlettré + filet doré `#A87C4F` + sous-titre Baskerville italique. ⚠️ Le doré clair sur fond crème est ILLISIBLE (2 essais ratés) → texte bronze foncé + voile opaque jusqu'à y=410 obligatoire.
- **Pipeline vidéo** : fond SANS texte → i2v `kling3_0_turbo` (caméra VERROUILLÉE, « no zoom » : sur une carte à texte incrusté un push-in fait sortir le texte du cadre — vécu sur « Instant massage ») → ffmpeg upscale 1080×1920 + overlay du texte net → **xfade 0,6 s vers l'outro de marque** (`hf_20260720_...mp4`, logo GOSSIP sur satin rosé, 5 s, fourni par Maxime) → **9,46 s** au total. Fichiers finaux : `medias/gossip-beauty-center/stories-video/story-*.mp4`.
- **27 stories d'août remplacées ✅** (01→31/08 sauf les 4 mercredis), brouillon, IG+FB. Vérifié : 31 stories, 1 par jour, 0 doublon.
- ⚠️ **Mercredi « Côté coiffure » (05, 12, 19, 26/08) reste en visuel IA fixe** : aucune photo de la partie coiffure dans le dossier → à refaire dès que Maxime en dépose une.
- Les 7 anciennes vidéos animées à partir des visuels IA sont archivées dans `ia/stories/anim-en-attente/` (obsolètes, non planifiées).

- Rotation réutilisable : la banque est hebdomadaire-générique (aucune date dans les visuels) → replanifier les mêmes 7 chaque semaine, ou régénérer des variantes. Contenu 100% conforme fiche : aucun prix/horaire inventé, texte sobre, jamais de visage (mains OK).
- ⚠️ 3 stories pré-existantes d'une planification antérieure ce même intervalle (29/07 18h, 31/07 17h30, 03/08 18h) — pas des doublons d'horaire, laissées en place. Mapping thématique : hammam→hammam/gommage/rituel/chaud-froid/héritage/5 piliers ; massage→massage/détente/sommeil/toucher/WWW ; coiffure→couleur/balayage/tendances/mythes ; produits-cheveux→soin cheveux/gras/pointes/bouclés/mouillés/chute/brossage/cuir chevelu ; soin-visage→peau/hydratation/stress-peau ; cocooning→septembre/pluie/staycation/weekend/lumière-sommeil ; accueil→institut/équipe/avis/coulisses/fidélité/cadeau ; octobre-rose→30/09 + 05/10 ; hammam (sobre)→entre-femmes ; cocooning (sobre)→Mawlid 26/08 à 10h.
