from flask import render_template
from app.errors import errors_bp


@errors_bp.app_errorhandler(500)
def internal_server_error(error):
    return render_template("500.html")
