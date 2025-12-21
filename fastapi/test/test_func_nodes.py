from lib import func_nodes

from .conftest import logger

PUT_NODE_ID = "test_id_12345"


class TestSuccessGET:
    def test_func_nodes_get_normal(self, id_token):
        params = {
            "method": "GET",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {},
            "query_params": {},
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 200
        assert type(response["body"]["nodes"]) is list

    def test_func_nodes_get_normal_with_params(self, id_token):
        params = {
            "method": "GET",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {},
            "query_params": {"node_id": "/Folder"},
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 200
        assert type(response["body"]["node"]) is dict


class TestFailGet:
    def test_func_node_get_no_token(self):
        params = {
            "method": "GET",
            "headers": {
                "content-type": "application/json",
                "authorization": ""
            },
            "body": {},
            "query_params": {},
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 401

    def test_func_node_get_invalid_token(self, invalid_id_token):
        params = {
            "method": "GET",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {invalid_id_token}"
            },
            "body": {},
            "query_params": {},
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 401

    def test_func_node_get_nonuser_token(self, nonuser_id_token):
        params = {
            "method": "GET",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {nonuser_id_token}"
            },
            "body": {},
            "query_params": {},
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 404

    def test_func_node_get_with_params_nonuser_token(self, nonuser_id_token):
        params = {
            "method": "GET",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {nonuser_id_token}"
            },
            "body": {},
            "query_params": {
                "node_id": "hogehogehogehoge"
            },
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 404


class TestSuccessPut:
    def test_func_nodes_put_normal(self, id_token):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {
                "node_id": f"{PUT_NODE_ID}",
                "text": f"#{PUT_NODE_ID}",
            },
            "query_params": {},
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 200
        assert type(response["body"]["node"]) is dict


class TestFailPut:
    def test_func_nodes_put_no_token(self):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": ""
            },
            "body": {},
            "query_params": {},
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 401

    def test_func_nodes_put_no_params(self, id_token):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {
                "node_id": "",
                "text": "",
            },
            "query_params": {},
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 400

    def test_func_nodes_put_conflict(self, id_token):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {
                "node_id": f"{PUT_NODE_ID}",
                "text": f"#{PUT_NODE_ID}",
            },
            "query_params": {},
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 409


class TestSuccessDelete:
    def test_func_nodes_delete_normal(self, id_token):
        params = {
            "method": "DELETE",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {},
            "query_params": {
                "node_id": f"{PUT_NODE_ID}",
            },
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 200
        assert type(response["body"]["node"]) is dict


class TestFailDelete:
    def test_func_nodes_delete_no_token(self):
        params = {
            "method": "DELETE",
            "headers": {
                "content-type": "application/json",
                "authorization": ""
            },
            "body": {},
            "query_params": {},
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 401

    def test_func_nodes_delete_noexist_node(self, id_token):
        params = {
            "method": "DELETE",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {},
            "query_params": {
                "node_id": "non_exist_node_id",
            },
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 404

    def test_func_nodes_delete_no_params(self, id_token):
        params = {
            "method": "DELETE",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {},
            "query_params": {
                "node_id": "",
            },
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 400
