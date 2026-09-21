# Projet Nina Ramen : reel 1 min 30, montage V1

Même démarche que le projet Salomon (`scripts/aftermovie.py`), transposée au
format reel avec `scripts/reel-montage.py`. Les rushs sont sur le disque dur
vert, dossier `Nina Ramen`. Le disque n'est pas accessible depuis le cloud :
**le montage se lance sur le Mac, disque branché**, avec `montage.sh`.

## Cahier des charges

| Point | Valeur |
|---|---|
| Format | reel vertical 1080×1920, 30 i/s, H.264, AAC |
| Durée | 1 min 30 (90 s) |
| Prises | plusieurs prises par scène, une seule retenue (netteté, exposition, longueur, son, dernière prise) |
| Son | **stéréo garanti** : les rushs mono ou « mono sur un canal » sont recopiés sur les deux canaux, niveaux rapprochés plan par plan, mix à −14 LUFS |
| Image | étalonnage sur **tout le montage** : exposition et contraste rapprochés plan par plan, plans **surexposés** détectés (moyenne haute, 90e centile au blanc ou plus de 3 % de pixels brûlés) et ramenés par une courbe maître (hautes lumières écrasées, tons moyens redescendus, ombres préservées), puis look `ramen` (chaud, contrasté, saturé, léger vignettage) sur la timeline entière |
| Images IA | aucune : ce sont les rushs du client et rien d'autre |
| Livrable | `o/nina-ramen-reel-v1.fcpxml` (timeline pour le projet DaVinci Resolve) + `o/nina-ramen-reel-v1.mp4` (rendu ffmpeg, optionnel) + `.montage.json` (EDL rééditable) + `.rapport.md` (prises, choix, diagnostics son) |

## Lancer le montage (sur le Mac)

```bash
cd ~/CM-OTEA           # ou le chemin du clone
pip install pillow numpy
./projets/nina-ramen/montage.sh
```

`montage.sh` cherche le dossier `Nina Ramen` sur les volumes montés (le nom
exact du disque vert n'est pas connu du repo : on le passe en premier argument
si la recherche échoue) et lance :

```bash
python3 scripts/reel-montage.py "/Volumes/<DISQUE VERT>/Nina Ramen" \
    --titre "NINA RAMEN" --duree 90 --look ramen \
    --sortie o/nina-ramen-reel-v1.mp4
```

Options utiles :

- `--accroche 4` : ouvrir sur la scène 4 (le plan le plus fort en premier) ;
- `--carton-fin "Nina Ramen\nRéservations sur ninaramen.fr"` : carton final ;
- `--musique ~/Musique/track.mp3` : musique sous l'ambiance ;
- `--lut fichier.cube` : ta propre LUT à la place du look `ramen` ;
- `--look neutre` ou `--look froid` : autres looks.

## Dans le projet DaVinci Resolve (déjà créé)

Le projet Nina Ramen existe déjà dans Resolve : on n'en crée pas un autre,
on y importe la timeline. Deux commandes, disque vert branché :

```bash
./projets/nina-ramen/montage.sh --sans-rendu        # analyse les rushs, écrit la timeline, pas de mp4
python3 projets/nina-ramen/davinci-import.py o/nina-ramen-reel-v1.fcpxml
```

La seconde passe par l'API de Resolve (Resolve ouvert sur le projet,
« Scripting externe » sur Local dans Préférences > Système > Général). Sans
l'API : **Fichier > Importer > Timeline**, choisir `o/nina-ramen-reel-v1.fcpxml`,
laisser « importer les clips source » coché (les rushs déjà dans la
bibliothèque sont réutilisés quand le chemin correspond, rien n'est dupliqué).

Ce que contient la timeline `nina-ramen-reel-v1` :

- les prises retenues, dans l'ordre, avec les mêmes points d'entrée et durées
  que le rendu ffmpeg (90 s au total, fondus de 0,2 s centrés sur les coupes) ;
- le titre en V2 sur l'accroche (`o/nina-ramen-reel-v1-titre.png`, à remplacer
  par un Text+ si tu veux le retravailler) et le carton de fin s'il est demandé ;
- le gain par plan (volume du clip), calculé pour rapprocher les niveaux ;
- **un marqueur sur chaque plan à traiter** : « Son : mono … dupliquer le bon
  canal sur G et D » ou « Image : surexposé … descendre les hautes lumières ».
  Ce sont les deux choses que le rendu ffmpeg fait seul et qu'une timeline ne
  transporte pas ; dans Resolve ça se fait à la main (Fairlight : panoramique
  ou canal dupliqué ; Color : courbe sur les hautes lumières), puis le look
  global sur l'ensemble.

À vérifier après import : réglages de la timeline **1080×1920, 30 i/s**
(réglages personnalisés si le projet est en 16:9) et mise à l'échelle des
rushs horizontaux sur **« remplir le cadre »** (Réglages du projet > Image >
Mise à l'échelle, ou clip par clip dans l'inspecteur).

