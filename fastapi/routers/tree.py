import uuid

import config
from fastapi import APIRouter, Depends, Path
from models import req
from models.jwt import JwtClaim
from models.node import Node
from models.tree import Tree
from models.uuid4_str import pattern
from utilities import errors
from utilities.dynamodb_client import DynamoDBClient
from utilities.jwt_client import JwtClient
from utilities.tree_handler import TreeHandler

router = APIRouter(tags=["Tree"])
db_client = DynamoDBClient()


@router.get(
    path="/tree",
    summary="Get tree",
    response_model=Tree,
    responses={401: config.RES_401},
)
async def func(
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    tree_info = db_client.get_tree_info(jwt.user_group)
    return tree_info.tree.model_dump()


@router.post(
    path="/tree/node",
    summary="Update tree, Insert node",
    response_model=Tree,
    responses={401: config.RES_401, 404: config.RES_404, 422: config.RES_422},
)
async def func(
    req: req.TreeNodePost,
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    tree_info = db_client.get_tree_info(jwt.user_group)

    insert_id = str(uuid.uuid4())
    insert_node = Tree(node_id=insert_id, label=req.label, children=[])

    tree_handler = TreeHandler(tree_info.tree)
    tree_handler.insert_node(req.parent_id, insert_node)
    new_tree = tree_handler.sort_tree()
    tree_info.tree = new_tree

    new_node = Node(user_group=jwt.user_group, node_id=insert_id, text="")

    db_client.put_tree_info(tree_info)
    db_client.put_node(new_node)

    return new_tree.model_dump()


@router.delete(
    path="/tree/node/{node_id}",
    summary="Update tree, Delete node",
    response_model=Tree,
    responses={
        401: config.RES_401,
        403: config.RES_403,
        404: config.RES_404,
        422: config.RES_422,
    },
)
async def func(
    node_id: str = Path(**pattern),
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    tree_info = db_client.get_tree_info(jwt.user_group)
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
        n = Node(user_group=jwt.user_group, node_id=del_id, text="")
        db_client.delete_node(n)
    db_client.put_tree_info(tree_info)

    return new_tree.model_dump()


@router.put(
    path="/tree/node/label/{node_id}",
    summary="Update tree, Update label of node",
    response_model=Tree,
    responses={401: config.RES_401, 404: config.RES_404, 422: config.RES_422},
)
async def func(
    req: req.TreeNodeLabelPut,
    node_id: str = Path(**pattern),
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    tree_info = db_client.get_tree_info(jwt.user_group)
    tree_handler = TreeHandler(tree_info.tree)

    tree_handler.update_node_label(node_id, req.label)
    new_tree = tree_handler.sort_tree()
    tree_info.tree = new_tree

    db_client.put_tree_info(tree_info)
    return new_tree.model_dump()


@router.put(
    path="/tree/node/move/{node_id}",
    summary="Update tree, Move node",
    response_model=Tree,
    responses={
        401: config.RES_401,
        403: config.RES_403,
        404: config.RES_404,
        422: config.RES_422,
    },
)
async def func(
    req: req.TreeNodeMovePut,
    node_id: str = Path(**pattern),
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    tree_info = db_client.get_tree_info(jwt.user_group)
    root_node_id = tree_info.tree.node_id
    if node_id == root_node_id:
        raise errors.ForbiddenError

    tree_handler = TreeHandler(tree_info.tree)
    tree_handler.move_node(req.parent_id, node_id)
    new_tree = tree_handler.sort_tree()
    tree_info.tree = new_tree

    db_client.put_tree_info(tree_info)
    return new_tree.model_dump()
