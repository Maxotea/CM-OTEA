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
| Livrable | `o/nina-ramen-reel-v1.mp4` + `.montage.json` (EDL rééditable) + `.rapport.md` (prises, choix, diagnostics son) |

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

   Le rendu repart sans refaire l'analyse.
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
