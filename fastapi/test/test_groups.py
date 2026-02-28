import time

from .conftest import EMAIL, GROUP_ID, fa_client


class TestGetGroupsSuccess:
    def test_get_groups(self, id_token):
        res = fa_client.get(
            url="/api/groups",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200
        body: list = res.json()
        assert type(body) is list
        assert type(body[0]["group_id"]) is str
        assert type(body[0]["group_name"]) is str
        assert type(body[0]["users"]) is list
        assert type(body[0]["users"][0]) is dict
        assert type(body[0]["users"][0]["email"]) is str
        assert type(body[0]["users"][0]["role"]) is str

    def test_get_group(self, id_token):
        res = fa_client.get(
            url=f"/api/groups/{GROUP_ID}",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200
        body = res.json()
        assert type(body) is dict
        assert body["group_id"] == GROUP_ID
        assert type(body["group_name"]) is str
        assert type(body["users"]) is list
        assert type(body["users"][0]) is dict
        assert type(body["users"][0]["email"]) is str
        assert type(body["users"][0]["role"]) is str


class TestGetGroupsFail:
    def test_with_invalid_token(self, invalid_id_token):
        res = fa_client.get(
            url="/api/groups",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401

    def test_get_non_exist_group(self, id_token):
        res = fa_client.get(
            url=f"/api/groups/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 404


class TestPostGroupsSuccess:
    def test_post_group(self, id_token):
        group_name = str(time.time())
        res = fa_client.post(
            url="/api/groups",
            headers={"Authorization": id_token},
            json={
                "group_name": group_name,
            },
        )
        assert res.status_code == 200
        body = res.json()
        group_id = body["group_id"]
        assert type(group_id) is str
        assert body["group_name"] == group_name

        # check if group is added to db
        res = fa_client.get(
            url="/api/groups",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200
        body: list = res.json()

        group = next((g for g in body if g["group_id"] == group_id), None)
        assert group is not None
        assert group["users"][0]["email"] == EMAIL
        assert group["users"][0]["role"] == "admin"

        # check if group is added to user's groups
        res = fa_client.get(
            url="/api/users/me",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200
        body = res.json()
        assert type(body["groups"]) is list
        assert body["groups"][-1] == group_id


class TestPostGroupsFail:
    def test_with_invalid_token(self, invalid_id_token):
        res = fa_client.post(
            url="/api/groups",
            headers={"Authorization": invalid_id_token},
            json={
                "group_name": "Test",
            },
        )
        assert res.status_code == 401

    def test_with_invalid_body(self, id_token):
        res = fa_client.post(
            url="/api/groups",
            headers={"Authorization": id_token},
            json={
                "group_name": "",
            },
        )
        assert res.status_code == 422

    def test_with_missing_group_name(self, id_token):
        res = fa_client.post(
            url="/api/groups",
            headers={"Authorization": id_token},
            json={},
        )
        assert res.status_code == 422
