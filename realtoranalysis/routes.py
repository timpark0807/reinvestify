from realtoranalysis import app
import json
from flask import render_template, jsonify, request
from realtoranalysis.scripts.calculator import mortgage_calc, downpayment_calc


@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', methods=['POST'])


@app.route("/about")
def about():
    return render_template('about.html', methods=['POST'])


@app.route("/data")
def test():
    values = [12, 19, 3]
    labels = ['Red', 'Blue', 'Yellow']
    colors = ['#ff0000','#0000ff','#008000']
    return render_template('calculator.html', values=values, labels=labels, colors=colors)


@app.route("/get_data")
def handle_test():
    labels = ["Africa", "Asia", "Europe", "Latin America", "North America"]
    data = [5578,5267,734,784,433]
    return jsonify({'payload':json.dumps({'data':data, 'labels':labels})})


@app.route("/analyze")
def analyze():
    return render_template('analyze.html', methods=['POST'])


@app.route("/calculator")
def calculator():
    return render_template('calculator.html')


@app.route("/process", methods=['POST'])
def process():
    input_price = request.form['price']
    input_down_payment = request.form['down_payment']
    input_term = request.form['term']
    input_interest_rate = request.form['interest_rate']

    down_payment = downpayment_calc(float(input_price),
                                    float(input_down_payment))

    mortgage_payment = mortgage_calc(float(input_price),
                                     float(input_down_payment),
                                     float(input_interest_rate),
                                     input_term)

    return jsonify({'mortgage_payment': mortgage_payment, 'down_payment': down_payment})
