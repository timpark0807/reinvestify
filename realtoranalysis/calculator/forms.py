from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, FloatField


class MortgageCalculatorForm(FlaskForm):

    price = StringField('Purchase Price', default='100,000')
    down_payment = StringField('Downpayment', default='20')
    term = SelectField(label='Term',
                       choices=[('30', '30 Year Fixed'),
                                ('15', '15 Year Fixed')])
    interest_rate = StringField('Interest Rate', default='5.0')
    property_tax = StringField('Property Tax', default='100')
    insurance = StringField('Insurance', default='90')
    submit = SubmitField()
