from sqlalchemy import Column, Integer, ForeignKey

from app.database import Base


class CoachLocation(Base):
    __tablename__ = "coaches_locations"

    id = Column(Integer, primary_key=True)
    coach_id = Column(Integer, ForeignKey("coaches.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))

    def __repr__(self):
        return f"<CoachLocation {self.id}>"
