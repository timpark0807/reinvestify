import secrets
from flask import render_template, jsonify, request, redirect, url_for, flash, abort
from flask_login import login_user, current_user, logout_user, login_required
from realtoranalysis import application, db, bcrypt
from realtoranalysis.forms import Analyze_Form, LoginForm, RegistrationForm
from realtoranalysis.models import User, Post
from realtoranalysis.scripts.property_calculations import Calculate, comma_dollar, handle_comma, remove_comma_dollar


######################################################################################################
# Error Handling
######################################################################################################


@application.errorhandler(400)
def handle_bad_request():
    return render_template('400.html'), 400


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@application.errorhandler(500)
def internal_error():
    return render_template('500.html'), 500


@application.errorhandler(403)
def application_forbidden():
    return render_template('403.html'), 403


######################################################################################################
# Login | Logout | Register |
######################################################################################################


@application.route('/login', methods=['GET', 'POST'])
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
                return redirect(url_for('analyzer.analyze'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@application.route('/logout')
def logout():
    logout_user()
    flash(f'You have been logged out.', 'success')
    return redirect(url_for('login'))


@application.route('/register', methods=['GET', 'POST'])
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
# Sidebar Nav
######################################################################################################


@application.route('/')
@application.route('/home')
def home():
    return redirect(url_for('analyzer.analyze'))


@application.route('/account')
@login_required
def account():
    return render_template('account.html')


@application.route('/properties/')
def properties():
    if current_user.is_authenticated:
        user = current_user.id

        posts = Post.query.filter_by(user_id=user).all()

        if posts == []:
            return render_template('no_properties.html')

        return render_template('my_properties.html', posts=posts)
    else:
        return render_template('login_properties.html')


@application.route('/about/')
def about():
    return render_template('home.html', methods=['POST'])

