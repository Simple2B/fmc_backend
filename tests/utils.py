from sqlalchemy.orm import Session

import app.model as m
from tests.fixture import TestData


def fill_db_by_test_data(db: Session, test_data: TestData):
    print("Filling up db with fake data")
    for u in test_data.test_users:
        if not db.query(m.User).filter_by(email=u.email).first():
            db.add(m.User(**u.dict()))
    db.commit()
