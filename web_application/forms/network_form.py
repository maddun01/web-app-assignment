"""Form for collecting user inputs for creating, updating and deleting devices."""

from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional


class AddNetwork(FlaskForm):
    """Inputs for adding a new network."""

    name = StringField("Network Name", validators=[DataRequired()])
    datatype = RadioField(validators=[DataRequired()])
    provenance = StringField("Network Provenance", validators=[DataRequired()])
    format = StringField("Network Format", validators=[DataRequired()])
    submit = SubmitField("Add Network")


class UpdateNetwork(FlaskForm):
    """Optional inputs for updating a saved network configuration."""

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
    submit = SubmitField("Update")


class DeleteNetwork(FlaskForm):
    """Gets the id of a network to delete."""

    id = SelectField("Network", validators=[DataRequired()])
    submit = SubmitField("Delete network")
