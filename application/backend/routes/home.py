from flask import Blueprint, request

from application.backend.config import settings
from application.backend.services.whatsapp import Whatsapp

home_bp = Blueprint('home', __name__)


@home_bp.route('/webhook', methods=['GET'])
def verify_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == settings.token and challenge != None:
            return challenge
        else:
            return 'token incorrecto', 403
    except Exception as e:
        return e, 403


@home_bp.route('/webhook', methods=['POST'])
def get_message():
    return Whatsapp().get_messages()


def init_app(app):
    app.register_blueprint(home_bp)
