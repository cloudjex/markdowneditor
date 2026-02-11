from pydantic import BaseModel, Field

from models.uuid4_str import pattern


class Node(BaseModel):
    user_group: str
    node_id: str = Field(**pattern)
    text: str
