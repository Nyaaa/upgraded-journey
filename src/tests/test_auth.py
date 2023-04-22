import pytest
from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app import hasher, auth
from app.api import models


@pytest.mark.asyncio
async def test_hash():
    password = "password"
    hashed = hasher.str_to_hash(password)
    assert hasher.verify(password, hashed)


@pytest.mark.asyncio
async def test_auth_passed(async_session: AsyncSession, create_user: models.User):
    cred = HTTPBasicCredentials(username="test@example.com", password="string")
    verified = await auth.get_current_user(credentials=cred, _db=async_session)
    assert verified == create_user


@pytest.mark.asyncio
async def test_auth_failed_username(async_session: AsyncSession):
    cred = HTTPBasicCredentials(username="111@example.com", password="string")
    with pytest.raises(HTTPException) as err:
        await auth.get_current_user(credentials=cred, _db=async_session)
    assert err.value.status_code == 401
    assert err.value.detail == "Incorrect email or password"


@pytest.mark.asyncio
async def test_auth_failed_password(
    async_session: AsyncSession, create_user: models.User
):
    cred = HTTPBasicCredentials(username="test@example.com", password="qwerty")
    with pytest.raises(HTTPException) as err:
        await auth.get_current_user(credentials=cred, _db=async_session)
    assert err.value.status_code == 401
    assert err.value.detail == "Incorrect email or password"
