from flask import Blueprint

heatmap_bp = Blueprint("heatmap", __name__)

from app.heatmap import heatmap
