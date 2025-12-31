from lib import func_trees_operate

from .conftest import logger


class TestSuccessPut:
    def test_func_trees_operate_put_normal(self, id_token):
        new_node_id = "/Nodes/test_new_node"
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {"node_id": new_node_id},
            "query_params": {},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 200
        tree = response["body"]["tree"]
        children = tree["children"]
        new_node = None
        for child in children:
            if child["id"] == new_node_id:
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
            "body": {"node_id": "test"},
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
            "body": {"node_id": ""},
            "query_params": {},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 400

    def test_func_trees_operate_put_invalid_node_id(self, id_token):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {"node_id": "/Nodes/"},
            "query_params": {},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 400

    def test_func_trees_operate_put_duplicate(self, id_token):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {"node_id": "/Nodes/test_new_node"},
            "query_params": {},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 409


class TestSuccessDelete:
    def test_func_trees_operate_delete_normal(self, id_token):
        new_node_id = "/Nodes/test_new_node"
        params = {
            "method": "DELETE",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {},
            "query_params": {"node_id": new_node_id},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 200
        tree = response["body"]["tree"]
        children = tree["children"]
        new_node = None
        for child in children:
            if child["id"] == new_node_id:
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
            "query_params": {"node_id": "test"},
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

    def test_func_trees_operate_delete_non_exist(self, id_token):
        params = {
            "method": "DELETE",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {},
            "query_params": {"node_id": "/non_exist_node"},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 404
