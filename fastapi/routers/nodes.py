import uuid
from typing import List

import config
from fastapi import APIRouter, Depends, Path
from lib import errors
from lib.dynamodb_client import DynamoDBClient
from lib.jwt_client import JwtClient
from lib.nodes_handler import NodesHandler
from models import req
from models.jwt import JwtClaim
from models.node import Node
from models.result import Result
from models.uuid4_str import pattern

router = APIRouter()
db_client = DynamoDBClient()


@router.get(
    path="/nodes",
    summary="Get nodes",
    response_model=List[Node],
    responses={
        401: config.RES_401,
    },
)
async def func(
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    items = db_client.get_nodes(jwt.group_id)
    return [i.model_dump() for i in items]


@router.get(
    path="/nodes/{node_id}",
    summary="Get node",
    response_model=Node,
    responses={
        401: config.RES_401,
        404: config.RES_404,
        422: config.RES_422,
    },
)
async def func(
    node_id: str = Path(**pattern),
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    item = db_client.get_node(jwt.group_id, node_id)
    if not item:
        raise errors.NotFoundError
    return item.model_dump()


@router.post(
    path="/nodes/{node_id}",
    summary="Post node",
    response_model=Node,
    responses={
        401: config.RES_401,
        404: config.RES_404,
        422: config.RES_422,
    },
)
async def func(
    req: req.NodePost,
    node_id: str = Path(**pattern),
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    parent_node = db_client.get_node(jwt.group_id, node_id)
    if not parent_node:
        raise errors.NotFoundError

    uuid_v4 = str(uuid.uuid4())
    parent_node.children_ids.append(uuid_v4)

    new_node = Node(
        group_id=jwt.group_id,
        node_id=uuid_v4,
        label=req.label,
        text="",
        children_ids=[],
    )

    db_client.put_node(parent_node)
    db_client.put_node(new_node)

    return new_node.model_dump()


@router.put(
    path="/nodes/{node_id}",
    summary="Put node",
    response_model=Node,
    responses={
        401: config.RES_401,
        404: config.RES_404,
        422: config.RES_422,
    },
)
async def func(
    req: req.NodePut,
    node_id: str = Path(**pattern),
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    node = db_client.get_node(jwt.group_id, node_id)
    if not node:
        raise errors.NotFoundError

    node.label = req.label
    node.text = req.text
    db_client.put_node(node)

    return node.model_dump()


@router.delete(
    path="/nodes/{node_id}",
    summary="Delete node",
    response_model=Node,
    responses={
        400: config.RES_400,
        401: config.RES_401,
        404: config.RES_404,
        422: config.RES_422,
    },
)
async def func(
    node_id: str = Path(**pattern),
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    node = db_client.get_node(jwt.group_id, node_id)
    if not node:
        raise errors.NotFoundError

    nodes_handler = NodesHandler(jwt.group_id)
    root_node = nodes_handler.get_root()
    if root_node.node_id == node_id:
        raise errors.BadRequestError

    del_targets = nodes_handler.children_ids_recursive(node_id)
    parent_node = nodes_handler.get_parent(node_id)
    parent_node.children_ids.remove(node_id)

    db_client.delete_node(node)
    for i in del_targets:
        db_client.delete_node(i)

    db_client.put_node(parent_node)

    return node.model_dump()


@router.put(
    path="/nodes/move/{node_id}",
    summary="Move node",
    response_model=Result,
    responses={
        400: config.RES_400,
        401: config.RES_401,
        404: config.RES_404,
        422: config.RES_422,
    },
)
async def func(
    req: req.NodeMovePut,
    node_id: str = Path(**pattern),
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    node = db_client.get_node(jwt.group_id, node_id)
    new_parent = db_client.get_node(jwt.group_id, req.parent_id)

    if not node or not new_parent:
        raise errors.NotFoundError

    # can not move root node
    nodes_handler = NodesHandler(jwt.group_id)
    root_node = nodes_handler.get_root()
    if root_node.node_id == node_id:
        raise errors.BadRequestError

    # can not move to child node
    childs = nodes_handler.children_ids_recursive(node_id)
    for i in childs:
        if i.node_id == req.parent_id:
            raise errors.BadRequestError

    if req.parent_id == nodes_handler.get_parent(node_id).node_id:
        # if move to same place, do nothing.
        pass
    else:
        # remove node id from old node
        now_parent = nodes_handler.get_parent(node_id)
        now_parent.children_ids.remove(node_id)

        # add node id to new node
        new_parent.children_ids.append(node_id)

        db_client.put_node(now_parent)
        db_client.put_node(new_parent)

    return {"result": "success"}
