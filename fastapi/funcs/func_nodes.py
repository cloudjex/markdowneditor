from funcs.utilities import errors
from funcs.utilities.dynamodb_client import DynamoDBClient


def get_node(user_group: str, node_id: str) -> dict:
    db_client = DynamoDBClient()

    item = db_client.get_node(user_group, node_id)
    if not item:
        raise errors.NotFoundError
    ret = item.model_dump()

    return ret


def get_nodes(user_group: str) -> dict:
    db_client = DynamoDBClient()

    items = db_client.get_nodes(user_group)
    return [i.model_dump() for i in items]


def put_node(user_group: str, node_id: str, text: str) -> dict:
    db_client = DynamoDBClient()
    node = db_client.get_node(user_group, node_id)
    if not node:
        raise errors.NotFoundError

    node.text = text
    db_client.put_node(node)

    return node.model_dump()
