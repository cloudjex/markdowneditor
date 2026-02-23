import time

import jwt

import config
from fastapi import Request
from lib import errors
from models.jwt import JwtClaim


class JwtClient:
    def encode(self, email: str, group_id: str = "") -> str:
        claim = {
            "email": email,
            "group_id": group_id,
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

    def verify_token(self, id_token: str) -> JwtClaim:
        try:
            decoded: dict = jwt.decode(
                jwt=id_token.removeprefix("Bearer "),
                key=config.JWT_KEY,
                algorithms=["HS256"],
                audience=config.APP_URL,
                issuer=config.APP_URL,
                verify=True,
            )

            required_key = ["email", "group_id"]
            if not all(k in decoded.keys() for k in required_key):
                raise errors.UnauthorizedError

            return JwtClaim(**decoded)

        except Exception as e:
            raise errors.UnauthorizedError from e

    async def verify(self, request: Request) -> JwtClaim:
        token = request.headers.get("Authorization", "")
        return self.verify_token(token)
