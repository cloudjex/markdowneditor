from .conftest import GROUP_ID, fa_client


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
