# SOCIAL MEDIA CEO — couche méthode

Le système Notion « SOCIAL MEDIA CEO » (formation Social Media Lab) transposé en
skills et documents de référence pour le projet CM OTEA.
Source : 36 pages, 4 boards, 33 bases de données.

## Fichiers

```
CLAUDE.md                                        contexte projet et règles transverses
.claude/references/social-media-ceo/
  ├── 00-architecture.md      la carte : 4 boards, 36 pages, dépendances entre bases
  ├── 01-bases-de-donnees.md  les 33 bases, champ par champ
  ├── 02-taxonomies.md        le vocabulaire contrôlé (statuts, piliers, catégories)
  ├── 03-workflow-contenu.md  le pipeline de production + arbitrage des piliers
  ├── 04-kpis.md              dictionnaire KPI et lecture des chiffres
  └── 05-rituels.md           quotidien / hebdo / mensuel / trimestriel
.claude/skills/
  ├── smc-contenu/            pipeline contenu, piliers, hashtags, recyclage
  ├── smc-client/             prospect → mission → outboarding, customer care
  ├── smc-kpi-review/         clôture KPI mensuelle, OKR, reporting client
  ├── smc-ceo-day/            vide-cerveau, tri GTD, revue hebdo, 90 days
  ├── smc-ops-finance/        devis, factures, relances, TVA, clôture
  └── smc-veille/             veille concurrentielle, offres et lancements
```

## Articulation avec cm-metricool

Le point de jonction est le statut `Prêt à programmer / publier` de la base
`Contenu` : en amont SOCIAL MEDIA CEO cadre (validation client, hashtags,
équilibrage), en aval `cm-metricool` programme dans Metricool.

**Piliers éditoriaux — arbitrage.** `cm-metricool` définit 5 piliers avec quotas,
SOCIAL MEDIA CEO en définit 6 sans quota. Sur un compte client les quotas
cm-metricool font foi ; les 6 piliers servent de taxonomie de classement. Sur le
contenu perso, ce sont les 6 piliers qui pilotent. Table d'équivalence dans
`03-workflow-contenu.md`.

## Ce qui a été repris, ce qui ne l'a pas été

**Repris** — l'architecture complète, les 33 schémas de bases avec leurs champs et
toutes les listes de valeurs, les pipelines (contenu, commercial, mission,
facturation), les règles de gestion financière, le dictionnaire KPI, les rituels.

**Non repris** — les données saisies dans les bases (le template est vide côté
contenu), la syntaxe des formules Notion (leur logique est décrite), les visuels.

Le Notion d'origine reste la source pour la manipulation des données. Ces fichiers
sont la couche méthode qui rend le système exécutable par Claude.

## À recalibrer

Les enveloppes financières (URSSAF + impôts 25 %, congés 10 %, trésorerie 7 %,
projet 5 %, rémunération = solde) viennent telles quelles du template Social Media
Lab. À ajuster au régime réel d'OTEA Production.
