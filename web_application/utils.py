from flask import current_app, redirect, url_for
from flask_login import current_user
from functools import wraps

from web_application import login_manager
from web_application.models.model import Datatype, Ip


@login_manager.unauthorized_handler
def unauthorized_callback():
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


def generate_network_dict(database_list):
    network_list = []
    for network in database_list:
        datatype_name = Datatype.query.filter_by(id=network.datatype_id).first()
        print(datatype_name.name)
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
