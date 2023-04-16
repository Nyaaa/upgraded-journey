from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field

from .validators import PhoneNumber, JSONValidator


class Image(BaseModel):
    title: str
    filepath: str

    class Config:
        orm_mode = True


class Coords(JSONValidator):
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


class PassageCreate(PassageBase, JSONValidator):
    user_id: int


class Passage(PassageBase):
    id: int
    user_id: int
    add_time: datetime
    status: Literal['new', 'pending', 'accepted', 'rejected']
    coords: Coords
    images: list[Image]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str | None = None
    phone: PhoneNumber = Field(None, example='+711111111')


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    passages: list[Passage] = []

    class Config:
        orm_mode = True
