import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("GMAIL_ADRESS") or "heatmap.feedback@gmail.com"
    MAIL_PASSWORD = os.environ.get("GMAIL_PW")
