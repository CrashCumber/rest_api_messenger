import datetime
from flask import request, render_template, redirect, make_response, session, abort
from sqlalchemy import or_

from app import app, db
from app.auth_views import is_auth
from app.forms import *
from app.models import User, Chat, Message


@app.route('/profile', methods=["PUT"])
@is_auth
def put_user():
    user_id = request.cookies.get('user_id')
    user = User.query.get(user_id)

    search_name = request.args.get('username')
    search_user = User.query.filter(name=search_name)

    if search_user == user:
        data = request.get_json()
        user.name = data["name"]
        user.email = data["email"]
        data = {
            "name": user.name,
            "email": user.email
        }

        db.session.add(user)
        db.session.commit(user)

    response = make_response({"data": data}, 200)

    return response


@app.route('/profile', methods=["GET"])
@is_auth
def get_user():
    search_name = request.args.get('username')
    search_user = User.query.filter(name=search_name)

    data = {
            "name": search_user.name,
            "email": search_user.email
            }

    response = make_response({"data": data}, 200)
    return response


@app.route('/profile', methods=["POST"])
@is_auth
def post_user():
    user_id = request.cookies.get('user_id')
    sender = User.query.get(user_id)

    search_name = request.args.get('username')
    search_user = User.query.filter(name=search_name)

    chat = Chat.query.filter(title=f"{search_name},{sender.name}").first() | Chat.query.filter(title=f"{sender.name},{search_name}").first()

    if chat == None:
        chat_ = Chat(title=f"{search_name},{sender.name}")
        db.session.add(chat_)
        db.session.commit()

        sender.chats.append(chat_)
        search_user.chats.append(chat_)

        db.session.commit(search_user, sender)
        db.session.commit()

    response = make_response('', 200)
    response.headers["Location"] = f"http://127.0.0.1:5000/chats/{chat_.id}"

    return response

