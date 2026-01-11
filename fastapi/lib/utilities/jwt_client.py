import time

import jwt

from lib import config
from lib.utilities import errors


class JwtClient:
    def generate_jwt(self, email: str) -> str:
        claim = {
            "email": email,
            "iss": config.APP_URL,
            "aud": config.APP_URL,
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600,
        }

        return jwt.encode(
            payload=claim,
            key=config.JWT_KEY,
            algorithm="HS256",
        )

    def verify_id_token(self, id_token: str) -> dict:
        try:
            return jwt.decode(
                jwt=id_token.removeprefix("Bearer "),
                key=config.JWT_KEY,
                algorithms="HS256",
                audience=config.APP_URL,
                issuer=config.APP_URL,
                verify=True,
            )

        except Exception:
            raise errors.UnauthorizedError("JwtClient.invalid_credentials")
