import time

from lib import func_trees_operate

from .conftest import ROOT_NODE_ID, logger


class TestSuccessPut:
    def test_func_trees_operate_put_normal(self, id_token):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {
                "parent_id": ROOT_NODE_ID,
                "label": str(time.time()),
            },
            "query_params": {},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 200

        body = response["body"]
        global new_id
        new_id = body["id"]
        node_tree = body["node_tree"]
        children = node_tree["children"]

        new_node = None
        for child in children:
            if child["id"] == new_id:
                new_node = child
        assert new_node is not None
        assert "id" in new_node
        assert "label" in new_node
        assert "children" in new_node


class TestFailPut:
    def test_func_trees_operate_put_no_token(self):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": ""
            },
            "body": {},
            "query_params": {},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 401

    def test_func_trees_operate_put_invalid_token(self, invalid_id_token):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {invalid_id_token}"
            },
            "body": {},
            "query_params": {},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 401

    def test_func_trees_operate_put_nonuser_token(self, nonuser_id_token):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {nonuser_id_token}"
            },
            "body": {"parent_id": "test", "label": "test"},
            "query_params": {},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 404

    def test_func_trees_operate_put_no_params(self, id_token):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {"": ""},
            "query_params": {},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 400

    def test_func_trees_operate_put_invalid_id(self, id_token):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {"parent_id": "invalid", "lable": "invalid"},
            "query_params": {},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 400


class TestSuccessDelete:
    def test_func_trees_operate_delete_normal(self, id_token):
        params = {
            "method": "DELETE",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {},
            "query_params": {"id": new_id},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 200
        node_tree = response["body"]["node_tree"]
        children = node_tree["children"]
        new_node = None
        for child in children:
            if child["id"] == new_id:
                new_node = child
        assert new_node is None


class TestFailDelete:
    def test_func_trees_operate_delete_no_token(self):
        params = {
            "method": "DELETE",
            "headers": {
                "content-type": "application/json",
                "authorization": ""
            },
            "body": {},
            "query_params": {},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 401

    def test_func_trees_operate_delete_invalid_token(self, invalid_id_token):
        params = {
            "method": "DELETE",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {invalid_id_token}"
            },
            "body": {},
            "query_params": {},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 401

    def test_func_trees_operate_delete_nonuser_token(self, nonuser_id_token):
        params = {
            "method": "DELETE",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {nonuser_id_token}"
            },
            "body": {},
            "query_params": {"id": "test"},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 404

    def test_func_trees_operate_delete_no_params(self, id_token):
        params = {
            "method": "DELETE",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {},
            "query_params": {},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 400

    def test_func_trees_operate_delete_root(self, id_token):
        params = {
            "method": "DELETE",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {},
            "query_params": {"id": ROOT_NODE_ID},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 403

    def test_func_trees_operate_delete_non_exist(self, id_token):
        params = {
            "method": "DELETE",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {},
            "query_params": {"id": "/Nodes/non_exist_node"},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 404
