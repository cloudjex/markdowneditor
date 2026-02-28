from typing import List
from uuid import uuid4

import config
from fastapi import APIRouter, Depends
from lib import errors
from lib.dynamodb_client import DynamoDBClient
from lib.jwt_client import JwtClient
from models import req
from models.group import Group
from models.jwt import JwtClaim
from models.node import Node

router = APIRouter()
db_client = DynamoDBClient()


@router.get(
    path="/groups",
    summary="Get user groups",
    response_model=List[Group],
    responses={
        401: config.RES_401,
    },
)
async def func(
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    user = db_client.get_user(jwt.email)
    groups = []
    for group_id in user.groups:
        group = db_client.get_group(group_id)
        if group:
            groups.append(group.model_dump())
    return groups


@router.get(
    path="/groups/{group_id}",
    summary="Get user group",
    response_model=Group,
    responses={
        401: config.RES_401,
        404: config.RES_404,
    },
)
async def func(
    group_id: str,
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    user = db_client.get_user(jwt.email)
    group = db_client.get_group(group_id)

    if (group_id not in user.groups) or (not group):
        raise errors.NotFoundError

    return group.model_dump()


@router.post(
    path="/groups",
    summary="Post user group",
    response_model=Group,
    responses={
        401: config.RES_401,
        422: config.RES_422,
    },
)
async def func(
    req: req.UserGroupPost,
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    group_id = str(uuid4())
    group = Group(
        group_id=group_id,
        group_name=req.group_name,
        users=[
            {
                "email": jwt.email,
                "role": "admin",
            },
        ],
    )

    user = db_client.get_user(jwt.email)
    user.groups.append(group_id)

    default_node = Node(
        group_id=group_id,
        node_id=str(uuid4()),
        label="Default",
        text="",
        children_ids=[],
    )

    db_client.put_group(group)
    db_client.put_user(user)
    db_client.put_node(default_node)

    return group.model_dump()


@router.delete(
    path="/groups/{group_id}",
    summary="Delete user group",
    response_model=Group,
    responses={
        401: config.RES_401,
        403: config.RES_403,
        404: config.RES_404,
        422: config.RES_422,
    },
)
async def func(
    group_id: str,
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    group = db_client.get_group(group_id)
    user = db_client.get_user(jwt.email)

    if (group_id not in user.groups) or (not group):
        raise errors.NotFoundError

    user_in_group = next((u for u in group.users if u.email == jwt.email), None)
    if (not user_in_group) or (user_in_group.role != "admin"):
        raise errors.ForbiddenError

    user.groups.remove(group_id)
    db_client.put_user(user)
    db_client.delete_group(group)

    nodes = db_client.get_nodes(group_id)
    for node in nodes:
        db_client.delete_node(node)

    return group.model_dump()
