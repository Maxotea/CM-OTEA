# Gossip Beauty Center by Sarah (Argenteuil) — fiche client

## Gossip Beauty Center by Sarah (Argenteuil) — profil éditorial validé juillet 2026
- Prestations : coiffure, spa, bien-être, hammam, massage. Tarifs : NON vérifiés — à demander (lien Planity ou liste) avant tout calcul ROI.
- Ton : classe à prix abordable — vouvoiement élégant, chaleureux, jamais de promo inventée.
- SPÉCIFICITÉS CLÉS : salon EXCLUSIVEMENT FÉMININ (argument majeur : intimité totale, femmes voilées libres — à rappeler ~1x/mois) + communauté musulmane active dans la clientèle.
- Calendrier hégirien à intégrer CHAQUE trimestre (dates à revérifier par recherche web, elles reculent ~11 jours/an) : Ramadan (~fév-mars 2027 : adapter les horaires de contenu, contenus douceur/patience, JAMAIS de récupération commerciale), Aïd el-Fitr (~mars 2027 : vœux + mise en beauté de fête), Aïd al-Adha (~mai 2027 : vœux sobres), Mawlid (26 août 2026 ±1j : vœux sobres sans CTA).
- Règle religieuse : posts de vœux sobres, inclusifs (« à toutes celles qui le célèbrent »), sans CTA commercial. Le hammam se raconte comme tradition/transmission (Maghreb, entre femmes).

## Charte de couleurs officielle (fournie par Maxime le 06/08/2026)

| Couleur | Hex | Usage dans les carrousels |
|---|---|---|
| Rose vif | `#E4017C` | aplat de la slide CTA — c'est la couleur des murs du salon |
| Magenta | `#B2005F` | kickers, texte secondaire, mots accentués (4,70:1 sur rose poudré) |
| Rose poudré | `#F7C9DE` | fond des slides de contenu |
| Or | `#C9A66B` | photos et décors uniquement — **jamais du texte** (1,57:1 sur rose poudré) |
| Noir | `#0A0A0A` | titres et corps de texte, texte de la slide CTA |

## Le lieu réel (photos reçues le 06/08/2026, dossier Drive du client)

Les photos du salon corrigent une erreur d'appréciation : **Gossip est un lieu clair et rose, pas
un lieu sombre.**

- **Murs rose vif** `#E4017C` environ, à moulures et panneaux — c'est la signature visuelle du lieu
- **Sol bois clair**, presque blond
- **Mobilier beige et bouclette** — fauteuils, tables cannelées, assises texturées
- **Appliques et socles dorés**, néons LED blancs en arcs autour des miroirs
- **Vasques blanches**, robinetterie noire (le noir n'est qu'un détail, jamais une surface)
- **Hammam en travertin beige** et laiton, lumière chaude sous banquette — pas de pierre noire
- Enseigne « GOSSIP Beauty Center » rétroéclairée sur mur rose

**Conséquence pour toute génération IA** : rose vif dominant sur les murs, bois clair au sol,
textiles beige et crème, or brossé, blanc, lumière abondante. **Jamais de fond noir, jamais de
marbre sombre, jamais d'ambiance tamisée façon spa hôtelier** — c'était le contresens de la
première banque.

**Priorité absolue aux vraies photos.** Le salon est photogénique et les images existent
désormais : l'IA redevient ce qu'elle doit être, un dernier recours pour les sujets abstraits.

## Contrastes utilisables (mesurés)

Rose vif sur rose poudré ne fait que **3,13:1** — illisible, donc l'accentuation des carrousels
passe en magenta `#B2005F` (4,70:1). L'or `#C9A66B` sur rose poudré tombe à 1,57:1 : réservé aux
photos, jamais au texte. Sur rose poudré, le noir donne 13,5:1.

⚠️ **Ne jamais déduire une DA de mots d'ambiance.** La première banque avait été construite sur
« crème, beige, laiton » lus dans cette fiche, la deuxième sur une base noire déduite de la charte
seule. Ni l'une ni l'autre ne ressemblait au salon. Une DA se fonde sur des photos du lieu.

## Visuels IA (Higgsfield)
- **Élément de référence : `Gossip-Studio`** (id `9c0e5746-c1ab-4d0c-8b1e-3e5a3763992f`). DA : institut féminin chaleureux/lumineux — rose poudré, beige, crème, laiton doré, fleurs roses (pivoine, rose, orchidée), marbre crème, touches orientales pour le hammam (seau laiton, savon noir, zellige). **Jamais de visage.** Réutiliser `<<<9c0e5746-c1ab-4d0c-8b1e-3e5a3763992f>>>`.
- Banque IA locale COMPLÈTE (8 visuels) `medias/gossip-beauty-center/ia/` : hammam, massage, coiffure (salon), produits-cheveux, soin-visage, cocooning, accueil, octobre-rose.
- Attachement : **Instagram + Facebook**, 18h. `schedule_post` + `media01`=URL, `draft:true`, `autoPublish:false` → corriger heure (`bulk_update_post_times` à 18:00, change les IDs) → supprimer l'ancien. ⚠️ Rate limit Zapier après ~6 créations : procéder par vagues de 6 avec pause ~90s ; ~1 création/vague échoue avec `followUpQuestion` (résolveur de compte) → refaire avec instruction compte explicite ; les suppressions échouent parfois « Code execution error » mais suppriment quand même (vérifier via list). ⚠️ Le champ `hasMedia` de list_scheduled_posts est trompeur (indiquait true alors que media vide) → vérifier via `get_post_raw`.
- **STATUT BRANCHEMENT : ✅ TERMINÉ (22/07/2026)** — 64 posts feed branchés en rotation, vérif finale = 0 post sans média.

