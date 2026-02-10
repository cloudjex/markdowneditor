from funcs.utilities.dynamodb_client import DynamoDBClient
from funcs.utilities.tree_handler import TreeHandler


def update_node_label(user_group: str, node_id: str, label: str) -> dict:
    db_client = DynamoDBClient()

    tree_info = db_client.get_tree_info(user_group)

    tree_handler = TreeHandler(tree_info.tree)
    tree_handler.update_node_label(node_id, label)
    new_tree = tree_handler.sort_tree()
    tree_info.tree = new_tree

    db_client.put_tree_info(tree_info)
    return new_tree.model_dump()
