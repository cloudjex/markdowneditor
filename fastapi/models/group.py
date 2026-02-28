from typing import List

from pydantic import BaseModel, EmailStr, Field

from models.uuid4_str import pattern


class Group(BaseModel):
    group_id: str = Field(**pattern)
    group_name: str = Field(min_length=1)
    users: List["User"]

    class User(BaseModel):
        email: EmailStr
        role: str
