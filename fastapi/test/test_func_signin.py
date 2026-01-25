from .conftest import EMAIL, fa_client


class TestSuccessPost:
    def test_func_signin_normal(self):
        res = fa_client.post(
            url="/api/signin",
            json={
                "email": EMAIL,
                "password": "test"
            }
        )
        assert res.status_code == 200
        body: dict = res.json()

        assert type(body["id_token"]) is str


class TestFailPost:
    def test_func_signin_no_params(self):
        res = fa_client.post(
            url="/api/signin",
            json={
                "email": "",
                "password": ""
            }
        )
        assert res.status_code == 401

    def test_func_signin_invalid_pw(self):
        res = fa_client.post(
            url="/api/signin",
            json={
                "email": "test@gmail.com",
                "password": "invalid_password"
            }
        )
        assert res.status_code == 401

    def test_func_signin_omit_params(self):
        res = fa_client.post(
            url="/api/signin",
            json={}
        )
        assert res.status_code == 422
