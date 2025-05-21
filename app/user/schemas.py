from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TimeData(BaseModel):
    session_start: datetime
    session_end: datetime
    delta: int


class HeatmapField(BaseModel):
    date: datetime
    count: int


class UserCreate(BaseModel):
    username: str
    password_hash: str


class UserCreated(BaseModel):
    id: int


class UserShow(BaseModel):
    id: int
    username: str
    time: int
    time_data: Optional[list[TimeData]]


class AllUsersShow(BaseModel):
    data: list[UserShow]


class ParsedTimeData(BaseModel):
    total_spent_time: int

    average_time_per_day: int
    average_time_per_week: int
    average_time_per_month: int

    most_visited_day_of_month: str
    most_visited_time_of_month: str

    heatmap: list[HeatmapField]
