"""Collection of necessary functions for various parts of the application."""

# pylint: disable=W0613

import datetime

from functools import wraps

from flask import current_app, redirect, url_for
from flask_login import current_user
from wtforms import ValidationError


from web_application import db, login_manager
from web_application.models.model import Datatype, Device, Ip, Network

DATETIME_FORMAT = "%H:%M:%S %d/%m/%Y"


# Used when an unauthorized user attempts to access restricted pages
@login_manager.unauthorized_handler
def unauthorized_callback():
    """Overrides flask-login's automatic redirect with the path for the homepage."""
    return redirect(url_for("index"))


def auth_required():
    """Decorator to check the role of a user and ensure they are logged in."""

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            user_role = current_user.is_admin
            if user_role is not True:
                return current_app.login_manager.unauthorized()
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


def format_last_run(field_last_run):
    """Handles None values for the last_run field."""
    if field_last_run is not None:
        last_run = datetime.datetime.strftime(field_last_run, DATETIME_FORMAT)
    else:
        last_run = None
    return last_run


def generate_device_dict(database_list):
    """Generates a device dictionary that can be displayed."""
    device_list = []
    for device in database_list:
        ip_name = Ip.query.filter_by(id=device.ip_id).first()

        last_run = format_last_run(device.last_run)
        dictionary = {
            "id": device.id,
            "name": device.name,
            "device_type": device.device_type,
            "os": device.os,
            "ip": ip_name.name,
            "date_added": datetime.datetime.strftime(
                device.date_added, DATETIME_FORMAT
            ),
            "last_run": last_run,
        }
        device_list.append(dictionary)
    return device_list


def generate_network_dict(database_list):
    """Generates a network dictionary that can be displayed."""
    network_list = []
    for network in database_list:
        datatype_name = Datatype.query.filter_by(id=network.datatype_id).first()

        last_run = format_last_run(network.last_run)
        dictionary = {
            "id": network.id,
            "name": network.name,
            "datatype": datatype_name.name,
            "provenance": network.provenance,
            "network_format": network.network_format,
            "date_added": datetime.datetime.strftime(
                network.date_added, DATETIME_FORMAT
            ),
            "last_run": last_run,
        }
        network_list.append(dictionary)
    return network_list


def set_device_choices():
    """Sets the dropdown choices for deleting devices by pulling from the db."""
    return [
        (
            device.id,
            (
                f"{device.name}, {device.device_type}, {device.os}, "
                f"{(Ip.query.get(device.ip_id)).name}, {device.date_added}"
            ),
        )
        for device in Device.query.all()
    ]


def set_network_choices():
    """Sets the dropdown choices for deleting networks by pulling from the db."""
    return [
        (
            network.id,
            (
                f"{network.name}, {(Datatype.query.get(network.datatype_id)).name}, "
                f"{network.provenance}, {network.network_format}, {network.date_added}",
            ),
        )
        for network in Network.query.all()
    ]


def clear_selected_table(model):
    """Deletes all records in a given table."""
    model.query.delete()
    db.session.commit()


def check_contents_of_table(table):
    """Checks the given table is not populated.
    This is to prevent the application attempting to
    add duplicate data if the url is manually accessed.
    """
    records = table.query.all()
    return len(records)


def populate_tables(tables: list):
    """Adds example entries to the database."""
    # match-case statement to call the correct function
    for table in tables:
        match table:
            case "1":
                populate_datatypes()
            case "2":
                populate_ips()


def populate_datatypes():
    """Adds example datatypes to the table."""
    current_records = check_contents_of_table(Datatype)
    if current_records == 0:
        f16 = Datatype("f16")
        f32 = Datatype("f32")
        int8 = Datatype("int8")
        uint8 = Datatype("uint8")
        db.session.add_all([f16, f32, int8, uint8])
        db.session.commit()


def populate_ips():
    """Adds example ips to the table."""
    current_records = check_contents_of_table(Ip)
    if current_records == 0:
        a55 = Ip("A55")
        a76 = Ip("A76")
        g57 = Ip("G57")
        g77 = Ip("G77")
        x1 = Ip("X1")
        x2 = Ip("X2")
        db.session.add_all([a55, a76, g57, g77, x1, x2])
        db.session.commit()


def disallow_characters(form, field):
    """Custom validator to help protect against injection attacks"""
    invalid_chars = ["'", '"', "--"]
    for char in invalid_chars:
        if char in field.data:
            raise ValidationError("Invalid character used")


def disallow_characters_auth(form, field):
    """Custom validator to help protect against injection attacks"""
    invalid_chars = [" ", "'", '"', "--"]
    for char in invalid_chars:
        if char in field.data:
            raise ValidationError("Invalid character used")
