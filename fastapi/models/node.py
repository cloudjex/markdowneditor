from pydantic import BaseModel


class Node(BaseModel):
    user_group: str
    node_id: str
    text: str
