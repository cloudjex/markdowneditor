from funcs.utilities import errors
from funcs.utilities.dynamodb_client import DynamoDBClient


def get(email: str) -> dict:
    db_client = DynamoDBClient()
    user = db_client.get_user(email)
    if not user:
        raise errors.NotFoundError("func_users.not_found")

    return user.to_dict(include_pw=False)
