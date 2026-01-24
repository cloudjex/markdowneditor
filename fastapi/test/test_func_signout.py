import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


class TestSuccessPost:
    def test_func_signout_normal(self, id_token):
        res = client.post(
            url="/api/signout",
            headers={"Authorization": f"Bearer {id_token}"}
        )
        assert res.status_code == 200


class TestFailPost:
    def test_func_signout_no_token(self):
        res = client.post(
            url="/api/signout",
        )
        assert res.status_code == 401

    def test_func_signout_invalid_token(self, invalid_id_token):
        res = client.post(
            url="/api/signout",
            headers={"Authorization": f"Bearer {invalid_id_token}"}
        )
        assert res.status_code == 401
