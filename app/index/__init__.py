from flask import Blueprint

index_bp = Blueprint("index", __name__)

from app.index import index
