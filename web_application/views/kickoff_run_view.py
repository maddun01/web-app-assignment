"""View for displaying kickoff run page."""

import datetime
import logging

from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

from web_application import db
from web_application.forms.kickoff_run_form import KickoffRun
from web_application.models.exceptions import AppError
from web_application.models.model import Device, Network
from web_application.utils import set_device_choices, set_network_choices

kickoff_blueprint = Blueprint("kickoff", __name__, template_folder="../templates")

logger = logging.getLogger(__name__)


@kickoff_blueprint.route("/run", methods=["GET", "POST"])
@login_required
def kickoff_run():
    """Mimics the kickoff of a new run on Jenkins"""
    form = KickoffRun()
    form.device_id.choices = set_device_choices()
    form.network_id.choices = set_network_choices()

    if form.validate_on_submit():
        try:

            device = db.session.get(Device, form.device_id.data)
            device.last_run = datetime.datetime.now()
            network = db.session.get(Network, form.network_id.data)
            network.last_run = datetime.datetime.now()
            db.session.add_all([device, network])
            db.session.commit()
        except Exception as e:
            logger.exception(
                "Failed to kickoff run using device id: %s and network id: %s",
                device.id,
                network.id,
            )
            raise AppError("Failed to Kick Off Run") from e
        logger.info(
            "Kicked off run using device id: %s and network id: %s",
            device.id,
            network.id,
        )
        return redirect(url_for("devices.list_devices"))
    return render_template("kickoff_run.html", form=form)
