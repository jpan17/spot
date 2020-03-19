import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'spot.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # This disables signals from Flask whenever database is about to be modified