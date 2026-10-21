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
pip3 install pillow numpy
cd CM-OTEA && git fetch && git checkout claude/cm-otea-migration-audit-jfipoe && git pull
# Fraunces est versionnée dans fonts/fraunces/ : le moteur la trouve seul

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

## Gabarit monologue

Demande de Maxime du 13/10/2026 : prendre en référence le reel de @rundadlift
[instagram.com/reel/DeHgY1RxPfB](https://www.instagram.com/reel/DeHgY1RxPfB/)
(même compte que le dialogue, 31,74 s, 12 683 vues). C'est le **monologue
intérieur d'un père qui court**, en phrases très courtes, sur une valse au piano
(« Une Valse Mystique », Piano Within, la même que sur DeH2T6FOUuJ). Chez Pierre :
anglais, première personne, chaleureux, un fait du dépôt au plus par reel, et
**aucune voix** (la sortie est muette, Maxime pose la musique dans Instagram ; on
ne synthétise jamais la voix de Pierre, le gabarit refuse la clé `voix`).

### Ce que fait le moteur

| | Gabarit `monologue` |
|---|---|
| Image | noir et blanc sombre et contrasté : LUT S-Log3, courbe en S (`COURBE_NB`), grain léger sur la luminance seule, chroma nulle. Flou de bougé facultatif (`flou_bouge` : nombre d'images de rush mélangées, 2 ou 3). 1080×1920, 25 i/s, libx264 yuv420p en **plage limitée (tv)** : les rushes FX3 sont en plage pleine, chaque plan est converti, sinon les cartons noirs sortaient gris foncé (17/255) après un plan FX3. **Muet** |
| Sous-titres | **centrés** ligne par ligne, bloc centré à **0,75 H** (lignes de base 0,7588 H pour une ligne, 0,7412 et 0,7764 H pour deux), **deux lignes au plus** |
| Police | Fraunces SemiBold statique (`fonts/fraunces/`, taille optique 100), **64 px**, approche -0,045 em entre les lettres d'un mot |
| Allumage | mot à mot, cumulé, chaque mot à sa place définitive : chaque ligne est centrée sur son texte **complet**, donc une ligne en cours paraît décalée à gauche, comme sur la référence. Instant de chaque mot interpolé entre `t` et `fin` au prorata de la longueur des mots (ou `horodatages` explicites). Fondu d'entrée 0,16 s (4 images), sortie du bloc en 0,16 s (`fondu_sortie: 0` = coupe sèche) |
| Couleurs | mots en **blanc cassé** #F5F1E6, `mots_jaunes` en **jaune** #F2D124 (mesuré sur la référence). `"mots_jaunes": "*"` = tout le bloc en jaune ; `"mot_en_cours": true` = karaoké (le dernier mot allumé reste jaune jusqu'au suivant) |
| Lisibilité | contour noir doux (60 %, 3 px, flou 0,8). Le contraste est **mesuré sous le texte sur chaque image du rendu** (maximum pixel à pixel du fond pendant le bloc) : cible **4,5 au pire pixel**. Sous la cible, un voile local léger s'ajoute derrière le bloc (0,45 au plus) ; le rapport du rendu donne, bloc par bloc, le contraste et le voile |
| Refus | tiret cadratin, demi-cadratin ou double tiret (sous-titres, mots jaunes, légende), plus de deux lignes, ligne plus large que 0,9 W, blocs qui se chevauchent, mot jaune absent du bloc, clé `voix` |

Spec type (les plans s'écrivent comme pour le gabarit `reel`) :

```json
{
  "gabarit": "monologue",
  "sortie": "pierre-monologue-m2.mp4",
  "ralenti": 4,
  "plans": [{"clip": "7351", "debut": 15.4, "duree": 0.95, "x": 0.45, "exposition": 1.3},
            {"clip": "CARTON NOIR", "duree": 4.6}],
  "sous_titres": [
    {"t": 0.4, "fin": 3.8, "lignes": ["53:34 in Rome.", "Then I'm Dad again."], "mots_jaunes": ["53:34"]},
    {"t": 4.0, "fin": 8.4, "lignes": ["He's my little boy."], "mots_jaunes": ["little", "boy."]}
  ]
}
```

Clés facultatives : `exposition` (globale ou par plan : LUT réécrite à cette
exposition), `courbe`, `contraste`, `luminosite`, `gamma`, `grain`,
`flou_bouge`, `taille`, `approche`, `graisse` et `graisse_jaune` (`regular` ou
`semibold`), `tenue`, `fondu`, `fondu_sortie`, `contraste_cible`, `voile_max`.
Les specs du chantier écrites au format `textes` (`debut`, `fin`, `texte`,
`jaunes`, `mots`) passent telles quelles.

### Ce qui est mesuré, ce qui est réglé

- **Police.** Fraunces SemiBold 64 px rend « Not most nights » avec 1 720 px
  d'encre (rendu ramené à 640×1136) contre 1 735 sur la couverture, 0,342 W de
  large contre 0,336 à 0,341, encre de 0,7342 à 0,7658 H contre 0,7333 à
  0,7658. Le bloc de deux lignes « Because I know there / will come a day »
  tombe de 0,7165 à 0,7835 H, exactement la couverture de DeH2T6FOUuJ. La
  Regular à 66 px proposée en repli par la fiche ne fait que 1 421 px d'encre :
  trop maigre. La police exacte de la référence n'est pas identifiable ;
  Fraunces reste plus contrastée et a un œil plus petit.
- **Couleurs.** Sur les quatre images de la référence, **tous les mots visibles
  sont jaunes** : aucun blanc cassé observé. Le blanc cassé avec mots clés en
  jaune vient de la demande (effet karaoké des reels voisins) ; `"*"` rend la
  couverture telle quelle. À trancher par Maxime sur un premier rendu.
- **Étalonnage.** Courbe calée le 13/10 sur trois images du clip 7351 (sled
  pull) lu sur Drive : p1 2 à 4, p5 6 à 8, médiane 51 à 86, p95 183 à 184,
  chroma 0, contre les cibles de la référence (p1 5 au plus, p5 5 à 26, médiane 50 à 90, p95 160
  à 255). L'ancien réglage (`eq=contrast=1.3`) bouchait les noirs (p5 à 0) et
  laissait la médiane à 96 à 129. Plan par plan, jouer d'abord sur
  `exposition`. Contrôle : `mesure_etalonnage.py` du chantier sur une image
  extraite du rendu.
- **Proposé, à caler à l'œil :** fondu 0,16 s, cadence des mots, durée des plans
  (3 à 5 s, coupe au changement de bloc).

### Lire les rushes de Rome sur Drive, sans les télécharger

```bash
python3 scripts/pierre-reel-ralenti.py spec-monologue.json \
    --drive-index rushes-drive.json --polices fonts --lut slog3.cube
```

`--drive-index` est la liste des MP4 du dossier Drive « PIERRE »
(`1cAaXJwg9h9zdO0I8VRVNdJX_xHONtU6v`) : `{"clips": [{"clip":
"FX3POST20260926_7351.MP4", "id": "…"}]}`, une liste de ces objets, ou `{nom:
id}`. `clip` peut aussi être directement une URL. Le moteur lit
`drive.usercontent.google.com/download?id=ID&export=download&confirm=t` à travers
le proxy de l'environnement (`HTTPS_PROXY`), par **plages bornées de 4 Mo** :
Drive répond « Quota exceeded » aux plages ouvertes que demande ffmpeg (constaté
le 13/10/2026), le moteur intercale donc un relais local qui découpe. Les blocs
lus restent dans `_cache_rushes/` : un clip monté trois fois n'est lu qu'une
fois. Une seconde de rush 4K 100p coûte environ 40 à 85 Mo. `--sans-relais`
passe l'URL telle quelle à ffmpeg avec `-http_proxy`.

### Les cinq reels du 13/10/2026

Specs dans `projets/pierre-huiban/reels-monologue/` : M3-R6 (18/10), M1-R7
(20/10), D1-R8 (22/10), M2-R11 (29/10), M4-R12 (01/11). Chaque plan dit ce
qu'on voit et pourquoi (`pourquoi`), `statut` « à caler » ou « à contrôler »
quand la seconde n'a pas été vue sur le rush. Règles tirées des vérifications
du 13/10 : aucun plan d'Antoine sous un « I » ou un « my » ; aucun gros plan
flou ni visage sous la bande du texte ; une seule fenêtre du même rush par
reel (M4 n'y est pas encore : deux fenêtres de 7351, recale à faire sur 7359,
7361 et 7363) ; le « him » qui désigne le fils est posé sur un plan sans
Antoine (M2, carte 7, sur un carton noir) ; contrôle de netteté (ETAPE=voir)
avant tout rendu. Au 13/10 à 15:00 UTC, aucun n'est rendu : Drive répondait
« Quota exceeded » à toute plage depuis 08:20.

## Fichiers

- `scripts/pierre-reel-ralenti.py` : le moteur. Gabarit `reel` (noir et blanc
  plus sous-titres), `story` (couleur plus calque de la DA, voir
  `scripts/pierre-story-photo-v2.py - SPEC CLE calque.png`) ou `monologue`
  (section précédente).
- `tests/test_pierre_reel_monologue.py` : découpage et horodatage des mots,
  refus des tirets, couleurs, position, contraste, relais Drive, rendu complet
  sur un rush synthétique, carton noir après un rush en plage pleine.
- `fonts/fraunces/` : Fraunces Regular et SemiBold statiques, licence OFL.
- `r01-how-do-you-win.json` : premier reel, rushes de Rome, voix prêtes. La
  légende proposée est dans la spec.
