import random
from datetime import datetime, timedelta
from typing import Generator

from sqlalchemy.exc import SQLAlchemyError
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
            try:
                db.flush()
            except SQLAlchemyError:
                db.rollback()
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
            try:
                db.flush()
            except SQLAlchemyError:
                db.rollback()
    db.commit()
    log(log.INFO, "Created [%d] coaches", db.query(m.Coach).count())


def create_dummy_students():
    if db.query(m.Student).count() < 100:
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
                try:
                    db.flush()
                except SQLAlchemyError:
                    db.rollback()
    db.commit()
    log(log.INFO, "Created [%d] students", db.query(m.Student).count())


def create_dummy_coach_lessons():
    coaches = db.query(m.Coach).all()
    for coach in coaches:
        sport_ids = [sport.id for sport in coach.sports]
        location_ids = [location.id for location in coach.locations]
        if location_ids:
            for _ in range(1, 10):
                coach_lesson = m.Lesson(
                    coach_id=random.randint(1, len(coaches)),
                    location_id=random.choice(location_ids),
                    sport_type_id=random.choice(sport_ids),
                )
                db.add(coach_lesson)
                try:
                    db.flush()
                except SQLAlchemyError:
                    db.rollback()
    db.commit()

    log(log.INFO, "Created [%d] coach lessons", db.query(m.Lesson).count())


def create_lessons():
    students = db.query(m.Student).all()
    coaches = db.query(m.Coach).all()
    for coach in coaches:
        for _ in range(10, 25):
            coach_lessons_ids = [lesson.id for lesson in coach.lessons]
            if coach_lessons_ids:
                lesson = m.StudentLesson(
                    student_id=random.randint(1, len(students)),
                    lesson_id=random.choice(coach_lessons_ids),
                    appointment_time=fake.date_between(
                        start_date=datetime.now() - timedelta(days=5),
                        end_date=datetime.now() + timedelta(days=7),
                    ),
                )
                db.add(lesson)
            try:
                db.flush()
            except SQLAlchemyError:
                db.rollback()
    db.commit()
    log(log.INFO, "Created [%d] lessons", db.query(m.StudentLesson).count())


def create_dummy_messages():
    lessons = db.query(m.StudentLesson).all()
    for lesson in lessons:
        author = db.query(m.Coach).filter_by(id=lesson.coach.id).first()
        receiver = db.query(m.Student).filter_by(id=lesson.student_id).first()
        message = m.Message(
            text=fake.sentence(),
            author_id=author.uuid,
            receiver_id=receiver.uuid,
        )
        db.add(message)
        db.flush()
    for lesson in lessons:
        author = db.query(m.Student).filter_by(id=lesson.student_id).first()
        receiver = db.query(m.Coach).filter_by(id=lesson.coach.id).first()
        message = m.Message(
            text=fake.sentence(),
            author_id=author.uuid,
            receiver_id=receiver.uuid,
        )
        db.add(message)
        db.flush()
    db.commit()
    log(log.INFO, "Created [%d] messages", db.query(m.Message).count())


def create_fake_reviews():
    student_lessons = db.query(m.StudentLesson).count()
    coach = db.query(m.Coach).count()
    for _ in range(0, 500):
        db.add(
            m.LessonReview(
                student_lesson_id=random.randint(1, student_lessons),
                coach_id=random.randint(1, coach),
                text=fake.sentence(),
                rate=random.randint(1, 5),
            )
        )
        try:
            db.flush()
        except SQLAlchemyError:
            db.rollback()
    db.commit()
    log(log.INFO, "Reviews created [%d]", db.query(m.LessonReview).count())


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


def create_dummy_schedules():
    coaches = db.query(m.Coach).all()
    for coach in coaches:
        location_ids = [location.id for location in coach.locations]
        if location_ids:
            for _ in range(0, 4):
                coach_schedule = m.CoachSchedule(
                    coach_id=coach.id,
                    location_id=random.choice(location_ids),
                    begin_hours=random.randint(0, 60),
                    begin_minutes=random.randint(0, 60),
                )
                db.add(coach_schedule)
            db.flush()
    db.commit()
    log(log.INFO, "Created - [%d] schedules", db.query(m.CoachSchedule).count())


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
    create_fake_reviews()
    create_dummy_newsletter_subscriptions()
    create_dummy_schedules()


@task
def create_sessions(_):
    """Create sessions between known users"""
    student = db.query(m.Student).filter_by(email=TEST_STUDENT_EMAIL).first()
    coach = db.query(m.Coach).filter_by(email=TEST_COACH_EMAIL).first()
    coach_lessons_ids = [
        lesson.id for lesson in db.query(m.Lesson).filter_by(coach_id=coach.id).all()
    ]
    for _ in range(0, 200):
        start_date = datetime.now() - timedelta(days=5)
        end_date = datetime.now() + timedelta(days=14)
        db.add(
            m.StudentLesson(
                student_id=student.id,
                lesson_id=random.randint(1, len(coach_lessons_ids)),
                appointment_time=fake.date_between(
                    start_date=start_date, end_date=end_date
                ),
            )
        )
    db.commit()
    log(
        log.INFO,
        "Session created for [%s] -:[%d]",
        TEST_STUDENT_EMAIL,
        db.query(m.StudentLesson).filter_by(student_id=student.id).count(),
    )
