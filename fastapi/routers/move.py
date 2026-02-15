import config
from fastapi import APIRouter, Depends, Path
from models import req
from models.jwt import JwtClaim
from models.result import Result
from models.uuid4_str import pattern
from utilities import errors
from utilities.dynamodb_client import DynamoDBClient
from utilities.jwt_client import JwtClient
from utilities.nodes_handler import NodesHandler

router = APIRouter(tags=["Move"])
db_client = DynamoDBClient()


@router.put(
    path="/nodes/move/{node_id}",
    summary="Move",
    response_model=Result,
    responses={
        400: config.RES_400,
        401: config.RES_401,
        404: config.RES_404,
        422: config.RES_422,
    },
)
async def func(
    req: req.NodeMovePut,
    node_id: str = Path(**pattern),
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    node = db_client.get_node(jwt.group_id, node_id)
    new_parent = db_client.get_node(jwt.group_id, req.parent_id)

    if not node or not new_parent:
        raise errors.NotFoundError

    # can not move root node
    nodes_handler = NodesHandler(jwt.group_id)
    root_node = nodes_handler.get_root()
    if root_node.node_id == node_id:
        raise errors.BadRequestError

    # can not move to child node
    childs = nodes_handler.children_ids_recursive(node_id)
    for i in childs:
        if i.node_id == req.parent_id:
            raise errors.BadRequestError

    if req.parent_id == nodes_handler.get_parent(node_id).node_id:
        # if move to same place, do nothing.
        pass
    else:
        # remove node id from old node
        now_parent = nodes_handler.get_parent(node_id)
        now_parent.children_ids.remove(node_id)

        # add node id to new node
        new_parent.children_ids.append(node_id)

        db_client.put_node(now_parent)
        db_client.put_node(new_parent)

    return {"result": "success"}
