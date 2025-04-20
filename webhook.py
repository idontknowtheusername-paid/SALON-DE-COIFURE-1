from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# Récupère les infos d’environnement Twilio
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
ADMIN_PHONE_NUMBER = os.environ.get("ADMIN_PHONE_NUMBER")  # Ton numéro à toi, ex: +229XXXXXXXX

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/webhook', methods=['POST'])
def calendly_webhook():
    data = request.json

    try:
        invitee_name = data['payload']['invitee']['name']
        invitee_phone = data['payload']['invitee']['sms']  # Utilise sms au lieu d'email
        event_time = data['payload']['event']['start_time']

        # SMS pour le client
        client.messages.create(
            body=f"Bonjour {invitee_name}, votre rendez-vous est bien confirmé pour le {event_time}. Merci !",
            from_=TWILIO_PHONE_NUMBER,
            to=invitee_phone
        )

        # SMS pour toi (admin)
        client.messages.create(
            body=f"Nouveau RDV pris par {invitee_name} pour le {event_time}.",
            from_=TWILIO_PHONE_NUMBER,
            to=ADMIN_PHONE_NUMBER
        )

        return jsonify({"success": True}), 200

    except Exception as e:
        print("Erreur:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)