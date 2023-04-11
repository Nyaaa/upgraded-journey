from datetime import datetime
from pydantic import BaseModel
from typing import Literal


class Image(BaseModel):
    title: str
    passage_id: int
    filepath: str

    class Config:
        orm_mode = True


class Coords(BaseModel):
    latitude: float
    longitude: float
    height: int

    class Config:
        orm_mode = True


class PassageBase(BaseModel):
    beauty_title: str
    title: str
    other_titles: str | None = None
    connect: str | None = None
    level_winter: str | None = None
    level_summer: str | None = None
    level_autumn: str | None = None
    level_spring: str | None = None
    coords: Coords


class PassageCreate(PassageBase):
    user_id: int


class Passage(PassageBase):
    id: int
    add_time: datetime
    status: Literal['new', 'pending', 'accepted', 'rejected']

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    middle_name: str
    phone: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    passages: list[Passage] = []

    class Config:
        orm_mode = True
