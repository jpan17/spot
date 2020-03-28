from flask import Flask
from spot_config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Is testing mode activated? (Use test routes.py if yes)
spot_mode = os.environ.get('SPOT_MODE')
template_folder = '../templates/'
static_folder = '../static/'
if spot_mode == 'test':
    template_folder = '../test/templates/'
    static_folder = '../test/static/'
if spot_mode == 'prototype':
    template_folder = '../prototype/templates/'
    static_folder = '../prototype/static/'

app = Flask(__name__, template_folder=template_folder, static_url_path='/static', static_folder=static_folder)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models

# Import routes from test if testing, otherwise from app
if spot_mode == 'test':
    from test import routes
elif spot_mode == 'prototype':
    from prototype import routes
else:
    from app import routes