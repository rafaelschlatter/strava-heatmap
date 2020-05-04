from flask import Blueprint
from flask_mail import Mail

contact_bp = Blueprint("contact", __name__)
mail = Mail()

from app.contact import contact
