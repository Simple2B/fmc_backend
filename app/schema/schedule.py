from datetime import datetime

from pydantic import BaseModel

from .user import Coach
from .lesson import Lesson


class BaseSchedule(BaseModel):
    lesson_id: int
    start_datetime: datetime | str
    end_datetime: datetime | str


class Schedule(BaseSchedule):
    id: int
    uuid: str
    lesson: Lesson
    coach_id: int
    coach: Coach
    reccurence: int | None

    class Config:
        orm_mode = True


class ScheduleList(BaseModel):
    schedules: list[Schedule]


# TODO rename
class CoachSchedule(BaseModel):
    date: str
    schedules: list[Schedule]


class CoachScheduleList(BaseModel):
    data: list[CoachSchedule]
