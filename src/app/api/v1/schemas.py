from pydantic import EmailStr, Field
from app.api.validators import PhoneNumber, JSONValidator


class Coords(JSONValidator):
    latitude: float
    longitude: float
    height: int

    class Config:
        orm_mode = True


class PassageBase(JSONValidator):
    beauty_title: str
    title: str
    other_titles: str | None = None
    connect: str | None = None
    level_winter: str | None = None
    level_summer: str | None = None
    level_autumn: str | None = None
    level_spring: str | None = None


class UserBase(JSONValidator):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str | None = None
    phone: PhoneNumber = Field(None, example='+711111111')
