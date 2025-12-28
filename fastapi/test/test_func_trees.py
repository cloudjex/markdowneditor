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
