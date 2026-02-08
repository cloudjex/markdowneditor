from funcs.utilities import errors
from funcs.utilities.dynamodb_client import DynamoDBClient


def get_node(user_group: str, node_id: str) -> dict:
    db_client = DynamoDBClient()

    item = db_client.get_node(user_group, node_id)
    if not item:
        raise errors.NotFoundError("func_nodes.not_found")
    ret = item.to_dict()

    return ret


def get_nodes(user_group: str) -> dict:
    db_client = DynamoDBClient()

    items = db_client.get_nodes(user_group)
    if not items:
        raise errors.NotFoundError("func_nodes.not_found")

    json_items = [i.to_dict() for i in items]
    return {"nodes": json_items}


def put_node(user_group: str, node_id: str, text: str) -> dict:
    db_client = DynamoDBClient()
    node = db_client.get_node(user_group, node_id)
    if not node:
        raise errors.NotFoundError("func_nodes.not_found")

    node.text = text
    db_client.put_node(node)

    return node.to_dict()
