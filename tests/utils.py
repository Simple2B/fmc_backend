from random import randint
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


def create_upcoming_student_lesson(db, student_id: int, lesson_id: int):
    student_lesson = (
        db.query(m.StudentLesson)
        .filter_by(student_id=student_id, lesson_id=lesson_id)
        .first()
    )
    if not student_lesson:
        student_lesson = m.StudentLesson(
            lesson_id=lesson_id,
            student_id=student_id,
            appointment_time=datetime.now() + timedelta(days=1),
            date=datetime.now() + timedelta(days=1),
        )
        db.add(student_lesson)
    db.commit()
    return student_lesson


def create_past_student_lesson(db, student_id: int, lesson_id: int):
    student_lesson = (
        db.query(m.StudentLesson)
        .filter_by(student_id=student_id, lesson_id=lesson_id)
        .first()
    )
    if not student_lesson:
        student_lesson = m.StudentLesson(
            lesson_id=lesson_id,
            student_id=student_id,
            appointment_time=datetime.now() - timedelta(days=1),
            date=datetime.now() - timedelta(days=1),
        )
        db.add(student_lesson)
    db.commit()
    return student_lesson


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
    sports = db.query(m.SportType).all()

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
                sport_type_id=randint(1, len(sports)),
            )
            db.add(lesson)
            db.commit()

    for s in test_data.test_students:
        if not db.query(m.Student).filter_by(email=s.email).first():
            db.add(m.Student(**s.dict()))
            db.commit()
    for auth_coach in test_data.test_authorized_coaches:
        if not db.query(m.Coach).filter_by(email=auth_coach.email).first():
            db.add(m.Coach(**auth_coach.dict()))
            db.commit()
    for auth_student in test_data.test_authorized_students:
        if not db.query(m.Student).filter_by(email=auth_student.email).first():
            db.add(m.Student(**auth_student.dict()))
            db.commit()
