from lib.utilities import errors
from lib.utilities.bcrypt_hash import BcryptHash
from lib.utilities.dynamodb_client import DynamoDBClient
from lib.utilities.jwt_client import JwtClient
from lib.utilities.response_handler import ResponseHandler


def main(params: dict) -> dict:
    try:
        body: dict = params["body"]
        email: str = body.get("email")
        pw: str = body.get("password")

        if not email or not pw:
            raise errors.BadRequestError("func_login.missing_params")

        db_client = DynamoDBClient()
        user = db_client.get_user(email=email)

        bcrypt = BcryptHash()
        if not user or not bcrypt.bcrypt_verify(pw, user.password):
            raise errors.UnauthorizedError("func_login.invalid_credentials")

        if not user.options.enabled:
            raise errors.ForbiddenError("func_login.not_enabled")

        id_token = JwtClient().generate_jwt(email)

        res = {
            "email": email,
            "options": user.options.json,
            "id_token": id_token,
        }

        return ResponseHandler().response(body=res, status_code=200)

    except Exception as e:
        return ResponseHandler().error_response(e)
