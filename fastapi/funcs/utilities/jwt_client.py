import time

import jwt

import config
from funcs.utilities import errors


class JwtClient:
    def encode(self, email: str) -> str:
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

    def verify(self, id_token: str) -> dict:
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
