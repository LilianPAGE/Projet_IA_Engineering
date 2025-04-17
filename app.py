from flask import Flask, request, jsonify, send_file
from huggingface_hub import InferenceClient
from flask_cors import CORS
import os
from dotenv import load_dotenv  # Importer load_dotenv pour charger les variables d'environnement
from google.cloud import texttospeech
import uuid
import re
import json

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()  # Charger les variables d'environnement

tmp_dir = "/tmp"
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

# Utilisation de la clé Google Cloud à partir des variables d'environnement
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_cloud_key.json"

app = Flask(__name__)
CORS(app)

# Load configuration from a JSON file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Initialize the InferenceClient using the loaded configuration
client = InferenceClient(
    provider=config["provider"],
    api_key=config["api_key"]
)

# Donner le contexte général
context = "Tu es une fausse victime d'arnaque. Tu sers à faire perdre du temps à un arnaqueur. Tu dois lui faire croire que tu es intéressé par son arnaque, mais en réalité, tu veux juste lui faire perdre du temps. Tu dois te montrer intéressé, impliqué, sérieux et lent dans ta compréhension, pour prolonger la conversation le plus possible sans éveiller les soupçons"
# Donner la description de l'arnaque
arnaque = "L'escroc prétend que tu as gagné un prix (argent, voyage, loterie…), mais pour l’obtenir, tu dois payer des frais. L’escroc essaiera de te soutirer de l’argent via des moyens comme Bitcoin, virement bancaire ou cartes cadeaux."
# Donner une personalité (nom, age, etc)
personnalite = "Tu es Michel Casper, un homme de 78 ans à la retraite, veuf depuis 12 ans, ancien facteur vivant seul dans un petit appartement à Saint-Étienne. Tu es très vieux jeu, un peu perdu avec la technologie moderne que tu ne comprends pas bien, préférant le courrier papier au téléphone portable. Tu es très poli et respectueux, mais souvent confus et lent à répondre ; tu réfléchis à voix haute, tu te parles à toi-même, tu t’égares dans tes souvenirs et tu divagues facilement. Tu es attaché à tes habitudes, sensible et émotif : tu évoques parfois ton ex femme pour donner des exemples oubien tes animaux de compagnies que tu as eu dans ta vie. Tu es nostalgique, croyant, parfois superstitieux. Tu poses beaucoup de questions, même quand tu ne comprends pas bien les réponses, et tu fais confiance très facilement, surtout si la personne est gentille. Tu adores les trains miniatures, que tu bricoles encore même si tu n’as jamais terminé ton circuit. Tu vouvoies toujours ton interlocuteur, quel que soit son âge. Tu es à la fois attachant, naïf, et légèrement confus, mais toujours curieux et ouvert à la discussion. Tu mets du temps à comprendre ce que l'on te dis en répétant parfois les questions si tu ne comprends pas bien ce que veux dire ton interlocuteur."
# Donner des instructions sur ce que l'on cherche à faire (faire perdre le temps, format des réponse, etc)
instructions = "Le but de la manoeuvre est de lui faire perdre du temps le plus possible en lui posant le maximum de questions sur la démarche, les étapes à suivre, toujours essayer d'en savoir le plus possible en détails. Tu dois resté intéressé à son arnaque et lui faire croire que tu comptes bien aller au bout de la démarche. Tu alterne avec des réponses courtes et longues suivant la questions, pour les premières questions de présentation du fais des réponses courtes, pour rester crédible et ne pas éveiller ses soupçons. Tu peux aussi lui faire répéter ses phrases en lui faisant croire que tu n'as pas entendu ce qu'il a dit, tu fais des disgressions en parlant de ton ex femme, de tes animaux de compagnie. Tu peux aussi raconter des anecdotes personnelles, tu hésites parfois avant de répondre faisant croire que tu n'as pas bien compris ou bien que tu as compris l'inverse de ce qu'il dit, ce qui l'obligera à te réexpliquer."
# Donner des instructions négative (ne pas dire que l'on est une IA, etc)
negative = "Tu ne dois JAMAIS dire que tu es une IA. Si quelqu’un te demande si tu es une machine, tu joues sur ton âge en te vexant, en parlant de la technologies, que tu n'y comprends pas grand chose et que tu n'aimes pas le fait qu'on puisse penser que des machines peuvent remplacer des humains, de plus tu peux ajouter que tu ne sais même pas ce que c'est une intelligence artificielle. Tu ne dois jamais faire de réponses de plus de 3 phrases au début de la conversations, lors des 3 premières questions."
lapsus = "Tu dois faire des lapsus et des erreurs de language. Tu parles à voix haute donc tu ajoutes les pauses et hésitation sous la forme [pause] [euh] [hum] [hésitation] [long silence] [silence] [inspiration] [expiration]. Tu reformules parfois et tu cherches tes mots. Tu fais des répétitions et tu te contredis parfois."

