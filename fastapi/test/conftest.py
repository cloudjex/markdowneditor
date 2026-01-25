import pytest

import app
from fastapi.testclient import TestClient
from funcs.utilities.jwt_client import JwtClient

EMAIL = "test@gmail.com"
NONUSER_EMAIL = "nonuser@gmail.com"
ROOT_NODE_ID = "1b92557a-74cb-4553-a791-529286d3b795"


fa_client = TestClient(app.app)


@pytest.fixture(scope="session")
def id_token():
    return f"Bearer {JwtClient().encode(EMAIL)}"


@pytest.fixture(scope="session")
def invalid_id_token():
    return "Bearer invalid_token"


@pytest.fixture(scope="session")
def nonuser_id_token():
    return f"Bearer {JwtClient().encode(NONUSER_EMAIL)}"
