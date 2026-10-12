# Catalogue public-apis : 1 958 API gratuites, triées pour OTEA

Source : le dépôt GitHub `public-apis/public-apis` (README lu le 30/09/2026),
la base derrière le guide « Public APIs : brancher 1900 API gratuites sur ton
Claude ». Le catalogue complet est dans `catalogue.json` (une entrée par API :
nom, url, description, authentification, https, cors, catégorie).

## Les chiffres

| Total | Sans clé | Clé API | OAuth | HTTPS | Catégories |
|---|---|---|---|---|---|
| 1 958 | 932 | 866 | 152 | 1 863 | 52 |

Une API « sans clé » s'appelle directement depuis un script. Une API « clé »
demande une inscription (souvent gratuite avec un quota). « OAuth » demande
une connexion au compte de l'utilisateur (Instagram, LinkedIn, Vimeo, Notion).

## Comment la brancher sur Claude

Trois chemins, du plus simple au plus solide :

1. **Claude Desktop sur le Mac** : le serveur MCP `public-apis-mcp` indexe le
   catalogue et donne deux outils à Claude, `search_public_apis` (chercher une
   API par besoin) et `get_public_api_details` (sa fiche). Prérequis : Python
   3.10 et `uv`. Config à coller dans `claude_desktop_config.json` :
   ```json
   {"mcpServers":{"public-apis":{"command":"uvx","args":["public-apis-mcp"]}}}
   ```
   Première fois : `uvx public-apis-mcp build-index`.
2. **Depuis les sessions cloud (ici)** : le réseau sortant est filtré, la plupart
   des API ne répondent pas directement. Passer par une code action Zapier,
   qui peut appeler n'importe quelle URL, ou par une routine.
3. **OTEA Moteur (dépôt PROSPECTION)** : pour un usage récurrent (adresse,
   SIRENE, jours fériés, météo), appeler l'API depuis le serveur Node, sans
   dépendance, et stocker le résultat en SQLite.

Règle : une API tierce ne reçoit jamais de donnée client nominative sans
l'accord de Maxime. Les listes sans clé ci-dessous sont sans risque.

## Sélection utile pour OTEA

### Vidéo et montage
- **Shotstack** (clé) : montage vidéo par API, templates, rendu cloud.
- **JSON2Video** (clé) : vidéos générées depuis un JSON (idéal stories, recap).
- **Rendobar**, **Hyperserve** : rendu vidéo et hébergement.
- **TubeToTranscript**, **VidWords** : transcription de vidéos YouTube.
- **OpenSubtitles** (clé) : sous-titres.
- **Vimeo** (OAuth), **YouTube** (OAuth) : publication et statistiques.
- **TMDb** (clé) : base films et séries (culture, références).
- **RunConvert**, **CloudConvert** (clé) : conversion audio, vidéo, image, doc.

### Photo, image, design
- **Pexels**, **Pixabay**, **Unsplash** (clé) : banques d'images libres.
  Rappel : interdites sur un compte client qui a de vraies photos.
- **Remove.bg**, **PhotoRoom**, **ObjectCut** (clé) : détourage.
- **UpRes**, **Smart Image Enhancement** (clé) : upscaling.
- **Tinify** (clé) : compression.
- **APITemplate.io**, **DynaPictures**, **Supportivekoala** (clé) : visuels
  générés depuis un template (cartes, citations, chiffres clés).
- **Screenshotlayer**, **ApiFlash**, **Framejet** (clé) : captures de sites.
- **The Color API**, **Serialif Color** (sans clé) : palettes et contrastes.
- **Google Fonts** (clé) : métadonnées des polices.
- **QuickChart**, **Image-Charts**, **ChartBytes** (sans clé) : graphiques PNG
  pour les reportings clients.
- **QR Code Crafter**, **Orca Scan**, **QR & Barcode** (sans clé) : QR codes.
- **Noun Project** (OAuth) : icônes. **Europeana** (clé) : fonds des musées.

