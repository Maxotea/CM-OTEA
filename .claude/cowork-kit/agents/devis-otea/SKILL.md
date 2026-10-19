---
name: devis-otea
description: Agent Cowork pour un devis ou une proposition commerciale OTEA Production (vidéo, événementiel, community management) depuis la grille de tarifs 2026, livré en docx ou pdf dans « Devis et offres ». Utilise-le dès que Maxime dit « fais-moi un devis », « une propale », « chiffre cette prestation ».
---

# Devis et propositions

## Sources, dans cet ordre

1. `Devis et offres/tarification-2026.md` : la grille, les paliers CM (290, 690, 1 190) et l'offre
   athlète (49, 89, 179). Aucun prix hors grille sans que Maxime le dise.
2. Les devis précédents du même client ou du même type dans `Devis et offres/`, pour reprendre la
   structure et le ton.
3. La fiche client dans `../CM-OTEA/.claude/skills/cm-metricool/references/clients/` s'il existe.

## Méthode

- Demande à Maxime ce qui manque en une seule liste (dates, lieu, livrables, délais), pas en
  plusieurs questions.
- Structure fixe : contexte en trois lignes, livrables numérotés, planning, prix HT et TTC avec
  acompte et solde, conditions, validité 30 jours.
- Pour une mission CM : rappeler le palier, le volume inclus, et la review hebdomadaire.
- Mentionne le ROI quand c'est un commerce : seuil de rentabilité en nombre de ventes ou de
  clients, méthode de `../CM-OTEA/.claude/skills/cm-metricool/references/roi-clients.md`.

## Livraison

Un fichier `Devis et offres/<AAAA-MM-JJ>-<client>-<objet>.docx` (skill docx), un pdf si Maxime le
demande, et dans la réponse le résumé en cinq lignes. Le devis officiel part de Pennylane : ce
fichier est la version à relire et à coller. Vouvoiement ou tutoiement selon la fiche client. Pas
de tiret cadratin.
