from lib.utilities import dynamodbs, jwt, response


def main(params: dict) -> dict:
    try:
        body: dict = params["body"]
        email: str = body.get("email")
        otp: str = body.get("otp")

        if not email or not otp:
            raise Exception({
                "status_code": 400,
                "exception": "Bad Request",
                "error_code": "func_signup_verify.missing_parameters",
            })

        user = dynamodbs.get_user(email)
        if not user:
            raise Exception({
                "status_code": 404,
                "exception": "User Not Found",
                "error_code": "func_signup_verify.user_not_found",
            })

        options: dict = user.get("options", {})
        if options.get("otp") != otp:
            raise Exception({
                "status_code": 401,
                "exception": "Unauthorized",
                "error_code": "func_signup_verify.invalid_otp",
            })

        options.pop("otp")
        options["enabled"] = True

        dynamodbs.put_user(email, user["password"], options)

        id_token = jwt.generate_jwt(email)

        res = {
            "email": email,
            "options": options,
            "id_token": id_token,
        }
        return response.response_handler(body=res, status_code=200)

    except Exception as e:
        return response.error_handler(e)
