from typing import List

from pydantic import BaseModel, Field

from models.uuid4_str import pattern


class Node(BaseModel):
    user_group: str
    node_id: str = Field(**pattern)
    label: str = Field(min_length=1)
    text: str
    children_ids: List[str]
