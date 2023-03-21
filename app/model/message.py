import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum

from app.database import Base, get_db
from app.utils import generate_uuid
from .coach import Coach
from .student import Student

db = get_db().__next__()


class MessageTypes(enum.Enum):
    MESSAGE = "message"
    NOTIFICATION = "notification"


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False, default=generate_uuid)

    text = Column(String(1024), nullable=False)

    author_id = Column(String(36), nullable=False)  # uuid of owner
    receiver_id = Column(String(36), nullable=False)  # uuid of recepient

    message_type = Column(Enum(MessageTypes), default=MessageTypes.MESSAGE)

    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime(timezone=True), default=datetime.max)

    created_at = Column(DateTime(timezone=True), default=datetime.now)
    is_deleted = Column(Boolean, nullable=False, default=False)

    @property
    def author(self) -> Coach | Student | None:
        student: Student | None = (
            db.query(Student).filter_by(uuid=self.author_id).first()
        )
        if student:
            return student
        coach: Coach | None = db.query(Coach).filter_by(uuid=self.author_id).first()
        return coach

    @property
    def receiver(self) -> Coach | Student | None:
        student: Student | None = (
            db.query(Student).filter_by(uuid=self.receiver_id).first()
        )
        return (
            student
            if student
            else db.query(Coach).filter_by(uuid=self.receiver_id).first()
        )

    def __repr__(self):
        return f"<{self.id}:{self.created_at} - {self.message_text[:12]}...>"
