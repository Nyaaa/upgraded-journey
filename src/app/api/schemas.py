from datetime import datetime
from pydantic import BaseModel
from typing import Literal
import json


class Validator(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class Image(BaseModel):
    title: str
    filepath: str

    class Config:
        orm_mode = True


class Coords(Validator):
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


class PassageCreate(PassageBase, Validator):
    user_id: int


class Passage(PassageBase):
    id: int
    add_time: datetime
    status: Literal['new', 'pending', 'accepted', 'rejected']
    coords: Coords
    images: list[Image]

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
