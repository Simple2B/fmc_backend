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
    request_data = s.BaseSchedule(
        location_id=1,
        week_day=m.WeekDay.FRIDAY.value,
        begin_hours=18,
        begin_minutes=30,
    ).dict()
    response = client.post(
        "/api/schedule/create",
        json=request_data,
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response
    assert db.query(m.CoachSchedule).count()

    # making sure we cannot create a new schedule with the same time
    response = client.post(
        "/api/schedule/create",
        json=request_data,
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
    assert resp_obj.uuid == db.query(m.CoachSchedule).first().uuid

    # deleting schedule
    response = client.delete(
        f"/api/schedule/{resp_obj.uuid}",
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response.status_code == 200
    assert not db.query(m.CoachSchedule).all()
