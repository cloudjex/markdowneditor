import uuid
from typing import List

import config
from db.dynamodb import DynamoDBClient
from fastapi import APIRouter, Depends, Path
from models import req
from models.jwt import JwtClaim
from models.node import Node
from models.uuid4_str import pattern
from utilities import errors
from utilities.jwt_client import JwtClient
from utilities.nodes_handler import NodesHandler

router = APIRouter(tags=["Nodes"])
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
