from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, validators, BooleanField, PasswordField


class RegForm(FlaskForm):
    name = StringField([validators.Length(min=4, max=25), validators.DataRequired()])
    email = StringField([validators.Email(), validators.DataRequired()])
    password = PasswordField([validators.DataRequired()])


class LoginForm(FlaskForm):
    name = StringField([validators.Length(min=4, max=25), validators.InputRequired()])
    password = PasswordField([validators. InputRequired()])


class ChatForm(FlaskForm):
    tittle_chat = StringField([validators.InputRequired()])


class SendMessageForm(FlaskForm):
    content = TextAreaField('Message')

