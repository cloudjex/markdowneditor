import uuid

from funcs.entities.node import Node
from funcs.entities.tree import TreeInfo
from funcs.utilities import errors
from funcs.utilities.dynamodb_client import DynamoDBClient


def post(email: str, otp: str) -> dict:
    db_client = DynamoDBClient()
    user = db_client.get_user(email)
    if not user:
        raise errors.NotFoundError("func_signup_verify.not_found")

    invalid: bool = (user.options.enabled) or (user.options.otp != otp)
    if invalid:
        raise errors.UnauthorizedError("func_signup_verify.invalid_otp")

    user.options.otp = ""
    user.options.enabled = True

    initial_id = str(uuid.uuid4())
    initial_tree = {
        "id": initial_id,
        "label": "Nodes",
        "children": [],
    }
    initial_tree_info = TreeInfo(user.email, initial_tree)
    initial_node = Node(user.email, initial_id, "")

    db_client.put_user(user)
    db_client.put_tree_info(initial_tree_info)
    db_client.put_node(initial_node)

    return {"result": "success"}
