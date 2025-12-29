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
        elif method == "PUT":
            res = put(params)
        return response.response_handler(body=res, status_code=200)

    except Exception as e:
        return response.error_handler(e)


def get(params) -> dict:
    try:
        email: str = params["email"]
        query_params: dict = params["query_params"]
        node_id: str = query_params.get("node_id")

        if node_id:
            item = dynamodbs.get_node(email, node_id)
            if not item:
                raise Exception({
                    "status_code": 404,
                    "exception": "Not Found",
                    "error_code": "func_nodes.not_found",
                })
            ret = {"node": item}

        else:
            items = dynamodbs.get_nodes(email)
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

        node = dynamodbs.get_node(email, node_id)
        if not node:
            raise Exception({
                "status_code": 404,
                "exception": "Not Found",
                "error_code": "func_nodes.not_found",
            })

        dynamodbs.post_node(email, node_id, text)

        return {
            "node": {
                "email": email,
                "node_id": node_id,
                "text": text,
            }
        }

    except Exception as e:
        raise e
