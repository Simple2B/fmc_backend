import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils import generate_uuid


class CoachSchedule(Base):
    class WeekDay(enum.Enum):
        monday = "Monday"
        tuesday = "Tuesday"
        wednesday = "Wednesday"
        thursday = "Thursday"
        friday = "Friday"
        saturday = "Saturday"
        sunday = "Sunday"

    __tablename__ = "coach_schedules"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)

    coach_id = Column(Integer, ForeignKey("coaches.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    notes = Column(String(256), nullable=True)

    week_day = Column(Enum(WeekDay), default=WeekDay.monday)
    begin = Column(String(32), nullable=False)  # e.g. 17:32
    end = Column(String(32), nullable=False)  # e.g. 18:32
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
