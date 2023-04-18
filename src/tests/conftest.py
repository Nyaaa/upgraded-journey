import asyncio
import os
from typing import Generator, AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from app.api.models import User, Image
from app.api.v1.routes import v1_app
from app.api.v2.routes import v2_app
from app.db import Base, get_db
from app.main import app
from tests.sample_data import USER

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionTesting = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def create_user(async_session):
    user = User(**USER)
    async_session.add(user)
    await async_session.commit()


@pytest.fixture
async def cleanup(async_session):
    yield None
    result = await async_session.execute(select(Image))
    img = result.scalars().all()
    for i in img:
        os.remove(i.filepath)


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client(async_session):
    def _get_test_db():
        yield async_session

    app.dependency_overrides[get_db] = _get_test_db
    # Main app dependency does not propagate to sub apps.
    # Without supplying dependency sub apps write to main DB.
    v1_app.dependency_overrides[get_db] = _get_test_db
    v2_app.dependency_overrides[get_db] = _get_test_db

    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionTesting() as s:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            yield s
            await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
