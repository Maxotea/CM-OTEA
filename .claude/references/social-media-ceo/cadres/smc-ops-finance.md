---
name: smc-ops-finance
description: Volet finances et administratif SOCIAL MEDIA CEO — devis, factures, échelle de relance des impayés, TVA, recettes et dépenses, clôture comptable mensuelle avec les enveloppes (URSSAF 25%, congés 10%, trésorerie 7%, projet 5%, rémunération), prévisionnel et suivi annuel. Utilise ce skill quand l'utilisateur parle de devis, de facture, d'impayé ou de relance, de TVA, de dépenses, de trésorerie, de son objectif de CA, ou veut faire sa clôture du mois. Ne donne jamais de conseil fiscal ou comptable personnalisé.
---

# Finances & administratif — SOCIAL MEDIA CEO

Référentiel : `.claude/references/social-media-ceo/01-bases-de-donnees.md` (finances), `.claude/references/social-media-ceo/02-taxonomies.md`.

> **Cadre.** Ce skill applique les règles de gestion du système SOCIAL MEDIA CEO.
> Il ne remplace ni un comptable ni un conseiller fiscal : présenter les chiffres
> et les règles, et renvoyer vers un professionnel pour toute décision fiscale.

## Devis et factures

Une seule base, trois types : `Devis`, `Acompte`, `Facture`.

**Fil devis** : `À faire` → `Transmis` → `Sans retours` → `Validé` | `Refusé` | `ANNULÉE`
**Fil facture** : `Ouverte` → `Relance 1` → `Relance 2` → `Partiellement payée` →
`Payée` | `Mise en demeure` → `Recouvrement`

Champs à ne pas oublier : `Montant HT`, `TVA` (20 % / 10 % / 5,5 % / sans),
`Date d'émission`, `Délai`, `Échéances de paiement` si paiement fractionné
(`✓ Paiement en plusieurs fois`), rattachement au contact, à la mission, au
produit et au mois de comptabilité.

Le TTC, la TVA, les soldes et les dates d'échéance sont **calculés**. Ne jamais
les saisir.

## Relancer un impayé

Séquence, à ne pas court-circuiter :

1. `Ouverte` — échéance dépassée : relance douce, ton du contact respecté.
2. `Relance 1` — rappel factuel avec la date d'échéance et le montant.
3. `Relance 2` — ferme, avec mention des pénalités si prévues au devis.
4. `Mise en demeure` — courrier formel. À ce stade, arrêter toute nouvelle
   production pour ce client.
5. `Recouvrement`.

Chaque relance se logge dans `Suivi des échanges` avec le sujet `Relance impayé`.
Consulter le champ `Ton utilisé` du contact avant de rédiger, et l'historique
(un bon payeur qui a un retard exceptionnel ne se traite pas comme un récidiviste).

## Recettes et dépenses

Chaque ligne : `Type` (Recette / Dépense), `Montant TTC`, `TVA` (20/10/8,8 %,
MIXTE, SANS — et `TVA mixte` en number si MIXTE), `Moyen de paiement`, `Date`,
`Fournisseur`, rattachement au mois et à la facture le cas échéant.

`Rapprochée` (checkbox) = ligne pointée avec le relevé bancaire. **Une clôture
avec des lignes non rapprochées n'est pas une clôture.**

## Clôture mensuelle

Saisies manuelles :
- Solde du compte bancaire
- Frais fixes
- Objectif du mois
- Nombre et montants de devis : validés / en attente / refusés ou ghostés

Puis vérifier : toutes les recettes et dépenses du mois rapprochées, toutes les
factures rattachées au bon mois comptable.

**Enveloppes appliquées automatiquement :**

| Enveloppe | Part |
|---|---|
| URSSAF + impôts | 25 % |
| Congés | 10 % |
| Trésorerie | 7 % |
| Projet X/Y | 5 % |
| Rémunération | le solde |

Ces pourcentages viennent du template. Si la situation de l'utilisateur diffère
(régime, TVA, charges), le signaler explicitement plutôt que d'appliquer les
chiffres aveuglément.

Lire ensuite : CA facturé HT, CA encaissé HT, dépenses TTC, TVA à payer,
bénéfices, solde de trésorerie, % de l'objectif atteint, et l'alerte TVA au niveau
annuel.

**Facturé ≠ encaissé.** Toujours distinguer les deux dans une réponse : c'est la
confusion la plus coûteuse.

## Prévisionnel

Lignes de recettes et dépenses attendues, avec `Réglée` (checkbox) et un solde
prévisionnel. Sert à voir venir un trou de trésorerie. À mettre à jour dès qu'un
devis est validé (recette prévue) ou qu'un engagement est pris (dépense prévue).

## Ce qui alimente les KPIs

Devis envoyés, factures envoyées, taux de conversion devis/facture, CA du mois,
évolution CA, revenu moyen. Tous calculés à partir de ces bases — d'où
l'importance des rattachements au mois.
