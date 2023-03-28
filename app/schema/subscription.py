from pydantic import BaseModel

from .user.profile import Coach
from .stripe import Product


class Subscription(BaseModel):
    product: Product
    stripe_subscription_id: str
    current_period_end: int
    current_period_start: int
    created: int
    status: str
    is_active: bool

    class Config:
        orm_mode = True


class CoachSubscription(Subscription):
    coach: Coach

    class Config:
        orm_mode = True
