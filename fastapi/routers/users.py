import config
from fastapi import APIRouter, Depends
from models import req
from models.jwt import JwtClaim
from models.result import Result
from models.user import User
from utilities import errors
from utilities.bcrypt_client import BcryptClient
from utilities.dynamodb_client import DynamoDBClient
from utilities.jwt_client import JwtClient

router = APIRouter(tags=["Users"])
db_client = DynamoDBClient()


@router.get(
    path="/users/me",
    summary="Get your user info",
    response_model=User,
    responses={
        401: config.RES_401,
    },
)
async def func(
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    user = db_client.get_user(jwt.email)
    user.password = "*****"
    return user


@router.put(
    path="/users/me/password",
    summary="Update your password",
    response_model=Result,
    responses={
        401: config.RES_401,
        422: config.RES_422,
    },
)
async def func(
    req: req.UpdatePassword,
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    user = db_client.get_user(jwt.email)
    if not BcryptClient().verify(req.old_password, user.password):
        raise errors.UnauthorizedError

    hashed_new_password = BcryptClient().hash(req.new_password)

    user.password = hashed_new_password
    db_client.put_user(user)
    return {"result": "success"}
