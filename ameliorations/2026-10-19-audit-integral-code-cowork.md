# Audit intégral : Claude Code, Cowork, compte, 19/10/2026

Suite de l'audit du 16/10 (qui ne regardait que le dépôt CM-OTEA et les routines). Ici : les
12 dépôts GitHub, les 19 skills du compte (ceux que Cowork et la conversation chargent partout),
et le plugin small-business. Verdict en une phrase : **la même connaissance CM vit à trois ou
quatre endroits avec des règles contradictoires, et une de ces copies dit à Claude de publier
directement.**

## 1. Ce que je vois, ce que je ne vois pas

Vu : les 12 dépôts (clonés et inventoriés), les 19 skills synchronisés du compte, le plugin
small-business, les routines.

Pas vu : les Projets claude.ai, les conversations, les tâches planifiées locales de Cowork, le
dossier de travail Cowork lui-même. Si une copie de ces contenus y vit, je ne peux pas le savoir.

## 2. Constat critique : deux skills du compte contredisent la règle n°1

Les skills `cm-otea` et `cm-b2c` sont installés **au niveau du compte** : ils se chargent dans
Cowork, dans la conversation et dans toute session Code, quel que soit le dépôt. Tous deux disent :

> Média avec URL publique : post complet planifié (`draft: false`, `autoPublish: true`).

La règle non négociable n°1 de `CLAUDE.md` dit l'inverse : tout en brouillon, seule exception OTEA
Production et Otea Filmakers via la relève GitHub. `CLAUDE.md` n'est lu que dans une session ouverte
sur le dépôt. Une session Cowork ou une conversation qui déclenche `cm-otea` sur « planifie le mois
de La Galerie » publiera donc directement. Le skill `cm-hyrox` du dépôt CM-BTOC a la même règle
(brouillon seulement si placeholder).

Autres écarts du `cm-otea` du compte : table des comptes datée d'août 2026 (Le Loft et Gossip
actifs, Pierre Huiban, ConfShine et Run On Invest absents), pas de carrousel du mercredi, pas de
review client, pas de règle sur les vraies photos et les stories.

**Décision proposée : remplacer `cm-otea` et `cm-b2c` du compte par des skills d'aiguillage** (deux
lignes : « le CM se fait dans le Projet du client ou dans le dépôt CM-OTEA, tout reste en
brouillon »). Textes prêts dans `.claude/cowork-kit/skills-compte/`. Je ne peux pas modifier les
skills du compte depuis ici : le dossier synchronisé est en lecture descendante.

## 3. Les 12 dépôts, et où chacun devrait vivre

| Dépôt | Dernier commit | Contenu | Verdict |
|---|---|---|---|
| **CM-OTEA** | 19/10 | moteur CM : 30 scripts Python, 99 tests, 4 workflows, 2 skills, mémoires | **Code, reste** |
| **PROSPECTION** (OTEA Moteur) | 29/09 | app Node locale : Ma journée, campagnes, autopilote, CRM gamifié | **Code, reste** ; chevauche le Bilan du matin (voir §5) |
| **MONTAGE-OTEA** (PostCam) | 12/10 | 45 scripts Python, outils DaVinci, `hyrox/` (splits, builder Resolve), AIIRF, Galec | **Code, reste** ; doit accueillir le skill hyrox du compte |
| **ACHILLE** | 31/08 | app TypeScript Cloudflare, Strava | **Code, reste** ; projet annexe |
| **TRESORIE-PARFAITE** | 12/10 | outil Python de plan de trésorerie, imports CSV, sync Pennylane | **Code, reste** ; contient `docs/etude-prix-cm.md` qui n'a rien à y faire |
| **RECMYRUN** | 27/09 | site Node athlète / vidéaste | **Code, reste** ; projet annexe |
| **makepeople-game** | 22/09 | jeu TypeScript (694 fichiers, 54 Mo), 5 workflows, skill `rituel-quotidien` | **Code, reste** ; `marketing/` et `ONBOARDING-CM-MAKEPEOPLE.md` sont du CM, pas du jeu |
| **COMMENT-** (ExpliqueMoi) | 21/08 | 28 JSON, 9 SRT, 13 md : la mémoire de production de la chaîne TikTok | **Données de la routine**, reste tant que la routine existe (désactivée depuis le 16/10) |
| **CM-BTOC** | 24/08 | 23 fichiers : skill `cm-hyrox` (298 lignes, 344 Ko), formulaires Apps Script, dossier athlète | **À fondre dans CM-OTEA** (fait ce jour, voir §6), puis archiver |
| **MAKEPEOPLE** | 29/07 | 8 fichiers, ancienne version du jeu sur Vercel | **Archiver** (remplacé par makepeople-game) |
| **STRUCTUREOTEA** | 03/09 | 1 README : « journal de bord de ma vie pour un documentaire » | **Pas un dépôt** : Cowork ou Projet « Journal » |
| **SITE-OTEA-PRODUCTION** | 03/09 | 1 README vide | **Archiver** ou y mettre vraiment le site |

Trois dépôts sur douze ne contiennent pas de code. Deux autres mélangent code et contenu CM.

## 4. La connaissance CM, quatre copies

