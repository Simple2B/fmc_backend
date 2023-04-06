from fastapi import APIRouter, Depends, Query, Request, Header, HTTPException, status
from sqlalchemy.orm import Session
from stripe.error import InvalidRequestError

from app.dependency.controller import get_stripe
from app.dependency.user import get_current_student
from app.logger import log
from app.config import get_settings, Settings
import app.model as m
import app.schema as s


from app.database import get_db


stripe_router = APIRouter(prefix="/stripe", tags=["Stripe"])


@stripe_router.get("/coach/products", response_model=s.Product)
def get_coach_stripe_product(
    db=Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    return (
        db.query(m.StripeProduct)
        .filter_by(stripe_product_id=settings.COACH_SUBSCRIPTION_PRODUCT_ID)
        .first()
    )


@stripe_router.post("/student/reserve")
def reserve_booking(
    schedule_uuids: list[int] | None = Query(None),
    db=Depends(get_db),
    student: m.Student = Depends(get_current_student),
    settings: Settings = Depends(get_settings),
    stripe=Depends(get_stripe),
):
    schedules: list[m.CoachSchedule] = (
        db.query(m.CoachSchedule).filter(m.CoachSchedule.uuid.in_(schedule_uuids)).all()
    )
    if not schedules:
        raise HTTPException(
            status=status.HTTP_409_CONFLICT, detail="Schedules was not found"
        )
    if not student.stripe_customer_id:
        try:
            customer = stripe.Customer.create(
                email=student.email, name=f"{student.first_name} {student.last_name}"
            )
        except InvalidRequestError as e:
            log(log.INFO, "Error creating student - customer - [%s]", e)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Error while creating student - customer",
            )
        student.stripe_customer_id = customer.id
        log(log.INFO, "Student [%s] created as a stripe customer", student.email)
        db.commit()

    # pass list of uuids to metadata in order to handle multiple schedule
    checkout = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[
            {
                "name": "Test appointment",
                "images": [
                    settings.DEFAULT_AVATAR_URL,
                ],
                "amount": 19999,
                "currency": "usd",
                "quantity": 1,
            }
        ],
        payment_intent_data={
            "metadata": {"test_data": "some really test data"},
        },
        mode="payment",
    )
    return checkout.url


@stripe_router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db),
    stripe_signature: str = Header(None),
    settings: Settings = Depends(get_settings),
    stripe=Depends(get_stripe),
):
    data = await request.body()
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
    if event.type == "checkout.session.completed":
        data = event["data"]["object"]
        print(data)
