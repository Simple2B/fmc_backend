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


def fill_db_by_test_data(db: Session, test_data: TestData):
    print("Filling up db with fake data")
    for c in test_data.test_coaches:
        if not db.query(m.Coach).filter_by(email=c.email).first():
            db.add(m.Coach(**c.dict()))
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
    for sport_type in SPORTS_TYPES:
        if not db.query(m.SportType).filter_by(name=sport_type).first():
            db.add(m.SportType(name=sport_type))
            db.commit()
