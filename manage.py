import os
from flask_migrate import MigrateCommand
from app import app, db
from app.models import *
from flask_script import Manager, Shell
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Chat=Chat, Message=Message)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
