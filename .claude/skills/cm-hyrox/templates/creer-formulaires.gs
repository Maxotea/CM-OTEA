/**
 * Dispositif athlète OTEA — génération des formulaires.
 *
 * Crée les DEUX formulaires du dispositif et leurs feuilles de réponses :
 *   1. « Dossier Athlète »  — rempli une fois, à l'onboarding
 *   2. « Point hebdo »      — rempli chaque dimanche, 30 secondes
 *
 * MODE D'EMPLOI
 *   1. script.google.com → Nouveau projet → coller ce fichier
 *   2. Exécuter `creerFormulaires` → autoriser l'accès à Drive
 *   3. Les URLs s'affichent dans le journal d'exécution (Ctrl+Entrée)
 *
 * POURQUOI UN SCRIPT ET PAS UN FORMULAIRE FAIT À LA MAIN
 *   Le formulaire se construit à partir du schéma, jamais l'inverse. Les libellés de questions
 *   deviennent les en-têtes de colonnes de la feuille de réponses : s'ils dérivent, l'import vers
 *   `profil.json` casse. Ici les deux sortent du même tableau `SCHEMA`, donc ils ne peuvent pas
 *   diverger. Et un athlète de plus = une exécution de plus, pas une recopie.
 *
 * CE QUI N'EST VOLONTAIREMENT PAS DANS LE FORMULAIRE
 *   La voix et le persona. Ils passent par un FACECAM de 3 minutes que l'athlète tourne seul :
 *   cinq questions, une seule prise, jamais publié. Un athlète qui écrit se corrige et lisse ses
 *   tournures ; une prise unique l'en empêche. Le formulaire porte la consigne et enregistre le
 *   mode d'envoi — il ne collecte pas les réponses. Voir references/persona-et-voix.md, §2.
 */

// ---------------------------------------------------------------------------
// LE SCHÉMA — source unique du formulaire et de la correspondance des champs
// ---------------------------------------------------------------------------
// type : 'court' | 'long' | 'choix' | 'liste' | 'date' | 'titre'
// champ : le chemin dans profil.json. '' pour les éléments de mise en page.

