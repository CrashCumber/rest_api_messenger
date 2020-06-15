import datetime
from functools import reduce

from flask import request, render_template, redirect, make_response
from jinja2 import Template

from app import app, db
from app.forms import *

from app.models import User, Chat, Message


@app.route('/chats/<id>', methods=["POST", "GET"])
def chats(id: int):
    user = User.query.get(id)
    chats = user.chats
    return render_template('chats.html', chats=chats, title="chats", user_id=id)


@app.route('/chat/<user_id>/<id>', methods=["POST", "GET"])
def chat(user_id: int, id: int):
    chat = Chat.query.get(id)
    form = SendMessageForm(request.form)
    if request.method == 'POST':
        data = form.content.data
        sender = User.query.get(1)
        mes = Message(content=data, chat_id=id, sender_id=sender.id)
        chat.last_message = data
        chat.last_message_time = datetime.datetime.now()
        db.session.add(mes, chat)
        db.session.commit()
    chat_mess = Message.query.filter(Message.chat_id == id).all()
    return render_template('chat.html', form=form, title=chat.title, messages=chat_mess, user_id=user_id)


@app.route('/create_chat/<id>', methods=["POST", "GET"])
def create_chat(id: int):
    form = ChatForm(request.form)
    if request.method == 'POST':
        data = form.tittle_chat.data
        chat_ = Chat(title=data)

        db.session.add(chat_)
        db.session.commit()

        user = User.query.get(id)
        user.chats.append(chat_)
        db.session.commit()

        return redirect(f'/chat/{id}/{chat_.id}')
    else:
        return render_template('create_chat.html', form=form, title="create_chat")


@app.route('/create_user', methods=["POST", "GET"])
def create_user():
    form = RegForm(request.form)
    if request.method == 'POST':
        data = {"name": form.name.data, "email": form.email.data, "password": form.password.data}
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return redirect(f'/chats/{user.id}')
    else:
        return render_template('create_user.html', form=form, title="registration")


@app.route('/login', methods=["POST", "GET"])
def login_user():
    form = LogForm(request.form)
    if request.method == 'POST':
        data = form.name.data
        user = User.query.get(data)
        return redirect(f'/chats/{user.id}')
    else:
        return render_template('login.html', form=form, title="login")
