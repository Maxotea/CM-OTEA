---
name: hyrox-veille
description: Veille résultats HYROX de Pierre Huiban, Antoine Bouhana et Julie Pekmezian. Repère une course dès que le résultat tombe sur HYRESULT, récupère chrono, classement, catégorie d'âge et splits, rend le visuel « résultat » dans la DA de Pierre (photo noir et blanc contrastée, léger masque sur Pierre, glow) et pose le post Instagram en brouillon à H+1 dans Metricool, puis prévient Maxime avec l'image. Utilise ce skill dès que Maxime parle du résultat ou du chrono d'une course de Pierre, Antoine ou Julie, d'un post « résultat », de la veille HYRESULT, d'ajouter un athlète à suivre, ou qu'il demande pourquoi un post de course n'est pas parti.
---

# Veille résultats HYROX — v1 (14/11/2026)

Demande de Maxime du 14/11/2026 : « repérer à chaque fois que Pierre, Julie ou Antoine font une
course, récupérer les stats, et anticiper un post dans l'heure avec une photo ».

Le skill parent est `cm-hyrox` : ses règles valent ici (aucun chiffre non vérifié, voix de
Pierre, anglais, aucun « LFG », partenaires cités tels que la fiche les donne).

## Ce qui tourne tout seul

`.github/workflows/hyrox-veille.yml`, toutes les 20 minutes de 6 h à 22 h UTC :

1. **Détection** — `scripts/hyrox_veille.py` lit la fiche HYRESULT de chaque athlète de
   `hyrox/veille.json` (`hyresult.com/athlete/<slug>`) et compare aux résultats déjà vus
   (`hyrox/veille-etat.json`). Un doubles Pierre + Antoine ne fait qu'un post : la clé est
   l'identifiant du résultat, pas l'athlète.
2. **Chiffres** — fiche résultat : chrono, rang / classés, rang et catégorie d'âge, division
   (lue dans le lien de classement), splits des stations. Fiche sans chrono = course en cours :
   rien n'est posté, on repasse 20 minutes plus tard.
3. **Visuel** — `scripts/hyrox_visuel.py`, 1080×1350, DA « trois vies » : registre ATHLETE
   allumé, label `HYROX <VILLE> · <DIVISION>`, titre Fraunces, chrono JetBrains Mono, rang et
   catégorie en accent aube, pied ROAD TO HONG KONG · JUNE 2027. **Photo : toujours en noir et
   blanc contrasté, léger masque qui relève Pierre, glow** (`.claude/memories/pierre-photo-nb-glow.md`).
   La photo vient du stock `photos/pierre-huiban.json` (vraies photos, masque de détourage
   rangé dans `photos/pierre-huiban/masques/`), en rotation.
4. **Post** — Instagram, daté à **maintenant + 60 min** arrondi au quart d'heure, dans la plage
   07:00–22:30 (au-delà : 07:00 le lendemain). **Créé en brouillon** (règle n°1 du `CLAUDE.md`).
   `armer_auto: true` dans `hyrox/veille.json` le passerait en publication automatique comme la
   relève `validation_auto` ; c'est `false` tant que Maxime ne l'a pas demandé.
5. **Notification** — `NOTIF_WEBHOOK` (Zapier → WhatsApp / SMS) et une issue GitHub
   `veille-hyrox` avec l'image et le lien Metricool. C'est là que Maxime récupère l'image pour
   la transférer en WhatsApp.

## Ce que Maxime (ou Claude en session) fait ensuite

- **Remplacer la photo d'attente** par une photo de la course dès qu'elle arrive : la rendre
  avec `python3 scripts/hyrox_visuel.py PHOTO.jpg SPEC.json SORTIE.jpg --masque M.png`, en
  détourant la photo une fois (Higgsfield `remove_background`, alpha réduit à 900 px de haut,
  rangé dans `photos/pierre-huiban/masques/`). Jamais une photo générée.
- **Ajouter un mot de Pierre** à la légende s'il en donne un. La légende automatique ne
  contient que la fiche : aucun ressenti, aucune anecdote inventée.
- **Valider** le brouillon dans Metricool.

## Rejouer, tester, corriger

| Besoin | Commande |
|---|---|
| Voir ce que donnerait un résultat | `python3 scripts/hyrox_veille.py --resultat <ID> --dry-run` (visuel dans `hyrox/visuels/`) |
| Reposter un résultat déjà vu | Action « Veille résultats HYROX », champ `resultat` |
| Repartir de zéro sans reposter l'historique | `python3 scripts/hyrox_veille.py --initialiser` |

Un échec est réessayé à chaque passage, signalé une seule fois, abandonné au 3e.

## Ajouter un athlète

Une ligne dans `hyrox/veille.json` → `athletes` : `slug` HYRESULT (fin de l'URL
`hyresult.com/athlete/<slug>`), prénom, `instagram` s'il est **donné par Maxime** (jamais un @
deviné), `compte` = clé d'un compte de `comptes` ou `null`. Avec `null`, la course est détectée
et notifiée, sans post. Un compte à soi demande un stock photo (`photos/<compte>.json` avec
masques) et une entrée dans `comptes` ; le pied et les hashtags y sont propres à l'athlète.

## État au 14/11/2026

- Pierre : compte `pierre-huiban` (blogId 6572293), stock de 2 photos (77 tapis néon, 85 arche
  de course). 86 écartée tant que le sujet n'est pas confirmé.
- Antoine (@antoine_bhna) et Julie : **pas de compte Metricool** connu → notification seule
  quand ils courent sans Pierre ; avec Pierre, le post part sur le compte de Pierre et les tague
  (Antoine par son @, Julie par son nom, son compte Instagram n'étant pas connu).
- Historique (42 résultats) marqué vu le 14/11/2026 ; Cairo 2026 posé à la main le même jour.
- Secrets utilisés : ceux des carrousels (`METRICOOL_USER_ID`, `METRICOOL_TOKEN`,
  `IMGBB_API_KEY`) et de la review (`NOTIF_WEBHOOK`).
