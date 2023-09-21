## Tests for the Datatype model

import unittest

from web_application import app, db
from web_application.models.model import Datatype
from web_application.utils import clear_selected_table


class DatatypeTests(unittest.TestCase):
    """Unittests for the Datatype database model. Note: running tests will clear the database tables."""

    def test_create_datatype(self):
        """Creates a new datatype object and adds it to the db.
        Asserts that the last (newest) entry matches."""
        with app.app_context():
            # Arrange
            clear_selected_table(Datatype)
            name = "test"
            datatype = Datatype(name)

            # Act
            db.session.add(datatype)
            db.session.commit()

            # Assert
            datatypes_list = Datatype.query.all()
            self.assertEqual(datatypes_list[-1].name, name)

    def test_delete_datatype(self):
        """Adds a new datatype to the table, checks it exists then deletes it.
        Checks if the table is empty."""
        with app.app_context():
            # Arrange
            clear_selected_table(Datatype)
            name = "test"
            datatype = Datatype(name)
            db.session.add(datatype)
            db.session.commit()
            datatypes_list = Datatype.query.all()
            self.assertEqual(datatypes_list[-1].name, name)

            # Act
            delete_id = datatype.query.filter_by(name=name).first().id
            delete_datatype = db.session.get(Datatype, delete_id)
            db.session.delete(delete_datatype)
            db.session.commit()

            # Assert
            test = datatype.query.filter_by(name=name)
            self.assertEqual(test.all(), [])
