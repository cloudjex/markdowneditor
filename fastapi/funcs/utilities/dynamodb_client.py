import boto3
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb import service_resource

import config
from funcs.entities.node import Node
from funcs.entities.tree import TreeInfo
from funcs.entities.user import User


class DynamoDBClient:
    def __init__(self):
        self._resource: service_resource = boto3.resource("dynamodb")
        self._db_client = self._resource.Table(config.TABLE_NAME)

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
                "options": user.options.to_dict(),
            }
        )

    ###############################
    # For TreeInfo
    ###############################
    def get_tree_info(self, email: str) -> TreeInfo | None:
        response = self._db_client.get_item(
            Key={
                "PK": f"EMAIL#{email}",
                "SK": "TREE_INFO",
            }
        )
        item = response.get("Item")

        if item is None:
            return None
        else:
            item["PK"] = item.pop("PK").removeprefix("EMAIL#")
            return TreeInfo(item["PK"], item["tree"])

    def put_tree_info(self, tree_info: TreeInfo) -> None:
        self._db_client.put_item(
            Item={
                "PK": f"EMAIL#{tree_info.email}",
                "SK": "TREE_INFO",
                "tree": tree_info.tree.to_dict(),
            }
        )

    ###############################
    # For Node
    ###############################
    def get_node(self, email: str, node_id: str) -> Node | None:
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
                "SK": f"NODE#{node.node_id}",
                "text": node.text,
            }
        )

    def delete_node(self, node: Node) -> None:
        self._db_client.delete_item(
            Key={
                "PK": f"EMAIL#{node.email}",
                "SK": f"NODE#{node.node_id}",
            }
        )
