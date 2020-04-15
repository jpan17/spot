import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):

    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # This disables signals from Flask whenever database is about to be modified