from lib.utilities import errors
from lib.utilities.dynamodb_client import DynamoDBClient
from lib.utilities.jwt_client import JwtClient
from lib.utilities.response_handler import ResponseHandler
from lib.utilities.tree_handler import TreeHandler


def main(params: dict) -> dict:
    try:
        headers: dict = params["headers"]
        id_token: str = headers.get("authorization")

        decoded = JwtClient().verify_id_token(id_token)
        params.update({"email": decoded["email"]})

        method: str = params["method"]
        if method == "PUT":
            res = put(params)
        elif method == "DELETE":
            res = delete(params)

        return ResponseHandler().response(body=res, status_code=200)

    except Exception as e:
        return ResponseHandler().error_response(e)


def put(params) -> dict:
    email: str = params["email"]
    body: dict = params["body"]
    node_id: str = body.get("node_id")

    if not node_id:
        raise errors.BadRequestError("func_trees_operate.missing_params")

    label = node_id.split("/")[-1]
    if not label:
        raise errors.BadRequestError("func_trees_operate.invalid_params")

    new_node = {
        "id": node_id,
        "label": label,
        "children": [],
    }

    db_client = DynamoDBClient()

    tree = db_client.get_tree(email)
    if not tree:
        raise errors.NotFoundError("func_trees_operate.not_found")

    tree_handler = TreeHandler(tree.tree.json)

    tree_handler.insert_node(new_node)
    new_tree = tree_handler.sort_tree()

    db_client.put_tree(email, new_tree)
    db_client.put_node(email, node_id, "")
    return {"tree": new_tree}


def delete(params) -> dict:
    email: str = params["email"]
    query_params: dict = params["query_params"]
    node_id: str = query_params.get("node_id")

    if not node_id:
        raise errors.BadRequestError("func_trees_operate.missing_params")

    if node_id == "/Nodes":
        raise errors.ForbiddenError("func_trees_operate.cant_delete")

    db_client = DynamoDBClient()

    tree = db_client.get_tree(email)
    if not tree:
        raise errors.NotFoundError("func_trees_operate.not_found")

    tree_handler = TreeHandler(tree.tree.json)

    children_ids = tree_handler.get_children_ids(node_id)
    tree_handler.delete_node(node_id)
    new_tree = tree_handler.sort_tree()

    for del_id in children_ids:
        db_client.delete_node(email, del_id)

    db_client.delete_node(email, node_id)
    db_client.put_tree(email, new_tree)

    return {"tree": new_tree}
