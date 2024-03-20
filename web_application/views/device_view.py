"""Views for displaying various device pages."""

# pylint: disable=R1705

import datetime
import logging
from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

from web_application import db
from web_application.forms.device_form import AddDevice, UpdateDevice, DeleteDevice
from web_application.models.exceptions import AppError
from web_application.models.model import Device, Ip
from web_application.utils import (
    auth_required,
    generate_device_dict,
    set_device_choices,
)

device_blueprint = Blueprint(
    "devices", __name__, template_folder="../templates/devices"
)

logger = logging.getLogger(__name__)


@device_blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add_device():
    """Adds a new device to the database given a valid form."""
    form = AddDevice()
    form.ip.choices = [(ip.id, ip.name) for ip in Ip.query.all()]

    if form.validate_on_submit():
        try:
            name = form.name.data
            device_type = form.device_type.data
            os = form.os.data
            ip = form.ip.data
            date_added = datetime.datetime.now()

            new_device = Device(name, device_type, os, ip, date_added, None)
            db.session.add(new_device)
            db.session.commit()
        except Exception as e:
            logger.exception("Failed to save device: %s", str(new_device))
            raise AppError("Failed to Save New Device") from e
        logger.info("New device saved: %s", str(new_device))
        return redirect(url_for("devices.list_devices"))
    else:
        return render_template("add_device.html", form=form)


@device_blueprint.route("/update", methods=["GET", "POST"])
@login_required
def update_device():
    """Updates a chosen device with the given data."""
    form = UpdateDevice()
    form.ip.choices = [(ip.id, ip.name) for ip in Ip.query.all()]
    form.device.choices = set_device_choices()

    if form.validate_on_submit():
        try:
            device = form.device.data
            updated_device = Device.query.get(device)

            # Mapping to replace bulky "if not None" statements
            field_mapping = {
                "name": ("name", form.name.data),
                "device_type": ("device_type", form.device_type.data),
                "os": ("os", form.os.data),
                "ip_id": ("ip_id", form.ip.data),
            }

            # Sets each of the device fields to the new data, if given
            for field, (  # pylint: disable=W0612
                device_field,
                data,
            ) in field_mapping.items():
                if data is not None:
                    setattr(updated_device, device_field, data)

            db.session.add(updated_device)
            db.session.commit()
        except Exception as e:
            logger.exception("Failed to update new device: %s", str(updated_device))
            raise AppError("Failed to Update Device")
        logger.info("Device with id %s updated", updated_device.id)
        return redirect(url_for("devices.list_devices"))
    return render_template("update_device.html", form=form)


@device_blueprint.route("/list")
@login_required
def list_devices():
    """Displays all current entries in the devices table."""
    devices = Device.query.all()
    device_dicts = generate_device_dict(devices)
    return render_template("list_devices.html", devices=device_dicts)


@device_blueprint.route("/delete", methods=["GET", "POST"])
@auth_required()
def delete_device():
    """Deletes a given device from the database."""
    form = DeleteDevice()
    form.id.choices = set_device_choices()

    if form.validate_on_submit():
        try:
            device_id = form.id.data
            device_del = db.session.get(Device, device_id)
            db.session.delete(device_del)
            db.session.commit()
        except Exception as e:
            logger.exception("Failed to delete device with id %s", device_id)
            raise AppError("Failed to Delete Device") from e
        logger.info("Deleted device with id %s", device_id)
        return redirect(url_for("devices.list_devices"))
    return render_template("delete_device.html", form=form)
