import secrets

from funcs.entities.user import User
from funcs.utilities import errors
from funcs.utilities.bcrypt_hash import Bcrypt
from funcs.utilities.dynamodb_client import DynamoDBClient
from funcs.utilities.smtp_client import SmtpClient


def post(email: str, password: str) -> dict:
    db_client = DynamoDBClient()
    user = db_client.get_user(email)
    if user and user.options.enabled:
        raise errors.ConflictError("func_signup.conflict_user")

    hashed = Bcrypt().hash(password)
    options = {
        "otp": f"{secrets.randbelow(1000000):06d}",
        "enabled": False,
    }

    new_user = User(email, hashed, options)

    db_client.put_user(new_user)
    SmtpClient().send(
        email,
        "ユーザ仮登録完了のお知らせ",
        f"ユーザ仮登録が完了しました。認証画面で以下の認証コードを入力してください。<br><br>認証コード: {new_user.options.otp}"
    )

    return {"result": "success"}
