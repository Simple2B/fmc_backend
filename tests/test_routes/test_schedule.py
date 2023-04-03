from datetime import datetime, timedelta

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
        notes="Test notes",
        week_day=m.CoachSchedule.WeekDay.friday.value,
        begin=(datetime.now() + timedelta(hours=1)).time().strftime("%H:%M"),
        end=(datetime.now() + timedelta(hours=2)).time().strftime("%H:%M"),
    ).dict()
    response = client.post(
        "/api/schedule/create",
        json=request_data,
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response
    assert db.query(m.CoachSchedule).count()

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
