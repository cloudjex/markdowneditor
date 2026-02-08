from .conftest import fa_client


class TestSuccessGET:
    def test_func_tree_get_normal(self, id_token):
        res = fa_client.get(
            url="/api/tree",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body = res.json()
        assert type(body["node_id"]) is str
        assert type(body["label"]) is str
        assert type(body["children"]) is list


class TestFailGet:
    def test_func_tree_get_invalid_token(self, invalid_id_token):
        res = fa_client.get(
            url="/api/tree",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401
