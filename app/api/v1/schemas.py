from datetime import datetime
from typing import Literal, Optional

from pydantic import EmailStr, Field, BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.api.validators import JSONValidatorMixin

OPTIONS = Literal["new", "pending", "accepted", "rejected"]


class Coords(BaseModel, JSONValidatorMixin):
    latitude: float
    longitude: float
    height: int


class Image(BaseModel):
    title: str
    filepath: str


class PassageBase(BaseModel, JSONValidatorMixin):
    beauty_title: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    level_winter: Optional[str] = None
    level_summer: Optional[str] = None
    level_autumn: Optional[str] = None
    level_spring: Optional[str] = None


class CoordsUpdate(BaseModel, JSONValidatorMixin):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    height: Optional[int] = None


class PassageUpdate(BaseModel, JSONValidatorMixin):
    beauty_title: Optional[str] = None
    title: Optional[str] = None
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    level_winter: Optional[str] = None
    level_summer: Optional[str] = None
    level_autumn: Optional[str] = None
    level_spring: Optional[str] = None
    status: Optional[OPTIONS] = None


class Passage(PassageBase):
    id: int
    user_id: int
    add_time: datetime
    status: OPTIONS
    coords: Coords
    images: list[Image]


class UserBase(BaseModel, JSONValidatorMixin):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    phone: Optional[PhoneNumber] = Field(None, json_schema_extra={"example": "+1-206-555-01-00"})
