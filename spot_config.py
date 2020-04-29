import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    
    UPLOAD_FOLDER = os.environ.get('SPOT_UPLOAD_FOLDER')

    SECRET_KEY = os.environ.get('SPOT_SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.environ.get('SPOT_SECURITY_PASSWORD_SALT')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # This disables signals from Flask whenever database is about to be modified
    
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

    # mail accounts
    MAIL_DEFAULT_SENDER = 'princeton.spot.team@gmail.com'    