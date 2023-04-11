from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, LargeBinary, Float
from sqlalchemy.orm import relationship
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    phone = Column(String)

    passages = relationship("Passage", back_populates="user")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filepath = Column(String)
    title = Column(String)
    passage_id = Column(Integer, ForeignKey("passages.id"))


class Coords(Base):
    __tablename__ = "coords"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Integer)

    passage = relationship("Passage", backref="coords")


class Passage(Base):
    __tablename__ = "passages"

    id = Column(Integer, primary_key=True, index=True)
    beauty_title = Column(String)
    title = Column(String)
    other_titles = Column(String)
    connect = Column(String)
    add_time = Column(DateTime)
    coords_id = Column(Integer, ForeignKey("coords.id"))
    level_winter = Column(String)
    level_summer = Column(String)
    level_autumn = Column(String)
    level_spring = Column(String)
    status = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    images = relationship("Image", backref="passages")
    user = relationship("User", back_populates="passages")
