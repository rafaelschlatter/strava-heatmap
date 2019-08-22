from flask import Flask
from flask_uploads import configure_uploads
from flask_bootstrap import Bootstrap
from app.config import Config
from app.errors import errors_bp
from app.index import index_bp
from app.upload import upload_bp
from app.process import process_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    configure_uploads(app, app.config["PHOTOS"])
    bootstrap = Bootstrap(app)
    app.register_blueprint(errors_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(process_bp)

    return app
