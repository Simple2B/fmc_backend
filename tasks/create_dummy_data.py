import random
from datetime import datetime, timedelta
from typing import Generator

from invoke import task
from faker import Faker

from app.config import Settings, get_settings
from app.database import get_db, Session
import app.model as m
from app.logger import log

db: Session = get_db().__next__()
settings: Settings = get_settings()
fake = Faker()
SPORTS: list[m.SportType] = db.query(m.SportType).all()

TEST_COACH_EMAIL = "coach1@gmail.com"
TEST_COACH_TWO_EMAIL = "coach2@gmail.com"
TEST_STUDENT_EMAIL = "student1@gmail.com"
TEST_PASSWORD = "password"

TEST_EMAIL = "user1@gmail.com"
TEST_PASSWORD = "user1"

TEST_FIRSTNAME = "John"
TEST_LASTNAME = "Doe"

TEST_NEWSLETTER_NUMBER_TODAYS_NEW = 5
TEST_NEWSLETTER_NUMBER_YESTERDAY_ACTIVE = 7


def create_dummy_locations():
    locations = db.query(m.Location).all()
    if not locations:
        for _ in range(1, 100):
            location = m.Location(
                city=fake.city(),
                street=fake.street_name(),
                postal_code=fake.postcode(),
            )
            db.add(location)
        db.commit()
    log(log.INFO, "Created [%d] locations", db.query(m.Location).count())


def create_dummy_coach():
    """We can authorize with this coach"""
    test_coach = db.query(m.Coach).filter_by(email=TEST_COACH_EMAIL).first()
    if not test_coach:
        test_coach = m.Coach(
            email=TEST_COACH_EMAIL,
            password=TEST_PASSWORD,
            username=TEST_COACH_EMAIL,
            first_name=TEST_FIRSTNAME,
            last_name=TEST_LASTNAME,
            is_verified=True,
            profile_picture="https://find-my-coach-eu.s3.eu-west-2.amazonaws.com/assets/test_coach_avatar.png",
        )
        db.add(test_coach)

        db.flush()
        coach_sport = m.CoachSport(
            coach_id=test_coach.id,
            sport_id=random.randint(1, len(SPORTS)),
            price=2000,
        )
        db.add(coach_sport)

    db.commit()


def create_second_dummy_coach():
    """We can authorize with this coach"""
    test_coach = db.query(m.Coach).filter_by(email=TEST_COACH_TWO_EMAIL).first()
    if not test_coach:
        test_coach = m.Coach(
            email=TEST_COACH_TWO_EMAIL,
            password=TEST_PASSWORD,
            username=TEST_COACH_TWO_EMAIL,
            first_name=TEST_FIRSTNAME,
            last_name=TEST_LASTNAME,
            is_verified=True,
        )
        db.add(test_coach)
        coach_sport = m.CoachSport(
            coach_id=test_coach.id,
            sport_id=random.randint(1, len(SPORTS)),
            price=2000,
        )
        db.add(coach_sport)
    db.commit()
    print(f"{TEST_COACH_TWO_EMAIL} created")


def create_dummy_student():
    """We can authorize with this student"""
    test_student = db.query(m.Student).filter_by(email=TEST_STUDENT_EMAIL).first()
    if not test_student:
        test_student = m.Student(
            email=TEST_STUDENT_EMAIL,
            password=TEST_PASSWORD,
            username=TEST_STUDENT_EMAIL,
            first_name=TEST_FIRSTNAME,
            last_name=TEST_LASTNAME,
            is_verified=True,
        )
        db.add(test_student)
        db.commit()


def create_dummy_coaches():
    locations = db.query(m.Location).all()
    sports = db.query(m.SportType).all()
    for _ in range(1, 200):
        if not db.query(m.Coach).filter_by(email=fake.email()).first():
            coach = m.Coach(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                username=fake.user_name(),
                profile_picture=settings.DEFAULT_AVATAR_URL,
                about=fake.sentence(),
                password_hash=fake.email(),
                is_for_adults=random.choice([True, False]),
                is_for_children=random.choice([True, False]),
            )
            db.add(coach)
            db.flush()
        # attaching sport to coach
        coach_sport = m.CoachSport(
            coach_id=coach.id,
            sport_id=random.randint(1, len(sports)),
        )
        db.add(coach_sport)
        # creating couple locations for the coach
        for _ in range(random.randint(0, 3)):
            coach_location = m.CoachLocation(
                coach_id=coach.id,
                location_id=random.randint(
                    1,
                    len(locations),
                ),
            )
            db.add(coach_location)
    db.commit()
    log(log.INFO, "Created [%d] coaches", db.query(m.Coach).count())


