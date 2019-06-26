from realtoranalysis import app, db, bcrypt
import json
from flask import render_template, jsonify, request, redirect, url_for, flash
from realtoranalysis.forms import Analyze_Form, LoginForm, RegistrationForm
from realtoranalysis.scripts.calculator import Calculations, comma_dollar
from realtoranalysis.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', methods=['POST'])


@app.route("/account")
@login_required
def account():
    return render_template('home.html', methods=['POST'])


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
            # log in with email. Check database to see if email exists
            user = User.query.filter_by(email=form.email.data).first()

            # if user exists, and password matches the hashed password that was created upon registration
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # when form validates, hash the password entered on the form, as a string (utf-8)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # we defined this User class in models.py
        # create a user from form inputs and add it to the database
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'You account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@app.route("/about")
def about():
    return render_template('home.html', methods=['POST'])

@app.route("/data")
def test():
    values = [12, 19, 3]
    labels = ['Red', 'Blue', 'Yellow']
    colors = ['#ff0000','#0000ff','#008000']
    return render_template('interactive_calculator.html', values=values, labels=labels, colors=colors)


@app.route("/get_data")
def handle_test():
    labels = ["Africa", "Asia", "Europe", "Latin America", "North America"]
    data = [5578,5267,734,784,433]
    return jsonify({'payload':json.dumps({'data':data, 'labels':labels})})


@app.route("/analyze", methods=['GET','POST'])
def analyze():
    form = Analyze_Form()
    return render_template('analyze.html', form=form)


@app.route("/handle_analyze", methods=['POST'])
def handle_analyze():
    if request.method == 'POST':
        title = request.form['title']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        type = request.form['type']
        year = request.form['year']
        bed = request.form['bed']
        bath = request.form['bath']
        sqft = request.form['sqft']
        price = request.form['price']
        term = request.form['term']
        down = request.form['down']
        interest = request.form['interest']
        closing = request.form['closing']
        rent = request.form['rent']
        vacancy = request.form['vacancy']
        taxes = request.form['taxes']
        expenses = request.form['expenses']
        appreciation = request.form['appreciation']

        house = Calculations(price, down, interest, term, rent, expenses, vacancy)

        cashflow_data = house.income_statement(10)

        monthly_income = comma_dollar(rent)
        monthly_expense = comma_dollar(house.monthly_expenses())
        mortgage_payment = house.mortgage_calc()
        down_payment = house.downpayment_calc()
        oop = house.outofpocket(closing)
        oi = house.operating_income()
        monthly_noi = house.noi(oi)
        cap_rate = house.cap_rate()

        cash_flow = house.cashflow(monthly_noi, mortgage_payment)
        coc = house.cashoncash(cash_flow, oop)

        clean_oi = comma_dollar(oi)
        clean_down_payment = comma_dollar(down_payment)
        clean_price = comma_dollar(price.replace(',',''))
        clean_mortgage_payment = comma_dollar(mortgage_payment)
        clean_outofpocket = comma_dollar(oop)
        clean_cash_flow = comma_dollar(cash_flow)

        # graph
        model_year, model_appreciation, model_loan, model_equity = house.year30model(appreciation, 2)
        data = {'model_year':model_year,
                'model_appreciation': model_appreciation,
                'model_loan': model_loan,
                'model_equity': model_equity,
                'pie_mortgage': mortgage_payment,
                'pie_expense': house.monthly_expenses(),
                'pie_cashflow': cash_flow,
                'grossrent': comma_dollar(int(rent)),
                'operating_income': clean_oi,
                'operating_expenses': comma_dollar(int(rent) * (1-(int(expenses)/100))),
                'loan_payment': clean_mortgage_payment,
                'cashflow': clean_cash_flow
                }

    return render_template('analyze_output.html', title=title, street=street, city=city, state=state, zipcode=zipcode,
                                                  price=clean_price, type=type, year=year, bed=bed, bath=bath,
                                                  sqft=sqft,
                                                  mortgage_payment=clean_mortgage_payment,
                                                  cap_rate=cap_rate,
                                                  operating_income=clean_oi, expenses=expenses,
                                                  monthly_income=monthly_income, monthly_expense=monthly_expense,
                                                  down_payment=clean_down_payment,
                                                  outofpocket=clean_outofpocket,
                                                  cashflow=clean_cash_flow,
                                                  cashoncash=coc,
                                                  data=data, cashflow_data=cashflow_data)


@app.route("/calculator")
def calculator():
    return render_template('interactive_calculator.html')


@app.route("/process", methods=['POST'])
def process():
    input_price = request.form['price']
    input_down_payment = request.form['down_payment']
    input_term = request.form['term']
    input_interest_rate = request.form['interest_rate']
    input_property_tax = request.form['property_tax']
    input_insurance = request.form['insurance']

    calc = Calculations(input_price, input_down_payment, input_interest_rate, input_term, 0,0,0)
    down_payment = calc.downpayment_calc()
    mortgage_payment = calc.mortgage_calc()


    # Calculates the payment with input as float
    # down_payment = downpayment_calc(float(input_price),
    #                                 float(input_down_payment))
    #
    # mortgage_payment = mortgage_calc(float(input_price),
    #                                  float(input_down_payment),
    #                                  float(input_interest_rate),
    #                                  input_term)

    # Returns floats as a string with dollar sign and comma separators
    down_payment_clean = comma_dollar(down_payment)
    mortgage_payment_clean = comma_dollar(mortgage_payment)


    labels = ["Mortgage", "Taxes", "Insurance"]
    number = [int(mortgage_payment), int(input_property_tax), int(input_insurance)]
    total = int(mortgage_payment) + int(input_property_tax) + int(input_insurance)

    return jsonify({'mortgage_payment': mortgage_payment_clean,
                    'down_payment': down_payment_clean,
                    'number': number,
                    'labels': labels,
                    'total': total
                })
