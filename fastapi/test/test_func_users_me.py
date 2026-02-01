from .conftest import EMAIL, PASSWORD, fa_client


class TestSuccessGet:
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


class TestSuccessPut:
    def test_func_users_me_put_pw(self, id_token):
        res = fa_client.put(
            url="/api/users/me/password",
            headers={"Authorization": id_token},
            json={
                "old_password": PASSWORD,
                "new_password": "NewTestPassword123!",
            }
        )
        assert res.status_code == 200

        body = res.json()
        assert body["result"] == "success"

        # Clean up
        res = fa_client.put(
            url="/api/users/me/password",
            headers={"Authorization": id_token},
            json={
                "old_password": "NewTestPassword123!",
                "new_password": PASSWORD,
            }
        )
        assert res.status_code == 200

        body = res.json()
        assert body["result"] == "success"


class TestFailPut:
    def test_func_users_me_put_invalid_token(self, invalid_id_token):
        res = fa_client.put(
            url="/api/users/me/password",
            headers={"Authorization": invalid_id_token},
            json={
                "old_password": "test",
                "new_password": "test",
            }
        )
        assert res.status_code == 401

    def test_func_users_me_put_invalid_password(self, id_token):
        res = fa_client.put(
            url="/api/users/me/password",
            headers={"Authorization": id_token},
            json={
                "old_password": PASSWORD + "wrong",
                "new_password": "wrong",
            }
        )
        assert res.status_code == 401

    def test_func_users_me_put_short_password(self, id_token):
        res = fa_client.put(
            url="/api/users/me/password",
            headers={"Authorization": id_token},
            json={
                "old_password": PASSWORD,
                "new_password": "123",
            }
        )
        assert res.status_code == 400

    def test_func_users_me_put_nonuser_token(self, nonuser_id_token):
        res = fa_client.put(
            url="/api/users/me/password",
            headers={"Authorization": nonuser_id_token},
            json={
                "old_password": "test",
                "new_password": "test",
            }
        )
        assert res.status_code == 404
