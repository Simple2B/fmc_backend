from datetime import datetime

from pydantic import BaseModel

# from .user import Coach
from .location import Location
import app.model as m


class BaseSchedule(BaseModel):
    location_id: int
    notes: str
    week_day: str | m.CoachSchedule.WeekDay
    begin: str
    end: str


class Schedule(BaseSchedule):
    uuid: str
    location: Location
    created_at: datetime

    class Config:
        orm_mode = True


class ScheduleList(BaseModel):
    schedules: list[Schedule]
