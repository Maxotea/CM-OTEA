# PASSATION — reprise du CM OTEA dans ce repo (état au 31/07/2026)

Ce repo (CM-OTEA) est désormais LA source de vérité de l'outil CM Premium. L'ancienne session (MAKEPEOPLE) ne pouvait pas y accéder — ce fichier transmet tout son état.

## Installation (si pas encore fait)
Dézipper ce paquet à la racine, puis : `git mv claude .claude && git commit -m "Install cm-metricool skill" && git push -u origin main`

## État Metricool (userId 3689627, 9 brands)
| Compte | blogId | Couvert jusqu'au | Notes |
|---|---|---|---|
| jlawsongolf | 6563137 | 23/10 | Posts Open Ryan Fox publiés ; ✅ placeholder [VAINQUEURE] AIG Women's Open COMPLÉTÉ le 02/08 (Shiho Kuwaki, post 357057266, brouillon) — WITB abandonné faute de source fiable, voir la fiche client |
| LE LOFT | 6191921 | 23/10 | Nettoyé (posts Hyrox migrés vers pierrehuiban89 en juillet) |
| Gossip Beauty Center | 5733306 | 23/10 | |
| La Galerie Immobilière | 5733302 | 23/10 | |
| OTEA PRODUCTION | 5733269 | 23/10 | 12 doublons supprimés le 20/07, calendrier propre |
| Otea Filmakers | 4728418 | 18/09 | 26 brouillons lifestyle fondateur ; batch 3 (21/09→16/10, 12 posts) rédigé mais NON poussé (validation du ton par Maxime en attente) |
| pierrehuiban89 | 6572293 | 29/08 | 14 posts dont annonce sponsors KAIRYN/GX Society/Split Nutrition ; PROLONGATION BLOQUÉE : demander à Maxime le calendrier réel de compétitions |
| Confshine Game | 6625190 | RIEN | ⚠️ URGENT : lancement LUNDI 03/08. 10 posts rédigés dans references/clients/confshine-game.md + calendrier-lancement (voir fiche). AUCUN réseau connecté au brand au 28/07 → vérifier que l'Instagram est lié, puis pousser les 10 posts via bulk_schedule_posts |
| brand sans nom | 6636615 | — | Vide, créé par erreur ? Demander à Maxime s'il faut le supprimer |

## Automatisation comptes rendus hebdo (references/compte-rendu-hebdo-clients.md)
- Politique validée : WhatsApp canal principal TOUS clients + doublon email. Mode brouillon (jamais d'envoi auto).
- ❌ La Routine serveur (lundi 9h Paris = cron 0 7 * * 1 UTC en été) N'A PAS PU être créée depuis l'ancienne session → LA CRÉER depuis cette session (create_trigger, connectors Zapier+Gmail).
- ❌ Coordonnées clients (WhatsApp + email) toujours pas fournies par Maxime → à collecter, puis remplir les champs dans chaque fiche.

## Jeux concours (préparés, en attente d'accord clients)
Fichier envoyé à Maxime le ~28/07 : 8 concours (lots : fitting 160 €, head spa 60 €, autres à confirmer). Ne rien planifier sans accord écrit du client sur le lot.

## Points de vigilance
- Zapier/MCP : erreurs "requires approval" intermittentes — retenter après reconnexion du serveur, ne jamais spammer.
- bulk_schedule_posts crée en brouillon (draft) nativement, fuseau Paris fiable. schedule_post unitaire a un bug de fuseau (voir SKILL.md étape 6).
- Règle d'or : jamais de date/prix/résultat inventé — toujours vérifier par recherche web.
