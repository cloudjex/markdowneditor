from lib.utilities import dynamodbs, utils


def main(params: dict) -> dict:
    try:
        headers: dict = params["headers"]
        id_token: str = headers.get("authorization")

        decoded = utils.verify_id_token(id_token)
        params.update({"email": decoded["email"]})

        method: str = params["method"]
        if method == "GET":
            res = get(params)
        elif method == "PUT":
            res = put(params)

        return utils.response_handler(body=res, status_code=200)

    except Exception as e:
        return utils.error_handler(e)


def get(params) -> dict:
    try:
        email: str = params["email"]

        tree_info = dynamodbs.get_tree(email=email)
        if not tree_info:
            raise Exception({
                "status_code": 404,
                "exception": "Not Found",
                "error_code": "func_trees.not_found",
            })

        tree_info["tree"] = sort_tree(tree_info["tree"])

        res = {
            "tree": tree_info["tree"],
        }

        return res

    except Exception as e:
        raise e


def put(params) -> dict:
    try:
        email: str = params["email"]
        body: dict = params.get("body")
        tree: dict = body.get("tree")

        if not tree:
            raise Exception({
                "status_code": 400,
                "exception": "Bad Request",
                "error_code": "func_trees.missing_parameters",
            })

        tree_info = dynamodbs.get_tree(email=email)
        if not tree_info:
            raise Exception({
                "status_code": 404,
                "exception": "Not Found",
                "error_code": "func_trees.not_found",
            })

        tree = sort_tree(tree)

        dynamodbs.update_tree(email=email, tree=tree)
        tree_info = dynamodbs.get_tree(email=email)

        res = {
            "tree": tree_info["tree"],
        }

        return res

    except Exception as e:
        raise e


def sort_tree(tree: dict) -> dict:
    """
    Sort tree recursively:
    - Nodes with children come first
    - Then nodes without children (files)
    - Within each group, sort by id alphabetically
    """
    if not tree or not isinstance(tree, dict):
        return tree

    def sort_key(child: dict) -> tuple[bool, str]:
        node_id: str = child.get("id", "")
        # children が存在すればフォルダ、なければファイル
        is_file = "children" not in child or not child.get("children")
        return (is_file, node_id)

    children = tree.get("children")
    if isinstance(children, list):
        # 子ノードをソート
        children.sort(key=sort_key)
        # 再帰的にソート
        for child in children:
            sort_tree(child)
        tree["children"] = children

    return tree
