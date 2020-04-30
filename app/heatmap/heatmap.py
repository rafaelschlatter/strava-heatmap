from flask import render_template
from app.heatmap import heatmap_bp


@heatmap_bp.route("/heatmap")
def heatmap():
    return render_template("heatmap.html")
