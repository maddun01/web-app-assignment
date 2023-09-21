import unittest

from utils import clear_selected_table
from web_application import app, db
from web_application.models.model import Ip


class IpTests(unittest.TestCase):
    """Unittests for the Ip database model. Note: running tests will clear the database tables"""

    def test_create_ip(self):
        """Creates a new ip object and adds it to the db.
        Asserts that the last (newest) entry matches."""
        with app.app_context():
            # Arrange
            clear_selected_table(Ip)
            name = "test"
            ip = Ip(name)

            # Act
            db.session.add(ip)
            db.session.commit()

            # Assert
            ips_list = Ip.query.all()
            self.assertEqual(ips_list[-1].name, name)

    def test_delete_ip(self):
        """Adds a new ip to the table, checks it exists then deletes it.
        Checks if the table is empty."""
        with app.app_context():
            # Arrange
            clear_selected_table(Ip)
            name = "test"
            ip = Ip(name)
            db.session.add(ip)
            db.session.commit()
            ips_list = Ip.query.all()
            self.assertEqual(ips_list[-1].name, name)

            # Act
            delete_id = ip.query.filter_by(name=name).first().id
            delete_ip = db.session.get(Ip, delete_id)
            db.session.delete(delete_ip)
            db.session.commit()

            # Assert
            test = ip.query.filter_by(name=name)
            self.assertEqual(test.all(), [])
