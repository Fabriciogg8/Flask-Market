import email
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class RegisterForm(FlaskForm):
    username = StringField(label='username')
    email_adress = StringField(label='email')
    password = PasswordField(label='password')
    confirm_password = PasswordField(label='confirm_password')
    submit = SubmitField(label='submit')