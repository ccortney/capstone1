from traceback import print_exception
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import Email, DataRequired, Optional

type_choices = [
('','Select Type'),
('busywork','Busywork'),
('charity', 'Charity'),
('cooking','Cooking'),
('diy','DIY'),
('education', 'Education'), 
('music','Music'),
('relaxation','Relaxation'),
('recreational','Recreational'),
('social','Social'),
]
price_choices = [('','Price'), 
('minprice=0&maxprice=0.3', 'Less than $50'), 
('minprice=0.4&maxprice=1','More than $50')]

partipant_choices = [('','Number of Participants'), 
('1', 'Participants: Limit to 1'), ('','Participants: Flexible')]

class UserForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Form for logging users in."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class SearchForm(FlaskForm):
    """Form for searching for/filtering an activity"""

    activity_type = SelectField('Type', choices = type_choices)
    price = SelectField('Price', choices = price_choices)
    participants = SelectField('Number of Participants', choices = partipant_choices)
