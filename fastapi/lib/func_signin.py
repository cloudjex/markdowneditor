from lib.utilities import dynamodbs, jwt, response


def main(params: dict) -> dict:
    try:
        body: dict = params["body"]
        email: str = body.get("email")
        pw: str = body.get("password")

        if not email or not pw:
            raise Exception({
                "status_code": 400,
                "exception": "Bad Request",
                "error_code": "func_login.missing_parameters",
            })

        user_info = dynamodbs.get_user(email=email)
        if not user_info or user_info.get("password") != pw:
            raise Exception({
                "status_code": 401,
                "exception": "Unauthorized",
                "error_code": "func_login.invalid_credentials",
            })

        id_token = jwt.generate_jwt(email)

        res = {
            "email": email,
            "options": user_info["options"],
            "id_token": id_token,
        }

        return response.response_handler(body=res, status_code=200)

    except Exception as e:
        return response.error_handler(e)
