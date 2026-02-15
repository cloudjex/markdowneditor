import pytest

from utilities.jwt_client import JwtClient

from .conftest import EMAIL, USER_GROUP, fa_client


@pytest.fixture()
def plain_id_token():
    print("\nsetup...")
    id_token = JwtClient().encode(EMAIL)

    yield id_token

    print("\nteardown...")


class TestSuccessPost:
    def test_func_signin_group_with_plain_token(self, plain_id_token):
        res = fa_client.post(
            url="/api/signin/group",
            headers={"Authorization": plain_id_token},
            json={
                "user_group": USER_GROUP,
            },
        )
        assert res.status_code == 200
        body: dict = res.json()

        assert type(body["id_token"]) is str

    def test_func_signin_group_with_group_token(self, id_token):
        res = fa_client.post(
            url="/api/signin/group",
            headers={"Authorization": id_token},
            json={
                "user_group": USER_GROUP,
            },
        )
        assert res.status_code == 200
        body: dict = res.json()

        assert type(body["id_token"]) is str


class TestFailPost:
    def test_func_signin_group_invalid_token(self, invalid_id_token):
        res = fa_client.post(
            url="/api/signin/group",
            headers={"Authorization": invalid_id_token},
            json={
                "user_group": USER_GROUP,
            },
        )
        assert res.status_code == 401

    def test_func_signin_group_bad_request(self, plain_id_token):
        res = fa_client.post(
            url="/api/signin/group",
            headers={"Authorization": plain_id_token},
            json={},
        )
        assert res.status_code == 422
