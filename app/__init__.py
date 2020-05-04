from flask import Flask
from app.config import Config
from app.index import index_bp
from app.contact import contact_bp, mail
from app.heatmap import heatmap_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(index_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(heatmap_bp)

    mail.init_app(app)

    return app
