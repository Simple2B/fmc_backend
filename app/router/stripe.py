from fastapi import APIRouter, Depends, Request, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.logger import log
from app.dependency.controller import get_stripe
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


@stripe_router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db),
    stripe_signature: str = Header(None),
    settings: Settings = Depends(get_settings),
    stripe=Depends(get_stripe),
):
    data = await request.body()

    request_data = await request.json()
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(
            payload=data, sig_header=stripe_signature, secret=webhook_secret
        )
        log(log.INFO, "Event:[%s]", event["type"])
    except Exception as e:
        log(log.ERROR, "Error - [%s]", e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{e}")
    if event["type"] == "customer.subscription.created":
        subscription = event["data"]["object"]
        coach: m.Coach = (
            db.query(m.Coach)
            .filter_by(stripe_customer_id=subscription.customer)
            .first()
        )
        product_id = subscription["items"]["data"][0].plan.product
        product: m.StripeProduct = (
            db.query(m.StripeProduct).filter_by(stripe_product_id=product_id).first()
        )
        coach_subscription = m.CoachSubscription(
            coach_id=coach.id,
            stripe_subscription_id=subscription.id,
            product_id=product.id,
            current_period_end=subscription.current_period_end,
            current_period_start=subscription.current_period_start,
            created=subscription.created,
            status=subscription.status,
        )
        db.add(coach_subscription)
        db.commit()
        log(log.INFO, "Coach subscription created")
        return status.HTTP_200_OK
