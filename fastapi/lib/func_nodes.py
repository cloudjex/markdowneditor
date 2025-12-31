from lib import config
from lib.utilities.dynamodb_client import DynamoDBClient
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
        elif method == "PUT":
            res = put(params)
        return ResponseHandler().response(body=res, status_code=200)

    except Exception as e:
        return ResponseHandler().error_response(e)

def get(params) -> dict:
    try:
        email: str = params["email"]
        query_params: dict = params["query_params"]
        node_id: str = query_params.get("node_id")

        db_client = DynamoDBClient(config.NODES_TABLE_NAME)
        if node_id:
            item = db_client.get_node(email, node_id)
            if not item:
                raise Exception({
                    "status_code": 404,
                    "exception": "Not Found",
                    "error_code": "func_nodes.not_found",
                })
            ret = {"node": item}

        else:
            items = db_client.get_nodes(email)
            if not items:
                raise Exception({
                    "status_code": 404,
                    "exception": "Not Found",
                    "error_code": "func_nodes.not_found",
                })
            ret = {"nodes": items}

        return ret

    except Exception as e:
        raise e


def put(params) -> dict:
    try:
        email: str = params["email"]
        body: dict = params["body"]

        node_id = body.get("node_id")
        text: str = body.get("text")

        if not node_id or text is None:
            raise Exception({
                "status_code": 400,
                "exception": "Bad Request",
                "error_code": "func_nodes.missing_parameters",
            })

        db_client = DynamoDBClient(config.NODES_TABLE_NAME)
        node = db_client.get_node(email, node_id)
        if not node:
            raise Exception({
                "status_code": 404,
                "exception": "Not Found",
                "error_code": "func_nodes.not_found",
            })

        db_client.put_node(email, node_id, text)

        return {
            "node": {
                "email": email,
                "node_id": node_id,
                "text": text,
            }
        }

    except Exception as e:
        raise e
