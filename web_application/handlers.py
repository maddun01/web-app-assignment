from flask import Blueprint, render_template

error_blueprint = Blueprint("error", __name__, template_folder="templates/errors")


@error_blueprint.app_errorhandler(Exception)
def error(error):
    """Custom error page for catching exceptions"""
    return render_template("error.html", error=error)
