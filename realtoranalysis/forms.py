from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField, PasswordField, IntegerField
from wtforms.validators import InputRequired, DataRequired, Email, Length, EqualTo, ValidationError
from realtoranalysis.models import User


class Analyze_Form(FlaskForm):
    street = StringField('Street', validators=[InputRequired()])
    city = StringField('City')
    state = StringField('State')
    zipcode = IntegerField('ZipCode')
    type = StringField('Type')
    year = IntegerField('Year')
    bed = IntegerField('Bed')
    bath = IntegerField('Bath')
    sqft = IntegerField('SqFt')
    price = IntegerField('Price')
    term = IntegerField('Term')
    down = IntegerField('Down')
    closing = IntegerField('Closing')
    interest = IntegerField('Interest')
    grossrent = IntegerField('GrossRent')
    vacancy = IntegerField('Vacancy')
    taxes = IntegerField('Taxes')
    expenses = IntegerField('Expenses', validators=[InputRequired()])
    appreciation = IntegerField('Appreciation')
    submit = SubmitField('Allocate')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Please choose a different one.')
