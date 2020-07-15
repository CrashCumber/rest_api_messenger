from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, validators, BooleanField, PasswordField


class RegForm(FlaskForm):
    name = StringField('name', [validators.Length(min=4, max=25), validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired(), validators.Length(min=6, max=50)])
    email = StringField('email', [validators.Email(), validators.DataRequired()])


class LoginForm(FlaskForm):
    name = StringField('name', [validators.DataRequired()])
    password = PasswordField('password',  [validators.DataRequired()])


class ChatForm(FlaskForm):
    title = StringField('title', [validators.DataRequired()])


class MessageForm(FlaskForm):
    content = TextAreaField('content', [validators.DataRequired()])


class UserForm(FlaskForm):
    name = StringField('name', [validators.Length(min=4, max=25), validators.DataRequired()])
    email = StringField('email', [validators.Email(), validators.DataRequired()])
