import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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


# imports for flask blueprints

from web_application.views.device_view import device_blueprint
from web_application.views.network_view import network_blueprint

app.register_blueprint(device_blueprint, url_prefix="/device")
app.register_blueprint(network_blueprint, url_prefix="/network")
