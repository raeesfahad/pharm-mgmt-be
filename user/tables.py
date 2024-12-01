from .models import UserBase
from typing import Optional
from sqlmodel import Field


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)