| Contenu | CM-OTEA | CM-BTOC | compte `cm-otea` | compte `cm-b2c` |
|---|---|---|---|---|
| Moteur CM (étapes, piliers, Metricool) | `cm-metricool` (135 lignes) | `cm-hyrox` (298 lignes) | 184 lignes | 203 lignes |
| `metricool-api.md` | mémoires `bulk-schedule-stories` | oui | oui (identique à cm-b2c) | oui |
| Fiche Pierre Huiban | 21,5 Ko, à jour (routines) | 16 Ko, août | non | non |
| Règle brouillon | **oui, non négociable** | non | **non, publie** | **non, publie** |
| Carrousel, review client, stories vraies photos | oui | non | non | non |
| Paliers et offre | `offre/tarification-2026.md` | `offre-athlete.md` (49/89/179) | `paliers-offre.md` | `offre-b2c.md` |

Une seule source doit rester : **CM-OTEA**. Les trois autres deviennent soit un skill du dépôt
(cm-hyrox), soit un aiguillage (compte), soit une archive (CM-BTOC).

## 5. Les doublons entre routines, dépôts et skills du compte

- **Le Bilan du matin et OTEA Moteur « Ma journée »** font la même chose : lire Gmail et l'agenda,
  sortir les 3 actions du jour. Le bilan lit même le mail d'OTEA Moteur pour en extraire 3 lignes.
  Deux moteurs pour une to-do. À trancher : soit OTEA Moteur produit la to-do et le bilan ne fait
  que la boîte mail et l'argent, soit l'inverse. Je penche pour garder OTEA Moteur sur la
  prospection (son métier) et le bilan sur le reste.
- **Trésorerie parfaite, le Point compta (fondu dans le bilan) et Finary** : trois lectures de la
  même trésorerie. L'outil Python est le seul qui produit un plan ; le bilan devrait lire sa sortie
  plutôt que refaire le calcul depuis Pennylane.
- **`hyrox-splits-montage` (compte) et `montage-otea/hyrox/hyrox_splits.py`** : le skill fait à la
  main (WebFetch sur HYRESULT, calcul Python dans la conversation) ce que le dépôt fait en script.
  Le skill doit devenir un skill du dépôt MONTAGE-OTEA qui appelle le script. Texte prêt dans le kit.
- **`reel-script` et `reel-lint`** : à leur place au niveau du compte (écriture, utilisés partout).
- **`morning`** : ne servait qu'au Résumé matinal, désactivé. À retirer du compte.
- **Plugin small-business** (une quarantaine de skills, outils anglo-saxons : Gusto, Xero, MYOB,
  QuickBooks, Square) : chargé dans toute session alors que la compta est sur Pennylane et Qonto.
  Deux skills utiles au plus (`inbox-manager`, `invoice-chase`). À désactiver dans Code, à garder
  dans Cowork seulement si tu t'en sers.

## 6. Ce qui est fait ce jour

- `cm-hyrox` importé de CM-BTOC dans `.claude/skills/cm-hyrox/` de CM-OTEA, avec trois corrections :
  la règle brouillon alignée sur `CLAUDE.md`, son `metricool-api.md` remplacé par un renvoi vers
  les mémoires du dépôt, sa fiche Pierre Huiban d'août retirée au profit de celle de `cm-metricool`
  (la plus récente, celle que les routines lisent). Les formulaires Apps Script et le dossier
  athlète suivent.
- Kit Cowork écrit dans `.claude/cowork-kit/` : arborescence du dossier de travail, cinq agents
  Cowork (review du vendredi, récap du lundi, devis, tri des médias, compta de la semaine), deux
  skills d'aiguillage pour remplacer `cm-otea` et `cm-b2c` dans le compte, un skill
  `hyrox-splits` pour MONTAGE-OTEA. Export en zip par `scripts/export_projets_claude.py`.
- `organisation-claude.md` : la carte des dépôts ajoutée au routage.

## 7. Ce qui reste à faire, et par qui

| Action | Qui | Durée |
|---|---|---|
| Remplacer `cm-otea` et `cm-b2c` dans les skills du compte par les deux aiguillages du kit (**urgent : règle brouillon**) | Maxime | 5 min |
| Retirer `hyrox-splits-montage` et `morning` du compte | Maxime | 2 min |
| Archiver CM-BTOC, MAKEPEOPLE, SITE-OTEA-PRODUCTION sur GitHub | Maxime | 5 min |
| Créer le dossier Cowork « OTEA » depuis le kit, y installer les cinq agents | Maxime | 30 min |
| Déplacer `marketing/` et `ONBOARDING-CM-MAKEPEOPLE.md` de makepeople-game vers une fiche client MAKE PEOPLE dans CM-OTEA | Claude sur demande (dépôt en lecture seule ici) | 20 min |
| Déplacer `docs/etude-prix-cm.md` de TRESORIE-PARFAITE vers `offre/` de CM-OTEA | Claude sur demande | 5 min |
| Poser le skill `hyrox-splits` dans MONTAGE-OTEA | Claude sur demande (accès push à donner) | 10 min |
| Trancher le doublon Bilan du matin / OTEA Moteur | Maxime | décision |
| Désactiver le plugin small-business dans Code | Maxime | 2 min |
