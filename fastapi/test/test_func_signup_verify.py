from .conftest import fa_client


class TestFailPost:
    def test_func_signup_verify_post_no_params(self):
        res = fa_client.post(
            url="/api/signup/verify",
            json={}
        )

        assert res.status_code == 422

    def test_func_signup_verify_post_non_exist_user(self):
        res = fa_client.post(
            url="/api/signup/verify",
            json={
                "email": "nonexist@gmail.com",
                "otp": "000000"
            }
        )

        assert res.status_code == 404
