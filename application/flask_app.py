import os
from flask import Flask


class FlaskApp:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FlaskApp, cls).__new__(cls)
            cls._instance._init_app()
        return cls._instance

    def _init_app(self):
        self.app = Flask(__name__)
        self._init_sessions()

    def _init_sessions(self):
        self.app.static_folder = os.path.join(os.path.dirname(__file__), 'frontend', 'static')
        self.app.template_folder = os.path.join(os.path.dirname(__file__), 'frontend', 'templates')

    def create_app(self):
        return self.app
