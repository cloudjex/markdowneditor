from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Tree(BaseModel):
    node_id: str
    label: str
    children: List[Tree] = []


class TreeInfo(BaseModel):
    user_group: str
    tree: Tree
