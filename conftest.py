from app.models import *
import pytest
from faker import Faker

fake = Faker()


@pytest.fixture(scope="function")
def config():
    url = 'http://127.0.0.1:5000'
    yield url
    user = User.query.filter(User.name == 'aleksa').first()
    print(user)


@pytest.fixture()
def data():
    """
    formation valid user data
    :return: {"name": name, "password": password, "email": email}
    deletion user after test
    """
    name = fake.name()
    password = fake.password()
    email = fake.email()

    data = {"name": name, "password": password, "email": email}

    yield data

    # user = User.query.filter(User.name == name).first()
    # print(user)


