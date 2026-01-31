from __future__ import annotations

from typing import List

from pydantic import BaseModel


# ================= Request Model =================
class SignInReq(BaseModel):
    email: str
    password: str


class SignUpReq(BaseModel):
    email: str
    password: str


class SignUpVerifyReq(BaseModel):
    email: str
    otp: str


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
    id: str
    label: str
    children: List[Tree] = []


class NodeRes(BaseModel):
    email: str
    id: str
    text: str


class NodesRes(BaseModel):
    nodes: List[NodeRes]
