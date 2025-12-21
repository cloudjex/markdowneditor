from lib import func_trees

from .conftest import logger


class TestSuccessGET:
    def test_func_trees_get_normal(self, id_token):
        params = {
            "method": "GET",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {},
            "query_params": {},
        }
        response = func_trees.main(params)
        logger(response)
        assert response["status_code"] == 200
        assert response["body"].get("tree") is not None


class TestFailGet:
    def test_func_trees_get_no_token(self):
        params = {
            "method": "GET",
            "headers": {
                "content-type": "application/json",
                "authorization": ""
            },
            "body": {},
            "query_params": {},
        }
        response = func_trees.main(params)
        logger(response)
        assert response["status_code"] == 401

    def test_func_trees_get_nonuser_token(self, nonuser_id_token):
        params = {
            "method": "GET",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {nonuser_id_token}"
            },
            "body": {},
            "query_params": {},
        }
        response = func_trees.main(params)
        logger(response)
        assert response["status_code"] == 404

    def test_func_trees_get_invalid_token(self, invalid_id_token):
        params = {
            "method": "GET",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {invalid_id_token}"
            },
            "body": {},
            "query_params": {},
        }
        response = func_trees.main(params)
        logger(response)
        assert response["status_code"] == 401


class TestSuccessPut:
    def test_func_trees_put_normal(self, id_token):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {
                "tree":  {
                    "id": '/Folder',
                    "label": 'Folder',
                    "children": [
                        {"id": '/Folder/テスト1', "label": 'テスト1'},
                        {"id": '/Folder/テスト2', "label": 'テスト2'},
                        {
                            "id": '/Folder/仕事',
                            "label": '仕事',
                            "children": [
                                {"id": '/Folder/仕事/page1',
                                 "label": 'page1'},
                                {"id": '/Folder/仕事/page2',
                                 "label": 'page2'},
                            ]
                        },
                        {
                            "id": '/Folder/日記',
                            "label": '日記',
                            "children": [
                                {"id": '/Folder/日記/page1', "label": 'page1'},
                                {"id": '/Folder/日記/page2', "label": 'page2'},
                            ]
                        },
                        {
                            "id": '/Folder/勉強',
                            "label": '勉強',
                            "children": [
                                {"id": '/Folder/勉強/page1', "label": 'page1'},
                                {"id": '/Folder/勉強/page2', "label": 'page2'},
                            ]
                        }
                    ]
                }
            },
            "query_params": {},
        }
        response = func_trees.main(params)
        logger(response)
        assert response["status_code"] == 200
        assert response["body"].get("tree") == params["body"]["tree"]


class TestFailPut:
    def test_func_trees_put_no_token(self):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": ""
            },
            "body": {},
            "query_params": {},
        }
        response = func_trees.main(params)
        logger(response)
        assert response["status_code"] == 401

    def test_func_trees_put_invalid_token(self, invalid_id_token):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {invalid_id_token}"
            },
            "body": {},
            "query_params": {},
        }
        response = func_trees.main(params)
        logger(response)
        assert response["status_code"] == 401

    def test_func_trees_put_no_params(self, id_token):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {id_token}"
            },
            "body": {
                "tree":  {}
            },
            "query_params": {},
        }
        response = func_trees.main(params)
        logger(response)
        assert response["status_code"] == 400

    def test_func_trees_put_nouser_token(self, nonuser_id_token):
        params = {
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "authorization": f"Bearer {nonuser_id_token}"
            },
            "body": {
                "tree": {
                    "id": '/Folder',
                    "label": 'Folder',
                }
            },
            "query_params": {},
        }
        response = func_trees.main(params)
        logger(response)
        assert response["status_code"] == 404
