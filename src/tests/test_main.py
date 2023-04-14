from app.db import get_db


def test_health_check(client):
    for index in ("/", "/v1/", "/v2/"):
        response = client.get(index)
        assert response.status_code == 200


def test_db(client):
    db = next(get_db())
    assert db.bind.url.database == 'FSTR'