const SCHEMA_DOSSIER = [
  { type: 'titre', titre: 'Toi, en compétition',
    aide: 'Les faits. Cinq minutes, et on ne te les redemande plus.' },

  { champ: 'nom',                     titre: 'Prénom et nom',                         type: 'court', requis: true },
  { champ: 'instagram',               titre: 'Ton compte Instagram (sans le @)',      type: 'court', requis: true },
  { champ: 'reseaux_autres',          titre: 'Tes autres comptes, si tu en as',       type: 'court' },
  { champ: 'naissance',               titre: 'Ta date de naissance',                  type: 'date',  requis: true,
    aide: 'Elle détermine ton groupe d\'âge — et en doubles, c\'est la moyenne des deux qui compte.' },

  { champ: 'division',                titre: 'Ta division cette saison',              type: 'liste', requis: true,
    choix: ['Open', 'Pro', 'Doubles Open', 'Doubles Pro', 'Doubles Mixte', 'Relais', 'Je ne sais pas encore'] },
  { champ: 'partenaire.nom',          titre: 'Si tu cours en doubles : le nom de ton partenaire', type: 'court' },
  { champ: 'partenaire.naissance',    titre: 'Sa date de naissance',                  type: 'date',
    aide: 'En doubles, le groupe d\'âge est la moyenne de vos deux âges.' },
  { champ: 'partenaire.instagram',    titre: 'Son compte Instagram',                  type: 'court' },

  { champ: 'entrainement.coach',      titre: 'Ton coach',                             type: 'court' },
  { champ: 'entrainement.club',       titre: 'Ton club ou ta team',                   type: 'court' },
  { champ: 'entrainement.salles',     titre: 'La ou les salles où tu t\'entraînes',   type: 'court' },
  { champ: 'entrainement.creneaux',   titre: 'Tes jours et créneaux de séance dans une semaine normale', type: 'long',
    aide: 'Ex. : lundi 6h30, mardi 19h, jeudi 6h30, samedi matin. C\'est ce qui nous sert à caler tes plans de tournage.' },

  { champ: 'historique',              titre: 'Tes trois dernières courses',           type: 'long', requis: true,
    aide: 'Une par ligne : ville, date, temps, et en une phrase comment ça s\'est passé.' },
  { champ: 'chiffres.splits',         titre: 'Tes splits, ou séances types si tu les as gardés', type: 'long',
    aide: 'Lien, capture d\'écran, copier-coller — peu importe le format. Ce sont eux qui alimentent tes contenus chiffrés.' },
  { champ: 'chiffres.pb',             titre: 'Ton record personnel, et où il a été fait', type: 'court' },

  { champ: 'courses_inscrit',         titre: 'Les courses où tu es DÉJÀ INSCRIT',     type: 'long', requis: true,
    aide: 'Ville et dates. C\'est ce qui structure tout ton calendrier de contenu.' },
  { champ: 'courses_vises',           titre: 'Les courses que tu VISES sans être inscrit', type: 'long' },
  { champ: 'objectif_saison',         titre: 'Ton objectif de la saison, en UN chiffre', type: 'court', requis: true,
    aide: 'Un temps, une place, une qualification. Un seul.' },
  { champ: 'objectif_qualitatif',     titre: 'Qu\'est-ce qui ferait de cette saison une réussite, même sans ce chiffre ?', type: 'long' },

  { type: 'titre', titre: 'Tes limites',
    aide: 'La partie qui nous empêche de faire une bêtise en ton nom. Sois franc, rien n\'est publié sans toi.' },

  { champ: 'positions_ok',            titre: 'Deux sujets sur lesquels tu acceptes de prendre position publiquement', type: 'long', requis: true,
    aide: 'Quitte à ce que ça fasse débat. C\'est ce qui fait la portée — et c\'est toi qui décides jusqu\'où.' },
  { champ: 'interdits',               titre: 'Trois sujets sur lesquels on ne parle JAMAIS en ton nom', type: 'long', requis: true },
  { champ: 'interdits_image',         titre: 'Ce qu\'on ne montre jamais', type: 'long',
    aide: 'Personnes, lieux, aspects de ta vie privée.' },
  { champ: 'sponsors',                titre: 'Tes partenaires et sponsors actuels',   type: 'long',
    aide: 'Pour chacun : la marque, son @ exact, ce que tu leur dois (nombre de publications, échéances), et s\'ils imposent un hashtag ou une façon de les citer.' },
  { champ: 'contraintes',             titre: 'Ton cadre professionnel', type: 'long',
    aide: 'Y a-t-il des choses à éviter à cause de ton métier ou de ton employeur ?' },
  { champ: 'contraintes_reglementaires', titre: 'Es-tu soumis à des contrôles, une fédération, un ordre professionnel ?', type: 'long' },

  { type: 'titre', titre: 'Ton matériel',
    aide: 'Deux minutes. On cale le protocole de tournage sur tes réponses.' },

  { champ: 'materiel.telephone',      titre: 'Le modèle de ton téléphone',            type: 'court' },
  { champ: 'materiel.micro_cravate',  titre: 'As-tu un micro-cravate sans fil ?',     type: 'choix', requis: true,
    choix: ['Oui', 'Non'],
    aide: 'C\'est le seul achat qu\'on te demande, autour de 50 €. Le son est ce qui fait décrocher une vidéo, pas l\'image.' },
  { champ: 'materiel.mode_son',       titre: 'Tu préfères parler pendant ta séance, ou filmer muet et enregistrer ta voix au calme le soir ?', type: 'choix', requis: true,
    choix: ['Parler pendant la séance', 'Filmer muet + voix off le soir', 'Je ne sais pas, on teste les deux'],
    aide: 'Les deux marchent. La voix off donne souvent un meilleur rendu et prend moins de temps.' },
  { champ: 'materiel.lieux',          titre: 'Deux endroits fixes où tu peux te filmer', type: 'long',
    aide: 'Un pour parler face caméra, un pour l\'action. Les fixer une fois évite d\'avoir à décider à chaque séance.' },
  { champ: 'materiel.autorisation',   titre: 'As-tu le droit de filmer dans ta salle ?', type: 'choix',
    choix: ['Oui', 'Non', 'Je dois vérifier'] },

  { type: 'titre', titre: 'Dernière étape — 3 minutes de vidéo',
    aide: 'Il reste la partie la plus importante : ta voix. Elle ne se fait pas par écrit — quand '
        + 'on écrit, on se corrige, on lisse, et on perd exactement ce qu\'on cherche.\n\n'
        + 'Tu lances l\'enregistrement sur ton téléphone, tu réponds aux cinq questions à la '
        + 'suite, tu envoies. Pas de rendez-vous à caler.\n\n'
        + 'LES QUATRE RÈGLES — elles comptent plus que tes réponses :\n'
        + '1. UNE SEULE PRISE. Tu ne recommences pas. Si tu bafouilles, tu continues : c\'est '
        + 'exactement ce qu\'on veut.\n'
        + '2. Tu ne coupes pas entre les questions, tu enchaînes.\n'
        + '3. 3 minutes en tout. Ne prépare rien.\n'
        + '4. Cette vidéo ne sera JAMAIS publiée. Elle sert à nous, pour apprendre à écrire '
        + 'comme toi.\n\n'
        + 'Ce n\'est pas une présentation : on ne veut pas que tu te vendes, on veut t\'entendre '
        + 'parler normalement. Téléphone vertical, cadre poitrine, là où tu es.\n\n'
        + 'LES CINQ QUESTIONS\n'
        + '1. Au sixième kilomètre, quand ça fait vraiment mal — qu\'est-ce que tu te dis dans ta '
        + 'tête ? Les mots exacts, même s\'ils sont bêtes ou grossiers.\n'
        + '2. Qu\'est-ce qui t\'énerve dans le milieu ? Sois franc, rien ne sort d\'ici.\n'
        + '3. Sur quoi tout le monde se trompe, d\'après toi ?\n'
        + '4. Le jour où tu as failli arrêter — c\'était quand, et pourquoi tu as continué ?\n'
        + '5. Décris la dernière personne qui t\'a écrit en DM. Qui c\'est, ce qu\'elle voulait.' },

  { champ: 'facecam_envoi',           titre: 'Comment tu nous envoies ta vidéo ?', type: 'choix', requis: true,
    choix: ['Je l\'envoie par WhatsApp tout de suite', 'Je la dépose dans le dossier partagé',
            'Je la fais dans les 48 h'],
    aide: 'Le plus simple est le mieux. Une vidéo de téléphone brute, sans montage.' },
  { champ: 'facecam_note',            titre: 'Un truc à nous dire sur cet exercice ?', type: 'long',
    aide: 'Optionnel. Si tu détestes te filmer, dis-le — on adapte le dispositif.' }
];

