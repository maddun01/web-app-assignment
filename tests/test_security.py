"""Tests for application authentication"""

import sqlalchemy
import unittest

from flask_login import current_user, login_user, logout_user
from flask_testing import TestCase

from app import index
from web_application import app, db
from web_application.models.model import User


class AuthenticationTests(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "mysecretkey"
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        return app

    def setUp(self):
        db.create_all()
        user = User(
            email="test@email.com", username="test_user", password="test_password"
        )
        db.session.add(user)

        admin_user = User(
            email="testadmin@email.com",
            username="test_admin",
            password="test_admin_password",
        )
        db.session.add(admin_user)
        db.session.commit()
        admin_id = User.query.filter_by(email="testadmin@email.com").first()

        admin = db.session.get(User, admin_id.id)

        admin.is_admin = True
        db.session.add(admin)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login(self):
        """Attempt to login with incorrect credentials"""
        self.client.post(
            "/auth/login",
            data=dict(username="test_user", password="test_password"),
            follow_redirects=True,
        )
        self.assertTrue(current_user.is_authenticated)

    def test_invalid_login(self):
        """Attempt to login with incorrect credentials"""
        response = self.client.post(
            "/auth/login",
            data=dict(username="wrong_user", password="wrong_password"),
            follow_redirects=True,
        )
        self.assertIn(b"Username does not exist", response.data)
        self.assertFalse(current_user.is_authenticated)

    def test_admin_access(self):
        """Test an attempt to access a restricted page with an admin account"""
        login_user(User.query.filter_by(username="test_admin").first())

        response = self.client.get("/auth/populate", follow_redirects=True)

        # This text only appears in the restricted page so can be used to verify access
        self.assertIn(b"Populate Database Tables", response.data)

    def test_restricted_access(self):
        """Test an attempt to access a restricted page with a user account"""
        login_user(User.query.filter_by(username="test_user").first())

        response = self.client.get("/auth/populate", follow_redirects=True)

        self.assertNotIn(b"Populate Database Tables", response.data)

    def test_logout(self):
        """Test logging out a user"""
        login_user(User.query.filter_by(username="test_user").first())

        logout_user()

        self.assertFalse(current_user.is_authenticated)


class InjectionTests(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "mysecretkey"
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        return app

    def setUp(self):
        db.create_all()
        user = User(
            email="test@email.com", username="test_user", password="test_password"
        )
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_sql_injection(self):
        response = self.client.post(
            "/auth/login",
            data=dict(
                username="' OR 1=1 --", password="password", follow_redirects=True
            ),
        )
        self.assertIn(b"Invalid character used", response.data)
