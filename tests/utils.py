from sqlalchemy.orm import Session

import app.model as m
from tests.fixture import TestData


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
