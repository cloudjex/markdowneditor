import app
from fastapi.testclient import TestClient

from .conftest import EMAIL

client = TestClient(app.app)


class TestSuccessPost:
    def test_func_signin_normal(self):
        res = client.post(
            url="/api/signin",
            json={
                "email": EMAIL,
                "password": "test"
            }
        )
        assert res.status_code == 200
        body: dict = res.json()

        assert body.get("id_token") != None
        assert body.get("email") == EMAIL
        assert type(body["options"]) is dict
        assert body["options"].get("enabled") == True


class TestFailPost:
    def test_func_signin_no_params(self):
        res = client.post(
            url="/api/signin",
            json={
                "email": "",
                "password": ""
            }
        )
        assert res.status_code == 401

    def test_func_signin_invalid_pw(self):
        res = client.post(
            url="/api/signin",
            json={
                "email": "test@gmail.com",
                "password": "invalid_password"
            }
        )
        assert res.status_code == 401

    def test_func_signin_omit_params(self):
        res = client.post(
            url="/api/signin",
            json={}
        )
        assert res.status_code == 422
