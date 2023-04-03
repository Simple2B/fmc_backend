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
