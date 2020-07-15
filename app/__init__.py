from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Command, Shell
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

import os, config

app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopmentConfig')

# инициализирует расширения
db = SQLAlchemy(app)
db.init_app(app)

migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

URL = "http://127.0.0.1:5000"

# import views
from . import chat_views, auth_views, user_views

