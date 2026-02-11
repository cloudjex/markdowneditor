from pydantic import BaseModel, EmailStr


class IdToken(BaseModel):
    id_token: str


class JwtClaim(BaseModel):
    email: EmailStr
    user_group: str
    iss: str
    aud: str
    iat: int
    exp: int
