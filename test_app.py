import app
import unittest


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def test_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status, '200 OK')


if __name__ == "__main__":
    unittest.main()
