import enum

from sqlalchemy import Column, Integer, String

from app.database import Base
from app.utils import generate_uuid


class SportTypes(enum.Enum):
    Volleyball = "Volleyball"
    Boxing = "Boxing"
    Tennis = "Tennis"
    Swimming = "Swimming"


class SportType(Base):
    __tablename__ = "sport_types"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)

    name = Column(String(64), default=SportTypes.Boxing.value)

    def __repr__(self) -> str:
        return f"{self.id}:{self.name}"
