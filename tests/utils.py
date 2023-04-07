from random import randint, choice
from datetime import datetime, timedelta


from sqlalchemy.orm import Session

import app.model as m
from tests.fixture import TestData

SPORTS_TYPES = [
    "Football",
    "Cricket",
    "Tennis",
    "Yoga",
    "Rugby",
    "Fitness",
    "Golf",
    "Swimming",
]


def create_upcoming_student_lesson(
    db, student_id: int, schedule_id: int, coach_id: int
):
    student_lesson = (
        db.query(m.StudentLesson)
        .filter_by(student_id=student_id, schedule_id=schedule_id)
        .first()
    )
    if not student_lesson:
        student_lesson = m.StudentLesson(
            schedule_id=schedule_id,
            coach_id=coach_id,
            student_id=student_id,
            appointment_time=datetime.now() + timedelta(days=1),
            created_at=datetime.now() + timedelta(days=1),
        )
        db.add(student_lesson)
    db.commit()
    return student_lesson


def create_past_student_lesson(db, student_id: int, schedule_id: int, coach_id: int):
    student_lesson = (
        db.query(m.StudentLesson)
        .filter_by(student_id=student_id, schedule_id=schedule_id)
        .first()
    )
    if not student_lesson:
        student_lesson = m.StudentLesson(
            schedule_id=schedule_id,
            student_id=student_id,
            coach_id=coach_id,
            appointment_time=datetime.now() - timedelta(days=1),
            created_at=datetime.now() - timedelta(days=1),
        )
        db.add(student_lesson)
    db.commit()
    return student_lesson


def create_coach_subscription(db: Session, test_data: TestData):
    product = db.query(m.StripeProduct).first()
    if not product:
        exit()
    coach = (
        db.query(m.Coach)
        .filter_by(email=test_data.test_authorized_coaches[0].email)
        .first()
    )
    db.add(
        m.CoachSubscription(
            coach_id=coach.id,
            stripe_subscription_id="sub_test",
            product_id=product.id,
            current_period_end=(datetime.now() + timedelta(days=30)).timestamp(),
            current_period_start=(datetime.now()).timestamp(),
            created=datetime.now().timestamp(),
            status=m.SubscriptionStatus.ACTIVE.value,
            is_active=True,
        )
    )
    db.commit()


def fill_db_by_test_data(db: Session, test_data: TestData):
    print("Filling up db with fake data")

    for sport_type in SPORTS_TYPES:
        if not db.query(m.SportType).filter_by(name=sport_type).first():
            db.add(m.SportType(name=sport_type))
            db.commit()
    for location in test_data.test_locations:
        if (
            not db.query(m.Location)
            .filter_by(city=location.city, street=location.street)
            .first()
        ):
            db.add(
                m.Location(
                    name=location.name,
                    city=location.city,
                    street=location.street,
                    postal_code=location.postal_code,
                )
            )
            db.commit()

    locations = db.query(m.Location).all()
    price = m.StripeProductPrice(
        stripe_price_id=test_data.test_subscription_price.stripe_price_id,
        currency=test_data.test_subscription_price.currency,
        created=datetime.now().timestamp(),
        unit_amount=test_data.test_subscription_price.unit_amount,
    )
    db.add(price)
    db.flush()
    db.refresh(price)
    db.add(
        m.StripeProduct(
            stripe_product_id=test_data.test_subscription_product.stripe_product_id,
            price_id=price.id,
            name=test_data.test_subscription_product.name,
            description=test_data.test_subscription_product.description,
            created=datetime.now().timestamp(),
        )
    )
    db.commit()

    for c in test_data.test_coaches:
        coach = db.query(m.Coach).filter_by(email=c.email).first()
        if not coach:
            db.add(m.Coach(**c.dict()))
            db.commit()

        # creating lesson for coaches
        coach: m.Coach = db.query(m.Coach).filter_by(email=c.email).first()
        if not db.query(m.Lesson).filter_by(coach_id=coach.id).first():
            lesson = m.Lesson(
                coach_id=coach.id,
                location_id=randint(1, len(locations)),
            )
            db.add(lesson)
            db.commit()
        if not coach.sports:
            sport = (
                db.query(m.SportType)
                .filter_by(id=randint(1, len(SPORTS_TYPES)))
                .first()
            )
            coach_sport = m.CoachSport(
                coach_id=coach.id,
                sport_id=sport.id,
            )
            db.add(coach_sport)
            db.flush()
        if not coach.locations:
            locations = db.query(m.Location).all()
            for _ in range(1, 3):
                coach_location = m.CoachLocation(
                    coach_id=coach.id, location_id=randint(1, len(locations))
                )
                db.add(coach_location)
        if not db.query(m.Lesson).filter_by(coach_id=coach.id).first():
            lesson = m.Lesson(
                coach_id=coach.id,
                location_id=choice([location.id for location in coach.locations]),
                sport_type_id=choice([sport.id for sport in coach.sports]),
            )
            db.add(lesson)
            db.flush()
        if not db.query(m.CoachSchedule).filter_by(coach_id=coach.id).first():
            for _ in range(1, 5):
                schedule = m.CoachSchedule(
                    coach_id=coach.id,
                    lesson_id=choice([lesson.id for lesson in coach.lessons]),
                    start_datetime=datetime.now() + timedelta(days=1),
                    end_datetime=datetime.now()
                    + timedelta(days=1, hours=randint(1, 3)),
                )
                db.add(schedule)
        db.commit()

    for s in test_data.test_students:
        if not db.query(m.Student).filter_by(email=s.email).first():
            db.add(m.Student(**s.dict()))
            db.commit()
    for auth_coach in test_data.test_authorized_coaches:
        if not db.query(m.Coach).filter_by(email=auth_coach.email).first():
            db.add(m.Coach(**auth_coach.dict()))
            db.commit()
            coach: m.Coach = db.query(m.Coach).filter_by(email=auth_coach.email).first()

            if not coach.sports:
                for _ in range(1, 3):
                    sport = (
                        db.query(m.SportType)
                        .filter_by(id=randint(1, len(SPORTS_TYPES)))
                        .first()
                    )
                    coach_sport = m.CoachSport(
                        coach_id=coach.id,
                        sport_id=sport.id,
                    )
                    db.add(coach_sport)
                    db.flush()
            db.commit()
            if not coach.locations:
                locations = db.query(m.Location).all()
                for _ in range(1, 3):
                    coach_location = m.CoachLocation(
                        coach_id=coach.id, location_id=randint(1, len(locations))
                    )
                    db.add(coach_location)
                db.commit()
            if not db.query(m.Lesson).filter_by(coach_id=coach.id).first():
                lesson = m.Lesson(
                    coach_id=coach.id,
                    location_id=choice([location.id for location in coach.locations]),
                    sport_type_id=choice([sport.id for sport in coach.sports]),
                )
                db.add(lesson)
                db.flush()
            db.commit()
            if not db.query(m.CoachSchedule).filter_by(coach_id=coach.id).first():
                for _ in range(1, 5):
                    schedule = m.CoachSchedule(
                        coach_id=coach.id,
                        lesson_id=choice([lesson.id for lesson in coach.lessons]),
                        start_datetime=datetime.now() + timedelta(days=1),
                        end_datetime=datetime.now()
                        + timedelta(days=1, hours=randint(1, 3)),
                    )
                    db.add(schedule)
            db.commit()

    for auth_student in test_data.test_authorized_students:
        if not db.query(m.Student).filter_by(email=auth_student.email).first():
            db.add(m.Student(**auth_student.dict()))
            db.commit()
    create_coach_subscription(db=db, test_data=test_data)
