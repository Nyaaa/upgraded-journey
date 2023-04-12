from datetime import datetime

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


def create_image(db: Session, objects: list):
    db.bulk_save_objects(objects)
    db.commit()
