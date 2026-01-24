import time

import app
from fastapi.testclient import TestClient

from .conftest import ROOT_NODE_ID

client = TestClient(app.app)


class TestSuccessPost:
    def test_func_trees_operate_post_normal(self, id_token):
        res = client.post(
            url="/api/trees/operate",
            headers={"Authorization": f"Bearer {id_token}"},
            json={
                "parent_id": ROOT_NODE_ID,
                "label": str(time.time()),
            }
        )
        assert res.status_code == 200

        body = res.json()
        global new_id
        new_id = body["id"]
        node_tree = body["node_tree"]
        children = node_tree["children"]

        new_node = None
        for child in children:
            if child["id"] == new_id:
                new_node = child
        assert new_node is not None
        assert "id" in new_node
        assert "label" in new_node
        assert "children" in new_node


class TestFailPost:
    def test_func_trees_operate_post_no_token(self):
        res = client.post(
            url="/api/trees/operate",
        )
        assert res.status_code == 401

    def test_func_trees_operate_post_invalid_token(self, invalid_id_token):
        res = client.post(
            url="/api/trees/operate",
            headers={"Authorization": f"Bearer {invalid_id_token}"}
        )
        assert res.status_code == 401

    def test_func_trees_operate_post_nonuser_token(self, nonuser_id_token):
        res = client.post(
            url="/api/trees/operate",
            headers={"Authorization": f"Bearer {nonuser_id_token}"},
            json={
                "parent_id": "invalid",
                "label": "invalid",
            }
        )
        assert res.status_code == 404

    def test_func_trees_operate_post_no_params(self, id_token):
        res = client.post(
            url="/api/trees/operate",
            headers={"Authorization": f"Bearer {id_token}"},
            json={}
        )
        assert res.status_code == 422


class TestSuccessDelete:
    def test_func_trees_operate_delete_normal(self, id_token):
        res = client.delete(
            url="/api/trees/operate",
            headers={"Authorization": f"Bearer {id_token}"},
            params={"id": new_id}
        )
        assert res.status_code == 200

        body = res.json()
        node_tree = body["node_tree"]
        children = node_tree["children"]
        new_node = None
        for child in children:
            if child["id"] == new_id:
                new_node = child
        assert new_node is None


class TestFailDelete:
    def test_func_trees_operate_delete_no_token(self):
        res = client.delete(
            url="/api/trees/operate",
        )
        assert res.status_code == 401

    def test_func_trees_operate_delete_invalid_token(self, invalid_id_token):
        res = client.delete(
            url="/api/trees/operate",
            headers={"Authorization": f"Bearer {invalid_id_token}"}
        )
        assert res.status_code == 401

    def test_func_trees_operate_delete_nonuser_token(self, nonuser_id_token):
        res = client.delete(
            url="/api/trees/operate",
            headers={"Authorization": f"Bearer {nonuser_id_token}"},
            params={"id": "test"}
        )
        assert res.status_code == 404

    def test_func_trees_operate_delete_root(self, id_token):
        res = client.delete(
            url="/api/trees/operate",
            headers={"Authorization": f"Bearer {id_token}"},
            params={"id": ROOT_NODE_ID}
        )
        assert res.status_code == 403

    def test_func_trees_operate_delete_non_exist(self, id_token):
        res = client.delete(
            url="/api/trees/operate",
            headers={"Authorization": f"Bearer {id_token}"},
            params={"id": "/Nodes/non_exist_node"}
        )
        assert res.status_code == 404

    def test_func_trees_operate_delete_no_params(self, id_token):
        res = client.delete(
            url="/api/trees/operate",
            headers={"Authorization": f"Bearer {id_token}"},
            params={}
        )
        assert res.status_code == 422
