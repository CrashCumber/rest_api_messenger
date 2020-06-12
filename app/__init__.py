from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Command, Shell
from flask_migrate import Migrate


import os, config

# создание экземпляра приложения
app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopmentConfig')

# инициализирует расширения
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# import views
from . import views

