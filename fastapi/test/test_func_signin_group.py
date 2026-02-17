import pytest

from utilities.jwt_client import JwtClient

from .conftest import EMAIL, GROUP_ID, fa_client


@pytest.fixture()
def user_token():
    print("\nsetup...")
    id_token = JwtClient().encode(EMAIL)

    yield id_token

    print("\nteardown...")


class TestSuccessPost:
    def test_signin_group_with_user_token(self, user_token):
        res = fa_client.post(
            url="/api/signin/group",
            headers={"Authorization": user_token},
            json={
                "group_id": GROUP_ID,
            },
        )
        assert res.status_code == 200
        body: dict = res.json()

        assert type(body["id_token"]) is str

    def test_signin_group_with_group_token(self, id_token):
        res = fa_client.post(
            url="/api/signin/group",
            headers={"Authorization": id_token},
            json={
                "group_id": GROUP_ID,
            },
        )
        assert res.status_code == 200
        body: dict = res.json()

        assert type(body["id_token"]) is str


class TestFailPost:
    def test_with_invalid_token(self, invalid_id_token):
        res = fa_client.post(
            url="/api/signin/group",
            headers={"Authorization": invalid_id_token},
            json={
                "group_id": GROUP_ID,
            },
        )
        assert res.status_code == 401

    def test_with_bad_request(self, user_token):
        res = fa_client.post(
            url="/api/signin/group",
            headers={"Authorization": user_token},
            json={},
        )
        assert res.status_code == 422
