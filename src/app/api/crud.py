import pathlib
from datetime import date
from datetime import datetime
from uuid import uuid4

import aiofiles
from sqlalchemy.orm import Session

from app import hasher
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def commit(db: Session, instance):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hasher.str_to_hash(user.password)
    db_user = models.User(email=user.email,
                          first_name=user.first_name,
                          last_name=user.last_name,
                          middle_name=user.middle_name,
                          phone=user.phone,
                          hashed_password=hashed_password)
    return commit(db, db_user)


def get_passages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Passage).offset(skip).limit(limit).all()


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

        await write_file(file_path, image_file)

        to_save.append(models.Image(title=image_title, passage_id=passage_id, filepath=file_path))
    db.bulk_save_objects(to_save)
    db.commit()


async def write_file(file_path, image_file):
    async with aiofiles.open(file_path, 'wb') as out_file:
        while content := await image_file.read(1024):
            await out_file.write(content)
