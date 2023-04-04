from pydantic import BaseModel

# from .user import Coach
from .location import Location
import app.model as m


class BaseSchedule(BaseModel):
    location_id: int
    week_day: int | m.CoachSchedule.WeekDay
    begin_hours: int
    begin_minutes: int
    duration: int | None

    class Config:
        orm_mode = True


class Schedule(BaseSchedule):
    uuid: str
    location: Location

    class Config:
        orm_mode = True


class ScheduleList(BaseModel):
    schedules: list[Schedule]
