import traceback

from lib.utilities.errors import BaseExceptionClass, InternalServerError


class ResponseHandler:
    def response(self, status_code: int, body: dict) -> dict:
        return {
            "headers": {"Content-Type": "application/json"},
            "status_code": status_code,
            "body": body,
        }

    def error_response(self, e: Exception) -> dict:
        if not isinstance(e, BaseExceptionClass):
            # Unexpected error (internal error)
            print(traceback.format_exc())
            e = InternalServerError("internal_server_erorr")

        return self.response(
            status_code=e.status_code,
            body={
                "error_code": e.error_code,
                "exception": e.exception,
            },
        )
