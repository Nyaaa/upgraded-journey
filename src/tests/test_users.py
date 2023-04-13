from app import hasher

URL = '/v2/users/'


def test_users_get_all(client, create_user):
    response = client.get(URL)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_users_get_one(client, create_user):
    response = client.get(f'{URL}1')
    assert response.status_code == 200
    assert response.json()['id'] == 1


def test_users_post(client):
    user = {
        "email": "user1@example.com",
        "first_name": "string",
        "last_name": "string",
        "phone": "+7 111 11 11",
        "password": "string"
    }
    response = client.post(url=URL, json=user)
    assert response.status_code == 200
    assert response.json()["email"] == "user1@example.com"
    assert response.json()["is_active"] is True
    assert response.json()["phone"] == "+71111111"


def test_users_wrong_phone(client):
    user = {
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "phone": "111",
        "password": "string"
    }
    response = client.post(url=URL, json=user)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Invalid phone number format"


def test_hash(client):
    password = 'password'
    hashed = hasher.str_to_hash(password)
    assert hasher.verify(password, hashed)


def test_users_duplicate_email(client, create_user):
    user = {
        "email": "test@example.com",
        "first_name": "string",
        "last_name": "string",
        "password": "string"
    }
    response = client.post(url=URL, json=user)
    assert response.status_code == 400
    assert response.json()['message'] == 'Email already registered'


def test_user_not_found(client):
    response = client.get(f'{URL}10')
    assert response.status_code == 404
    assert response.json()['message'] == 'User not found'
