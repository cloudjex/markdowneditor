from lib.utilities import exceptions
from lib.utilities.response_handler import ResponseHandler


def main(params: dict) -> dict:
    try:
        headers: dict = params["headers"]
        id_token: str = headers.get("authorization")

        if not id_token:
            raise exceptions.BadRequestError({
                "error_code": "func_logout.missing_parameters",
            })

        res = {
            "result": "success"
        }

        return ResponseHandler().response(body=res, status_code=200)

    except Exception as e:
        return ResponseHandler().error_response(e)
