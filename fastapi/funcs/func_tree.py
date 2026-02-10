from funcs.utilities.dynamodb_client import DynamoDBClient


def get_tree(user_group: str) -> dict:
    db_client = DynamoDBClient()
    tree_info = db_client.get_tree_info(user_group)

    return tree_info.tree.model_dump()
