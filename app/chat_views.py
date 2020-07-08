import datetime
from flask import request, render_template, redirect, make_response, session, abort
from app import app, db
from app.auth_views import is_auth
from app.forms import *
from app.models import User, Chat, Message


@app.route('/chats', methods=["GET"])
@is_auth
def get_chats():
    user_id = request.cookies.get('user_id')
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
        chat_ = Chat.query.filter(title=data).all()

        if chat_ == None:
            chat_ = Chat(title=data)

            db.session.add(chat_)
            db.session.commit()

            user_id = request.cookies.get('user_id')
            user = User.query.get(user_id)
            user.chats.append(chat_)
            db.session.commit()

            response = make_response('', 200)
            response.headers["Location"] = f"http://127.0.0.1:5000/chats/{chat_.id}"

            return response
        abort(400)
    except:
        abort(403)


@app.route('/chats/<chat_id>', methods=["GET"])
@is_auth
def get_chat(chat_id: int):
    try:
        user_id = request.cookies.get('user_id')
        user = User.query.get(user_id)

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
    except :
        abort(403)


@app.route('/chats/<chat_id>', methods=["POST"])
@is_auth
def post_message(chat_id: int):
    try:
        user_id = request.cookies.get('user_id')
        user = User.query.get(user_id)

        form = SendMessageForm()

        sender = User.query.get(user_id)
        data = form.content.data

        message = Message(content=data, chat_id=chat_id, sender_id=sender.id)

        chat = Chat.query.get(chat_id)
        chat.last_message = data
        chat.last_message_time = datetime.datetime.now()

        db.session.add(message, chat)
        db.session.commit()

        response = make_response('',200)
        return response
    except:
        abort(403)




