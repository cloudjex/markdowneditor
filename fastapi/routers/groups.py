from typing import List
from uuid import uuid4

import config
from fastapi import APIRouter, Depends
from lib.dynamodb_client import DynamoDBClient
from lib.jwt_client import JwtClient
from models import req
from models.group import Group
from models.jwt import JwtClaim
from models.node import Node
from models.user import User

router = APIRouter(tags=["Groups"])
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
    for i in user.groups:
        group = db_client.get_group(i.group_id)
        if group:
            groups.append(group.model_dump())
    return groups


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
    )

    group_for_user = User.Group(
        group_id=group_id,
        role="admin",
    )
    user = db_client.get_user(jwt.email)
    user.groups.append(group_for_user)

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
