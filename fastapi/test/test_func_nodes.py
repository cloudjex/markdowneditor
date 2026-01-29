import textwrap

from .conftest import ROOT_NODE_ID, fa_client


class TestSuccessGET:
    def test_func_nodes_get_normal(self, id_token):
        res = fa_client.get(
            url="/api/nodes",
            headers={"Authorization": id_token}
        )
        assert res.status_code == 200

        body: dict = res.json()
        nodes = body["nodes"]
        assert type(nodes) is list
        assert type(nodes[0]["id"]) is str
        assert type(nodes[0]["email"]) is str
        assert type(nodes[0]["text"]) is str

    def test_func_nodes_get_normal_with_id(self, id_token):
        res = fa_client.get(
            url=f"/api/nodes/{ROOT_NODE_ID}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200

        body: dict = res.json()
        assert type(body["id"]) is str
        assert type(body["email"]) is str
        assert type(body["text"]) is str

class TestFailGet:
    def test_func_node_get_invalid_token(self, invalid_id_token):
        res = fa_client.get(
            url="/api/nodes",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_func_node_get_nonuser_token(self, nonuser_id_token):
        res = fa_client.get(
            url="/api/nodes",
            headers={"Authorization": nonuser_id_token},
        )
        assert res.status_code == 404

    def test_func_node_get_with_id_nonuser_token(self, nonuser_id_token):
        res = fa_client.get(
            url="/api/nodes/hogehogehoge",
            headers={"Authorization": nonuser_id_token},
        )
        assert res.status_code == 404


class TestSuccessPut:
    def test_func_nodes_put_normal(self, id_token):
        # First, get the current text
        res = fa_client.get(
            url=f"/api/nodes/{ROOT_NODE_ID}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200
        before = res.json()["text"]

        # Test
        text = """
            # MarkdownEditor

            ## CICD Status
            [![CICD Workflow](https://github.com/cloudjex/markdowneditor/actions/workflows/cicd.yaml/badge.svg)](https://github.com/cloudjex/markdowneditor/actions/workflows/cicd.yaml)

            ## Sample Application URL
            https://www.cloudjex.com
        """
        text = textwrap.dedent(text).strip("\n")

        res = fa_client.put(
            url=f"/api/nodes/{ROOT_NODE_ID}",
            headers={"Authorization": id_token},
            json={
                "text": f"{text}",
            }
        )
        assert res.status_code == 200

        body = res.json()
        assert type(body) is dict
        assert body["text"] == text
        assert type(body["id"]) is str
        assert type(body["email"]) is str

        # Restore previous text
        res = fa_client.put(
            url=f"/api/nodes/{ROOT_NODE_ID}",
            headers={"Authorization": id_token},
            json={
                "text": f"{before}",
            }
        )
        assert res.status_code == 200

    def test_func_nodes_put_empty_text(self, id_token):
        # First, get the current text
        res = fa_client.get(
            url=f"/api/nodes/{ROOT_NODE_ID}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200
        before = res.json()["text"]

        # Test
        res = fa_client.put(
            url=f"/api/nodes/{ROOT_NODE_ID}",
            headers={"Authorization": id_token},
            json={
                "text": "",
            }
        )
        assert res.status_code == 200

        body = res.json()
        assert type(body) is dict
        assert body["text"] == ""
        assert type(body["id"]) is str
        assert type(body["email"]) is str

        # Restore previous text
        res = fa_client.put(
            url=f"/api/nodes/{ROOT_NODE_ID}",
            headers={"Authorization": id_token},
            json={
                "text": f"{before}",
            }
        )
        assert res.status_code == 200


class TestFailPut:
    def test_func_node_put_invalid_token(self, invalid_id_token):
        res = fa_client.put(
            url="/api/nodes/test",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_func_nodes_put_no_exist_node(self, id_token):
        res = fa_client.put(
            url="/api/nodes/non_existing_id",
            headers={"Authorization": id_token},
            json={
                "text": "",
            }
        )
        assert res.status_code == 404
