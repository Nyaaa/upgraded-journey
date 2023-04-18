import pytest
from httpx import AsyncClient

from app import hasher
from tests.sample_data import USER2, USER

URL = '/v2/users/'


@pytest.mark.asyncio
async def test_users_get_all(client: AsyncClient, create_user):
    response = await client.get(URL)
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_users_get_one(client, create_user):
    response = await client.get(f'{URL}1')
    assert response.status_code == 200
    assert response.json()['id'] == 1


@pytest.mark.asyncio
async def test_users_post(client):
    user = USER2 | {"password": "string", "phone": "+7 111 11 11"}
    response = await client.post(url=URL, json=user)
    assert response.status_code == 200
    assert response.json()["email"] == USER2['email']
    assert response.json()["is_active"] is True
    assert response.json()["phone"] == "+71111111"


@pytest.mark.asyncio
async def test_users_wrong_phone(client):
    user = USER2 | {"password": "string", "phone": "111"}
    response = await client.post(url=URL, json=user)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Invalid phone number format"


@pytest.mark.asyncio
async def test_hash(client):
    password = 'password'
    hashed = hasher.str_to_hash(password)
    assert hasher.verify(password, hashed)


@pytest.mark.asyncio
async def test_users_duplicate_email(client, create_user):
    user = USER | {"password": "string"}
    response = await client.post(url=URL, json=user)
    assert response.status_code == 400
    assert response.json()['detail'] == {'status': 400, 'message': 'Email already registered'}


@pytest.mark.asyncio
async def test_user_not_found(client):
    response = await client.get(f'{URL}10')
    assert response.status_code == 404
    assert response.json()['detail'] == {'status': 404, 'message': 'User not found'}
