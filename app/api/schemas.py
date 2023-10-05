from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from .validators import JSONValidatorMixin


class Image(BaseModel):
    title: str
    filepath: str


class Coords(BaseModel, JSONValidatorMixin):
    latitude: float
    longitude: float
    height: int


class PassageBase(BaseModel, JSONValidatorMixin):
    beauty_title: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    level_winter: Optional[str] = None
    level_summer: Optional[str] = None
    level_autumn: Optional[str] = None
    level_spring: Optional[str] = None


class Passage(PassageBase):
    id: int
    user_id: int
    add_time: datetime
    status: Literal["new", "pending", "accepted", "rejected"]
    coords: Coords
    images: list[Image]


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    phone: Optional[PhoneNumber] = Field(None, json_schema_extra={"example": "+1-206-555-01-00"})


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    passages: list[Passage] = []


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
