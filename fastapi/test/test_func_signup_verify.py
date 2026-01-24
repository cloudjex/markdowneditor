import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


class TestFailPost:
    def test_func_signup_verify_post_no_params(self):
        res = client.post(
            url="/api/signup/verify",
            json={}
        )

        assert res.status_code == 422

    def test_func_signup_verify_post_non_exist_user(self):
        res = client.post(
            url="/api/signup/verify",
            json={
                "email": "nonexist@gmail.com",
                "otp": "000000"
            }
        )

        assert res.status_code == 404
