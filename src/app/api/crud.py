from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + 'notreallyhashed'
    db_user = models.User(email=user.email,
                          first_name=user.first_name,
                          last_name=user.last_name,
                          middle_name=user.middle_name,
                          phone=user.phone,
                          hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_passages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Passage).offset(skip).limit(limit).all()


def create_passage(db: Session, passage: schemas.PassageCreate, coords):
    db_passage = models.Passage(**passage.dict(), add_time=datetime.utcnow(),
                                status='new', coords_id=coords.id)
    db.add(db_passage)
    db.commit()
    db.refresh(db_passage)
    return db_passage


def create_coords(db: Session, coords: schemas.Coords):
    db_coords = models.Coords(**coords.dict())
    db.add(db_coords)
    db.commit()
    db.refresh(db_coords)
    return db_coords


def create_image(db: Session, objects: list):
    db.bulk_save_objects(objects)
    db.commit()
