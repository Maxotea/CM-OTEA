---
name: bulk-schedule-stories-metricool
description: "Code action Zapier sur mesure pour créer des stories Metricool en masse (brouillon, média, heure Paris exacte)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 554c009b-345e-4df0-8ba6-f1dbfb275952
  modified: 2026-07-29T12:24:04.105Z
---

Code action `code_action_metricoolcliapi__bulk_schedule_stories` (créée 27/07/2026 via write_code_action, API MetricoolCLIAPI). Params : `blog_id`, `networks` (JSON ex `["instagram","facebook"]`), `posts` (JSON array de `{date_time:"YYYY-MM-DDTHH:mm:ss", text, media_url}`). Crée des **STORY en brouillon** avec média, `timezone: Europe/Paris` exacte → **pas de bug +7h**, ~12 posts par appel en ~15 s (rester ≤12/batch pour éviter le timeout sandbox). ~10× plus rapide que `schedule_post` unitaire et sans résolveur LLM (zéro risque de mauvais compte). Renvoie `{date_time, success, post_id}` par post. Utilisée pour planifier 190 stories d'août 2026 sur les 6 comptes ([[hebergement-photos-reelles-metricool]] pour héberger les visuels). Adaptable : le même pattern write_code_action peut produire un bulk pour les POSTs feed.

**Actions sœurs créées le 29/07/2026** : `bulk_replace_posts` (items [{old_post_id, date_time, text, media_url}] + networks → crée le POST feed remplaçant en brouillon avec heure Paris exacte puis supprime l'ancien — LA méthode pour changer un visuel) et `bulk_delete_posts` (post_ids array). ⚠️ Piège découvert : le **PUT** /scheduler/posts de Metricool ne remplace pas le média (répond 200, parfois recrée le post sous un nouvel ID → doublons fantômes). Toujours passer par replace+delete, jamais par update.

⚠️ **Bug corrigé le 29/07/2026** : la 1ʳᵉ version de `bulk_replace_posts` créait les posts en `draft:false` malgré les requirements (code Zapier généré déviant) → 6 posts feed OTEA ont dû être re-remplacés. La version actuelle fait une **vérification obligatoire post-création** (GET du post créé, `draft_verified` dans le résultat, rollback si non-draft). Règle : toute nouvelle code action qui CRÉE du contenu doit inclure cette vérification draft, et après tout gros batch, relire un échantillon avec les champs `draft`/`autoPublish`.

**Sémantique API (vérifiée par témoin)** : le GET renvoie fidèlement `draft` ; `detailedStatus` des providers est TOUJOURS « Pending » (ne distingue pas brouillon/programmé). 3 états : `draft:true` = brouillon ; `draft:false + autoPublish:true` = publication auto ; `draft:false + autoPublish:false` = notification mobile le jour J. **Signature d'une validation du gérant dans l'UI Metricool** : passage en draft:false (souvent autoPublish:true), parfois RECRÉATION sous un nouvel id avec creationDate = heure de validation et texte-note vidé (les stories n'ont pas de légende). Ne JAMAIS « corriger »/supprimer ces contenus validés — c'est le travail du client (il valide au fil de l'eau depuis le 28/07/2026).
