from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from moto import mock_s3


from app.config import Settings
from app.controller import create_s3_conn
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


@mock_s3
def test_save_image_to_profile(
    client: TestClient,
    test_data: TestData,
    db: Session,
    authorized_coach_tokens: list,
):
    s3 = create_s3_conn(settings)
    s3.create_bucket(Bucket=settings.AWS_S3_BUCKET_NAME)
    client.headers[
        "Authorization"
    ] = f"Bearer {authorized_coach_tokens[0].access_token}"
    response = client.post(
        "api/profile/coach/upload-image",
        files={
            "file": (
                "avatar_test.jpg",
                open("tests/avatar_test.jpg", "rb"),
                "image/jpeg",
            )
        },
    )
    assert response
    coach = (
        db.query(m.Coach)
        .filter_by(email=test_data.test_authorized_coaches[0].email)
        .first()
    )
    assert coach
    file_path = s3.list_objects_v2(Bucket=settings.AWS_S3_BUCKET_NAME)["Contents"][0][
        "Key"
    ]
    # checking if path to profile image is correct
    assert coach.profile_picture == f"{settings.AWS_S3_BUCKET_URL}{file_path}"
