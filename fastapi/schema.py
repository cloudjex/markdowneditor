from pydantic import BaseModel


class SignInRequest(BaseModel):
    email: str
    password: str


class SignUpRequest(BaseModel):
    email: str
    password: str


class SignUpVerifyRequest(BaseModel):
    email: str
    otp: str


class TreePostRequest(BaseModel):
    parent_id: str
    label: str

class NodePutRequest(BaseModel):
    id: str
    text: str
