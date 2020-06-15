from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, validators, BooleanField, PasswordField


class RegForm(FlaskForm):
    name = StringField('Username', [validators.Length(min=4, max=25), validators.DataRequired()])
    email = StringField('Email', validators=[validators.Email()])
    password = PasswordField('New Password', [validators.DataRequired()])

class LogForm(FlaskForm):
    name = StringField('Username', [validators.Length(min=4, max=25), validators.DataRequired()])

class ChatForm(FlaskForm):
    tittle_chat = StringField('Title')


class SendMessageForm(FlaskForm):
    content = TextAreaField('Message')
