"""UserActivity Model Tests"""

import os
from unittest import TestCase

from models import db, User, UserActivity
from sqlalchemy.exc import IntegrityError

os.environ['DATABASE_URL'] = "postgresql:///bored-test"

from app import app

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.create_all()

class UserActivityModelTestCase(TestCase):
    """Tests UserActivity Model."""

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
    
    def test_save_activity(self):
        """Saving a new activity should increase the count to 2"""
        user_activity3 = UserActivity(
            user_id = 999,
            activity_id = 8926492,
            status = "in-progress"
        )
        db.session.add(user_activity3)
        db.session.commit()

        find_user_activity = UserActivity.query.filter(UserActivity.user_id == 999).count() 

        self.assertEqual(find_user_activity, 3)

        """Should get an integrity error if trying to save an already saved activity"""
        user_activity4 = UserActivity(
            user_id = 999,
            activity_id = 8926492,
            status = "in-progress"
        )
        db.session.add(user_activity4)
        self.assertRaises(IntegrityError, db.session.commit)
    
    def test_find_inprogress_activities(self):
        """Should find all in-progress activities for a user"""

        user_activities = UserActivity.find_inprogress_activities(self.user1.id)
        self.assertEqual(len(user_activities), 1)
    
    def test_find_completed_activities(self):
        """Should find all completed activities for a user"""

        user_activities = UserActivity.find_completed_activities(self.user1.id)
        self.assertEqual(len(user_activities), 1)

    def test_change_status_to_completed(self):
        """Should change status from in-progress to completed"""

        UserActivity.change_status_to_completed(
            self.user1.id, 
            self.user_activity1.activity_id)
        
        user_activities = UserActivity.find_completed_activities(self.user1.id)
        self.assertEqual(len(user_activities), 2)

    def test_remove_activity(self):
        """Should remove an activity that could previously be found"""
        user_activity3 = UserActivity(
            user_id = 999,
            activity_id = 8926492,
            status = "in-progress"
        )
        db.session.add(user_activity3)
        db.session.commit()

        saved_result = UserActivity.query.filter(UserActivity.user_id == user_activity3.user_id, 
        UserActivity.activity_id ==  user_activity3.activity_id).first()
        self.assertIsNotNone(saved_result)
        
        UserActivity.remove_activity(user_activity3.user_id, user_activity3.activity_id)

        deleted_result = UserActivity.query.filter(UserActivity.user_id == user_activity3.user_id, 
        UserActivity.activity_id ==  user_activity3.activity_id).first()
        self.assertIsNone(deleted_result)

    def test_activities_total_completed(self):
        """Should find count of completed activities for a user"""

        user_activities = UserActivity.activities_total_completed(self.user1.id)
        self.assertEqual(user_activities, 1)

    def test_activities_percent_of_saved(self):
        """Should correctly find percent of saved activities completed"""
       
        user_activities = UserActivity.activities_percent_of_saved(self.user1.id)
        self.assertEqual(user_activities, 50.0)


    
    