"""Form for mimicking starting a Jenkins Run."""

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class KickoffRun(FlaskForm):
    """Inputs for selecting configurations for a new Jenkins run."""

    device_id = SelectField(validators=[DataRequired()])
    network_id = SelectField(validators=[DataRequired()])
    submit = SubmitField("Start Run")
