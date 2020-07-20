import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:flask@db:3306/messenger'#'mysql+pymysql://root@0.0.0.0:3307/messenger'
    threaded = True
    WTF_CSRF_ENABLED = False


