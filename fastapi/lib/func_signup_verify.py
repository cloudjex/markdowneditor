from lib.utilities import errors
from lib.utilities.dynamodb_client import DynamoDBClient
from lib.utilities.response_handler import ResponseHandler


def main(params: dict) -> dict:
    try:
        body: dict = params["body"]
        email: str = body.get("email")
        otp: str = body.get("otp")

        if not email or not otp:
            raise errors.BadRequestError("func_signup_verify.missing_params")

        db_client = DynamoDBClient()
        user = db_client.get_user(email)
        if not user:
            raise errors.NotFoundError("func_signup_verify.not_found")

        options: dict = user["options"]
        invalid: bool = (options.get("enabled")) or (options.get("otp") != otp)
        if invalid:
            raise errors.UnauthorizedError("func_signup_verify.invalid_otp")

        options.pop("otp")
        options["enabled"] = True

        initial_tree = {
            "id": "/Nodes",
            "label": "Nodes",
            "children": [],
        }
        initial_node_id = "/Nodes"

        db_client.put_user(email, user["password"], options)
        db_client.put_tree(email, initial_tree)
        db_client.put_node(email, initial_node_id, "")

        res = {
            "result": "success"
        }
        return ResponseHandler().response(body=res, status_code=200)

    except Exception as e:
        return ResponseHandler().error_response(e)
