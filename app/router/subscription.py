from fastapi import APIRouter, Depends, status

from app.dependency import get_current_coach
from app.config import get_settings, Settings
import app.model as m
import app.schema as s


from app.database import get_db


subscription_router = APIRouter(prefix="/subscription", tags=["Subscription"])


@subscription_router.post("/create", status_code=status.HTTP_200_OK)
def create_coach_subscription(
    coach: m.Coach = Depends(get_current_coach),
    db=Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    if not coach.stripe_customer_id:
        ...
        # TODO
