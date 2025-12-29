import traceback


def error_handler(e: Exception) -> dict:
    try:
        args = e.args[0]

        status_code = None
        params = {}

        if type(args) is dict and args.get("status_code"):
            # Expected Errors
            status_code = args["status_code"]
            params.update({
                "exception": args.get("exception"),
                "error_code": args.get("error_code"),
            })

        else:
            # Unexpected error (internal error)
            status_code = 500
            traceback_str = traceback.format_exc()
            params.update({"exception": traceback_str})

        return response_handler(body=params, status_code=status_code)

    except Exception as e:
        raise e


def response_handler(body: dict, status_code: int = 200) -> dict:
    try:
        return {
            "headers": {"Content-Type": "application/json"},
            "status_code": status_code,
            "body": body,
        }

    except Exception as e:
        raise e
