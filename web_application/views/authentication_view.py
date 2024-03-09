"""Views for displaying various login pages."""

from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import login_user, login_required, logout_user

from web_application import db
from web_application.forms.authentication_form import (
    LoginForm,
    RegistrationForm,
    PopulateTableForm,
)
from web_application.models.model import User
from web_application.utils import auth_required, populate_tables

# Creates a blueprint path for authentication views and directs the application to the templates
authentication_blueprint = Blueprint(
    "authentication", __name__, template_folder="../templates/authentication"
)


@authentication_blueprint.route("/logout")
@login_required
def logout():
    """Logs a user out using flask-login's in-built function."""
    logout_user()
    return redirect(url_for("index"))


@authentication_blueprint.route("login", methods=["GET", "POST"])
def login():
    """Logs in the user so they can access protected pages."""
    form = LoginForm()

    if form.validate_on_submit():
        # Gets the requested user object from the database
        user_object = User.query.filter_by(username=form.username.data).first()

        # Checks that a password is entered and if it matches the stored hash
        if user_object.check_password(form.password.data) and user_object is not None:
            login_user(user_object)
            next_page = request.args.get("next")
            if next_page is None or not next[0] == "/":  # pylint: disable=E1136
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html", form=form)


@authentication_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """Registers a new user account and saves it to the database."""
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("authentication.login"))
    return render_template("register.html", form=form)


@authentication_blueprint.route("/populate", methods=["GET", "POST"])
@auth_required()
def populate_db_tables():
    """Populates selected db tables with example entries."""
    form = PopulateTableForm()
    if form.validate_on_submit():
        populate_tables(form.tables.data)
        return redirect(url_for("index"))
    return render_template("populate_tables.html", form=form)
