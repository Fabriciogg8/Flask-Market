from market import app
from market.models import Item, User
from market.forms import RegisterForm
from market import db

from flask import redirect, render_template, url_for, flash


@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)


@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_create = User(username = form.username.data,
                        email_adress = form.email_adress.data,
                        password_hash = form.password.data)
        db.session.add(user_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validators
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user {err_msg}', category='danger')
    return render_template('register.html', form=form)

