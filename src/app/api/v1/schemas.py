from datetime import datetime
from typing import Literal

from pydantic import EmailStr, Field, BaseModel

from app.api.validators import PhoneNumber, JSONValidator


class Coords(JSONValidator):
    latitude: float
    longitude: float
    height: int

    class Config:
        orm_mode = True


class Image(BaseModel):
    title: str
    filepath: str


class PassageBase(JSONValidator):
    beauty_title: str
    title: str
    other_titles: str | None = None
    connect: str | None = None
    level_winter: str | None = None
    level_summer: str | None = None
    level_autumn: str | None = None
    level_spring: str | None = None


class Passage(PassageBase):
    id: int
    user_id: int
    add_time: datetime
    status: Literal['new', 'pending', 'accepted', 'rejected']
    coords: Coords
    images: list[Image]


class UserBase(JSONValidator):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str | None = None
    phone: PhoneNumber = Field(None, example='+711111111')
