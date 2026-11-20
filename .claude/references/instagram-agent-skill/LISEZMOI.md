# Instagram Agent Skill (13 skills `ig-*`)

Source : https://github.com/Jakeschincariol/instagram-agent-skill (licence MIT,
copie du commit d03c56b, 13 septembre 2026). Trouvé via le guide de Damien
(@damien.mapt). Code relu le 13 octobre 2026 : les scripts Python ne font que
du traitement de texte local, sans accès réseau ni identifiants, et aucun skill
ne publie, ne commente ni n'envoie de message à la place de l'utilisateur.

Les skills sont dans `.claude/skills/ig-*`. Par où commencer : `/ig-profile`,
puis `/ig-viral`, `/ig-reel`, `/ig-plan`.

## Ce qui prime sur ces skills chez OTEA

- Tout contenu créé dans Metricool reste en brouillon : Maxime valide.
- Les stories partent des vraies photos du client (règles dans `.claude/memories/`).
- Le tutoiement ou le vouvoiement suit le champ « Ton utilisé » de chaque contact.
- Aucun tiret cadratin ni demi-cadratin. `/ig-human` les remplace aussi.
- Sur un compte client, les quotas de piliers de `cm-metricool` font foi.
- `/ig-reel` recoupe `reel-script` et `reel-lint` : on peut comparer les deux.

## Option : la voix de Maxime

`/ig-reel` et `/ig-plan` lisent `~/.claude/instagram/voice.md` s'il existe. Le
modèle vierge est `voice.md` dans ce dossier : le remplir puis le copier à cet
endroit sur le Mac.
