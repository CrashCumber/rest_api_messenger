import datetime
from functools import wraps
from flask import request, render_template, redirect, make_response, session
from jinja2 import Template

from app import app, db
from app.forms import *

from app.models import User, Chat, Message


def is_auth(func):
    @wraps(func)
    def wrapper():
        if not session.get('is_auth', False):
            return redirect('/login')

        return func()
    return wrapper


@app.route('/registration', methods=["POST", "GET"])
def registration():
    form = RegForm()
    error_msg = False

    if form.validate_on_submit():

        data = {"name": form.name.data, "email": form.email.data, "password": form.password.data}

        if not User.query.filter(User.name == data["name"]).first():
            user = User(**data)

            db.session.add(user)
            db.session.commit()

            session["is_auth"] = True
            session["username"] = data["name"]
            session["user_id"] = user.id

            return redirect(f'/chats')
        error_msg = 'User already exist'

    return render_template('create_user.html', form=form, title="registration", error_msg=error_msg)


@app.route('/login', methods=["POST", "GET"])
def login():
    if session.get("is_auth"):
        return redirect("/")

    form = LoginForm()
    error_msg = False

    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data

        user = User.query.filter(User.name == username and User.password == password).first()

        if user:
            session["is_auth"] = True
            session["username"] = username
            session["user_id"] = user.id
            return redirect(f'/chats')
        else:
            error_msg = 'Wrong password or username'

    return render_template('login.html', form=form, title="login", error_msg=error_msg)


@app.route('/logout')
def logout():
    session["is_auth"] = False
    session.pop("username")
    session.pop("user_id")

    return redirect(f'/login')


@app.route('/')
@is_auth
def home():
    return 'Home'


@app.route('/chats', methods=["POST", "GET"])
@is_auth
def chats():
    user = User.query.get(session["user_id"])

    return render_template('chats.html', chats=user.chats, title="chats")


@app.route('/create_chat', methods=["POST", "GET"])
@is_auth
def create_chat():
    form = ChatForm()
    error_msg = False

    if form.validate_on_submit():

        data = form.tittle_chat.data
        chat_ = Chat(title=data)

        db.session.add(chat_)
        db.session.commit()

        user = User.query.get(session["user_id"])
        user.chats.append(chat_)
        db.session.commit()

        return redirect(f'/chat/{chat_.id}')

    return render_template('create_chat.html', form=form, title="create_chat", error_msg=error_msg)


@app.route('/chat/<chat_id>', methods=["POST", "GET"])
@is_auth
def chat(chat_id: int):
    chat = Chat.query.get(chat_id)

    form = SendMessageForm()
    sender = User.query.get(session["user_id"])

    if form.validate_on_submit():

        data = form.content.data

        message = Message(content=data, chat_id=chat_id, sender_id=sender.id)
        chat.last_message = data
        chat.last_message_time = datetime.datetime.now()

        db.session.add(message, chat)
        db.session.commit()

    chat_messages = Message.query.filter(Message.chat_id == chat_id).all()

    return render_template('chat.html', form=form, title=chat.title, messages=chat_messages)


