import traceback

from lib.utilities.errors import BaseExceptionClass


class ResponseHandler:
    def __init__(self):
        pass

    def error_response(self, e: Exception) -> dict:
        if isinstance(e, BaseExceptionClass):
            status_code = e.status_code
            error_code = e.args[0]
            body = {
                "error_code": error_code,
                "exception": e.exception,
            }
        else:
            # Unexpected error (internal error)
            status_code = 500
            body = {
                "error_code": traceback.format_exc(),
                "exception": "INTERNAL_SERVER_ERROR",
            }

        return self.response(status_code, body)

    def response(self, status_code: int, body: dict) -> dict:
        return {
            "headers": {"Content-Type": "application/json"},
            "status_code": status_code,
            "body": body,
        }
