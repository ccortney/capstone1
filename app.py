import os

from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError, DataError

from forms import UserForm, LoginForm, FilterForm
from models import db, connect_db, User, UserActivity, preset_activites
from api import ApiCall

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///bored'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
# toolbar = DebugToolbarExtension(app)

connect_db(app)

##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If logged in, add current user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def login_action(user):
    """Log user in."""
    session[CURR_USER_KEY] = user.id

def logout_action(user):
    """Logs user out."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods = ['GET', 'POST'])
def signup(): 
    """Handles user sign up. 
    Creates a new user, adds to DB, then redirects to the user home page."""

    form = UserForm()
    
    if form.validate_on_submit():
        try: 
            user = User.signup(
                username = form.username.data,
                password = form.password.data, 
                email = form.email.data,
            )
            db.session.commit()
        
        except IntegrityError:
            flash("Username or Email already taken")
            return render_template('signup.html', form = form)
        
        login_action(user)
        return redirect('/home')
    
    else:
        return render_template('signup.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login(): 
    """Handles logging user in."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.login(
                username = form.username.data,
                password = form.password.data)
        
        if user:
            login_action(user)
            return redirect('/home')
        
        else:
            flash("Username or Password not correct")
    
    
    return render_template('login.html', form = form)

@app.route('/logout')
def logout(): 
    """Handles logging user out."""
    if g.user:
        logout_action(g.user)
    
    return redirect('/login')



##############################################################################
# General Routes

@app.route('/')
def boredboard_homepage():
    """Show homepage for non-logged in users"""
    
    if g.user:
        return redirect("/home")
    
    activities = preset_activites

    return render_template('boredboard.html', activities = activities)

@app.route('/home')
def home():
    """Show homepage for logged in users"""

    if not g.user:
        flash("Please login or sign up!", "danger")
        return redirect("/")

    form = FilterForm()
    results = UserActivity.find_inprogress_activities(g.user.id)
    saved_results = []
    for result in results:
        saved_results.append(ApiCall.get_activity_from_key(result.activity_id))
    results = UserActivity.find_completed_activities(g.user.id)
    completed_results = []
    for result in results:
        completed_results.append(ApiCall.get_activity_from_key(result.activity_id))  
    total_completed = UserActivity.activities_total_completed(g.user.id)
    total_saved = UserActivity.activities_total_saved(g.user.id)
    activities_left = UserActivity.activities_left(g.user.id)
    percent_of_saved = UserActivity.activities_percent_of_saved(g.user.id)
             
    return render_template('user_home.html', 
    saved_results = saved_results, 
    completed_results = completed_results, form = form, 
    total_completed = total_completed,
    total_saved = total_saved, 
    activities_left = activities_left, 
    percent_of_saved = percent_of_saved)

##############################################################################
# API routes:

@app.route('/random')
def random_activity():
    """Will return a random activity from the API"""
    if not g.user:
        flash("Please login or sign up!", "danger")
        return redirect("/")

    activity = ApiCall.get_random_activity()
    return activity

# @app.route('/activity/<int:id>')
# def activity_by_key(id):
#     """Will show user activity details for a given activity id"""
#     activity = ApiCall.get_activity_from_key(id)
#     return render_template('activity.html', activity = activity)

@app.route('/activity/<int:activity_id>/save')
def save_activity(activity_id):
    """Will save activity to user's list"""
    if not g.user:
        flash("Please login or sign up!", "danger")
        return redirect("/")
    
    try: 
        UserActivity.save_activity(g.user.id, activity_id)

    except IntegrityError:
            flash("Activity already saved!", 'danger')
            db.session.rollback()
    
    return redirect('/home')

@app.route('/activity/<int:activity_id>/completed')
def complete_activity(activity_id):
    """Will change activity status from in-progress to completed"""
    if not g.user:
        flash("Please login or sign up!", "danger")
        return redirect("/")

    try: 
        UserActivity.change_status_to_completed(g.user.id, activity_id)

    except IntegrityError:
            flash("Activity already saved!", 'danger')
            db.session.rollback()
    
    return redirect('/home')

@app.route('/activity/<int:activity_id>/remove')
def remove_activity(activity_id):
    """Will remove activity from user's list"""
    if not g.user:
        flash("Please login or sign up!", "danger")
        return redirect("/")

    UserActivity.remove_activity(g.user.id, activity_id)
    return redirect('/home')

@app.route('/activitycounts')
def activity_counts():
    """Will return a counts for completed activity by type"""
    if not g.user:
        flash("Please login or sign up!", "danger")
        return redirect("/")

    counts = ApiCall.completed_categories(g.user.id)
    return counts

@app.route('/home', methods = ["POST"])
def filter_activity():
    if not g.user:
        flash("Please login or sign up!", "danger")
        return redirect("/")

    form = FilterForm()
    activity_type = form.activity_type.data
    print(f"activity type: {activity_type}")
    price = form.price.data
    participants = form.participants.data
    activity = ApiCall.get_activity_search(activity_type, price, participants)
    
    return activity