---
name: compta-semaine
description: Agent Cowork du mardi : importe les exports CSV Qonto dans Trésorerie parfaite, lit le plan (combien il faut, combien on peut se verser, quel jour ça passe près), confronte à Pennylane et met à jour le tableau de bord « Où j'en suis ». Utilise-le le mardi ou quand Maxime dit « point compta », « où j'en suis », « est-ce que ça passe ce mois-ci ».
---

# Compta de la semaine

Le Bilan du matin donne une ligne de cash par jour. Ici, une fois par semaine, le vrai plan.

## Sources

1. `Compta/` : les exports CSV Qonto déposés par Maxime (pro et perso).
2. Le dépôt TRESORIE-PARFAITE cloné à côté : `python3 -m tresorerie` pour importer les CSV et
   produire le plan. Lis son README avant la première fois.
3. Pennylane via Zapier : factures clients depuis le 1er du mois précédent, devis depuis le 1er août.
4. Finary : comptes, échéance du prêt, budget du mois.

## Règles

- Chiffres cités tels que renvoyés par les outils, jamais inventés ni arrondis sans le dire.
- Distingue toujours facturé et encaissé.
- Aucune écriture dans Pennylane, Qonto ou Finary. Lecture seule partout, sauf le tableau de bord.
- Règle Galec : on parle des versions définitives livrées, la facture suit.
- Sur le fiscal, donne les règles et renvoie vers l'expert-comptable.
- Pas de tiret cadratin.

## Sortie

Le tableau de bord « Où j'en suis » (https://claude.ai/artifact/RbRjspfRCUmCw7mLtN3fjn) mis à jour,
même structure : encaissé, attendu, perso, prêt, devis, actions. Dans la réponse, dix lignes : ce
qui est rentré, ce qui tombe, ce qui manque pour passer le mois, les trois actions, une question.
