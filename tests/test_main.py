import pytest
from httpx import AsyncClient

from app.settings import settings
from app.api.crud import get_db


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    for index in '/', '/v1/', '/v2/':
        response = await client.get(index, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_db():
    db = anext(get_db())  # NOSONAR
    db = await db
    assert db.bind.url.database == settings.DB_NAME
