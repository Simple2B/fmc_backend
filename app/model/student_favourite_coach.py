from sqlalchemy import Column, Integer, ForeignKey

from app.database import Base


class StudentFavouriteCoach(Base):
    __tablename__ = "student_favourite_coaches"

    id = Column(Integer, primary_key=True)

    coach_id = Column(Integer, ForeignKey("coaches.id"))
    student_id = Column(Integer, ForeignKey("students.id"))

    def __repr__(self):
        return f"<Coach {self.coach_id} - Student {self.student_id}>"
