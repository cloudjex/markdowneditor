import uuid

from funcs.entities.node import Node
from funcs.entities.tree import Tree
from funcs.utilities import errors
from funcs.utilities.dynamodb_client import DynamoDBClient
from funcs.utilities.tree_handler import TreeHandler


def post(email: str, parent_id: str, label: str) -> dict:
    db_client = DynamoDBClient()

    tree_info = db_client.get_tree_info(email)
    if not tree_info:
        raise errors.NotFoundError("func_tree_node.not_found")

    insert_id = str(uuid.uuid4())
    insert_node = {
        "node_id": insert_id,
        "label": label,
        "children": [],
    }

    tree_handler = TreeHandler(tree_info.tree.to_dict())
    tree_handler.insert_node(parent_id, insert_node)
    new_tree = tree_handler.sort_tree()

    tree_info.tree = Tree(
        new_tree["node_id"],
        new_tree["label"],
        new_tree["children"]
    )

    new_node = Node(email, insert_id, "")

    db_client.put_tree_info(tree_info)
    db_client.put_node(new_node)

    return new_tree


def delete(email: str, node_id: str) -> dict:
    db_client = DynamoDBClient()

    tree_info = db_client.get_tree_info(email)
    if not tree_info:
        raise errors.NotFoundError("func_tree_node.not_found")

    tree_handler = TreeHandler(tree_info.tree.to_dict())

    node = tree_handler.get_node(node_id)
    if node["node_id"] == tree_info.tree.node_id:
        raise errors.ForbiddenError("func_tree_node.cant_delete")

    del_targets = tree_handler.get_children_ids(node_id)
    del_targets.append(node_id)

    tree_handler.del_node(node_id)
    new_tree = tree_handler.sort_tree()

    tree_info.tree = Tree(
        new_tree["node_id"],
        new_tree["label"],
        new_tree["children"]
    )

    for del_id in del_targets:
        db_client.delete_node(Node(email, del_id, ""))
    db_client.put_tree_info(tree_info)

    return new_tree
