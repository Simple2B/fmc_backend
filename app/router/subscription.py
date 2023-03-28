from fastapi import APIRouter, Depends, status, HTTPException
from stripe.error import InvalidRequestError

from app.logger import log
from app.dependency import get_current_coach
from app.dependency.controller import get_stripe
from app.config import get_settings, Settings
import app.model as m
import app.schema as s


from app.database import get_db


subscription_router = APIRouter(prefix="/subscription", tags=["Subscription"])


@subscription_router.post(
    "/coach/create", status_code=status.HTTP_200_OK, response_model=s.CheckoutSession
)
def create_coach_subscription(
    coach: m.Coach = Depends(get_current_coach),
    db=Depends(get_db),
    settings: Settings = Depends(get_settings),
    stripe=Depends(get_stripe),
):
    if not coach.stripe_customer_id:
        try:
            customer = stripe.Customer.create(
                email=coach.email, name=f"{coach.first_name} {coach.last_name}"
            )
        except InvalidRequestError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Error while creating customer",
            )
        coach.stripe_customer_id = customer.id
        log(log.INFO, "Coach [%s] created a stripe customer", coach.email)
        db.commit()
    if coach.subscription:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Coach already owns this subscription",
        )

    subscription_product: m.StripeProduct = (
        db.query(m.StripeProduct)
        .filter_by(stripe_product_id=settings.COACH_SUBSCRIPTION_PRODUCT_ID)
        .first()
    )
    if not subscription_product:
        log(log.INFO, "Subscription product not found")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    try:
        checkout_session = stripe.checkout.Session.create(
            customer=coach.stripe_customer_id,
            # http://localhost:3000/profiles/coach?my_appointments#success
            success_url="https://findmycoach.co.uk/profiles/coach?my_appointments#success",
            cancel_url="https://findmycoach.co.uk/profiles/coach?my_appointments#cancel",
            line_items=[
                {
                    "price": subscription_product.price.stripe_price_id,
                    "quantity": 1,
                },
            ],
            mode="subscription",
        )
    except InvalidRequestError as e:
        log(log.ERROR, "Error while creating a checkout session - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error while creating a checkout session",
        )
    log(log.INFO, "URL:[%s]", checkout_session.url)
    return s.CheckoutSession(url=checkout_session.url)
