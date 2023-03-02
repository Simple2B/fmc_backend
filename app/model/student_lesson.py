from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base
from app.utils import generate_uuid


class StudentLesson(Base):
    __tablename__ = "students_lessons"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)

    student_id = Column(Integer, ForeignKey("students.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    student_lesson_payment_id = Column(
        Integer, ForeignKey("student_lesson_payments.id")
    )

    def __repr__(self):
        return f"<StudentLesson {self.id}>"
