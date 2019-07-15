import secrets
import os
from PilLite import Image
from realtoranalysis import app, db, bcrypt
from flask import render_template, jsonify, request, redirect, url_for, flash, abort, session
from realtoranalysis.forms import Analyze_Form, LoginForm, RegistrationForm
from realtoranalysis.models import User, Post
from realtoranalysis.scripts.property_calculations import Calculate, comma_dollar, handle_comma, remove_comma_dollar
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


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/account')
@login_required
def account():
    return render_template('account.html' )


@app.route('/properties')
@login_required
def properties():
    if current_user.is_authenticated:
        user = current_user.id

    posts = Post.query.filter_by(user_id=user).all()

    if posts == []:
        return redirect(url_for('analyze'))

    return render_template('properties.html', posts=posts)


@app.route('/about')
def about():
    return render_template('home.html', methods=['POST'])


######################################################################################################
# Login | Logout | Register |
######################################################################################################


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('properties'))
    form = LoginForm()
    if form.validate_on_submit():
            # log in with email. Check database to see if email exists
            user = User.query.filter_by(email=form.email.data).first()

            # if user exists, and password matches the hashed password that was created upon registration
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('properties'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('properties'))
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/property_pics', picture_fn)

    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():

    """
        This route is used when a user wants to analyze a new property
        When the form is submitted, the form inputs are passed to variables (eg: title = form['title'])
        We initialize a house object where we pass in variables as parameters to make calculations

        If user is logged in, we insert these variables and calculations to a SQL database
        The user is redirected to a route /analyze/<post.id> that requeries this information and displays it

        Else: user is anonymous so we pass the variables and calculations as a dictionary to the jinja2 webpage
    """
    picture_file = 'default.png'

    form = Analyze_Form()
    if form.is_submitted():

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

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

        price = handle_comma(request.form['price'])
        term = request.form['term']
        down = request.form['down']
        interest = request.form['interest']
        closing = request.form['closing']

        rent = handle_comma(request.form['rent'])
        other = handle_comma(request.form['other'])
        expenses = request.form['expenses']
        vacancy = request.form['vacancy']
        appreciation = request.form['appreciation']
        income_growth = request.form['income_growth']
        expense_growth = request.form['expense_growth']

        if len(title) == 0:
            title = 'Untitled'
        if len(sqft) == 0:
            sqft = '-'
        if len(bed) == 0:
            bed = '-'
        if len(bath) == 0:
            bath = '-'
        if len(year) == 0:
            year = '-'

        # when user is logged in, current_user is authenticated and redirects to /analyze/<post.id>
        # /analyze/<post.id> queries data from the Post table into variable post 
        # THEN renders analyze_output.html while passing in variable post to the .HTML template
        # the .HTML template uses {{ post.title }} to display the database results on the dashboard
        if current_user.is_authenticated:
            user = current_user
            post = Post(title=title,
                        url=url,
                        street=street,
                        image_file=picture_file,
                        city=city,
                        state=state,
                        zipcode=zipcode,

                        type=type,
                        year=year,
                        bed=bed,
                        bath=bath,
                        sqft=sqft,

                        price=price,
                        term=term,
                        down=down,
                        interest=interest,
                        closing=closing,

                        rent=rent,
                        other=other,
                        expenses=expenses,
                        vacancy=vacancy,
                        appreciation=appreciation,
                        income_growth=income_growth,
                        expense_growth=expense_growth,

                        author=user)

            db.session.add(post)
            db.session.commit()
            return redirect(url_for('post', post_id=post.id))

        # below calls current_user.get_id() which returns 'None' when user is NOT logged in
        # redirects to /post_anon route which does not incorporate the <post.id> in route like above
        # /post_anon does NOT query data from the database ... just render templates the dashboard and passes in values

        # if you want to store anon data
        # below calls current_user.get_id() which returns 'None' when user is NOT logged in
        # saves to sqlite with None as usertype
        # redirects to /analyze/anon which doesn't require a post id to view
        else:
            user = current_user.get_id()
            post = Post(title=title,
                        url=url,
                        image_file=picture_file,
                        street=street,
                        city=city,
                        state=state,
                        zipcode=zipcode,

                        type=type,
                        year=year,
                        bed=bed,
                        bath=bath,
                        sqft=sqft,

                        price=price,
                        term=term,
                        down=down,
                        interest=interest,
                        closing=closing,

                        rent=rent,
                        other=other,
                        expenses=expenses,
                        vacancy=vacancy,
                        appreciation=appreciation,
                        income_growth=income_growth,
                        expense_growth=expense_growth,

                        author=user)

            db.session.add(post)
            db.session.commit()
            return redirect(url_for('post_anon', post_id=post.id))

    return render_template('analyze.html', form=form)


