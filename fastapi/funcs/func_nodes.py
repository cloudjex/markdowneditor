from funcs.utilities import errors
from funcs.utilities.dynamodb_client import DynamoDBClient


def get(email: str, node_id: str | None) -> dict:
    db_client = DynamoDBClient()
    if node_id:
        item = db_client.get_node(email, node_id)
        if not item:
            raise errors.NotFoundError("func_nodes.not_found")
        ret = item.to_dict()

    else:
        items = db_client.get_nodes(email)
        if not items:
            raise errors.NotFoundError("func_nodes.not_found")

        json_items = [i.to_dict() for i in items]
        ret = {"nodes": json_items}

    return ret


def put(email: str, node_id: str, text: str) -> dict:
    db_client = DynamoDBClient()
    node = db_client.get_node(email, node_id)
    if not node:
        raise errors.NotFoundError("func_nodes.not_found")

    node.text = text
    db_client.put_node(node)

    return node.to_dict()
