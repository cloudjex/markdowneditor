import time

import jwt

import config
from funcs.utilities import errors


class JwtClient:
    def encode(self, email: str, user_group: str) -> str:
        claim = {
            "email": email,
            "user_group": user_group,
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
            decoded = jwt.decode(
                jwt=id_token.removeprefix("Bearer "),
                key=config.JWT_KEY,
                algorithms="HS256",
                audience=config.APP_URL,
                issuer=config.APP_URL,
                verify=True,
            )

            if "email" not in decoded or "user_group" not in decoded:
                raise errors.UnauthorizedError("JwtClient.invalid_payload")

            return decoded

        except Exception as e:
            raise errors.UnauthorizedError(
                "JwtClient.invalid_credentials"
            ) from e
