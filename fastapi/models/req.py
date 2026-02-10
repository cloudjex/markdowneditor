from pydantic import BaseModel


class SignInReq(BaseModel):
    email: str
    password: str


class SignInGroupReq(BaseModel):
    user_group: str


class UpdatePasswordReq(BaseModel):
    old_password: str
    new_password: str


class TreeNodePostReq(BaseModel):
    parent_id: str
    label: str


class TreeNodeLabelPutReq(BaseModel):
    label: str


class TreeNodeMovePutReq(BaseModel):
    parent_id: str


class NodePutReq(BaseModel):
    text: str
