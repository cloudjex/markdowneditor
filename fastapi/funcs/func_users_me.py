from funcs.utilities import errors
from funcs.utilities.bcrypt_hash import Bcrypt
from funcs.utilities.dynamodb_client import DynamoDBClient


def get(email: str) -> dict:
    db_client = DynamoDBClient()
    user = db_client.get_user(email)
    if not user:
        raise errors.NotFoundError("func_users.not_found")

    return user.to_dict(include_pw=False)


def put(email: str, old_password: str, new_password: str) -> dict:
    db_client = DynamoDBClient()
    user = db_client.get_user(email)
    if not user:
        raise errors.NotFoundError("func_users.not_found")

    if not Bcrypt().verify(old_password, user.password):
        raise errors.UnauthorizedError("func_users.incorrect_password")

    if len(new_password) < 4 or len(new_password) > 20:
        raise errors.BadRequestError("func_users.invalid_password")

    hashed_new_password = Bcrypt().hash(new_password)

    user.password = hashed_new_password
    db_client.put_user(user)

    return {"result": "success"}
