---
name: motion-canvas
description: "Motion Canvas : animations vectorielles écrites en TypeScript, construites pas à pas avec des générateurs et calées sur une voix off. Utilise ce skill dès que Maxime parle de Motion Canvas, d'un schéma animé, d'une explication qui se dessine étape par étape, d'une animation à synchroniser sur une voix, ou d'un projet contenant `@motion-canvas/core`. Pour un habillage de reel ou des sous-titres, préférer Remotion (voir `video-en-code`)."
---

# Motion Canvas

Skill écrit pour OTEA le 26/11/2026 (il n'existe pas de skill officiel).
Il résume l'usage courant : en cas de doute sur une fonction, lire la
documentation (motioncanvas.io/docs) plutôt que deviner. Licence MIT.

## Ce que c'est

Une scène est une fonction génératrice. Chaque `yield*` joue une animation et
attend sa fin. On écrit donc l'animation dans l'ordre où elle se déroule, ce
qui en fait l'outil le plus lisible pour une explication pas à pas.

L'éditeur tourne dans le navigateur : on y voit la ligne de temps, on y cale
les événements sur la piste audio, on y lance le rendu.

## Démarrer un projet

Toujours dans un dossier à part (jamais dans le `package.json` du dépôt) :

    mkdir -p video-code/<client> && cd video-code/<client>
    npm init @motion-canvas@latest      # répondre : TypeScript, exporteur ffmpeg
    cd <projet> && npm install
    npm start                           # ouvre l'éditeur sur http://localhost:9000

## Régler le format (vertical OTEA)

Dans l'éditeur, onglet Video Settings : résolution 1080 × 1920, 30 images par
seconde, espace colorimétrique sRGB. Ces réglages sont enregistrés dans
`src/project.meta`.

## Une scène type

```tsx
// src/scenes/titre.tsx
import {makeScene2D, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, easeOutCubic, waitFor, waitUntil} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  const carte = createRef<Rect>();
  const titre = createRef<Txt>();

  view.fill('#0b0f1a');
  view.add(
    <Rect ref={carte} width={0} height={260} radius={32} fill={'#ffffff'}>
      <Txt ref={titre} text={'3 erreurs en HYROX'} fontSize={72} fontWeight={700} opacity={0} />
    </Rect>,
  );

  yield* carte().width(860, 0.6, easeOutCubic);
  yield* titre().opacity(1, 0.3);
  yield* waitUntil('chute');            // événement calé à la souris sur l'audio
  yield* all(carte().scale(1.08, 0.2), titre().fill('#e11d48', 0.2));
  yield* waitFor(1);
});
```

Puis déclarer la scène dans `src/project.ts` :

```ts
import {makeProject} from '@motion-canvas/core';
import titre from './scenes/titre?scene';
import voix from '../audio/voix.mp3';

export default makeProject({scenes: [titre], audio: voix});
```

## Les briques à connaître

| Brique | Rôle |
|---|---|
| `createRef<T>()` | garder la main sur un élément pour l'animer |
| `noeud().propriete(valeur, duree, courbe)` | animer une propriété |
| `all(...)`, `sequence(delai, ...)`, `chain(...)` | en même temps, en décalé, à la suite |
| `waitFor(secondes)`, `waitUntil('nom')` | attendre une durée ou un repère de la ligne de temps |
| `createSignal(valeur)` | une valeur dont dépendent d'autres propriétés (compteur, jauge) |
| `Rect`, `Circle`, `Line`, `Txt`, `Img`, `Layout`, `Code`, `Latex` | les éléments |
| `Layout` avec `layout`, `direction`, `gap` | mise en page automatique (flexbox) |

## Rendre la vidéo

Le rendu se lance depuis l'éditeur, bouton RENDER, exporteur « Video (FFmpeg) »
(paquet `@motion-canvas/ffmpeg`, proposé à la création du projet). Le fichier
sort dans `output/`. Il n'y a pas de commande de rendu sans éditeur : si Claude
travaille seul sur une machine sans écran, il prépare la scène et Maxime clique
sur RENDER, ou bien on passe par Remotion qui se rend en ligne de commande.

## Pièges

- Oublier le `*` de `yield*` : l'animation ne joue pas, sans message d'erreur.
- Importer une scène sans le suffixe `?scene` : la scène n'apparaît pas.
- Le son du projet sert à caler l'animation. Pour un reel OTEA, exporter sans
  audio : la musique se pose dans Instagram.
- Aucun tiret cadratin dans un texte affiché.
