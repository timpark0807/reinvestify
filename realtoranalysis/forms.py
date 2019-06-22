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
    closing = StringField('Closing')
    interest = StringField('Interest')
    grossrent = StringField('GrossRent')
    vacancy = StringField('Vacancy')
    taxes = StringField('Taxes')
    expenses = StringField('Expenses', validators=[InputRequired()])
    appreciation = StringField('Appreciation')
    submit = SubmitField('Allocate')
