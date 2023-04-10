from pydantic import BaseModel


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str
    email: str
    phone: int

    class Config:
        orm_mode = True
