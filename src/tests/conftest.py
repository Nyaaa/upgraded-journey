from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app import db, main
from app.api import crud, models, schemas
from app.api.v1.routes import v1_app
from app.api.v2.routes import v2_app
from tests.sample_data import USER, COORDS, PASSAGE

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite://"
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionTesting = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture
async def create_user(async_session: AsyncSession) -> models.User:
    user = models.User(**USER)
    async_session.add(user)
    await async_session.commit()
    return user


@pytest_asyncio.fixture
async def create_passage(
    async_session: AsyncSession, create_user: models.User
) -> models.Passage:
    user = create_user
    crd = schemas.Coords(**COORDS)
    coords = await crud.create_coords(async_session, crd)
    pas = schemas.PassageBase(**PASSAGE)
    passage = await crud.create_passage(
        db=async_session, passage=pas, coords=coords, user=user
    )
    return passage


@pytest_asyncio.fixture
async def client(async_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    def _get_test_db():
        yield async_session

    main.app.dependency_overrides[db.get_db] = _get_test_db
    # Main app dependency does not propagate to sub apps.
    # Without supplying dependency sub apps write to main DB.
    v1_app.dependency_overrides[db.get_db] = _get_test_db
    v2_app.dependency_overrides[db.get_db] = _get_test_db

    async with AsyncClient(app=main.app, base_url="http://127.0.0.1:8000/") as _client:
        yield _client


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionTesting() as s:
        async with engine.begin() as conn:
            await conn.run_sync(db.Base.metadata.create_all)
            yield s
            await conn.run_sync(db.Base.metadata.drop_all)
    await engine.dispose()
