import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum

from app.database import Base
from app.utils import generate_uuid


class NewsletterSubscription(Base):
    __tablename__ = "newsletter_subscriptions"

    class State(enum.Enum):
        NEW = "NEW"
        ACTIVE = "ACTIVE"
        CANCELED = "CANCELED"

    id: int = Column(Integer, primary_key=True)
    uuid: str = Column(String(36), nullable=False, default=generate_uuid)

    email: str = Column(String(64), nullable=False)

    created_at: datetime = Column(DateTime, default=datetime.now)
    state: State = Column(Enum(State), default=State.NEW)

    def __repr__(self):
        return f"<{self.id}:{self.email}:{self.state.name}>"
