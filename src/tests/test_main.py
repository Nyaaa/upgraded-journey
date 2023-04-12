from app import main


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200


def test_db(client):
    db = next(main.get_db())
    assert db.bind.url.database == 'FSTR'
