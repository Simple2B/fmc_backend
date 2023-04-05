import enum
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils import generate_uuid


def get_default_end_dateime():
    return datetime.now() + timedelta(minutes=60)


class ReccurencyType(enum.Enum):
    NO_REPEAT = 0
    WEEKLY = 1
    MONTHLY = 2


class CoachSchedule(Base):
    __tablename__ = "coach_schedules"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)

    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    coach_id = Column(Integer, ForeignKey("coaches.id"), nullable=False)

    reccurence = Column(Integer, nullable=False, default=ReccurencyType.NO_REPEAT.value)
    start_datetime = Column(DateTime, nullable=False, default=datetime.now)
    end_datetime = Column(Integer, nullable=False, default=get_default_end_dateime)

    created_at = Column(DateTime(), default=datetime.now)

    lesson = relationship(
        "Lesson", foreign_keys="CoachSchedule.lesson_id", viewonly=True
    )
    coach = relationship("Coach", foreign_keys="CoachSchedule.coach_id", viewonly=True)

    def __repr__(self):
        return f"<CoachSchedule {self.id}>"
