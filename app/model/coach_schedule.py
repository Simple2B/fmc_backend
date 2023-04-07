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

    reccurence = Column(
        Integer, nullable=False, default=ReccurencyType.NO_REPEAT.value
    )  # TODO switch to enum
    start_datetime = Column(
        DateTime(timezone=True), nullable=False, default=datetime.now
    )  # maybe we should make it unique ????
    end_datetime = Column(DateTime(timezone=True), nullable=False, default=get_default_end_dateime)

    created_at = Column(DateTime(), default=datetime.now)

    lesson = relationship("Lesson", viewonly=True)
    coach = relationship("Coach", viewonly=True)

    def __repr__(self):
        return f"<CoachSchedule {self.id}:{self.start_datetime}:{self.lesson}>"

    @property
    def duration(self):
        return self.end_datetime - self.start_datetime
