import boto3
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb.service_resource import Table

from lib import config


class DynamoDBClient:
    def __init__(self):
        self._db_client: Table = boto3.resource("dynamodb").Table(config.TABLE_NAME)

    def get_user(self, email: str) -> dict | None:
        response = self._db_client.get_item(
            Key={
                "PK": f"EMAIL#{email}",
                "SK": "PROFILE",
            }
        )
        item = response.get("Item")

        if item:
            item["email"] = item.pop("PK").replace("EMAIL#", "")
            item.pop("SK")
        return item

    def put_user(self, email: str, password: str, options: dict) -> None:
        self._db_client.put_item(
            Item={
                "PK": f"EMAIL#{email}",
                "SK": "PROFILE",
                "password": password,
                "options": options,
            }
        )

    def get_tree(self, email: str) -> dict | None:
        response = self._db_client.get_item(
            Key={
                "PK": f"EMAIL#{email}",
                "SK": "TREE",
            }
        )
        item = response.get("Item")

        if item:
            item["email"] = item.pop("PK").replace("EMAIL#", "")
            item.pop("SK")
        return item

    def put_tree(self, email: str, tree: dict) -> None:
        self._db_client.put_item(
            Item={
                "PK": f"EMAIL#{email}",
                "SK": "TREE",
                "tree": tree,
            }
        )

    def get_node(self, email: str, node_id) -> dict | None:
        response = self._db_client.get_item(
            Key={
                "PK": f"EMAIL#{email}",
                "SK": f"NODE#{node_id}",
            }
        )
        item = response.get("Item")

        if item:
            item["email"] = item.pop("PK").replace("EMAIL#", "")
            item["id"] = item.pop("SK").replace("NODE#", "")
        return item

    def get_nodes(self, email: str) -> list[dict]:
        response = self._db_client.query(
            KeyConditionExpression=(
                Key("PK").eq(f"EMAIL#{email}") &
                Key("SK").begins_with("NODE#")
            )
        )
        items = response.get("Items", [])

        for item in items:
            item["email"] = item.pop("PK").replace("EMAIL#", "")
            item["id"] = item.pop("SK").replace("NODE#", "")
        return items

    def put_node(self, email: str, node_id: str, text: str) -> None:
        self._db_client.put_item(
            Item={
                "PK": f"EMAIL#{email}",
                "SK": f"NODE#{node_id}",
                "text": text,
            }
        )

    def delete_node(self, email: str, node_id: str) -> None:
        self._db_client.delete_item(
            Key={
                "PK": f"EMAIL#{email}",
                "SK": f"NODE#{node_id}",
            }
        )
