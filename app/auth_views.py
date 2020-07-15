from flask import request, make_response, abort
import random
from app import app, db, URL
from app.forms import LoginForm, RegForm
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

    for i in range(random.randint(30, 100)):
        token += random.choice(chars)

    return token


@app.route('/api/login', methods=["POST"])
def post_login():
    form = LoginForm(csrf_enabled=False)

    if request.content_type != 'application/x-www-form-urlencoded':
        error_msg = 'Invalid content type'
        response = make_response({"error": error_msg}, 400)
        return response

    if not form.validate_on_submit():
        error_msg = 'Invalid form data'
        response = make_response({"error": error_msg}, 400)
        return response

    username = form.name.data
    password = form.password.data
    user = User.query.filter(User.name == username).first()

    if user is not None and user.check_password(password):
        user.token = get_token()
        db.session.add(user)
        db.session.commit()

        response = make_response({"status": "ok"}, 200)
        response.headers["Location"] = URL + "/api/chats"
        response.set_cookie('user_id', str(user.id))
        response.set_cookie('access_token', user.token)

        return response

    error_msg = 'Wrong password or username'
    response = make_response({"error": error_msg}, 400)
    return response


@app.route('/api/logout', methods=["GET"])
@is_auth
def logout():
    user_id = request.cookies.get('user_id', False)
    user = User.query.get(user_id)

    user.token = None

    response = make_response({"status": "ok"}, 200)
    response.headers["Location"] = URL + "/api/login"
    response.set_cookie('access_token', ' ', max_age=0)
    response.set_cookie('user_id', ' ', max_age=0)
    return response

