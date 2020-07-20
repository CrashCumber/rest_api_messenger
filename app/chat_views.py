import datetime
from flask import request, make_response
from app import app, db, URL
from app.auth_views import is_auth
from app.forms import ChatForm, MessageForm
from app.models import User, Chat, Message


@app.route('/api/chats', methods=["GET"])
@is_auth
def get_chats():
    """
    Get all chats of authorized user
    """
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


@app.route('/api/chats', methods=["POST"])
@is_auth
def post_chats():
    """
    Create chat
    """
    form = ChatForm()

    if request.content_type != 'application/x-www-form-urlencoded':
        error_msg = 'Invalid content type'
        response = make_response({"error": error_msg}, 400)
        return response

    if not form.validate_on_submit():
        error_msg = 'Invalid form data'
        response = make_response({"error": error_msg}, 400)
        return response

    data = form.title.data

    chat_ = Chat(title=data)

    db.session.add(chat_)
    db.session.commit()

    user_id = request.cookies.get('user_id')
    user = User.query.get(user_id)
    user.chats.append(chat_)
    db.session.commit()

    response = make_response({"status": "ok"}, 201)
    response.headers["Location"] = f"{URL}/chats/{chat_.id}"

    return response


@app.route('/api/chats', methods=["DELETE"])
@is_auth
def delete_chat():
    """
    Delete user from chat
    """
    user_id = request.cookies.get('user_id')
    user = User.query.get(user_id)
    chat_id = request.args.get('chat_id')

    chat = Chat.query.get(chat_id)
    user.chats.remove(chat)

    if len(chat.users) == 0:
        db.session.delete(chat)
    else:
        db.session.add(user)

    db.session.commit()

    response = make_response({"status": "ok"}, 200)
    return response


@app.route('/api/chats/<chat_id>', methods=["GET"])
@is_auth
def get_chat(chat_id: int):
    """
    Get chat`s messages
    """
    user_id = request.cookies.get('user_id')
    user = User.query.get(user_id)
    chat = Chat.query.get(chat_id)

    if chat not in user.chats:
        error_msg = 'Access is closed'
        response = make_response({"error": error_msg}, 403)
        return response

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


@app.route('/api/chats/<chat_id>', methods=["POST"])
@is_auth
def post_chat(chat_id: int):
    """
    Send message in chat
    """
    user_id = request.cookies.get('user_id')
    sender = User.query.get(user_id)
    chat = Chat.query.get(chat_id)

    if chat not in sender.chats:
        error_msg = 'Access is closed'
        response = make_response({"error": error_msg}, 403)
        return response

    form = MessageForm()

    if request.content_type != 'application/x-www-form-urlencoded':
        error_msg = 'Invalid content type'
        response = make_response({"error": error_msg}, 400)
        return response

    if not form.validate_on_submit():
        error_msg = 'Invalid form data'
        response = make_response({"error": error_msg}, 400)
        return response

    data = form.content.data

    if chat is None:
        error_msg = 'Non exist chat'
        response = make_response({"error": error_msg}, 404)
        return response

    message = Message(content=data, chat_id=chat_id, sender_id=sender.id)

    chat.last_message = data
    chat.last_message_time = datetime.datetime.now()

    db.session.add(message, chat)
    db.session.commit()

    response = make_response({"status": "ok"}, 201)
    return response


@app.route('/api/chats/<chat_id>', methods=["PUT"])
@is_auth
def put_chat(chat_id: int):
    """
    Rename chat
    """
    user_id = request.cookies.get('user_id')
    sender = User.query.get(user_id)
    chat = Chat.query.get(chat_id)

    if chat not in sender.chats:
        error_msg = 'Access is closed'
        response = make_response({"error": error_msg}, 403)
        return response

    form = ChatForm(csrf_enabled=False)

    if request.content_type != 'application/x-www-form-urlencoded':
        error_msg = 'Invalid content type'
        response = make_response({"error": error_msg}, 400)
        return response

    if not form.validate_on_submit():
        error_msg = 'Invalid form data'
        response = make_response({"error": error_msg}, 400)
        return response

    data = form.title.data

    if chat is None:
        error_msg = 'Non exist chat'
        response = make_response({"error": error_msg}, 404)
        return response

    chat.title = data

    db.session.add(chat)
    db.session.commit()

    response = make_response({"status": "ok"}, 200)
    return response


@app.route('/api/chats/<chat_id>', methods=["DELETE"])
@is_auth
def delete_chat_mes(chat_id: int):
    """
    Delete chat`s message
    """
    user_id = request.cookies.get('user_id')
    user = User.query.get(user_id)
    chat = Chat.query.get(chat_id)
    mes = request.args.get('id')

    if mes not in user.messages or mes not in chat.messages:
        error_msg = 'Access is closed'
        response = make_response({"error": error_msg}, 403)
        return response

    message = Message.query.get(mes)

    db.session.delete(message)
    db.session.commit()

    response = make_response({"status": "ok"}, 200)
    return response
