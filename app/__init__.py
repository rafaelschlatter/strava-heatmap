import os
from flask import Flask
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler
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

    middleware = FlaskMiddleware(
        app,
        exporter=AzureExporter(
            connection_string="InstrumentationKey={key}".format(
                key=os.environ.get("APPINSIGHTS_INSTRUMENTATIONKEY")
            )
        ),
        sampler=ProbabilitySampler(rate=1.0),
    )

    return app
