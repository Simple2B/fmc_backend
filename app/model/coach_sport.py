from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float

from app.database import Base
from app.utils import generate_uuid


class CoachSport(Base):
    __tablename__ = "coaches_sports"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)

    coach_id = Column(Integer, ForeignKey("coaches.id"))
    sport_id = Column(Integer, ForeignKey("sport_types.id"))

    amount = Column(
        Float, default=9.99
    )  # hypotheticall the price of a coach lesson for the sport he teaches may differ
    created_at = Column(DateTime(), default=datetime.now)

    def __repr__(self):
        return f"<CoachSport {self.id}>"
