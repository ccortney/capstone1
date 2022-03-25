"""User Model Tests"""

import os
from sqlite3 import IntegrityError
from unittest import TestCase

from models import db, User, UserActivity
from sqlalchemy.exc import IntegrityError

os.environ['DATABASE_URL'] = "postgresql:///bored-test"

from app import app

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.create_all()

class UserModelTestCase(TestCase):
    """Tests User model."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        UserActivity.query.delete()

        self.client = app.test_client()

        """Add sample user"""

        user1 = User.signup(
            username = "testUser1",
            email = "test1@email.com",
            password = "password")
        db.session.add(user1)
        db.session.commit()

        self.user1 = user1
    
    def tearDown(self):
        """Clean up any fouled transactions"""
        db.session.rollback()
    
    def test_user_model(self):
        """Does user model work?"""

        user2 = User.signup(
            username = "testUser2",
            email = "test2@mail.com",
            password = "password"
        )
        db.session.add(user2)
        db.session.commit()

        #the saved password should not be password, it should be hashed
        self.assertNotEqual(user2.password, "password")
    
    def test_invalid_signup_email(self):
        """Signup should fail if email is not unique"""

        User.signup(
            username = "testUser",
            email = "test1@email.com",
            password = "password"
        )
        
        self.assertRaises(IntegrityError, db.session.commit)
    
    def test_invalid_signup_username(self):
        """Signup should fail if username is not unique"""

        User.signup(
            username = "testUser1",
            email = "test@email.com",
            password = "password"
        )
        
        self.assertRaises(IntegrityError, db.session.commit)
    
    def test_invalid_signup_password(self):
        """Signup should fail if username is not unique"""

        with self.assertRaises(ValueError) as context: 
            User.signup(
                username = "testUser",
                email = "test@email.com",
                password = ""
            )

        with self.assertRaises(ValueError) as context: 
            User.signup(
                username = "testUser",
                email = "test@email.com",
                password = None
            )

    def test_user_login(self):
        """User should be logged in successfully if username
        and password are correct"""

        logged_in_user = User.login("testUser1", "password")
        self.assertIsNotNone(logged_in_user)
        self.assertEqual(self.user1, logged_in_user)
    
    def test_invalid_login_username(self):
        """User should not be logged in if username is incorrect"""

        invalid_user1 = User.login("testUser11", "password")
        self.assertFalse(invalid_user1)
    
    def test_invalid_login_password(self):
        """User should not be logged in if password is incorrect"""

        invalid_user1 = User.login("testUser1", "passwword")
        self.assertFalse(invalid_user1)