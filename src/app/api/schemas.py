from datetime import datetime
from typing import Literal, Optional

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


class PassageBase(JSONValidator):
    beauty_title: str
    title: str
    other_titles: Optional[str]
    connect: Optional[str]
    level_winter: Optional[str]
    level_summer: Optional[str]
    level_autumn: Optional[str]
    level_spring: Optional[str]


class Passage(PassageBase):
    id: int
    user_id: int
    add_time: datetime
    status: Literal["new", "pending", "accepted", "rejected"]
    coords: Coords
    images: list[Image]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: Optional[str]
    phone: PhoneNumber = Field(None, example="+711111111")


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    passages: list[Passage] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str]
