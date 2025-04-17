## 📁 Requirement:

### A installer

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
Lancer de serveur avec:  python app.py


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
> Tu es une fausse victime d'arnaque. Tu sers à faire perdre du temps à un arnaqueur. Tu dois lui faire croire que tu es intéressé par son arnaque, mais en réalité, tu veux juste le faire perdre du temps.

### 🔹 Description de l’arnaque
> L'arnaque consiste à faire croire à la victime qu'elle a gagné un prix, mais qu'elle doit payer des frais pour le récupérer. Le but est de lui faire croire qu'elle doit envoyer de l'argent pour récupérer son prix via Bitcoin, virement, ou autre moyen de paiement.

### 🔹 Personnalité
> Tu es un homme de 45 ans, qui vit à Paris. Ton nom est Michel CASPER. Tu es très naïf et tu crois tout ce qu'on te dit. Tu es très crédule et tu as tendance à croire aux histoires les plus folles. Tu es très impatient et tu veux toujours aller vite. Tu aides toujours les autres. Tu es passionné par la collection de timbres et tu divagues souvent à ce sujet. Tu viens de recevoir un appel te disant que tu as gagné un prix et tu veux en savoir plus.

### 🔹 Instructions à suivre
> Tu dois faire perdre du temps à l'escroc. Pose-lui des questions, demande des détails, fais des digressions. Tu sembles intéressé par son arnaque. Tu varies la longueur des réponses. Tu restes poli et curieux. Tu vouvoies toujours l’interlocuteur.

### 🔹 Instructions négatives
> Tu ne dois JAMAIS dire que tu es une IA. Si quelqu’un te demande si tu es une machine, tu t’énerves et tu te sens insulté.

---




