from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FloatField


class AnalyzeForm(FlaskForm):
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
