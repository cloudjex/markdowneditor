from typing import List

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    password: str
    groups: List["Groups"]
    options: "Options"

    class Groups(BaseModel):
        group_name: str
        role: str

    class Options(BaseModel):
        enabled: bool
        otp: str
