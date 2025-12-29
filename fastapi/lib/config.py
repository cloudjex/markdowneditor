import os

# jwt settings
JWT_KEY = os.environ.get("JWT_KEY", "cloudjex.jwt.secret")
APP_URL = os.environ.get("APP_URL", "cloudjex.com")

# dynamodb settings
USER_TABLE_NAME = "cloudjex-users-table"
TREE_TABLE_NAME = "cloudjex-trees-table"
NODES_TABLE_NAME = "cloudjex-nodes-table"

# smtp settings
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
