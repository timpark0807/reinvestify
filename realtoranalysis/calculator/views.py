from . import calculator as calc
from .forms import MortgageCalculatorForm
from flask import render_template, request
from .functions import remove_comma, get_mortgage_calculator_json


@calc.route('/')
def calculator():
    form = MortgageCalculatorForm()
    return render_template('calculator.html', form=form)


@calc.route('/process', methods=['POST'])
def process():
    """ Captures user input on the front end mortgage calculator form.
        Returns a json containing chart information.
    """
    input_price = remove_comma(request.form['price'])
    input_down_payment = request.form['down_payment']
    input_term = request.form['term']
    input_interest_rate = request.form['interest_rate']
    input_property_tax = request.form['property_tax']
    input_insurance = request.form['insurance']

    values = (input_price, input_down_payment, input_term, input_interest_rate, input_property_tax, input_insurance)
    json = get_mortgage_calculator_json(values)
    return json
