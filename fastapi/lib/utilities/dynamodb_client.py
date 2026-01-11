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
            item["PK"] = item.pop("PK").removeprefix("EMAIL#")
            return User(item["PK"], item["password"], item["options"])

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
            item["PK"] = item.pop("PK").removeprefix("EMAIL#")
            return Tree(item["PK"], item["node_tree"])

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
            item["PK"] = item.pop("PK").removeprefix("EMAIL#")
            item["SK"] = item.pop("SK").removeprefix("NODE#")
            return Node(item["PK"], item["SK"], item["text"])

    def get_nodes(self, email: str) -> list[Node] | None:
        response = self._db_client.query(
            KeyConditionExpression=(
                Key("PK").eq(f"EMAIL#{email}") &
                Key("SK").begins_with("NODE#")
            )
        )
        items = response.get("Items")

        if items is None:
            return None
        else:
            entities = []
            for item in items:
                item["PK"] = item.pop("PK").removeprefix("EMAIL#")
                item["SK"] = item.pop("SK").removeprefix("NODE#")
                entities.append(Node(item["PK"], item["SK"], item["text"]))
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
