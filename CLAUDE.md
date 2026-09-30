# SOCIAL MEDIA CEO — contexte projet

Système de gestion issu de la formation Social Media Lab, transposé pour le
projet **CM OTEA**. Source : Notion « SOCIAL MEDIA CEO » (36 pages, 4 boards,
33 bases de données).

## En une phrase

Quatre tableaux de bord — **OPS** (piloter), **BRAIN** (capitaliser),
**CX** (les clients), **CONTENT** (produire) — assis sur un socle unique de
bases de données partagées. Une donnée n'existe qu'à un seul endroit.

## Où trouver quoi

| Fichier | Contenu |
|---|---|
| `.claude/references/social-media-ceo/00-architecture.md` | la carte des 4 boards et des 36 pages, les dépendances entre bases |
| `.claude/references/social-media-ceo/01-bases-de-donnees.md` | les 33 bases, champs par champ |
| `.claude/references/social-media-ceo/02-taxonomies.md` | le vocabulaire contrôlé — statuts, piliers, catégories |
| `.claude/references/social-media-ceo/03-workflow-contenu.md` | le pipeline de production de contenu |
| `.claude/references/social-media-ceo/04-kpis.md` | le dictionnaire KPI et la lecture des chiffres |
| `.claude/references/social-media-ceo/05-rituels.md` | les boucles quotidienne, hebdo, mensuelle, trimestrielle |
| `.claude/references/public-apis/README.md` | le catalogue public-apis (1 958 API gratuites), la sélection utile pour OTEA et comment le brancher sur Claude |

## Les skills

| Skill | Déclenche sur |
|---|---|
| `smc-contenu` | idée, calendrier, piliers, validation client, hashtags, recyclage |
| `smc-client` | prospect, relance, devis, onboarding, mission, réponse client, témoignage |
| `smc-kpi-review` | bilan du mois, performances, reporting client, OKR |
| `smc-ceo-day` | point hebdo, tri des idées, planification trimestrielle |
| `smc-ops-finance` | devis, facture, impayé, TVA, trésorerie, clôture |
| `smc-veille` | analyse concurrent, offre ou lancement du marché |

## Articulation avec les skills existants

- **`cm-metricool`** — le calendrier calé sur l'actualité du secteur, la rédaction
  des légendes et la programmation Metricool. Point de jonction : le statut
  `Prêt à programmer / publier` de la base `Contenu`. En amont c'est SOCIAL MEDIA
  CEO (cadrage, validation client, hashtags), en aval c'est `cm-metricool`.

  **Conflit de piliers, arbitré :** `cm-metricool` définit 5 piliers avec quotas
  (P1 30 %, P2 25 %, P3 20 %, P4 15 %, P5 10 %), SOCIAL MEDIA CEO en définit 6
  sans quota. Sur un **compte client, les quotas cm-metricool font foi** ; les
  6 piliers ne servent que de taxonomie de classement. Sur le **contenu perso**,
  ce sont les 6 piliers qui pilotent. Table d'équivalence dans
  `.claude/references/social-media-ceo/03-workflow-contenu.md`.
- **`reel-script` / `reel-lint`** — l'écriture et la notation des vidéos courtes,
  appelées depuis le statut `Rédaction` / `Tournage`.

## Règles permanentes du CM (non négociables)

Ces deux règles priment sur toute autre considération d'exécution. Elles
vivaient dans les mémoires Claude, hors du repo — elles sont désormais
versionnées dans `.claude/memories/` pour survivre à tout changement de poste.

1. **Tout contenu créé dans Metricool reste en BROUILLON** (`draft:true`,
   jamais `autoPublish`). Maxime valide lui-même dans l'interface. Toute code
   action qui crée du contenu doit vérifier le `draft` après création.
   → `.claude/memories/autonomie-decisions-cm.md`
2. **Les stories partent des VRAIES photos du client, animées en IA.**
   Deux choses distinctes, à ne pas confondre (règle reprécisée le 21/08/2026) :
   - ✅ **L'animation i2v est la méthode standard**, sur tous les comptes. Un
     simple mouvement de caméra ffmpeg (`zoompan`) ne suffit pas — Maxime l'a
     refusé le 01/08 (« pas des images animées mais juste des zooms »). Il veut
     du vrai mouvement dans l'image. Le `zoompan` n'est qu'un secours si un
     visage se déforme malgré le prompt renforcé.
   - ⛔ **Les images 100 % générées par IA restent interdites** sur un compte
     qui possède de vraies photos. C'est ce que William du Loft a reproché le
     21/08 : « 80 % des posts sont des photos qui ne sont pas prises chez moi ».
     Elles ne sont autorisées que sur un compte **sans aucune banque photo**, et
     compte par compte (Run On Invest, accordé le 04/08/2026).
   Prompt i2v **verrouillé sur l'identité** et **contrôle de la dernière frame**
   contre la photo source avant de brancher quoi que ce soit.
   → `.claude/memories/stories-vraies-photos-sans-ia.md`
   → Chaîne complète validée le 28/08/2026 (crop 9:16 → i2v → plein cadre
     1080×1920 → texte en overlay → muette → brouillon) :
     `.claude/memories/story-video-plein-cadre.md`
   - **Limite absolue, quel que soit le compte : aucune personne réelle
     identifiable générée.** On ne fabrique jamais le visage d'un client, d'un
     participant ou de Maxime.
3. **Aucune bande son sur les vidéos de story.** Elles partent muettes, Maxime
   ajoute l'audio dans Instagram au moment de valider.
   → `.claude/memories/stories-sans-son.md`

Index complet des mémoires : `.claude/memories/MEMORY.md`.

## Règles transverses

1. **Ne jamais inventer une valeur de statut, de pilier ou de catégorie.** Les
   listes fermées sont dans `.claude/references/social-media-ceo/02-taxonomies.md` ; les vues et formules
   en dépendent.
2. **Ne jamais écrire dans les bases « publiée ne pas toucher »** (Contenu,
   Portail client, Plateformes) : ce sont des vues techniques.
3. **Ne jamais saisir un champ formule ou rollup**, en particulier ceux dont le
   nom contient « (affichage) ».
4. **Respecter le champ `Ton utilisé`** (tutoiement / vouvoiement) de chaque
   contact dans toute rédaction.
5. **Distinguer facturé et encaissé** dans toute réponse financière.
6. **Rattacher au mois** : sans rattachement, les KPIs et la compta sont faux.
7. Sur les questions fiscales, comptables ou juridiques : donner les chiffres et
   les règles du système, renvoyer vers un professionnel pour la décision.
