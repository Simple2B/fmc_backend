from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.database import Base
from app.utils import generate_uuid


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False, default=generate_uuid)

    email_from = Column(String(64), nullable=False)
    message = Column(String(1024), nullable=False)

    have_replied = Column(Boolean, default=False)
    in_review = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<{self.id}:{self.email_from}>"
