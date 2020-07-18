from time import sleep

import pytest
import requests
from app.models import *
from db_connection.db_connection import DbClient
from test_api.base import BaseCase

data1 = {"name": "valentina", "password": "none"}
data2 = {"name": "v", "password": ""}
data3 = {"name": ""}
data4 = {"password": ""}


# @pytest.mark.skip()
class TestLogin(BaseCase):

    def test_post_login_db_user_id(self):
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        body = {"name": 'aleksa', "password": '111111111'}
        location = self.url + '/login'

        response = requests.post(headers=headers,  data=body, url=location)

        user = self.db.get_user(body["name"])
        assert int(response.cookies.get("user_id")) is not None, response.json()
        assert user["id"] == int(response.cookies.get("user_id"))

    def test_post_login_db_token(self):
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        # body = {"name": reg_user["name"], "password": reg_user["password"]}
        body = {"name": 'aleksa', "password": '111111111'}

        location = self.url + '/login'

        response = requests.post(headers=headers, data=body, url=location)

        user = self.db.get_user(body["name"])
        user_ = User.query.filter(User.name == body["name"]).first()
        print(user, '\n', user_)

        assert response.cookies.get("access_token") is not None, response.content
        token = response.cookies.get("access_token").replace('"', '')

        assert user_.token == token

    def test_post_login(self):
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        body = {"name": 'aleksa', "password": '111111111'}
        location = self.url + '/login'

        response = requests.post(headers=headers,  data=body, url=location)
        location = response.headers["Location"]

        # cookies_jar.set('user_id', response.cookies.get("user_id"))

        assert location == self.url + '/chats'

    def test_post_login_wrong_content_type(self):
        headers = {'Content-Type': "application/json"}
        body = {"name": 'aleksa', "password": '111111111'}
        location = self.url + '/login'

        response = requests.post(headers=headers,  data=body, url=location)

        assert response.status_code == 400

    @pytest.mark.parametrize("body", [data1, data2, data3, data4])
    def test_post_login_wrong_data(self, token, body):
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        location = self.url + '/login'

        response = requests.post(headers=headers,  data=body, url=location)

        assert response.status_code == 400


class InvalidReg:
    data1 = {"name": "nemmw", "password": "nonknne", "email": "ojdoprjfpo"}
    data2 = {"name": "jjv", "password": "valentina", "email": "ojdoprjf@po.ru"}
    data3 = {"name": "", "password": "v", "email": "val@ijfir.ru"}
    data4 = {"name": "valentina", "password": "", "email": "ojdoprj@fpo.ru"}


@pytest.mark.skip()
class TestReg(BaseCase):

    def test_post_reg_db_user_id(self, new_user):
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        location = self.url + '/user'

        response = requests.post(headers=headers, data=new_user, url=location)

        user = self.db.get_user(new_user["name"])
        assert int(response.cookies.get("user_id")) is not None
        assert user["id"] == int(response.cookies.get("user_id"))

    def test_post_reg_db_token(self, new_user):
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        location = self.url + '/user'

        response = requests.post(headers=headers, data=new_user, url=location)
        token = response.cookies.get("access_token").replace('"', '')

        user = self.db.get_user(new_user["name"])

        assert response.cookies.get("access_token") is not None
        assert user["token"] == token

    def test_post_reg(self, new_user):
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        location = self.url + '/user'

        response = requests.post(headers=headers, data=new_user, url=location)
        location = response.headers["Location"]

        assert location == self.url + '/chats'
        assert response.status_code == 201

    def test_post_login_wrong_content_type(self, new_user):
        headers = {'Content-Type': "application/json"}
        location = self.url + '/user'

        response = requests.post(headers=headers, data=new_user, url=location)

        assert response.status_code == 400

    @pytest.mark.parametrize("body", [InvalidReg.data1, InvalidReg.data2, InvalidReg.data3, InvalidReg.data4])
    def test_post_login_wrong_data(self, token, body):
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        location = self.url + '/user'

        response = requests.post(headers=headers, data=body, url=location)

        assert response.status_code == 400