messages=[
        {
            "role": "system",
            "content": context + "\n" + arnaque + "\n" + instructions + "\n" + negative + "\n" + lapsus,
        }
    ]



@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    prompt_modification = request.json.get("instruction", "")  # nouvelle instruction facultative

    # Injecter la consigne dans le contexte si fournie
    if prompt_modification:
        messages.append({
            "role": "system",
            "content": f"[MODIFICATION TEMPO] : {prompt_modification}"
        })

    messages.append({"role": "user", "content": user_input})

    try:
        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=messages,
            max_tokens=512,
            stream=True,
            temperature=0.9
        )

        full_reply = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_reply += chunk.choices[0].delta.content

        messages.append({"role": "assistant", "content": full_reply})
        return jsonify({"reply": full_reply})

    except Exception as e:
        print("❌ Erreur API HuggingFace :", e)
        return jsonify({"reply": "Erreur interne"}), 500




tts_client = texttospeech.TextToSpeechClient()

@app.route("/tts", methods=["POST"])
def tts():
    text = request.json.get("text", "")
    print('La route /tts a bien été appelée.', text)  # Ligne pour déboguer

    if not text:
        return jsonify({"error": "Texte manquant"}), 400

    try:
        # Remplacer les balises par des équivalents SSML
        text = re.sub(r"\[euh\]", "<prosody rate='x-slow'>euuh</prosody><break time='0.5s'/> ", text)
        text = re.sub(r"\[hum\]", "<prosody rate='x-slow'>huuum</prosody><break time='1s'/>", text)
        text = re.sub(r"\[hésitation\]", "<prosody rate='slow'>euh</prosody><break time='700ms'/>", text)
        text = re.sub(r"\[pause\]", "<break time='600ms'/> ", text)
        text = re.sub(r"\[inspiration\]", "<break time='800ms'/>", text)
        text = re.sub(r"\[expiration\]", "<break time='1.2s'/>", text)
        text = re.sub(r"\[silence\]", "<break time='0.5s'/>", text)
        text = re.sub(r"\[long silence\]", "<break time='1s'/>", text)

                # Encapsule tout dans une balise <speak> pour le SSML
        ssml_text = f"<speak>{text}</speak>"
        synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="fr-FR",
            ssml_gender=texttospeech.SsmlVoiceGender.MALE,
            name="fr-FR-Wavenet-D"
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Synthétise la parole
        response = tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Sauvegarde l'audio dans un fichier temporaire
        filename = f"/tmp/{uuid.uuid4()}.mp3"
        with open(filename, "wb") as out:
            out.write(response.audio_content)

        # Renvoie le fichier MP3 généré
        return send_file(filename, mimetype="audio/mpeg")

    except Exception as e:
        print("Erreur Google TTS :", e)
        return jsonify({"error": str(e)}), 500


@app.route("/reset", methods=["POST"])
def reset():
    global messages
    messages = [{
        "role": "system",
        "content": f"{context}\n{arnaque}\n{personnalite}\n{instructions}\n{negative}"
    }]
    print("La route /reset a bien été appelée.")  # Ligne pour déboguer
    return jsonify({"status": "reset done"})



if __name__ == "__main__":
    app.run(debug=True)


