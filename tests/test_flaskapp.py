from realtoranalysis import app
import unittest

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

    # test /login page
    def test_register(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    # test /login page
    def test_home(self):
        response = self.app.get('/home')
        self.assertEqual(response.status_code, 200)

    # test /calculator page
    def test_calculator(self):
        response = self.app.get('/calculator')
        self.assertEqual(response.status_code, 200)

    # test /analyze page
    def test_analyze(self):
        response = self.app.get('/analyze')
        self.assertEqual(response.status_code, 200)

    # test /BH_PS page
    def test_analyze2(self):
        response = self.app.get('/analyze2')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
