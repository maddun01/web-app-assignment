## FORM

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SelectField, SubmitField


class AddDevice(FlaskForm):
    name = StringField("Device Name")
    type = StringField("Device Type")
    os = StringField("Device Operating System")
    ip = RadioField()
    submit = SubmitField("Add Device")


class UpdateDevice(FlaskForm):
    device = SelectField("Select a Device")
    name = StringField("Current Device Name ")
    type = StringField("Current Type")
    os = StringField("Current OS")
    ip = RadioField()
    submit = SubmitField("Update")


class DeleteDevice(FlaskForm):
    id = IntegerField("Device ID")
    submit = SubmitField("Delete Device")
