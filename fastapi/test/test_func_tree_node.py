import time

from .conftest import fa_client


class TestSuccessPost:
    def test_func_tree_node_post_normal(self, id_token, root_node_id):
        new_node_label = str(time.time())
        res = fa_client.post(
            url="/api/tree/node",
            headers={"Authorization": id_token},
            json={
                "parent_id": root_node_id,
                "label": new_node_label,
            }
        )
        assert res.status_code == 200

        body = res.json()
        children = body["children"]

        global new_node
        new_node = None
        for child in children:
            if child["label"] == new_node_label:
                new_node = child
        assert new_node is not None
        assert type(new_node["node_id"]) is str
        assert type(new_node["label"]) is str
        assert type(new_node["children"]) is list


class TestFailPost:
    def test_func_tree_node_post_invalid_token(self, invalid_id_token):
        res = fa_client.post(
            url="/api/tree/node",
            headers={"Authorization": invalid_id_token}
        )
        assert res.status_code == 401

    def test_func_tree_node_post_nonuser_token(self, nonuser_id_token):
        res = fa_client.post(
            url="/api/tree/node",
            headers={"Authorization": nonuser_id_token},
            json={
                "parent_id": "invalid",
                "label": "invalid",
            }
        )
        assert res.status_code == 404

    def test_func_tree_node_post_no_params(self, id_token):
        res = fa_client.post(
            url="/api/tree/node",
            headers={"Authorization": id_token},
            json={}
        )
        assert res.status_code == 422


class TestSuccessDelete:
    def test_func_tree_node_delete_normal(self, id_token):
        global new_node
        del_node_id = new_node["node_id"]
        res = fa_client.delete(
            url=f"/api/tree/node/{del_node_id}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body = res.json()
        children = body["children"]
        new_node = None
        for child in children:
            if child["node_id"] == del_node_id:
                new_node = child
        assert new_node is None


class TestFailDelete:
    def test_func_tree_node_delete_invalid_token(self, invalid_id_token):
        res = fa_client.delete(
            url="/api/tree/node/test",
            headers={"Authorization": invalid_id_token}
        )
        assert res.status_code == 401

    def test_func_tree_node_delete_nonuser_token(self, nonuser_id_token):
        res = fa_client.delete(
            url="/api/tree/node/test",
            headers={"Authorization": nonuser_id_token},
        )
        assert res.status_code == 404

    def test_func_tree_node_delete_root(self, id_token, root_node_id):
        res = fa_client.delete(
            url=f"/api/tree/node/{root_node_id}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 403

    def test_func_tree_node_delete_non_exist(self, id_token):
        res = fa_client.delete(
            url="/api/tree/node/non_exist_node",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 404
