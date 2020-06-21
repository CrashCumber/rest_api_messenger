import datetime
from functools import wraps
from flask import request, render_template, redirect, make_response, session, abort
from jinja2 import Template

from app import app, db
from app.forms import *

from app.models import User, Chat, Message


def is_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('is_auth', False):
            return redirect('/login')

        return func(*args, **kwargs)
    return wrapper


@app.route('/registration', methods=["POST", "GET"])
def registration():
    form = RegForm()

    token = str(form.csrf_token).split(' ')
    token = token[-1]
    token = token[7:len(token) - 2]

    if request.method == 'GET':
        session["csrf_token"] = token
        response = make_response(' ')
        response.headers["X-CSRF-Token"] = token
        return response

    if request.content_type != 'application/x-www-form-urlencoded':
        abort(400)

    error_msg = False

    if form.csrf_token.data == token:

        if form.validate_on_submit():

            data = {"name": form.name.data, "email": form.email.data, "password": form.password.data}

            if not User.query.filter(User.name == data["name"]).first():
                user = User(**data)

                db.session.add(user)
                db.session.commit()

                session["is_auth"] = True
                session["username"] = data["name"]
                session["user_id"] = user.id

                response = make_response('', 302)
                response.headers["Location"] = "http://127.0.0.1:5000/chats"
                response.headers["X-CSRF-Token"] = session["csrf_token"]

                return response

            error_msg = 'User already exist'
            response = make_response(error_msg)
            return response

    abort(500)


@app.route('/login', methods=["POST", "GET"])
def login():
    if session.get("is_auth"):
        return redirect("/")

    form = LoginForm()

    token = str(form.csrf_token).split(' ')
    token = token[-1]
    token = token[7:len(token)-2]

    if request.method == 'GET':
        session["csrf_token"] = token
        response = make_response(' ')
        response.headers["X-CSRF-Token"] = token
        return response

    if request.content_type != 'application/x-www-form-urlencoded':
        abort(400)

    error_msg = False
    form.csrf_token.data = token

    if form.csrf_token.data == token:

        if form.validate_on_submit():
            username = form.name.data
            password = form.password.data

            user = User.query.filter(User.name == username).filter(User.password == password).first()

            if user:
                session["is_auth"] = True
                session["username"] = username
                session["user_id"] = user.id

                response = make_response('', 302)
                response.headers["Location"] = "http://127.0.0.1:5000/chats"
                response.headers["X-CSRF-Token"] = session["csrf_token"]

                return response
            else:
                error_msg = 'Wrong password or username'
                response = make_response(error_msg)

                return response
    abort(500)
    # return render_template('login.html', form=form, title="login", error_msg=error_msg)


@app.route('/logout')
def logout():
    session["is_auth"] = False
    session.pop("username")
    session.pop("user_id")
    session.pop("csrf_token")

    response = make_response('', 302)
    response.headers["Location"] = "http://127.0.0.1:5000/login"

    return response


@app.route('/')
@is_auth
def home():
    return 'Home'


@app.route('/chats', methods=["GET"])
@is_auth
def chats():
    if request.headers["X-CSRF-Token"] == session["csrf_token"]:
        user = User.query.get(session["user_id"])
        body = []

        for chat in user.chats:
            data = {"id": chat.id,
                    "title": chat.title,
                    "last_message": chat.last_message,
                    "last_message_time": chat.last_message_time,
                    "sender_id": chat.sender_id
                    }
            body.append(data)

        response = make_response({"chats":body})
        return response

    abort(403)


@app.route('/create_chat', methods=["POST", "GET"])
@is_auth
def create_chat():
    if request.headers["X-CSRF-Token"] == session["csrf_token"]:
        form = ChatForm()
        error_msg = False

        if request.method == 'POST':

            data = form.tittle_chat.data
            chat_ = Chat(title=data)

            db.session.add(chat_)
            db.session.commit()

            user = User.query.get(session["user_id"])
            user.chats.append(chat_)
            db.session.commit()

            response = make_response('', 302)
            response.headers["Location"] = f"http://127.0.0.1:5000/chat/{chat_.id}"

            return response

    abort(403)


@app.route('/chat/<chat_id>', methods=["POST", "GET"])
@is_auth
def chat(chat_id: int):
    if request.headers["X-CSRF-Token"] == session["csrf_token"]:

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
            return response

        if request.method == "POST":

            form = SendMessageForm()

            sender = User.query.get(session["user_id"])
            data = form.content.data

            message = Message(content=data, chat_id=chat_id, sender_id=sender.id)

            chat = Chat.query.get(chat_id)
            chat.last_message = data
            chat.last_message_time = datetime.datetime.now()

            db.session.add(message, chat)
            db.session.commit()
    abort(403)




