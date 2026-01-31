import pytest

import app
from fastapi.testclient import TestClient
from funcs.utilities.jwt_client import JwtClient

EMAIL = "test@gmail.com"
NONUSER_EMAIL = "nonuser@gmail.com"


fa_client = TestClient(app.app)


@pytest.fixture(scope="session")
def root_node_id(id_token):
    res = fa_client.get(
        url="/api/tree",
        headers={"Authorization": id_token}
    )
    assert res.status_code == 200

    body: dict = res.json()
    assert type(body) is dict
    assert type(body["node_id"]) is str
    return body["node_id"]


@pytest.fixture(scope="session")
def id_token():
    return f"Bearer {JwtClient().encode(EMAIL)}"


@pytest.fixture(scope="session")
def invalid_id_token():
    return "Bearer invalid_token"


@pytest.fixture(scope="session")
def nonuser_id_token():
    return f"Bearer {JwtClient().encode(NONUSER_EMAIL)}"
