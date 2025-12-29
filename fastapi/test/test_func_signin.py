from lib import func_signin

from .conftest import logger


class TestSuccessPost:
    def test_func_signin_normal(self):
        params = {
            "method": "POST",
            "headers": {
                "content-type": "application/json"
            },
            "body": {
                "email": "test@gmail.com",
                "password": "test"
            },
            "query_params": {},
        }
        response = func_signin.main(params)
        logger(response)
        assert response["status_code"] == 200

        body: dict = response["body"]
        assert body.get("id_token") != None
        assert body.get("email") != None


class TestFailPost:
    def test_func_signin_no_params(self):
        params = {
            "method": "POST",
            "headers": {
                "content-type": "application/json"
            },
            "body": {
                "email": "",
                "password": ""
            },
            "query_params": {},
        }
        response = func_signin.main(params)
        logger(response)
        assert response["status_code"] == 400

    def test_func_signin_omit_params(self):
        params = {
            "method": "POST",
            "headers": {
                "content-type": "application/json"
            },
            "body": {},
            "query_params": {},
        }
        response = func_signin.main(params)
        logger(response)
        assert response["status_code"] == 400

    def test_func_signin_invalid_pw(self):
        params = {
            "method": "POST",
            "headers": {
                "content-type": "application/json"
            },
            "body": {
                "email": "test@gmail.com",
                "password": "invalid_password"
            },
            "query_params": {},
        }
        response = func_signin.main(params)
        logger(response)
        assert response["status_code"] == 401

    def test_func_signin_invalid_id_and_pw(self):
        params = {
            "method": "POST",
            "headers": {
                "content-type": "application/json"
            },
            "body": {
                "email": "hogehoge@gmail.com",
                "password": "hogehoge"
            },
            "query_params": {},
        }
        response = func_signin.main(params)
        logger(response)
        assert response["status_code"] == 401
