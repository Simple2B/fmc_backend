from datetime import datetime

from pydantic import BaseModel, validator

# from .user import Coach
from .location import Location
import app.model as m


class BaseSchedule(BaseModel):
    location_id: int
    notes: str
    week_day: str | m.CoachSchedule.WeekDay
    begin: str
    end: str

    @validator("begin", "end")
    def check_time(cls, v):
        # check if its valid format
        if not datetime.strptime(v, "%H:%M").time():
            raise ValueError("Bad time format")
        return v


class Schedule(BaseSchedule):
    uuid: str
    location: Location
    created_at: datetime

    class Config:
        orm_mode = True


class ScheduleList(BaseModel):
    schedules: list[Schedule]