const SCHEMA_HEBDO = [
  { champ: 'seances',  titre: '1. Mes séances de la semaine',                        type: 'long',  requis: true,
    aide: 'Combien, lesquelles. Deux lignes suffisent.' },
  { champ: 'chiffre',  titre: '2. Mon chiffre de la semaine',                        type: 'court', requis: true,
    aide: 'Un chrono, une charge, un volume. C\'est celui qui ouvrira tes contenus de la semaine.' },
  { champ: 'dur',      titre: '3. Ce qui a été dur',                                 type: 'long' },
  { champ: 'question', titre: '4. Une question qu\'on m\'a posée',                    type: 'long',
    aide: 'En DM, à la salle, n\'importe où. Ce sont elles qui font les meilleurs contenus.' },
  { champ: 'a_venir',  titre: '5. Ce qui arrive la semaine prochaine',               type: 'court' }
];

// ---------------------------------------------------------------------------
// GÉNÉRATION
// ---------------------------------------------------------------------------

function creerFormulaires() {
  const dossier = construire_(
    'Dossier Athlète — OTEA',
    'Pour que ce qu\'on publie sur ton compte sonne comme toi, et pas comme une agence.\n\n'
    + 'Tes mots, tes chiffres, tes prises de position — pas les nôtres.\n\n'
    + 'Compte 10 minutes. Une seule fois : ensuite, cinq lignes par semaine suffisent.',
    SCHEMA_DOSSIER,
    'C\'est envoyé, merci.\n\nIl reste la vidéo : 3 minutes, cinq questions, une seule prise, '
    + 'jamais publiée — les questions sont dans la dernière section de ce formulaire. Ensuite tu ne '
    + 'reçois plus qu\'un lien le dimanche, cinq lignes, trente secondes.',
    false
  );

  const hebdo = construire_(
    'Point hebdo — OTEA',
    'Cinq lignes, trente secondes. C\'est ce qui alimente tout ce qu\'on publie sur ton compte '
    + 'la semaine suivante.\n\nÀ remplir le dimanche soir.',
    SCHEMA_HEBDO,
    'Reçu. Bonne semaine.',
    true
  );

  Logger.log('\n=== DOSSIER ATHLÈTE ===');
  Logger.log('À envoyer     : ' + dossier.url);
  Logger.log('Réponses      : ' + dossier.sheet);
  Logger.log('Édition       : ' + dossier.edit);
  Logger.log('\n=== POINT HEBDO ===');
  Logger.log('À envoyer     : ' + hebdo.url);
  Logger.log('Réponses      : ' + hebdo.sheet);
  Logger.log('Édition       : ' + hebdo.edit);
  Logger.log('\nMettre le lien du point hebdo en rappel récurrent le dimanche 19h.');
}

