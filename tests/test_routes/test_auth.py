from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.controller import MailClient
from app.config import Settings
import app.model as m
import app.schema as s
from tests.conftest import get_test_settings
from tests.fixture import TestData


settings: Settings = get_test_settings()


def test_signup_and_confirm_account_student(
    client: TestClient,
    test_data: TestData,
    db: Session,
    mail_client: MailClient,
):
    with mail_client.mail.record_messages() as outbox:
        request_data = s.UserSignUp(
            email=test_data.test_student.email,
            password=test_data.test_student.password,
            username=test_data.test_student.username,
        ).dict()
        response = client.post("api/auth/student/sign-up", json=request_data)
        assert response
        assert len(outbox) == 1
    student = db.query(m.Student).filter_by(email=test_data.test_student.email).first()
    assert student
    assert not student.is_verified
    old_token = student.verification_token
    response = client.get(
        f"api/auth/student/account-confirmation?token={student.verification_token}"
    )
    assert response
    student = db.query(m.Student).filter_by(email=test_data.test_student.email).first()
    assert student
    assert student.is_verified
    assert student.verification_token != old_token


def test_signup_and_confirm_account_coach(
    client: TestClient,
    test_data: TestData,
    db: Session,
    mail_client: MailClient,
):
    with mail_client.mail.record_messages() as outbox:
        request_data = s.UserSignUp(
            email=test_data.test_coach.email,
            password=test_data.test_coach.password,
            username=test_data.test_coach.username,
        ).dict()
        response = client.post("api/auth/coach/sign-up", json=request_data)
        assert response
        assert len(outbox) == 1
    coach = db.query(m.Coach).filter_by(email=test_data.test_coach.email).first()
    assert coach
    assert not coach.is_verified
    old_token = coach.verification_token

    response = client.get(
        f"api/auth/coach/account-confirmation?token={coach.verification_token}"
    )
    assert response
    coach = db.query(m.Coach).filter_by(email=test_data.test_coach.email).first()
    assert coach
    assert coach.is_verified
    assert coach.verification_token != old_token


def test_forgot_password_coach(
    client: TestClient,
    db: Session,
    test_data: TestData,
    mail_client: MailClient,
):
    coach: m.Coach | None = (
        db.query(m.Coach).filter_by(email=test_data.test_coaches[0].email).first()
    )

    assert coach

    old_password = coach.password
    assert coach
    with mail_client.mail.record_messages() as outbox:
        request_data = s.UserEmail(email=coach.email).dict()
        response = client.post("api/auth/coach/forgot-password", json=request_data)
        assert response
        assert len(outbox) == 1
        coach: m.Coach | None = (
            db.query(m.Coach).filter_by(email=test_data.test_coaches[0].email).first()
        )
        assert coach
        assert coach.password != old_password

    old_token = coach.verification_token
    TEST_NEW_PASSWORD = "test_new_password"

    # confirm the new password
    request_data = s.UserResetPassword(
        password=TEST_NEW_PASSWORD, password1=TEST_NEW_PASSWORD
    ).dict()
    response = client.post(
        f"api/auth/coach/reset-password/{coach.verification_token}", json=request_data
    )
    assert response
    coach: m.Coach | None = (
        db.query(m.Coach).filter_by(email=test_data.test_coaches[0].email).first()
    )
    assert coach
    assert coach.verification_token != old_token


def test_forgot_password_student(
    client: TestClient,
    db: Session,
    test_data: TestData,
    mail_client: MailClient,
):
    student: m.Student | None = (
        db.query(m.Student).filter_by(email=test_data.test_students[0].email).first()
    )

    assert student

    old_password = student.password
    assert student
    with mail_client.mail.record_messages() as outbox:
        request_data = s.UserEmail(email=student.email).dict()
        response = client.post("api/auth/student/forgot-password", json=request_data)
        assert response
        assert len(outbox) == 1
        student: m.Student | None = (
            db.query(m.Student)
            .filter_by(email=test_data.test_students[0].email)
            .first()
        )
        assert student
        assert student.password != old_password

    old_token = student.verification_token
    TEST_NEW_PASSWORD = "test_new_password"

    # confirm the new password
    request_data = s.UserResetPassword(
        password=TEST_NEW_PASSWORD, password1=TEST_NEW_PASSWORD
    ).dict()
    response = client.post(
        f"api/auth/student/reset-password/{student.verification_token}",
        json=request_data,
    )
    assert response
    student: m.Student | None = (
        db.query(m.Student).filter_by(email=test_data.test_students[0].email).first()
    )
    assert student
    assert student.verification_token != old_token


def test_whoami_routes(
    client: TestClient,
    authorized_coach_tokens: list,
    authorized_student_tokens: list,
):
    client.headers[
        "Authorization"
    ] = f"Bearer {authorized_coach_tokens[0].access_token}"
    response = client.get("api/whoami/student")
    assert response.status_code == 200

    client.headers[
        "Authorization"
    ] = f"Bearer {authorized_coach_tokens[0].access_token}"
    response = client.get("api/whoami/coach")
    assert response.status_code == 200
