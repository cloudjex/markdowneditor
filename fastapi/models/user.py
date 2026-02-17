from typing import List

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4, examples=["*****"])
    groups: List["Groups"]
    options: "Options"

    class Groups(BaseModel):
        group_id: str
        role: str

    class Options(BaseModel):
        enabled: bool
        otp: str
