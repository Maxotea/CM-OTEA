# Modèle : mail du lundi avec le tableau de validation

Le mail hebdomadaire de review, préparé chaque **vendredi** en brouillon par la routine
« Review, préparation du vendredi » et envoyé le **lundi matin** (automatiquement si
`envoi_review_auto` + `email_confirme` dans `clients-config.json`, seule exception à la
règle « ne jamais envoyer automatiquement », sinon par Maxime). Adapter le
tutoiement/vouvoiement au `ton` du client sans toucher à la structure. Pas de pièce
jointe : le client télécharge depuis le tableau s'il veut Excel. {LIEN_SHEET} = le
`drive_fichier` de la semaine (reviews/config.json) ; le dossier parent
(`drive_dossier`) est le lien permanent du client : le rappeler en une ligne.

**Objet** : 📅 Vos publications de la semaine du {LUNDI} au {DIMANCHE} : validation en 3 minutes

---

Bonjour {PRÉNOM},

Voici vos {N} publications prévues cette semaine sur vos réseaux. Trois minutes suffisent
pour tout valider :

👉 **Ouvrir votre tableau de validation** : {LIEN_SHEET}

*En HTML : bouton sombre, libellé « 👉 Ouvrir votre tableau de validation ». Attention :
Gmail **supprime la propriété raccourcie `background`** d'un style en ligne mais garde
`background-color` et l'attribut `bgcolor`. Un `<a style="background:#1a1a1a;color:#fff">`
arrive donc en texte blanc sur fond blanc : bouton invisible. Toujours écrire le bouton
en cellule de tableau, ceinture et bretelles :*

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:28px 0">
  <tr><td bgcolor="#1a1a1a" style="background-color:#1a1a1a;border-radius:8px">
    <a href="{LIEN_SHEET}" style="display:inline-block;padding:14px 26px;color:#ffffff;text-decoration:none;font-weight:600">👉 Ouvrir votre tableau de validation</a>
  </td></tr>
</table>
```

*Même règle pour l'encadré gris de fin. Après création, relire le brouillon avec
`list_drafts` en vue complète : si `bgcolor` a disparu du HTML rendu, le bouton est
illisible et il faut le refaire.*

Comment ça marche :
1. Relisez chaque ligne : vous pouvez corriger la légende directement dans la case, et
   ajuster l'heure si besoin.
2. Choisissez votre décision dans le menu de chaque ligne :
   ✅ **OK pour publier** : la publication part automatiquement, plus rien à faire
   ✏️ **À corriger** (voir commentaire) : on la retravaille et on vous la représente
   ⛔ **Ne pas publier** : elle est retirée de la semaine
3. C'est tout. Vos décisions sont prises en compte automatiquement plusieurs fois par jour.

À savoir : une ligne laissée sans décision reste en attente, rien ne part sans votre
accord. Les visuels marqués « à venir » seront ajoutés avant publication. Votre tableau
vit toujours au même endroit : votre dossier « Validation hebdo » ({LIEN_DOSSIER}).
Chaque lundi, la nouvelle semaine vous y attend.

Si vous préférez travailler hors ligne, ouvrez le tableau puis Fichier → Télécharger →
Microsoft Excel : remplissez-le et renvoyez-le simplement en réponse à ce mail.

Belle semaine,

Maxime
OTEA Production

---

Variante tutoiement (Le Loft, Pierre Huiban…) : « Salut {PRÉNOM} », « tes publications »,
« corrige la légende directement dans la case », « tes décisions sont prises en compte »,
signature identique. Le fond ne change pas : 3 étapes, 3 décisions, rien ne part sans accord.
