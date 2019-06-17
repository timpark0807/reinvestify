from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField, SelectField
from wtforms.validators import InputRequired

class Analyze_Form(FlaskForm):
    street = StringField('Street', validators=[InputRequired()])
    city = StringField('City')
    state = StringField('State')
    zipcode = StringField('ZipCode')
    type = StringField('Type')
    year = StringField('Year')
    bed = StringField('Bed')
    bath = StringField('Bath')
    sqft = StringField('SqFt')
    price = StringField('Price')
    term = StringField('Term')
    down = StringField('Down')
    interest = StringField('Interest')
    grossrent = StringField('GrossRent')
    grossrent = StringField('Vacancy')
    taxes = StringField('Taxes')
    expenses = StringField('Expenses', validators=[InputRequired()])
    submit = SubmitField('Allocate')
