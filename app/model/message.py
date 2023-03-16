import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.database import Base
from app.utils import generate_uuid, get_datetime


class MessageTypes(enum.Enum):
    MESSAGE = "message"
    NOTIFICATION = "notification"


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False, default=generate_uuid)
    message_text = Column(String(1024), nullable=False)
    message_from = Column(String(36), nullable=False)  # uuid of owner
    message_to = Column(String(36), nullable=False)  # uuid of recepient
    message_type = Column(String(36), default=MessageTypes.MESSAGE.value)
    is_read = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now)
    created_at_timestamp = Column(Integer, default=get_datetime)

    def __repr__(self):
        return f"<{self.id}:{self.created_at}>"
