from funcs.utilities import errors
from funcs.utilities.dynamodb_client import DynamoDBClient


def get(email: str) -> dict:
    db_client = DynamoDBClient()
    tree_info = db_client.get_tree_info(email=email)
    if not tree_info:
        raise errors.NotFoundError("func_tree.not_found")

    return tree_info.tree.to_dict()
