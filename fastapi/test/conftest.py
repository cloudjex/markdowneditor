import pytest

import app
from fastapi.testclient import TestClient
from lib.jwt_client import JwtClient

# Test Accounts
EMAIL = "test@cloudjex.com"
PASSWORD = "test"
GROUP_ID = "a4baa583-f327-47db-a989-0a9e0386f2a2"

fa_client = TestClient(app.app)


@pytest.fixture(scope="session")
def root_node_id(id_token):
    res = fa_client.get(
        url="/api/tree",
        headers={"Authorization": id_token},
    )
    assert res.status_code == 200
    body: dict = res.json()
    return body["node_id"]


@pytest.fixture(scope="session")
def id_token():
    return f"Bearer {JwtClient().encode(EMAIL, GROUP_ID)}"


@pytest.fixture(scope="session")
def user_token():
    return f"Bearer {JwtClient().encode(EMAIL)}"


@pytest.fixture(scope="session")
def invalid_id_token():
    # expired token
    return "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAY2xvdWRqZXguY29tIiwiZ3JvdXBfaWQiOiJhNGJhYTU4My1mMzI3LTQ3ZGItYTk4OS0wYTllMDM4NmYyYTIiLCJpc3MiOiJ3d3cuY2xvdWRqZXguY29tIiwiYXVkIjoid3d3LmNsb3VkamV4LmNvbSIsImlhdCI6MTc3MTMyNDU5MSwiZXhwIjoxNzcxMzI4MTkxfQ.WTr84SqVsspaRLlOD62oZv0JQiwxbC9r0dhEsEbt2Qg"
