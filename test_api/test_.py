import pytest
import requests

from db_connection.db_connection import DbClient
data1 = {"name": "valentina", "password": "none"}
data2 = {"name": "v", "password": "valentina"}
data3 = {"name": "", "password": "v"}
data4 = {"name": "", "password": ""}


@pytest.mark.skip()
class TestToken:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, config):
        self.db , self.url = config

    def test_get_token(self):
        location = self.url + '/token'
        response = requests.get(location)

        assert response.cookies.get("access_token") is not None

    def test_get_token_body(self):
        location = self.url + '/token'
        response = requests.get(location)
        status = response.json()["status"]

        assert status == "ok"


class TestLogin:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, config):
        self.db, self.url = config

    def test_post_login_db(self):
        cookies_jar = requests.cookies.RequestsCookieJar()
        token = token.replace('"', '')
        cookies_jar.set('access_token', token)

        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        body = {"name": "valentina", "password": "v"}
        location = self.url + '/login'

        response = requests.post(headers=headers,  data=body, url=location, cookies=cookies_jar)

        user = self.db.get_user(body["name"])

        assert user["id"] == int(response.cookies.get("user_id"))
        assert user["token"] == token

    def test_post_login(self):
        cookies_jar = requests.cookies.RequestsCookieJar()
        cookies_jar.set('access_token', token)

        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        body = {"name": "valentina", "password": "v"}
        location = self.url + '/login'

        response = requests.post(headers=headers,  data=body, url=location, cookies=cookies_jar)
        location = response.headers["Location"]

        # cookies_jar.set('user_id', response.cookies.get("user_id"))

        assert location == self.url + '/chats'
        assert response.cookies.get("user_id") is not None

    def test_post_login_wrong_content_type(self):
        cookies_jar = requests.cookies.RequestsCookieJar()
        token = token.replace('"', '')
        cookies_jar.set('access_token', token)

        headers = {'Content-Type': "application/json"}
        body = {"name": "valentina", "password": "v"}
        location = self.url + '/login'

        response = requests.post(headers=headers,  data=body, url=location, cookies=cookies_jar)

        assert response.status_code == 400

    def test_post_login_without_token(self):
        cookies_jar = requests.cookies.RequestsCookieJar()

        headers = {'Content-Type': "application/x-www-form-urlencodedn"}
        body = {"name": "valentina", "password": "v"}
        location = self.url + '/login'

        response = requests.post(headers=headers,  data=body, url=location, cookies=cookies_jar)

        assert response.status_code == 400

    @pytest.mark.parametrize("body", [data1, data2, data3, data4])
    def test_post_login_wrong_data(self, token, body):
        cookies_jar = requests.cookies.RequestsCookieJar()
        token = token.replace('"', '')
        cookies_jar.set('access_token', token)

        headers = {'Content-Type': "application/x-www-form-urlencoded"}

        location = self.url + '/login'

        response = requests.post(headers=headers,  data=body, url=location, cookies=cookies_jar)
        assert response.status_code == 400




