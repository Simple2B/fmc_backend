import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


from app.database import Base


class SubscriptionStatus(enum.Enum):  # stripe statuses
    ACTIVE = "active"
    INACTIVE = "inactive"


class CoachSubscription(Base):
    __tablename__ = "coach_subscriptions"

    id = Column(Integer, primary_key=True)

    coach_id = Column(Integer, ForeignKey("coaches.id"), nullable=False)
    stripe_subscription_id = Column(String(64), nullable=False)
    product_id = Column(Integer, ForeignKey("stripe_products.id"))

    current_period_end = Column(Integer, nullable=False)
    current_period_start = Column(Integer, nullable=False)
    created = Column(Integer, nullable=False)

    status = Column(String(32), default=SubscriptionStatus.ACTIVE.value)
    is_active = Column(Boolean, default=True)

    def __str__(self) -> str:
        return f"<{self.id}: {self.name}>"
