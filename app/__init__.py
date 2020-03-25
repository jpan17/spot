from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Is testing mode activated? (Use test routes.py if yes)
spot_test = os.environ.get('SPOT_TEST') == 'true'
template_folder = '../templates/'
if spot_test:
    template_folder = '../test/templates/'

app = Flask(__name__, template_folder=template_folder)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models

# Import routes from test if testing, otherwise from app
if spot_test:
    from test import routes
else:
    from app import routes