from .conftest import fa_client


class TestSuccessPost:
    def test_func_signout_normal(self, id_token):
        res = fa_client.post(
            url="/api/signout",
            headers={"Authorization": id_token}
        )
        assert res.status_code == 200

        body = res.json()
        assert body["result"] == "success"


class TestFailPost:
    def test_func_signout_no_token(self):
        res = fa_client.post(
            url="/api/signout",
        )
        assert res.status_code == 401

    def test_func_signout_invalid_token(self, invalid_id_token):
        res = fa_client.post(
            url="/api/signout",
            headers={"Authorization": invalid_id_token}
        )
        assert res.status_code == 401
