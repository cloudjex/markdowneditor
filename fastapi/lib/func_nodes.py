from lib.utilities import errors
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
    email: str = params["email"]
    query_params: dict = params["query_params"]
    id: str = query_params.get("id")

    db_client = DynamoDBClient()
    if id:
        item = db_client.get_node(email, id)
        if not item:
            raise errors.NotFoundError("func_nodes.not_found")
        ret = {"node": item.to_dict()}

    else:
        items = db_client.get_nodes(email)
        if not items:
            raise errors.NotFoundError("func_nodes.not_found")

        json_items = [i.to_dict() for i in items]
        ret = {"nodes": json_items}

    return ret


def put(params) -> dict:
    email: str = params["email"]
    body: dict = params["body"]

    id = body.get("id")
    text: str = body.get("text")

    if not id or text is None:
        raise errors.BadRequestError("func_nodes.missing_params")

    db_client = DynamoDBClient()
    node = db_client.get_node(email, id)
    if not node:
        raise errors.NotFoundError("func_nodes.not_found")

    node.text = text
    db_client.put_node(node)

    return {
        "node": node.to_dict()
    }
