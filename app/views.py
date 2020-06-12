from flask import request, render_template, redirect
from jinja2 import Template

from app import app, db
from app.forms import *

from app.models import User


@app.route('/chats', methods=["POST", "GET"])
def chats():
    print('chats')

@app.route('/chat', methods=["POST", "GET"])
def chat():
    return 'chat'

@app.route('/create_chat', methods=["POST", "GET"])
def create_chat():
    return 'chat'


@app.route('/create_user', methods=["POST", "GET"])
def create_user():
    form = RegForm(request.form)
    if request.method == 'POST':
        data = {"name": form.name.data, "email": form.email.data, "password": form.password.data}
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return redirect('/chat')
    else:
        return render_template('create_user.html', form=form, title="registration")
