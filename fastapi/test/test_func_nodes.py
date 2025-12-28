import textwrap

from lib import func_nodes

from .conftest import logger


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
            "query_params": {"node_id": "/Nodes"},
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
        text = """
            # MarkdownEditor

            ## CICD Status
            [![CICD Workflow](https://github.com/cloudjex/markdowneditor/actions/workflows/cicd.yaml/badge.svg)](https://github.com/cloudjex/markdowneditor/actions/workflows/cicd.yaml)

            ## Sample Application URL
            https://www.cloudjex.com
        """
        text = textwrap.dedent(text)

        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {
                "node_id": "/Nodes",
                "text": f"{text}",
            },
            "query_params": {},
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 200
        assert response["body"]["node"]["text"] == text

    def test_func_nodes_put_empty_text(self, id_token):
        # First, get the current text
        params = {
            "method": "GET",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {},
            "query_params": {"node_id": "/Nodes"},
        }
        response = func_nodes.main(params)
        assert response["status_code"] == 200
        before = response["body"]["node"]["text"]

        # Update with empty text
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {
                "node_id": "/Nodes",
                "text": "",
            },
            "query_params": {},
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 200
        assert response["body"]["node"]["text"] == ""

        # Restore previous text
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {
                "node_id": "/Nodes",
                "text": f"{before}",
            },
            "query_params": {},
        }
        func_nodes.main(params)


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

    def test_func_nodes_put_no_exist_node(self, id_token):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {
                "node_id": "non_existing_node_id",
                "text": "",
            },
            "query_params": {},
        }
        response = func_nodes.main(params)
        logger(response)
        assert response["status_code"] == 404