## V2 : les retours de la cliente

Retours reçus par message après la V1 (détail et réponse dans
`retours-v1.md`) :

1. **Couper les blancs entre les phrases.** Elle parle phrase par phrase et
   ça se voit. `--couper-blancs` détecte les silences de plus de 0,4 s dans
   chaque plan, les saute en gardant 0,12 s de respiration de chaque côté, et
   remplit le plan avec les phrases suivantes de la même prise : le reel garde
   ses 90 s mais dit plus de choses, et le rythme monte. Dans la timeline
   DaVinci chaque bout de phrase devient un clip (`(1/3)`, `(2/3)`…), coupe
   franche entre eux. Le rapport donne le nombre de coupes et les secondes
   de blanc retirées, plan par plan.
2. **Sous-titres : dans Submagic**, pas dans l'outil (consigne Maxime). Le
   circuit : rendre la V2 en mp4 → nouveau projet Submagic, langue français,
   import du mp4 → choisir un modèle de sous-titres proche de la charte
   (police et couleur de l'encre) → relire les mots (noms propres, plats) →
   exporter en 1080×1920 → `o/nina-ramen-reel-v2-sous-titres.mp4`. Garder
   les sous-titres dans le tiers central de l'image, loin des zones
   d'interface Instagram (bas et droite).
3. **Appel à l'action** : carton de fin aux couleurs de la charte, avec le
   logo. Le dossier graphisme envoyé par la cliente (brand book PDF + dossier
   « Imagerie » sur son Drive) se télécharge sur le Mac dans
   `projets/nina-ramen/charte/` (dossier ignoré par git : ce sont ses
   fichiers). En sortir : le logo en PNG fond transparent, la police, les deux
   couleurs (fond, encre).

```bash
./projets/nina-ramen/montage.sh --couper-blancs \
  --carton-fin "Réservez votre table\nninaramen.fr · @ninaramen" \
  --cta-fond "#F3E9D2" --cta-texte "#1F1F1F" \
  --cta-police projets/nina-ramen/charte/Police.otf \
  --cta-logo projets/nina-ramen/charte/logo.png \
  --sortie o/nina-ramen-reel-v2.mp4
```

Les couleurs ci-dessus sont des exemples : prendre celles du brand book. Le
texte du carton est à confirmer avec elle (réservation, site, compte). Si la
V1 a été retouchée dans Resolve plutôt que rendue par l'outil, relancer avec
`--sans-rendu` et réimporter le `.fcpxml` : la nouvelle timeline contient
les coupes de blancs et le carton, il reste à exporter le mp4 depuis Resolve
pour Submagic.

Ordre des opérations pour la V2 : coupes + carton (outil ou Resolve) →
export mp4 → Submagic (sous-titres) → envoi à la cliente. Les sous-titres
se font en dernier parce que chaque coupe déplace le texte.

## Retoucher la V1

1. Lire `o/nina-ramen-reel-v1.rapport.md` : chaque scène liste ses prises,
   la retenue (✅) et la note de chacune. Le diagnostic son dit ce qui a été
   converti (mono → stéréo, canal mort recopié).
2. Pour changer une prise ou un point d'entrée : éditer
   `o/nina-ramen-reel-v1.montage.json` (champ `fichier`, `debut`, `duree`,
   `pan`, `gain_db`, `correction`) puis :

   ```bash
   python3 scripts/reel-montage.py --edl o/nina-ramen-reel-v1.montage.json
   ```

   Le rendu et la timeline `.fcpxml` repartent sans refaire l'analyse
   (réimporter le `.fcpxml` dans Resolve : il crée une nouvelle timeline,
   l'ancienne reste).
3. Si des plans restent trop clairs à l'image : le rapport les marque
   « ⚠ surexposé, ramené (YAVG …, N % brûlé) ». Pour refaire seulement
   l'étalonnage des plans retenus, sans retoucher le choix des prises :

   ```bash
   python3 scripts/reel-montage.py --edl o/nina-ramen-reel-v1.montage.json --reetalonner
   ```

   Pour forcer la main sur un plan précis : éditer son champ `correction`
   dans l'EDL (par exemple `curves=master='0/0 0.7/0.55 1/0.9'`) et relancer
   avec `--edl` seul.
4. Avant diffusion : vérifier dans le rapport la ligne « Son de sortie :
   2 canaux … stéréo OK » et regarder le reel une fois en entier sur un
   téléphone.

## Contrôle qualité fait sur cet outil

Testé sur des rushs synthétiques (4K, 1080p, vertical, 25/30/50 i/s, prises
floues, audio mono, stéréo à canal mort, sans piste, saturé) : 90,0 s,
1080×1920, deux canaux avec signal équilibré, re-rendu depuis l'EDL, LUT
`.cube`. Le résultat sur les vrais rushs Nina Ramen reste à valider par Maxime.
