from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base, get_db
from app.utils import generate_uuid

from .location import Location
from .sport_type import SportType
from .coach_sport import CoachSport

db = get_db().__next__()


class Lesson(Base):  # Package
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False, default=generate_uuid)

    name = Column(String(64), nullable=False, default="")

    coach_id = Column(Integer, ForeignKey("coaches.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    sport_type_id = Column(Integer, ForeignKey("sport_types.id"))

    about = Column(String(512), default="")
    max_people = Column(Integer, default=1)
    price = Column(Integer, default=999)

    created_at = Column(DateTime, default=datetime.now)

    # relationships
    coach = relationship("Coach", foreign_keys="Lesson.coach_id", viewonly=True)
    location = relationship(
        "Location", foreign_keys="Lesson.location_id", viewonly=True
    )

    @property
    def is_personal(self):
        return self.max_people and self.max_people == 1

    @property
    def name(self) -> str:
        return f"1-on-1 {self.sport.name} Lesson with {self.coach.first_name}"

    @property
    def location(self) -> Location:
        return db.query(Location).filter_by(id=self.location_id).first()

    @property
    def sport(self) -> SportType:
        return db.query(SportType).filter_by(id=self.sport_type_id).first()

    @property
    def price(self) -> float:
        coach_sport: CoachSport = (
            db.query(CoachSport)
            .filter_by(coach_id=self.coach_id, sport_id=self.sport_type_id)
            .first()
        )
        return coach_sport.price

    def __repr__(self):
        return f"<{self.id}:{self.date}>"
