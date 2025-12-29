import json
import logging

import pytest

from lib.utilities import jwt

_logger = logging.getLogger('Logger')
_logger.setLevel(logging.INFO)
_console_handler = logging.StreamHandler()
_formatter = logging.Formatter('[%(levelname)s][%(filename)s:%(lineno)d] %(message)s')
_console_handler.setFormatter(_formatter)
_logger.addHandler(_console_handler)

EMAIL = "test@gmail.com"
NONUSER_EMAIL = "nonuser@gmail.com"


def logger(x):
    res = json.dumps(x, indent=2, ensure_ascii=False)
    _logger.info(res, stacklevel=2)


@pytest.fixture
def id_token():
    return jwt.generate_jwt(EMAIL)


@pytest.fixture
def invalid_id_token():
    return "invalid_token"


@pytest.fixture
def nonuser_id_token():
    return jwt.generate_jwt(NONUSER_EMAIL)
