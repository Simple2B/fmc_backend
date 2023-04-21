from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import app.model as m
import app.schema as s
from tests.fixture import TestData


def test_packages(
    client: TestClient,
    test_data: TestData,
    db: Session,
    authorized_student_tokens,
    authorized_coach_tokens,
):
    coach = (
        db.query(m.Coach)
        .filter_by(email=test_data.test_authorized_coaches[0].email)
        .first()
    )
    assert coach
    request_data = s.BaseLesson(
        title="Package #1",
        location=coach.locations[0],
        sport=coach.sports[0],
        price=29.99,
        max_people=5,
        about="Cool package",
    ).dict()

    response = client.post(
        "/api/package/create",
        json=request_data,
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response.status_code == 201
    coach = (
        db.query(m.Coach)
        .filter_by(email=test_data.test_authorized_coaches[0].email)
        .first()
    )
    assert coach
    assert db.query(m.Lesson).filter_by(coach_id=coach.id).first()

    response = client.get(
        "/api/package/packages",
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response.status_code == 201
    resp_obj = s.LessonList.parse_obj(response.json())
    assert resp_obj.lessons
    response = client.get(
        f"/api/package/packages/{coach.uuid}",
    )
    assert response.status_code == 201
    resp_obj = s.LessonList.parse_obj(response.json())
    assert resp_obj.lessons

    # getting single package
    package_uuid = resp_obj.lessons[0].uuid
    response = client.get(
        f"/api/package/{package_uuid}",
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response.status_code == 201
    resp_obj = s.Lesson.parse_obj(response.json())
    assert resp_obj.uuid == package_uuid
