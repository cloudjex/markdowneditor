import secrets

import config
from fastapi import APIRouter, Depends
from models import req
from models.jwt import IdToken, JwtClaim
from models.result import Result
from models.user import User
from utilities import errors
from utilities.bcrypt_client import BcryptClient
from utilities.dynamodb_client import DynamoDBClient
from utilities.jwt_client import JwtClient
from utilities.smtp_client import SmtpClient

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
    if not user or not BcryptClient().verify(req.password, user.password):
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

    if not any(req.group_id == g.group_id for g in user.groups):
        raise errors.ForbiddenError

    id_token = JwtClient().encode(jwt.email, req.group_id)
    return {"id_token": id_token}


@router.post(
    path="/signup",
    summary="Sign up",
    response_model=Result,
    responses={
        409: config.RES_409,
        422: config.RES_422,
    },
)
async def func(
    req: req.SignUp,
):
    if db_client.get_user(req.email) is not None:
        raise errors.ConflictError

    user = User(
        email=req.email,
        password=BcryptClient().hash(req.password),
        groups=[],
        options={
            "enabled": False,
            "otp": f"{secrets.randbelow(1000000):06d}",
        },
    )

    db_client.put_user(user)

    SmtpClient().send(
        recipient=user.email,
        subject="ユーザ仮登録が完了しました",
        body=f"以下のワンタイムパスワードを入力し、Email認証を完了してください<br>{user.options.otp}",
    )

    return {"result": "success"}


@router.post(
    path="/signup/verify",
    summary="Verify sign up",
    response_model=Result,
    responses={
        401: config.RES_401,
        404: config.RES_404,
        422: config.RES_422,
    },
)
async def func(
    req: req.SignUpVerify,
):
    user = db_client.get_user(req.email)
    if not user:
        raise errors.NotFoundError

    if user.options.otp != req.otp:
        raise errors.UnauthorizedError

    user.options.enabled = True
    user.options.otp = ""

    db_client.put_user(user)

    return {"result": "success"}


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
