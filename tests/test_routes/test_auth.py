from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.controller import MailClient
from app.config import Settings
import app.model as m
import app.schema as s
from tests.conftest import get_test_settings
from tests.fixture import TestData


settings: Settings = get_test_settings()


def test_signup_student(
    client: TestClient,
    test_data: TestData,
    db: Session,
):
    request_data = s.UserSignUp(
        email=test_data.test_student.email, password=test_data.test_student.password
    ).dict()
    response = client.post("api/auth/student/sign-up", json=request_data)
    assert response
    assert db.query(m.Student).filter_by(email=test_data.test_student.email).first()


def test_signup_coach(
    client: TestClient,
    test_data: TestData,
    db: Session,
):
    request_data = s.UserSignUp(
        email=test_data.test_coach.email, password=test_data.test_coach.password
    ).dict()
    response = client.post("api/auth/coach/sign-up", json=request_data)
    assert response
    assert db.query(m.Coach).filter_by(email=test_data.test_coach.email).first()


def test_login(client: TestClient, db: Session, test_data: TestData):
    ...


def test_mail(mail_client: MailClient):
    with mail_client.mail.record_messages():
        ...
