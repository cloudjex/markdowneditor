from __future__ import annotations

from typing import List

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    password: str
    user_groups: List[UserGroup]
    options: Options

    class UserGroup(BaseModel):
        group_name: str
        role: str

    class Options(BaseModel):
        enabled: bool
        otp: str
