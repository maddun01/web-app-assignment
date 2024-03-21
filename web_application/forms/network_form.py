"""Form for collecting user inputs for creating, updating and deleting devices."""

from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional


from web_application.utils import disallow_characters


class AddNetwork(FlaskForm):
    """Inputs for adding a new network."""

    name = StringField("Network Name", validators=[DataRequired(), disallow_characters])
    datatype = RadioField(validators=[DataRequired()])
    provenance = StringField(
        "Network Provenance", validators=[DataRequired(), disallow_characters]
    )
    network_format = StringField(
        "Network Format", validators=[DataRequired(), disallow_characters]
    )
    submit = SubmitField("Add Network")


class UpdateNetwork(FlaskForm):
    """Optional inputs for updating a saved network configuration."""

    network = SelectField(
        "Select a Network", validators=[Optional()], filters=[lambda x: x or None]
    )
    name = StringField(
        "New Network Name",
        validators=[Optional(), disallow_characters],
        filters=[lambda x: x or None],
    )
    datatype = RadioField(validators=[Optional()], filters=[lambda x: x or None])
    provenance = StringField(
        "New Provenance",
        validators=[Optional(), disallow_characters],
        filters=[lambda x: x or None],
    )
    network_format = StringField(
        "New Network Format",
        validators=[Optional(), disallow_characters],
        filters=[lambda x: x or None],
    )
    submit = SubmitField("Update")


class DeleteNetwork(FlaskForm):
    """Gets the id of a network to delete."""

    id = SelectField("Network", validators=[DataRequired()])
    submit = SubmitField("Delete network")
