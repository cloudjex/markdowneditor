import boto3
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb import service_resource

import config
from models.node import Node
from models.tree import TreeInfo
from models.user import User


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
                "SK": "USER",
            }
        )
        item = response.get("Item")

        if item is None:
            return None
        else:
            item["PK"] = item.pop("PK").removeprefix("EMAIL#")
            return User(
                email=item["PK"],
                password=item["password"],
                user_groups=item["user_groups"],
                options=item["options"],
            )

    def put_user(self, user: User) -> None:
        self._db_client.put_item(
            Item={
                "PK": f"EMAIL#{user.email}",
                "SK": "USER",
                "password": user.password,
                "user_groups": [i.model_dump() for i in user.user_groups],
                "options": user.options.model_dump(),
            }
        )

    ###############################
    # For TreeInfo
    ###############################
    def get_tree_info(self, user_group: str) -> TreeInfo | None:
        response = self._db_client.get_item(
            Key={
                "PK": f"GROUP_NAME#{user_group}",
                "SK": "TREE_INFO",
            }
        )
        item = response.get("Item")

        if item is None:
            return None
        else:
            item["PK"] = item.pop("PK").removeprefix("GROUP_NAME#")
            return TreeInfo(user_group=item["PK"], tree=item["tree"])

    def put_tree_info(self, tree_info: TreeInfo) -> None:
        self._db_client.put_item(
            Item={
                "PK": f"GROUP_NAME#{tree_info.user_group}",
                "SK": "TREE_INFO",
                "tree": tree_info.tree.model_dump(),
            }
        )

    ###############################
    # For Node
    ###############################
    def get_node(self, user_group: str, node_id: str) -> Node | None:
        response = self._db_client.get_item(
            Key={
                "PK": f"GROUP_NAME#{user_group}",
                "SK": f"NODE#{node_id}",
            }
        )
        item = response.get("Item")

        if item is None:
            return None
        else:
            item["PK"] = item.pop("PK").removeprefix("GROUP_NAME#")
            item["SK"] = item.pop("SK").removeprefix("NODE#")
            return Node(user_group=item["PK"], node_id=item["SK"], text=item["text"])

    def get_nodes(self, user_group: str) -> list[Node]:
        response = self._db_client.query(
            KeyConditionExpression=(
                Key("PK").eq(f"GROUP_NAME#{user_group}")
                & Key("SK").begins_with("NODE#")
            )
        )
        items = response.get("Items")

        entities = []
        for item in items:
            item["PK"] = item.pop("PK").removeprefix("GROUP_NAME#")
            item["SK"] = item.pop("SK").removeprefix("NODE#")
            entities.append(
                Node(user_group=item["PK"], node_id=item["SK"], text=item["text"])
            )
        return entities

    def put_node(self, node: Node) -> None:
        self._db_client.put_item(
            Item={
                "PK": f"GROUP_NAME#{node.user_group}",
                "SK": f"NODE#{node.node_id}",
                "text": node.text,
            }
        )

    def delete_node(self, node: Node) -> None:
        self._db_client.delete_item(
            Key={
                "PK": f"GROUP_NAME#{node.user_group}",
                "SK": f"NODE#{node.node_id}",
            }
        )
