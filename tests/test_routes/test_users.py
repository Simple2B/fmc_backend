from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from moto import mock_s3


from app.config import Settings
from app.dependency import get_s3_conn
import app.model as m
import app.schema as s
from app.hash_utils import make_hash, hash_verify
from tests.conftest import get_test_settings
from tests.fixture import TestData


settings: Settings = get_test_settings()


def test_get_profile(
    client: TestClient,
    db: Session,
    authorized_coach_tokens: list,
):
    # getting coach profile
    response = client.get(
        "/api/profile/info/coach",
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response
    resp_obj = s.Coach.parse_obj(response.json())
    coach = (
        db.query(m.Coach).filter_by(email="test_authorized_coach1@gmail.com").first()
    )
    assert coach
    assert coach.email == resp_obj.email

    # getting student profile
    response = client.get(
        "/api/profile/student",
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response
    resp_obj = s.BaseUser.parse_obj(response.json())
    student = (
        db.query(m.Student)
        .filter_by(email="test_authorized_student1@gmail.com")
        .first()
    )
    assert student
    assert student.email == resp_obj.email

    # getting subscription for coach
    response = client.get(
        "api/profile/coach/subscription",
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response.status_code == 200
    resp_obj = s.Subscription.parse_obj(response.json())
    subscription = db.query(m.CoachSubscription).first()
    assert subscription
    assert resp_obj.stripe_subscription_id == subscription.stripe_subscription_id

    # # get all coaches cards
    # response = client.get(
    #     "api/profile/coach/profiles/cards",
    # )
    # assert response.status_code == 200
    # resp_obj = s.CoachList.parse_obj(response.json())
    # assert (
    #     len(resp_obj.coaches) == db.query(m.Coach).filter_by(is_verified=True).count()
    # )


@mock_s3
def test_save_personal_info(
    client: TestClient,
    test_data: TestData,
    db: Session,
    authorized_coach_tokens: list,
    authorized_student_tokens: list,
):
    TEST_FIRST_NAME = "John"
    TEST_LAST_NAME = "Doe"
    # creating a bucket
    s3 = get_s3_conn(settings)
    s3.create_bucket(Bucket=settings.AWS_S3_BUCKET_NAME)

    # upload image for coach
    response = client.post(
        "api/profile/coach/personal-info",
        data=dict(
            first_name=TEST_FIRST_NAME,
            last_name=TEST_LAST_NAME,
        ),
        files={
            "file": open("tests/avatar_test.jpg", "rb"),
        },
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response
    coach = (
        db.query(m.Coach)
        .filter_by(email=test_data.test_authorized_coaches[0].email)
        .first()
    )
    assert coach
    assert coach.first_name == TEST_FIRST_NAME
    file_path = s3.list_objects_v2(Bucket=settings.AWS_S3_BUCKET_NAME)["Contents"][0][
        "Key"
    ]
    # checking if path to profile image is correct
    assert coach.profile_picture == f"{settings.AWS_S3_BUCKET_URL}{file_path}"

    # upload image for student
    response = client.post(
        "api/profile/student/personal-info",
        data=dict(
            first_name=TEST_FIRST_NAME,
            last_name=TEST_LAST_NAME,
        ),
        files={
            "file": open("tests/avatar_test.jpg", "rb"),
        },
        headers={
            "Authorization": f"Bearer {authorized_student_tokens[0].access_token}"
        },
    )
    assert response
    student = (
        db.query(m.Student)
        .filter_by(email=test_data.test_authorized_students[0].email)
        .first()
    )
    assert student
    assert student.first_name == "John"
    file_path = s3.list_objects_v2(Bucket=settings.AWS_S3_BUCKET_NAME)["Contents"][1][
        "Key"
    ]
    # checking if path to profile image is correct
    assert student.profile_picture == f"{settings.AWS_S3_BUCKET_URL}{file_path}"


def test_get_api_keys(
    client: TestClient,
):
    response = client.get("/api/keys/google")
    assert response.status_code == 200


def test_change_profile_password(
    client: TestClient,
    test_data: TestData,
    db: Session,
    authorized_coach_tokens: list,
):
    TEST_NEW_PASSWORD = "NEW_PASSWORD"
    # Changing coache`s password
    coach = (
        db.query(m.Coach)
        .filter_by(email=test_data.test_authorized_coaches[0].email)
        .first()
    )
    assert coach
    old_password: str = coach.password
    request_data = s.ProfileChangePasswordIn(
        old_password=test_data.test_authorized_coaches[0].password,
        new_password=TEST_NEW_PASSWORD,
        new_password_confirmation=TEST_NEW_PASSWORD,
    ).dict()
    response = client.post(
        "api/profile/coach/change-password",
        json=request_data,
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response.status_code == 200

    assert old_password != make_hash(TEST_NEW_PASSWORD)
    coach = (
        db.query(m.Coach)
        .filter_by(email=test_data.test_authorized_coaches[0].email)
        .first()
    )
    assert coach
    assert hash_verify(TEST_NEW_PASSWORD, coach.password)
