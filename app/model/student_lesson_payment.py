from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base
from app.utils import generate_uuid


class StudentLessonPayment(Base):
    __tablename__ = "student_lesson_payments"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)
    # stripe_checkout_id - implemented later
    status = Column(String(32))

    created_at = Column(DateTime(), default=datetime.now)

    def __repr__(self):
        return f"<Payment {self.id}>"
