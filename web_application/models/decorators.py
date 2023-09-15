from flask import current_app, redirect, url_for
from flask_login import current_user
from functools import wraps
from web_application import login_manager


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
