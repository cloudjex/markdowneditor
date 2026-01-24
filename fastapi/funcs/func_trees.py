from funcs.utilities import errors
from funcs.utilities.dynamodb_client import DynamoDBClient


def get(email: str) -> dict:
    db_client = DynamoDBClient()
    tree = db_client.get_tree(email=email)
    if not tree:
        raise errors.NotFoundError("func_trees.not_found")

    res = {
        "node_tree": tree.node_tree.to_dict(),
    }

    return res
