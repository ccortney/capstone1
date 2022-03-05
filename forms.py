from traceback import print_exception
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import Email, DataRequired, Optional

type_choices = [
('null','Select Type'),
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
price_choices = [('null','Price'), ('less', 'Less than $50'), ('more','More than $50')]

partipant_choices = [('null','Number of Participants'), ('1', 'One'), ('2','More than One')]

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

    keyword = StringField('Keyword')
    activity_type = SelectField('Type', choices = type_choices)
    price = SelectField('Price', choices = price_choices)
    participants = SelectField('Number of Participants', choices = partipant_choices)
