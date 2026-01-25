import time

from .conftest import ROOT_NODE_ID, fa_client


class TestSuccessPost:
    def test_func_tree_operate_post_normal(self, id_token):
        new_node_label = str(time.time())
        res = fa_client.post(
            url="/api/tree/operate",
            headers={"Authorization": id_token},
            json={
                "parent_id": ROOT_NODE_ID,
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
        assert type(new_node["id"]) is str
        assert type(new_node["label"]) is str
        assert type(new_node["children"]) is list


class TestFailPost:
    def test_func_tree_operate_post_no_token(self):
        res = fa_client.post(
            url="/api/tree/operate",
        )
        assert res.status_code == 401

    def test_func_tree_operate_post_invalid_token(self, invalid_id_token):
        res = fa_client.post(
            url="/api/tree/operate",
            headers={"Authorization": invalid_id_token}
        )
        assert res.status_code == 401

    def test_func_tree_operate_post_nonuser_token(self, nonuser_id_token):
        res = fa_client.post(
            url="/api/tree/operate",
            headers={"Authorization": nonuser_id_token},
            json={
                "parent_id": "invalid",
                "label": "invalid",
            }
        )
        assert res.status_code == 404

    def test_func_tree_operate_post_no_params(self, id_token):
        res = fa_client.post(
            url="/api/tree/operate",
            headers={"Authorization": id_token},
            json={}
        )
        assert res.status_code == 422


class TestSuccessPut:
    def test_func_tree_operate_put_normal(self, id_token):
        global new_node
        put_node_id = new_node["id"]
        new_label = str(time.time())
        res = fa_client.put(
            url=f"/api/tree/operate/{put_node_id}",
            headers={"Authorization": id_token},
            json={
                "label": new_label,
            }
        )
        assert res.status_code == 200

        body = res.json()
        children = body["children"]

        check_node = None
        for child in children:
            if child["label"] == new_label:
                check_node = child
        assert check_node is not None
        assert type(check_node["id"]) is str
        assert type(check_node["label"]) is str
        assert type(check_node["children"]) is list


class TestFailPut:
    def test_func_tree_operate_put_no_token(self):
        res = fa_client.put(
            url="/api/tree/operate/test",
        )
        assert res.status_code == 401

    def test_func_tree_operate_put_invalid_token(self, invalid_id_token):
        res = fa_client.put(
            url="/api/tree/operate/test",
            headers={"Authorization": invalid_id_token}
        )
        assert res.status_code == 401

    def test_func_tree_operate_put_nonuser_token(self, nonuser_id_token):
        res = fa_client.put(
            url="/api/tree/operate/test",
            headers={"Authorization": nonuser_id_token},
            json={
                "label": "invalid",
            }
        )
        assert res.status_code == 404

    def test_func_tree_operate_put_no_params(self, id_token):
        res = fa_client.put(
            url="/api/tree/operate/test",
            headers={"Authorization": id_token},
            json={}
        )
        assert res.status_code == 422


class TestSuccessDelete:
    def test_func_tree_operate_delete_normal(self, id_token):
        global new_node
        del_node_id = new_node["id"]
        res = fa_client.delete(
            url=f"/api/tree/operate/{del_node_id}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body = res.json()
        children = body["children"]
        new_node = None
        for child in children:
            if child["id"] == del_node_id:
                new_node = child
        assert new_node is None


class TestFailDelete:
    def test_func_tree_operate_delete_no_token(self):
        res = fa_client.delete(
            url="/api/tree/operate/test",
        )
        assert res.status_code == 401

    def test_func_tree_operate_delete_invalid_token(self, invalid_id_token):
        res = fa_client.delete(
            url="/api/tree/operate/test",
            headers={"Authorization": invalid_id_token}
        )
        assert res.status_code == 401

    def test_func_tree_operate_delete_nonuser_token(self, nonuser_id_token):
        res = fa_client.delete(
            url="/api/tree/operate/test",
            headers={"Authorization": nonuser_id_token},
        )
        assert res.status_code == 404

    def test_func_tree_operate_delete_root(self, id_token):
        res = fa_client.delete(
            url=f"/api/tree/operate/{ROOT_NODE_ID}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 403

    def test_func_tree_operate_delete_non_exist(self, id_token):
        res = fa_client.delete(
            url="/api/tree/operate/non_exist_node",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 404
