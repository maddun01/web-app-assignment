"""Form for collecting user inputs for registering, logging in and populating "hidden" databases."""

# pylint: disable=W0613
# pylint: disable=R0903

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    SelectMultipleField,
    ValidationError,
    widgets,
)
from wtforms.validators import DataRequired, Email, EqualTo, Optional, Regexp

from web_application.models.model import User


class MultiCheckboxField(SelectMultipleField):
    """Creates a custom WTForms RadioField that can handle multiple selections."""

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class NotEqualTo(EqualTo):
    """Creates a custom WTForms validator that checks given forms do not match"""

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError as exc:
            raise ValidationError(
                field.gettext("Invalid field name '%s'.") % self.fieldname
            ) from exc
        if field.data != other.data:
            return

        d = {
            "other_label": hasattr(other, "label")
            and other.label.text
            or self.fieldname,
            "other_name": self.fieldname,
        }
        message = self.message
        if message is None:
            message = field.gettext("Field must be equal to %(other_name)s.")

        raise ValidationError(message % d)


class LoginForm(FlaskForm):
    """Allows registered users to access the application."""

    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter password", validators=[DataRequired()])
    submit = SubmitField("Login")

    def validate_username(self, username):
        """Check if the given username is stored in the db."""
        if not User.query.filter_by(username=self.username.data).first():
            raise ValidationError("Username does not exist")

    def validate_password(self, password):
        """Check if the given password matches."""
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            if not user.check_password(self.password.data):
                raise ValidationError("Incorrect password")


class RegistrationForm(FlaskForm):
    """Registration form for new users."""

    email = StringField(
        "Enter email", validators=[Email("Invalid Email"), DataRequired()]
    )
    username = StringField(
        "Enter Username",
        validators=[
            DataRequired(),
            Regexp(
                "^[\\w-]+$",
                message="Username must only contain alphanumeric characters",
            ),
        ],
    )
    password = PasswordField(
        "Enter password",
        validators=[
            DataRequired(),
            EqualTo("confirm_password", message="Passwords do not match"),
            NotEqualTo("username", message="Username and password cannot be the same"),
        ],
    )
    confirm_password = PasswordField("Reenter Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, email):
        """Checks if an account has already been created with the given email."""
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError("Email has already been registered")

    def validate_username(self, username):
        "Checks if a given username is already in use."
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError("Username is already taken")


class PopulateTableForm(FlaskForm):
    """Gathers the selected tables to populate."""

    # Custom WTForms field
    tables = MultiCheckboxField(
        choices=[("1", "Datatypes"), ("2", "Ips")],
        validators=[Optional()],
    )
    submit = SubmitField("Populate Tables")
