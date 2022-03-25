"""User View Tests."""

import os
from unittest import TestCase

from flask import session

from models import db, User, UserActivity
from sqlalchemy.exc import IntegrityError

os.environ['DATABASE_URL'] = "postgresql:///bored-test"

from app import app, CURR_USER_KEY

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Test views for useres."""

    def setUp(self): 
        """Create test client, add sample data."""


        UserActivity.query.delete()
        User.query.delete()

        self.client = app.test_client()

        """Add sample user"""

        user1 = User.signup(
            username = "testUser1",
            email = "test1@email.com",
            password = "password")
        db.session.add(user1)
        db.session.commit()

        self.user1 = user1
        self.user1.id = 999

        """Add sample activities for user"""

        user_activity1 = UserActivity(
            user_id = 999,
            activity_id = 6553978,
            status = "in-progress"
            )
        db.session.add(user_activity1)
        db.session.commit()

        self.user_activity1 = user_activity1

        user_activity2 = UserActivity(
            user_id = 999,
            activity_id = 4809815,
            status = "completed"
        )
        db.session.add(user_activity2)
        db.session.commit()

        self.user_activity2 = user_activity2

    def tearDown(self):
        """Clean up any fouled transactions"""
        db.session.rollback()
    
    def test_site_homepage(self):
        """Do we see the preset activities on the homepage when not logged in?"""

        with self.client as client:
            res = client.get('/')

            self.assertEqual(res.status_code, 200)
            self.assertIn('homepage', str(res.data))
    
    def test_logging_in(self):
        """Can we successfully log in?"""
        
        with self.client as client:
            with client.session_transaction() as sess:
                client.post('/login', data = {'username': 'testUser1', 'password': 'password'})
                self.assertEqual(CURR_USER_KEY, self.user1.id)

    def test_user_homepage(self):
        """Do we see the user's homepage when logged in?"""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
                res = client.get("/home")
            
                self.assertEqual(res.status_code, 200)
                self.assertIn(f"Hi {self.user1.username}", str(res.data))

    # def test_random_activity(self):
    #     """"""
        
    # def test_filter_activity(self):
    #     """"""

    # def test_save_activity(self):
    #     """"""
        
    # def test_complete_activity(self):
    #     """"""

    # def test_remove_inprogress_activity(self):
    #     """"""

    # def test_remove_completed_activity(self):
    #     """"""

    # def test_save_activity_not_loggedin(self):
    #     """"""

    # def test_complete_activity_not_loggedin(self):
    #     """"""

    # def test_remove_activity_not_loggedin(self):
    #     """"""
