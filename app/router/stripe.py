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


@stripe_router.post("/student/reserve", status_code=status.HTTP_201_CREATED)
def reserve_booking(
    schedule_uuids: list[str] | None = Query(None),
    db=Depends(get_db),
    student: m.Student = Depends(get_current_student),
    settings: Settings = Depends(get_settings),
    stripe=Depends(get_stripe),
):
    schedules: list[m.CoachSchedule] = (
        db.query(m.CoachSchedule).filter(m.CoachSchedule.uuid.in_(schedule_uuids)).all()
    )
    if not schedules:
        log(log.INFO, "No schedules with such uuid`s was found")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Schedules was not found"
        )
    # check if anyone has already purchased appointment for this schedules
    coach_uuid = schedules[0].coach.uuid
    for schedule in schedules:
        if (
            db.query(m.StudentLesson)
            .filter_by(schedule_id=schedule.id, student_id=student.id)
            .first()
        ):
            log(log.INFO, "This schedule has been booked")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot book this appointment",
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
        db.commit()
    log(log.INFO, "Student [%s] created as a stripe customer", student.email)
    total_price = sum([schedule.lesson.price for schedule in schedules])

    checkout = stripe.checkout.Session.create(
        success_url=f"{settings.BASE_URL}/coach_search/{coach_uuid}#success",
        cancel_url=f"{settings.BASE_URL}/coach_search/{coach_uuid}#cancel",
        customer=student.stripe_customer_id,
        line_items=[
            {
                "price_data": {
                    "currency": "gbp",
                    "unit_amount": total_price,
                    "product_data": {
                        "name": "Test appointment",
                    },
                },
                "quantity": 1,
            },
        ],
        payment_intent_data={
            "metadata": {
                "schedules": ",".join(
                    map(str, [schedule.uuid for schedule in schedules])
                ),
                "student_uuid": student.uuid,
            },
        },
        mode="payment",
    )
    log(log.INFO, "Checkout url generated - [%s]", checkout.url)
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

    if event.type == "payment_intent.succeeded":
        # Processing the successful purchase of appointments
        data = event["data"]["object"]
        schedule_uuids = data.metadata["schedules"].split(",")
        schedules = (
            db.query(m.CoachSchedule)
            .filter(m.CoachSchedule.uuid.in_(schedule_uuids))
            .all()
        )
        student = (
            db.query(m.Student).filter_by(uuid=data.metadata["student_uuid"]).first()
        )

        for schedule in schedules:
            schedule = db.query(m.CoachSchedule).get(schedule.id)
            schedule.is_booked = True

            student_lesson = m.StudentLesson(
                student_id=student.id,
                schedule_id=schedule.id,
                coach_id=schedule.coach.id,
                appointment_time=schedule.start_datetime,
            )
            db.add(student_lesson)
            db.commit()
        log(log.INFO, "Created [%d] appointments", len(schedules))
        log(log.INFO, "Schedule - [%s] is now booked", schedule.uuid)
        return status.HTTP_200_OK
