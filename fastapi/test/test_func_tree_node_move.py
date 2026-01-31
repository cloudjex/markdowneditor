from .conftest import fa_client


class TestSuccessPut:
    def test_func_tree_node_move_put_normal(self, id_token, root_node_id):
        # First, create node
        res = fa_client.post(
            url=f"/api/tree/node",
            headers={"Authorization": id_token},
            json={
                "parent_id": root_node_id,
                "label": "test",
            }
        )
        assert res.status_code == 200

        body = res.json()
        children = body["children"]
        first_new_node = None
        for child in children:
            if child["label"] == "test":
                first_new_node = child
        assert first_new_node is not None

        # Second, create another node to be parent
        res = fa_client.post(
            url=f"/api/tree/node",
            headers={"Authorization": id_token},
            json={
                "parent_id": root_node_id,
                "label": "test",
            }
        )
        assert res.status_code == 200

        body = res.json()
        children = body["children"]
        second_new_node = None
        for child in children:
            if child["label"] == "test":
                second_new_node = child
        assert second_new_node is not None

        # Test
        res = fa_client.put(
            url=f"/api/tree/node/move/{first_new_node['node_id']}",
            headers={"Authorization": id_token},
            json={
                "parent_id": second_new_node["node_id"],
            }
        )
        assert res.status_code == 200

        body = res.json()
        children = body["children"]
        parent_node = None
        for child in children:
            if child["node_id"] == second_new_node["node_id"]:
                parent_node = child
        assert parent_node is not None

        moved_new_node = None
        for child in parent_node["children"]:
            if child["node_id"] == first_new_node["node_id"]:
                moved_new_node = child
        assert moved_new_node is not None

        # Clean up
        res = fa_client.delete(
            url=f"/api/tree/node/{second_new_node['node_id']}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200


class TestFailPut:
    def test_func_tree_node_move_put_invalid_token(self, invalid_id_token):
        res = fa_client.put(
            url="/api/tree/node/move/test_id",
            headers={"Authorization": invalid_id_token},
            json={
                "parent_id": "parent_test_id",
            }
        )
        assert res.status_code == 401

    def test_func_tree_node_move_put_root_node(self, id_token, root_node_id):
        res = fa_client.put(
            url=f"/api/tree/node/move/{root_node_id}",
            headers={"Authorization": id_token},
            json={
                "parent_id": "test",
            }
        )
        assert res.status_code == 403

    def test_func_tree_node_move_put_nonuser_token(self, nonuser_id_token):
        res = fa_client.put(
            url="/api/tree/node/move/test",
            headers={"Authorization": nonuser_id_token},
            json={
                "parent_id": "parent_test_id",
            }
        )
        assert res.status_code == 404

    def test_func_tree_node_move_put_no_params(self, id_token):
        res = fa_client.put(
            url="/api/tree/node/move/test",
            headers={"Authorization": id_token},
            json={}
        )
        assert res.status_code == 422
