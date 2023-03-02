from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.database import Base
from app.utils import generate_uuid


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False, default=generate_uuid)

    coach_id = Column(Integer, ForeignKey("coaches.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    sport_type_id = Column(Integer, ForeignKey("sport_types.id"))

    date = Column(DateTime, nullable=False, default=datetime.now)

    created_at = Column(DateTime(), default=datetime.now)

    def __repr__(self):
        return f"<{self.id}:{self.date}>"
