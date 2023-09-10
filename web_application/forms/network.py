## FORM

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SubmitField


class AddNetwork(FlaskForm):
    name = StringField("Enter network name: ")
    datatype = StringField("RADIO ")
    provenance = StringField("Enter provenance: ")
    format = StringField("Enter format: ")
    submit = SubmitField("Add network")


class DeleteNetwork(FlaskForm):
    id = IntegerField("Enter network ID: ")
    submit = SubmitField("Delete network")
