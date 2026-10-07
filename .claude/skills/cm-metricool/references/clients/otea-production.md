# OTEA PRODUCTION — fiche client

## OTEA PRODUCTION (oteaproduction.com) — profil validé juillet 2026
- Production audiovisuelle B2B : vidéo d'entreprise, captation événementielle (séminaires, salons, aftermovies), interviews/marque employeur, drone, style cinématique (Sony FX3, étalonnage chaud). Otea Filmakers (blogId 4728418) = marque vitrine créative/voyage, à traiter séparément.
- Réseaux posts texte : Instagram + Facebook + LinkedIn (TikTok et YouTube = vidéo uniquement). Horaire B2B : 12h00. Ton : vouvoiement pro accessible, expert qui challenge, CTA « lien en bio » vers devis/portfolio.
- Typologie ROI : B2B projet — devis variables (demander les fourchettes de devis moyens au user) ; 1 projet signé couvre largement la prestation CM ; compter aussi les leads qualifiés (DM, calls découverte).
- Temps forts annuels : rentrée = budgets Q4/plans com ; SEPT-OCT = pousser les VŒUX vidéo de fin d'année (se tournent en oct-nov, jamais en déc) ; salons d'automne ; janvier = plans annuels.

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

## Validation hebdo à deux semaines d'avance (07/10/2026)
Maxime a demandé le même circuit que Pierre Huiban : dossier Drive « Validation hebdo — OTEA PRODUCTION » (`1GeMYG_myNbXPTY9W3K8YLdSAm2jJwofw`, Archives `1JQI4xUCI1yuZ2MfBCNiv_UjXbScFIDfB`), tableaux des semaines du 12-10 et du 19-10 déposés. Config dans `reviews/config.json` (PR #56). Le dossier n'a aucun partage par lien : à passer en Éditeur pour que la relève le lise. À reprendre : le post du 21/10 (« Les 3 questions à te poser ») tutoie alors que le compte vouvoie.
