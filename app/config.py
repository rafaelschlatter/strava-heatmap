import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    STRAVA_CLIENT_ID = os.environ.get("STRAVA_CLIENT_ID") or 29843
    STRAVA_CLIENT_SECRET = os.environ.get("STRAVA_CLIENT_SECRET") or "3b927ec04c2212f0fa5ced18b046668acbecc870"
