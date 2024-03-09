"""Error handler for the application."""

from flask import Blueprint, render_template

error_blueprint = Blueprint("error", __name__, template_folder="templates/errors")


# Handles http and internal errors
@error_blueprint.app_errorhandler(Exception)
def error(received_error):
    """Custom error page for catching exceptions."""
    return render_template("error.html", error=received_error)
