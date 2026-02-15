import config
from fastapi import APIRouter, Depends
from models import req
from models.jwt import IdToken, JwtClaim
from models.result import Result
from utilities import errors
from utilities.bcrypt_hash import Bcrypt
from utilities.dynamodb_client import DynamoDBClient
from utilities.jwt_client import JwtClient

router = APIRouter(tags=["Auth"])
db_client = DynamoDBClient()


@router.post(
    path="/signin",
    summary="Sign in",
    response_model=IdToken,
    responses={
        401: config.RES_401,
        403: config.RES_403,
        422: config.RES_422,
    },
)
async def func(
    req: req.SignIn,
):
    user = db_client.get_user(email=req.email)
    if not user or not Bcrypt().verify(req.password, user.password):
        raise errors.UnauthorizedError

    if not user.options.enabled:
        raise errors.ForbiddenError

    id_token = JwtClient().encode(req.email)
    return {"id_token": id_token}


@router.post(
    path="/signin/group",
    summary="Sign in to user group",
    response_model=IdToken,
    responses={
        403: config.RES_403,
        422: config.RES_422,
    },
)
async def func(
    req: req.SignInGroup,
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    user = db_client.get_user(email=jwt.email)
    if not user.options.enabled:
        raise errors.ForbiddenError

    if not any(req.user_group == g.group_name for g in user.user_groups):
        raise errors.ForbiddenError

    id_token = JwtClient().encode(jwt.email, req.user_group)
    return {"id_token": id_token}


@router.post(
    path="/signout",
    summary="Sign out",
    response_model=Result,
    responses={
        401: config.RES_401,
    },
)
async def func(
    _=Depends(JwtClient().verify),
):
    return {"result": "success"}
