from flask import Flask
from flask_bootstrap import Bootstrap
from app.config import Config
from app.errors import errors_bp
from app.index import index_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    bootstrap = Bootstrap(app)
    app.register_blueprint(errors_bp)
    app.register_blueprint(index_bp)

    return app
