from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config import Settings
import app.model as m
import app.schema as s
from tests.conftest import get_test_settings
from tests.fixture import TestData


settings: Settings = get_test_settings()


def test_get_profile(
    client: TestClient,
    test_data: TestData,
    db: Session,
    authorized_student_tokens: list,
    authorized_coach_tokens: list,
):
    # getting coach profile
    client.headers[
        "Authorization"
    ] = f"Bearer {authorized_coach_tokens[0].access_token}"
    response = client.get("/api/profile/coach/")
    assert response
    resp_obj = s.UserProfile.parse_obj(response.json())
    coach = (
        db.query(m.Coach).filter_by(email="test_authorized_coach1@gmail.com").first()
    )
    assert coach
    assert coach.email == resp_obj.email
    # getting student profile
    client.headers[
        "Authorization"
    ] = f"Bearer {authorized_coach_tokens[0].access_token}"
    response = client.get("/api/profile/student/")
    assert response
    resp_obj = s.UserProfile.parse_obj(response.json())
    student = (
        db.query(m.Student)
        .filter_by(email="test_authorized_student1@gmail.com")
        .first()
    )
    assert student
    assert student.email == resp_obj.email


def test_get_api_keys(
    client: TestClient,
):
    response = client.get("/api/keys/")
    assert response.status_code == 200
