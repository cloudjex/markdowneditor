from .conftest import EMAIL, PASSWORD, fa_client


class TestSuccessPost:
    def test_signin(self):
        res = fa_client.post(
            url="/api/signin",
            json={
                "email": EMAIL,
                "password": PASSWORD,
            },
        )
        assert res.status_code == 200
        body: dict = res.json()

        assert type(body["id_token"]) is str


class TestFailPost:
    def test_with_incorrect_email_pw(self):
        res = fa_client.post(
            url="/api/signin",
            json={
                "email": "invalid@gmail.com",
                "password": "invalid",
            },
        )
        assert res.status_code == 401

    def test_with_incorrect_pw(self):
        res = fa_client.post(
            url="/api/signin",
            json={
                "email": EMAIL,
                "password": "invalid_password",
            },
        )
        assert res.status_code == 401

    def test_with_bad_request(self):
        res = fa_client.post(
            url="/api/signin",
            json={},
        )
        assert res.status_code == 422
