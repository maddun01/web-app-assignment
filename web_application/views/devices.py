## VIEW
import datetime
from flask import Blueprint, redirect, render_template, url_for
from web_application import db
from web_application.forms.device import AddDevice
from web_application.models import Device

device_blueprint = Blueprint(
    "devices", __name__, template_folder="../templates/devices"
)


@device_blueprint.route("/add", methods=["GET", "POST"])
def add_device():
    form = AddDevice()

    if form.validate_on_submit:
        name = form.name.data
        type = form.type.data
        os = form.os.data
        ip = form.ip.data
        date_added = datetime.datetime.now()
        last_run = datetime.datetime.now()

        new_device = Device(name, type, os, ip, date_added, last_run)
        db.session.add(new_device)
        db.session.commit()
        return redirect(url_for("devices.list"))
    else:
        return render_template("add_device.html")
