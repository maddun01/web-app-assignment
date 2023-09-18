## FORM

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from web_application.models.model import User


class LoginForm(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    email = StringField("Enter email", validators=[DataRequired(), Email()])
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
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError("Email has already been registered")

    def validate_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError("Username is already taken")
