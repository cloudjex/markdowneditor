from typing import List

import config
from fastapi import APIRouter, Depends, Path
from models import req
from models.jwt import JwtClaim
from models.node import Node
from models.uuid4_str import pattern
from utilities import errors
from utilities.dynamodb_client import DynamoDBClient
from utilities.jwt_client import JwtClient

router = APIRouter(tags=["Node"])
db_client = DynamoDBClient()


@router.get(
    path="/nodes",
    summary="Get nodes",
    response_model=List[Node],
    responses={401: config.RES_401},
)
async def func(
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    items = db_client.get_nodes(jwt.user_group)
    return [i.model_dump() for i in items]


@router.get(
    path="/nodes/{node_id}",
    summary="Get node",
    response_model=Node,
    responses={401: config.RES_401, 404: config.RES_404, 422: config.RES_422},
)
async def func(
    node_id: str = Path(**pattern),
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    item = db_client.get_node(jwt.user_group, node_id)
    if not item:
        raise errors.NotFoundError
    ret = item.model_dump()

    return ret


@router.put(
    path="/nodes/{node_id}",
    summary="Put node",
    response_model=Node,
    responses={401: config.RES_401, 404: config.RES_404, 422: config.RES_422},
)
async def func(
    req: req.NodePut,
    node_id: str = Path(**pattern),
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    node = db_client.get_node(jwt.user_group, node_id)
    if not node:
        raise errors.NotFoundError

    node.text = req.text
    db_client.put_node(node)

    return node.model_dump()
