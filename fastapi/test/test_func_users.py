from .conftest import fa_client, EMAIL


class TestSuccessGET:
    def test_func_users_me_get_normal(self, id_token):
        res = fa_client.get(
            url="/api/users/me",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body = res.json()
        assert body["email"] == EMAIL
        assert body["password"] == "***"
        assert type(body["options"]) is dict
        assert type(body["options"]["enabled"]) is bool
        assert type(body["options"]["otp"]) is str


class TestFailGet:
    def test_func_users_me_get_invalid_token(self, invalid_id_token):
        res = fa_client.get(
            url="/api/users/me",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_func_users_me_get_nonuser_token(self, nonuser_id_token):
        res = fa_client.get(
            url="/api/users/me",
            headers={"Authorization": nonuser_id_token},
        )
        assert res.status_code == 404
