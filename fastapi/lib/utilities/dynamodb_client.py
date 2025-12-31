import boto3
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb.service_resource import Table

from lib import config


class BaseDynamoDBClient:
    def __init__(self, table_name: str):
        self._dynamodb_client: Table = boto3.resource("dynamodb").Table(table_name)


class UserTableClient(BaseDynamoDBClient):
    def __init__(self):
        super().__init__(config.USERS_TABLE_NAME)

    def get_user(self, email: str) -> dict | None:
        try:
            response = self._dynamodb_client.get_item(
                Key={"email": email}
            )
            return response.get("Item")

        except Exception as e:
            raise e

    def put_user(self, email: str, password: str, options: dict) -> None:
        try:
            self._dynamodb_client.put_item(
                Item={
                    "email": email,
                    "password": password,
                    "options": options,
                }
            )

        except Exception as e:
            raise e


class TreeTableClient(BaseDynamoDBClient):
    def __init__(self):
        super().__init__(config.TREES_TABLE_NAME)

    def get_tree(self, email: str) -> dict | None:
        try:
            response = self._dynamodb_client.get_item(
                Key={"email": email}
            )
            return response.get("Item")

        except Exception as e:
            raise e

    def put_tree(self, email: str, tree: dict) -> None:
        try:
            self._dynamodb_client.put_item(
                Item={
                    "email": email,
                    "tree": tree,
                }
            )

        except Exception as e:
            raise e


class NodeTableClient(BaseDynamoDBClient):
    def __init__(self):
        super().__init__(config.NODES_TABLE_NAME)

    def get_node(self, email: str, node_id) -> dict | None:
        try:
            response = self._dynamodb_client.get_item(
                Key={
                    "email": email,
                    "id": node_id,
                }
            )
            return response.get("Item")

        except Exception as e:
            raise e

    def get_nodes(self, email: str) -> list[dict]:
        try:
            response = self._dynamodb_client.query(
                KeyConditionExpression=Key("email").eq(email)
            )

            items = response.get("Items", [])
            return items

        except Exception as e:
            raise e

    def put_node(self, email: str, node_id: str, text: str) -> None:
        try:
            self._dynamodb_client.put_item(
                Item={
                    "email": email,
                    "id": node_id,
                    "text": text,
                }
            )

        except Exception as e:
            raise e

    def delete_node(self, email: str, node_id: str) -> None:
        try:
            self._dynamodb_client.delete_item(
                Key={
                    "email": email,
                    "id": node_id,
                }
            )

        except Exception as e:
            raise e
