from lib.utilities import exceptions
from lib.utilities.dynamodb_client import NodeTableClient, TreeTableClient
from lib.utilities.jwt_client import JwtClient
from lib.utilities.response_handler import ResponseHandler
from lib.utilities.tree_handler import TreeHander


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
    try:
        email: str = params["email"]
        body: dict = params["body"]
        node_id: str = body.get("node_id")

        if not node_id:
            raise exceptions.BadRequestError({
                "error_code": "func_trees_operate.missing_parameters",
            })

        label = node_id.split("/")[-1]
        if not label:
            raise exceptions.BadRequestError({
                "error_code": "func_trees_operate.invalid_node_id",
            })

        tree = get_tree(email)

        tree_hander = TreeHander()
        parent_node = tree_hander.get_parent_node(node_id, tree)
        if not parent_node:
            raise exceptions.NotFoundError({
                "error_code": "func_trees_operate.not_found",
            })

        new_node = {
            "id": node_id,
            "label": label,
            "children": [],
        }
        children: list = parent_node.get("children")

        if any(child["id"] == node_id for child in children):
            raise exceptions.ConflictError({
                "error_code": "func_trees_operate.duplicate_node",
            })

        children.append(new_node)

        parent_node["children"] = children
        tree = tree_hander.sort_tree(tree)

        tree_db_client = TreeTableClient()
        node_db_client = NodeTableClient()

        tree_db_client.put_tree(email, tree)
        node_db_client.put_node(email, node_id, "")
        return {"tree": tree}

    except Exception as e:
        raise e


def delete(params) -> dict:
    try:
        email: str = params["email"]
        query_params: dict = params["query_params"]
        node_id: str = query_params.get("node_id")

        if not node_id:
            raise exceptions.BadRequestError({
                "error_code": "func_trees_operate.missing_parameters",
            })

        tree = get_tree(email)

        tree_hander = TreeHander()
        parent_node = tree_hander.get_parent_node(node_id, tree)
        if not parent_node:
            raise exceptions.NotFoundError({
                "error_code": "func_trees_operate.not_found",
            })

        children: list = parent_node.get("children")
        delete_node = tree_hander.get_node(node_id, tree)

        if not delete_node:
            raise exceptions.NotFoundError({
                "error_code": "func_trees_operate.not_found",
            })

        children_ids = tree_hander.get_children_ids(node_id, tree)
        target_and_following: list = [node_id] + children_ids
        children.remove(delete_node)

        tree = tree_hander.sort_tree(tree)

        tree_db_client = TreeTableClient()
        node_db_client = NodeTableClient()

        tree_db_client.put_tree(email, tree)
        for del_id in target_and_following:
            node_db_client.delete_node(email, del_id)

        return {"tree": tree}

    except Exception as e:
        raise e


def get_tree(email: str) -> dict:
    db_client = TreeTableClient()
    tree_info = db_client.get_tree(email)
    if not tree_info:
        raise exceptions.NotFoundError({
            "error_code": "func_trees_operate.not_found",
        })

    tree = tree_info.get("tree")
    return tree
