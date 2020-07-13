import pytest
import requests
from sqlalchemy import null

from db_connection.db_connection import DbClient


@pytest.fixture(scope='session')
def config():
    url = 'http://127.0.0.1:5000'
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


