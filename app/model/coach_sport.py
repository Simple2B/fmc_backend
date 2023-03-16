from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base
from app.utils import generate_uuid
from app.config import get_settings

settings = get_settings()


class CoachSport(Base):
    __tablename__ = "coaches_sports"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False, default=generate_uuid)

    coach_id = Column(Integer, ForeignKey("coaches.id"))
    sport_id = Column(Integer, ForeignKey("sport_types.id"))

    price = Column(
        Integer, nullable=False, default=settings.COACH_DEFAULT_LESSON_PRICE
    )  # cents

    def __repr__(self):
        return f"<CoachSport {self.id}>"
