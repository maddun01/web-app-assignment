"""Error handler for the application."""

import logging

from flask import Blueprint, render_template
from werkzeug import exceptions

from web_application.models.exceptions import AppError

error_blueprint = Blueprint("error", __name__, template_folder="templates/errors")

logger = logging.getLogger(__name__)


# Handles http and internal errors
@error_blueprint.app_errorhandler(Exception)
def error(received_error):
    """Custom error handler for catching exceptions."""
    logger.exception(received_error)
    return received_error
    # return render_template("error.html", error="An Error Has Occurred")


@error_blueprint.app_errorhandler(exceptions.NotFound)
def error(received_error):
    """Custom error handler for catching Page Not Found Errors."""
    logger.error(received_error)
    return render_template("error.html", error="Page not Found")


@error_blueprint.app_errorhandler(AppError)
def error(received_error):
    """Custom error handler for catching custom App Errors."""
    return render_template("error.html", error=received_error)
