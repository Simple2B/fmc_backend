import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils import generate_uuid


class WeekDay(enum.IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WENDESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class CoachSchedule(Base):
    __tablename__ = "coach_schedules"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)

    coach_id = Column(Integer, ForeignKey("coaches.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))

    week_day = Column(Integer, default=WeekDay.FRIDAY.value)
    begin_hours = Column(Integer, nullable=False)
    begin_minutes = Column(Integer, nullable=False)
    duration = Column(Integer, default=60)

    created_at = Column(DateTime(), default=datetime.now)

    coach = relationship(
        "Coach",
        viewonly=True,
    )
    location = relationship(
        "Location",
        viewonly=True,
    )

    def __repr__(self):
        return f"<CoachSchedule {self.id}>"
