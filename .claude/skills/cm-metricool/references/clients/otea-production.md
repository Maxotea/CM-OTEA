# OTEA PRODUCTION — fiche client

## OTEA PRODUCTION (oteaproduction.com) — profil validé juillet 2026
- Production audiovisuelle B2B : vidéo d'entreprise, captation événementielle (séminaires, salons, aftermovies), interviews/marque employeur, drone, style cinématique (Sony FX3, étalonnage chaud). Otea Filmakers (blogId 4728418) = marque vitrine créative/voyage, à traiter séparément.
- Réseaux posts texte : Instagram + Facebook + LinkedIn (TikTok et YouTube = vidéo uniquement). Horaire B2B : 12h00. Ton : vouvoiement pro accessible, expert qui challenge, CTA « lien en bio » vers devis/portfolio.
- Typologie ROI : B2B projet — devis variables (demander les fourchettes de devis moyens au user) ; 1 projet signé couvre largement la prestation CM ; compter aussi les leads qualifiés (DM, calls découverte).
- Temps forts annuels : rentrée = budgets Q4/plans com ; SEPT-OCT = pousser les VŒUX vidéo de fin d'année (se tournent en oct-nov, jamais en déc) ; salons d'automne ; janvier = plans annuels.

## Cap du 13/10/2026 : montrer au lieu de dire (prime sur les habitudes ci-dessous)
Décidé avec Maxime le 13/10/2026 sur les chiffres Metricool (81 abonnés Instagram, 20 sur la page LinkedIn, portée moyenne 34 par post photo contre 180 pour le seul reel de l'été, aucune publication du 02/09 au 12/10). Plan complet : `plans/otea/2026-10-plan-de-bataille.md`.
- **2 reels par semaine** de coulisses réelles (jour J, plateau, retour moniteur, rush brut contre film livré avec accord du client), montés depuis les disques de Maxime ; un post photo sur deux est remplacé par un reel dès qu'il est prêt. Les carrousels de méthode du mercredi restent.
- **LinkedIn perso de Maxime** (connecté dans la marque Otea Filmakers de Metricool) : une publication B2B par semaine, à la première personne.
- **CTA « écrivez-nous en message »** tant que oteaproduction.com n'affiche qu'une installation WordPress vierge (constat du 13/10) : plus de « lien en bio » dans les nouvelles légendes.
- Promesse face à la concurrence : **100 % tourné, vraies images** (aucune agence parisienne au-dessus de 6 000 abonnés Instagram, concurrents sur la vidéo IA ou le prix d'appel).

## Charte graphique (Brandbook 2026, PDF livré)
- Couleurs primaires : **Orange `#FF5800`** (couleur phare — énergie, chaleur narrative, plateau de tournage) · Blanc `#F1F1F1` · Noir `#201E1E` · **Vert d'eau `#ACC1C0`**. Combinaisons : Orange & Noir (impact), Vert & Noir (sobriété), Blanc & Noir (minimalisme).
- Typo : **Forma DJR Display** (titres Bold, sous/sur-titres Medium, corps Text Normal).
- Univers photographique officiel : « images contrastées, silhouettes, scènes de tournage, matériel cinématographique, portraits émotionnels. Ambiance réelle, sensorielle, immersive. »
- ADN : culture polynésienne (vague / Koru) + production audiovisuelle. Valeurs : Émotion, Création, Héritage, Exigence, Authenticité — « montrer le vrai, raconter le réel ».
- Assets livrés : `/Volumes/VERT SSD/Livraison finale/` (LOGOTYPE, MONOGRAMME vague/Koru, ICONOGRAPHIE monoligne, FONT, SIGNATURE MAIL).

## Visuels IA (Higgsfield) + branchement
- **Élément de référence : `OTEA-Studio`** (id `b40ad9de-ba3e-428a-bc87-a6fa42b3e7bd`, environment). DA : plateau de tournage cinéma, silhouettes contrastées, contre-jour orange vif dans brume, noir charbon, accents vert d'eau, matériel ciné, réel/sensoriel/immersif, jamais de logo ni texte. Réutiliser `<<<b40ad9de-ba3e-428a-bc87-a6fa42b3e7bd>>>`.
- Banque IA locale (9 visuels) `medias/otea-production/ia/` : plateau-tournage (silhouette gimbal), camera-gear (caméra ciné), etalonnage (coloriste/monitors), interview-setup (softbox + tabouret), drone (coucher de soleil orange), captation-event (opérateur en événement), mains-focus (mains sur objectif), projecteur (faisceau fresnel), vague-koru (motif marque orange/vert d'eau).
- **STATUT BRANCHEMENT : ✅ (23/07/2026)** — 37/37 posts feed avec média, 0 sans média, vérifié. Réseaux : **Instagram + Facebook + LinkedIn** (user a dit IG+LinkedIn mais a choisi de garder FB pour la portée). Horaire **12h** (B2B). Doublon du 11/09 supprimé.
- ✅ **2ᵉ passe VRAIES PHOTOS FAITE (29/07/2026)** : 31 vraies photos (shooting HOMESANFAUTE + portrait pro) déposées dans `medias/otea-production/`. **20 des 31 posts feed futurs basculés en vraie photo** (mapping thématique : témoignage→interview micro, verticale→gimbal, coulisses→BTS, golden hour→extérieur doré, salon→écran « Bienvenue rencontre entrepreneurs », LinkedIn→portrait pro, storytelling→prise de parole, etc.), 11 gardés en IA (drone, étalonnage, projecteur, vague-koru, camera-gear… = pas de photo correspondante). Vérifié : 1 post/date, 0 sans média, 0 doublon. Les 3 posts déjà passés (24-29/07) non touchés.
- ✅ **Correctif 29/07 après-midi** : la 1ʳᵉ version de `bulk_replace_posts` créait en `draft:false` → les 6 posts feed touchés (03→14/08) ont été recréés en brouillon vérifié (ids 355355641/688/715/729/758/797). L'action vérifie désormais le draft après chaque création (`draft_verified`).
- 🟢 **Le gérant VALIDE au fil de l'eau dans Metricool** (vu les 28-29/07) : semaine 01→08/08 stories validées en auto + posts feed 17 & 19/08 validés (ids recréés par l'UI : 355338045/111/173/284/336, 355322884/959). Story dim 09/08 en mode notification (355319371). Ne pas re-toucher les contenus validés.
- ⚠️ **PIÈGE API : le PUT scheduler Metricool ne remplace PAS le média** — il répond 200 mais recrée parfois le post sous un nouvel ID (fantômes/doublons). Pour changer un visuel : **`bulk_replace_posts`** (code action : crée le nouveau post avec média + heure Paris exacte, puis supprime l'ancien) + `bulk_delete_posts` pour nettoyer. Ne JAMAIS utiliser bulk_update_post_media (retirée de la méthode).
- Méthode : recréation via `schedule_post` (pas d'action « attacher média par URL » ; `upload_image_attach_post` existe mais exige le base64, non exploitable à l'échelle). Bug +7h → `bulk_update_post_times` à 12:00. Vérifier `resolvedParams.blogId.label` = OTEA PRODUCTION à chaque création.

## Stories quotidiennes août 2026 (28/07/2026)
- Banque 7 stories 9:16 `medias/otea-production/ia/stories/` (lun belle-semaine, mar idée-vidéo, mer coulisses, jeu conseil, ven parlons-projet, sam captation, dim inspiration). DA orange/noir/teal. Vérifiées.
- **31 stories planifiées ✅** 01→31/08 à 10:00, IG+FB (stories LinkedIn non supportées), brouillon, via `bulk_schedule_stories`.
- **Vraies photos dans les stories (29/07)** : 3 slots de la rotation basculés en cartes photo composées via PIL (photo réelle intacte + barre orange #FF5800 + titre HelveticaNeue, fond flouté) : **mercredi Coulisses** (`story-coulisses-photo.jpg`, gros plan objectif), **vendredi Parlons projet** (`story-projet-photo.jpg`, sourire derrière caméra), **samedi Captation événement** (`story-captation-photo.jpg`, micro en événement). 13 stories d'août remplacées, doublon 08/08 purgé, vérifié 1 story/jour. Lun/mar/jeu/dim restent IA (silhouette, clap, fauteuil, drone). Script PIL réutilisable pour composer des cartes 9:16 photo+texte sans IA (pas d'altération de visages).
- ⛔ **PLUS AUCUN VISUEL IA DANS LES STORIES (règle Maxime, 01/08/2026)** — voir [[stories-vraies-photos-sans-ia]]. Les 13 stories qui tournaient encore sur les visuels IA (lun/mar/jeu/dim) sont remplacées par **4 cartes issues de ses vraies photos**, réellement animées en i2v : lun `260506-153801` (gimbal en action) · mar `260702-103536` (tournage studio à deux) · jeu `251107-094553` (échange conseil au bureau) · dim `260506-155121` (plan large graphique, lampe suspendue). Fichiers : `medias/otea-production/stories-video/`. Ids août : 356689499/502/504/507/508/513/515, 356689545/550/555/560/563/571.
- **Août = 100 % vraies photos animées** : 13 (nouvelles) + 9 cartes photo animées (mer/ven/sam) + 4 stories photo fixes déjà validées par Maxime, non touchées.
- **Cartes photo ANIMÉES (30/07)** : les 9 stories photo encore en brouillon (mer 12/19/26, ven 14/21/28, sam 15/22/29 août — ids 355805218/232/244/250/261/270/280/299/310) sont passées en **vidéo 5 s** (`story-*-anim.mp4` dans `ia/stories/`). Pipeline réutilisable : calques PIL séparés (fond photo sans texte + PNG texte avec scrim dégradé sombre en haut pour lisibilité) → i2v Higgsfield `kling3_0_turbo` (7,5 crédits/5 s, prompt « subtle cinemagraph, slow push-in, face stays identical, no morphing ») → ffmpeg upscale 1080x1920 + overlay du texte fixe (net) → mp4 hébergé via media_upload → `bulk_schedule_stories` accepte les .mp4 tel quel. Frames vérifiées : visages intacts. Les 4 stories photo VALIDÉES par Maxime (01, 05, 07, 08/08) restent en photo fixe — ne pas re-toucher ; proposer la bascule vidéo s'il re-valide.

## 🔇 Stories muettes — corrigé le 19/08/2026
Les **3 cartes photo composées le 29/07** (Coulisses, Parlons projet, Captation
événement) portaient une bande son incrustée, contrairement à ce que supposait
`_portage/REPRISE-STORIES-PHOTOS.md`. Elles ont été redéposées muettes :

| Slot | Ancien média (sonore) | Nouveau média (muet) | Nouveaux ids (19 + 26/08, 21 + 28/08, 22 + 29/08) |
|---|---|---|---|
| mercredi Coulisses | `b7f45530` | `85fc08f7-301b-4d2a-a464-845f100f3516` | 363861326 · 363861333 |
| vendredi Parlons projet | `da10744b` | `422579cc-be31-42ca-95f3-8e6fb5d1c6d0` | 363861348 · 363861359 |
| samedi Captation | `1fe49bcf` | `dcaa7c92-abeb-4d9b-9a29-0890745af254` | 363861362 · 363861363 |

Les 4 cartes IA (Le conseil, Inspiration, Belle semaine, Idée vidéo) étaient
déjà muettes — non touchées. Anciens brouillons supprimés : 355805250, …261,
…270, …280, …299, …310. Vérifié : 13 stories, une par jour du 19 au 31/08.

⚠️ Toute nouvelle story de ce compte part **sans son** (`-an` au montage) :
`.claude/memories/stories-sans-son.md`.

## Carrousel hebdo (créneau du mercredi, 12h, Instagram + Facebook + LinkedIn)
- **Typologie** : B2B projet → la preuve est la méthode et le cadrage. **Cible** : dirigeant ou responsable communication de PME, souvent échaudé par une première vidéo qui n'a rien donné. Ce qu'il veut vérifier : que ça sert un objectif business et que ça ne va pas immobiliser son entreprise.
- **Archétypes prioritaires** : A2 (erreurs), A1 (méthode), A8 (rétroplanning saisonnier), A7 (coulisses, lève l'objection « on va bloquer les bureaux »). A6 possible mais **toute statistique du secteur exige une source web datée**.
- **DA carrousel** (`scripts/themes.json` → `otea-production`) : fond #201E1E, texte #F1F1F1, accent orange #FF5800, secondaire vert d'eau #ACC1C0, titres en capitales, sans filet. Charte Brandbook 2026, police Forma DJR Display si installée.
- **Planifiés (spec dans `carrousels/otea-production/`)** : 12/08 A2 « 5 erreurs qui plombent une vidéo d'entreprise » · 19/08 A1 « De l'idée au film livré » · 26/08 A8 « Vœux 2027 : le rétroplanning » (temps fort sept-oct de la fiche) · 02/09 A7 « Ce qui se passe le jour du tournage ».
- **Réserve de sujets** : « Vertical ou horizontal : comment choisir » (A5) · « Ce qu'une journée de tournage peut produire » (A1, argument déclinaisons) · budgets Q4 et plans de com (A8, septembre) · cas client commenté (A3, avec accord).
- **Vigilance** : les fourchettes de devis ne sont pas renseignées → aucun tarif ni délai chiffré tant que Maxime ne les fournit pas. Ce compte est aussi la vitrine de l'offre CM : un carrousel réussi ici est un cas d'usage commercial réutilisable.

## 🎬 Inspirations de montage

Les prochains reels de ce compte reprennent les styles listés pour lui dans `../inspirations-montage.md` (n°1 au 08/10/2026). La relire avant chaque script.

## Validation automatique (07/10/2026)
Maxime est le client de ce compte : « tu peux considérer que c'est validé à chaque fois, car c'est moi », puis choix explicite de la publication automatique. Plus de tableau de validation (le dossier « Validation hebdo — OTEA PRODUCTION » et ses tableaux du 12-10 et du 19-10 restent en place, sans usage). Le contenu est toujours créé en brouillon ; la relève GitHub (`validation_auto` dans `reviews/config.json`, PR #56) passe en publication les brouillons des 14 jours à venir qui passent les garde-fous : média présent, pas de placeholder, pas de tiret cadratin dans une légende, pas de note « À tourner », pas de visuel IA de juillet (`medias_retenus`).
- 07/10 : tirets cadratins retirés des 14 légendes feed du 07/10 au 06/11, et « Les 3 questions à te poser » passé au vouvoiement (21/10). Nouveaux ids 390382088 à 390382469.
- ⚠️ Visuels IA de juillet encore en place les 09/10 (« La cohérence visuelle ») et 16/10 (« Dernière ligne droite avant la Toussaint ») : bloqués tant qu'une vraie photo ne les remplace pas.

## Relance du 13/10/2026

Journaux complets : scratchpad de la session, `relance/` (état, exécution, animation, décembre, pilotage, clôture).

- **DA photo** : Orange et Noir, vouvoiement, vraies photos seulement (banque HOME SANFAUTE, manifeste
  `photos/otea-production.json`). Carrousels « fond photo » rendus par `scripts/carrousel.py` (thème otea-production,
  Inter Display en attendant une licence Forma DJR, Q5), logotype horizontal blanc versionné (Q6). Les visuels IA de
  juillet sont tous remplacés (le 16/10 est 394461848, vraie photo 10).
- **Stories** : une par jour à 10:00, Instagram et Facebook. Toutes muettes depuis le 13/10 : les vidéos mer, ven et
  sam portaient une piste AAC, refaites en `-an` (mp4 18f768b2 mer, a6fad937 ven, 5333de1a sam ; 5 stories armées
  recréées en brouillon puis réarmées par la relève de 14h02 : 394878015,
  394878048, 394878083, 394878113, 394878134 ; 10 brouillons changés de média).
  Samedi en DA plein cadre i2v du 24/10 au 28/11 (mp4 0889c651 ; 24/10 réarmé en 394877979, puis
  394727280 à 394727345). Lun, mar, mer et jeu :
  i2v refusés le 13/10 (visages qui dérivent, personne inventée, faux logo), l'ancienne story reste. Ven non animé
  (plancher de 100 crédits), dim bloqué (photo 42 refusée deux fois). Aucune story en décembre.
- **Crédits Higgsfield (13/10 après-midi)** : plancher ramené de 100 à 40 par Maxime, solde partagé de 55,25 après les stories R.O.I. animées (leurs ids sont dans `run-on-invest.md`, aucune ne concerne ce compte).
- **Feed** : carrousel A8 variante Noël au 28/10 12:00 (394672845, remplace le vœux 390382341, Q16). Décembre posé en
  brouillon : 13 posts à 12:00, IG, FB, LinkedIn, 394836453 à 394837622 ; carrousels du mercredi A2 (02/12), A1
  (09/12), A6 Wistia 47 % (16/12), A5 (23/12), A8 fenêtres 2027 (30/12) ; Connecter le 14/12 et le 25/12. Le 11/12
  (394836543) et le 30/12 (394837622) restent bloqués par une ligne à confirmer : disponibilité de tournage du 06 au
  22/02 et du 03 au 19/04, réponse attendue avant le 26/11. Le reel du 07/12 attend des rushes (sinon l'image part).
- **Décisions de Maxime** : Q1 oui (Noël, 394180229 armé) ; Q2 « quelques jours » (394180259) ; Q5 Inter Display ;
  Q6 logotype ; Q7 stories armées remplacées à partir du 19/10 (fait pour le samedi) ; Q8 plafond 187,5 crédits,
  solde Higgsfield 100,25 le 13/10, plancher de 100 tenu ; Q15 pas de rattrapage du 12/10 ; Q16 oui (galette le 25/11,
  A8 le 28/10). Q4 ne concerne pas ce compte : personne n'y est présenté comme Maxime.
- **Chiffres (13/09 au 12/10)** : 81 abonnés Instagram, 0 publication feed depuis le 02/09 (chute mécanique de la
  portée), LinkedIn 20 abonnés et 14 des 24 clics du trimestre sur 3 carrousels, Facebook 1 abonnée.
- **Reste** : A4 SATIS 30/10 (390382368 : CTA neutre et photo 9ea5ec6b doublon du 23/10, avant le 16/10 12h) ;
  02/11 (390382400) et 12/11 (394180718) reprennent mot pour mot des slides de l'A8 ; A5 « avant le 5 décembre »
  (394180951, avant le 13/11) ; rotation 30 jours des 04, 12 et 18/11 ; carrousel LinkedIn en PDF impossible par
  Zapier ; lien en bio vers un WordPress vierge ; stories de décembre ; ligne KPI d'octobre le 02/11. Proposé par la
  lecture KPI, non appliqué : feed à 11:00 (LinkedIn 11h vaut 2 à 2,4 fois 12h).
- **Publicité** : deux specs en brouillon, `campagnes/otea-production/2026-11-seminaires-janvier.json` et
  `2026-12-vacances-hiver.json`. Rien n'est créé dans Meta.

## Correction et rattrapage du 21/10/2026

Décision de Maxime : « rattraper tout ce qui n'a pas été publié ». Source : audit du 21/10 au matin. Journal des ids
dans le scratchpad de la session (`otea-2110/journal-ids.json`).

- **Connexion** : Instagram et Facebook toujours absents de la marque à 15:05 UTC (`getBrandSettings` : LinkedIn,
  TikTok, YouTube seulement). Rien n'a été recréé pour contourner la panne. Les providers instagram et facebook sont
  restés dans tous les posts, Metricool les accepte encore en écriture.
- **CTA** : « lien en bio » devient « écrivez-nous en message » dans 16 légendes à venir, état de publication
  conservé. Armés : 23/10 402251845, 26/10 402249588, 28/10 402251900, 30/10 402250284 (SATIS : CTA seul, photo
  9ea5ec6b gardée en attendant que Maxime confirme), 02/11 402250335. Brouillons : 04/11 402250385, 06/11 402249319,
  09/11 402250439, 12/11 402250488, 13/11 402250537, 16/11 402250584, 18/11 402250636, 20/11 402250671,
  23/11 402250697, 25/11 402250737, 27/11 402250797, 30/11 402250849. Le 21/10 (393966788) était déjà passé.
- **Carrousel du 28/10** : slide 8 re-rendue par `scripts/carrousel.py` (thème otea-production, Inter Display, Q5),
  même spec que le 13/10 au mot près sauf « Lien en bio. » devenu « Écrivez-nous en message. ». Les slides 1 à 7
  re-rendues sortent identiques au bit près aux PNG publiés. Nouvelle slide 8 : `7dcc4be2-a341-4637-bd3a-2e881c3564bb.png`
  (md5 0f5f8a036b851e09c718ae9d6d540aab, contrôlé sur CloudFront). La spec reste hors dépôt (bac à sable du 12/10).
- **Doublon 9ea5ec6b** : le 23/10 passe sur la photo 03 (171bb0cd, salle de conférence, orateur et public).
- **02/11** : réécrit sur le tri des images de l'année, ne reprend plus la slide 5 de l'A8.
- **Rattrapage, en brouillon** (la relève les arme) : 03/11 Noël IG+FB 402253293 (photo 08, 2dd6e51e, au lieu de
  5f97a127 qui ouvre le carrousel du 13/11 ; J-46 avant le 19/12) ; 05/11 « Les 3 questions » IG+FB 402253328
  (LinkedIn publié le 21/10) ; 10/11 « On n'a rien d'intéressant à filmer » 402253695 (sans tiret cadratin, photo 21
  62ec4b1e au lieu de la 42 en 2:3 déjà slide 7 de l'A8) ; 17/11 aftermovie 402253740 (photo 12, 42e049a6, à la place
  du visuel IA de juillet) ; 24/11 « La cohérence visuelle » 402253810 (photo 01, 08decdeb). Toutes en 3:2.
- **Contrôle final** : 21/10 au 30/11, 64 contenus (41 stories intactes, 23 posts), un post feed par créneau, aucun
  doublon, aucun post sans média, aucun placeholder.
- **Reste à traiter** : les 13 légendes de décembre portent encore « lien en bio » (et sans doute la dernière slide
  des carrousels du 02, 09, 16, 23 et 30/12) ; images en 2:3 hors de la plage feed : 26/10 (ba99c54d, déjà armé),
  13/11 (1fb3c4bc en 6e image) et 30/11 (96fe141e), ces deux derniers seront retenus par la relève ; le 12/11 reprend
  toujours la slide 4 de l'A8 ; 17 brouillons du 01 au 12/10 et stories en erreur des 18 au 21/10 non supprimés
  (proposition à Maxime).
