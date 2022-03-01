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
    
class Activity(db.Model):
    """Stores user and activty status."""

    __tablename__ = 'activities'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    activity_id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.Text, nullable = False)

    user = db.relationship('User', backref=db.backref("activities", cascade="all, delete-orphan"))