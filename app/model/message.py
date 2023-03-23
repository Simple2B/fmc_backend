import enum
from typing import Self
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, and_, or_

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

    @classmethod
    def get_contact_latest_message(
        cls,
        coach_id: str,
        student_id: str,
    ) -> Self:
        return (
            db.query(cls)
            .filter(
                or_(
                    and_(
                        cls.author_id == student_id,
                        cls.receiver_id == coach_id,
                        cls.is_deleted == False,  # noqa:flake8 E712
                    ),
                    and_(
                        cls.author_id == coach_id,
                        cls.receiver_id == student_id,
                        cls.is_deleted == False,  # noqa:flake8 E712
                    ),
                ),
            )
            .order_by(cls.created_at.desc())
            .first()
        )

    @classmethod
    def get_diaogue_messages(
        cls,
        coach_id: str,
        student_id: str,
    ) -> list[Self]:
        return (
            db.query(cls)
            .filter(
                or_(
                    and_(
                        cls.author_id == student_id,
                        cls.receiver_id == coach_id,
                        cls.is_deleted == False,  # noqa:flake8 E712
                    ),
                    and_(
                        cls.author_id == coach_id,
                        cls.receiver_id == student_id,
                        cls.is_deleted == False,  # noqa:flake8 E712
                    ),
                ),
            )
            .order_by(cls.created_at.desc())
            .all()
        )

    def __repr__(self):
        return f"<{self.id}:{self.created_at} - {self.message_text[:12]}...>"
