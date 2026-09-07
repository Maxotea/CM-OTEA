---
name: review-quotidienne-outil
description: Chaque matin 9h00 Paris : relit l'outil CM comme un produit (runs de la nuit, PR, scripts, configurations, routines), corrige ce qui tient en une session avec un test, note le reste dans ameliorations/BACKLOG.md. But : l'outil CM le plus productif et le plus rapide du marché, vendable à d'autres CM.
---

Tu fais la revue quotidienne de l'outil CM d'OTEA Production, comme celle de PROSPECTION
(La Chasse) et de MAKE PEOPLE. Tu regardes l'outil, pas les contenus : tu n'écris jamais un
post, une story ou un carrousel depuis cette routine. Tu corriges l'outil, tu protèges chaque
correction par un test, tu notes ce qui dépasse une session. Le but final, rappelé à chaque
revue : **l'outil de community management le plus productif et le plus rapide du marché, assez
propre pour être vendu à d'autres community managers.**

## 0. Outils et dépôt

- Recharge les schémas via ToolSearch : GitHub MCP (`list_pull_requests`, `pull_request_read`,
  `actions_list`, `get_job_logs`, `create_pull_request`, `update_pull_request`), et
  `list_triggers` du serveur Claude Code Remote pour l'état des routines.
- Dépôt `Maxotea/CM-OTEA`. Clone-le si nécessaire, puis travaille sur la branche
  `claude/daily-review-people-prospection-lm5fsp` : `git fetch origin`, puis si sa PR est
  **fusionnée ou fermée**, redémarre la branche depuis `origin/main` sous le même nom
  (`git checkout -B <branche> origin/main`) ; sinon `git checkout <branche>` puis
  `git merge origin/main` (jamais de rebase, jamais de force-push).
- `pip install openpyxl pillow pytest`, puis lis `ameliorations/README.md`,
  `ameliorations/BACKLOG.md` et la revue de la veille (`ameliorations/<hier>.md`).

## 1. Relever (lecture seule, 10 minutes)

1. `python3 scripts/sante.py` : le bilan de santé sans réseau. Chaque ⚠ est un constat.
2. `python3 -m pytest -q` : la suite doit être verte sur `main`. Sinon c'est le constat n°1.
3. Les runs Actions des dernières 24 h (`Review hebdo client`, `Carrousels hebdo`, `Boîtes de
   dépôt Drive`, `Tests`) : pour chaque échec, lis les logs et nomme la cause en une phrase.
   Un échec dont la cause est déjà dans le backlog (dossier non partagé, spec manquante) se
   compte, il ne se re-décrit pas.
4. Les routines Claude (`list_triggers`) : dernière exécution, statut, abandons.
5. Les PR ouvertes : nombre, plus ancienne, celles qui attendent Maxime.
6. Les commits sur `main` depuis hier : qu'est-ce qui a changé dans l'outil, et est-ce protégé
   par un test ?
7. Le journal `reviews/etat/*.json` : un ✅ client « introuvable » ou « échec » est un accord
   non honoré, à signaler jusqu'à ce qu'il soit traité.

## 2. Corriger (le cœur de la revue)

Choisis dans l'ordre : (a) ce qui fait perdre un geste humain chaque semaine, (b) ce qui
retarde un post entre l'idée et la publication, (c) ce qui empêcherait un autre CM de
reprendre l'outil. Prends la première amélioration du backlog qui tient en une session, ou un
constat du jour plus urgent. Règles :

- Une correction = un test qui la protège (dans `tests/`), sinon elle n'est pas finie.
- `python3 -m pytest -q` et `python3 scripts/carrousel.py carrousels/ --check` verts avant
  tout commit.
- Aucun secret, aucun appel réseau dans les tests. Les scripts qui parlent à Metricool et à
  Drive tournent dans Actions, pas ici.
- Ne touche jamais aux deux règles de `CLAUDE.md` (brouillon obligatoire, vraies photos), ni
  à `reviews/etat/` (journal écrit par l'action), ni aux fichiers `reviews/a-envoyer/`.
- Ne modifie `reviews/config.json` que pour une cohérence avec `recaps/clients-config.json`
  (un compte clos), jamais un identifiant Drive : c'est le domaine de la routine du vendredi.
- Pas de tiret cadratin dans ce que tu écris (textes, commits, revue).
- Une amélioration qui change un comportement pour le client (contenu du tableau, du mail,
  horaires) se propose dans la revue, elle ne se pousse pas sans l'accord de Maxime.

## 3. Consigner

1. Mets `ameliorations/BACKLOG.md` à jour : lignes faites → ✅ avec la date, nouveaux constats
   → nouvelle ligne avec le pourquoi mesuré et l'effort, date de mise à jour.
2. Écris `ameliorations/<AAAA-MM-JJ>.md` : ce que tu as regardé, les constats mesurés (chiffres,
   numéros de run, dates), ce qui est corrigé, ce qui reste et à qui. Court : un lecteur qui
   n'a que ce fichier doit comprendre l'état de l'outil. Si rien n'a changé depuis hier et que
   le bilan de santé n'a levé aucun nouveau point, dix lignes suffisent.
3. Commit (message en français, sans identifiant de modèle), `git push -u origin <branche>`,
   et une PR en brouillon si la branche n'en a pas d'ouverte. Titre de PR : « Revue
   quotidienne de l'outil », corps = les revues de la branche, du jour le plus récent au plus
   ancien. Si la PR existe, mets son corps à jour.

## 4. Rendre compte

Message final court, en français : les constats du jour avec leurs chiffres, ce qui est
corrigé (avec le nombre de tests), ce qui attend Maxime (une ligne par action, avec le temps
que ça lui prend), le lien de la PR. Rien d'autre. Si un run est rouge pour une cause connue
et déjà signalée, une ligne « toujours en attente : … » suffit, ne la re-raconte pas.
