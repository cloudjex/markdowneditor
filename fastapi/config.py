import os

# jwt settings
JWT_KEY = os.environ.get("JWT_KEY", "local.test")
APP_URL = "www.cloudjex.com"

# dynamodb settings
TABLE_NAME = "cloudjex-table"

# smtp settings
SMTP_HOST = "smtp.resend.com"
SMTP_PORT = 587
SMTP_USER = "resend"
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

# For API Document
RES_400 = {"description": "BadRequest Error"}
RES_401 = {"description": "Unauthorized Error"}
RES_403 = {"description": "Forbidden Error"}
RES_404 = {"description": "NotFound Error"}
RES_409 = {"description": "Conflict Error"}
RES_422 = {"description": "Validation Error"}
