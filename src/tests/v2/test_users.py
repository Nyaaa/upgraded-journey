import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import schemas, models
from app.api.v2 import routes
from tests.sample_data import USER2, USER

URL = "/v2/users/"


@pytest.mark.asyncio
async def test_users_get_all(client: AsyncClient, create_user: models.User):
    response = await client.get(URL)
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_users_get_one(async_session: AsyncSession, create_user: models.User):
    user = await routes.read_user_by_id(user_id=1, db=async_session)
    assert user.id == 1


@pytest.mark.asyncio
async def test_users_post(async_session: AsyncSession):
    user = schemas.UserCreate(**USER2 | {"password": "string", "phone": "+7 111 11 11"})
    response = await routes.create_user(db=async_session, user=user)
    assert response.email == USER2["email"]
    assert response.is_active is True
    assert response.phone == "+71111111"


@pytest.mark.asyncio
async def test_users_wrong_phone(client: AsyncClient):
    user = USER2 | {"password": "string", "phone": "111"}
    response = await client.post(url=URL, json=user)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Invalid phone number format"


@pytest.mark.asyncio
async def test_users_duplicate_email(
    async_session: AsyncSession, create_user: models.User
):
    user = schemas.UserCreate(**USER | {"password": "string"})
    with pytest.raises(HTTPException) as err:
        await routes.create_user(db=async_session, user=user)
    assert err.value.status_code == 400
    assert err.value.detail == {"status": 400, "message": "Email already registered"}


@pytest.mark.asyncio
async def test_user_not_found(async_session: AsyncSession):
    with pytest.raises(HTTPException) as err:
        await routes.read_user_by_id(db=async_session, user_id=10)
    assert err.value.status_code == 404
    assert err.value.detail == {"status": 404, "message": "User not found"}


@pytest.mark.asyncio
async def test_login(create_user: models.User, async_session: AsyncSession):
    form = OAuth2PasswordRequestForm(
        username=create_user.email, password="string", scope=""
    )
    token = await routes.login(form, async_session)
    assert token
    return token


@pytest.mark.asyncio
async def test_login_failed(async_session: AsyncSession):
    form = OAuth2PasswordRequestForm(username="", password="", scope="")
    with pytest.raises(HTTPException) as err:
        await routes.login(form, async_session)
    assert err.value.status_code == 401


@pytest.mark.asyncio
async def test_get_restricted_access(
    client: AsyncClient, create_user: models.User, async_session: AsyncSession
):
    token = await test_login(create_user, async_session)
    key = token["access_token"]
    response = await client.get(
        url=f"{URL}me/", headers={"Authorization": f"Bearer {key}"}
    )
    assert response.status_code == 200
