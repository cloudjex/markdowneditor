import pytest

from funcs.utilities.jwt_client import JwtClient

EMAIL = "test@gmail.com"
NONUSER_EMAIL = "nonuser@gmail.com"
ROOT_NODE_ID = "1b92557a-74cb-4553-a791-529286d3b795"


@pytest.fixture
def id_token():
    return JwtClient().generate_jwt(EMAIL)


@pytest.fixture
def invalid_id_token():
    return "invalid_token"


@pytest.fixture
def nonuser_id_token():
    return JwtClient().generate_jwt(NONUSER_EMAIL)
