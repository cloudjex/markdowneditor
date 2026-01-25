from .conftest import fa_client


class TestSuccessPost:
    def test_func_signup_post_normal(self):
        email = "pytest@gmail.com"
        res = fa_client.post(
            url="/api/signup",
            json={
                "email": email,
                "password": "pytest",
            }
        )
        assert res.status_code == 200

        body = res.json()
        assert body["result"] == "success"


class TestFailPost:
    def test_func_signup_post_no_params(self):
        res = fa_client.post(
            url="/api/signup",
            json={}
        )
        assert res.status_code == 422

    def test_func_signup_post_duplicate_user(self):
        res = fa_client.post(
            url="/api/signup",
            json={
                "email": "test@gmail.com",
                "password": "test",
            }
        )
        assert res.status_code == 409
