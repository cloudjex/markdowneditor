import time

from .conftest import EMAIL, GROUP_ID, PASSWORD, fa_client


class TestSigninSuccess:
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


class TestSigninFail:
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


class TestSigninGroupSuccess:
    def test_signin_group_with_user_token(self, user_token):
        res = fa_client.post(
            url="/api/signin/group",
            headers={"Authorization": user_token},
            json={
                "group_id": GROUP_ID,
            },
        )
        assert res.status_code == 200
        body: dict = res.json()
        assert type(body["id_token"]) is str

    def test_signin_group_with_group_token(self, id_token):
        res = fa_client.post(
            url="/api/signin/group",
            headers={"Authorization": id_token},
            json={
                "group_id": GROUP_ID,
            },
        )
        assert res.status_code == 200
        body: dict = res.json()
        assert type(body["id_token"]) is str


class TestSigninGroupFail:
    def test_with_invalid_token(self, invalid_id_token):
        res = fa_client.post(
            url="/api/signin/group",
            headers={"Authorization": invalid_id_token},
            json={
                "group_id": GROUP_ID,
            },
        )
        assert res.status_code == 401

    def test_with_bad_request(self, user_token):
        res = fa_client.post(
            url="/api/signin/group",
            headers={"Authorization": user_token},
            json={},
        )
        assert res.status_code == 422


class TestSignupSuccess:
    def test_signup(self):
        user = f"{int(time.time())}@cloudjex.com"
        res = fa_client.post(
            url="/api/signup",
            json={
                "email": user,
                "password": PASSWORD,
            },
        )
        assert res.status_code == 200
        body: dict = res.json()
        assert body["result"] == "success"


class TestSignupFail:
    def test_with_existing_email(self):
        res = fa_client.post(
            url="/api/signup",
            json={
                "email": EMAIL,
                "password": PASSWORD,
            },
        )
        assert res.status_code == 409

    def test_with_bad_request(self):
        res = fa_client.post(
            url="/api/signup",
            json={},
        )
        assert res.status_code == 422

    def test_with_invalid_pw(self):
        res = fa_client.post(
            url="/api/signup",
            json={
                "email": EMAIL,
                "password": "123",
            },
        )
        assert res.status_code == 422


class TestSignoutSuccess:
    def test_signout(self, id_token):
        res = fa_client.post(
            url="/api/signout",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200
        body = res.json()
        assert body["result"] == "success"


class TestSignoutFail:
    def test_with_invalid_token(self, invalid_id_token):
        res = fa_client.post(
            url="/api/signout",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401
