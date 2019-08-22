import os
from flask_uploads import UploadSet, IMAGES


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    UPLOADED_PHOTOS_DEST = "app/static/input_img"
    TEMP_DIR = "app/static/temp"
    PHOTOS = UploadSet("photos", IMAGES)
