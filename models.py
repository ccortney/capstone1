"""SQLAlchemy models for Capstone - Currently Not Named."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    email = db.Column(db.Text, nullable = False, unique = True)
    username = db.Column(db.Text, nullable = False, unique = True)
    password = db.Column(db.Text, nullable = False)


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password):
        """Sign up a user. Hashes password and adds user to system."""
        hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username = username, email = email, password = hashed_password)
        db.session.add(user)
        return user
    
    @classmethod
    def login(cls, username, password):
        """Find user with username and password. 
        This class method searches for a user whose password hash matches this password. 
        If it finds a user, returns that user object. If not, returns False."""

        user = cls.query.filter_by(username = username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        
        return False
    
class UserActivity(db.Model):
    """Stores user and activty status."""

    __tablename__ = 'users_activities'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    activity_id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.Text, nullable = False)

    user = db.relationship('User', backref=db.backref("activities", cascade="all, delete-orphan"))

    def find_inprogress_activities(user_id):
        results = UserActivity.query.filter(UserActivity.user_id == user_id, 
        UserActivity.status == 'in-progress').all()
        return results

    def find_completed_activities(user_id):
        results = UserActivity.query.filter(UserActivity.user_id == user_id, 
        UserActivity.status == 'completed').all()
        return results
    
    def save_activity(user_id, activity_id):
        newRecord = UserActivity(user_id = user_id, activity_id = activity_id, status = 'in-progress')
        db.session.add(newRecord)
        db.session.commit()
    
    def change_status_to_completed(user_id, activity_id):
        result = UserActivity.query.filter(UserActivity.user_id == user_id, 
        UserActivity.activity_id == activity_id).first()
        result.status = "completed"
        db.session.commit()

    def remove_activity(user_id, activity_id):
        result = UserActivity.query.filter(UserActivity.user_id == user_id, 
        UserActivity.activity_id == activity_id).first()
        db.session.delete(result)
        db.session.commit()

    def activities_total_completed(user_id):
        total = UserActivity.query.filter(UserActivity.user_id == user_id, 
        UserActivity.status == 'completed').count()
        return total

    def activities_total_inprogress(user_id):
        total = UserActivity.query.filter(UserActivity.user_id == user_id, 
        UserActivity.status == 'in-progress').count()
        return total

    def activities_total_saved(user_id):
        total_saved = UserActivity.query.filter(UserActivity.user_id == user_id, 
        UserActivity.status == 'in-progress').count()
        total_completed = UserActivity.query.filter(UserActivity.user_id == user_id, 
        UserActivity.status == 'completed').count()
        return total_saved + total_completed
    
    def activities_left(user_id):
        total = UserActivity.query.filter(UserActivity.user_id == user_id, 
        UserActivity.status == 'completed').count()
        activities_left = 185 - total
        return activities_left

    def activities_percent_of_saved(user_id):
        completed_total = UserActivity.query.filter(UserActivity.user_id == user_id, 
        UserActivity.status == 'completed').count()
        saved_total = UserActivity.query.filter(UserActivity.user_id == user_id, 
        UserActivity.status == 'in-progress').count()
        if ((saved_total + completed_total) == 0):
            return 0
        else:
            percent = (round(completed_total/(saved_total + completed_total)*100, 2))

        return percent

class Activity():
    def __init__(self, activity, type, price, participants):
        self.activity = activity
        self.type = type
        self.price = price
        self.participants = participants

activity1 = Activity('Get a Massage', 'Relaxation', '0.4', 1)
activity2 = Activity('Find a Recipe on Instagram', 'Cooking', '0', 1)
activity3 = Activity('Meet up with Friends for a Drink', 'Social', '0.3', 3)
activity4 = Activity('Refurbish a Flea Market Find', 'DIY', '0.5', 2)
activity5 = Activity('Watch a Documentary', 'Education', '0', 1)

preset_activites = [activity1, activity2, activity3, activity4, activity5]
