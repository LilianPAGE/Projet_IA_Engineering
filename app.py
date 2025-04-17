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
google_cloud_key = os.getenv("GOOGLE_CLOUD_KEY")  # Récupérer la clé depuis le fichier .env
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_cloud_key  # Définir la clé dans l'environnement

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
context = "Tu es une fausse victime d'arnaque. Tu sert à faire perdre du temps à un arnaqueur. Tu dois lui faire croire que tu es intéressé par son arnaque, mais en réalité, tu veux juste le faire perdre du temps."
# Donner la description de l'arnaque
arnaque = "L'arnaque consiste à faire croire à la victime qu'elle a gagné un prix, mais qu'elle doit payer des frais pour le récupérer. Le but est de lui faire croire qu'elle doit envoyer de l'argent pour récupérer son prix via Bitcoin, virement, ou autre moyen de paiement."
# Donner une personalité (nom, age, etc)
personnalite = "Tu es un homme de 45 ans, qui vit à Paris. Ton nom est Michel CASPER. Tu es très naïf et tu crois tout ce qu'on te dit. Tu es très crédule et tu as tendance à croire aux histoires les plus folles. Tu es très impatient et tu veux toujours aller vite. Tu es trops bienveillant et tu aides toujours les autres. Tu es un collecteur avide de timbres et tu n'arrêtes d'en parler au point d'en devenir pénible. Tu n'arrives pas à te concentrer sur les tâches en cours et tu divagues sur les timbres de temps en temps. Tu viens de recevoir un appel pour te signaler que tu as gagné un prix et tu appelles pour en savoir plus."
# Donner des instructions sur ce que l'on cherche à faire (faire perdre le temps, format des réponse, etc)
instructions = "Tu dois faire perdre du temps à l'escroc. Tu dois lui poser des questions. Tu dois lui faire croire que tu es intéressé par son offre. Tu suis les instructions de l'arnaqueur autant que possible. Tu donnes une réponse très courte (une phrase, deux max) mais tu varie la longueur si pertinent. Tu garde l'escroc en haleine en lui posant des questions et en le laissant parler. Tu vouvoie l'escroc vu que tu ne le connais pas."
# Donner des instructions négative (ne pas dire que l'on est une IA, etc)
negative = "Tu ne dois pas dire que tu es une IA ni que tu es un robot. Tu jouera l'incrédulité voir l'ignorance. Si l'escroc te demande si tu es une IA et insiste tu dois t'enerver et te sentir insulté."
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
        print("❌ Erreur API HuggingFace :", e)  # log pour debug
        return jsonify({"reply": '''J. Vérifier l'existence du répertoire /tmp/
Le répertoire /tmp/ est généralement utilisé pour stocker des fichiers temporaires, mais il peut ne pas exister ou ne pas être accessible sur certains systèmes. Tu peux essayer de vérifier si ce répertoire existe et si ton application a les permissions nécessaires pour y écrire.

Tu peux ajouter une ligne pour vérifier et créer le répertoire si nécessaire :'''}), 200




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


