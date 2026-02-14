from pydantic import BaseModel, EmailStr, Field

from models.uuid4_str import pattern


class SignIn(BaseModel):
    email: EmailStr
    password: str


class SignInGroup(BaseModel):
    user_group: str


class UpdatePassword(BaseModel):
    old_password: str
    new_password: str = Field(min_length=4, max_length=20)


class TreeNodePost(BaseModel):
    parent_id: str = Field(**pattern)
    label: str = Field(min_length=1)


class TreeNodeLabelPut(BaseModel):
    label: str = Field(min_length=1)


class NodeMovePut(BaseModel):
    parent_id: str = Field(**pattern)


class NodePost(BaseModel):
    label: str = Field(min_length=1)
    text: str


class NodePut(BaseModel):
    label: str = Field(min_length=1)
    text: str
