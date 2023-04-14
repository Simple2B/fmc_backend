from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.orm import relationship

from app.hash_utils import make_hash, hash_verify
from app.database import Base, Session
from app.utils import generate_uuid


class Coach(Base):
    __tablename__ = "coaches"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False, index=True, default=generate_uuid)

    first_name = Column(String(64), nullable=False, default="")
    last_name = Column(String(64), nullable=False, default="")
    email = Column(String(128), nullable=False, unique=True)
    username = Column(String(64), nullable=False, unique=False)
    profile_picture = Column(String(256), nullable=True)
    google_open_id = Column(String(128), nullable=True)

    about = Column(String(1024), nullable=False, default="")

    experience = Column(String(1024), nullable=True, default="")
    credentials = Column(String(1024), nullable=True, default="")

    certificate_url = Column(String(256), nullable=True)

    verification_token = Column(
        String(36), nullable=True, default=generate_uuid
    )  # for email confirmation and forgot password

    password_hash = Column(String(128), nullable=False)
    is_verified = Column(Boolean, default=True)
    is_for_adults = Column(Boolean, default=True)
    is_for_children = Column(Boolean, default=False)
    stripe_customer_id = Column(
        String(32), nullable=True
    )  # customer identifier in stripe system
    stripe_account_id = Column(String(32), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    # relationship
    sports = relationship("SportType", secondary="coaches_sports", viewonly=True)
    subscription = relationship("CoachSubscription", viewonly=True)
    certificates = relationship("Certificate", viewonly=True)
    locations = relationship("Location", secondary="coaches_locations", viewonly=True)
    reviews = relationship("LessonReview", viewonly=True)
    lessons = relationship("Lesson", viewonly=True)
    schedules = relationship("CoachSchedule", viewonly=True)

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

    @property
    def total_rate(self) -> float:
        review_count = len(self.reviews)
        if not review_count:
            return 0
        rate = sum([review.rate for review in self.reviews]) / review_count
        return round(rate, 2)

    def __repr__(self):
        return f"<{self.id}: {self.email}>"
