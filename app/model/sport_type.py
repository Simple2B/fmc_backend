from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base
from app.utils import generate_uuid


class SportType(Base):
    __tablename__ = "sport_types"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)

    name = Column(String(64), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}:{self.name}"


class SportSkill(Base):
    __tablename__ = "sport_skills"
    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)

    sport_id = Column(Integer, ForeignKey("sport_types.id"), nullable=False)
    name = Column(String(32), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}:{self.name}"
