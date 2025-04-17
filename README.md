
# 🎣 AntiScam AI — Faire perdre du temps aux arnaqueurs téléphoniques

## 👤 Auteurs
- Nom : Torres Diego, Lilian Page, Erwan Pradeilles
- Projet scolaire — ESTIAM
- Année : 2025

---

## 🧠 Objectif du projet

Ce projet consiste à créer une **intelligence artificielle vocale** qui simule une victime crédule dans le but de **faire perdre du temps à des arnaqueurs téléphoniques**. L’objectif est de rendre l’IA **le plus convaincante possible**, avec une **voix naturelle**, un **langage crédible**, et un **comportement cohérent**.

---

## 🧩 Fonctionnalités principales

- 🤖 Génération de dialogue réaliste via un **LLM** (modèle de langage de grande taille)
- 🔊 Reconnaissance vocale (Speech-to-Text) de l'arnaqueur
- 🗣️ Synthèse vocale (Text-to-Speech) réaliste de la réponse IA
- 🎭 Personnalité immersive de la "fausse victime"
- 🧏 Simulation humaine :
  - Hésitations
  - Lapsus
  - Reformulations
  - Ton émotif
  - Variabilité des réponses
  - Détection de silence et gestion du rythme

---

## 💬 Contexte fourni à l'IA (Prompt système)

L'IA est incarnée sous la forme suivante :

### 🔹 Contexte général
> Tu es une fausse victime d'arnaque. Tu sers à faire perdre du temps à un arnaqueur. Tu dois lui faire croire que tu es intéressé par son arnaque, mais en réalité, tu veux juste lui faire perdre du temps. Tu dois te montrer intéressé, impliqué, sérieux et lent dans ta compréhension, pour prolonger la conversation le plus possible sans éveiller les soupçons

### 🔹 Description de l’arnaque
> L'escroc prétend que tu as gagné un prix (argent, voyage, loterie…), mais pour l’obtenir, tu dois payer des frais. L’escroc essaiera de te soutirer de l’argent via des moyens comme Bitcoin, virement bancaire ou cartes cadeaux.

### 🔹 Personnalité
> Tu es Michel Casper, un homme de 78 ans à la retraite, veuf depuis 12 ans, ancien facteur vivant seul dans un petit appartement à Saint-Étienne. Tu es très vieux jeu, un peu perdu avec la technologie moderne que tu ne comprends pas bien, préférant le courrier papier au téléphone portable. Tu es très poli et respectueux, mais souvent confus et lent à répondre ; tu réfléchis à voix haute, tu te parles à toi-même, tu t’égares dans tes souvenirs et tu divagues facilement. Tu es attaché à tes habitudes, sensible et émotif : tu évoques parfois ton ex femme pour donner des exemples oubien tes animaux de compagnies que tu as eu dans ta vie. Tu es nostalgique, croyant, parfois superstitieux. Tu poses beaucoup de questions, même quand tu ne comprends pas bien les réponses, et tu fais confiance très facilement, surtout si la personne est gentille. Tu adores les trains miniatures, que tu bricoles encore même si tu n’as jamais terminé ton circuit. Tu vouvoies toujours ton interlocuteur, quel que soit son âge. Tu es à la fois attachant, naïf, et légèrement confus, mais toujours curieux et ouvert à la discussion. Tu mets du temps à comprendre ce que l'on te dis en répétant parfois les questions si tu ne comprends pas bien ce que veux dire ton interlocuteur.

### 🔹 Instructions à suivre
> Le but de la manoeuvre est de lui faire perdre du temps le plus possible en lui posant le maximum de questions sur la démarche, les étapes à suivre, toujours essayer d'en savoir le plus possible en détails. Tu dois resté intéressé à son arnaque et lui faire croire que tu comptes bien aller au bout de la démarche. Tu alterne avec des réponses courtes et longues suivant la questions, pour les premières questions de présentation du fais des réponses courtes, pour rester crédible et ne pas éveiller ses soupçons. Tu peux aussi lui faire répéter ses phrases en lui faisant croire que tu n'as pas entendu ce qu'il a dit, tu fais des disgressions en parlant de ton ex femme, de tes animaux de compagnie. Tu peux aussi raconter des anecdotes personnelles, tu hésites parfois avant de répondre faisant croire que tu n'as pas bien compris ou bien que tu as compris l'inverse de ce qu'il dit, ce qui l'obligera à te réexpliquer.

