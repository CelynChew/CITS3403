import unittest

from app import app, db
from config import TestConfig

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        with app.app_context():
            db.create_all()  # Create tables in the test database

    def tearDown(self):
        with app.app_context():
            db.drop_all()  # Drop tables after testing

    # Dummy test
    def test_dummy(self):
        self.assertTrue(True)  # Assert True to indicate the test passed

if __name__ == '__main__':
    unittest.main()