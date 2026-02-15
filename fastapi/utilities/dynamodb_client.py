import boto3
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb import service_resource

import config
from models.group import Group
from models.node import Node
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
                groups=item["groups"],
                options=item["options"],
            )

    def put_user(self, user: User) -> None:
        self._db_client.put_item(
            Item={
                "PK": f"EMAIL#{user.email}",
                "SK": "USER",
                "password": user.password,
                "groups": [i.model_dump() for i in user.groups],
                "options": user.options.model_dump(),
            }
        )

    ###############################
    # For Group
    ###############################
    def get_group(self, group_id: str) -> Group | None:
        response = self._db_client.get_item(
            Key={
                "PK": f"GROUP_ID#{group_id}",
                "SK": "USER_GROUP",
            }
        )
        item = response.get("Item")

        if item is None:
            return None
        else:
            item["PK"] = item.pop("PK").removeprefix("GROUP_ID#")
            return Group(
                group_id=item["PK"],
                group_name=item["group_name"],
                users=item["users"],
            )

    ###############################
    # For Node
    ###############################
    def get_node(self, group_id: str, node_id: str) -> Node | None:
        response = self._db_client.get_item(
            Key={
                "PK": f"GROUP_ID#{group_id}",
                "SK": f"NODE#{node_id}",
            }
        )
        item = response.get("Item")

        if item is None:
            return None
        else:
            item["PK"] = item.pop("PK").removeprefix("GROUP_ID#")
            item["SK"] = item.pop("SK").removeprefix("NODE#")
            return Node(
                group_id=item["PK"],
                node_id=item["SK"],
                label=item["label"],
                text=item["text"],
                children_ids=item["children_ids"],
            )

    def get_nodes(self, group_id: str) -> list[Node]:
        response = self._db_client.query(
            KeyConditionExpression=(
                Key("PK").eq(f"GROUP_ID#{group_id}") & Key("SK").begins_with("NODE#")
            )
        )
        items = response.get("Items")

        entities = []
        for item in items:
            item["PK"] = item.pop("PK").removeprefix("GROUP_ID#")
            item["SK"] = item.pop("SK").removeprefix("NODE#")
            entities.append(
                Node(
                    group_id=item["PK"],
                    node_id=item["SK"],
                    label=item["label"],
                    text=item["text"],
                    children_ids=item["children_ids"],
                )
            )
        return entities

    def put_node(self, node: Node) -> None:
        self._db_client.put_item(
            Item={
                "PK": f"GROUP_ID#{node.group_id}",
                "SK": f"NODE#{node.node_id}",
                "label": node.label,
                "text": node.text,
                "children_ids": node.children_ids,
            }
        )

    def delete_node(self, node: Node) -> None:
        self._db_client.delete_item(
            Key={
                "PK": f"GROUP_ID#{node.group_id}",
                "SK": f"NODE#{node.node_id}",
            }
        )
