import pytest

import app
from fastapi.testclient import TestClient
from utilities.jwt_client import JwtClient

# Test Accounts
EMAIL = "test@gmail.com"
PASSWORD = "test"
GROUP_ID = "a4baa583-f327-47db-a989-0a9e0386f2a2"
NONUSER_EMAIL = "nonuser@gmail.com"


fa_client = TestClient(app.app)


@pytest.fixture(scope="session")
def root_node_id(id_token):
    res = fa_client.get(
        url="/api/tree",
        headers={"Authorization": id_token},
    )
    assert res.status_code == 200

    body: dict = res.json()
    assert type(body) is dict
    assert type(body["node_id"]) is str
    return body["node_id"]


@pytest.fixture(scope="session")
def id_token():
    return f"Bearer {JwtClient().encode(EMAIL, GROUP_ID)}"


@pytest.fixture(scope="session")
def user_token():
    return f"Bearer {JwtClient().encode(EMAIL)}"


@pytest.fixture(scope="session")
def invalid_id_token():
    return "Bearer invalid_token"
