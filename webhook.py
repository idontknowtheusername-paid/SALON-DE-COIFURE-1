from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# Vérifie si les variables d'environnement sont bien définies
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
ADMIN_PHONE_NUMBER = os.getenv("ADMIN_PHONE_NUMBER")

if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, ADMIN_PHONE_NUMBER]):
    raise ValueError("Les variables d'environnement de Twilio sont manquantes !")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/webhook', methods=['POST'])
def calendly_webhook():
    try:
        # Récupère les données JSON envoyées par Calendly
        data = request.json
        print("Données reçues : ", data)  # Affiche les données pour vérifier

        # Vérifie si les clés nécessaires sont présentes dans les données
        if 'payload' not in data:
            raise ValueError("Données de payload manquantes")
        if 'invitee' not in data['payload']:
            raise ValueError("Données de l'invité manquantes")
        if 'name' not in data['payload']['invitee']:
            raise ValueError("Nom de l'invité manquant")
        if 'sms' not in data['payload']['invitee']:
            raise ValueError("Numéro de téléphone de l'invité manquant")
        if 'event' not in data['payload']:
            raise ValueError("Données de l'événement manquantes")
        if 'start_time' not in data['payload']['event']:
            raise ValueError("Heure de début de l'événement manquante")

        # Extraire les informations nécessaires
        invitee_name = data['payload']['invitee']['name']
        invitee_phone = data['payload']['invitee']['sms']  # Utilise sms au lieu d'email
        event_time = data['payload']['event']['start_time']

        # Affiche les informations extraites pour vérifier
        print(f"Nom de l'invité : {invitee_name}")
        print(f"Téléphone de l'invité : {invitee_phone}")
        print(f"Heure de l'événement : {event_time}")

        # Envoi du SMS au client
        client.messages.create(
            body=f"Bonjour {invitee_name}, votre rendez-vous est bien confirmé pour le {event_time}. Merci !",
            from_=TWILIO_PHONE_NUMBER,
            to=invitee_phone
        )

        # Envoi du SMS à l'admin
        client.messages.create(
            body=f"Nouveau RDV pris par {invitee_name} pour le {event_time}.",
            from_=TWILIO_PHONE_NUMBER,
            to=ADMIN_PHONE_NUMBER
        )

        return jsonify({"success": True}), 200

    except ValueError as e:
        print(f"Erreur de validation des données : {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return jsonify({"error": "Une erreur interne s'est produite"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)