@app.route('/analyze/<int:post_id>')
def post(post_id):
    """ The user is redirected to this route after submitting the form on the /analyze/ route
        As recap, the /analyze/ route submission inserts form inputs into a database
        The database automatically assigns a primary key "post id" to the data

        This route queries the database using the post id as SQL's WHERE clause (WHERE post_id = post_id)
        By querying thru post_id, we have access to the variables input on the form and inserted by the /analyze/ route
        We can get price by calling post.price

        We call the Calculate class defined in property_calculations.py and pass form inputs as parameters
        We then call methods of the class to calculate metrics such as down payment, cap rates, etc.

        We take the results of the calculations and insert them into the dictionary {data}
        This route passes the dictionary as a parameter in render_template()
        Now we can access the calculations in the jinja2 template
    """
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    property = Calculate(float(post.price),
                         float(post.down),
                         float(post.interest),
                         float(post.term),
                         float(post.rent),
                         float(post.expenses),
                         float(post.vacancy),
                         float(post.closing),
                         float(post.other)
                         )

    down_payment = property.down_payment()
    mortgage_payment = property.mortgage_payment()
    out_of_pocket = property.outofpocket()
    vacancy_loss = property.vacancy_loss()
    operating_income = property.operating_income()
    operating_expense = property.operating_expense()
    noi = property.noi()
    cash_flow = property.cashflow()
    cap_rate = property.cap_rate()
    coc = property.cashoncash()

    # 30 year appreciation, equity, loan
    model_year, model_appreciation, model_loan, model_equity = property.year30model(float(post.appreciation))

    # 30 year cash flow
    bar_year, bar_rent = property.cash_flow_30_year(post.income_growth, post.expense_growth)

    # cash flow table
    cashflow_data = property.income_statement()


    data = {'model_year': model_year,
            'model_appreciation': model_appreciation,
            'model_loan': model_loan,
            'model_equity': model_equity,
            'bar_year': bar_year,
            'bar_rent': bar_rent,
            'price': comma_dollar(float(post.price)),
            'mortgage': comma_dollar(mortgage_payment),
            'outofpocket': comma_dollar(out_of_pocket),
            'cap_rate': cap_rate,
            'coc': coc,
            'operating_income': comma_dollar(operating_income),
            'operating_expense': comma_dollar(operating_expense),
            'cash_flow': comma_dollar(cash_flow),
            'noi': comma_dollar(noi),
            'vacancy': vacancy_loss,
            'pie_ma': (int(mortgage_payment) * 12),
            'pie_oe': remove_comma_dollar(cashflow_data['annual_operating_expenses']),
            'pie_cf': remove_comma_dollar(cashflow_data['annual_cashflow']),

            }


    # can't view report unless you are the user who created it

    return render_template('analyze_output.html',
                           title=post.title,
                           post=post,
                           cashflow_data=cashflow_data,
                           data=data
                           )


