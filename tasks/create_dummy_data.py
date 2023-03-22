import random
from datetime import datetime, timedelta
from invoke import task
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db, Session
import app.model as m

db: Session = get_db().__next__()

SPORTS: list[m.SportType] = db.query(m.SportType).all()

TEST_COACH_EMAIL = "coach1@gmail.com"
TEST_COACH_TWO_EMAIL = "coach2@gmail.com"
TEST_STUDENT_EMAIL = "student1@gmail.com"
TEST_PASSWORD = "password"
TEST_FIRSTNAME = "John"
TEST_LASTNAME = "Doe"


def create_dummy_coach():
    test_coach = db.query(m.Coach).filter_by(email=TEST_COACH_EMAIL).first()
    if not test_coach:
        test_coach = m.Coach(
            email=TEST_COACH_EMAIL,
            password=TEST_PASSWORD,
            username=TEST_COACH_EMAIL,
            first_name=TEST_FIRSTNAME,
            last_name=TEST_LASTNAME,
            is_verified=True,
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
        fc_sport = m.CoachSport(coach_id=football_coach.id, sport_id=SPORTS[0].id)
        db.add(fc_sport)
        db.commit()
        print(f"Coach {football_coach} created successfully")
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
        bc_sport = m.CoachSport(coach_id=boxing_coach.id, sport_id=SPORTS[0].id)
        db.add(bc_sport)
        db.commit()
        print(f"Coach {boxing_coach} created successfully")
    return db.query(m.Coach).filter_by(email=BOXING_COACH_EMAIL).first()


def create_dummy_locations():
    locations = db.query(m.Location).all()
    if not locations:
        locations = [
            m.Location(
                name="São Paulo Sport Hall",
                city="Rua São Paulo",
                street="123",
            ),
            m.Location(
                name="Rio de Janeiro Sport Hall",
                city="Rua São Paulo",
                street="124",
            ),
            m.Location(
                name="Rio de Janeiro Sport Hall #2",
                city="Rua São Paulo",
                street="125",
            ),
        ]
        db.add_all(locations)
        try:
            db.commit()
        except SQLAlchemyError:
            pass
        print("Locations created successfully")
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
        print("Students created successfully")
    return students


def create_dummy_lesson():
    coach = db.query(m.Coach).filter_by(email=TEST_COACH_EMAIL).first()
    location = db.query(m.Location).first()
    lesson = db.query(m.Lesson).first()
    student = db.query(m.Student).filter_by(email=TEST_STUDENT_EMAIL).first()
    if not lesson:
        lesson = m.Lesson(
            coach_id=coach.id,
            location_id=location.id,
            sport_type_id=random.randint(1, len(SPORTS)),
        )
        db.add(lesson)
        db.commit()
    student_lesson = m.StudentLesson(
        student_id=student.id,
        lesson_id=lesson.id,
        appointment_time=(datetime.now() + timedelta(days=1)),
        date=datetime.now() + timedelta(days=1),
    )
    db.add(student_lesson)
    db.commit()


def create_dummy_messages():
    coach = db.query(m.Coach).filter_by(email=TEST_COACH_EMAIL).first()
    student = db.query(m.Student).filter_by(email=TEST_STUDENT_EMAIL).first()
    # creating dumme messages
    message_one = m.Message(
        receiver_id=coach.uuid, author_id=student.uuid, text="Hey,whats up buddy !"
    )
    db.add(message_one)
    message_two = m.Message(
        receiver_id=student.uuid, author_id=coach.uuid, text="I`m good,thanks !"
    )
    db.add(message_two)

    second_coach = db.query(m.Coach).filter_by(email=TEST_COACH_TWO_EMAIL).first()
    message_three = m.Message(
        receiver_id=student.uuid, author_id=second_coach.uuid, text="Hey buddy"
    )
    db.add(message_three)
    db.commit()
    print("Messages created")


@task
def dummy_data(_):
    # users
    create_dummy_coach()
    create_second_dummy_coach()
    create_dummy_student()

    create_dummy_locations()
    create_footbal_coach()
    create_boxing_coach()
    create_dummy_students()
    # lesson
    create_dummy_lesson()
    create_dummy_messages()


# todo create lessons
