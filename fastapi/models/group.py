from typing import List

from pydantic import BaseModel, Field

from models.uuid4_str import pattern


class Group(BaseModel):
    group_id: str = Field(**pattern)
    group_name: str = Field(min_length=1)
