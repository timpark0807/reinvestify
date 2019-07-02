from realtoranalysis import app, db, bcrypt
import json
from flask import render_template, jsonify, request, redirect, url_for, flash, abort, session
from realtoranalysis.forms import Analyze_Form, LoginForm, RegistrationForm
from realtoranalysis.scripts.calculator import Calculations
from realtoranalysis.models import User, Post
from realtoranalysis.scripts.refactor_calculator import Calculate, comma_dollar
from flask_login import login_user, current_user, logout_user, login_required

######################################################################################################
# Error Handler
######################################################################################################


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


@app.errorhandler(403)
def app_forbidden(e):
    return render_template('403.html'), 403


######################################################################################################
# Sidebar Nav
######################################################################################################


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.filter_by().first()
    return render_template('home.html', post=posts)


@app.route("/account")
@login_required
def account():
    return render_template('account.html' )


@app.route("/properties")
@login_required
def properties():
    posts = Post.query.filter_by(id=5).first()
    return render_template('properties.html', post=posts)


@app.route("/about")
def about():
    return render_template('home.html', methods=['POST'])


@app.route("/analyze/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')

    return redirect(url_for('home'))


######################################################################################################
# Login / Logout / Register
######################################################################################################


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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


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


######################################################################################################
# Analyze
######################################################################################################


@app.route("/analyze", methods=['GET', 'POST'])
def analyze():

    """
        This route is used when a user wants to analyze a new property
        When the form is submitted, the form inputs are passed to variables (eg: title = form['title'])
        We initialize a house object where we pass in variables as parameters to make calculations

        If user is logged in, we insert these variables and calculations to a SQL database
        The user is redirected to a route /analyze/<post.id> that requeries this information and displays it

        Else: user is anonymous so we pass the variables and calculations as a dictionary to the jinja2 webpage
    """

    form = Analyze_Form()
    if form.is_submitted():

        # Pass form inputs as variables

        title = request.form['title']
        url = request.form['url']
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
        other = request.form['other']
        expenses = request.form['expenses']
        vacancy = request.form['vacancy']
        appreciation = request.form['appreciation']

        income_growth = request.form['income_growth']
        expense_growth = request.form['expense_growth']

        # call Calculate class and pass in form inputs as parameters
        house = Calculate(price, down, interest, term, rent, expenses, vacancy, closing)

        # call methods of the Calculate class to make calculations , comma_dollar add $ and , to integer
        clean_price = price
        down_payment = house.down_payment()
        mortgage_payment = house.mortgage_payment()
        out_of_pocket = house.outofpocket()
        vacancy_loss = house.vacancy_loss()
        operating_income = house.operating_income()
        operating_expense = house.operating_expense()
        noi = house.noi()
        cash_flow = house.cashflow()
        cap_rate = house.cap_rate()
        coc = house.cashoncash()

        model_year, model_appreciation, model_loan, model_equity = house.year30model(float(appreciation))

        data = {'model_year': model_year,
                'model_appreciation': model_appreciation,
                'model_loan': model_loan,
                'model_equity': model_equity,
                }

        # when user is logged in, current_user is authenticated and redirects to /analyze/<post.id>
        # /analyze/<post.id> queries data from the Post table into variable post 
        # THEN renders analyze_output_2.html while passing in variable post to the .HTML template
        # the .HTML template uses {{ post.title }} to display the database results on the dashboard
        if current_user.is_authenticated:
            user = current_user
            post = Post(title=title,
                        url=url,
                        street=street,
                        city=city,
                        state=state,
                        zipcode=zipcode,

                        type=type,
                        year=year,
                        bed=bed,
                        bath=bath,
                        sqft=sqft,

                        price=clean_price,
                        term=term,
                        down=down,
                        interest=interest,
                        closing=closing,

                        rent=rent,
                        other=other,
                        expenses=expenses,
                        vacancy=vacancy,
                        appreciation=appreciation,

                        mortgage=mortgage_payment,
                        outofpocket=out_of_pocket,
                        cap_rate=cap_rate,
                        coc=coc,
                        operating_income=operating_income,
                        operating_expense=operating_expense,
                        cash_flow=cash_flow,

                        author=user)

            db.session.add(post)
            db.session.commit()
            return redirect(url_for('post', post_id=post.id))

        # below calls current_user.get_id() which returns 'None' when user is NOT logged in
        # redirects to /post_anon route which does not incorporate the <post.id> in route like above
        # /post_anon does NOT query data from the database ... just render templates the dashboard and passes in values
        # else:
        #     post = {'id':0,
        #             'title': title,
        #             'street': street,
        #             'city': city,
        #             'state': state,
        #             'zipcode': zipcode,
        #
        #             'type': type,
        #             'year': year,
        #             'bed': bed,
        #             'bath': bath,
        #             'sqft': sqft,
        #
        #             'price': clean_price,
        #             'term': term,
        #             'down': down,
        #             'interest': interest,
        #             'closing': closing,
        #
        #             'rent': rent,
        #             'other': other,
        #             'expenses': expenses,
        #             'vacancy': vacancy,
        #
        #
        #             'mortgage': mortgage_payment,
        #             'outofpocket': out_of_pocket,
        #             'cap_rate': cap_rate,
        #             'coc': coc,
        #             'operating_income': operating_income,
        #             'operating_expense': operating_expense,
        #             'cash_flow': cash_flow,
        #             'appreciation': appreciation
        #             }
        #
        #     # 30 year model
        #     model_year, model_appreciation, model_loan, model_equity = house.year30model(float(post['appreciation']))
        #
        #     data = {'model_year': model_year,
        #             'model_appreciation': model_appreciation,
        #             'model_loan': model_loan,
        #             'model_equity': model_equity,
        #             }
        #
        #     # cash flow table
        #     cashflow_data = house.income_statement(float(post['other']))
        #
        #     # Pulls data from query, puts it in a dictionary, and runs a function that adds commas and dollars
        #     clean = {'price': comma_dollar(float(post['price'])),
        #              'mortgage': comma_dollar(post['mortgage']),
        #              'outofpocket': comma_dollar(post['outofpocket']),
        #              'cap_rate': post['cap_rate'],
        #              'coc': post['coc'],
        #              'operating_income': comma_dollar(post['operating_income']),
        #              'operating_expense': comma_dollar(post['operating_expense']),
        #              'cash_flow': comma_dollar(post['cash_flow'])
        #              }
        #
        #     return render_template("analyze_output_2.html",
        #                            title=post['title'],
        #                            post=post,
        #                            clean=clean,
        #                            cashflow_data=cashflow_data,
        #                            data=data)

        # if you want to store anon data
        # below calls current_user.get_id() which returns 'None' when user is NOT logged in
        # saves to sqlite with None as usertype
        # redirects to /analyze/anon which doesn't require a post id to view
        else:
            user = current_user.get_id()
            post = Post(title=title,
                        street=street,
                        zipcode=zipcode,
                        price=clean_price,
                        mortgage=mortgage_payment,
                        author=user)

            db.session.add(post)
            db.session.commit()
            return redirect("/analyze/anon")

    return render_template('analyze.html', form=form)


# when user is logged in,
@app.route("/analyze/<int:post_id>")
def post(post_id):
    """ The user is redirected to this route after submitting the form on the /analyze/ route
        As recap, the /analyze/ route submission inserts form inputs into a database
        The database automatically assigns a primary key "post id" to the data

        This route queries the database using the post id as the SQL WHERE clause
        By querying this, we now have access to the variables input on the form and inserted by the /analyze/ route
        We can get price by calling post.price

        This route passes the calculations in as a parameter in render_template()
        Now we can access the calculations in the jinja2 template
    """


    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    house = Calculate(float(post.price),
                      float(post.down),
                      float(post.interest),
                      float(post.term),
                      float(post.rent),
                      float(post.expenses),
                      float(post.vacancy),
                      float(post.closing)
                      )

    # 30 year model
    model_year, model_appreciation, model_loan, model_equity = house.year30model(float(post.appreciation))

    data = {'model_year': model_year,
            'model_appreciation': model_appreciation,
            'model_loan': model_loan,
            'model_equity': model_equity,
            }

    # cash flow table
    cashflow_data = house.income_statement(float(post.other))

    # Pulls data from query, puts it in a dictionary, and runs a function that adds commas and dollars
    clean = {'price': comma_dollar(float(post.price)),
             'mortgage': comma_dollar(post.mortgage),
             'outofpocket': comma_dollar(post.outofpocket),
             'cap_rate': post.cap_rate,
             'coc': post.coc,
             'operating_income': comma_dollar(post.operating_income),
             'operating_expense': comma_dollar(post.operating_expense),
             'cash_flow': comma_dollar(post.cash_flow)
             }

    # can't view report unless you are the user who created it

    return render_template("analyze_output_2.html",
                           title=post.title,
                           post=post,
                           clean=clean,
                           cashflow_data=cashflow_data,
                           data=data)


# when user is logged in and authenticated
@app.route("/analyze/<int:post_id>/update", methods=['GET','POST'])
def update_post(post_id):
    """ This route allows a user to update the form inputs

        This route renders the analyze_update.html template
        This update template differs in that the form inputs preload database information
            Using a GET request
                On load, it first queries the database for information associated with the post_id
                It sets the form inputs as the variables we query from the database

        When we POST this form,
            We insert the form inputs back into the database
            Since when we load the update page, the original information is prefilled into the form,
                Only changes we make will be change data inserted into the database
    """
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = Analyze_Form()
    if form.is_submitted():
        post.title = form.title.data
        post.street = form.street.data
        post.city = form.city.data
        post.state = form.state.data
        post.zipcode = form.zipcode.data

        post.type = form.type.data
        post.year = form.year.data
        post.bed = form.bed.data
        post.bath = form.bath.data
        post.sqft = form.sqft.data

        post.price = form.price.data
        post.down = form.down.data
        post.interest = form.interest.data
        post.closing = form.closing.data

        post.rent = form.grossrent.data
        post.other = form.other.data
        post.expenses = form.expenses.data
        post.vacancy = form.vacancy.data
        post.appreciation = form.appreciation.data

        db.session.commit()

        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.street.data = post.street
        form.city.data = post.city
        form.state.data = post.state
        form.zipcode.data = post.zipcode

        form.type.data = post.type
        form.year.data = post.year
        form.bed.data = post.bed
        form.bath.data = post.bath
        form.sqft.data = post.sqft

        form.price.data = post.price
        form.down.data = post.down
        form.interest.data = post.interest
        form.closing.data = post.closing

        form.grossrent.data = post.rent
        form.other.data = post.other
        form.expenses.data = post.expenses
        form.vacancy.data = post.vacancy
        form.appreciation.data = post.appreciation

    return render_template('analyze_update.html', form=form)


# /analyze2 redirects to this route when current_user is not authenticated bc user is not logged in
@app.route("/analyze/anon")
def post_anon():
    return render_template("analyze_output_2.html", post=post)


######################################################################################################
######################################################################################################
######################################################################################################
# Not in use
######################################################################################################
######################################################################################################
######################################################################################################


@app.route("/analyze2", methods=['GET','POST'])
def analyze2():
    form = Analyze_Form()
    return render_template('analyze_update.html', form=form)


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
        other = request.form['other']
        expenses = request.form['expenses']
        vacancy = request.form['vacancy']

        appreciation = request.form['appreciation']
        income_growth = request.form['income_growth']
        expense_growth = request.form['expense_growth']

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
    return render_template('calculator.html')


@app.route("/process", methods=['POST'])
def process():
    input_price = request.form['price']
    input_down_payment = request.form['down_payment']
    input_term = request.form['term']
    input_interest_rate = request.form['interest_rate']
    input_property_tax = request.form['property_tax']
    input_insurance = request.form['insurance']

    calc = Calculations(input_price, input_down_payment, input_interest_rate, input_term, 0, 0, 0)
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
