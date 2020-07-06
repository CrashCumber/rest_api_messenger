import pytest

from api_client.api_client import Api


@pytest.fixture(scope='session')
def config_api():
    url = ' http://127.0.0.1:5000'
    return Api(url)
