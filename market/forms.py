from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class RegisterForm(FlaskForm):
    username = StringField(label='User name: ')
    email_adress = StringField(label='Email adress: ')
    password = PasswordField(label='Password: ')
    confirm_password = PasswordField(label='Confirm password: ')
    submit = SubmitField(label='Create Account')