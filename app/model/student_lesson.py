from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from app.database import Base, get_db
from app.utils import generate_uuid

from .lesson import Lesson
from .coach import Coach

db = get_db().__next__()


class StudentLesson(Base):
    __tablename__ = "students_lessons"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)

    student_id = Column(Integer, ForeignKey("students.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    student_lesson_payment_id = Column(
        Integer,
        ForeignKey("student_lesson_payments.id"),
        nullable=True,
    )
    appointment_time = Column(DateTime(timezone=True), default=datetime.now)
    date = Column(DateTime, nullable=False, default=datetime.now)

    @property
    def coach(self) -> Coach:
        lesson = db.query(Lesson).filter_by(id=self.lesson_id).first()
        return lesson.coach

    @property
    def lesson(self) -> Lesson:
        return db.query(Lesson).filter_by(id=self.lesson_id).first()

    def __repr__(self):
        return f"<StudentLesson {self.id}>"
