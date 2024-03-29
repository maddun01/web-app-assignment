"""Form for collecting user inputs for creating, updating and deleting devices."""

from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional


from web_application.utils import disallow_characters


class AddDevice(FlaskForm):
    """Inputs for a new device."""

    name = StringField("Device Name", validators=[DataRequired(), disallow_characters])
    device_type = StringField(
        "Device Type", validators=[DataRequired(), disallow_characters]
    )
    os = StringField(
        "Device Operating System", validators=[DataRequired(), disallow_characters]
    )
    ip = RadioField(validators=[DataRequired()])
    submit = SubmitField("Add Device")


class UpdateDevice(FlaskForm):
    """Optional inputs for updating a saved device configuration."""

    device = SelectField(
        "Select a Device", validators=[Optional()], filters=[lambda x: x or None]
    )
    name = StringField(
        "New Device Name",
        validators=[Optional(), disallow_characters],
        filters=[lambda x: x or None],
    )
    device_type = StringField(
        "New Device Type",
        validators=[Optional(), disallow_characters],
        filters=[lambda x: x or None],
    )
    os = StringField(
        "New OS",
        validators=[Optional(), disallow_characters],
        filters=[lambda x: x or None],
    )
    ip = RadioField(validators=[Optional()], filters=[lambda x: x or None])
    submit = SubmitField("Update")


class DeleteDevice(FlaskForm):
    """Gets the id of a selected device to delete."""

    id = SelectField("Device", validators=[DataRequired()])
    submit = SubmitField("Delete Device")
