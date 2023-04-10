from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils import generate_uuid


class CoachSchedule(Base):
    __tablename__ = "coach_schedules"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)

    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    coach_id = Column(Integer, ForeignKey("coaches.id"), nullable=False)

    is_booked = Column(Boolean, default=False)

    start_datetime = Column(DateTime(timezone=True), nullable=False)
    end_datetime = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(), default=datetime.now)

    lesson = relationship("Lesson", viewonly=True)
    coach = relationship("Coach", viewonly=True)

    def __repr__(self):
        return f"<CoachSchedule {self.id}:{self.start_datetime}:{self.lesson}>"

    @property
    def duration(self):
        return self.end_datetime - self.start_datetime
