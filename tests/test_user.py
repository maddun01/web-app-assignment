import unittest

from utils import clear_selected_table
from web_application import app, db
from web_application.models.model import User
from werkzeug.security import check_password_hash


class UserTests(unittest.TestCase):
    """Unittests for the User database model. Note: running tests will clear the database tables"""

    def test_create_user(self):
        """Creates a new user object and adds it to the db.
        Asserts that the last (newest) entry matches."""
        with app.app_context():
            # Arrange
            clear_selected_table(User)
            email = "test@testcase.com"
            username = "testcase"
            password = "testcase"
            user = User(email, username, password)

            # Act
            db.session.add(user)
            db.session.commit()

            # Assert
            users_list = User.query.all()
            self.assertEqual(users_list[-1].email, email)
            self.assertEqual(users_list[-1].username, username)
            self.assertTrue(check_password_hash(user.password_hash, password))

    def test_delete_user(self):
        """Adds a new user to the table, checks it exists then deletes it.
        Checks if the table is empty."""
        with app.app_context():
            # Arrange
            clear_selected_table(User)
            email = "delete@testcase.com"
            username = "delete_testcase"
            password = "delete_testcase"
            user = User(email, username, password)
            db.session.add(user)
            db.session.commit()
            users_list = User.query.all()
            self.assertEqual(users_list[-1].email, email)

            # Act
            delete_id = user.query.filter_by(email="delete@testcase.com").first().id
            delete_user = db.session.get(User, delete_id)
            db.session.delete(delete_user)
            db.session.commit()
            # Assert
            test = user.query.filter_by(email="delete@testcase.com")
            self.assertEqual(test.all(), [])

    def test_check_password_true(self):
        """Tests the check_password User model function"""
        with app.app_context():
            # Arrange
            clear_selected_table(User)
            email = "delete@testcase.com"
            username = "delete_testcase"
            password = "delete_testcase"
            user = User(email, username, password)
            db.session.add(user)
            db.session.commit()

            # Act
            result = user.check_password(password)

            # Assert
            self.assertTrue(result)

    def test_check_password_false(self):
        """Tests the check_password User model function"""
        with app.app_context():
            # Arrange
            clear_selected_table(User)
            email = "delete@testcase.com"
            username = "delete_testcase"
            password = "delete_testcase"
            user = User(email, username, password)
            db.session.add(user)
            db.session.commit()

            # Act
            false_password = "false_password"
            result = user.check_password(false_password)

            # Assert
            self.assertFalse(result)
