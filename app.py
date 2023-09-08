from markupsafe import escape
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
app.config["SQL_ALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)


class Device(db.Model):
    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    type = db.Column(db.Text)
    os = db.Column(db.Text)
    # ONE TO ONE
    ip = db.relationship("Ip", backref="device", uselist=False)
    date_added = db.Column(db.DateTime)
    last_run = db.Column(db.DateTime)

    def __init__(self, name, type, os, date_added, last_run):
        self.name = name
        self.type = type
        self.os = os
        self.date_added = date_added
        self.last_run = last_run

    def __repr__(self):
        if self.ip:
            return f"Device details: \n{self.name}\n{self.type}\n{self.os}\n{self.ip.name}\n{self.date_added}\n{self.last_run}"
        else:
            return f"Device details: \n{self.name}\n{self.type}\n{self.os}\nNo IP provided\n{self.date_added}\n{self.last_run}"


class Ip(db.Model):
    __tablename__ = "ips"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"))

    def __init__(self, name, device_id):
        self.name = name
        self.device_id = device_id


class Network(db.Model):
    __tablename__ = "networks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # ONE TO MANY
    datatype = db.relationship("Datatype", backref="network", lazy="dynamic")
    provenance = db.Column(db.Text)
    format = db.Column(db.Text)
    date_added = db.Column(db.DateTime)
    last_run = db.Column(db.DateTime)

    def __init__(self, name, provenance, format, date_added, last_run):
        self.name = name
        self.provenance = provenance
        self.format = format
        self.date_added = date_added
        self.last_run = last_run

    def __repr__(self):
        return f"Network details: \n{self.name}\n{self.provenance}\n{self.format}\n{self.date_added}\n{self.last_run}"

    def display_datatypes(self):
        print("Datatypes")
        for dt in self.datatype:
            print(dt.name)


class Datatype(db.Model):
    __tablename__ = "datatypes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    network_id = db.Column(db.Integer, db.ForeignKey("networks.id"))

    def __init__(self, name, network_id):
        self.name = name
        self.network_id = network_id


# @app.route("/")
# def index():
#     return "<h1>Hello!</h1>"


# if __name__ == "__main__":
#     app.run(debug=True)
