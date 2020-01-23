from . import calculator as calc
from .forms import MortgageCalculatorForm
from flask import render_template, request
from .functions import get_mortgage_calculator_json


@calc.route('/')
def calculator():
    form = MortgageCalculatorForm()
    return render_template('calculator.html', form=form)


@calc.route('/process', methods=['POST'])
def process():
    """
        AJAX call sends a POST request containing form values to this route
        Pass the form values into the calculate function which
        Returns a json containing mortgage payment.
    """
    form_values = request.form.values()
    json = get_mortgage_calculator_json(form_values)
    return json
