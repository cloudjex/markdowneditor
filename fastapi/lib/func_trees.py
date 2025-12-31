from lib.utilities import exceptions
from lib.utilities.dynamodb_client import TreeTableClient
from lib.utilities.jwt_client import JwtClient
from lib.utilities.response_handler import ResponseHandler


def main(params: dict) -> dict:
    try:
        headers: dict = params["headers"]
        id_token: str = headers.get("authorization")

        decoded = JwtClient().verify_id_token(id_token)
        params.update({"email": decoded["email"]})

        method: str = params["method"]
        if method == "GET":
            res = get(params)

        return ResponseHandler().response(body=res, status_code=200)

    except Exception as e:
        return ResponseHandler().error_response(e)

def get(params) -> dict:
    try:
        email: str = params["email"]

        db_client = TreeTableClient()
        tree_info = db_client.get_tree(email=email)
        if not tree_info:
            raise exceptions.NotFoundError({
                "error_code": "func_trees.not_found",
            })

        res = {
            "tree": tree_info["tree"],
        }

        return res

    except Exception as e:
        raise e
