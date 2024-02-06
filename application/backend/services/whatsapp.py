import os

from flask import request
from application.backend.config import settings
from application.backend.services.bot import Bot


class Whatsapp:

    @staticmethod
    def replace_start(s):
        prefix_mapping = {"521": "52", "549": "54"}
        for prefix, replacement in prefix_mapping.items():
            if s.startswith(prefix):
                return replacement + s[len(prefix):]
        return s

    @staticmethod
    def get_message(message):
        type_message = message.get('type', 'unknown')
        if type_message == 'text':
            return message['text']['body']
        elif type_message == 'button':
            return message['button']['text']
        elif type_message == 'interactive' and message['interactive']['type'] == 'list_reply':
            return message['interactive']['list_reply']['title']
        elif type_message == 'interactive' and message['interactive']['type'] == 'button_reply':
            return message['interactive']['button_reply']['title']
        else:
            return 'mensaje no procesado'

    @staticmethod
    def verify_token():
        try:
            token = request.args.get('hub.verify_token')
            challenge = request.args.get('hub.challenge')

            if token == os.getenv('TOKEN') and challenge is not None:
                return challenge
            else:
                return 'token incorrecto', 403
        except Exception as e:
            return e, 403

    @classmethod
    def get_messages(cls):
        try:
            body = request.get_json()
            entry = body.get('entry', [])[0]
            changes = entry.get('changes', [])[0]
            value = changes.get('value', {})
            message = value.get('messages', [])[0]
            number = cls.replace_start(message.get('from', ''))
            message_id = message.get('id', '')
            contacts = value.get('contacts', [])[0]
            name = contacts.get('profile', {}).get('name', '')
            text = cls.get_message(message)

            Bot(text, number, message_id, name).manage()
            return 'enviado'
        except Exception as e:
            return 'no enviado ' + str(e)
