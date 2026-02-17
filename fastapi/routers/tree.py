import config
from db.dynamodb import DynamoDBClient
from fastapi import APIRouter, Depends
from models.jwt import JwtClaim
from models.tree import Tree
from utilities.jwt_client import JwtClient
from utilities.nodes_handler import NodesHandler

router = APIRouter(tags=["Tree"])
db_client = DynamoDBClient()


@router.get(
    path="/tree",
    summary="Get tree",
    response_model=Tree,
    responses={
        401: config.RES_401,
    },
)
async def func(
    jwt: JwtClaim = Depends(JwtClient().verify),
):
    nodes_handler = NodesHandler(jwt.group_id)
    root = nodes_handler.get_root()
    return nodes_handler.tree(root.node_id)
