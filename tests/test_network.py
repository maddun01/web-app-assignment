import datetime
import unittest

from utils import clear_selected_table
from web_application import app, db
from web_application.models.model import Network, Datatype


class NetworkTests(unittest.TestCase):
    """Unittests for the Network database model. Note: running tests will clear the database tables"""

    def test_create_network(self):
        """Creates a new network object and adds it to the db.
        Asserts that the last (newest) entry matches."""
        with app.app_context():
            # Arrange

            # create a datatype (to add the foreign key to the network)
            clear_selected_table(Datatype)
            datatype_name = "test"
            datatype = Datatype(datatype_name)
            db.session.add(datatype)
            db.session.commit()

            # create a network
            clear_selected_table(Network)
            name = "test network"
            datatype_id = Datatype.query.filter_by(name=datatype_name).first().id
            provenance = "test provenance"
            format = "test format"
            date_added = datetime.datetime.now()
            network = Network(name, datatype_id, provenance, format, date_added, None)

            # Act
            db.session.add(network)
            db.session.commit()

            # Assert
            networks_list = Network.query.all()
            self.assertEqual(networks_list[-1].name, name)

    def test_delete_network(self):
        """Adds a new network to the table, checks it exists then deletes it.
        Checks if the table is empty."""
        with app.app_context():
            # Arrange

            # create a datatype
            clear_selected_table(Datatype)
            datatype_name = "test"
            datatype = Datatype(datatype_name)
            db.session.add(datatype)
            db.session.commit()

            # create a network
            clear_selected_table(Network)
            name = "test network"
            datatype_id = Datatype.query.filter_by(name=datatype_name).first().id
            provenance = "test provenance"
            format = "test format"
            date_added = datetime.datetime.now()
            network = Network(name, datatype_id, provenance, format, date_added, None)
            db.session.add(network)
            db.session.commit()
            networks_list = Network.query.all()
            self.assertEqual(networks_list[-1].name, name)

            # Act
            delete_id = network.query.filter_by(name=name).first().id
            delete_network = db.session.get(Network, delete_id)
            db.session.delete(delete_network)
            db.session.commit()

            # Assert
            test = network.query.filter_by(name=name)
            self.assertEqual(test.all(), [])
