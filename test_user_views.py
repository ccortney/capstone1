"""User View Tests."""

import os
from unittest import TestCase

from flask import session
from api import ApiCall

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
            client.post('/login', 
                    data = {'username': 'testUser1', 'password': 'password'})
            
            self.assertEqual(session[CURR_USER_KEY], self.user1.id)

    def test_user_homepage(self):
        """Do we see the user's homepage when logged in?"""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            
            res = client.get("/home")
        
            self.assertEqual(res.status_code, 200)
            self.assertIn(f"Hi {self.user1.username}", str(res.data))

    def test_random_activity(self):
        """Should randomly get a new activity when random button clicked"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            
            res1 = client.get("/random")
            data1 = res1.json
        
            res2 = client.get("/random")
            data2 = res2.json

            self.assertNotEqual(data1, data2)      
    
    def test_filter_activity(self):
        """Should correctly filter for an activity"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            activity_type = "cooking"
            price = ""
            participants = ""
            
            res = ApiCall.get_activity_search(activity_type, price, participants)

            self.assertEqual(res['type'], 'cooking')

            activity_type = ""
            price = ""
            participants = 4
            
            res = ApiCall.get_activity_search(activity_type, price, participants)

            self.assertEqual(res['participants'], 4)

    def test_save_activity(self):
        """When an activity is saved, it shows up in the saved list both 
        in the database and on the webpage"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            activity_id = 1799120
            user_activities = UserActivity.query.filter(UserActivity.user_id == self.user1.id).all()
            user_activities_ids = [activity.activity_id for activity in user_activities]
            self.assertNotIn(1799120, user_activities_ids)

            res = client.get(f'/activity/{activity_id}/save', follow_redirects = True)
        
            user_activities = UserActivity.query.filter(UserActivity.user_id == self.user1.id).all()
            user_activities_ids = [activity.activity_id for activity in user_activities]
            self.assertIn(1799120, user_activities_ids)

            self.assertIn(f'<a href="/activity/{activity_id}/completed">Completed</a>', str(res.data))

        
    def test_complete_activity(self):
        """When an activity is completed, the status in the 
        database should change and move to the completed list"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            
                completed_activities = UserActivity.query.filter(
                    UserActivity.user_id == self.user1.id, 
                    UserActivity.status == "completed").all()
                completed_activities_ids = [activity.activity_id for activity in completed_activities]
                self.assertNotIn(self.user_activity1.activity_id, completed_activities_ids)

            res = client.get(f'/activity/{self.user_activity1.activity_id}/completed', follow_redirects = True)

            completed_activities = UserActivity.query.filter(
                UserActivity.user_id == self.user1.id, 
                UserActivity.status == "completed").all()
            completed_activities_ids = [activity.activity_id for activity in completed_activities]
            self.assertIn(self.user_activity1.activity_id, completed_activities_ids)

            self.assertNotIn(f'<a href="/activity/{self.user_activity1.activity_id}/completed">Completed</a>', str(res.data))
            self.assertIn(f'<a href="/activity/{self.user_activity1.activity_id}/remove">Remove</a>', str(res.data))


    def test_remove_inprogress_activity(self):
        """Should remove an activity from the database and webpage"""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            
                user_activities = UserActivity.query.filter(UserActivity.user_id == self.user1.id).all()
                user_activities_ids = [activity.activity_id for activity in user_activities]
                self.assertIn(self.user_activity1.activity_id, user_activities_ids)
            
            res = client.get(f'/activity/{self.user_activity1.activity_id}/remove', follow_redirects = True)

            user_activities = UserActivity.query.filter(UserActivity.user_id == self.user1.id).all()
            user_activities_ids = [activity.activity_id for activity in user_activities]
            self.assertNotIn(self.user_activity1.activity_id, user_activities_ids)

            self.assertNotIn(f'<a href="/activity/{self.user_activity1.activity_id}/remove">Remove</a>', str(res.data))

    def test_remove_completed_activity(self):
        """Should remove an activity from the database and webpage"""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            
                user_activities = UserActivity.query.filter(UserActivity.user_id == self.user1.id).all()
                user_activities_ids = [activity.activity_id for activity in user_activities]
                self.assertIn(self.user_activity1.activity_id, user_activities_ids)
            
            res = client.get(f'/activity/{self.user_activity2.activity_id}/remove', follow_redirects = True)

            user_activities = UserActivity.query.filter(UserActivity.user_id == self.user1.id).all()
            user_activities_ids = [activity.activity_id for activity in user_activities]
            self.assertNotIn(self.user_activity2.activity_id, user_activities_ids)

            self.assertNotIn(f'<a href="/activity/{self.user_activity2.activity_id}/remove">Remove</a>', str(res.data))

    def test_save_activity_not_loggedin(self):
        """User should be redirected to homepage if not logged in"""
        
        with self.client as client:

            activity_id = 1799120
            res = client.get(f'/activity/{activity_id}/save', follow_redirects = True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('homepage', str(res.data))

    def test_complete_activity_not_loggedin(self):
        """User should be redirected to homepage if not logged in"""
        
        with self.client as client:

            res = client.get(f'/activity/{self.user_activity1.activity_id}/completed', follow_redirects = True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('homepage', str(res.data))

    def test_remove_activity_not_loggedin(self):
        """User should be redirected to homepage if not logged in"""
        
        with self.client as client:

            res = client.get(f'/activity/{self.user_activity1.activity_id}/remove', follow_redirects = True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('homepage', str(res.data))
