from typing import List

from pydantic import BaseModel, EmailStr, Field

from models.uuid4_str import pattern


class User(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4, examples=["*****"])
    groups: List["Group"]
    options: "Options"

    class Group(BaseModel):
        group_id: str = Field(**pattern)
        role: str = Field(examples=["admin", "editor", "viewer"])

    class Options(BaseModel):
        enabled: bool
        otp: str = Field(min_length=0, max_length=6, examples=["123456"])
