import os

# jwt settings
JWT_KEY = os.environ.get("JWT_KEY", "cloudjex.jwt.secret")
APP_URL = os.environ.get("APP_URL", "cloudjex.com")

# dynamodb settings
USER_TABLE_NAME = "cloudjex-users"
TREE_TABLE_NAME = "cloudjex-trees"
NODES_TABLE_NAME = "cloudjex-nodes"
