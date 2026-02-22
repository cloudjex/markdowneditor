from pydantic import BaseModel, EmailStr, Field

from models.uuid4_str import pattern


class SignIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4)


class SignInGroup(BaseModel):
    group_id: str = Field(**pattern)


class SignUp(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4)


class UpdatePassword(BaseModel):
    old_password: str = Field(min_length=4)
    new_password: str = Field(min_length=4)


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
