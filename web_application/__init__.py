import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#create a login manager
login_manager = LoginManager()

# set up flask application
app = Flask(__name__)
# secret key for forms

app.config["SECRET_KEY"] = "mysecretkey"
# database setup and config
basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
app.config["SQL_ALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)

# initialise login manager using the app and set the login page
login_manager.init_app(app)
login_manager.login_view = "login"


# imports for flask blueprints

from web_application.views.authentication_view import authentication_blueprint
from web_application.views.device_view import device_blueprint
from web_application.views.network_view import network_blueprint

app.register_blueprint(authentication_blueprint, url_prefix="/auth")
app.register_blueprint(device_blueprint, url_prefix="/device")
app.register_blueprint(network_blueprint, url_prefix="/network")
