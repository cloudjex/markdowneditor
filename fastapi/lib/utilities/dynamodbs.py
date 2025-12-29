import boto3
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb.service_resource import Table

from lib import config


def _get_table(table_name: str) -> Table:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    return table


def get_user(email: str) -> dict:
    try:
        table = _get_table(config.USER_TABLE_NAME)

        response = table.get_item(
            Key={"email": email}
        )

        return response.get("Item")

    except Exception as e:
        raise e


def put_user(email: str, password: str, options: dict) -> dict:
    try:
        table = _get_table(config.USER_TABLE_NAME)

        table.put_item(
            Item={
                "email": email,
                "password": password,
                "options": options,
            }
        )

    except Exception as e:
        raise e


def get_tree(email: str) -> dict:
    try:
        table = _get_table(config.TREE_TABLE_NAME)

        response = table.get_item(
            Key={"email": email}
        )

        return response.get("Item")

    except Exception as e:
        raise e


def put_tree(email: str, tree: dict) -> dict:
    try:
        table = _get_table(config.TREE_TABLE_NAME)

        table.put_item(
            Item={
                "email": email,
                "tree": tree,
            }
        )

    except Exception as e:
        raise e


def get_node(email: str, node_id) -> dict:
    try:
        table = _get_table(config.NODES_TABLE_NAME)

        response = table.get_item(
            Key={
                "email": email,
                "id": node_id,
            }
        )

        return response.get("Item")

    except Exception as e:
        raise e


def get_nodes(email: str) -> dict:
    try:
        table = _get_table(config.NODES_TABLE_NAME)

        response = table.query(
            KeyConditionExpression=Key("email").eq(email)
        )

        items = response.get("Items", [])

        return items

    except Exception as e:
        raise e


def put_node(email: str, node_id: str, text: str) -> dict:
    try:
        table = _get_table(config.NODES_TABLE_NAME)

        table.put_item(
            Item={
                "email": email,
                "id": node_id,
                "text": text,
            }
        )

    except Exception as e:
        raise e


def delete_node(email: str, node_id: str) -> dict:
    try:
        table = _get_table(config.NODES_TABLE_NAME)

        table.delete_item(
            Key={
                "email": email,
                "id": node_id,
            }
        )

    except Exception as e:
        raise e
