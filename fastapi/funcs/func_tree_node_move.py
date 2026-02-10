from funcs.utilities import errors
from funcs.utilities.dynamodb_client import DynamoDBClient
from funcs.utilities.tree_handler import TreeHandler


def node_move(user_group: str, node_id: str, parent_id: str) -> dict:
    db_client = DynamoDBClient()

    tree_info = db_client.get_tree_info(user_group)

    root_node_id = tree_info.tree.node_id
    if node_id == root_node_id:
        raise errors.ForbiddenError

    tree_handler = TreeHandler(tree_info.tree)
    tree_handler.move_node(parent_id, node_id)
    new_tree = tree_handler.sort_tree()
    tree_info.tree = new_tree

    db_client.put_tree_info(tree_info)
    return new_tree.model_dump()
