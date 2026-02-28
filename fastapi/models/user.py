from typing import List

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4, examples=["*****"])
    groups: List[str]
    options: "Options"

    class Options(BaseModel):
        enabled: bool
        otp: str = Field(min_length=0, max_length=6, examples=["123456"])
