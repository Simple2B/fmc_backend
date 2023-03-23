from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from app.database import Base
from app.utils import generate_uuid


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False, index=True, default=generate_uuid)
    coach_id = Column(Integer, ForeignKey("coaches.id"))

    certificate_url = Column(String(256), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f" certificate <{self.id}>"
