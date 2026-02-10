from __future__ import annotations

from typing import List

from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str
    user_groups: List[UserGroup]
    options: Options

    class UserGroup(BaseModel):
        group_name: str
        role: str

    class Options(BaseModel):
        enabled: bool
        otp: str

    def model_dump(self, include_pw: bool = False, **kwargs):
        data = super().model_dump(**kwargs)
        if not include_pw:
            data["password"] = "***"
        return data
