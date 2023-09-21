## FORM

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    SelectMultipleField,
    ValidationError,
    widgets,
)
from wtforms.validators import DataRequired, Email, EqualTo, Optional

from web_application.models.model import User


class MultiCheckboxField(SelectMultipleField):
    """Creates a RadioField that can handle multiple selections"""

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class LoginForm(FlaskForm):
    """Allows registered users to access the application"""

    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter password", validators=[DataRequired()])
    submit = SubmitField("Login")

    def validate_username(self, username):
        """Check if the given username is stored in the db"""
        if not User.query.filter_by(username=self.username.data).first():
            raise ValidationError("Username does not exist")

    def validate_password(self, password):
        """Check if the given password matches"""
        user = User.query.filter_by(username=self.username.data).first()
        if user != None:
            if not user.check_password(self.password.data):
                raise ValidationError("Incorrect password")


class RegistrationForm(FlaskForm):
    """Registration form for new users"""

    email = StringField(
        "Enter email", validators=[Email("Invalid Email"), DataRequired()]
    )
    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField(
        "Enter password",
        validators=[
            DataRequired(),
            EqualTo("confirm_password", message="Passwords do not match"),
        ],
    )
    confirm_password = PasswordField("Reenter Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, email):
        """Checks if an account has already been created with the given email"""
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError("Email has already been registered")

    def validate_username(self, username):
        "Checks if a given username is already in use"
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError("Username is already taken")


class PopulateTableForm(FlaskForm):
    """Gathers the selected tables to populate"""

    tables = MultiCheckboxField(
        choices=[("1", "Datatypes"), ("2", "Ips")],
        validators=[Optional()],
    )
    submit = SubmitField("Populate Tables")
