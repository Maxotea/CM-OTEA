# Rattacher le compte publicitaire d'un client

Une campagne client ne se crée jamais sur le compte pub de Maxime : le budget
est l'argent du client, la facture Meta doit être à son nom, et l'historique
de son compte lui appartient s'il part. L'agence travaille en **accès
partenaire**.

## Côté OTEA Production, une fois pour toutes

1. Créer un **Business Manager OTEA Production** (business.facebook.com),
   y rattacher la page OTEA Production et le compte pub Maks Otéa.
   Au 02/09/2026 le compte pub est personnel (`business_id` vide) : il ne peut
   ni recevoir un accès partenaire ni en donner.
2. Rattacher les comptes Instagram @oteaproduction et @oteafilmakers au
   Business, puis au compte pub. Sans ça `ads_get_ig_accounts` reste vide.
3. Poser le pixel Meta sur oteaproduction.com (Gestionnaire d'événements),
   noter `pixel_id` dans le registre.
4. Accepter les conditions Lead Ads sur chaque page qui fera des formulaires
   (https://www.facebook.com/legal/leadgen/tos).

## Côté client, à faire ensemble (30 minutes en visio)

1. **Il a un Business Manager** : il ajoute OTEA Production comme
   partenaire sur son compte pub (rôle « Gérer les campagnes ») et sur sa page
   (rôle « Créer des publicités »). Il ajoute aussi son Instagram si ce n'est
   pas fait.
2. **Il n'en a pas** : on le crée avec lui, à son nom, avec son adresse. On
   y transfère sa page, on crée le compte pub, il enregistre **sa** carte.
   L'agence n'est jamais titulaire du moyen de paiement.
3. Relever avec `ads_get_ad_accounts` (id, devise, minimum journalier,
   `has_payment_method`), `ads_get_pages_for_business` ou
   `ads_get_ad_account_pages` (page, `leadgen_tos_accepted`),
   `ads_get_ig_accounts` (Instagram).
4. Fixer par écrit avec le client : budget mensuel maximal, plafond par
   campagne, qui valide quoi. Ces trois lignes vont dans `plafonds` et
   `notes` du registre.
5. Repérer la **catégorie spéciale** : immobilier → HOUSING, crédit → CREDIT,
   emploi → EMPLOYMENT. La noter dans le registre ; elle se déclare sur chaque
   campagne.
6. Renseigner `dsa_payor` (qui paie Meta : le client) et `dsa_beneficiary`
   (qui bénéficie : le client, ou sa marque).

## Entrée du registre

Copier un bloc de `campagnes/comptes.json`, remplir, passer `actif` à `true`
seulement quand `ad_account_id`, `page_id`, `dsa_*` et `plafonds` sont là.
Puis `python3 scripts/campagne.py liste` pour vérifier qu'il n'est plus dans
les « clients sans compte pub rattaché ».

## Ce qui reste dû sur le banc d'essai (02/09/2026)

- Business Manager OTEA Production : à créer.
- Instagram @oteaproduction et @oteafilmakers : à rattacher au compte pub.
- Page OTEA Production : à confirmer comme signataire sur le compte Maks Otéa
  (elle n'apparaît pas dans `ads_get_ad_account_pages`).
- Pixel oteaproduction.com : à poser.
