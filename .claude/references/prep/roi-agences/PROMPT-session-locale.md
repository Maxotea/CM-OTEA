Tu es mon bras droit (Maxime Dietrich, OTEA Production). On finit le teaser vidéo de Run on Investment (R.O.I.) et l'envoi aux agences événementielles sport. Tout en français, tutoiement, aucun jargon, aucun tiret cadratin (« — ») ni demi-cadratin (« – »), nulle part.

RÈGLE ABSOLUE : R.O.I. comporte une application, c'est un secret. Les mots « application », « app », « plateforme », « toute l'année » n'apparaissent dans AUCUN livrable (vidéo, page, mails). Le teasing officiel : « Il y a un dernier élément, on vous le présente en visio. »

## Où sont les fichiers
Dépôt GitHub Maxotea/CM-OTEA, branche `claude/friendly-hamilton-9he6oa` (PR #67). Clone ou pull cette branche. Dossier : `.claude/references/prep/roi-agences/`
- `marque.md` : identité (noir #0A0A0A, rouge #DC2626, Caladea, Carlito)
- `habillages/` : titres animés à fond transparent (ProRes 4444) façon Nike/Adidas/Puma, plus `LISEZMOI.md` avec le découpage conseillé. S'il n'y est pas encore, attends-le ou dis-le-moi.
- `broll/` : 8 plans de running générés sur Higgsfield. S'ils n'y sont pas, récupère-les avec le connecteur Higgsfield (jobs 24897e52-d40c-4d33-b510-f1fcd5571f30, 96a7f575-f252-4cbb-90b0-db707581023a, 807723b9-a2ef-4887-b61c-e22340d2ccd1, 05397f1d-4912-46cc-a0f1-8b8c5c4ab7a1, 1e3485a5-b5ab-4e00-9f9d-c96069dba4d0, 1fc7d897-d3e5-4b1a-8ab1-1d4ab9a92d40, a72fb583-2ecc-496c-bbb4-4b7f8d7f956c, e6513d65-ddc5-4be1-919e-8af0f2bd11d3).
- `ROI_Run_on_Investment_Agences.pdf` et `deck-slide-*.png` : le deck agences (validé)
- `roi-agences.html` : la page en ligne https://claude.ai/artifact/JRUvaxk3EWhMp4XdJhwkA9 (vidéo + deck + contact)
- `mails-24-agences.json` : les 24 mails personnalisés, déjà écrits
- `../2026-10-12-session-agences-roi.md` : le kit de la séance (contacts, numéros, script d'appel)
- La musique : « Runaway (Cascade Remix) », que je viens de télécharger sur ce Mac (cherche-la dans Téléchargements). Je prends la responsabilité de la licence.

## Ce que je veux
1. **Le teaser, environ 40 secondes, 16:9, 1080p.** Montage très dynamique, codes Nike, Adidas, Puma : coupes sèches calées sur le rythme de la musique, speed ramps, un ou deux flashs rouges sur les temps forts. Images : les plans `broll/` (et des extraits de mon « PROJET MARATHON.mp4 » si utile, il est sur le Drive). Par-dessus : les habillages, selon le découpage du `LISEZMOI.md`. Fin sur la signature (R.O.I., « On en parle 30 minutes ? », Maxime Dietrich · 07 79 97 19 61). Commence par détecter le tempo de la musique, choisis le meilleur passage de 40 s (montée puis drop), et cale les coupes dessus.
   - Monte dans DaVinci Resolve si tu peux le piloter (API de script de Resolve ou contrôle de l'ordinateur). Sinon monte avec ffmpeg et livre en plus une timeline importable dans DaVinci (FCPXML ou EDL) pour que je puisse retoucher.
   - Exporte `ROI_Run_on_Investment_teaser.mp4` (H.264, moins de 15 Mo) dans `roi-agences/`, montre-moi 6 images clés, puis attends mon go.
2. **Après mon go :**
   - remplace la vidéo de la page en republiant `roi-agences.html` à la même adresse (lis d'abord l'artifact), et rappelle-moi de la passer en « Toute personne disposant du lien » ;
   - crée les 24 brouillons Gmail depuis `mails-24-agences.json` (objet : « Run on Investment · 10 000 entrepreneurs à La Défense en 2027 »). Ne les envoie qu'avec mon accord explicite ;
   - committe et pousse sur la branche, avec ces deux lignes à la fin de chaque message de commit :
     Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
     Claude-Session: https://claude.ai/code/session_01CszLyDrc69zqJTj51VNYC4
3. **Bonus, si Chrome est connecté :** sur LinkedIn, lis ma conversation avec Rim Abdelqader. Elle m'a demandé un devis : récupère sa liste de demandes et son budget, et prépare le devis (Pennylane) et ma réponse. N'envoie rien sans moi.
