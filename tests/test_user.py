import unittest
from flask_login import current_user
from realtoranalysis import application, db
from realtoranalysis.models import Post


class UserTestCase(unittest.TestCase):


    ################################################################################################
    # Set up and Tear Down
    ################################################################################################

    # Executed prior to each test
    def setUp(self):
        application.config['TESTING'] = True
        application.config['WTF_CSRF_ENABLED'] = False
        application.config['DEBUG'] = False
        application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

        self.application = application.test_client()
        db.drop_all()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.drop_all()
        db.session.close()
        pass

    ################################################################################################
    # Helper Functions
    ################################################################################################

    def add_post(self):
        pass

    def register(self, username, email, password, confirm):
        return self.application.post('/register',
                             data={'username': username,
                                    'email': email,
                                    'password': password,
                                    'confirm_password': confirm})

    def login(self, email, password):
        return self.application.post('/login', data=dict(email=email, password=password))

    def logout(self):
        return self.application.get('/logout', follow_redirects=True)

    ################################################################################################
    # Tests
    ################################################################################################

    def test_user_registration(self):
        # test that the register route returns a successful response
        response = self.application.get('/register')
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
        response = self.application.get('/login')
        self.assertEqual(response.status_code, 200)

        # send a post request to login with registered user info
        response = self.login('user@test.com', 'password')

        # Test that response is a redirect
        self.assertEqual(response.status_code, 302)

    def test_database_table_post(self):
        # test that we can add entries to the post table in our database
        with self.application:
            self.register('user', 'user@test.com', 'password', 'password')
            self.login('user@test.com', 'password')
            user = current_user
            post = Post(title='Test',
                        url='test.com',
                        street='111 West Sesame Street',
                        city='New York',
                        state='NY',
                        zipcode='99999',

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
                        income_growth='3',
                        expense_growth='1',

                        author=user)

            db.session.add(post)
            db.session.commit()

        # query the post we inserted
        query = Post.query.filter_by(title='Test').first()

        # check that query results for a few columns are accurate
        self.assertEqual(query.title, 'Test')
        self.assertEqual(query.interest, '5')
        self.assertEqual(query.rent, '1500')

    def test_database_table_post_floats(self):
        # test that we can add entries to the post table in our database
        with self.application:
            self.register('user', 'user@test.com', 'password', 'password')
            self.login('user@test.com', 'password')
            user = current_user
            post = Post(title='Test',
                        url='test.com',
                        street='111 West Sesame Street',
                        city='New York',
                        state='NY',
                        zipcode='99999',

                        type='Single Family',
                        year='1994',
                        bed='4',
                        bath='3',
                        sqft='2300',

                        price='100000.00',
                        term='30',
                        down='20.00',
                        interest='5.0',
                        closing='3.0',

                        rent='1500.0',
                        other='0',
                        expenses='50.0',
                        vacancy='10.0',
                        appreciation='3.0',
                        income_growth='3.0',
                        expense_growth='1.0',

                        author=user)

            db.session.add(post)
            db.session.commit()

        # query the post we inserted
        query = Post.query.filter_by(title='Test').first()

        # check that query results for a few columns are accurate
        self.assertEqual(query.title, 'Test')
        self.assertEqual(query.interest, '5.0')
        self.assertEqual(query.rent, '1500.0')

    def test_edit_update_delete_post(self):
        # test that we can add, edit, update, and delete entries to the post table in our database
        with self.application:
            self.register('user', 'user@test.com', 'password', 'password')
            self.login('user@test.com', 'password')
            user = current_user
            post = Post(title='Test',
                        url='test.com',
                        street='111 West Sesame Street',
                        city='New York',
                        state='NY',
                        zipcode='99999',

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
                        income_growth='3',
                        expense_growth='1',

                        author=user)

            db.session.add(post)
            db.session.commit()

            # test that we can view the dashboard of property #1
            response = self.application.get('analyze/1')
            self.assertEqual(response.status_code, 200)

            # test that we can access the update form
            response = self.application.get('analyze/1/update')
            self.assertEqual(response.status_code, 200)

            # send a post request to delete property 1
            self.application.post('analyze/1/delete')

            # query all posts and check that the length returned is 0, an empty list
            query = Post.query.all()
            self.assertEqual(len(query), 0)

    def test_edit_update_delete_post_float(self):
        # test that we can add, edit, update, and delete entries to the post table in our database
        with self.application:
            self.register('user', 'user@test.com', 'password', 'password')
            self.login('user@test.com', 'password')
            user = current_user
            post = Post(title='Test',
                        url='test.com',
                        street='111 West Sesame Street',
                        city='New York',
                        state='NY',
                        zipcode='99999',

                        type='Single Family',
                        year='1994',
                        bed='4',
                        bath='3',
                        sqft='2300',

                        price='100000.00',
                        term='30',
                        down='20.00',
                        interest='5.0',
                        closing='3.0',

                        rent='1500.0',
                        other='0',
                        expenses='50.0',
                        vacancy='10.0',
                        appreciation='3.0',
                        income_growth='3.0',
                        expense_growth='1.0',

                        author=user)

            db.session.add(post)
            db.session.commit()

            # test that we can view the dashboard of property with floats
            response = self.application.get('analyze/1')
            self.assertEqual(response.status_code, 200)

            # test that we can access the update form
            response = self.application.get('analyze/1/update')
            self.assertEqual(response.status_code, 200)

            # send a post request to delete property 1
            self.application.post('analyze/1/delete')

            # query all posts and check that the length returned is 0, an empty list
            query = Post.query.all()
            self.assertEqual(len(query), 0)


if __name__ == '__main__':
    unittest.main()
