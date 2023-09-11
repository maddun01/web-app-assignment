## FORM

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SubmitField


class AddDevice(FlaskForm):
    name = StringField("Enter device name: ")
    type = StringField("Enter device type: ")
    os = StringField("Enter operating system: ")
    ip = StringField("RADIO: ")
    submit = SubmitField("Add device")


class DeleteDevice(FlaskForm):
    id = IntegerField("Enter device ID: ")
    submit = SubmitField("Delete device")
