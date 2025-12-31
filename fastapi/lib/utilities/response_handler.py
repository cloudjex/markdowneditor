import traceback

from lib.utilities.exceptions import BaseExceptions


class ResponseHandler:
    def __init__(self):
        pass

    def error_response(self, e: Exception) -> dict:
        try:
            args = e.args[0]

            if isinstance(e, BaseExceptions):
                status_code = e.status_code
                body = {
                    "error_code": args.get("error_code"),
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

        except Exception as e:
            raise e


    def response(self, status_code: int, body: dict) -> dict:
        try:
            return {
                "headers": {"Content-Type": "application/json"},
                "status_code": status_code,
                "body": body,
            }

        except Exception as e:
            raise e
