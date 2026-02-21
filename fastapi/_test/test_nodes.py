import time

import pytest

from .conftest import fa_client


class TestGetNodesSuccess:
    def test_get_nodes(self, id_token):
        res = fa_client.get(
            url="/api/nodes",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body: list = res.json()
        assert type(body) is list
        assert type(body[0]["group_id"]) is str
        assert type(body[0]["node_id"]) is str
        assert type(body[0]["label"]) is str
        assert type(body[0]["text"]) is str
        assert type(body[0]["children_ids"]) is list

    def test_get_node(self, id_token, root_node_id):
        res = fa_client.get(
            url=f"/api/nodes/{root_node_id}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body: dict = res.json()
        assert type(body) is dict
        assert type(body["group_id"]) is str
        assert type(body["node_id"]) is str
        assert type(body["label"]) is str
        assert type(body["text"]) is str
        assert type(body["children_ids"]) is list


class TestGetNodesFail:
    def test_with_invalid_token(self, invalid_id_token):
        res = fa_client.get(
            url="/api/nodes",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_with_invalid_token2(self, invalid_id_token):
        res = fa_client.get(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_get_non_exist_node(self, id_token):
        res = fa_client.get(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 404


class TestPostNodesSuccess:
    @pytest.fixture()
    def delete_node(self, id_token):
        # Nothing to set up
        print("\nsetup...")

        context = {}
        yield context

        # Delete created node
        node = context["node"]
        print("\nteardown...")
        res = fa_client.delete(
            url=f"/api/nodes/{node['node_id']}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

    def test_post_node(self, id_token, root_node_id, delete_node):
        new_node_label = str(time.time())
        res = fa_client.post(
            url=f"/api/nodes/{root_node_id}",
            headers={"Authorization": id_token},
            json={
                "label": new_node_label,
                "text": "",
            },
        )
        assert res.status_code == 200
        new_node = res.json()

        # check node is created
        res = fa_client.get(
            url=f"/api/tree",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body = res.json()

        children = body["children"]
        children_ids = [i["node_id"] for i in children]
        assert new_node["node_id"] in children_ids

        # return context to fixture
        delete_node["node"] = new_node


class TestPostNodesFail:
    def test_with_invalid_token(self, invalid_id_token):
        res = fa_client.post(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_with_bad_request(self, id_token):
        res = fa_client.post(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
            json={},
        )
        assert res.status_code == 422

    def test_with_invalid_str(self, id_token):
        res = fa_client.post(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
            json={
                "label": "",
                "text": "",
            },
        )
        assert res.status_code == 422


class TestPutNodesSuccess:
    @pytest.fixture()
    def reset_root_node(self, id_token, root_node_id):
        # Backup current label and text
        print("\nsetup...")
        res = fa_client.get(
            url=f"/api/nodes/{root_node_id}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200
        res_json = res.json()

        yield res_json["label"], res_json["text"]

        # Restore previous label and text
        print("\nteardown...")
        res = fa_client.put(
            url=f"/api/nodes/{root_node_id}",
            headers={"Authorization": id_token},
            json={
                "label": res_json["label"],
                "text": res_json["text"],
            },
        )
        assert res.status_code == 200

    def test_put_node(self, id_token, root_node_id, reset_root_node):
        label = reset_root_node[0]
        text = "test text"

        res = fa_client.put(
            url=f"/api/nodes/{root_node_id}",
            headers={"Authorization": id_token},
            json={
                "label": label,
                "text": text,
            },
        )
        assert res.status_code == 200

        body = res.json()
        assert type(body) is dict
        assert body["text"] == text
        assert body["label"] == label
        assert type(body["group_id"]) is str
        assert type(body["node_id"]) is str
        assert type(body["children_ids"]) is list

    def test_with_empty_text(self, id_token, root_node_id, reset_root_node):
        label = reset_root_node[0]
        text = ""

        res = fa_client.put(
            url=f"/api/nodes/{root_node_id}",
            headers={"Authorization": id_token},
            json={
                "label": label,
                "text": text,
            },
        )
        assert res.status_code == 200

        body = res.json()
        assert type(body) is dict
        assert body["text"] == text
        assert body["label"] == label
        assert type(body["group_id"]) is str
        assert type(body["node_id"]) is str
        assert type(body["children_ids"]) is list

    def test_update_label(self, id_token, root_node_id, reset_root_node):
        label = f"{reset_root_node[0]} ver2"
        text = reset_root_node[1]

        res = fa_client.put(
            url=f"/api/nodes/{root_node_id}",
            headers={"Authorization": id_token},
            json={
                "label": label,
                "text": text,
            },
        )
        assert res.status_code == 200

        body = res.json()
        assert type(body) is dict
        assert body["text"] == text
        assert body["label"] == label
        assert type(body["group_id"]) is str
        assert type(body["node_id"]) is str
        assert type(body["children_ids"]) is list


class TestPutNodesFail:
    def test_with_invalid_token(self, invalid_id_token):
        res = fa_client.put(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_put_no_exist_node(self, id_token):
        res = fa_client.put(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
            json={
                "label": "test",
                "text": "",
            },
        )
        assert res.status_code == 404

    def test_with_bad_request(self, id_token):
        res = fa_client.put(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
            json={},
        )
        assert res.status_code == 422


class TestDeleteNodesSuccess:
    @pytest.fixture()
    def prepare_node(self, id_token, root_node_id):
        # Create new node
        print("\nsetup...")
        new_node_label = str(time.time())
        res = fa_client.post(
            url=f"/api/nodes/{root_node_id}",
            headers={"Authorization": id_token},
            json={
                "label": new_node_label,
                "text": "",
            },
        )
        assert res.status_code == 200

        yield res.json()

        # Nothig to tear down
        print("\nteardown...")

    def test_delete_node(self, id_token, prepare_node):
        del_node_id = prepare_node["node_id"]
        res = fa_client.delete(
            url=f"/api/nodes/{del_node_id}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        # check node is deleted
        res = fa_client.get(
            url=f"/api/tree",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body = res.json()
        children = body["children"]
        children_ids = [i["node_id"] for i in children]
        assert del_node_id not in children_ids


class TestDeleteNodesFail:
    def test_delete_root_node(self, id_token, root_node_id):
        res = fa_client.delete(
            url=f"/api/nodes/{root_node_id}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 400

    def test_with_invalid_token(self, invalid_id_token):
        res = fa_client.delete(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_delete_non_exist_node(self, id_token):
        res = fa_client.delete(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 404