def create_dummy_students():
    for _ in range(0, 300):
        if not db.query(m.Student).filter_by(email=fake.email()).first():
            student = m.Student(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                username=fake.user_name(),
                profile_picture=settings.DEFAULT_AVATAR_URL,
                password_hash=fake.email(),
            )
            db.add(student)
        db.commit()
    log(log.INFO, "Created [%d] students", db.query(m.Student).count())


def create_dummy_coach_lessons():
    # TODO

    coaches = db.query(m.Coach).all()
    locations = db.query(m.Location).all()
    sports = db.query(m.SportType).all()
    for _ in range(0, 50):
        coach_lesson = m.Lesson(
            coach_id=random.randint(1, len(coaches)),
            location_id=random.randint(1, len(locations)),
            sport_type_id=random.randint(1, len(sports)),
        )
        db.add(coach_lesson)
    db.commit()
    log(log.INFO, "Created [%d] coach lessons", len(db.query(m.Lesson).all()))


def create_lessons():
    students = db.query(m.Student).all()
    coach_lessons = db.query(m.Lesson).all()
    for _ in range(0, 200):
        lesson = m.StudentLesson(
            student_id=random.randint(1, len(students)),
            lesson_id=random.randint(1, len(coach_lessons)),
            appointment_time=fake.date_between(
                start_date=datetime.now() - timedelta(days=5),
                end_date=datetime.now() + timedelta(days=7),
            ),
        )
        db.add(lesson)
        db.flush()
    db.commit()
    log(log.INFO, "Created [%d] lessons", db.query(m.StudentLesson).all())


def create_dummy_messages():
    coaches = db.query(m.Coach).all()
    students = db.query(m.Student).all()
    for _ in range(0, 100):
        author_id: str = db.query(m.Coach).get(random.randint(1, len(coaches))).uuid
        receiver_id: str = (
            db.query(m.Student).get(random.randint(1, len(students))).uuid
        )
        message = m.Message(
            text=fake.sentence(),
            author_id=author_id,
            receiver_id=receiver_id,
        )
        db.add(message)
    db.flush()
    for _ in range(0, 100):
        author_id: str = db.query(m.Student).get(random.randint(1, len(students))).uuid
        receiver_id: str = db.query(m.Coach).get(random.randint(1, len(coaches))).uuid
        message = m.Message(
            text=fake.sentence(),
            author_id=author_id,
            receiver_id=receiver_id,
        )
        db.add(message)
    db.commit()
    log(log.INFO, "Created [%d] messages", db.query(m.Message).count())


def create_fake_reviews():
    # TODO
    ...


def gen_number_emails(num_emails: int) -> Generator[str, None, None]:
    DOMAINS = ("com", "com.br", "net", "net.br", "org", "org.br", "gov", "gov.br")

    for _ in range(num_emails):
        # Primary name
        first_name = fake.first_name()

        # Secondary name
        last_name = fake.last_name()

        company = fake.company().split()[0].strip(",")

        # Company DNS
        dns_org = fake.random_choices(elements=DOMAINS, length=1)[0]

        # email formatting
        yield f"{first_name}.{last_name}@{company}.{dns_org}".lower()


def create_dummy_newsletter_subscriptions(db: Session = db):
    from datetime import timedelta, datetime

    if db.query(m.NewsletterSubscription).count():
        log(log.INFO, "Newsletter Subscriptions already present")
        return
    db.add_all(
        [
            m.NewsletterSubscription(email=email)
            for email in gen_number_emails(TEST_NEWSLETTER_NUMBER_TODAYS_NEW)
        ]
        + [
            m.NewsletterSubscription(
                email=email,
                state=m.NewsletterSubscription.State.ACTIVE,
                created_at=(datetime.now() - timedelta(days=1)),
            )
            for email in gen_number_emails(TEST_NEWSLETTER_NUMBER_YESTERDAY_ACTIVE)
        ]
    )
    db.commit()
    log(log.INFO, "Newsletter Subscriptions created successfully")


@task
def dummy_data(_):
    # locations
    create_dummy_locations()
    # users
    create_dummy_coach()
    create_second_dummy_coach()
    create_dummy_student()
    create_dummy_coaches()
    create_dummy_students()

    # coach lessons
    create_dummy_coach_lessons()
    # just lessons
    create_lessons()
    create_dummy_messages()

    create_dummy_newsletter_subscriptions()
