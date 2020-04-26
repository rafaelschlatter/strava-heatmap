from flask import Flask
from app.config import Config
from app.index import index_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(index_bp)

    return app
