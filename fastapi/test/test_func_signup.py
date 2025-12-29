from lib import func_signup

from .conftest import logger


class TestSuccessPost:
    def test_func_signup_post_normal(self):
        email = "pytest@gmail.com"
        params = {
            "method": "POST",
            "headers": {
                "content-type": "application/json",
            },
            "body": {
                "email": email,
                "password": "pytest",
            },
            "query_params": {},
        }
        response = func_signup.main(params)
        logger(response)
        assert response["status_code"] == 200
        assert response["body"]["email"] == email


class TestFailPost:
    def test_func_signup_post_no_params(self):
        params = {
            "method": "POST",
            "headers": {
                "content-type": "application/json",
            },
            "body": {},
            "query_params": {},
        }
        response = func_signup.main(params)
        logger(response)
        assert response["status_code"] == 400

    def test_func_signup_post_duplicate_user(self):
        params = {
            "method": "POST",
            "headers": {
                "content-type": "application/json",
            },
            "body": {
                "email": "test@gmail.com",
                "password": "test",
            },
            "query_params": {},
        }
        response = func_signup.main(params)
        logger(response)
        assert response["status_code"] == 409
