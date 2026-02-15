from typing import List

from pydantic import BaseModel, Field

from models.uuid4_str import pattern


class Node(BaseModel):
    group_id: str = Field(**pattern)
    node_id: str = Field(**pattern)
    label: str = Field(min_length=1)
    text: str
    children_ids: List[str]
