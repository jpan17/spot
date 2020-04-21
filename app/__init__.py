from flask import Flask
from flask_mail import Mail
from spot_config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

# Is testing mode activated? (Use test routes.py if yes)
spot_mode = os.environ.get('SPOT_MODE').lower()
template_folder = '../templates/'
static_folder = '../static/'
if spot_mode == 'test':
    template_folder = '../test/templates/'
    static_folder = '../test/static/'
if spot_mode == 'prototype':
    template_folder = '../prototype/templates/'
    static_folder = '../prototype/static/'

# Start app with config
app = Flask(__name__, template_folder=template_folder, static_url_path='/static', static_folder=static_folder)
app.config.from_object(Config)

mail = Mail(app)

# Initialize SQLAlchemy and Migrate for database management
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize flask-login for user authentication/session management
if spot_mode != 'test' and spot_mode != 'prototype':
    login_manager = LoginManager()
    login_manager.init_app(app)

from app import models

# Import routes from test if testing, otherwise from app
if spot_mode == 'test':
    from test import routes
elif spot_mode == 'prototype':
    from prototype import routes
else:
    from app import routes