import os

import requests
import json
import time


class Bot:
    def __init__(self, text, number, message_id, name):
        self.text = text
        self.number = number
        self.message_id = message_id
        self.name = name

    @staticmethod
    def _create_message_data(**kwargs):
        return json.dumps(kwargs)

    def _mark_read(self):
        return self._create_message_data(
            messaging_product="whatsapp",
            status="read",
            message_id=self.message_id
        )

    def _button_reply_message(self, options, body, footer, sed):
        buttons = [
            {
                "type": "reply",
                "reply": {
                    "id": f"{sed}_btn_{i + 1}",
                    "title": option
                }
            }
            for i, option in enumerate(options)
        ]
        return self._create_message_data(
            messaging_product="whatsapp",
            recipient_type="individual",
            to=self.number,
            type="interactive",
            interactive={
                "type": "button",
                "body": {"text": body},
                "footer": {"text": footer},
                "action": {"buttons": buttons}
            }
        )

    def _reply_reaction_message(self, emoji):
        return self._create_message_data(
            messaging_product="whatsapp",
            recipient_type="individual",
            to=self.number,
            type="reaction",
            reaction={"message_id": self.message_id, "emoji": emoji}
        )

    def manage(self):
        print('entre aca a manejar')
        print(self.text.lower())
        text = self.text.lower()
        messages = [self._mark_read()]

        time.sleep(2)

        if "hola" in text:
            body = "¡Hola! 👋 Bienvenido a Bigdateros. ¿Cómo podemos ayudarte hoy?"
            footer = "Equipo Bigdateros"
            options = ["✅ servicios", "📅 agendar cita"]

            messages.append(self._reply_reaction_message("🫡"))
            messages.append(self._button_reply_message(options, body, footer, "sed1"))

        for item in messages:
            self._send_whatsapp_message(item)

    @staticmethod
    def _send_whatsapp_message(data):
        try:
            whatsapp_token = os.getenv('WHATSAPP_TOKEN')
            whatsapp_url = os.getenv('WHATSAPP_URL')
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + whatsapp_token}
            response = requests.post(whatsapp_url, headers=headers, data=data)
            if response.status_code == 200:
                return 'mensaje enviado', 200
            else:
                return 'error al enviar mensaje', response.status_code
        except Exception as e:
            return e, 403
