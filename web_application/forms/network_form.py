## FORM

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SelectField, SubmitField


class AddNetwork(FlaskForm):
    name = StringField("Network Name")
    datatype = RadioField()
    provenance = StringField("Network Provenance")
    format = StringField("Network Format")
    submit = SubmitField("Add Network")


class UpdateNetwork(FlaskForm):
    network = SelectField("Select a Network")
    name = StringField("Current Network Name ")
    datatype = RadioField()
    provenance = StringField("Current Provenance")
    format = StringField("Current Format")
    submit = SubmitField("Update")


class DeleteNetwork(FlaskForm):
    id = IntegerField("Network ID")
    submit = SubmitField("Delete network")
