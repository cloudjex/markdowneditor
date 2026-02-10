from pydantic import BaseModel


class IdToken(BaseModel):
    id_token: str


class JwtClaim(BaseModel):
    email: str
    user_group: str
    iss: str
    aud: str
    iat: int
    exp: int
