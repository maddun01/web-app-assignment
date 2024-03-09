"""Database model classes."""

# pylint: disable=R0903
# pylint: disable=R0913

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from web_application import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Loads the currently authenticated user."""
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    """Create a table for users in the db."""

    # Overrides the default table name
    __tablename__ = "users"

    # Table fields
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    # Init function for creating new objects
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks the given password matches the hashed entry in the db."""
        return check_password_hash(self.password_hash, password)


class Datatype(db.Model):
    """Create a table for datatypes in the db."""

    __tablename__ = "datatypes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)

    # One to many relationship between datatype and network
    datatype = db.relationship("Network", backref="datatype", lazy="dynamic")

    def __init__(self, name):
        self.name = name


class Device(db.Model):
    """Create a table for devices in the db."""

    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    device_type = db.Column(db.Text, nullable=False)
    os = db.Column(db.Text, nullable=False)

    # Many to one relationship between device and ip
    ip_id = db.Column(db.Integer, db.ForeignKey("ips.id"), nullable=False)
    date_added = db.Column(db.DateTime)
    last_run = db.Column(db.DateTime, nullable=True)

    def __init__(self, name, device_type, os, ip_id, date_added, last_run):
        self.name = name
        self.device_type = device_type
        self.os = os
        self.ip_id = ip_id
        self.date_added = date_added
        self.last_run = last_run


class Ip(db.Model):
    """Create a table for ips in the db."""

    __tablename__ = "ips"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    device = db.relationship("Device", backref="ip", lazy="dynamic")

    def __init__(self, name):
        self.name = name


class Network(db.Model):
    """Create a table for networks in the db."""

    __tablename__ = "networks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    datatype_id = db.Column(db.Integer, db.ForeignKey("datatypes.id"))
    provenance = db.Column(db.Text)
    network_format = db.Column(db.Text)
    date_added = db.Column(db.DateTime)
    last_run = db.Column(db.DateTime, nullable=True)

    def __init__(
        self, name, datatype_id, provenance, network_format, date_added, last_run
    ):
        self.name = name
        self.datatype_id = datatype_id
        self.provenance = provenance
        self.network_format = network_format
        self.date_added = date_added
        self.last_run = last_run
