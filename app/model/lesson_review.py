from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils import generate_uuid


class LessonReview(Base):
    __tablename__ = "lesson_reviews"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False, default=generate_uuid)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))  # todo lesson_id
    coach_id = Column(Integer, ForeignKey("coaches.id"))

    text = Column(String(36), nullable=True)
    rate = Column(Integer, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    lesson = relationship("Lesson", viewonly=True)

    def __repr__(self) -> str:
        return f"{self.id}"
