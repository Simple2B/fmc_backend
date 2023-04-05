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

    student_id = Column(Integer, ForeignKey("students.id"))
    schedule_id = Column(Integer, ForeignKey("coach_schedules.id"))

    student_lesson_payment_id = Column(
        Integer,
        ForeignKey("student_lesson_payments.id"),
        nullable=True,
    )

    appointment_time = Column(
        DateTime(timezone=True), nullable=False
    )  # This field shouldnt be nullable , since we get it from the frontend

    created_at = Column(
        DateTime, nullable=False, default=datetime.now
    )  # to do rename as created_at
    review_id = Column(Integer, nullable=True)  # fake FK on review

    # relationships
    student = relationship(
        "Student", foreign_keys="StudentLesson.student_id", viewonly=True
    )
    schedule = relationship(
        "CoachSchedule", foreign_keys="StudentLesson.schedule_id", viewonly=True
    )

    # @property
    # def schedule(self) -> Lesson:
    #     return db.query(Lesson).filter_by(id=self.lesson_id).first()

    def __repr__(self):
        return f"<StudentLesson {self.id}>"
