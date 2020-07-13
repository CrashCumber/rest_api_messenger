from flask import request, render_template, redirect, make_response, session, abort
import random
from app import app, db
from app.forms import *
from app.models import User
from functools import wraps


def is_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = request.cookies.get('user_id')
        user = User.query.get(user_id)

        if user_id is not None and user is not None:
            token = user.token

            if token == request.cookies.get('access_token'):
                return func(*args, **kwargs)

        abort(401)
    return wrapper


def get_token():
    chars = 'QWERTYUIOP[]ASDFGHJKLZXCVBNMZqwertyup[asdfghjklzxcvbnm.1234567890-='
    token = ''

    for i in range(random.randint(30, 60)):
        token += random.choice(chars)

    return token


@app.route('/registration', methods=["POST"])
def post_registration():
    form = RegForm(csrf_enabled=False)
    try:
        assert request.content_type == 'application/x-www-form-urlencoded'

        assert form.validate_on_submit()

        data = {"name": form.name.data, "email": form.email.data, "password": form.password.data}

        if User.query.filter(User.name == data["name"]).first() is None:
            user = User(**data)
            user.token = get_token()

            db.session.add(user)
            db.session.commit()

            response = make_response({"user_id": str(user.id)}, 201)
            response.headers["Location"] = "http://127.0.0.1:5000/chats"
            response.set_cookie('user_id', str(user.id))
            response.set_cookie('access_token', user.token)

            return response

        error_msg = 'User already exist'
        response = make_response(error_msg, 400)
        return response

    except AssertionError:
        error_msg = 'Invalid request data'
        response = make_response({"error": error_msg}, 400)
        return response


@app.route('/login', methods=["POST"])
def post_login():
    form = LoginForm(csrf_enabled=False)
    try:
        assert request.content_type == 'application/x-www-form-urlencoded'

        assert form.validate_on_submit()

        username = form.name.data
        password = form.password.data
        user = User.query.filter(User.name == username).filter(User.password == password).first()

        if user is not None:
            user.token = get_token()
            db.session.add(user)
            db.session.commit()

            response = make_response({"user_id": str(user.id)}, 200)
            response.headers["Location"] = "http://127.0.0.1:5000/chats"
            response.set_cookie('user_id', str(user.id))
            response.set_cookie('access_token', user.token)

            return response

        error_msg = 'Wrong password or username'
        response = make_response({"error": error_msg}, 400)
        return response

    except AssertionError:
        error_msg = 'Invalid request data'
        response = make_response({"error": error_msg}, 400)
        return response


@app.route('/logout')
@is_auth
def logout():
    user_id = request.cookies.get('user_id', False)
    user = User.query.get(user_id)

    user.token = None

    response = make_response({"status": "ok"}, 200)
    response.headers["Location"] = "http://127.0.0.1:5000/login"
    response.set_cookie('access_token', ' ', max_age=0)
    response.set_cookie('user_id', ' ', max_age=0)

    return response

