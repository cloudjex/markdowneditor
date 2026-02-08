import pytest

from .conftest import fa_client


@pytest.fixture()
def setup1(id_token, root_node_id):
    # First, create 2 nodes
    print("\nsetup...")
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
    to_be_parent_node = None
    for child in children:
        if child["label"] == "test":
            to_be_parent_node = child
    assert to_be_parent_node is not None

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
    to_be_child_node = None
    for child in children:
        if child["label"] == "test":
            to_be_child_node = child
    assert to_be_child_node is not None

    yield [to_be_parent_node, to_be_child_node]

    # Clean up
    print("\nteardown...")
    res = fa_client.delete(
        url=f"/api/tree/node/{to_be_parent_node['node_id']}",
        headers={"Authorization": id_token},
    )
    assert res.status_code == 200


class TestSuccessPut:
    def test_func_tree_node_move_put_normal(self, id_token, setup1):
        # Test
        to_be_parent_node = setup1[0]
        to_be_child_node = setup1[1]

        res = fa_client.put(
            url=f"/api/tree/node/move/{to_be_child_node['node_id']}",
            headers={"Authorization": id_token},
            json={
                "parent_id": to_be_parent_node["node_id"],
            }
        )
        assert res.status_code == 200

        body = res.json()
        children = body["children"]
        parent_node = None
        for child in children:
            if child["node_id"] == to_be_parent_node["node_id"]:
                parent_node = child
        assert parent_node is not None

        child_node = None
        for child in parent_node["children"]:
            if child["node_id"] == to_be_child_node["node_id"]:
                child_node = child
        assert child_node is not None


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

    def test_func_tree_node_move_put_move_to_child(self, id_token, setup1):
        # Test
        to_be_parent_node = setup1[0]
        to_be_child_node = setup1[1]

        # First, move child under parent
        res = fa_client.put(
            url=f"/api/tree/node/move/{to_be_child_node['node_id']}",
            headers={"Authorization": id_token},
            json={
                "parent_id": to_be_parent_node["node_id"],
            }
        )
        assert res.status_code == 200

        # Then, try to move parent under child
        res = fa_client.put(
            url=f"/api/tree/node/move/{to_be_parent_node['node_id']}",
            headers={"Authorization": id_token},
            json={
                "parent_id": to_be_child_node["node_id"],
            }
        )
        assert res.status_code == 403

    def test_func_tree_node_move_put_no_params(self, id_token):
        res = fa_client.put(
            url="/api/tree/node/move/test",
            headers={"Authorization": id_token},
            json={}
        )
        assert res.status_code == 422
