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
        token = response.cookies.get("access_token")
        cookies_jar = requests.cookies.RequestsCookieJar()
        cookies_jar.set('access_token', token)
        print(response.cookies, type(response.cookies))
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        body = {"name": "valentina", "password": "v"}
        location = self.url + '/login'
        print(cookies_jar)

        response = requests.post(headers=headers,  data=body, url=location, cookies=cookies_jar)
        cookies_jar.set('user_id', response.cookies.get("user_id"))

        location = response.headers["Location"]

        response = requests.get(url=location, cookies=cookies_jar)
        print(response.content, cookies_jar)




