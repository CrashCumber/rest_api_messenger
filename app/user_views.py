from flask import request, make_response, abort
from app import app, db
from app.auth_views import is_auth, get_token
from app.models import User
from app.forms import UserForm, RegForm


@app.route('/api/user', methods=["GET"])
@is_auth
def get_user():
    """
    Get user by param "name" in url
    """
    search_name = request.args.get('name')

    if search_name is None:
        error_msg = 'User nonexist'
        response = make_response({"error": error_msg}, 404)
        return response

    search_user = User.query.filter(User.name == search_name).first()

    data = {
        "name": search_user.name,
        "email": search_user.email
    }

    response = make_response({"user": data}, 200)
    return response


@app.route('/api/user', methods=["PUT"])
@is_auth
def put_user():
    """
    User is modified
    """
    form = UserForm()

    user_id = request.cookies.get('user_id')
    user = User.query.get(user_id)

    search_name = request.args.get('name')
    search_user = User.query.filter(User.name == search_name).first()

    if search_user is None:
        error_msg = 'User absent'
        response = make_response({"error": error_msg}, 404)
        return response

    if search_user != user:
        error_msg = 'You cannot change information of another user'
        response = make_response({"error": error_msg}, 403)
        return response

    if request.content_type != 'application/x-www-form-urlencoded':
        error_msg = 'Invalid content type'
        response = make_response({"error": error_msg}, 400)
        return response

    if not form.validate_on_submit():
        error_msg = 'Invalid form data'
        response = make_response({"error": error_msg}, 400)
        return response

    username = form.name.data
    email = form.email.data

    user.name = username
    user.email = email

    db.session.add(user)
    db.session.commit(user)

    response = make_response({"status": "ok"}, 200)
    return response


@app.route('/api/user', methods=["POST"])
def post_user():
    """
    User is created and authorized
    """
    form = RegForm()

    if request.content_type != 'application/x-www-form-urlencoded':
        error_msg = 'Invalid content type'
        response = make_response({"error": error_msg}, 400)
        return response

    if not form.validate_on_submit():
        error_msg = 'Invalid form data'
        response = make_response({"error": error_msg}, 400)
        return response

    data = {"name": form.name.data, "password": form.password.data, "email": form.email.data}

    if User.query.filter(User.name == data["name"]).first() is None:
        user = User(**data)
        user.token = get_token()
        user.hash_password()

        db.session.add(user)
        db.session.commit()

        response = make_response({"status": "ok"}, 201)
        response.headers["Location"] = f"http://{request.host}/api/chats"
        response.set_cookie('user_id', str(user.id))
        response.set_cookie('access_token', user.token)
        return response

    error_msg = 'User already exist'
    response = make_response(error_msg, 400)
    return response


@app.route('/api/user', methods=["DELETE"])
@is_auth
def delete_user():
    """
    User is deleted
    """
    user_id = request.cookies.get('user_id')
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    response = make_response({"status": "ok"}, 200)
    response.set_cookie('access_token', ' ', max_age=0)
    response.set_cookie('user_id', ' ', max_age=0)
    return response
