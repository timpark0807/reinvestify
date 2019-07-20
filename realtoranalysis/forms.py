from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, FloatField
from wtforms.validators import InputRequired, DataRequired, Email, Length, EqualTo, ValidationError
from realtoranalysis.models import User
from flask_wtf.file import FileField, FileAllowed

class Analyze_Form(FlaskForm):
    # Form 1
    title = StringField('Title')
    url = StringField('URL')
    street = StringField('Street')
    city = StringField('City')
    state = StringField('State')
    zipcode = StringField('ZipCode')

    # Form 2
    type = SelectField(label='Type',
                       choices=[('Single Family', 'Single Family'),
                                ('Multi Family', 'Multi Family'),
                                ('Apartment', 'Apartment Unit'),
                                ('Condo', 'Condo'),])
    year = StringField('Year')
    bed = StringField('Bed')
    bath = StringField('Bath')
    sqft = StringField('SqFt')

    # Form 3
    price = StringField('Price')
    term = SelectField(label='Term',
                       choices=[
                                ('30', '30 Year Fixed'),
                                ('15', '15 Year Fixed')])

    down = FloatField('Down')
    interest = FloatField('Interest')
    closing = FloatField('Closing')

    # Form 4
    grossrent = StringField('GrossRent')
    other = StringField('Other Income')
    vacancy = FloatField('Vacancy')
    taxes = FloatField('Taxes')
    expenses = FloatField('Expenses')
    appreciation = FloatField('Appreciation')
    income_growth = FloatField('Income Growth')
    expense_growth = FloatField('Expense Growth')

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
