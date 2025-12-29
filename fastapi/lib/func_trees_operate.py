from lib.utilities import dynamodbs, jwt, response, trees


def main(params: dict) -> dict:
    try:
        headers: dict = params["headers"]
        id_token: str = headers.get("authorization")

        decoded = jwt.verify_id_token(id_token)
        params.update({"email": decoded["email"]})

        method: str = params["method"]
        if method == "PUT":
            res = put(params)
        elif method == "DELETE":
            res = delete(params)

        return response.response_handler(body=res, status_code=200)

    except Exception as e:
        return response.error_handler(e)


def put(params) -> dict:
    try:
        email: str = params["email"]
        body: dict = params["body"]
        node_id: str = body.get("node_id")

        if not node_id:
            raise Exception({
                "status_code": 400,
                "exception": "Bad Request",
                "error_code": "func_trees_operate.missing_parameters",
            })

        label = node_id.split("/")[-1]
        if not label:
            raise Exception({
                "status_code": 400,
                "exception": "Bad Request",
                "error_code": "func_trees_operate.invalid_node_id",
            })

        tree = get_tree(email)
        parent_node = get_parent_node(node_id, tree)

        new_node = {
            "id": node_id,
            "label": label,
            "children": [],
        }
        children: list = parent_node.get("children")

        if any(child["id"] == node_id for child in children):
            raise Exception({
                "status_code": 409,
                "exception": "Conflict",
                "error_code": "func_trees_operate.duplicate_node",
            })

        children.append(new_node)

        parent_node["children"] = children
        tree = trees.sort_tree(tree)

        dynamodbs.update_tree(email, tree)
        dynamodbs.post_node(email, node_id, "")

        return {"tree": tree}

    except Exception as e:
        raise e


def delete(params) -> dict:
    try:
        email: str = params["email"]
        query_params: dict = params["query_params"]
        node_id: str = query_params.get("node_id")

        if not node_id:
            raise Exception({
                "status_code": 400,
                "exception": "Bad Request",
                "error_code": "func_trees_operate.missing_parameters",
            })

        tree = get_tree(email)
        parent_node = get_parent_node(node_id, tree)

        children: list = parent_node.get("children")
        delete_node = trees.find_node(node_id, tree)

        if not delete_node:
            raise Exception({
                "status_code": 404,
                "exception": "Not Found",
                "error_code": "func_trees_operate.not_found",
            })

        children_ids = trees.find_children_ids(node_id, tree)
        target_and_following: list = [node_id] + children_ids
        children.remove(delete_node)

        tree = trees.sort_tree(tree)

        dynamodbs.update_tree(email, tree)
        for del_id in target_and_following:
            dynamodbs.delete_node(email, del_id)

        return {"tree": tree}

    except Exception as e:
        raise e


def get_tree(email: str) -> dict:
    tree_info = dynamodbs.get_tree(email)
    if not tree_info:
        raise Exception({
            "status_code": 404,
            "exception": "Not Found",
            "error_code": "func_trees_operate.not_found",
        })

    tree = tree_info.get("tree")
    return tree


def get_parent_node(node_id: str, tree: dict) -> dict:
    parent_node_ids = node_id.split("/")
    parent_node_id = "/" + "/".join(parent_node_ids[1: -1])

    parent_node = trees.find_node(parent_node_id, tree)
    if not parent_node:
        raise Exception({
            "status_code": 404,
            "exception": "Not Found",
            "error_code": "func_trees_operate.parent_not_found",
        })
    return parent_node
