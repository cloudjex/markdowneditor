import boto3
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb.service_resource import Table

from lib import config


class BaseDynamoDBClient:
    def __init__(self, table: str):
        self._dynamodb_client: Table = boto3.resource("dynamodb").Table(table)


class UserTableClient(BaseDynamoDBClient):
    def __init__(self):
        super().__init__(config.USERS_TABLE_NAME)

    def get_user(self, email: str) -> dict | None:
        response = self._dynamodb_client.get_item(
            Key={"email": email}
        )
        return response.get("Item")

    def put_user(self, email: str, password: str, options: dict) -> None:
        self._dynamodb_client.put_item(
            Item={
                "email": email,
                "password": password,
                "options": options,
            }
        )


class TreeTableClient(BaseDynamoDBClient):
    def __init__(self):
        super().__init__(config.TREES_TABLE_NAME)

    def get_tree(self, email: str) -> dict | None:
        response = self._dynamodb_client.get_item(
            Key={"email": email}
        )
        return response.get("Item")

    def put_tree(self, email: str, tree: dict) -> None:
        self._dynamodb_client.put_item(
            Item={
                "email": email,
                "tree": tree,
            }
        )


class NodeTableClient(BaseDynamoDBClient):
    def __init__(self):
        super().__init__(config.NODES_TABLE_NAME)

    def get_node(self, email: str, node_id) -> dict | None:
        response = self._dynamodb_client.get_item(
            Key={
                "email": email,
                "id": node_id,
            }
        )
        return response.get("Item")

    def get_nodes(self, email: str) -> list[dict]:
        response = self._dynamodb_client.query(
            KeyConditionExpression=Key("email").eq(email)
        )
        return response.get("Items", [])

    def put_node(self, email: str, node_id: str, text: str) -> None:
        self._dynamodb_client.put_item(
            Item={
                "email": email,
                "id": node_id,
                "text": text,
            }
        )

    def delete_node(self, email: str, node_id: str) -> None:
        self._dynamodb_client.delete_item(
            Key={
                "email": email,
                "id": node_id,
            }
        )
