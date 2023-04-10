from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database import Base, get_db
from app.utils import generate_uuid

db = get_db().__next__()


class StudentLesson(Base):  # booking
    __tablename__ = "students_lessons"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("coach_schedules.id"), nullable=False)
    coach_id = Column(Integer, ForeignKey("coaches.id"), nullable=False)

    appointment_time = Column(
        DateTime(timezone=True), nullable=False
    )  # This field shouldnt be nullable , since we get it from the frontend

    created_at = Column(DateTime, nullable=False, default=datetime.now)

    # relationships
    student = relationship(
        "Student", foreign_keys="StudentLesson.student_id", viewonly=True
    )
    schedule = relationship(
        "CoachSchedule", foreign_keys="StudentLesson.schedule_id", viewonly=True
    )
    coach = relationship("Coach", foreign_keys="StudentLesson.coach_id", viewonly=True)

    def __repr__(self):
        return f"<StudentLesson {self.id}>"
