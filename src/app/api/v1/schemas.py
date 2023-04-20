from datetime import datetime
from typing import Literal, Optional

from pydantic import EmailStr, Field, BaseModel

from app.api.validators import PhoneNumber, JSONValidator

OPTIONS = Literal["new", "pending", "accepted", "rejected"]


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


class CoordsUpdate(JSONValidator):
    latitude: Optional[float]
    longitude: Optional[float]
    height: Optional[int]


class PassageUpdate(JSONValidator):
    beauty_title: Optional[str]
    title: Optional[str]
    other_titles: Optional[str]
    connect: Optional[str]
    level_winter: Optional[str]
    level_summer: Optional[str]
    level_autumn: Optional[str]
    level_spring: Optional[str]
    status: Optional[OPTIONS]


class Passage(PassageBase):
    id: int
    user_id: int
    add_time: datetime
    status: OPTIONS
    coords: Coords
    images: list[Image]


class UserBase(JSONValidator):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str | None = None
    phone: PhoneNumber = Field(None, example="+711111111")
