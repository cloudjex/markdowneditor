import time

from .conftest import fa_client


class TestSuccessPut:
    def test_func_tree_node_label_put_normal(self, id_token):
        # Get tree
        res = fa_client.get(
            url=f"/api/tree",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body = res.json()
        root_id = body["id"]
        root_label = body["label"]

        # Test
        new_label = str(time.time())
        res = fa_client.put(
            url=f"/api/tree/node/label/{root_id}",
            headers={"Authorization": id_token},
            json={
                "label": new_label,
            }
        )
        assert res.status_code == 200

        body = res.json()
        assert body["label"] == new_label
        assert type(body["id"]) is str
        assert type(body["label"]) is str
        assert type(body["children"]) is list

        # Reset
        res = fa_client.put(
            url=f"/api/tree/node/label/{root_id}",
            headers={"Authorization": id_token},
            json={
                "label": root_label,
            }
        )
        assert res.status_code == 200

        body = res.json()
        assert body["label"] == root_label


class TestFailPut:
    def test_func_tree_node_label_put_invalid_token(self, invalid_id_token):
        res = fa_client.put(
            url="/api/tree/node/label/test",
            headers={"Authorization": invalid_id_token}
        )
        assert res.status_code == 401

    def test_func_tree_node_label_put_nonuser_token(self, nonuser_id_token):
        res = fa_client.put(
            url="/api/tree/node/label/test",
            headers={"Authorization": nonuser_id_token},
            json={
                "label": "invalid",
            }
        )
        assert res.status_code == 404

    def test_func_tree_node_label_put_no_params(self, id_token):
        res = fa_client.put(
            url="/api/tree/node/label/test",
            headers={"Authorization": id_token},
            json={}
        )
        assert res.status_code == 422
