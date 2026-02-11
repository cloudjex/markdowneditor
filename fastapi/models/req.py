from pydantic import BaseModel


class SignIn(BaseModel):
    email: str
    password: str


class SignInGroup(BaseModel):
    user_group: str


class UpdatePassword(BaseModel):
    old_password: str
    new_password: str


class TreeNodePost(BaseModel):
    parent_id: str
    label: str


class TreeNodeLabelPut(BaseModel):
    label: str


class TreeNodeMovePut(BaseModel):
    parent_id: str


class NodePut(BaseModel):
    text: str
