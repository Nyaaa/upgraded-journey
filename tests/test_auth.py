from datetime import timedelta

import pytest
from fastapi import HTTPException
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app import auth
from app.api import models


@pytest.mark.asyncio
async def test_hash():
    password = 'password'
    hashed = auth.str_to_hash(password)
    assert auth.verify(password, hashed)


@pytest.mark.asyncio
async def test_user_is_active(create_user: models.User):
    user = await auth.get_current_active_user(create_user)
    assert user.is_active is True
    user.is_active = False
    with pytest.raises(HTTPException) as err:
        await auth.get_current_active_user(user)
    assert err.value.status_code == 400
    assert err.value.detail == 'Inactive user'


@pytest.mark.asyncio
async def test_authenticate(
    create_user: models.User, async_session: AsyncSession
):
    user = await auth.authenticate_user(
        'test@example.com', 'string', async_session
    )
    assert user

    user = await auth.authenticate_user('', 'string', async_session)
    assert user is False

    user = await auth.authenticate_user('test@example.com', '', async_session)
    assert user is False


@pytest.mark.asyncio
async def test_generate_token():
    access_token_expires = timedelta(
        minutes=auth.Settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    times = (None, access_token_expires)
    for t in times:
        token = auth.create_access_token({}, expires_delta=t)
        decode = jwt.decode(
            token,
            auth.Settings.SECRET_KEY,
            algorithms=[auth.Settings.ALGORITHM],
        )
        time = decode['exp']
        assert time


@pytest.mark.asyncio
async def test_get_current_user(
    create_user: models.User, async_session: AsyncSession
):
    access_token = auth.create_access_token(data={'sub': create_user.email})
    user = await auth.get_current_user(access_token, async_session)
    assert user


@pytest.mark.asyncio
async def test_get_current_user_none(async_session: AsyncSession):
    data = ({}, {'sub': ''})
    for d in data:
        with pytest.raises(HTTPException) as err:
            access_token = auth.create_access_token(data=d)
            await auth.get_current_user(access_token, async_session)
        assert err.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_expired_key(
    create_user: models.User, async_session: AsyncSession
):
    with pytest.raises(HTTPException) as err:
        access_token = auth.create_access_token(
            data={'sub': create_user.email}, expires_delta=timedelta(hours=-2)
        )
        await auth.get_current_user(access_token, async_session)
    assert err.value.status_code == 401
