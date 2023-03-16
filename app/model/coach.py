from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.orm import relationship

from app.hash_utils import make_hash, hash_verify
from app.database import Base, Session
from app.utils import generate_uuid


class Coach(Base):
    __tablename__ = "coaches"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False, default=generate_uuid)

    first_name = Column(String(64), nullable=False, default="")
    last_name = Column(String(64), nullable=False, default="")
    email = Column(String(128), nullable=False, unique=True)
    username = Column(String(64), nullable=False, unique=False)
    profile_picture = Column(String(256), nullable=True)
    google_open_id = Column(String(128), nullable=True)

    verification_token = Column(
        String(36), nullable=True, default=generate_uuid
    )  # for email confirmation

    password_hash = Column(String(128), nullable=False)
    is_verified = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now)

    # relationship
    sports = relationship("SportType", secondary="coaches_sports", viewonly=True)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value: str):
        self.password_hash = make_hash(value)

    @classmethod
    def authenticate(cls, db: Session, user_id: str, password: str):
        user = (
            db.query(cls)
            .filter(
                func.lower(cls.email) == func.lower(user_id),
            )
            .first()
        )
        if user is not None and hash_verify(password, user.password):
            return user

    def __repr__(self):
        return f"<{self.id}: {self.email}>"
