import unittest
from flask import current_app
from app import create_app, db
from app.models import User

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testint(self):
        self.assertTrue(current_app.config['TESTING'])

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.u = User(password = 'cat')

    def test_password_setter(self):
        self.assertTrue(self.u.password_hash is not None)

    def test_no_password_getter(self):
        with self.assertRaises(AttributeError):
            self.u.password

    def test_password_verification(self):
        self.assertTrue(self.u.verify_password('cat'))
        self.assertFalse(self.u.verify_password('dog'))

    def test_passwords_salts_are_random(self):
        u2 = User(password = 'cat')
        self.assertTrue(self.u.password_hash != u2.password_hash)            