## Stories quotidiennes (créées 27/07/2026)
- **Banque de 7 stories 9:16** dans `medias/gossip-beauty-center/ia/stories/` — DA Gossip-Studio, texte info incrusté sur le visuel (vérifié sans coquille) : lundi `story-lundi-semaine` (BELLE SEMAINE + liste services), mardi `story-hammam` (LE RITUEL HAMMAM), mercredi `story-coiffure` (CÔTÉ COIFFURE — Coupe·Couleur·Soin), jeudi `story-massage` (INSTANT MASSAGE), vendredi `story-weekend-resa` (PENSEZ AU WEEK-END), samedi `story-feminin` (UN LIEU 100% FÉMININ), dimanche `story-dimanche` (DOUCEUR DU DIMANCHE).
- **Planifiées ✅ (27/07)** : 35 stories en brouillon du 28/07 au 31/08 à **10:00**, IG+FB, rotation hebdo jour↔visuel (27/07/2026 = un lundi ; 1re planif était décalée d'un jour → supprimée et recréée). Créées via la code action **`bulk_schedule_stories`** (écrite sur mesure : posts JSON [{date_time, text, media_url}] + blog_id + networks → STORY draft avec média, timezone Paris correcte = PAS de bug +7h, ~12 posts/appel en ~15s). Rester ≤12 posts/batch (timeout sandbox).
- Rotation réutilisable : la banque est hebdomadaire-générique (aucune date dans les visuels) → replanifier les mêmes 7 chaque semaine, ou régénérer des variantes. Contenu 100% conforme fiche : aucun prix/horaire inventé, texte sobre, jamais de visage (mains OK).
- ⚠️ 3 stories pré-existantes d'une planification antérieure ce même intervalle (29/07 18h, 31/07 17h30, 03/08 18h) — pas des doublons d'horaire, laissées en place. Mapping thématique : hammam→hammam/gommage/rituel/chaud-froid/héritage/5 piliers ; massage→massage/détente/sommeil/toucher/WWW ; coiffure→couleur/balayage/tendances/mythes ; produits-cheveux→soin cheveux/gras/pointes/bouclés/mouillés/chute/brossage/cuir chevelu ; soin-visage→peau/hydratation/stress-peau ; cocooning→septembre/pluie/staycation/weekend/lumière-sommeil ; accueil→institut/équipe/avis/coulisses/fidélité/cadeau ; octobre-rose→30/09 + 05/10 ; hammam (sobre)→entre-femmes ; cocooning (sobre)→Mawlid 26/08 à 10h.

## Carrousel hebdo (créneau du mercredi, 18h, Instagram + Facebook)
- **Typologie** : récurrence forte + forfaits à panier élevé → raisonner LTV, preuve par la régularité et la douceur. **Cible** : femme d'Argenteuil et alentours, souvent jamais venue en institut, qui craint de se tromper ou d'être jugée. Aucun jargon, vocabulaire sensoriel.
- **Archétypes prioritaires** : A7 (coulisses, lève la barrière d'entrée), A2 (erreurs), A5 (guide de choix), A8 (checklist saisonnière). A3 (avant/après) seulement avec accord écrit et sans allégation de résultat.
- **DA carrousel** (`scripts/themes.json` → `gossip-beauty-center`) : fond rose poudré #F7C9DE, titres noirs #0A0A0A, texte secondaire et accentuation magenta #B2005F, slide CTA en aplat rose vif #E4017C sur texte noir — le rose du mur du salon. Titres en bas-de-casse.
- ⚠️ **L'élément `Gossip-Studio` est périmé** : il produit des images crème et beige qui ne ressemblent pas au salon. À refaire à partir des vraies photos avant toute nouvelle génération.
- **Planifiés (spec dans `carrousels/gossip-beauty-center/`)** : 12/08 A7 « Le hammam étape par étape » (porte aussi le rappel mensuel « lieu 100 % féminin ») · 19/08 A2 « 5 erreurs qui abîment vos cheveux en été » · 26/08 A5 « Quel soin visage pour quelle peau » · 02/09 A8 « Cinq rendez-vous pour la rentrée ».
- **Réserve de sujets** : « Ce que le massage fait vraiment » (A7) · « Coloration : 5 idées reçues » (A4) · préparation des fêtes (A8, novembre) · Ramadan ~fév-mars 2027 : contenus douceur et patience, **jamais de récupération commerciale**, dates à revérifier par recherche web.
- **Vigilance** : **aucun tarif n'est vérifié pour ce compte** → ne jamais citer de prix dans un carrousel tant que la liste ou le lien Planity n'a pas été fourni. Aucune allégation médicale ni promesse de résultat. Si le Mawlid tombe le 26/08, le carrousel glisse au jeudi 27/08 et la journée reste au message de vœux sobre.