### Réseaux sociaux
- **Ayrshare**, **PostLake**, **Publora**, **Postproxy** (clé) : publication
  multi-réseaux par API (Metricool reste l'outil de référence, en brouillon).
- **Instagram**, **LinkedIn**, **TikTok** (OAuth) : API officielles.
- **TrendsMCP**, **SocialCrawl** : tendances et veille.
- **Telegram Bot**, **Bluesky** (sans clé ou simple token).
- **Imgflip**, **justmeme.wtf**, **Memesio** : memes et templates.
- **LinkPreview**, **OpenGraphr** : aperçu d'un lien (titre, image).

### Sport et HYROX (skill `cm-hyrox`)
- **Strava** (OAuth), **Fitbit** (OAuth) : données d'entraînement des athlètes.
- **Wger** (sans clé) : base d'exercices.
- **TheSportsDB** (clé) : résultats, équipes, ligues.
- **Sport Vision** : analyse vidéo sportive.
- **Padel Snipe** (sans clé) : 4 000 clubs de padel en Europe (prospection).
- **City Bikes**, **JCDecaux** : vélos en libre-service.

### Météo et calendrier (tournages, événements)
- **Météo-France** (clé) : prévisions et vigilances officielles.
- **Open-Meteo** (sans clé) : prévisions horaires, usage non commercial.
- **wttr.in** (sans clé) : météo en une ligne.
- **Sunrise and Sunset** (sans clé) : heures dorées pour les tournages.
- **Nager.Date**, **caldays** (sans clé) : jours fériés France.
- **Calendarific** (clé) : jours fériés et fêtes.

### Entreprises, facturation, prospection
- **TrustyData** (clé) : recherche INSEE et contrôle d'adresse française.
- **GlobalEntity** (clé), **OpenRegistry** (OAuth) : registres d'entreprises
  européens (dont France).
- **Neotimo DGFiP Mirror** (sans clé) : annuaire des plateformes agréées de
  facturation électronique, recherche par SIRET. Utile pour la réforme 2026.
- **PolyDoc** (clé) : PDF et e-factures Factur-X. **Attestwire** (clé) :
  validation de factures EN 16931 (Factur-X, Peppol).
- **EuroValidate**, **VATComply** (sans clé), **TaxID**, **VerifNow** :
  validation de TVA intracom (VIES) et d'IBAN.
- **Clearbit Logo** (sans clé) : logo d'une entreprise depuis son domaine.
- **Tomba**, **Hunter** (clé) : emails professionnels par domaine.
- **Signaliz**, **Crustdata** (clé) : signaux d'achat et données entreprises.
- **Bidledger** (sans clé) : tous les appels d'offres publics de l'UE (TED).
- **gankdat** (clé) : appels d'offres UK et UE.
- **Pick an Agency** : annuaire d'agences (veille concurrentielle).
- **InvoiceIn**, **Invovate** : génération de factures (Pennylane reste maître).
- **DocStruct** (sans clé) : extraction IA de factures et reçus en JSON.
- **Sendinblue (Brevo)**, **Mailtrap**, **SMTPfast**, **PostStack** (clé) :
  envoi d'emails en masse (newsletter, relances).
- **mailboxlayer**, **Kickbox**, **Disify** : vérification d'adresses email
  avant une campagne.
- **Email Spam Tester** (sans clé) : score anti-spam d'un mail de prospection.
- **AGPC Domain Check** (sans clé) : SPF, DKIM, DMARC du domaine
  oteaproduction.com.

### Événementiel
- **Eventbrite** (OAuth), **Ticketmaster** (clé), **SeatGeek** (clé) :
  événements, billetterie.
- **Bandsintown**, **Songkick** : concerts et dates d'artistes.
- **Wander Atlas** : heures creuses des lieux touristiques.
- **Transport for Paris (RATP)**, **Velib**, **SNCF**, **Navitia** (clé),
  **Transport for Bordeaux** (clé) : logistique des déplacements.

### Musique et son
- **Freesound** (OAuth), **Jamendo** (clé) : sons et musiques libres.
- **Deezer**, **Spotify** (OAuth) : catalogues.
- **AI Mastering** (clé) : mastering automatique.
- **Audexum** (clé) : transcription 25 langues et voix de synthèse.
- **IBM Text to Speech** (clé) : voix off de test.

### Texte, IA, traduction
- **Groq**, **Google Gemini**, **Hugging Face**, **Jina AI** (clé) : modèles
  et embeddings gratuits.
- **LibreTranslate** (sans clé), **Lecto**, **Langbly** (clé) : traduction.
- **Detect Language**, **languagelayer** : détection de langue.
- **Perspective** (clé) : toxicité d'un commentaire (modération).
- **Sentiment Analysis**, **NLP Cloud** (clé) : sentiment des commentaires.
- **Hirak OCR**, **OCR.Space** (clé) : texte depuis une image.
- **ToHuman** (clé) : réécriture plus humaine d'un brouillon IA.
- **GeoScore** (clé) : lisibilité d'un contenu par les moteurs IA.
- **Blague.xyz** (clé) : la plus grande API de blagues en français.
- **Datamuse** (sans clé) : mots proches, rimes, synonymes (titres de posts).

### Documents, productivité
- **Notion** (OAuth), **Todoist** (OAuth), **Airtable**, **Monday**,
  **ClickUp**, **Asana**, **Clockify** (clé) : outils de gestion.
- **Google Docs**, **Sheets**, **Slides**, **Keep** (OAuth).
- **iLovePDF** (clé, 250 docs/mois), **PDFMint**, **Html2PDF**, **CraftMyPDF**,
  **Formfeed** : génération et manipulation de PDF (devis, dossiers).
- **PandaDoc** (clé) : signature électronique.
- **Bitly** (OAuth), **Cutt.ly**, **Lix.li**, **Rebrandly** (clé) : liens
  courts avec statistiques.
- **File.io**, **GoFile** : envoi de fichiers temporaires.
- **Dropbox**, **Google Drive**, **OneDrive**, **Box** (OAuth).

### Données publiques françaises
- **adresse.data.gouv.fr** (sans clé) : géocodage d'adresses.
- **GeoApi** api.gouv.fr (sans clé) : communes, départements, régions.
- **data.gouv.fr** (clé) : jeux de données publics.
- **Nantes Open Data** (clé), **Transport Grenoble**, **CTS Strasbourg**.
- **PVGIS** (sans clé) : ensoleillement par lieu.
- **SustainMetrics** (clé) : facteurs d'émission ADEME (bilan carbone d'un
  tournage ou d'un événement).
- **Right to Disconnect** (sans clé) : droit à la déconnexion par pays UE.
- **Tollmint** (sans clé) : règles publicitaires, abonnements, mentions IA
  (utile pour la conformité des posts sponsorisés).

### Sécurité et hygiène numérique
- **HaveIBeenPwned** (clé) : fuite d'un email.
- **VirusTotal**, **URLScan.io**, **Google Safe Browsing** (clé) : vérifier
  un lien reçu (pièce jointe suspecte, mail douteux).
- **SSL Labs** (sans clé) : santé du certificat du site OTEA.
- **Is This Site Down?** (sans clé) : disponibilité du site.
- **GitGuardian** (clé) : détection de clés qui traînent dans un dépôt.
- **Sealed Rose** (clé) : détection de contenu synthétique (deepfake).

### Utilitaires sans clé pour scripts
- **Frankfurter**, **Exchangerate.host** : taux de change.
- **REST Countries**, **Nominatim**, **Zippopotam.us** : pays, géocodage.
- **Agify**, **Genderize**, **Nationalize** : deviner âge, genre, nationalité
  depuis un prénom (à manier avec prudence).
- **ipapi.co**, **IPify** : IP et localisation.
- **Timezone WorldTime** : fuseaux horaires (tournages à l'étranger).
- **Quotable**, **Zen Quotes**, **Stoicism Quote** : citations pour posts.
- **Advice Slip**, **Bored** : contenu léger.
- **UUID Generator**, **RandomUser**, **DummyJSON** : données de test.
- **Wikipedia**, **Wikidata**, **Open Library**, **Gutendex** : savoir libre.

## Les 52 catégories du catalogue

Development 193 · Government 115 · Games & Comics 106 · Geocoding 103 ·
Transportation 88 · Cryptocurrency 86 · Finance 83 · Open Data 63 ·
Sports & Fitness 56 · Security 54 · Social 54 · Video 52 · Science & Math 47 ·
Documents & Productivity 45 · Weather 43 · Health 42 · Machine Learning 42 ·
Business 38 · Music 35 · Photography 34 · Test Data 33 · Email 32 ·
Food & Drink 31 · Jobs 29 · Art & Design 27 · Books 26 · News 26 ·
Currency Exchange 26 · Personality 26 · Environment 25 · Animals 24 ·
Shopping 21 · URL Shorteners 21 · Anime 19 · Cloud Storage 19 ·
Text Analysis 19 · Anti-Malware 18 · Calendar 18 · Entertainment 18 ·
Blockchain 16 · Dictionaries 16 · Data Validation 14 · Vehicle 14 ·
Open Source Projects 11 · Tracking 11 · Authentication 7 · Phone 7 ·
APILayer 6 · Continuous Integration 6 · Programming 5 · Events 4 · Patent 4.

Les catégories sans intérêt direct pour OTEA (crypto, blockchain, jeux vidéo,
anime, santé US, astrologie) sont conservées dans `catalogue.json` pour
recherche, pas détaillées ici.

## Points de vigilance

- Le catalogue est communautaire et sponsorisé par APILayer : beaucoup
  d'entrées récentes sont des services payants avec un petit palier gratuit.
  Vérifier le quota avant d'automatiser quoi que ce soit.
- Une partie des API listées « sans clé » impose une limite de requêtes par
  jour ou un usage non commercial (Open-Meteo, Nominatim).
- Depuis les sessions Claude cloud, le proxy bloque la plupart des domaines :
  un test réel se fait depuis le Mac ou via Zapier.
