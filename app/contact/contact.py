from flask import render_template
from app.contact import contact_bp


@contact_bp.route("/contact")
def contact():
    return render_template("contact.html")
