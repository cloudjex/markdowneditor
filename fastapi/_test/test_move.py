import pytest

from .conftest import fa_client


class TestMoveNodeSuccess:
    @pytest.fixture()
    def prepare_2_node(self, id_token, root_node_id):
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

    def test_move_node(self, id_token, prepare_2_node):
        # Test
        to_be_parent_node_id = prepare_2_node[0]
        to_be_child_node_id = prepare_2_node[1]

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


class TestMoveNodeFail:
    @pytest.fixture()
    def prepare_2_node(self, id_token, root_node_id):
        # Create parent node and child node
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
        parent_node_id = res.json()["node_id"]

        res = fa_client.post(
            url=f"/api/nodes/{parent_node_id}",
            headers={"Authorization": id_token},
            json={
                "label": "this is to be child node",
                "text": "",
            },
        )
        assert res.status_code == 200
        child_node_id = res.json()["node_id"]

        yield [parent_node_id, child_node_id]

        # Clean up
        print("\nteardown...")
        res = fa_client.delete(
            url=f"/api/nodes/{parent_node_id}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

    def test_move_root_node(self, id_token, root_node_id):
        res = fa_client.put(
            url=f"/api/nodes/move/{root_node_id}",
            headers={"Authorization": id_token},
            json={
                "parent_id": root_node_id,
            },
        )
        assert res.status_code == 400

    def test_move_node_to_child(self, id_token, prepare_2_node):
        # Test
        parent_node_id = prepare_2_node[0]
        child_node_id = prepare_2_node[1]

        # move parent node to under child
        res = fa_client.put(
            url=f"/api/nodes/move/{parent_node_id}",
            headers={"Authorization": id_token},
            json={
                "parent_id": child_node_id,
            },
        )
        assert res.status_code == 400

    def test_with_invalid_token(self, invalid_id_token):
        res = fa_client.put(
            url="/api/nodes/move/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": invalid_id_token},
            json={
                "parent_id": "00000000-0000-0000-0000-000000000000",
            },
        )
        assert res.status_code == 401

    def test_move_non_exist_node(self, id_token):
        res = fa_client.put(
            url="/api/nodes/move/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
            json={
                "parent_id": "00000000-0000-0000-0000-000000000000",
            },
        )
        assert res.status_code == 404

    def test_with_bad_request(self, id_token):
        res = fa_client.put(
            url="/api/nodes/move/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
            json={},
        )
        assert res.status_code == 422
