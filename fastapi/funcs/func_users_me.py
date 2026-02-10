from funcs.utilities import errors
from funcs.utilities.bcrypt_hash import Bcrypt
from funcs.utilities.dynamodb_client import DynamoDBClient


def get_myuser(email: str) -> dict:
    db_client = DynamoDBClient()
    user = db_client.get_user(email)

    return user.model_dump(include_pw=False)


def update_mypw(email: str, old_password: str, new_password: str) -> dict:
    db_client = DynamoDBClient()
    user = db_client.get_user(email)

    if len(new_password) < 4 or len(new_password) > 20:
        raise errors.BadRequestError

    if not Bcrypt().verify(old_password, user.password):
        raise errors.UnauthorizedError

    hashed_new_password = Bcrypt().hash(new_password)

    user.password = hashed_new_password
    db_client.put_user(user)

    return {"result": "success"}
