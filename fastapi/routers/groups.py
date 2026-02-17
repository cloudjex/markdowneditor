from typing import List

import config
from db.dynamodb import DynamoDBClient
from fastapi import APIRouter, Depends
from models.group import Group
from models.jwt import JwtClaim
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
    groups = [db_client.get_group(i.group_id) for i in user.groups]
    return groups
