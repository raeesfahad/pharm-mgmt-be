from sqlmodel import SQLModel
from typing import Optional
from sqlmodel import Field


class UserBase(SQLModel):
    username: str
    password: str

class UserCreate(UserBase):
    pass


class UserUpdate(SQLModel):
    username: Optional[str] = None
    password: Optional[str] = None


class UserPublic(UserBase):
    id: int