import uuid

from funcs.entities.node import Node
from funcs.entities.tree import NodeTree
from funcs.utilities import errors
from funcs.utilities.dynamodb_client import DynamoDBClient
from funcs.utilities.tree_handler import TreeHandler


def post(email: str, parent_id: str, label: str) -> dict:
    db_client = DynamoDBClient()

    tree = db_client.get_tree(email)
    if not tree:
        raise errors.NotFoundError("func_trees_operate.not_found")

    insert_id = str(uuid.uuid4())
    insert_node = {
        "id": insert_id,
        "label": label,
        "children": [],
    }

    tree_handler = TreeHandler(tree.node_tree.to_dict())
    tree_handler.insert_node(parent_id, insert_node)
    new_node_tree = tree_handler.sort_tree()

    tree.node_tree = NodeTree(
        new_node_tree["id"],
        new_node_tree["label"],
        new_node_tree["children"]
    )

    new_node = Node(email, insert_id, "")

    db_client.put_tree(tree)
    db_client.put_node(new_node)

    return {
        "node_tree": new_node_tree,
        "id": insert_id,
    }


def delete(email: str, node_id: str) -> dict:
    db_client = DynamoDBClient()

    tree = db_client.get_tree(email)
    if not tree:
        raise errors.NotFoundError("func_trees_operate.not_found")

    tree_handler = TreeHandler(tree.node_tree.to_dict())

    node = tree_handler.get_node(node_id)
    if node["label"] == "Nodes":
        raise errors.ForbiddenError("func_trees_operate.cant_delete")

    del_targets = tree_handler.get_children_ids(node_id)
    del_targets.append(node_id)

    tree_handler.del_node(node_id)
    new_node_tree = tree_handler.sort_tree()

    tree.node_tree = NodeTree(
        new_node_tree["id"],
        new_node_tree["label"],
        new_node_tree["children"]
    )

    for del_id in del_targets:
        db_client.delete_node(Node(email, del_id, ""))
    db_client.put_tree(tree)

    return {
        "node_tree": new_node_tree,
        "id": node_id,
    }
