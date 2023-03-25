from fastapi import APIRouter, Depends
from app.config import get_settings, Settings
import app.model as m
import app.schema as s


from app.database import get_db


stripe_router = APIRouter(prefix="/stripe", tags=["Stripe"])


@stripe_router.get("/products", response_model=s.Product)
def get_coach_stripe_product(
    db=Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    return (
        db.query(m.StripeProduct)
        .filter_by(stripe_product_id=settings.COACH_SUBSCRIPTION_PRODUCT_ID)
        .first()
    )
