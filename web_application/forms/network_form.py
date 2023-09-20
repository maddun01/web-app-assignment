## FORM

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional


class AddNetwork(FlaskForm):
    name = StringField("Network Name", validators=[DataRequired()])
    datatype = RadioField(validators=[DataRequired()])
    provenance = StringField("Network Provenance", validators=[DataRequired()])
    format = StringField("Network Format", validators=[DataRequired()])
    submit = SubmitField("Add Network", validators=[DataRequired()])


class UpdateNetwork(FlaskForm):
    network = SelectField(
        "Select a Network", validators=[Optional()], filters=[lambda x: x or None]
    )
    name = StringField(
        "New Network Name", validators=[Optional()], filters=[lambda x: x or None]
    )
    datatype = RadioField(validators=[Optional()], filters=[lambda x: x or None])
    provenance = StringField(
        "New Provenance", validators=[Optional()], filters=[lambda x: x or None]
    )
    format = StringField(
        "New Format", validators=[Optional()], filters=[lambda x: x or None]
    )
    submit = SubmitField(
        "Update", validators=[Optional()], filters=[lambda x: x or None]
    )


class DeleteNetwork(FlaskForm):
    id = IntegerField("Network ID", validators=[DataRequired()])
    submit = SubmitField("Delete network")