# when user is logged in and authenticated
@app.route('/analyze/<int:post_id>/update', methods=['GET','POST'])
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

        post.price = handle_comma(form.price.data)
        post.term = form.term.data
        post.down = form.down.data
        post.interest = form.interest.data
        post.closing = form.closing.data

        post.rent = handle_comma(form.grossrent.data)
        post.other = handle_comma(form.other.data)
        post.expenses = form.expenses.data
        post.vacancy = form.vacancy.data
        post.appreciation = form.appreciation.data
        post.income_growth = form.income_growth.data
        post.expense_growth = form.expense_growth.data

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
        form.income_growth.data = post.income_growth
        form.expense_growth.data = post.expense_growth

    return render_template('analyze_update.html', form=form)


# /analyze2 redirects to this route when current_user is not authenticated bc user is not logged in
@app.route('/analyze/anon/<int:post_id>')
def post_anon(post_id):

    post = Post.query.get_or_404(post_id)

    property = Calculate(float(post.price),
                         float(post.down),
                         float(post.interest),
                         float(post.term),
                         float(post.rent),
                         float(post.expenses),
                         float(post.vacancy),
                         float(post.closing),
                         float(post.other)
                         )

    down_payment = property.down_payment()
    mortgage_payment = property.mortgage_payment()
    out_of_pocket = property.outofpocket()
    vacancy_loss = property.vacancy_loss()
    operating_income = property.operating_income()
    operating_expense = property.operating_expense()
    noi = property.noi()
    cash_flow = property.cashflow()
    cap_rate = property.cap_rate()
    coc = property.cashoncash()

    # 30 year model
    model_year, model_appreciation, model_loan, model_equity = property.year30model(float(post.appreciation))

    # 30 year cash flow
    bar_year, bar_rent = property.cash_flow_30_year(post.income_growth, post.expense_growth)

    # cash flow table
    cashflow_data = property.income_statement()

    data = {'model_year': model_year,
            'model_appreciation': model_appreciation,
            'model_loan': model_loan,
            'model_equity': model_equity,
            'bar_year': bar_year,
            'bar_rent': bar_rent,
            'price': comma_dollar(float(post.price)),
            'mortgage': comma_dollar(mortgage_payment),
            'outofpocket': comma_dollar(out_of_pocket),
            'cap_rate': cap_rate,
            'coc': coc,
            'operating_income': comma_dollar(operating_income),
            'operating_expense': comma_dollar(operating_expense),
            'cash_flow': comma_dollar(cash_flow),
            'noi': comma_dollar(noi),
            'vacancy': vacancy_loss,
            'pie_ma': (int(mortgage_payment) * 12),
            'pie_oe': remove_comma_dollar(cashflow_data['annual_operating_expenses']),
            'pie_cf': remove_comma_dollar(cashflow_data['annual_cashflow']),
            }

    return render_template('analyze_output.html',
                           title=post.title,
                           post=post,
                           cashflow_data=cashflow_data,
                           data=data)


