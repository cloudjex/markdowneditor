import hashlib
import random

from lib import config
from lib.utilities import dynamodbs, mail, response


def main(params: dict) -> dict:
    try:
        body: dict = params["body"]
        email: str = body.get("email")
        password: str = body.get("password")

        if not email or not password:
            raise Exception({
                "status_code": 400,
                "exception": "Bad Request",
                "error_code": "func_signup.missing_parameters",
            })

        user = dynamodbs.get_user(email)
        if user and user["options"]["enabled"]:
            raise Exception({
                "status_code": 409,
                "exception": "Conflict",
                "error_code": "func_signup.user_already_exists",
            })

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        otp = str(random.randint(100000, 999999))
        options = {
            "otp": otp,
            "enabled": False,
        }

        dynamodbs.put_user(email, hashed_password, options)
        if config.SMTP_PASSWORD:
            mail.send_mail(
                to=email,
                subject="ユーザ仮登録完了のお知らせ",
                body=f"ユーザ仮登録が完了しました。認証画面で以下の認証コードを入力してください。<br><br>認証コード: {otp}"
            )
        else:
            print(f"Warning: SMTP is not configured. OTP for {email} is {otp}")

        res = {"email": email}
        return response.response_handler(body=res, status_code=200)

    except Exception as e:
        return response.error_handler(e)