function construire_(titre, description, schema, confirmation, reponsesMultiples) {
  const form = FormApp.create(titre);
  form.setDescription(description);
  form.setConfirmationMessage(confirmation);
  form.setProgressBar(true);
  form.setAllowResponseEdits(true);
  form.setLimitOneResponsePerUser(false);
  if (reponsesMultiples) {
    form.setShowLinkToRespondAgain(true);
  }

  schema.forEach(function (q) {
    var item;
    switch (q.type) {
      case 'titre':
        item = form.addPageBreakItem().setTitle(q.titre);
        if (q.aide) { item.setHelpText(q.aide); }
        return;
      case 'long':   item = form.addParagraphTextItem(); break;
      case 'choix':  item = form.addMultipleChoiceItem().setChoiceValues(q.choix); break;
      case 'liste':  item = form.addListItem().setChoiceValues(q.choix); break;
      case 'date':   item = form.addDateItem(); break;
      default:       item = form.addTextItem();
    }
    item.setTitle(q.titre);
    if (q.aide)   { item.setHelpText(q.aide); }
    if (q.requis) { item.setRequired(true); }
  });

  const ss = SpreadsheetApp.create(titre + ' — réponses');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  return {
    url: form.shortenFormUrl(form.getPublishedUrl()),
    edit: form.getEditUrl(),
    sheet: ss.getUrl()
  };
}

/**
 * Imprime la correspondance « libellé de colonne → champ de profil.json ».
 * À exécuter une fois et à reporter dans athletes/<slug>/ pour l'import.
 */
function afficherCorrespondance() {
  Logger.log('--- DOSSIER → profil.json ---');
  SCHEMA_DOSSIER.forEach(function (q) {
    if (q.champ) { Logger.log(q.champ + '  ←  ' + q.titre); }
  });
  Logger.log('\n--- HEBDO → semaines/<ISO>.json ---');
  SCHEMA_HEBDO.forEach(function (q) {
    Logger.log(q.champ + '  ←  ' + q.titre);
  });
}

/**
 * Relit les formulaires VIVANTS et recrache leur état réel.
 *
 * À exécuter après toute retouche manuelle dans l'interface Google Forms. Un libellé modifié à la
 * main devient un en-tête de colonne modifié dans la feuille de réponses : si le SCHEMA ci-dessus
 * n'est pas recalé dessus, l'import vers profil.json cherche une colonne qui n'existe plus.
 *
 * Sortie : les deux liens publics, et la liste numérotée des questions telles qu'elles sont.
 */
function exporterFormulaires() {
  [['DOSSIER', '1mH9WpKs82c-hSgKV3kT72KCP36vOZhj_PZ7bW8f0tj4'],
   ['HEBDO',   '1eNeUNxUzUz-ggGbi8o-0b4MZ1D9dmrXhElb2Aex6kvA']].forEach(function (f) {
    var form = FormApp.openById(f[1]);
    Logger.log('=== ' + f[0] + ' === ' + form.shortenFormUrl(form.getPublishedUrl()));
    form.getItems().forEach(function (it, i) {
      Logger.log((i + 1) + ' | ' + it.getType() + ' | ' + it.getTitle());
    });
  });
}

