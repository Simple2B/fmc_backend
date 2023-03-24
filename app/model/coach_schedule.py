import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum

from app.database import Base
from app.utils import generate_uuid


class WeekDay(enum.Enum):
    monday = "Monday"
    tuesday = "Tuesday"
    wednesday = "Wednesday"
    thursday = "Thursday"
    friday = "Friday"
    saturday = "Saturday"
    sunday = "Sunday"


class CoachSchedule(Base):
    __tablename__ = "coach_schedules"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)

    coach_id = Column(Integer, ForeignKey("coaches.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    notes = Column(String(256), nullable=True)

    week_day = Column(Enum(WeekDay), default=WeekDay.monday)
    begin = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    created_at = Column(DateTime(), default=datetime.now)

    def __repr__(self):
        return f"<CoachSchedule {self.id}>"
