## VIEW
from flask import Blueprint, redirect, render_template, url_for,flash, request
from flask_login import login_user, login_required, logout_user
from web_application import db
from web_application.forms.authentication_form import LoginForm, RegistrationForm
from web_application.models.model import User

authentication_blueprint = Blueprint(
    "authentication", __name__, template_folder="../templates/authentication"
)

@authentication_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("index"))

@authentication_blueprint.route("login", methods=["GET", "POST"])
def login():
    """Logs in the user so they can access protected pages"""
    form = LoginForm()

    if form.validate_on_submit():
        # gets the requested user object from the database
        user_object = User.query.filter_by(email=form.username.data).first()
        if user_object is not None and user_object.check_password(form.password.data):
            login_user(user_object)
            flash("You have successfully logged in!")
            next_page = request.args.get("next")
            print(next_page)
            if next_page == None or not next[0]=="/":
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html", form=form)

@authentication_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """Registers a new user account and saves it to the database"""
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        
        db.session.add(new_user)
        db.session.commit()
        flash("Successfully registered! Please log in")
        return redirect(url_for("authentication.login"))
    return render_template("register.html", form=form)