from funcs.utilities import errors
from funcs.utilities.bcrypt_hash import Bcrypt
from funcs.utilities.dynamodb_client import DynamoDBClient
from funcs.utilities.jwt_client import JwtClient


def signin(email: str, password: str) -> dict:
    db_client = DynamoDBClient()
    user = db_client.get_user(email=email)

    if not user or not Bcrypt().verify(password, user.password):
        raise errors.UnauthorizedError

    if not user.options.enabled:
        raise errors.ForbiddenError

    id_token = JwtClient().encode(email, "")

    return {"id_token": id_token}


def signin_group(email: str, user_group: str) -> dict:
    db_client = DynamoDBClient()
    user = db_client.get_user(email=email)

    if not user.options.enabled:
        raise errors.ForbiddenError

    if not any(user_group == g.group_name for g in user.user_groups):
        raise errors.UnauthorizedError

    id_token = JwtClient().encode(email, user_group)

    return {"id_token": id_token}
