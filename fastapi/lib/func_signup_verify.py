from lib.utilities import exceptions
from lib.utilities.dynamodb_client import UserTableClient
from lib.utilities.jwt_client import JwtClient
from lib.utilities.response_handler import ResponseHandler


def main(params: dict) -> dict:
    try:
        body: dict = params["body"]
        email: str = body.get("email")
        otp: str = body.get("otp")

        if not email or not otp:
            raise exceptions.BadRequestError({
                "error_code": "func_signup_verify.missing_parameters",
            })

        db_client = UserTableClient()
        user = db_client.get_user(email)
        if not user:
            raise exceptions.NotFoundError({
                "error_code": "func_signup_verify.user_not_found",
            })

        options: dict = user.get("options", {})
        if options.get("otp") != otp:
            raise exceptions.UnauthorizedError({
                "error_code": "func_signup_verify.invalid_otp",
            })

        options.pop("otp")
        options["enabled"] = True

        db_client.put_user(email, user["password"], options)

        id_token = JwtClient().generate_jwt(email)

        res = {
            "email": email,
            "options": options,
            "id_token": id_token,
        }
        return ResponseHandler().response(body=res, status_code=200)

    except Exception as e:
        return ResponseHandler().error_response(e)
