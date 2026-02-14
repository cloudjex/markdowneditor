import pytest

from .conftest import fa_client


@pytest.fixture()
def setup_for_move(id_token, root_node_id):
    # First, create 2 nodes
    print("\nsetup...")
    res = fa_client.post(
        url=f"/api/nodes/{root_node_id}",
        headers={"Authorization": id_token},
        json={
            "label": "this is to be parent node",
            "text": "",
        },
    )
    assert res.status_code == 200
    to_be_parent_node = res.json()

    res = fa_client.post(
        url=f"/api/nodes/{root_node_id}",
        headers={"Authorization": id_token},
        json={
            "label": "this is to be child node",
            "text": "",
        },
    )
    assert res.status_code == 200
    to_be_child_node = res.json()

    yield [to_be_parent_node["node_id"], to_be_child_node["node_id"]]

    # Clean up
    print("\nteardown...")
    res = fa_client.delete(
        url=f"/api/nodes/{to_be_parent_node['node_id']}",
        headers={"Authorization": id_token},
    )
    assert res.status_code == 200


class TestSuccessPut:
    def test_func_tree_node_move_put_normal(self, id_token, setup_for_move):
        # Test
        to_be_parent_node_id = setup_for_move[0]
        to_be_child_node_id = setup_for_move[1]

        res = fa_client.put(
            url=f"/api/nodes/move/{to_be_child_node_id}",
            headers={"Authorization": id_token},
            json={
                "parent_id": to_be_parent_node_id,
            },
        )
        assert res.status_code == 200
        body = res.json()
        assert body["result"] == "success"

        # check node is moved
        res = fa_client.get(
            url=f"/api/tree",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body = res.json()
        top_children = [
            i for i in body["children"] if i["node_id"] == to_be_parent_node_id
        ]
        second_children = top_children[0]["children"]
        second_children_ids = [j["node_id"] for j in second_children]
        assert to_be_child_node_id in second_children_ids


class TestFailPut:
    def test_func_tree_node_move_put_root_node(self, id_token, root_node_id):
        res = fa_client.put(
            url=f"/api/nodes/move/{root_node_id}",
            headers={"Authorization": id_token},
            json={
                "parent_id": "00000000-0000-0000-0000-000000000000",
            },
        )
        assert res.status_code == 400

    def test_func_tree_node_move_put_move_to_child(self, id_token, setup_for_move):
        # Test
        to_be_parent_node_id = setup_for_move[0]
        to_be_child_node_id = setup_for_move[1]

        # First, move child under parent
        res = fa_client.put(
            url=f"/api/nodes/move/{to_be_child_node_id}",
            headers={"Authorization": id_token},
            json={
                "parent_id": to_be_parent_node_id,
            },
        )
        assert res.status_code == 200

        # Then, try to move parent under child
        res = fa_client.put(
            url=f"/api/nodes/move/{to_be_parent_node_id}",
            headers={"Authorization": id_token},
            json={
                "parent_id": to_be_child_node_id,
            },
        )
        assert res.status_code == 400

    def test_func_tree_node_move_put_invalid_token(self, invalid_id_token):
        res = fa_client.put(
            url="/api/nodes/move/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": invalid_id_token},
            json={
                "parent_id": "00000000-0000-0000-0000-000000000000",
            },
        )
        assert res.status_code == 401

    def test_func_tree_node_move_put_bad_request(self, id_token):
        res = fa_client.put(
            url="/api/nodes/move/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
            json={},
        )
        assert res.status_code == 422
