from datetime import datetime, timedelta

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import app.model as m
import app.schema as s
from tests.fixture import TestData


def test_schedule(
    client: TestClient,
    test_data: TestData,
    db: Session,
    authorized_coach_tokens,
):
    # creating a new schedule for coach
    coach = (
        db.query(m.Coach)
        .filter_by(email=test_data.test_authorized_coaches[0].email)
        .first()
    )
    lesson = db.query(m.Lesson).filter_by(coach_id=coach.id).first()
    request_data = s.BaseSchedule(
        lesson_id=lesson.id,
        start_datetime=datetime.now() + timedelta(days=1),
        end_datetime=datetime.now() + timedelta(days=1, hours=2),
    )
    response = client.post(
        "/api/schedule/create",
        json=jsonable_encoder(request_data),
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response
    assert db.query(m.CoachSchedule).count()

    # making sure we cannot create a new schedule with the same time
    response = client.post(
        "/api/schedule/create",
        json=jsonable_encoder(request_data),
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert not response.status_code == 200
    # getting list of coach schedules
    response = client.get(
        "/api/schedule/schedules",
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response.status_code == 200
    resp_obj = s.ScheduleList.parse_obj(response.json())
    assert db.query(m.CoachSchedule).filter_by(uuid=resp_obj.schedules[0].uuid).first()

    # getting single schedule by uuid
    response = client.get(
        f"/api/schedule/{resp_obj.schedules[0].uuid}",
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response.status_code == 200
    resp_obj = s.Schedule.parse_obj(response.json())
    assert (
        resp_obj.uuid
        == db.query(m.CoachSchedule).filter_by(uuid=resp_obj.uuid).first().uuid
    )

    # editing schedule
    coach_schedule = (
        db.query(m.CoachSchedule)
        .join(m.Coach)
        .filter(m.Coach.email == test_data.test_authorized_coaches[0].email)
        .first()
    )
    request_data = s.BaseSchedule(
        lesson_id=coach_schedule.lesson.id,
        start_datetime=datetime.now() + timedelta(days=2),
        end_datetime=datetime.now() + timedelta(days=2, hours=1),
    )
    response = client.put(
        f"/api/schedule/{coach_schedule.uuid}",
        json=jsonable_encoder(request_data),
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response.status_code == 201
    # deleting schedule
    response = client.delete(
        f"/api/schedule/{resp_obj.uuid}",
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response.status_code == 200
    assert not db.query(m.CoachSchedule).filter_by(uuid=resp_obj.uuid).first()
