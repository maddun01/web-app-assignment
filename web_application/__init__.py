"""Initialises the web app and the database."""

# pylint: disable=C0413

import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Create a login manager
login_manager = LoginManager()

# Set up flask application
app = Flask(__name__)

# Secret key for forms
app.config["SECRET_KEY"] = "mysecretkey"

# Database setup and config
basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
app.config["SQL_ALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)

# Initialise login manager using the app and set the login page
login_manager.init_app(app)
login_manager.login_view = "login"


# Imports for flask blueprints
from web_application.handlers import error_blueprint
from web_application.views.authentication_view import authentication_blueprint
from web_application.views.device_view import device_blueprint
from web_application.views.kickoff_run_view import kickoff_blueprint
from web_application.views.network_view import network_blueprint

# Blueprints
app.register_blueprint(authentication_blueprint, url_prefix="/auth")
app.register_blueprint(device_blueprint, url_prefix="/device")
app.register_blueprint(error_blueprint, url_prefix="/error")
app.register_blueprint(kickoff_blueprint, url_prefix="/kickoff")
app.register_blueprint(network_blueprint, url_prefix="/network")
