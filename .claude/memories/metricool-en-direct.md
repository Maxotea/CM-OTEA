---
name: metricool-en-direct
description: "Metricool se pilote par son connecteur direct (gratuit) ; Zapier seulement pour supprimer, remplacer un visuel et contrôler"
metadata:
  node_type: memory
  type: feedback
---

Décision de Maxime du 18/11/2026, confirmée le 20/11 (« Go pour Metricool ») : on arrête de
payer Zapier à l'action. Zapier compte 2 tâches par appel, même en lecture, et un mois de
dépassement a coûté 116,14 € à l'été 2026.

**La règle** : lister les marques, lire, créer et modifier passent par le connecteur Metricool
direct (`getBrandSettings`, `getScheduledPosts`, `createScheduledPost`, `updateScheduledPost`).
Toujours `draft: true` et `autoPublish: false`, toujours une relecture après création.

**Ce qui reste sur Zapier** tant que ce n'est pas refait dans Make : supprimer un post, changer un
visuel (remplacer puis supprimer), le contrôle `audit_publication_safety`, l'envoi d'une image
sans adresse publique. Regrouper ces appels, ils sont payants.

**Ne pas débrancher Zapier** : Maxime garde Make (54 $ par an) pour y refaire ces actions, puis
Zapier repassera en gratuit. Pas avant.

Détail, gabarit et ce qui est vérifié ou non :
`.claude/skills/cm-metricool/references/metricool-en-direct.md`.
