import pytest

from .conftest import fa_client


@pytest.fixture()
def setup1(id_token, root_node_id):
    # Backup current text
    print("\nsetup...")
    res = fa_client.get(
        url=f"/api/nodes/{root_node_id}",
        headers={"Authorization": id_token},
    )
    assert res.status_code == 200
    before = res.json()["text"]

    yield

    # Restore previous text
    print("\nteardown...")
    res = fa_client.put(
        url=f"/api/nodes/{root_node_id}",
        headers={"Authorization": id_token},
        json={
            "text": f"{before}",
        }
    )
    assert res.status_code == 200


class TestSuccessGet:
    def test_func_nodes_get_nodes(self, id_token):
        res = fa_client.get(
            url="/api/nodes",
            headers={"Authorization": id_token}
        )
        assert res.status_code == 200

        body: list = res.json()
        assert type(body) is list
        assert type(body[0]["user_group"]) is str
        assert type(body[0]["node_id"]) is str
        assert type(body[0]["text"]) is str

    def test_func_nodes_get_node(self, id_token, root_node_id):
        res = fa_client.get(
            url=f"/api/nodes/{root_node_id}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body: dict = res.json()
        assert type(body["user_group"]) is str
        assert type(body["node_id"]) is str
        assert type(body["text"]) is str


class TestFailGet:
    def test_func_nodes_get_nodes_invalid_token(self, invalid_id_token):
        res = fa_client.get(
            url="/api/nodes",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_func_nodes_get_non_exists_node_invalid_token(self, invalid_id_token):
        res = fa_client.get(
            url="/api/nodes/nonexists",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_func_node_get_node_non_exists(self, id_token):
        res = fa_client.get(
            url="/api/nodes/nonexists",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 404


class TestSuccessPut:
    def test_func_nodes_put_normal(self, id_token, root_node_id, setup1):
        text = "test text"
        res = fa_client.put(
            url=f"/api/nodes/{root_node_id}",
            headers={"Authorization": id_token},
            json={
                "text": text,
            }
        )
        assert res.status_code == 200

        body = res.json()
        assert type(body) is dict
        assert body["text"] == text
        assert type(body["user_group"]) is str
        assert type(body["node_id"]) is str

    def test_func_nodes_put_empty_text(self, id_token, root_node_id, setup1):
        res = fa_client.put(
            url=f"/api/nodes/{root_node_id}",
            headers={"Authorization": id_token},
            json={
                "text": "",
            }
        )
        assert res.status_code == 200

        body = res.json()
        assert type(body) is dict
        assert body["text"] == ""
        assert type(body["user_group"]) is str
        assert type(body["node_id"]) is str


class TestFailPut:
    def test_func_node_put_invalid_token(self, invalid_id_token):
        res = fa_client.put(
            url="/api/nodes/test",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_func_nodes_put_no_exist_node(self, id_token):
        res = fa_client.put(
            url="/api/nodes/non_existing_id",
            headers={"Authorization": id_token},
            json={
                "text": "",
            }
        )
        assert res.status_code == 404

    def test_func_nodes_put_bad_request(self, id_token):
        res = fa_client.put(
            url="/api/nodes/non_existing_id",
            headers={"Authorization": id_token},
            json={}
        )
        assert res.status_code == 422
