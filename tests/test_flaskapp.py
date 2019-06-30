import unittest
from flask_login import current_user
from realtoranalysis import app, db
from realtoranalysis.models import Post

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

    ################################################################################################
    # Set up and Tear Down
    ################################################################################################

    # Executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

        self.app = app.test_client()
        db.session.remove()
        db.drop_all()
        db.create_all()

    # executed after each test
    def tearDown(self):
        # db.drop_all()
        pass
    ################################################################################################
    # Helper Functions
    ################################################################################################

    def register(self, username, email, password, confirm):
        return self.app.post('/register',
                             data={'username': username,
                                    'email': email,
                                    'password': password,
                                    'confirm_password': confirm})

    def login(self, email, password):
        return self.app.post('/login', data=dict(email=email, password=password))

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    ################################################################################################
    # Tests
    ################################################################################################

    def test_user_registration(self):
        # Register page loads
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

        # send a post request to register with following inputs
        response = self.register('user', 'user@test.com', 'password', 'password')

        # Test that response is a redirect
        self.assertEqual(response.status_code, 302)

    def test_duplicate_user_registration(self):

        # send a post request to /register with following inputs
        response = self.register('user', 'user@test.com', 'password', 'password')

        # assert that this redirects us after successful registration
        self.assertEqual(response.status_code, 302)

        # send another post request to register with the username/email duplicated
        response = self.register('user', 'user@test.com', 'password', 'password')

        # assert this does not redirect us
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):

        # register a user
        self.register('user', 'user@test.com', 'password', 'password')

        # Login page loads
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

        # send a post request to login with registered user info
        response = self.login('user@test.com', 'password')

        # Test that response is a redirect
        self.assertEqual(response.status_code, 302)

    def test_analyze(self):
        with self.app:
            self.register('user', 'user@test.com', 'password', 'password')
            self.login('user@test.com', 'password')
            user = current_user
            post = Post(title='Test',
                        url='test.com',
                        street='21 West Arrellaga',
                        city='Santa Barbara',
                        state='CA',
                        zipcode='93101',

                        type='Single Family',
                        year='1994',
                        bed='4',
                        bath='3',
                        sqft='2300',

                        price='100000',
                        term='30',
                        down='20',
                        interest='5',
                        closing='3',

                        rent='1500',
                        other='0',
                        expenses='50',
                        vacancy='10',
                        appreciation='3',

                        mortgage='429',
                        outofpocket='22000',
                        cap_rate='8',
                        coc='7',
                        operating_income='1350',
                        operating_expense='750',
                        cash_flow='131',

                        author=user)

            db.session.add(post)
            db.session.commit()
            self.assertEqual(post.title, 'Test')

            # response = self.app.post('/analyze',  data=dict(title='Test',
            #                                                 url='test.com',
            #                                                 street='21 West Arrellaga',
            #                                                 city='Santa Barbara',
            #                                                 state='CA',
            #                                                 zipcode='93101',
            #
            #                                                 type='Single Family',
            #                                                 year='1994',
            #                                                 bed='4',
            #                                                 bath='3',
            #                                                 sqft='2300',
            #
            #                                                 price='100000',
            #                                                 term='30',
            #                                                 down='20',
            #                                                 interest='5',
            #                                                 closing='3',
            #
            #                                                 rent='1500',
            #                                                 other='0',
            #                                                 expenses='50',
            #                                                 vacancy='10',
            #                                                 appreciation='3',
            #
            #                                                 mortgage='429',
            #                                                 outofpocket='22000',
            #                                                 cap_rate='8',
            #                                                 coc='7',
            #                                                 operating_income='1350',
            #                                                 operating_expense='750',
            #                                                 cash_flow='131',
            #
            #                                                 author=user))

if __name__ == '__main__':
    unittest.main()
