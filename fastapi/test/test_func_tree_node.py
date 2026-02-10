import time

import pytest

from .conftest import fa_client


@pytest.fixture()
def setup1(id_token):
    # Nothing to set up
    print("\nsetup...")

    yield

    # Delete created node
    print("\nteardown...")
    if new_node is not None:
        res = fa_client.delete(
            url=f"/api/tree/node/{new_node['node_id']}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200


@pytest.fixture()
def setup2(id_token, root_node_id):
    # Nothing to set up
    print("\nsetup...")
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

    new_node = None
    for child in children:
        if child["label"] == new_node_label:
            new_node = child
    assert new_node is not None

    yield new_node

    # Nothig to tear down
    print("\nteardown...")


class TestSuccessPost:
    def test_func_tree_node_post_normal(self, id_token, root_node_id, setup1):
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
    def test_func_tree_node_post_bad_request(self, id_token):
        res = fa_client.post(
            url="/api/tree/node",
            headers={"Authorization": id_token},
            json={}
        )
        assert res.status_code == 400

    def test_func_tree_node_post_invalid_token(self, invalid_id_token):
        res = fa_client.post(
            url="/api/tree/node",
            headers={"Authorization": invalid_id_token}
        )
        assert res.status_code == 401


class TestSuccessDelete:
    def test_func_tree_node_delete_normal(self, id_token, setup2):
        new_node = setup2
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
