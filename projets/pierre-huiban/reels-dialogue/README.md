# Pierre Huiban : reels « dialogue » (père et fils)

Décision de Maxime du 07/10/2026. Modèle : le reel de @rundadlift
(instagram.com/p/DeH2T6FOUuJ), « Dad & Daughter Dialogues ». Dans ce modèle,
l'image est en noir et blanc et au ralenti. Une voix d'enfant pose une
question, et la réponse du père s'affiche en sous-titres jaunes à empattements.

## Le principe

- **La voix de l'enfant :**
  - voix de synthèse Artlist, en anglais ;
  - elle doit sonner comme un enfant de **3-4 ans** ;
  - ce n'est jamais un clone de la voix de son fils, ni de celle de Pierre.
- **Pierre ne parle pas.** Sa réponse est écrite : sous-titres jaunes en
  Fraunces, dans le tiers bas de l'image. Si Pierre veut s'enregistrer
  lui-même, sa voix remplace les sous-titres. On ne synthétise jamais sa voix.
- **Les images dépendent de la question :**
  - « why do you train so much? », « why do you get up so early? » : images
    d'**ENTRAÎNEMENT** ;
  - « how do you win? », « are you going to make it? » : images de
    **COMPÉTITION** (Rome).
- **Ralenti réel.** Les rushes FX3 sont en 100p : le ralenti ×4 ne fabrique
  aucune image. Pour un rush d'entraînement en 50p, mettre `"ralenti": 2` sur
  le plan ; en 25p, `"ralenti": 1`.
- **Son :** seule la voix de l'enfant est présente, aucune musique. Maxime
  ajoute le son tendance dans Instagram.
- **Textes :**
  - aucun chiffre ni fait qui ne soit déjà dans le dépôt (Rome 53:34, 1ers des
    35-39, Hong Kong juin 2027, doubles avec Antoine, job et famille) ;
  - aucun tiret cadratin ;
  - l'employeur n'est jamais cité.
- **Validation :** tout passe par la feuille de validation de Pierre avant
  publication. Dans Metricool, tout reste en **brouillon**.
- **Qui est qui dans les rushes de Rome :** Pierre porte le **débardeur noir**,
  Antoine le débardeur vert avec la chaîne. C'est déduit des photos de la banque
  et **reste à confirmer par Maxime**.

## Sur le MacBook Pro (là où sont les rushes)

```bash
brew install ffmpeg              # ffmpeg de Homebrew, avec rubberband
pip3 install pillow
cd CM-OTEA && git fetch && git checkout claude/cm-otea-migration-audit-jfipoe && git pull
mkdir -p fonts   # y déposer Fraunces-Regular.ttf (Google Fonts, famille Fraunces)

python3 scripts/pierre-reel-ralenti.py \
    projets/pierre-huiban/reels-dialogue/r01-how-do-you-win.json \
    --rushes "/chemin/vers/PIERRE" --polices fonts
```

`--rushes` est le dossier des rushes. Il est fouillé en entier : `"clip":
"7374"` trouve `FX3POST20260926_7374.MP4`. La sortie est un mp4 1080×1920 en
25 i/s, avec la voix seule. À vérifier à l'œil avant de l'attacher au
brouillon Metricool :
- les points d'entrée (`debut`) ;
- le cadrage (`x`, de 0 à 1) : Pierre doit rester dans le cadre 9:16.

Pour reprendre avec Claude Code sur le Mac : « continue les reels dialogue de
Pierre, lis projets/pierre-huiban/reels-dialogue/README.md ».

## Les voix

**Générées le 07/10**, voix « Curiosity » (la seule voix enfant d'Artlist), puis
rajeunies : +5 demi-tons et tempo ×0,92 par rubberband, blancs coupés, -16 LUFS.

| Réplique | Fichier (déjà rajeuni) |
|---|---|
| Daddy, how do you win? | https://d2ol7oe51mr4n9.cloudfront.net/user_2zae6klRfE97hlBWhyQP6j7d9cR/f2e88dc5-98c8-450b-908e-91bf447a53f8.mp3 |
| Are you going to win in Hong Kong? | https://d2ol7oe51mr4n9.cloudfront.net/user_2zae6klRfE97hlBWhyQP6j7d9cR/6186dba0-1e31-4540-aafe-f6822ad5487e.mp3 |

**Pour une nouvelle réplique :**
1. Générer avec `generate_voiceover`, voix « Curiosity ».
2. Ne mettre **que le texte**. Le champ `prompt` de réglage est lu à voix
   haute par le modèle : 66 crédits perdus le 07/10.
3. Rajeunir ensuite :
   ```bash
   ffmpeg -i brut.mp3 -af "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,rubberband=pitch=1.335:tempo=0.92,highpass=f=180,loudnorm=I=-16:TP=-1.5" -ar 48000 voix.mp3
   ```
   On peut aussi mettre `"hauteur": 1.335` sur la voix dans la spec.

## Les dialogues

Les textes de Pierre sont des propositions, à faire valider par lui.

| # | Type | L'enfant | Pierre (sous-titres) | Images |
|---|---|---|---|---|
| r01 | compétition | Daddy, how do you win? / Are you going to win in Hong Kong? | You don't win on race day. You win on the mornings nobody sees. On tired legs. With Antoine next to me. I don't know, buddy. But I'll give everything. Like in Rome. 53:34. First in our age group. | Rome, spec prête |
| r02 | entraînement | Daddy, why do you get up so early? | Because the rest of the day belongs to you. And to work. So I train before everyone wakes up. | séances du matin (rushes du Mac) |
| r03 | entraînement | Why do you train so much? | Because I want to show you that you can do hard things. Even with a job. Even with a family. | entraînement |
| r04 | entraînement | Are you tired, Daddy? | Yes. But tired is part of it. | fin de séance |
| r05 | compétition | Daddy, did you win? | 53:34. First in our age group. With Antoine. | arrivée de Rome (7376 à 7378) |
| r06 | compétition | Is Hong Kong far? | Very far. June 2027. Every session counts until then. | Rome, puis l'entraînement en plan final |

## Fichiers

- `scripts/pierre-reel-ralenti.py` : le moteur. Gabarit `reel` (noir et blanc
  plus sous-titres) ou `story` (couleur plus calque de la DA, voir
  `scripts/pierre-story-photo-v2.py - SPEC CLE calque.png`).
- `r01-how-do-you-win.json` : premier reel, rushes de Rome, voix prêtes. La
  légende proposée est dans la spec.
