from .conftest import fa_client


class TestSuccessPost:
    def test_signout(self, id_token):
        res = fa_client.post(
            url="/api/signout",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body = res.json()
        assert body["result"] == "success"


class TestFailPost:
    def test_with_invalid_token(self, invalid_id_token):
        res = fa_client.post(
            url="/api/signout",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401
