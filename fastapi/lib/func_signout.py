from lib.utilities import errors
from lib.utilities.response_handler import ResponseHandler


def main(params: dict) -> dict:
    try:
        headers: dict = params["headers"]
        id_token: str = headers.get("authorization")

        if not id_token:
            raise errors.BadRequestError("func_logout.missing_params")

        res = {
            "result": "success"
        }

        return ResponseHandler().response(body=res, status_code=200)

    except Exception as e:
        return ResponseHandler().error_response(e)
