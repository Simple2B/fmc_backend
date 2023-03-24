from typing import Generator
from invoke import task
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db, Session
import app.model as m
from app.logger import log

db: Session = get_db().__next__()

TEST_EMAIL = "user1@gmail.com"
TEST_PASSWORD = "user1"
TEST_FIRSTNAME = "John"
TEST_LASTNAME = "Doe"

TEST_NEWSLETTER_NUMBER_TODAYS_NEW = 5
TEST_NEWSLETTER_NUMBER_YESTERDAY_ACTIVE = 7


@task
def create_dummy_coach(_):
    test_coach = db.query(m.Coach).filter_by(email=TEST_EMAIL).first()
    if not test_coach:
        test_coach = m.Coach(
            email=TEST_EMAIL,
            password=TEST_PASSWORD,
            username=TEST_EMAIL,
            first_name=TEST_FIRSTNAME,
            last_name=TEST_LASTNAME,
            is_verified=True,
        )
        db.add(test_coach)
        db.commit()


@task
def create_dummy_student(_):
    test_student = db.query(m.Student).filter_by(email=TEST_EMAIL).first()
    if not test_student:
        test_student = m.Student(
            email=TEST_EMAIL,
            password=TEST_PASSWORD,
            username=TEST_EMAIL,
            first_name=TEST_FIRSTNAME,
            last_name=TEST_LASTNAME,
            is_verified=True,
        )
        db.add(test_student)
        db.commit()


def create_footbal_coach():
    FOOTBALL_COACH_EMAIL = "mourinho@gmail.com"
    football_coach = db.query(m.Coach).filter_by(email=FOOTBALL_COACH_EMAIL).first()
    if not football_coach:
        football_coach = m.Coach(
            first_name="Jose",
            last_name="Mourinho",
            username="FootballCoach",
            email=FOOTBALL_COACH_EMAIL,
            password="password",
            is_verified=True,
        )
        db.add(football_coach)
        db.commit()
        sport_id: int = db.query(m.SportType).first().id

        fc_sport = m.CoachSport(coach_id=football_coach.id, sport_id=sport_id)
        db.add(fc_sport)
        db.commit()
        log(log.INFO, f"Coach {football_coach} created successfully")
    return football_coach


def create_boxing_coach():
    BOXING_COACH_EMAIL = "tyson@gmail.com"
    boxing_coach = db.query(m.Coach).filter_by(email=BOXING_COACH_EMAIL).first()
    if not boxing_coach:
        boxing_coach = m.Coach(
            first_name="Michael",
            last_name="Tyson",
            username="BoxingCoach",
            email=BOXING_COACH_EMAIL,
            password="password",
            is_verified=True,
        )
        db.add(boxing_coach)
        db.commit()
        sport_id: int = db.query(m.SportType).first().id
        bc_sport = m.CoachSport(coach_id=boxing_coach.id, sport_id=sport_id)
        db.add(bc_sport)
        db.commit()
        log(log.INFO, f"Coach {boxing_coach} created successfully")
    return db.query(m.Coach).filter_by(email=BOXING_COACH_EMAIL).first()


def create_dummy_locations():
    locations = db.query(m.Location).all()
    if not locations:
        locations = [
            m.Location(
                name="São Paulo Sport Hall",
                address_line_1="Rua São Paulo",
                address_line_2="123",
            ),
            m.Location(
                name="Rio de Janeiro Sport Hall",
                address_line_1="Rua São Paulo",
                address_line_2="124",
            ),
            m.Location(
                name="Rio de Janeiro Sport Hall #2",
                address_line_1="Rua São Paulo",
                address_line_2="125",
            ),
            m.Location(
                name="Rio de Janeiro Sport Hall #3",
                address_line_1="Rua São Paulo",
                address_line_2="126",
            ),
        ]
        db.add_all(locations)
        try:
            db.commit()
        except SQLAlchemyError:
            pass
        log(log.INFO, "Locations created successfully")
    return locations


def create_dummy_students():
    students = db.query(m.Student).all()
    if not students:
        students = [
            m.Student(
                first_name="John",
                last_name="Doe",
                username="johndoe",
                email="user1@gmail.com",
                password="user1",
                is_verified=True,
            ),
            m.Student(
                first_name="Jane",
                last_name="Doe",
                username="janedoe",
                email="janedoe@gmail.com",
                password="password",
                is_verified=True,
            ),
        ]
        db.add_all(students)
        try:
            db.commit()
        except SQLAlchemyError:
            pass
        log(log.INFO, "Students created successfully")
    return students


def gen_number_emails(num_emails: int) -> Generator[str, None, None]:
    from faker import Faker

    fake = Faker()

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
    create_footbal_coach()
    create_boxing_coach()
    # create_dummy_locations()
    create_dummy_students()
    create_dummy_newsletter_subscriptions()

    # todo create lessons
