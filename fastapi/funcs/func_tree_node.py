import uuid

from funcs.utilities import errors
from funcs.utilities.dynamodb_client import DynamoDBClient
from funcs.utilities.tree_handler import TreeHandler
from models.node import Node
from models.tree import Tree


def post_node(user_group: str, parent_id: str, label: str) -> dict:
    db_client = DynamoDBClient()

    tree_info = db_client.get_tree_info(user_group)

    insert_id = str(uuid.uuid4())
    insert_node = Tree(node_id=insert_id, label=label, children=[])

    tree_handler = TreeHandler(tree_info.tree)
    tree_handler.insert_node(parent_id, insert_node)
    new_tree = tree_handler.sort_tree()
    tree_info.tree = new_tree

    new_node = Node(user_group=user_group, node_id=insert_id, text="")

    db_client.put_tree_info(tree_info)
    db_client.put_node(new_node)

    return new_tree.model_dump()


def delete_node(user_group: str, node_id: str) -> dict:
    db_client = DynamoDBClient()

    tree_info = db_client.get_tree_info(user_group)

    tree_handler = TreeHandler(tree_info.tree)

    node = tree_handler.recursive_get(node_id)
    if not node:
        raise errors.NotFoundError
    if node.node_id == tree_info.tree.node_id:
        raise errors.ForbiddenError

    del_targets = tree_handler.get_children_ids(node_id)
    del_targets.append(node_id)

    tree_handler.del_node(node_id)
    new_tree = tree_handler.sort_tree()
    tree_info.tree = new_tree

    for del_id in del_targets:
        n = Node(user_group=user_group, node_id=del_id, text="")
        db_client.delete_node(n)
    db_client.put_tree_info(tree_info)

    return new_tree.model_dump()
