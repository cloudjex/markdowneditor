from .conftest import fa_client


class TestSuccessGet:
    def test_func_groups_get_nodes(self, id_token):
        res = fa_client.get(
            url="/api/groups",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body: list = res.json()
        assert type(body) is list
        assert type(body[0]["group_id"]) is str
        assert type(body[0]["group_name"]) is str


class TestFailGet:
    def test_func_groups_get_nodes_invalid_token(self, invalid_id_token):
        res = fa_client.get(
            url="/api/nodes",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401
