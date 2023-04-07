from datetime import datetime

from pydantic import BaseModel

from .user import Coach
from .lesson import Lesson


class BaseSchedule(BaseModel):
    lesson_id: int
    start_datetime: datetime | str
    end_datetime: datetime | str


class Schedule(BaseSchedule):
    uuid: str
    lesson: Lesson
    coach_id: int
    coach: Coach
    reccurence: int | None

    class Config:
        orm_mode = True


class ScheduleList(BaseModel):
    schedules: list[Schedule]
