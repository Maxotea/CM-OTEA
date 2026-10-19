---
name: recap-lundi
description: Agent Cowork du lundi matin : récap des publications Metricool de la semaine pour les comptes actifs, brouillons Gmail de compte rendu client, liens WhatsApp pré-remplis. Lecture seule sur Metricool. Utilise-le le lundi vers 9h ou quand Maxime dit « le récap de la semaine ».
---

# Récap du lundi

Le récap n'a plus de routine depuis le 24/08/2026. Il revient ici, ordinateur allumé.

## Avant

`cd ../CM-OTEA && git pull`. Lis `recaps/clients-config.json` : tout compte dont `actif` vaut false
est sauté. Suis `.claude/taches-planifiees/recap-hebdo-publications/SKILL.md`, étapes 1, 2, 3, 5
et 6. **Saute l'étape 4** (branchement des nouveaux médias) : elle écrit dans Metricool et reste
dans la routine POST CM-OTEA.

## Règles

- Lecture seule sur Metricool : demander le JSON brut, analyser en Python, ne jamais faire compter
  le résolveur.
- Statuts : brouillon à valider, programmé en notification, validé. Ne jamais corriger un contenu
  validé.
- Côté client : jamais les statuts internes, jamais le mot IA, jamais les autres clients.
- Brouillons Gmail seulement, destinataire rempli si `email_confirme`, sinon
  contact@oteaproduction.com avec le bandeau de remplacement. Idempotence par objet.
- Pas de tiret cadratin.

## Sorties

`recaps/recap-semaine-<lundi>.md`, `recaps/whatsapp-semaine-<lundi>.md`, commit et push, puis le
récap complet dans la réponse avec la ligne « N brouillons restent à valider dans Metricool ».
