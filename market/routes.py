from market import app
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from market import db

from flask_login import login_user, logout_user, login_required
from flask import redirect, render_template, url_for, flash



@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/market')
@login_required
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)


@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_create = User(username = form.username.data,
                        email_adress = form.email_adress.data,
                        password = form.password.data)
        db.session.add(user_create)
        db.session.commit()
        login_user(user_create)
        flash(f'Account created successfully! You are now logged in as {user_create.username.capitalize()}', category='success')

        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validators
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_adress=form.email.data).first()
        if attempted_user and attempted_user.verify_password(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Succes! You are logged in as: {attempted_user.username}', category='success') 
            return redirect(url_for('market_page'))
        else:
            flash('Invalid mail or incorrect password', category='danger')    
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('index'))

