## VIEW
import datetime
from flask import Blueprint, redirect, render_template, url_for
from web_application import db
from web_application.forms.network_form import AddNetwork, DeleteNetwork

# from web_application.models.network_model import Network
from web_application.models.model import Network

network_blueprint = Blueprint(
    "networks", __name__, template_folder="../templates/networks"
)


@network_blueprint.route("/add", methods=["GET", "POST"])
def add_network():
    """Adds a new network to the database given a valid form"""
    form = AddNetwork()

    if form.validate_on_submit():
        name = form.name.data
        datatype = form.datatype.data
        provenance = form.provenance.data
        format = form.format.data
        date_added = datetime.datetime.now()
        last_run = datetime.datetime.now()

        new_network = Network(name, datatype, provenance, format, date_added, last_run)
        db.session.add(new_network)
        db.session.commit()
        return redirect(url_for("networks.list_networks"))
    else:
        return render_template("add_network.html", form=form)


@network_blueprint.route("/list")
def list_networks():
    """Displays all current entries in the networks table"""
    networks = Network.query.all()
    return render_template("list_networks.html", networks=networks)


@network_blueprint.route("/delete", methods=["GET", "POST"])
def delete_network():
    """Deletes a given network from the database"""
    form = DeleteNetwork()
    if form.validate_on_submit():
        id = form.id.data
        network_del = db.session.get(Network, id)
        db.session.delete(network_del)
        db.session.commit()
        return redirect(url_for("networks.list_networks"))
    return render_template("delete_network.html", form=form)
