from typing import List

from pydantic import BaseModel, Field

from models.uuid4_str import pattern


class Tree(BaseModel):
    node_id: str = Field(**pattern)
    label: str = Field(min_length=1)
    children: List["Tree"] = []
