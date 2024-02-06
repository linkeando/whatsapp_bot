from flask import Blueprint

from application.backend.services.whatsapp import Whatsapp

home_bp = Blueprint('home', __name__)


@home_bp.route('/webhook', methods=['GET'])
def verify_token():
    Whatsapp().verify_token()


@home_bp.route('/webhook', methods=['POST'])
def get_message():
    Whatsapp().get_messages()


def init_app(app):
    app.register_blueprint(home_bp)
