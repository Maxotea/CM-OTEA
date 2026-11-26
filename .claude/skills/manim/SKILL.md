---
name: manim
description: "Manim (édition Community) : animations mathématiques et de données écrites en Python, rendues en ligne de commande. Utilise ce skill dès que Maxime parle de Manim, d'un chiffre ou d'un graphique animé, d'une courbe qui se trace, d'une formule, d'une démonstration, d'une comparaison de temps ou de pourcentages, d'un style « tableau noir », ou d'un fichier contenant `from manim import`. Pour un habillage de reel ou des sous-titres, préférer Remotion (voir `video-en-code`)."
---

# Manim (Community)

Skill écrit pour OTEA le 26/11/2026 (il n'existe pas de skill officiel).
Il résume l'usage courant : en cas de doute, lire docs.manim.community plutôt
que deviner. Licence MIT. Attention à ne pas confondre avec `manimgl`, la
version personnelle de 3Blue1Brown : les deux ne sont pas compatibles.

## Installer

Dans un environnement à part, jamais dans les dépendances du dépôt :

    python3 -m venv .venv-manim && . .venv-manim/bin/activate
    pip install manim
    manim checkhealth                 # dit ce qui manque

Si `pip install` échoue sur `manimpango`, il manque les bibliothèques Pango et
Cairo : sur Mac, `brew install pango cairo pkg-config`, puis relancer. C'est
ce qui est arrivé le 26/11/2026 dans la session cloud de Claude (Python 3.13,
pas de droit d'installer ces bibliothèques) : **l'exemple ci-dessous n'a donc
pas été rendu**, à vérifier au premier usage sur le Mac.

LaTeX n'est nécessaire que pour `MathTex` et `Tex` (formules). Pour du texte
simple, `Text` suffit et n'en a pas besoin : commencer sans.

## Une scène type (verticale)

```python
# chiffre.py
from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30
config.frame_height = 16.0            # unités de la scène, en hauteur
config.frame_width = 9.0
config.background_color = "#0b0f1a"


class TempsHyrox(Scene):
    def construct(self):
        titre = Text("Temps moyen HYROX", font_size=40, weight=BOLD).to_edge(UP, buff=2)
        barres = BarChart(values=[92, 84, 71], bar_names=["2024", "2025", "2026"],
                          y_range=[0, 100, 20], x_length=7, y_length=6)
        compteur = Integer(92, font_size=96).next_to(barres, DOWN, buff=1)

        self.play(Write(titre))
        self.play(Create(barres), run_time=1.5)
        self.play(FadeIn(compteur))
        self.play(ChangeDecimalToValue(compteur, 71), run_time=1.2)
        self.play(Indicate(barres.bars[2], color=RED))
        self.wait(1)
```

## Rendre

    manim -ql chiffre.py TempsHyrox      # brouillon rapide, pour vérifier
    manim -qh chiffre.py TempsHyrox      # rendu final (la taille vient de config)
    manim -qh -t chiffre.py TempsHyrox   # fond transparent, à poser sur une vidéo
    manim -s chiffre.py TempsHyrox       # la dernière image seulement

Le fichier sort dans `media/videos/<fichier>/<qualité>/`. Ajouter `media/` au
`.gitignore`.

## Les briques à connaître

| Brique | Rôle |
|---|---|
| `Text`, `MarkupText`, `Paragraph` | texte sans LaTeX |
| `MathTex`, `Tex` | formules (LaTeX requis) |
| `Integer`, `DecimalNumber`, `ValueTracker` | chiffres qui défilent |
| `Axes`, `NumberPlane`, `BarChart`, `axes.plot(...)` | graphiques |
| `Create`, `Write`, `FadeIn`, `FadeOut`, `Transform`, `ReplacementTransform` | animations |
| `objet.animate.shift(...).scale(...)` | animer n'importe quelle méthode |
| `VGroup(...).arrange(DOWN, buff=0.5)` | grouper et aligner |
| `self.play(a, b, run_time=1)`, `self.wait(1)` | jouer en même temps, attendre |
| `always_redraw(lambda: ...)` | élément recalculé à chaque image |

## Pièges

- Vérifier la sortie image par image avant de livrer : `manim -s` sort la
  dernière image, rapide à contrôler à l'œil.
- En vertical, tout ce qui dépasse 9 unités de large sort du cadre : utiliser
  `scale_to_fit_width(8)`.
- Les accents passent avec `Text`. Avec `Tex`, il faut un modèle LaTeX adapté.
- Aucun son dans le fichier d'un reel OTEA, aucun tiret cadratin à l'écran.
