from flask import render_template, request, redirect, url_for, abort, flash
from flask_login import current_user
from realtoranalysis import db
from .forms import AnalyzeForm
from realtoranalysis.models import User, Post
from realtoranalysis.scripts.property_calculations import Calculate, comma_dollar, handle_comma, remove_comma_dollar
from . import analyzer
from .functions import get_kwargs, get_data

######################################################################################################
# Analyze
######################################################################################################


@analyzer.route('/', methods=['GET', 'POST'])
def analyze():

    """
    Renders a template containing the form for the user to input property details and assumptions.
    Form values are posted to the database and user is redirected to the report page on submit.
    """

    form = AnalyzeForm()

    if form.is_submitted():

        kwargs = get_kwargs(request.form)
        user = current_user

        if not current_user.is_authenticated:
            user = current_user.get_id()

        post = Post(**kwargs,
                    author=user)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('analyzer.post', post_id=post.id))

    return render_template('analyze.html', form=form)


@analyzer.route('/<int:post_id>', methods=['POST', 'GET'])
def post(post_id):
    """
    The user is redirected to this route after submitting the form on the /analyze/ route
    As recap, the /analyze/ route submission inserts form inputs and calculations into a database
    The database automatically assigns a primary key "post_id" to the row data

    This route queries the database using the post id as the SQL WHERE operator (WHERE post_id = post_id)
    We now have access to the variables input on the analyze form and inserted by the /analyze/ route
    For example, we can get price by calling post.price

    If there is an account associate with the account, we verify the user created the report.
    Otherwise, it is a viewable public report
    The return statement passes query results and the dictionary as a parameter in render_template()
    Now we can access the query results and calculations in the jinja2 template
    """

    post = Post.query.get_or_404(post_id)

    if post.author and post.author != current_user:
        abort(403)

    data, cashflow_data = get_data(post)

    return render_template('analyze_output.html',
                           title=post.title,
                           post=post,
                           cashflow_data=cashflow_data,
                           data=data
                           )


######################################################################################################
# Edit | Share | Delete |
######################################################################################################


@analyzer.route('/<int:post_id>/update', methods=['GET', 'POST'])
def update_post(post_id):
    """
    This route renders the analyze_update.html template and allows a user to update the form inputs.

    This update template differs in that the form preloads query results as values
        Using a GET request:
            On load, it first queries the database for information associated with the post_id
            It sets the form inputs as the variables we query from the database

        When we POST this form,
            We insert the form inputs back into the database
            Since when we load the update page, the original information is prefilled into the form,
                Only changes we make will be change data inserted into the database
    """
    post = Post.query.get_or_404(post_id)

    # Raise Forbidden error if current user did not create the report
    if post.author != current_user:
        abort(403)

    form = AnalyzeForm()

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
        return redirect(url_for('analyzer.post', post_id=post.id))

    # This block will pre-fill the form with database values
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


@analyzer.route('/<int:post_id>/<share>')
def shared_post(post_id, share):
    """
    This route allows a user to share a report.
    Registered reports are private, with access only being granted if the current_user is authenticated.

    However, in the /analyze/ route, we generated a string of random characters and inserted it into the database.

    This route will first query the data using <int:post_id>.
    Then it will check the <share> string in the uRL against the share string in the database

    If the share string in the url is equal to the share string in the database, the report will be generated
    """
    post = Post.query.get_or_404(post_id)

    if share == post.share:
        data, cashflow_data = get_data(post)
        return render_template('analyze_output.html',
                               title=post.title,
                               post=post,
                               cashflow_data=cashflow_data,
                               data=data
                               )
    else:
        return redirect(url_for('analyzer.analyze'))


@analyzer.route('/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')

    return redirect(url_for('properties'))

