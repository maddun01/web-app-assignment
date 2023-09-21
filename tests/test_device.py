## Tests for the Device model

import datetime
import unittest

from web_application import app, db
from web_application.models.model import Device, Ip
from web_application.utils import clear_selected_table


class DeviceTests(unittest.TestCase):
    """Unittests for the Device database model. Note: running tests will clear the database tables."""

    def test_create_device(self):
        """Creates a new device object and adds it to the db.
        Asserts that the last (newest) entry matches."""
        with app.app_context():
            # Arrange

            # Create an ip (to add the foreign key to the device)
            clear_selected_table(Ip)
            ip_name = "test"
            ip = Ip(ip_name)
            db.session.add(ip)
            db.session.commit()

            # Create a device
            clear_selected_table(Device)
            name = "test device"
            type = "test type"
            os = "test os"
            ip_id = Ip.query.filter_by(name=ip_name).first().id
            date_added = datetime.datetime.now()
            device = Device(name, type, os, ip_id, date_added, None)

            # Act
            db.session.add(device)
            db.session.commit()

            # Assert
            devices_list = Device.query.all()
            self.assertEqual(devices_list[-1].name, name)

    def test_delete_device(self):
        """Adds a new device to the table, checks it exists then deletes it.
        Checks if the table is empty."""
        with app.app_context():
            # Arrange

            # Create an ip (to add the foreign key to the device)
            clear_selected_table(Ip)
            ip_name = "test"
            ip = Ip(ip_name)
            db.session.add(ip)
            db.session.commit()

            # Create a device
            clear_selected_table(Device)
            name = "test device"
            type = "test type"
            os = "test os"
            ip_id = Ip.query.filter_by(name=ip_name).first().id
            date_added = datetime.datetime.now()
            device = Device(name, type, os, ip_id, date_added, None)

            # Add device to the table and check it exists
            db.session.add(device)
            db.session.commit()
            devices_list = Device.query.all()
            self.assertEqual(devices_list[-1].name, name)

            # Act
            delete_id = device.query.filter_by(name=name).first().id
            delete_device = db.session.get(Device, delete_id)
            db.session.delete(delete_device)
            db.session.commit()

            # Assert
            test = device.query.filter_by(name=name)
            self.assertEqual(test.all(), [])
            clear_selected_table(Ip)
