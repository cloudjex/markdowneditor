import time

import pytest

from .conftest import fa_client


@pytest.fixture()
def setup_for_post(id_token):
    # Nothing to set up
    print("\nsetup...")

    yield

    # Delete created node
    print("\nteardown...")
    if new_node is not None:
        res = fa_client.delete(
            url=f"/api/nodes/{new_node['node_id']}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200


@pytest.fixture()
def setup_for_put(id_token, root_node_id):
    # Backup current text
    print("\nsetup...")
    res = fa_client.get(
        url=f"/api/nodes/{root_node_id}",
        headers={"Authorization": id_token},
    )
    assert res.status_code == 200
    res_json = res.json()

    yield res_json["label"], res_json["text"]

    # Restore previous text
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


@pytest.fixture()
def setup_for_delete(id_token, root_node_id):
    # Nothing to set up
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


class TestSuccessGet:
    def test_func_nodes_get_nodes(self, id_token):
        res = fa_client.get(url="/api/nodes", headers={"Authorization": id_token})
        assert res.status_code == 200

        body: list = res.json()
        assert type(body) is list
        assert type(body[0]["user_group"]) is str
        assert type(body[0]["node_id"]) is str
        assert type(body[0]["label"]) is str
        assert type(body[0]["text"]) is str
        assert type(body[0]["children_ids"]) is list

    def test_func_nodes_get_node(self, id_token, root_node_id):
        res = fa_client.get(
            url=f"/api/nodes/{root_node_id}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body: dict = res.json()
        assert type(body["user_group"]) is str
        assert type(body["node_id"]) is str
        assert type(body["label"]) is str
        assert type(body["text"]) is str
        assert type(body["children_ids"]) is list


class TestFailGet:
    def test_func_nodes_get_nodes_invalid_token(self, invalid_id_token):
        res = fa_client.get(
            url="/api/nodes",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_func_nodes_get_non_exists_node_invalid_token(self, invalid_id_token):
        res = fa_client.get(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_func_nodes_get_node_non_exists(self, id_token):
        res = fa_client.get(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 404


class TestSuccessPost:
    def test_func_nodes_post_normal(self, id_token, root_node_id, setup_for_post):
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

        body = res.json()
        global new_node
        new_node = body

        # check node is created
        res = fa_client.get(
            url=f"/api/tree",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body = res.json()
        children = body["children"]

        created = False
        for i in children:
            if i["node_id"] == new_node["node_id"]:
                created = True
        assert created


class TestFailPost:
    def test_func_nodes_post_invalid_token(self, invalid_id_token):
        res = fa_client.post(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_func_nodes_post_bad_request(self, id_token):
        res = fa_client.post(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
            json={},
        )
        assert res.status_code == 422

    def test_func_nodes_post_invalid_str(self, id_token):
        res = fa_client.post(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
            json={
                "label": "",
                "text": "",
            },
        )
        assert res.status_code == 422


class TestSuccessPut:
    def test_func_nodes_put_normal(self, id_token, root_node_id, setup_for_put):
        text = "test text"
        label = setup_for_put[0]
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
        assert type(body["user_group"]) is str
        assert type(body["node_id"]) is str
        assert type(body["children_ids"]) is list

    def test_func_nodes_put_empty_text(self, id_token, root_node_id, setup_for_put):
        text = ""
        label = setup_for_put[0]
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
        assert type(body["user_group"]) is str
        assert type(body["node_id"]) is str
        assert type(body["children_ids"]) is list

    def test_func_nodes_put_update_label(self, id_token, root_node_id, setup_for_put):
        text = setup_for_put[1]
        label = f"{setup_for_put[0]} version2"
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
        assert type(body["user_group"]) is str
        assert type(body["node_id"]) is str
        assert type(body["children_ids"]) is list


class TestFailPut:
    def test_func_nodes_put_invalid_token(self, invalid_id_token):
        res = fa_client.put(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_func_nodes_put_no_exist_node(self, id_token):
        res = fa_client.put(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
            json={
                "label": "test",
                "text": "",
            },
        )
        assert res.status_code == 404

    def test_func_nodes_put_bad_request(self, id_token):
        res = fa_client.put(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
            json={},
        )
        assert res.status_code == 422


class TestSuccessDelete:
    def test_func_nodes_delete_normal(self, id_token, setup_for_delete):
        del_node_id = setup_for_delete["node_id"]
        res = fa_client.delete(
            url=f"/api/nodes/{del_node_id}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body = res.json()
        assert body["result"] == "success"

        # check node is deleted
        res = fa_client.get(
            url=f"/api/tree",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body = res.json()
        children = body["children"]
        assert del_node_id not in children


class TestFailDelete:
    def test_func_nodes_delete_invalid_token(self, invalid_id_token):
        res = fa_client.delete(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_func_nodes_delete_root(self, id_token, root_node_id):
        res = fa_client.delete(
            url=f"/api/nodes/{root_node_id}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 403

    def test_func_nodes_delete_non_exist(self, id_token):
        res = fa_client.delete(
            url="/api/nodes/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 404
