from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.database import Base, get_db
from app.utils import generate_uuid

from .location import Location
from .coach import Coach
from .sport_type import SportType

db = get_db().__next__()


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False, default=generate_uuid)

    coach_id = Column(Integer, ForeignKey("coaches.id"))

    location_id = Column(Integer, ForeignKey("locations.id"))
    sport_type_id = Column(Integer, ForeignKey("sport_types.id"))

    created_at = Column(DateTime, default=datetime.now)

    @property
    def coach(self) -> Coach:
        return db.query(Coach).filter_by(id=self.coach_id).first()

    @property
    def location(self) -> Location:
        return db.query(Location).filter_by(id=self.location_id).first()

    @property
    def sport(self) -> SportType:
        return db.query(SportType).filter_by(id=self.sport_type_id).first()

    def __repr__(self):
        return f"<{self.id}:{self.date}>"
