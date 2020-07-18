from time import sleep

import pytest
import requests
from sqlalchemy import null
from faker import Faker
fake = Faker()
from db_connection.db_connection import DbClient
from app.models import *

@pytest.fixture()
def config():
    url = 'http://127.0.0.1:5000/api'
    db = DbClient()
    return db, url


@pytest.fixture(scope='function')
def token(config):
    location = 'http://127.0.0.1:5000/token'
    response = requests.get(location)

    yield response.cookies.get('access_token')
    db, url = config
    data = {"field_name": "token", "new_data": "NULL", "name": "valentina"}
    db.update_user(data)


@pytest.fixture()
def new_user(config):
    name = fake.name()
    password = fake.password()
    email = fake.email()

    data = {"name": name, "password": password, "email": email}

    yield data

    db, url = config
    user = User.query.filter(User.name == data["name"]).first()
    print(user)


@pytest.fixture()
def reg_user(config):
    name = fake.name()
    password = fake.password()
    email = fake.email()

    data = {"name": name, "password": password, "email": email}
    db, url = config

    db.insert_user(data)
    data = db.get_user(name)

    yield data
    data = db.get_user(name)
    # db.delete_user(name)
