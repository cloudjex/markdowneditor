import boto3
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb.service_resource import Table

from lib import config
from lib.entities import node, tree, user


class DynamoDBClient:
    def __init__(self):
        self._db_client: Table = boto3.resource("dynamodb").Table(config.TABLE_NAME)

    ###############################
    # For User
    ###############################
    def get_user(self, email: str) -> user.User | None:
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
            entity = user.User(_email, item["password"], item["options"])
            return entity

    def put_user(self, email: str, password: str, options: dict) -> None:
        self._db_client.put_item(
            Item={
                "PK": f"EMAIL#{email}",
                "SK": "PROFILE",
                "password": password,
                "options": options,
            }
        )

    ###############################
    # For Tree
    ###############################
    def get_tree(self, email: str) -> tree.Tree | None:
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
            entity = tree.Tree(_email, item["tree"])
            return entity

    def put_tree(self, email: str, tree: dict) -> None:
        self._db_client.put_item(
            Item={
                "PK": f"EMAIL#{email}",
                "SK": "TREE",
                "tree": tree,
            }
        )

    ###############################
    # For Node
    ###############################
    def get_node(self, email: str, node_id) -> tree.Tree | None:
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
            entity = node.Node(_email, _node_id, item["text"])
            return entity

    def get_nodes(self, email: str) -> list[node.Node] | list:
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
                entity = node.Node(_email, _node_id, item["text"])
                entities.append(entity)
            return entities

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
