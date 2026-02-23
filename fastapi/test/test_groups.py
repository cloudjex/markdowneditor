import time

from .conftest import fa_client


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


class TestGetGroupsFail:
    def test_with_invalid_token(self, invalid_id_token):
        res = fa_client.get(
            url="/api/groups",
            headers={"Authorization": invalid_id_token},
        )
        assert res.status_code == 401


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
        assert any(group["group_id"] == group_id for group in body)

        # check if group is added to user's groups
        res = fa_client.get(
            url="/api/users/me",
            headers={"Authorization": id_token},
        )
        assert res.status_code == 200
        body = res.json()
        assert type(body["groups"]) is list
        assert body["groups"][-1]["group_id"] == group_id


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
