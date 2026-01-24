from funcs.utilities import errors
from funcs.utilities.bcrypt_hash import BcryptHash
from funcs.utilities.dynamodb_client import DynamoDBClient
from funcs.utilities.jwt_client import JwtClient


def post(email: str, password: str) -> dict:
    db_client = DynamoDBClient()
    user = db_client.get_user(email=email)

    if not user or not BcryptHash().bcrypt_verify(password, user.password):
        raise errors.UnauthorizedError("func_login.invalid_credentials")

    if not user.options.enabled:
        raise errors.ForbiddenError("func_login.not_enabled")

    id_token = JwtClient().generate_jwt(email)

    res = {
        "email": email,
        "options": user.options.to_dict(),
        "id_token": id_token,
    }

    return res
