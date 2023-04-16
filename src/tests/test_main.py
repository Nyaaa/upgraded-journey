import pytest
from httpx import AsyncClient

from app.db import get_db


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    for index in "/", "/v1/", "/v2/":
        response = await client.get(index, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_db(client: AsyncClient):
    async for db in get_db():
        assert db.bind.url.database == 'FSTR'
