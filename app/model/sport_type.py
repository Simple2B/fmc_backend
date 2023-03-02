import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum

from app.database import Base
from app.utils import generate_uuid


class SportTypes(enum.Enum):
    volleyball = "Volleyball"
    box = "Box"
    tennis = "Tennis"
    swimming = "Swimming"


class SportType(Base):
    __tablename__ = "sport_types"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)

    name = Column(Enum(SportTypes), name="sport_types_enum", default=SportTypes.box)
    created_at = Column(DateTime(), default=datetime.now)

    def __repr__(self) -> str:
        return f"{self.name.value}"
