from lib.utilities import exceptions
from lib.utilities.bcrypt_hash import BcryptHash
from lib.utilities.dynamodb_client import UserTableClient
from lib.utilities.jwt_client import JwtClient
from lib.utilities.response_handler import ResponseHandler


def main(params: dict) -> dict:
    try:
        body: dict = params["body"]
        email: str = body.get("email")
        pw: str = body.get("password")

        if not email or not pw:
            raise exceptions.BadRequestError({
                "error_code": "func_login.missing_parameters",
            })

        db_client = UserTableClient()
        user_info = db_client.get_user(email=email)

        bcrypt = BcryptHash()
        if not user_info or not bcrypt.bcrypt_verify(pw, user_info.get("password")):
            raise exceptions.UnauthorizedError({
                "error_code": "func_login.invalid_credentials",
            })

        options: dict = user_info.get("options")
        if not options.get("enabled"):
            raise exceptions.ForbiddenError({
                "error_code": "func_login.account_not_enabled",
            })

        id_token = JwtClient().generate_jwt(email)

        res = {
            "email": email,
            "options": options,
            "id_token": id_token,
        }

        return ResponseHandler().response(body=res, status_code=200)

    except Exception as e:
        return ResponseHandler().error_response(e)
