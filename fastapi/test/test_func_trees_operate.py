from lib import func_trees_operate

from .conftest import logger


class TestSuccessPut:
    def test_func_trees_operate_put_normal(self, id_token):
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
        assert response["status_code"] == 200
        assert type(response["body"]) is dict


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

    def test_func_trees_operate_put_dupulicate(self, id_token):
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
        params = {
            "method": "DELETE",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {},
            "query_params": {"node_id": "/Nodes/test_new_node"},
        }
        response = func_trees_operate.main(params)
        logger(response)
        assert response["status_code"] == 200
        assert type(response["body"]) is dict


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
