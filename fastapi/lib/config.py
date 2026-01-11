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
