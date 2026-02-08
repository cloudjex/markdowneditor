from __future__ import annotations

from typing import List

from pydantic import BaseModel


# ================= Request Model =================
class SignInReq(BaseModel):
    email: str
    password: str


class SignInGroupReq(BaseModel):
    user_group: str


class UserReq(BaseModel):
    email: str
    password: str
    user_groups: List[UserGroup]
    options: Options

    class UserGroup(BaseModel):
        group_name: str
        role: str

    class Options(BaseModel):
        enabled: bool
        otp: str


class UpdatePasswordReq(BaseModel):
    old_password: str
    new_password: str


class TreeNodePostReq(BaseModel):
    parent_id: str
    label: str


class TreeNodeLabelPutReq(BaseModel):
    label: str


class TreeNodeMovePutReq(BaseModel):
    parent_id: str


class NodePutReq(BaseModel):
    text: str


# ================= Response Model =================
class SignInRes(BaseModel):
    id_token: str


class ResultRes(BaseModel):
    result: str


class Tree(BaseModel):
    node_id: str
    label: str
    children: List[Tree] = []


class NodeRes(BaseModel):
    user_group: str
    node_id: str
    text: str


class NodesRes(BaseModel):
    nodes: List[NodeRes]
