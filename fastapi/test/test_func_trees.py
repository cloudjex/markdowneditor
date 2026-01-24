import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


class TestSuccessGET:
    def test_func_trees_get_normal(self, id_token):
        res = client.get(
            url="/api/trees",
            headers={"Authorization": f"Bearer {id_token}"},
        )
        assert res.status_code == 200

        body = res.json()
        tree = body["node_tree"]
        assert "id" in tree
        assert "label" in tree
        assert "children" in tree


class TestFailGet:
    def test_func_trees_get_no_token(self):
        res = client.get(
            url="/api/trees",
        )
        assert res.status_code == 401

    def test_func_trees_get_invalid_token(self, invalid_id_token):
        res = client.get(
            url="/api/trees",
            headers={"Authorization": f"Bearer {invalid_id_token}"},
        )
        assert res.status_code == 401

    def test_func_trees_get_nonuser_token(self, nonuser_id_token):
        res = client.get(
            url="/api/trees",
            headers={"Authorization": f"Bearer {nonuser_id_token}"},
        )
        assert res.status_code == 404
