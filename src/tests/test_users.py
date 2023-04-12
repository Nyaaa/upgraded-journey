def test_users_get_all(client, create_user):
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_users_get_one(client, create_user):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()['id'] == 1


def test_users_post(client):
    user = {
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "password": "string"
    }
    response = client.post(url="/users/", json=user)
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"
    assert response.json()["is_active"] is True
