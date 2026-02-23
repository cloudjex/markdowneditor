from typing import List
from uuid import uuid4

import config
from fastapi import APIRouter, Depends
from models import req
from models.group import Group
from models.jwt import JwtClaim
from models.user import User
from utilities.dynamodb_client import DynamoDBClient
from utilities.jwt_client import JwtClient

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
        role="owner",
    )
    user = db_client.get_user(jwt.email)
    user.groups.append(group_for_user)

    db_client.put_group(group)
    db_client.put_user(user)

    return group.model_dump()
