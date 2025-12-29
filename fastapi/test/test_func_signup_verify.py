from lib import func_signup_verify

from .conftest import logger


class TestFailPost:
    def test_func_signup_verify_post_no_params(self):
        params = {
            "method": "POST",
            "headers": {
                "content-type": "application/json",
            },
            "body": {},
            "query_params": {},
        }
        response = func_signup_verify.main(params)
        logger(response)
        assert response["status_code"] == 400

    def test_func_signup_verify_post_non_exist_user(self):
        params = {
            "method": "POST",
            "headers": {
                "content-type": "application/json",
            },
            "body": {
                "email": "nonexist@gmail.com",
                "otp": "000000"
            },
            "query_params": {},
        }
        response = func_signup_verify.main(params)
        logger(response)
        assert response["status_code"] == 404
