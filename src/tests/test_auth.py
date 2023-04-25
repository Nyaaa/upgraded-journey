import pytest

from app import auth


@pytest.mark.asyncio
async def test_hash():
    password = "password"
    hashed = auth.str_to_hash(password)
    assert auth.verify(password, hashed)
