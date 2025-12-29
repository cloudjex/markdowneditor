from lib.utilities import dynamodbs, jwt, response


def main(params: dict) -> dict:
    try:
        headers: dict = params["headers"]
        id_token: str = headers.get("authorization")

        decoded = jwt.verify_id_token(id_token)
        params.update({"email": decoded["email"]})

        method: str = params["method"]
        if method == "GET":
            res = get(params)

        return response.response_handler(body=res, status_code=200)

    except Exception as e:
        return response.error_handler(e)


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

        res = {
            "tree": tree_info["tree"],
        }

        return res

    except Exception as e:
        raise e
