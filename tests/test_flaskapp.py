from realtoranalysis import app, db
import unittest
from flask import url_for
import os

class PageLoadTestCase(unittest.TestCase):
    """"
    Simple test to check whether pages will return a 200 response code (success)
    """

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

  # test /login page
    def test_login(self):
        # sends HTTP GET request to the application
        # on the specified path
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    # test /register page
    def test_register(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    # test /login page
    def test_home(self):
        response = self.app.get('/home')
        self.assertEqual(response.status_code, 200)

    # test /analyze page
    def test_analyze(self):
        response = self.app.get('/analyze')
        self.assertEqual(response.status_code, 200)

    # test /calculator page
    def test_calculator(self):
        response = self.app.get('/calculator')
        self.assertEqual(response.status_code, 200)


class UserTestCase(unittest.TestCase):

    ########################
    # Set up and Tear Down
    ########################

    # Executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    # executed after each test
    def tearDown(self):
        pass

    ########################
    # Helper Functions
    ########################

    def register(self, username, email, password, confirm):
        return self.app.post('/register', data=dict(username=username, email=email, password=password, confirm_password=confirm), follow_redirects=True)

    def login(self, email, password):
        return self.app.post('/login', data=dict(email=email, password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    ########################
    # Tests
    ########################

    def test_user_registration(self):
        # Register page loads
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

        # send a post request to register with following inputs
        response = self.app.post('/register', data={'username': 'user',
                                                    'email': 'user@test.com',
                                                    'password': 'password',
                                                    'confirm_password': 'password'})
        # Test that response is a redirect
        self.assertEqual(response.status_code, 302)

        # send a post request to register for a user with duplicated username and email
        response = self.app.post('/register', data={'username': 'user',
                                                    'email': 'user@test.com',
                                                    'password': 'pass',
                                                    'confirm_password': 'pass'})
        # Test that response is not a redirect
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
