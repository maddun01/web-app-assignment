"""Views for displaying various network pages."""

import datetime
from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

from web_application import db
from web_application.forms.network_form import AddNetwork, UpdateNetwork, DeleteNetwork
from web_application.models.model import Network, Datatype
from web_application.utils import (
    auth_required,
    generate_network_dict,
    set_network_choices,
)

network_blueprint = Blueprint(
    "networks", __name__, template_folder="../templates/networks"
)


@network_blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add_network():
    """Adds a new network to the database given a valid form."""
    form = AddNetwork()
    form.datatype.choices = [
        (datatype.id, datatype.name) for datatype in Datatype.query.all()
    ]
    if form.validate_on_submit():
        name = form.name.data
        datatype = form.datatype.data
        provenance = form.provenance.data
        format = form.format.data
        date_added = datetime.datetime.now()

        new_network = Network(name, datatype, provenance, format, date_added, None)
        db.session.add(new_network)
        db.session.commit()
        return redirect(url_for("networks.list_networks"))
    else:
        return render_template("add_network.html", form=form)


@network_blueprint.route("/update", methods=["GET", "POST"])
@login_required
def update_network():
    """Updates a chosen network with the given data."""
    form = UpdateNetwork()
    form.datatype.choices = [
        (datatype.id, datatype.name) for datatype in Datatype.query.all()
    ]
    form.network.choices = set_network_choices()

    if form.validate_on_submit():
        network = form.network.data
        updated_network = Network.query.get(network)

        # Mapping to replace bulky "if not None" statements
        field_mapping = {
            "name": ("name", form.name.data),
            "datatype_id": ("datatype_id", form.datatype.data),
            "provenance": ("provenance", form.provenance.data),
            "format": ("format", form.format.data),
        }

        # Sets each of the network fields to the new data, if given
        for field, (network_field, data) in field_mapping.items():
            if data is not None:
                setattr(updated_network, network_field, data)

        db.session.add(updated_network)
        db.session.commit()
        return redirect(url_for("networks.list_networks"))
    return render_template("update_network.html", form=form)


@network_blueprint.route("/list")
@login_required
def list_networks():
    """Displays all current entries in the networks table."""
    networks = Network.query.all()
    network_dicts = generate_network_dict(networks)
    return render_template("list_networks.html", networks=network_dicts)


@network_blueprint.route("/delete", methods=["GET", "POST"])
@auth_required()
def delete_network():
    """Deletes a given network from the database."""
    form = DeleteNetwork()
    form.id.choices = set_network_choices()
    if form.validate_on_submit():
        id = form.id.data
        network_del = db.session.get(Network, id)
        db.session.delete(network_del)
        db.session.commit()
        return redirect(url_for("networks.list_networks"))
    return render_template("delete_network.html", form=form)
