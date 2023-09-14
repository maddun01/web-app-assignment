from flask_login import UserMixin
from web_application import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    """Create a table for users in the db"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
class Datatype(db.Model):
    """Create a table for datatypes in the db"""
    __tablename__ = "datatypes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # ONE TO MANY
    datatype = db.relationship("Network", backref="datatype", lazy="dynamic")
    # network_id = db.Column(db.Integer, db.ForeignKey("networks.id"))

    def __init__(self, name):
        self.name = name


class Device(db.Model):
    """Create a table for devices in the db"""
    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    type = db.Column(db.Text)
    os = db.Column(db.Text)
    # MANY TO ONE
    ip_id = db.Column(db.Integer, db.ForeignKey("ips.id"))
    # ip = db.relationship("Ip", backref="device", uselist=False)
    date_added = db.Column(db.DateTime)
    last_run = db.Column(db.DateTime)

    def __init__(self, name, type, os, ip_id, date_added, last_run):
        self.name = name
        self.type = type
        self.os = os
        self.ip_id = ip_id
        self.date_added = date_added
        self.last_run = last_run

    def __repr__(self):
        return f"Device details: \n{self.name}\n{self.type}\n{self.os}\n{self.ip_id}\n{self.date_added}\n{self.last_run}"


class Ip(db.Model):
    """Create a table for ips in the db"""
    __tablename__ = "ips"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # ONE TO MANY
    device = db.relationship("Device", backref="ip", lazy="dynamic")
    # device_id = db.Column(db.Integer, db.ForeignKey("devices.id"))

    def __init__(self, name):
        self.name = name


class Network(db.Model):
    """Create a table for networks in the db"""
    __tablename__ = "networks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # MANY TO ONE
    datatype_id = db.Column(db.Integer, db.ForeignKey("datatypes.id"))
    # datatype = db.relationship("Datatype", backref="network", lazy="dynamic")
    provenance = db.Column(db.Text)
    format = db.Column(db.Text)
    date_added = db.Column(db.DateTime)
    last_run = db.Column(db.DateTime)

    def __init__(self, name, datatype_id, provenance, format, date_added, last_run):
        self.name = name
        self.datatype_id = datatype_id
        self.provenance = provenance
        self.format = format
        self.date_added = date_added
        self.last_run = last_run

    def __repr__(self):
        return f"Network details: \n{self.name}\n{self.datatype_id}\n{self.provenance}\n{self.format}\n{self.date_added}\n{self.last_run}"
