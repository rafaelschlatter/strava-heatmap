from flask import Blueprint

upload_bp = Blueprint("upload", __name__)

from app.upload import upload
