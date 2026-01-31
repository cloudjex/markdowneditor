from funcs.entities.tree import Tree
from funcs.utilities import errors
from funcs.utilities.dynamodb_client import DynamoDBClient
from funcs.utilities.tree_handler import TreeHandler


def put(email: str, id: str, parent_id: str) -> dict:
    db_client = DynamoDBClient()

    tree_info = db_client.get_tree_info(email)
    if not tree_info:
        raise errors.NotFoundError("func_tree_node.not_found")

    tree_handler = TreeHandler(tree_info.tree.to_dict())
    tree_handler.move_node(parent_id, id)
    new_tree = tree_handler.sort_tree()

    tree_info.tree = Tree(
        new_tree["id"],
        new_tree["label"],
        new_tree["children"]
    )

    db_client.put_tree_info(tree_info)
    return new_tree
