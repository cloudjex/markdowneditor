import boto3
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb.service_resource import Table

from lib import config
from lib.entities.node import Node
from lib.entities.tree import Tree
from lib.entities.user import User


class DynamoDBClient:
    def __init__(self):
        self._db_client: Table = boto3.resource("dynamodb").Table(config.TABLE_NAME)

    ###############################
    # For User
    ###############################
    def get_user(self, email: str) -> User | None:
        response = self._db_client.get_item(
            Key={
                "PK": f"EMAIL#{email}",
                "SK": "PROFILE",
            }
        )
        item = response.get("Item")
        if item is None:
            return None

        else:
            _email = item.pop("PK").replace("EMAIL#", "")
            entity = User(_email, item["password"], item["options"])
            return entity

    def put_user(self, user: User) -> None:
        self._db_client.put_item(
            Item={
                "PK": f"EMAIL#{user.email}",
                "SK": "PROFILE",
                "password": user.password,
                "options": user.options.json,
            }
        )

    ###############################
    # For Tree
    ###############################
    def get_tree(self, email: str) -> Tree | None:
        response = self._db_client.get_item(
            Key={
                "PK": f"EMAIL#{email}",
                "SK": "TREE",
            }
        )
        item = response.get("Item")
        if item is None:
            return None

        else:
            _email = item.pop("PK").replace("EMAIL#", "")
            entity = Tree(_email, item["node_tree"])
            return entity

    def put_tree(self, tree: Tree) -> None:
        self._db_client.put_item(
            Item={
                "PK": f"EMAIL#{tree.email}",
                "SK": "TREE",
                "node_tree": tree.node_tree.json,
            }
        )

    ###############################
    # For Node
    ###############################
    def get_node(self, email: str, node_id) -> Node | None:
        response = self._db_client.get_item(
            Key={
                "PK": f"EMAIL#{email}",
                "SK": f"NODE#{node_id}",
            }
        )
        item = response.get("Item")
        if item is None:
            return None

        else:
            _email = item.pop("PK").replace("EMAIL#", "")
            _node_id = item.pop("SK").replace("NODE#", "")
            entity = Node(_email, _node_id, item["text"])
            return entity

    def get_nodes(self, email: str) -> list[Node] | list:
        response = self._db_client.query(
            KeyConditionExpression=(
                Key("PK").eq(f"EMAIL#{email}") &
                Key("SK").begins_with("NODE#")
            )
        )
        items = response.get("Items", [])
        if items is []:
            return []

        else:
            entities = []
            for item in items:
                _email = item.pop("PK").replace("EMAIL#", "")
                _node_id = item.pop("SK").replace("NODE#", "")
                entity = Node(_email, _node_id, item["text"])
                entities.append(entity)
            return entities

    def put_node(self, node: Node) -> None:
        self._db_client.put_item(
            Item={
                "PK": f"EMAIL#{node.email}",
                "SK": f"NODE#{node.id}",
                "text": node.text,
            }
        )

    def delete_node(self, node: Node) -> None:
        self._db_client.delete_item(
            Key={
                "PK": f"EMAIL#{node.email}",
                "SK": f"NODE#{node.id}",
            }
        )
