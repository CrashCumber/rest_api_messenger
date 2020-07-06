import pytest
import requests

from api_client.api_client import Api


class Test():
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, config_api):
        self.url = config_api.url

    def test_login(self):
        location = self.url + '/token'
        response = requests.get(location)

        headers = {'Content-Type': "application/x-www-form-urlencoded", "X-CSRF-Token": response.headers["X-CSRF-Token"]}
        # body = {"name": "valentina", "password": "v"}
        body = {"name": "frhhhefefhui", "password": "v", 'email': 'nsdb@nfdfvn.ru'}

        location = self.url + '/registration'

        response = requests.post(headers=headers,  data=body, url=location)
        print(response.headers)

        location = response.headers["Location"]
        headers = response.headers

        response = requests.get(url=location, headers=headers)
        print(response.json())