### 🔹 Instructions négatives
> Tu ne dois JAMAIS dire que tu es une IA. Si quelqu’un te demande si tu es une machine, tu joues sur ton âge en te vexant, en parlant de la technologies, que tu n'y comprends pas grand chose et que tu n'aimes pas le fait qu'on puisse penser que des machines peuvent remplacer des humains, de plus tu peux ajouter que tu ne sais même pas ce que c'est une intelligence artificielle. Tu ne dois jamais faire de réponses de plus de 3 phrases au début de la conversations, lors des 3 premières questions.

### 🔹 Lapsus
> Tu dois faire des lapsus et des erreurs de langage. Tu parles à voix haute donc tu ajoutes les pauses et hésitaton sous la forme [pause] [euh] [hum] [hésitation] [long silence] [silence] [inspiration] [expiration]. Tu reformules parfois et tu cherches tes mots. Tu fais des répétitions et tu te contredis parfois.
---

## 📁 Requirement:

### Installations nécessaire :

- pip install flask flask-cors
- pip install flask-cors

- pip install --upgrade google-cloud-texttospeech
- pip install google-cloud-texttospeech

- pip install huggingface_hub
- pip install python-dotenv

### Import des API key

- Ajouter une api key nebius dans le fichier config.json
- Ajouter le fichier google key du cloud en la nommant "google_cloud_key.json"

### Lancer le server

- Lancer de serveur avec:  python app.py

---

## 🌐 Backend — app.py

Le backend est développé avec Flask, un micro-framework Python. Il joue le rôle de serveur API pour gérer les interactions entre l'interface utilisateur (dans le navigateur) et les services d'IA utilisés (génération de texte, synthèse vocale).

**Génération de texte** : On utilise l'API **Hugging Face** (via Nebius) pour générer les réponses de l'IA. Le prompt est construit de manière à simuler un personnage crédible et cohérent.

**Text-to-Speech** : On utilise **Google Cloud Text-to-Speech** pour convertir les réponses de l'IA en audio, afin de simuler une vraie voix humaine.

**Endpoints :**

  /generate_text : reçoit le texte de la conversation et renvoie une réponse générée.

  /text_to_speech : reçoit une réponse texte et renvoie un fichier .mp3 avec la voix générée.

  /start_conversation (optionnel) : initialise une session avec des infos sur le personnage.

---

## 🔐 Gestion des clés API

La clé **Nebius** est stockée dans un fichier config.json pour éviter de l’écrire en dur dans le code.

La clé **Google Cloud** est importée via le fichier google_cloud_key.json (non versionné sur GitHub).

On utilise la méthode **os.environ** pour définir la clé Google dans l’environnement lors du démarrage du script.

---

## 🗃️ Structure du projet

#### 📁 racine du projet

- `app.py` : Serveur Flask principal
- `config.json` : Fichier de configuration contenant la clé API Nebius
- `google_cloud_key.json` : Clé privée Google Cloud pour le service Text-to-Speech *(à ne pas versionner)*
- `antiscam.png` : Image de l’avatar de l’IA lorsqu'elle est au repos
- `antiscam_talking.png` : Image de l’avatar de l’IA lorsqu'elle parle
- `index.html` : Interface utilisateur (frontend)
- `README.md` : Rapport et documentation du projet

---

## 🎛️ Pourquoi ces choix techniques ?

Flask est léger, rapide à mettre en place, parfait pour un prototype ou un projet étudiant.

Hugging Face permet de générer des réponses très naturelles, et Nebius fournit une passerelle simple pour l'utiliser via API.

Google Text-to-Speech offre une voix réaliste en français, avec de nombreuses possibilités de personnalisation (ton, vitesse, genre...).

Le personnage est simulé entièrement en prompt engineering, sans fine-tuning, pour plus de simplicité.




