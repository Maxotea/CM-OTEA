---
name: smc-client
description: Cycle client SOCIAL MEDIA CEO — pipeline commercial (prospect → signé), onboarding et outboarding d'une mission, portail client, offres et tarifs, réponses types de customer care, témoignages et améliorations. Utilise ce skill quand l'utilisateur parle d'un prospect, d'une relance, d'un devis à faire, d'un nouveau client à démarrer, d'une mission qui se termine, d'une réponse à écrire à un client, d'un avis ou d'un témoignage, ou demande "où j'en suis avec X".
---

# Cycle client — SOCIAL MEDIA CEO

Référentiel : `.claude/references/social-media-ceo/01-bases-de-donnees.md` (CX), `.claude/references/social-media-ceo/02-taxonomies.md`.

## Les deux pipelines à ne pas confondre

**Pipeline commercial** (base `Contacts`, champ Statut) :
```
À contacter → Contacté → En contact → A rappeler → Appel découverte réservé
→ Faire un devis → Devis envoyé → En négo → Signé | Perdu
```

**Pipeline mission** (base `Gestion des missions`) — démarre après `Signé` :
```
Onboarding à faire → Onboarding en cours → Attente paiement
→ Mission à venir → Mission en cours → Outboarding en cours → Mission terminée
```

Un contact passe de `Prospect` à `Client` au moment de `Signé`. `Non converti` et
`Ancien client` existent : les utiliser plutôt que de supprimer une fiche.

## Toujours vérifier avant d'écrire à quelqu'un

1. Le champ **Ton utilisé** du contact (`Tutoiement` / `Vouvoiement`). Le respecter
   sans exception.
2. Le **dernier échange** (base `Suivi des échanges`) — ne jamais repartir de zéro.
3. Le **statut de facturation** en cours — on ne relance pas commercialement
   quelqu'un qui a une facture en `Mise en demeure`.

Toute interaction (mail, appel, visio, présentiel, vocal, courrier) se logge dans
`Suivi des échanges` avec un `Sujet` parmi : Prospection, Appel découverte, Offre,
Brief créatif, Suivi, Rencontre client, Relance impayé.

## Onboarding d'une mission

À faire dans cet ordre :

1. Créer la ligne dans `Gestion des missions` → statut `Onboarding à faire`,
   rattacher le client, le produit/service, la période.
2. Créer le **portail client** (`Portails clients`) : statut `Non débuté`, dates
   de prestation, équipe.
3. Émettre devis ou acompte (`Devis et factures`, type `Devis` ou `Acompte`).
4. Passer en `Attente paiement` jusqu'à encaissement.
5. Brief créatif → logger dans `Suivi des échanges` (sujet `Brief créatif`).
6. Créer les tâches d'amorçage (type `🫂 Client`).
7. Passer la mission en `Mission en cours` et le portail en `En cours`.

## Outboarding — l'étape qu'on oublie

`Outboarding en cours` est un statut à part entière. Il comprend :

- solde facturé et encaissé vérifié (`Solde mission` à zéro),
- livrables et accès transmis,
- **demande de témoignage** → créer la ligne dans `Témoignages`,
- **retour d'expérience** → alimenter `Améliorations clients` si quelque chose a
  frotté, avec le produit/service concerné,
- passage du contact en `Ancien client`,
- portail client en `Terminé`.

Seulement ensuite : `Mission terminée`.

## Customer care

La base `Customer Care : réponses types` est indexée par moment du cycle :
`STRUCTURE` · `AVANT MISSION/ACHAT` · `PENDANT MISSION` · `APRÈS-VENTE` ·
`PAIEMENTS` · `MARKETING / BUSINESS` · `FORMATION/UTILISATION` ·
`TROLLS / HATERS` · `AUTRES TEMPLATES`.

Quand l'utilisateur doit répondre à quelqu'un : identifier la catégorie, proposer
une réponse dans le bon ton, et suggérer de la sauvegarder comme réponse type si
le cas est susceptible de revenir. Une réponse type peut être reliée à un `Process`.

## Offres

`Produits et services` porte le prix HT, la TVA, le statut (`Idée`,
`En cours de création`, `Refonte`, `Actif`, `Inactif`), le CA facturé et le
nombre de missions. Avant de proposer un tarif, regarder ce qui a déjà été
facturé pour ce service et le `Tarif proposé` éventuellement noté sur le contact.

Ne jamais recommander un prix de façon péremptoire : présenter l'historique
(CA facturé, nombre de missions, tarifs pratiqués) et laisser la décision.

## Boucle d'amélioration

`Améliorations clients` → relié à un produit/service et à des tâches.
`Témoignages` → relié au client, au produit et éventuellement à une amélioration.
Un témoignage obtenu sans amélioration loggée est une occasion manquée : demander
systématiquement ce qui aurait pu être mieux.
