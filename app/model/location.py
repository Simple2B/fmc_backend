from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base
from app.utils import generate_uuid


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)

    name = Column(String(64), default="")
    city = Column(String(64), default="")
    address_line_1 = Column(String(64), default="")
    address_line_2 = Column(String(64), default="")

    created_at = Column(DateTime(), default=datetime.now)

    def __repr__(self):
        return f"<Location {self.name} - {self.city}>"
