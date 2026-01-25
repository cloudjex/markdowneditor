from .conftest import fa_client


class TestSuccessGET:
    def test_func_trees_get_normal(self, id_token):
        res = fa_client.get(
            url="/api/trees",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body = res.json()
        assert type(body["id"]) is str
        assert type(body["label"]) is str
        assert type(body["children"]) is list


class TestFailGet:
    def test_func_trees_get_no_token(self):
        res = fa_client.get(
            url="/api/trees",
        )
        assert res.status_code == 401

    def test_func_trees_get_invalid_token(self, invalid_id_token):
        res = fa_client.get(
            url="/api/trees",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_func_trees_get_nonuser_token(self, nonuser_id_token):
        res = fa_client.get(
            url="/api/trees",
            headers={"Authorization": nonuser_id_token},
        )
        assert res.status_code == 404
