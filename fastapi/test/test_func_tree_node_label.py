import time

import pytest

from .conftest import fa_client


@pytest.fixture()
def setup1(id_token, root_node_id):
    # Get current tree root label
    print("\nsetup...")
    res = fa_client.get(
        url=f"/api/tree",
        headers={"Authorization": id_token},
    )
    assert res.status_code == 200
    body = res.json()
    root_label = body["label"]

    yield

    # Restore previous tree root label
    print("\nteardown...")
    res = fa_client.put(
        url=f"/api/tree/node/label/{root_node_id}",
        headers={"Authorization": id_token},
        json={
            "label": root_label,
        }
    )
    assert res.status_code == 200

    body = res.json()
    assert body["label"] == root_label


class TestSuccessPut:
    def test_func_tree_node_label_put_normal(self, id_token, root_node_id, setup1):
        new_label = str(time.time())
        res = fa_client.put(
            url=f"/api/tree/node/label/{root_node_id}",
            headers={"Authorization": id_token},
            json={
                "label": new_label,
            }
        )
        assert res.status_code == 200

        body = res.json()
        assert body["label"] == new_label
        assert type(body["node_id"]) is str
        assert type(body["label"]) is str
        assert type(body["children"]) is list


class TestFailPut:
    def test_func_tree_node_label_put_invalid_token(self, invalid_id_token):
        res = fa_client.put(
            url="/api/tree/node/label/test",
            headers={"Authorization": invalid_id_token}
        )
        assert res.status_code == 401

    def test_func_tree_node_label_put_no_params(self, id_token):
        res = fa_client.put(
            url="/api/tree/node/label/test",
            headers={"Authorization": id_token},
            json={}
        )
        assert res.status_code == 422
