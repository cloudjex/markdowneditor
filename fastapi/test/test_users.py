import pytest

from .conftest import EMAIL, PASSWORD, fa_client


class TestGetUsersMeSuccess:
    def test_get_user_me(self, id_token):
        res = fa_client.get(
            url="/api/users/me",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200
        body = res.json()
        assert body["email"] == EMAIL
        assert body["password"] == "*****"
        assert type(body["groups"]) is list
        assert type(body["groups"][0]) is str
        assert type(body["options"]) is dict
        assert type(body["options"]["enabled"]) is bool
        assert type(body["options"]["otp"]) is str


class TestGetUsersMeFail:
    def test_with_invalid_token(self, invalid_id_token):
        res = fa_client.get(
            url="/api/users/me",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401


class TestPutUsersMeSuccess:
    @pytest.fixture()
    def reset_pw(self, id_token):
        # Return new pw
        new_password = "NewTestPassword123!"

        yield new_password

        # Reset to original pw
        res = fa_client.put(
            url="/api/users/me/password",
            headers={"Authorization": id_token},
            json={
                "old_password": new_password,
                "new_password": PASSWORD,
            },
        )
        assert res.status_code == 200

    def test_put_me_pw(self, id_token, reset_pw):
        new_password = reset_pw

        res = fa_client.put(
            url="/api/users/me/password",
            headers={"Authorization": id_token},
            json={
                "old_password": PASSWORD,
                "new_password": new_password,
            },
        )
        assert res.status_code == 200
        body = res.json()
        assert body["result"] == "success"


class TestPutUsersMeFail:
    def test_with_invalid_token(self, invalid_id_token):
        res = fa_client.put(
            url="/api/users/me/password",
            headers={"Authorization": invalid_id_token},
            json={
                "old_password": "test",
                "new_password": "test",
            },
        )
        assert res.status_code == 401

    def test_put_me_pw_with_incorrect_pw(self, id_token):
        res = fa_client.put(
            url="/api/users/me/password",
            headers={"Authorization": id_token},
            json={
                "old_password": PASSWORD + "wrong",
                "new_password": "wrong",
            },
        )
        assert res.status_code == 401

    def test_with_bad_request(self, id_token):
        res = fa_client.put(
            url="/api/users/me/password",
            headers={"Authorization": id_token},
            json={},
        )
        assert res.status_code == 422

    def test_put_me_pw_with_invalid_str(self, id_token):
        res = fa_client.put(
            url="/api/users/me/password",
            headers={"Authorization": id_token},
            json={
                "old_password": PASSWORD,
                "new_password": "123",
            },
        )
        assert res.status_code == 422
