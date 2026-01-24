import textwrap

import app
from fastapi.testclient import TestClient

from .conftest import ROOT_NODE_ID

client = TestClient(app.app)


class TestSuccessGET:
    def test_func_nodes_get_normal(self, id_token):
        res = client.get(
            url="/api/nodes",
            headers={"Authorization": f"Bearer {id_token}"}
        )
        assert res.status_code == 200

        body: dict = res.json()
        nodes = body["nodes"]
        assert type(nodes) is list
        assert "email" in nodes[0]
        assert "id" in nodes[0]
        assert "text" in nodes[0]

    def test_func_nodes_get_normal_with_params(self, id_token):
        res = client.get(
            url="/api/nodes",
            headers={"Authorization": f"Bearer {id_token}"},
            params={"id": ROOT_NODE_ID}
        )
        assert res.status_code == 200

        body: dict = res.json()
        node = body["node"]
        assert type(node) is dict
        assert "email" in node
        assert "id" in node
        assert "text" in node


class TestFailGet:
    def test_func_node_get_no_token(self):
        res = client.get(
            url="/api/nodes",
        )
        assert res.status_code == 401

    def test_func_node_get_invalid_token(self, invalid_id_token):
        res = client.get(
            url="/api/nodes",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_func_node_get_nonuser_token(self, nonuser_id_token):
        res = client.get(
            url="/api/nodes",
            headers={"Authorization": nonuser_id_token},
        )
        assert res.status_code == 404

    def test_func_node_get_with_params_nonuser_token(self, nonuser_id_token):
        res = client.get(
            url="/api/nodes",
            headers={"Authorization": nonuser_id_token},
            params={"id": "hogehoge"}
        )
        assert res.status_code == 404


class TestSuccessPut:
    def test_func_nodes_put_normal(self, id_token):
        # First, get the current text
        res = client.get(
            url="/api/nodes",
            headers={"Authorization": id_token},
            params={"id": ROOT_NODE_ID}
        )
        assert res.status_code == 200
        before = res.json()["node"]["text"]

        # Test
        text = """
            # MarkdownEditor

            ## CICD Status
            [![CICD Workflow](https://github.com/cloudjex/markdowneditor/actions/workflows/cicd.yaml/badge.svg)](https://github.com/cloudjex/markdowneditor/actions/workflows/cicd.yaml)

            ## Sample Application URL
            https://www.cloudjex.com
        """
        text = textwrap.dedent(text).strip("\n")

        res = client.put(
            url="/api/nodes",
            headers={"Authorization": id_token},
            json={
                "id": ROOT_NODE_ID,
                "text": f"{text}",
            }
        )
        assert res.status_code == 200

        body = res.json()
        node = body["node"]
        assert type(node) is dict
        assert node["text"] == text
        assert "email" in node
        assert "id" in node

        # Restore previous text
        res = client.put(
            url="/api/nodes",
            headers={"Authorization": id_token},
            json={
                "id": ROOT_NODE_ID,
                "text": f"{before}",
            }
        )
        assert res.status_code == 200

    def test_func_nodes_put_empty_text(self, id_token):
        # First, get the current text
        res = client.get(
            url="/api/nodes",
            headers={"Authorization": id_token},
            params={"id": ROOT_NODE_ID}
        )
        assert res.status_code == 200
        before = res.json()["node"]["text"]

        # Test
        res = client.put(
            url="/api/nodes",
            headers={"Authorization": id_token},
            json={
                "id": ROOT_NODE_ID,
                "text": "",
            }
        )
        assert res.status_code == 200

        body = res.json()
        node = body["node"]
        assert type(node) is dict
        assert node["text"] == ""
        assert "email" in node
        assert "id" in node

        # Restore previous text
        res = client.put(
            url="/api/nodes",
            headers={"Authorization": id_token},
            json={
                "id": ROOT_NODE_ID,
                "text": f"{before}",
            }
        )
        assert res.status_code == 200


class TestFailPut:
    def test_func_nodes_put_no_token(self):
        res = client.put(
            url="/api/nodes",
        )
        assert res.status_code == 401

    def test_func_node_put_invalid_token(self, invalid_id_token):
        res = client.put(
            url="/api/nodes",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_func_nodes_put_no_exist_node(self, id_token):
        res = client.put(
            url="/api/nodes",
            headers={"Authorization": id_token},
            json={
                "id": "non_existing_id",
                "text": "",
            }
        )
        assert res.status_code == 404

    def test_func_nodes_put_no_params(self, id_token):
        res = client.put(
            url="/api/nodes",
            headers={"Authorization": id_token},
            json={}
        )
        assert res.status_code == 422