// ---------------------------------------------------------------------------
// IMPORT — de la feuille de réponses vers le dépôt
// ---------------------------------------------------------------------------

const SHEET_DOSSIER = '1J25NjJPJpF01qEiMIcNjDa5Ht3547HUgU_M8cavu57o';
const SHEET_HEBDO   = '1FreB-RK645deVVshBfj3-M7WL20NHkVIFF_J0T15zWY';

/**
 * Lit la DERNIÈRE réponse au Dossier Athlète et imprime le profil.json correspondant.
 * À copier dans athletes/<slug>/profil.json du dépôt CM-BTOC.
 *
 * Les champs que le formulaire ne collecte pas — mantra, tics, DA, blog_id — ne sont pas
 * inventés : ils sortent à null et se remplissent à la main après l'entretien oral.
 */
function genererProfil() {
  const profil = lireDerniereReponse_(SHEET_DOSSIER, SCHEMA_DOSSIER);
  if (!profil) { Logger.log('Aucune réponse pour le moment.'); return; }

  profil.slug = slugifier_(profil.nom || 'athlete');
  profil.blog_id = null;
  profil.mantra = null;
  profil.tics = [];
  profil.da = null;
  profil.palier = null;
  profil._source = 'Dossier Athlète — réponse du ' + profil._horodatage;
  profil._a_completer = ['blog_id', 'mantra', 'tics', 'da',
                         'persona (entretien oral)', 'questions_recurrentes (entretien oral)'];

  Logger.log(JSON.stringify(profil, null, 2));
}

/**
 * Lit la dernière réponse au Point hebdo et imprime le semaines/<ISO>.json correspondant.
 */
function genererSemaine() {
  const semaine = lireDerniereReponse_(SHEET_HEBDO, SCHEMA_HEBDO);
  if (!semaine) { Logger.log('Aucune réponse pour le moment.'); return; }

  const d = new Date(semaine._horodatage);
  semaine.semaine = d.getUTCFullYear() + '-W' + numeroSemaine_(d);
  Logger.log(JSON.stringify(semaine, null, 2));
}

function lireDerniereReponse_(sheetId, schema) {
  const sheet = SpreadsheetApp.openById(sheetId).getSheets()[0];
  const lignes = sheet.getDataRange().getValues();
  if (lignes.length < 2) { return null; }

  const entetes = lignes[0];
  const derniere = lignes[lignes.length - 1];

  // index par libellé, puisque c'est le libellé qui fait le lien entre le formulaire et le schéma
  const parLibelle = {};
  entetes.forEach(function (t, i) { parLibelle[String(t).trim()] = i; });

  const out = { _horodatage: formater_(derniere[0]) };
  const manquants = [];

  schema.forEach(function (q) {
    if (!q.champ) { return; }
    const i = parLibelle[q.titre.trim()];
    if (i === undefined) { manquants.push(q.titre); return; }
    poser_(out, q.champ, formater_(derniere[i]));
  });

  if (manquants.length) {
    Logger.log('/* ATTENTION — libellés du schéma absents de la feuille, donc non importés :');
    manquants.forEach(function (m) { Logger.log(' - ' + m); });
    Logger.log('   Le formulaire a été modifié sans recaler le SCHEMA. */');
  }
  return out;
}

function poser_(obj, chemin, valeur) {
  const parts = chemin.split('.');
  var cur = obj;
  for (var i = 0; i < parts.length - 1; i++) {
    if (!cur[parts[i]]) { cur[parts[i]] = {}; }
    cur = cur[parts[i]];
  }
  cur[parts[parts.length - 1]] = valeur;
}

function formater_(v) {
  if (v === '' || v === null || v === undefined) { return null; }
  if (Object.prototype.toString.call(v) === '[object Date]') {
    return Utilities.formatDate(v, 'Europe/Paris', 'yyyy-MM-dd');
  }
  return String(v).trim();
}

function slugifier_(s) {
  return String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function numeroSemaine_(d) {
  const t = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()));
  t.setUTCDate(t.getUTCDate() + 4 - (t.getUTCDay() || 7));
  const debut = new Date(Date.UTC(t.getUTCFullYear(), 0, 1));
  const n = Math.ceil((((t - debut) / 86400000) + 1) / 7);
  return (n < 10 ? '0' : '') + n;
}