@app.route('/analyze/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        if post.author is None:
            db.session.delete(post)
            db.session.commit()
            flash('Your post has been deleted!', 'success')
            return redirect(url_for('analyze'))
        else:
            abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')

    return redirect(url_for('properties'))


######################################################################################################
# Calculator
######################################################################################################


@app.route('/calculator')
def calculator():
    return render_template('calculator.html')


@app.route('/process', methods=['POST'])
def process():
    input_price = handle_comma(request.form['price'])
    input_down_payment = request.form['down_payment']
    input_term = request.form['term']
    input_interest_rate = request.form['interest_rate']
    input_property_tax = request.form['property_tax']
    input_insurance = request.form['insurance']

    calc = Calculate(input_price, input_down_payment, input_interest_rate, input_term, 0, 0, 0, 0, 0)
    down_payment = calc.down_payment()
    mortgage_payment = calc.mortgage_payment()

    # Returns floats as a string with dollar sign and comma separators
    down_payment_clean = comma_dollar(down_payment)
    mortgage_payment_clean = comma_dollar(mortgage_payment)

    labels = ['Mortgage', 'Taxes' , 'Insurance']
    number = [int(mortgage_payment), int(input_property_tax), int(input_insurance)]
    total = int(mortgage_payment) + int(input_property_tax) + int(input_insurance)

    return jsonify({'mortgage_payment': mortgage_payment_clean,
                    'down_payment': down_payment_clean,
                    'number': number,
                    'labels': labels,
                    'total': total
                })

######################################################################################################
######################################################################################################
######################################################################################################
# Not in use
######################################################################################################
######################################################################################################
######################################################################################################

#
# @app.route("/analyze2", methods=['GET','POST'])
# def analyze2():
#     form = Analyze_Form()
#     return render_template('analyze_update.html', form=form)
#
#
# @app.route("/handle_analyze", methods=['POST'])
# def handle_analyze():
#     if request.method == 'POST':
#         title = request.form['title']
#         street = request.form['street']
#         city = request.form['city']
#         state = request.form['state']
#         zipcode = request.form['zipcode']
#
#         type = request.form['type']
#         year = request.form['year']
#         bed = request.form['bed']
#         bath = request.form['bath']
#         sqft = request.form['sqft']
#
#         price = request.form['price']
#         term = request.form['term']
#         down = request.form['down']
#         interest = request.form['interest']
#         closing = request.form['closing']
#
#         rent = request.form['rent']
#         other = request.form['other']
#         expenses = request.form['expenses']
#         vacancy = request.form['vacancy']
#
#         appreciation = request.form['appreciation']
#         income_growth = request.form['income_growth']
#         expense_growth = request.form['expense_growth']
#
#         house = Calculations(price, down, interest, term, rent, expenses, vacancy)
#
#         cashflow_data = house.income_statement(10)
#
#         monthly_income = comma_dollar(rent)
#         monthly_expense = comma_dollar(house.monthly_expenses())
#         mortgage_payment = house.mortgage_calc()
#         down_payment = house.downpayment_calc()
#         oop = house.outofpocket(closing)
#         oi = house.operating_income()
#         monthly_noi = house.noi(oi)
#         cap_rate = house.cap_rate()
#
#         cash_flow = house.cashflow(monthly_noi, mortgage_payment)
#         coc = house.cashoncash(cash_flow, oop)
#
#         clean_oi = comma_dollar(oi)
#         clean_down_payment = comma_dollar(down_payment)
#         clean_price = comma_dollar(price.replace(',',''))
#         clean_mortgage_payment = comma_dollar(mortgage_payment)
#         clean_outofpocket = comma_dollar(oop)
#         clean_cash_flow = comma_dollar(cash_flow)
#
#         # graph
#         model_year, model_appreciation, model_loan, model_equity = house.year30model(appreciation, 2)
#         data = {'model_year':model_year,
#                 'model_appreciation': model_appreciation,
#                 'model_loan': model_loan,
#                 'model_equity': model_equity,
#                 'pie_mortgage': mortgage_payment,
#                 'pie_expense': house.monthly_expenses(),
#                 'pie_cashflow': cash_flow,
#                 'grossrent': comma_dollar(int(rent)),
#                 'operating_income': clean_oi,
#                 'operating_expenses': comma_dollar(int(rent) * (1-(int(expenses)/100))),
#                 'loan_payment': clean_mortgage_payment,
#                 'cashflow': clean_cash_flow
#                 }
#
#     return render_template('analyze_output.html', title=title, street=street, city=city, state=state, zipcode=zipcode,
#                                                   price=clean_price, type=type, year=year, bed=bed, bath=bath,
#                                                   sqft=sqft,
#                                                   mortgage_payment=clean_mortgage_payment,
#                                                   cap_rate=cap_rate,
#                                                   operating_income=clean_oi, expenses=expenses,
#                                                   monthly_income=monthly_income, monthly_expense=monthly_expense,
#                                                   down_payment=clean_down_payment,
#                                                   outofpocket=clean_outofpocket,
#                                                   cashflow=clean_cash_flow,
#                                                   cashoncash=coc,
#                                                   data=data, cashflow_data=cashflow_data)
#
