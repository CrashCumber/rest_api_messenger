import datetime
from functools import wraps
from flask import request, render_template, redirect, make_response, session, abort
import random
from app import app, db
from app.forms import *

from app.models import User, Chat, Message


def is_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        user_id = request.headers["Cookies"].split('=')[-1]
        user = User.query.get(user_id)
        token = user.token

        if token == request.headers["X-CSRF-Token"]:
            return func(*args, **kwargs)

        abort(401)
    return wrapper


@app.route('/token', methods=["GET"])
def get_token():
    chars = 'QWERTYUIOP[]ASDFGHJKLZXCVBNMZqwertyup[asdfghjkl;zxcvbnm,,../1234567890-='
    token = ''

    for i in range(random.randint(30, 60)):
        token += random.choice(chars)

    response = make_response(' ')
    response.headers["X-CSRF-Token"] = token

    return response


@app.route('/registration', methods=["POST"])
def post_registration():
    form = RegForm()

    try:
        assert request.content_type != 'application/x-www-form-urlencoded'

        token = request.headers["X-CSRF-Token"]
        data = {"name": form.name.data, "email": form.email.data, "password": form.password.data}

        if not User.query.filter(User.name == data["name"]).first():
            user = User(**data)
            user.token = token

            db.session.add(user)
            db.session.commit()

            response = make_response('', 201)
            response.headers["Location"] = "http://127.0.0.1:5000/chats"
            response.headers["X-CSRF-Token"] = token
            response.headers["Cookies"] = f"user_id={user.id}"

            return response

        error_msg = 'User already exist'
        response = make_response(error_msg)
        return response
    except:
        abort(400)


@app.route('/login', methods=["POST"])
def post_login():
    form = LoginForm()
    try:
        assert request.content_type != 'application/x-www-form-urlencoded'
        token = request.headers["X-CSRF-Token"]

        username = form.name.data
        password = form.password.data
        user = User.query.filter(User.name == username).filter(User.password == password).first()

        if user:
            data = {'access_token': token, 'user_id': user.id}
            response = make_response(data)

            response.headers["Location"] = "http://127.0.0.1:5000/chats"
            response.headers["Cookies"] = f"user_id={user.id}"
            response.headers["X-CSRF-Token"] = token
            user.token = token

            db.session.add(user)
            db.session.commit()

            return response

        error_msg = 'Wrong password or username'
        response = make_response(error_msg)
        response.headers["X-CSRF-Token"] = token

        return response
    except:
        abort(400)


@app.route('/chats', methods=["GET"])
@is_auth
def get_chats():
    user_id = request.headers["Cookies"].split('=')[-1]
    user = User.query.get(user_id)
    body = []

    for chat in user.chats:
        data = {"id": chat.id,
                "title": chat.title,
                "last_message": chat.last_message,
                "last_message_time": chat.last_message_time,
                "sender_id": chat.sender_id
                }
        body.append(data)

    response = make_response({"chats": body})
    response.headers["X-CSRF-Token"] = user.token

    return response


@app.route('/logout')
@is_auth
def logout():
    user_id = request.headers["Cookies"].split('=')[-1]
    user = User.query.get(user_id)

    user.token = None

    response = make_response('')
    response.headers["Location"] = "http://127.0.0.1:5000/login"

    return response


@app.route('/')
@is_auth
def home():
    return 'Home'


@app.route('/create_chat', methods=["POST"])
@is_auth
def post_chat():
    try:
        form = ChatForm()

        data = form.tittle_chat.data
        chat_ = Chat(title=data)

        db.session.add(chat_)
        db.session.commit()

        user_id = request.headers["Cookies"].split('=')[-1]
        user = User.query.get(user_id)
        user.chats.append(chat_)
        db.session.commit()

        response = make_response('', 302)
        response.headers["Location"] = f"http://127.0.0.1:5000/chat/{chat_.id}"
        response.headers["X-CSRF-Token"] = user.token

        return response
    except:
        abort(403)


@app.route('/chat/<chat_id>', methods=["POST", "GET"])
@is_auth
def chat(chat_id: int):
    try:
        user_id = request.headers["Cookies"].split('=')[-1]
        user = User.query.get(user_id)

        if request.method == 'GET':
            chat_messages = Message.query.filter(Message.chat_id == chat_id).all()
            body = []
            for mes in chat_messages:
                data = {"id": mes.id,
                        "content": mes.content,
                        "sender_id": mes.sender_id,
                        "time": mes.time
                        }
                body.append(data)

            response = make_response({"messages": body})
            response.headers["X-CSRF-Token"] = user.token

            return response

        if request.method == "POST":
            form = SendMessageForm()

            sender = User.query.get(user_id)
            data = form.content.data

            message = Message(content=data, chat_id=chat_id, sender_id=sender.id)

            chat = Chat.query.get(chat_id)
            chat.last_message = data
            chat.last_message_time = datetime.datetime.now()

            db.session.add(message, chat)
            db.session.commit()
    except:
        abort(403)




