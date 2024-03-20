"""Error handler for the application."""

import logging

from flask import Blueprint, render_template
from sqlalchemy import exc
from werkzeug import exceptions

from web_application.models.exceptions import AppError

error_blueprint = Blueprint("error", __name__, template_folder="templates/errors")

logger = logging.getLogger(__name__)


# Handles http and internal errors
@error_blueprint.app_errorhandler(Exception)
def general_error(received_error):
    """Custom error handler for catching exceptions."""
    logger.exception(received_error)
    return received_error
    # return render_template("error.html", error="An Error Has Occurred")


@error_blueprint.app_errorhandler(exceptions.NotFound)
def page_not_found_error(received_error):
    """Custom error handler for catching Page Not Found Errors."""
    logger.error(received_error)
    return render_template("error.html", error="Page not Found")


@error_blueprint.app_errorhandler(AppError)
def app_error(received_error):
    """Custom error handler for catching custom App Errors."""
    return render_template("error.html", error=received_error)


@error_blueprint.app_errorhandler(exc.OperationalError)
def sqlalchemy_error(received_error):
    """Custom error handler for catching SQLAlchemy errors."""
    return render_template(
        "error.html",
        error="Unable to access the database. Please contact the administrator",
    )
