import unittest

from app import app, db
from app.models import User
from config import TestConfig

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all() # Create tables in the test database

    def tearDown(self):
        db.session.remove()
        db.drop_all() # Drop tables after testing
        self.app_context.pop()

    def test_username_uniqueness(self):
        # Create a user with a unique username
        user1 = User(username='test_user', password='password')
        db.session.add(user1)
        db.session.commit()

        # Attempt to create another user with the same username
        user2 = User(username='test_user', password='password')
        db.session.add(user2)

        # Assert that adding the second user raises an IntegrityError
        with self.assertRaises(Exception) as context:
            db.session.commit()
        self.assertTrue('UNIQUE constraint failed: user.username' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
