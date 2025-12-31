import time

import jwt

from lib import config
from lib.utilities import errors


class JwtClient:
    def __init__(self):
        pass

    def generate_jwt(self, email: str) -> str:
        try:
            claim = {
                "email": email,
                "iss": config.APP_URL,
                "aud": config.APP_URL,
                "iat": int(time.time()),
                "exp": int(time.time()) + 3600,
            }

            str_jwt = jwt.encode(
                payload=claim,
                key=config.JWT_KEY,
                algorithm="HS256",
            )
            return str_jwt

        except Exception as e:
            raise e

    def verify_id_token(self, id_token: str) -> dict:
        try:
            id_token = id_token.replace("Bearer ", "")

            json_payload: dict = jwt.decode(
                jwt=id_token,
                key=config.JWT_KEY,
                algorithms="HS256",
                audience=config.APP_URL,
                issuer=config.APP_URL,
                verify=True,
            )

            return json_payload

        except Exception:
            raise errors.UnauthorizedError("JwtClient.invalid_credentials")
