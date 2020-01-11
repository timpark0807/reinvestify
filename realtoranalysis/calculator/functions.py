from realtoranalysis.scripts.property_calculations import Calculate, comma_dollar
from flask import jsonify


def remove_comma(number):
    if ',' in number:
        return number.replace(',', '')
    else:
        return str(number)


def get_mortgage_calculator_json(values):
    input_price, input_down_payment, input_term, input_interest_rate, input_property_tax, input_insurance = values
    calc = Calculate(input_price, input_down_payment, input_interest_rate, input_term, 0, 0, 0, 0, 0)
    mortgage_payment = calc.mortgage_payment()

    # Returns floats as a string with dollar sign and comma separators
    mortgage_payment_processed = comma_dollar(mortgage_payment)

    chart_labels = ['Mortgage', 'Taxes', 'Insurance']
    chart_values = [int(mortgage_payment), int(input_property_tax), int(input_insurance)]
    total = int(mortgage_payment) + int(input_property_tax) + int(input_insurance)

    return jsonify({'mortgage_payment': mortgage_payment_processed,
                     'number': chart_values,
                     'labels': chart_labels,
                     'total': total
                     })
