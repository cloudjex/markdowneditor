from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from models.uuid4_str import pattern


class Tree(BaseModel):
    node_id: str = Field(**pattern)
    label: str
    children: List[Tree] = []


class TreeInfo(BaseModel):
    user_group: str
    tree: Tree
