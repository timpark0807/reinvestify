import unittest
from realtoranalysis import application


class PageLoadTestCase(unittest.TestCase):
    """"
    Simple test to check whether pages will return a 200 response code (success)
    """

    ################################################################################################
    # Set up and Tear Down
    ################################################################################################

    def setUp(self):
        # creates a test client
        self.application = application.test_client()
        # propagate the exceptions to the test client
        self.application.testing = True

    ################################################################################################
    # Tests
    ################################################################################################

    def test_login_pageload(self):
        # sends HTTP GET request to the application
        # on the specified path
        response = self.application.get('/login')
        self.assertEqual(response.status_code, 200)

    # test /register page
    def test_register_pageload(self):
        response = self.application.get('/register')
        self.assertEqual(response.status_code, 200)

    # test /login page
    def test_home_pageload(self):
        response = self.application.get('/home')
        self.assertEqual(response.status_code, 302)

    # test /analyze page
    def test_analyze_pageload(self):
        response = self.application.get('/analyze')
        self.assertEqual(response.status_code, 308)

    # test /calculator page
    def test_calculator_pageload(self):
        response = self.application.get('/mortgage_calculator')
        self.assertEqual(response.status_code, 308)


if __name__ == '__main__':
    unittest.main()
