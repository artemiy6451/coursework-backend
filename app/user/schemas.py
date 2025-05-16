from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password_hash: str


class UserCreated(BaseModel):
    id: int


class UserShow(BaseModel):
    username: str
    time: int
    time_data: Optional[list[tuple[datetime, datetime]]]


class AllUsersShow(BaseModel):
    data: list[UserShow]
