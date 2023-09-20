from flask import current_app, redirect, url_for
from flask_login import current_user
from functools import wraps

from web_application import login_manager
from web_application.models.model import Datatype, Ip


# used when an unauthorized user attempts to access restricted pages
@login_manager.unauthorized_handler
def unauthorized_callback():
    """Overrides flask-login's automatic redirect with the path for the homepage"""
    return redirect(url_for("index"))


def auth_required():
    """Decorator to check the role of a user and ensure they are logged in"""

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            user_role = current_user.is_admin
            if user_role != True:
                return current_app.login_manager.unauthorized()
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


def generate_device_dict(database_list):
    """Generates a device dictionary that can be displayed"""
    device_list = []
    for device in database_list:
        ip_name = Ip.query.filter_by(id=device.ip_id).first()
        dictionary = {
            "id": device.id,
            "name": device.name,
            "type": device.type,
            "os": device.os,
            "ip": ip_name.name,
            "date_added": device.date_added,
            "last_run": device.last_run,
        }
        device_list.append(dictionary)
    return device_list


def generate_network_dict(database_list):
    """Generates a network dictionary that can be displayed"""
    network_list = []
    for network in database_list:
        datatype_name = Datatype.query.filter_by(id=network.datatype_id).first()
        dictionary = {
            "id": network.id,
            "name": network.name,
            "datatype": datatype_name.name,
            "provenance": network.provenance,
            "format": network.format,
            "date_added": network.date_added,
            "last_run": network.last_run,
        }
        network_list.append(dictionary)
    return network_list
