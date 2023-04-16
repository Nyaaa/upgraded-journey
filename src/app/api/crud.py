import pathlib
from datetime import date
from datetime import datetime
from uuid import uuid4

import aiofiles
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app import hasher
from . import models, schemas


async def get_user(db: Session, user_id: int):
    q = select(models.User).where(models.User.id == user_id)
    result = await db.execute(q)
    return result.scalars().first()


async def get_user_by_email(db: Session, email: str):
    q = select(models.User).where(models.User.email == email)
    result = await db.execute(q)
    return result.scalars().first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    q = select(models.User).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


async def commit(db: Session, instance):
    db.add(instance)
    await db.commit()
    await db.refresh(instance)
    return instance


async def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hasher.str_to_hash(user.password)
    db_user = models.User(email=user.email,
                          first_name=user.first_name,
                          last_name=user.last_name,
                          middle_name=user.middle_name,
                          phone=user.phone,
                          hashed_password=hashed_password)
    return await commit(db, db_user)


async def get_passages(db: Session, skip: int = 0, limit: int = 100):
    q = select(models.Passage).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


def create_passage(db: Session, passage: schemas.PassageCreate, coords):
    db_passage = models.Passage(**passage.dict(), add_time=datetime.utcnow(),
                                status='new', coords_id=coords.id)
    return commit(db, db_passage)


def create_coords(db: Session, coords: schemas.Coords):
    db_coords = models.Coords(**coords.dict())
    return commit(db, db_coords)


async def create_image(db: Session, files: list, passage_id: int):
    to_save = []

    for image_title, image_file in files:
        path = pathlib.Path('./media') / str(date.today())
        path.mkdir(parents=True, exist_ok=True)
        ext = pathlib.Path(image_file.filename).suffix
        filename = pathlib.Path(str(uuid4())).with_suffix(ext)
        file_path = path.joinpath(filename).as_posix()

        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await image_file.read(1024):
                await out_file.write(content)

        to_save.append(models.Image(title=image_title, passage_id=passage_id, filepath=file_path))
    db.add_all(to_save)
    await db.commit()
