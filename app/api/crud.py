import pathlib
import tempfile
from datetime import datetime, date
from typing import Sequence
from uuid import uuid4

import aiofiles
from fastapi import UploadFile
from pydantic import BaseModel
from sqlalchemy import Row
from sqlalchemy.future import select
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from . import models, schemas
from app.settings import settings

engine = create_async_engine(settings.DATABASE_URL)
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


# Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_object_by_id(db: AsyncSession, model, obj_id: int):
    q = select(model).where(model.id == obj_id)
    result = await db.execute(q)
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> models.User:
    q = select(models.User).where(models.User.email == email)
    result = await db.execute(q)
    return result.scalars().first()


async def commit(db: AsyncSession, instance):
    db.add(instance)
    await db.commit()
    await db.refresh(instance)
    return instance


async def get_all_objects(
    db: AsyncSession, model, skip: int = 0, limit: int = 100
):
    q = select(model).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().unique().all()


async def create_passage(
    db: AsyncSession,
    passage: schemas.PassageBase,
    coords: models.Coords,
    user: models.User,
) -> models.Passage:
    db_passage = models.Passage(
        **passage.model_dump(),
        add_time=datetime.utcnow(),
        status='new',
        coords_id=coords.id,
        user_id=user.id,
    )
    return await commit(db, db_passage)


async def create_coords(
    db: AsyncSession, coords: schemas.Coords
) -> models.Coords:
    db_coords = models.Coords(**coords.model_dump())
    return await commit(db, db_coords)


async def create_image(
    db: AsyncSession, files: list[tuple[str, UploadFile]], passage_id: int
) -> list[models.Image]:
    to_save = []

    for image_title, image_file in files:
        if str(db.bind.url) == 'sqlite+aiosqlite://':
            file_path = tempfile.NamedTemporaryFile().name
        else:
            path = pathlib.Path('./media') / str(date.today())
            path.mkdir(parents=True, exist_ok=True)
            ext = pathlib.Path(image_file.filename).suffix
            filename = pathlib.Path(str(uuid4())).with_suffix(ext)
            file_path = path.joinpath(filename).as_posix()

        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await image_file.read(1024):
                await out_file.write(content)

        to_save.append(
            models.Image(
                title=image_title, passage_id=passage_id, filepath=file_path
            )
        )
    db.add_all(to_save)
    await db.commit()
    return to_save


async def get_passage_by_email(
    db: AsyncSession, email: str
) -> Sequence[models.Passage]:
    q = (
        select(models.Passage)
        .join(models.User)
        .where(models.User.email == email)
    )
    result = await db.execute(q)
    return result.scalars().unique().all()


async def update_instance(db: AsyncSession, instance: Row, data: BaseModel):
    """Probably not a good way to update. Cannot use query due to async session."""
    passage = dict(data).items()
    for key, value in passage:
        setattr(instance, key, value) if value else None
    return await commit(db, instance)
